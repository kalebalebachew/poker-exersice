"use client";

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import pokerApi, { GameState, Action, HandHistory } from "../services/api";

interface PokerContextType {
  gameState: GameState | null;
  handHistories: HandHistory[];
  isLoading: boolean;
  error: string | null;
  stackSize: number;
  setStackSize: (size: number) => void;
  startNewGame: () => Promise<void>;
  resetGame: () => Promise<void>;
  performAction: (action: Action) => Promise<void>;
  formatActionShort: (action: Action) => string;
}

const defaultGameState: GameState = {
  id: "",
  stacks: [1000, 1000, 1000, 1000, 1000, 1000],
  positions: {
    dealer: 0,
    sb: 1,
    bb: 2,
  },
  player_cards: {},
  board_cards: [],
  actions: [],
};

const PokerContext = createContext<PokerContextType | undefined>(undefined);

export const PokerProvider = ({ children }: { children: ReactNode }) => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [handHistories, setHandHistories] = useState<HandHistory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stackSize, setStackSize] = useState(1000);

  // Debug log API URL
  useEffect(() => {
    console.log("API URL:", process.env.NEXT_PUBLIC_API_URL);
  }, []);

  // Load hand histories on mount
  useEffect(() => {
    const fetchHandHistories = async () => {
      try {
        setIsLoading(true);
        console.log("Fetching hand histories...");
        const histories = await pokerApi.getHandHistories();
        console.log("Hand histories response:", histories);
        setHandHistories(histories);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch hand histories:", err);
        setError("Failed to load hand histories");
      } finally {
        setIsLoading(false);
      }
    };

    fetchHandHistories();
  }, []);

  const startNewGame = async () => {
    try {
      setIsLoading(true);
      console.log("Starting new game...");
      // Create a new game using the API
      const newGame = await pokerApi.createNewGame();
      console.log("New game response:", newGame);

      // Since the backend doesn't accept stack size, we'll modify the returned game state
      if (stackSize !== 1000) {
        newGame.stacks = newGame.stacks.map(() => stackSize);
      }

      setGameState(newGame);
      setError(null);
    } catch (err) {
      console.error("Failed to start new game:", err);
      setError("Failed to start new game");
    } finally {
      setIsLoading(false);
    }
  };

  const resetGame = async () => {
    try {
      setIsLoading(true);
      console.log("Resetting game...");
      // Create a new game using the API
      const newGame = await pokerApi.createNewGame();
      console.log("Reset game response:", newGame);

      // Since the backend doesn't accept stack size, we'll modify the returned game state
      if (stackSize !== 1000) {
        newGame.stacks = newGame.stacks.map(() => stackSize);
      }

      setGameState(newGame);
      setError(null);
    } catch (err) {
      console.error("Failed to reset game:", err);
      setError("Failed to reset game");
    } finally {
      setIsLoading(false);
    }
  };

  const performAction = async (action: Action) => {
    if (!gameState) {
      setError("No active game");
      return;
    }

    try {
      setIsLoading(true);
      console.log(
        `Performing action ${action.type} on game ${gameState.id}...`
      );
      const updatedState = await pokerApi.performAction(gameState.id, action);
      console.log("Action response:", updatedState);
      setGameState(updatedState);

      // If this was the last action and the hand is complete, fetch updated histories
      if (isHandComplete(updatedState)) {
        const histories = await pokerApi.getHandHistories();
        setHandHistories(histories);
      }

      setError(null);
    } catch (err) {
      console.error("Failed to perform action:", err);
      setError("Failed to perform action");
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to check if a hand is complete
  const isHandComplete = (state: GameState): boolean => {
    // A hand is complete when only one player is active or all community cards are dealt and betting is complete
    const activePlayerCount = state.stacks.filter(
      (_, i) => !state.actions.some((a) => a.type === "fold" && a.player === i)
    ).length;

    const allCardsDelt = state.board_cards.length === 5;
    const bettingComplete =
      state.actions.length > 0 &&
      !state.actions.some((a) => ["bet", "raise", "call"].includes(a.type));

    return activePlayerCount === 1 || (allCardsDelt && bettingComplete);
  };

  // Format action for hand history display
  const formatActionShort = (action: Action): string => {
    switch (action.type) {
      case "fold":
        return "f";
      case "check":
        return "x";
      case "call":
        return "c";
      case "bet":
        return `b${action.amount}`;
      case "raise":
        return `r${action.amount}`;
      case "allin":
        return "allin";
      case "deal_flop":
        return gameState?.board_cards.slice(0, 3).join("");
      case "deal_turn":
        return gameState?.board_cards[3] || "";
      case "deal_river":
        return gameState?.board_cards[4] || "";
      default:
        return "";
    }
  };

  return (
    <PokerContext.Provider
      value={{
        gameState,
        handHistories,
        isLoading,
        error,
        stackSize,
        setStackSize,
        startNewGame,
        resetGame,
        performAction,
        formatActionShort,
      }}
    >
      {children}
    </PokerContext.Provider>
  );
};

export const usePoker = () => {
  const context = useContext(PokerContext);
  if (context === undefined) {
    throw new Error("usePoker must be used within a PokerProvider");
  }
  return context;
};
