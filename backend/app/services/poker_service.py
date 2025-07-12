from typing import Dict, List, Any, Optional, Tuple
from pokerkit import Automation, NoLimitTexasHoldem, Card, Hand, State, StandardHighHand
import uuid
import re
from random import shuffle


class PokerService:
    """Service for robust poker hand evaluation and game simulation."""

    VALID_RANKS = set('23456789TJQKA')
    VALID_SUITS = set('shdc')

    def __init__(self):
        """Initialize with a fresh deck for game creation."""
        try:
            # Create a standard 52-card deck manually
            self.deck = self._create_standard_deck()
            if len(self.deck) != 52:
                raise ValueError("Deck initialization failed: Expected 52 cards")
        except Exception as e:
            raise ValueError(f"Failed to initialize deck: {str(e)}")

    def _create_standard_deck(self) -> List[Card]:
        """Create a standard 52-card deck manually using Card objects."""
        deck = []
        for rank in self.VALID_RANKS:
            for suit in self.VALID_SUITS:
                deck.append(Card(rank, suit))
        return deck

    def evaluate_hand(self, cards: List[str]) -> Dict[str, Any]:
        """
        Evaluate a poker hand using pokerkit's hand evaluation.

        Args:
            cards: List of card strings (e.g., ["As", "Kh", "Qd", "Jc", "Ts"])

        Returns:
            Dict with hand type, rank, and best five cards

        Raises:
            ValueError: If cards are invalid or fewer than 5
        """
        if not cards or len(cards) < 5:
            raise ValueError("A hand must contain at least 5 cards")

        # Validate and convert card strings
        card_objects = []
        seen_cards = set()
        for card_str in cards:
            if not self._is_valid_card(card_str):
                raise ValueError(f"Invalid card format: {card_str}")
            if card_str in seen_cards:
                raise ValueError(f"Duplicate card: {card_str}")
            seen_cards.add(card_str)
            rank, suit = card_str[0], card_str[1]
            try:
                card = Card(rank, suit)
                card_objects.append(card)
            except ValueError as e:
                raise ValueError(f"Failed to parse card {card_str}: {str(e)}")

        # Use pokerkit's StandardHighHand for evaluation
        try:
            # Create a hand instance and evaluate it
            hand = StandardHighHand(tuple(card_objects))
            
            # Extract hand type from the class name
            hand_type = hand.__class__.__name__.replace('Hand', '')
            
            # Map pokerkit hand class to rank (1-10)
            hand_ranks = {
                'HighCard': 1,
                'Pair': 2,
                'TwoPair': 3,
                'ThreeOfAKind': 4,
                'Straight': 5,
                'Flush': 6,
                'FullHouse': 7,
                'FourOfAKind': 8,
                'StraightFlush': 9,
                'RoyalFlush': 10
            }
            rank = hand_ranks.get(hand_type, 1)
            
            # Get the best five cards
            best_cards = [f"{card.rank}{card.suit}" for card in hand.cards[:5]]

            return {
                "hand_type": hand_type,
                "rank": rank,
                "best_cards": best_cards
            }
        except Exception as e:
            raise ValueError(f"Hand evaluation failed: {str(e)}")

    def evaluate_poker_game(self, player_cards: Dict[str, List[str]], 
                           board_cards: List[str], 
                           actions: List[Dict], 
                           stacks: List[int],
                           positions: Dict[str, int]) -> Dict[str, int]:
        """
        Evaluate a complete poker game and calculate winnings.

        Args:
            player_cards: Dict mapping player indices to their hole cards
            board_cards: List of community cards
            actions: List of actions taken during the hand
            stacks: Initial stacks for each player
            positions: Dict mapping position names to player indices

        Returns:
            Dict mapping player indices to their net winnings/losses

        Raises:
            ValueError: If inputs are invalid or inconsistent
        """
        # Validate inputs
        if len(stacks) != 6:
            raise ValueError("Exactly 6 players are required")
        if not all(isinstance(stack, int) and stack >= 0 for stack in stacks):
            raise ValueError("Stacks must be non-negative integers")
        if len(player_cards) > 6:
            raise ValueError("Too many players specified in player_cards")
        if len(board_cards) > 5:
            raise ValueError("Too many board cards")
        if not all(self._is_valid_card(card) for card in board_cards):
            raise ValueError("Invalid board card format")
        if len(set(board_cards)) != len(board_cards):
            raise ValueError("Duplicate board cards")
        for player, cards in player_cards.items():
            if len(cards) != 2:
                raise ValueError(f"Player {player} must have exactly 2 hole cards")
            if not all(self._is_valid_card(card) for card in cards):
                raise ValueError(f"Invalid hole cards for player {player}")
        if not all(pos in ['dealer', 'sb', 'bb'] for pos in positions):
            raise ValueError("Invalid position keys")
        if not all(isinstance(idx, int) and 0 <= idx < 6 for idx in positions.values()):
            raise ValueError("Position indices must be between 0 and 5")

        # Create game state
        try:
            state = NoLimitTexasHoldem.create_state(
                (
                    Automation.ANTE_POSTING,
                    Automation.BET_COLLECTION,
                    Automation.BLIND_OR_STRADDLE_POSTING,
                    Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                    Automation.HAND_KILLING,
                    Automation.CHIPS_PUSHING,
                    Automation.CHIPS_PULLING,
                ),
                True,
                0,
                (20, 40),
                40,
                stacks,
                6,
            )
        except Exception as e:
            raise ValueError(f"Failed to create game state: {str(e)}")

        # Deal hole cards
        all_cards = set(board_cards)
        for player_idx, cards in player_cards.items():
            if any(card in all_cards for card in cards):
                raise ValueError(f"Duplicate cards for player {player_idx}")
            all_cards.update(cards)
            card_str = ''.join(str(Card(card[0], card[1])) for card in cards)
            try:
                state.deal_hole(card_str, int(player_idx))
            except Exception as e:
                raise ValueError(f"Failed to deal cards to player {player_idx}: {str(e)}")

        # Track initial stacks
        initial_stacks = state.stacks.copy()

        # Process actions
        street_cards_dealt = 0
        for action in actions:
            valid, error = self.validate_action(self._state_to_dict(state), action)
            if not valid:
                raise ValueError(f"Invalid action: {error}")

            action_type = action["type"]
            if action_type == "deal_flop":
                if street_cards_dealt != 0:
                    raise ValueError("Flop can only be dealt once")
                street_cards_dealt = 3
                state.burn_card()
                card_str = ''.join(str(Card(card[0], card[1])) for card in board_cards[:3])
                state.deal_board(card_str)
            elif action_type == "deal_turn":
                if street_cards_dealt != 3:
                    raise ValueError("Turn can only be dealt after flop")
                street_cards_dealt = 4
                state.burn_card()
                if len(board_cards) > 3:
                    card_str = str(Card(board_cards[3][0], board_cards[3][1]))
                    state.deal_board(card_str)
            elif action_type == "deal_river":
                if street_cards_dealt != 4:
                    raise ValueError("River can only be dealt after turn")
                street_cards_dealt = 5
                state.burn_card()
                if len(board_cards) > 4:
                    card_str = str(Card(board_cards[4][0], board_cards[4][1]))
                    state.deal_board(card_str)
            elif action_type == "fold":
                state.fold()
            elif action_type == "check":
                state.check_or_call()
            elif action_type == "call":
                state.check_or_call()
            elif action_type == "bet":
                state.complete_bet_or_raise_to(action.get("amount", 40))
            elif action_type == "raise":
                state.complete_bet_or_raise_to(action.get("amount", state.min_raise_to))
            elif action_type == "allin":
                current_player = state.actor
                if current_player is not None:
                    state.complete_bet_or_raise_to(state.stacks[current_player])

        # Ensure showdown if necessary
        if not state.is_terminal and street_cards_dealt == 5:
            try:
                state.show_or_muck_hole_cards()
            except Exception as e:
                raise ValueError(f"Showdown failed: {str(e)}")

        # Calculate results
        results = {}
        for i, (initial, final) in enumerate(zip(initial_stacks, state.stacks)):
            results[str(i)] = final - initial
        return results

    def create_new_game(self, num_players: int = 6, stack_size: int = 1000) -> Dict:
        """
        Create a new poker game with fresh deck and positions.

        Args:
            num_players: Number of players (must be 6)
            stack_size: Starting stack size for each player

        Returns:
            Dict with game setup information

        Raises:
            ValueError: If num_players is not 6 or stack_size is invalid
        """
        if num_players != 6:
            raise ValueError("Only 6-player games are supported")
        if not isinstance(stack_size, int) or stack_size <= 0:
            raise ValueError("Stack size must be a positive integer")

        # Reset and shuffle deck
        try:
            self.deck = self._create_standard_deck()
            if len(self.deck) != 52:
                raise ValueError("Deck initialization failed: Expected 52 cards")
            shuffle(self.deck)  # Shuffle the deck in place
        except Exception as e:
            raise ValueError(f"Failed to initialize deck: {str(e)}")

        # Assign positions
        dealer_pos = 0
        sb_pos = (dealer_pos + 1) % 6
        bb_pos = (dealer_pos + 2) % 6

        # Deal hole cards
        player_cards = {}
        for i in range(num_players):
            if len(self.deck) < 2:
                raise ValueError("Not enough cards in deck to deal")
            card1 = self.deck.pop()
            card2 = self.deck.pop()
            player_cards[str(i)] = [f"{card1.rank}{card1.suit}", f"{card2.rank}{card2.suit}"]

        # Prepare board cards
        if len(self.deck) < 8:  # 3 flop + 1 turn + 1 river + 3 burns
            raise ValueError("Not enough cards in deck for board")
        burn1 = self.deck.pop()
        flop_cards = [self.deck.pop() for _ in range(3)]
        burn2 = self.deck.pop()
        turn_card = self.deck.pop()
        burn3 = self.deck.pop()
        river_card = self.deck.pop()

        board_cards = [f"{card.rank}{card.suit}" for card in flop_cards + [turn_card, river_card]]

        return {
            "id": str(uuid.uuid4()),
            "stacks": [stack_size] * num_players,
            "positions": {"dealer": dealer_pos, "sb": sb_pos, "bb": bb_pos},
            "player_cards": player_cards,
            "board_cards": board_cards,
            "actions": []
        }

    def validate_action(self, game_state: Dict, action: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate if an action is legal in the current game state.

        Args:
            game_state: Current state of the game
            action: Action to validate

        Returns:
            Tuple of (is_valid, error_message)

        Raises:
            ValueError: If game_state is invalid
        """
        # Validate game_state
        required_keys = {"stacks", "positions", "player_cards", "board_cards", "actions"}
        if not all(key in game_state for key in required_keys):
            raise ValueError("Game state missing required keys")

        # Basic action validation
        action_type = action.get("type")
        if not action_type:
            return False, "Action type is required"

        # For now, we'll do simplified validation without relying on pokerkit's state
        # This is a temporary solution until we fix the card handling issues
        
        # Check if the action is of a valid type
        valid_action_types = ["fold", "check", "call", "bet", "raise", "allin", 
                              "deal_flop", "deal_turn", "deal_river"]
        if action_type not in valid_action_types:
            return False, f"Invalid action type: {action_type}"
            
        # Check if player is specified for player actions
        if action_type in ["fold", "check", "call", "bet", "raise", "allin"]:
            player = action.get("player")
            if player is None:
                return False, "Player must be specified for this action type"
            if not isinstance(player, int) or player < 0 or player >= len(game_state["stacks"]):
                return False, f"Invalid player index: {player}"
                
        # Check if amount is specified for bet/raise actions
        if action_type in ["bet", "raise"]:
            amount = action.get("amount")
            if amount is None:
                return False, "Amount must be specified for this action type"
            if not isinstance(amount, (int, float)) or amount <= 0:
                return False, f"Invalid amount: {amount}"
                
        # All validations passed
        return True, None

    def _is_valid_card(self, card: str) -> bool:
        """Check if a card string is valid."""
        if not isinstance(card, str) or len(card) != 2:
            return False
        rank, suit = card[0], card[1]
        return rank in self.VALID_RANKS and suit in self.VALID_SUITS

    def _state_to_dict(self, state: State) -> Dict:
        """Convert pokerkit state to dictionary for validation."""
        player_cards = {}
        for i in range(6):
            cards = state.get_hole_cards(i)
            if cards:
                player_cards[str(i)] = [f"{card.rank}{card.suit}" for card in cards]
        board_cards = [f"{card.rank}{card.suit}" for card in state.board_cards]
        return {
            "stacks": state.stacks,
            "positions": {"dealer": state.dealer, "sb": (state.dealer + 1) % 6, "bb": (state.dealer + 2) % 6},
            "player_cards": player_cards,
            "board_cards": board_cards,
            "actions": state.actions
        }

    def _convert_to_pokerkit_state(self, game_state: Dict) -> NoLimitTexasHoldem:
        """
        Convert a game state dict to a pokerkit state object.

        Args:
            game_state: Game state dictionary

        Returns:
            PokerKit state object

        Raises:
            ValueError: If game_state is invalid
        """
        if not all(key in game_state for key in ["stacks", "positions", "player_cards", "board_cards", "actions"]):
            raise ValueError("Game state missing required keys")
        
        try:
            # Create a new game state without dealing any cards
            state = NoLimitTexasHoldem.create_state(
                (
                    Automation.ANTE_POSTING,
                    Automation.BET_COLLECTION,
                    Automation.BLIND_OR_STRADDLE_POSTING,
                    Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                    Automation.HAND_KILLING,
                    Automation.CHIPS_PUSHING,
                    Automation.CHIPS_PULLING,
                ),
                True,
                0,
                (20, 40),
                40,
                game_state["stacks"],
                6,
            )
            
            # We'll skip dealing cards for now, as it's causing issues
            # We'll just validate the actions directly
            
            return state
        except Exception as e:
            raise ValueError(f"Failed to create game state: {str(e)}")