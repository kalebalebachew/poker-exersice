import axios, { AxiosError } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_PREFIX = "/api/v1/poker"; // Add the API prefix from backend configuration

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Card {
  rank: string;
  suit: string;
}

export interface HandEvaluation {
  hand_type: string;
  rank: number;
  best_cards: string[];
}

export interface Player {
  index: number;
  stack: number;
  cards?: string[];
}

export interface GameState {
  id: string;
  stacks: number[];
  positions: {
    dealer: number;
    sb: number;
    bb: number;
  };
  player_cards: Record<string, string[]>;
  board_cards: string[];
  actions: Action[];
}

export interface Action {
  type:
    | "fold"
    | "check"
    | "call"
    | "bet"
    | "raise"
    | "allin"
    | "deal_flop"
    | "deal_turn"
    | "deal_river";
  player?: number;
  amount?: number;
}

export interface HandHistory {
  id: string;
  stacks: number[];
  positions: {
    dealer: number;
    sb: number;
    bb: number;
  };
  player_cards: Record<string, string[]>;
  board_cards: string[];
  actions: Action[];
  results: Record<string, number>;
}

// Helper function to handle API errors
const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError;
    if (
      axiosError.response?.data &&
      typeof axiosError.response.data === "object" &&
      "detail" in axiosError.response.data
    ) {
      throw new Error(`API Error: ${axiosError.response.data.detail}`);
    }
  }
  throw new Error(
    `API Error: ${error instanceof Error ? error.message : "Unknown error"}`
  );
};

export const pokerApi = {
  // Hand evaluation
  evaluateHand: async (cards: string[]): Promise<HandEvaluation> => {
    try {
      const response = await api.post(`${API_PREFIX}/hands/`, { cards });
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  // Game state management
  createNewGame: async (
    numPlayers: number = 6,
    stackSize: number = 1000
  ): Promise<GameState> => {
    try {
      // The backend doesn't accept parameters for createNewGame
      // We'll need to modify the game state after creation if we want custom stack sizes
      const response = await api.post(`${API_PREFIX}/games/`);
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  // Game actions
  performAction: async (gameId: string, action: Action): Promise<GameState> => {
    try {
      console.log(`Performing action on game ${gameId}:`, action);
      const response = await api.post(
        `${API_PREFIX}/games/${gameId}/actions/`,
        action
      );
      return response.data;
    } catch (error) {
      console.error("Error performing action:", error);
      return handleApiError(error);
    }
  },

  // Hand history
  getHandHistories: async (): Promise<HandHistory[]> => {
    try {
      const response = await api.get(`${API_PREFIX}/games/`);
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  getHandHistory: async (handId: string): Promise<HandHistory> => {
    try {
      const response = await api.get(`${API_PREFIX}/games/${handId}`);
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },
};

export default pokerApi;
