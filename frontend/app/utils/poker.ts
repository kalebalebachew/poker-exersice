// Card formatting utilities
export const formatCard = (card: string): string => {
  if (!card || card.length !== 2) return card;

  const rank = card[0];
  const suit = card[1];

  // Convert suit to symbol
  let suitSymbol = suit;
  switch (suit.toLowerCase()) {
    case "s":
      suitSymbol = "♠";
      break;
    case "h":
      suitSymbol = "♥";
      break;
    case "d":
      suitSymbol = "♦";
      break;
    case "c":
      suitSymbol = "♣";
      break;
  }

  return `${rank}${suitSymbol}`;
};

export const formatCards = (cards: string[] | undefined): string => {
  if (!cards || cards.length === 0) return "";
  return cards.map(formatCard).join(" ");
};

// Hand type formatting
export const formatHandType = (handType: string): string => {
  switch (handType) {
    case "HighCard":
      return "High Card";
    case "Pair":
      return "Pair";
    case "TwoPair":
      return "Two Pair";
    case "ThreeOfAKind":
      return "Three of a Kind";
    case "Straight":
      return "Straight";
    case "Flush":
      return "Flush";
    case "FullHouse":
      return "Full House";
    case "FourOfAKind":
      return "Four of a Kind";
    case "StraightFlush":
      return "Straight Flush";
    case "RoyalFlush":
      return "Royal Flush";
    default:
      return handType;
  }
};

// Position formatting
export const getPositionName = (
  position: number,
  totalPlayers: number
): string => {
  if (position === 0) return "BTN"; // Button
  if (position === 1) return "SB"; // Small Blind
  if (position === 2) return "BB"; // Big Blind

  // Calculate positions for 6-max table
  if (totalPlayers === 6) {
    if (position === 3) return "UTG"; // Under the Gun
    if (position === 4) return "MP"; // Middle Position
    if (position === 5) return "CO"; // Cut Off
  }

  return `P${position + 1}`;
};

// Action formatting for log
export const formatActionForLog = (
  action: any,
  playerIndex: number
): string => {
  const playerPrefix = `Player ${playerIndex + 1}`;

  switch (action.type) {
    case "fold":
      return `${playerPrefix} folds`;
    case "check":
      return `${playerPrefix} checks`;
    case "call":
      return `${playerPrefix} calls`;
    case "bet":
      return `${playerPrefix} bets ${action.amount}`;
    case "raise":
      return `${playerPrefix} raises to ${action.amount}`;
    case "allin":
      return `${playerPrefix} goes all-in`;
    case "deal_flop":
      return "Flop is dealt";
    case "deal_turn":
      return "Turn is dealt";
    case "deal_river":
      return "River is dealt";
    default:
      return `${playerPrefix} performs unknown action`;
  }
};
