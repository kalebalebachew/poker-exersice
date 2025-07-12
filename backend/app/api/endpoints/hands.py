"""API endpoints for poker hands."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.models.hand import Hand, HandCreate, HandResponse, PokerHand, PokerHandCreate, PokerHandResponse
from app.services.poker_service import PokerService
from app.repositories.hand_repository import HandRepository

router = APIRouter()


def get_repository() -> HandRepository:
    """Dependency to get the hand repository."""
    return HandRepository()


def get_poker_service() -> PokerService:
    """Dependency to get the poker service."""
    return PokerService()


@router.post("/hands/", response_model=HandResponse, status_code=status.HTTP_201_CREATED)
async def create_hand(
    hand: HandCreate,
    repository: HandRepository = Depends(get_repository),
    poker_service: PokerService = Depends(get_poker_service)
):
    """
    Create a new poker hand and evaluate it.
    
    This endpoint evaluates a set of cards and returns the hand type and rank.
    The hand is also saved to the database.
    """
    try:
        result = poker_service.evaluate_hand(hand.cards)
        hand_data = Hand(cards=hand.cards, hand_type=result["hand_type"], rank=result["rank"])
        saved_hand = repository.create_hand(hand_data)
        return HandResponse(
            id=saved_hand.id,
            cards=saved_hand.cards,
            hand_type=saved_hand.hand_type,
            rank=saved_hand.rank
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/hands/", response_model=List[HandResponse])
async def get_hands(repository: HandRepository = Depends(get_repository)):
    """
    Get all saved poker hands.
    
    This endpoint returns all previously evaluated poker hands from the database.
    """
    hands = repository.get_all_hands()
    return [
        HandResponse(
            id=hand.id,
            cards=hand.cards,
            hand_type=hand.hand_type,
            rank=hand.rank
        ) for hand in hands
    ]


@router.get("/hands/{hand_id}", response_model=HandResponse)
async def get_hand(
    hand_id: int,
    repository: HandRepository = Depends(get_repository)
):
    """
    Get a specific poker hand by ID.
    
    This endpoint returns a single poker hand from the database.
    """
    hand = repository.get_hand(hand_id)
    if hand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hand with ID {hand_id} not found"
        )
    return HandResponse(
        id=hand.id,
        cards=hand.cards,
        hand_type=hand.hand_type,
        rank=hand.rank
    )


@router.post("/games/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_game(
    poker_service: PokerService = Depends(get_poker_service),
    repository: HandRepository = Depends(get_repository)
):
    """
    Create a new poker game.
    
    This endpoint creates a new poker game with fresh deck and positions.
    """
    try:
        game_dict = poker_service.create_new_game()
        
        # Create a PokerHand object to save to the database
        poker_hand = PokerHand(
            id=game_dict["id"],
            stacks=game_dict["stacks"],
            positions=game_dict["positions"],
            player_cards={int(k): v for k, v in game_dict["player_cards"].items()},
            board_cards=game_dict["board_cards"],
            actions=game_dict["actions"],
            results={}  # Empty results since game is not evaluated yet
        )
        
        # Save the game to the database
        saved_game = repository.create_poker_hand(poker_hand)
        
        # Return the game dictionary
        return game_dict
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/games/evaluate/", response_model=Dict[str, int])
async def evaluate_game(
    game: PokerHandCreate,
    repository: HandRepository = Depends(get_repository),
    poker_service: PokerService = Depends(get_poker_service)
):
    """
    Evaluate a complete poker game and calculate winnings.
    
    This endpoint takes a complete poker game state and calculates the winnings
    for each player. The game is also saved to the database.
    """
    try:
        # Convert player_cards from string keys to int keys for the service
        player_cards_int = {int(k): v for k, v in game.player_cards.items()}
        
        # Evaluate the game
        results = poker_service.evaluate_poker_game(
            player_cards=player_cards_int,
            board_cards=game.board_cards,
            actions=game.actions,
            stacks=game.stacks,
            positions=game.positions
        )
        
        # Create a PokerHand object to save to the database
        poker_hand = PokerHand(
            stacks=game.stacks,
            positions=game.positions,
            player_cards=player_cards_int,
            board_cards=game.board_cards,
            actions=game.actions,
            results=results
        )
        
        # Save the game to the database
        saved_game = repository.create_poker_hand(poker_hand)
        
        return results
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating game: {str(e)}"
        )


@router.get("/games/", response_model=List[PokerHandResponse])
async def get_games(repository: HandRepository = Depends(get_repository)):
    """
    Get all saved poker games.
    
    This endpoint returns all previously played poker games from the database.
    """
    games = repository.get_all_poker_hands()
    return [
        PokerHandResponse(
            id=game.id,
            stacks=game.stacks,
            positions=game.positions,
            player_cards={str(k): v for k, v in game.player_cards.items()},
            board_cards=game.board_cards,
            actions=game.actions,
            results={str(k): v for k, v in game.results.items()}
        ) for game in games
    ]


@router.get("/games/{game_id}", response_model=PokerHandResponse)
async def get_game(
    game_id: str,
    repository: HandRepository = Depends(get_repository)
):
    """
    Get a specific poker game by ID.
    
    This endpoint returns a single poker game from the database.
    """
    game = repository.get_poker_hand(game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    return PokerHandResponse(
        id=game.id,
        stacks=game.stacks,
        positions=game.positions,
        player_cards={str(k): v for k, v in game.player_cards.items()},
        board_cards=game.board_cards,
        actions=game.actions,
        results={str(k): v for k, v in game.results.items()}
    )


@router.post("/games/{game_id}/actions/", response_model=Dict[str, Any])
async def add_action(
    game_id: str,
    action: Dict[str, Any],
    repository: HandRepository = Depends(get_repository),
    poker_service: PokerService = Depends(get_poker_service)
):
    """
    Add an action to an existing poker game.
    
    This endpoint adds a new action to an existing poker game and returns the
    updated game state.
    """
    # Get the existing game
    game = repository.get_poker_hand(game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    
    # Convert to a dict for validation
    game_dict = {
        "id": game.id,
        "stacks": game.stacks,
        "positions": game.positions,
        "player_cards": game.player_cards,
        "board_cards": game.board_cards,
        "actions": game.actions
    }
    
    try:
        # Validate the action
        is_valid, error = poker_service.validate_action(game_dict, action)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error or "Invalid action"
            )
        
        # Add the action to the game
        game.actions.append(action)
        
        # Save the updated game
        repository.create_poker_hand(game)
        
        # Return the updated game state
        return {
            "id": game.id,
            "stacks": game.stacks,
            "positions": game.positions,
            "player_cards": {str(k): v for k, v in game.player_cards.items()},
            "board_cards": game.board_cards,
            "actions": game.actions
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing action: {str(e)}"
        ) 