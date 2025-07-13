"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { usePoker } from "../contexts/PokerContext";
import { Action } from "../services/api";

const BIG_BLIND_SIZE = 40; // Big blind size is set to 40

const ActionControls = () => {
  const { gameState, performAction, isLoading } = usePoker();
  const [betAmount, setBetAmount] = useState<number>(BIG_BLIND_SIZE);
  const [raiseAmount, setRaiseAmount] = useState<number>(BIG_BLIND_SIZE * 2);

  // Reset bet/raise amounts when game state changes
  useEffect(() => {
    setBetAmount(BIG_BLIND_SIZE);
    setRaiseAmount(BIG_BLIND_SIZE * 2);
  }, [gameState?.id]);

  if (!gameState) {
    return null;
  }

  const currentPlayer = getCurrentPlayer();
  const lastBet = getLastBetAmount();
  const canCheck = lastBet === 0;
  const canCall = lastBet > 0;
  const canBet = lastBet === 0;
  const canRaise = lastBet > 0;

  function getCurrentPlayer(): number {
    // In a real implementation, this would track the current player based on game state
    // For simplicity, we'll assume player 0 is always the current player
    return 0;
  }

  function getLastBetAmount(): number {
    // Find the last bet or raise in the actions
    const bettingActions =
      gameState?.actions.filter(
        (action) => action.type === "bet" || action.type === "raise"
      ) || [];
    if (bettingActions.length === 0) return 0;
    return bettingActions[bettingActions.length - 1].amount || 0;
  }

  const handleAction = (actionType: Action["type"], amount?: number) => {
    const action: Action = { type: actionType };

    if (amount !== undefined) {
      action.amount = amount;
    }

    if (currentPlayer !== undefined) {
      action.player = currentPlayer;
    }

    performAction(action);
  };

  const incrementAmount = (
    setter: React.Dispatch<React.SetStateAction<number>>
  ) => {
    setter((prev) => prev + BIG_BLIND_SIZE);
  };

  const decrementAmount = (
    setter: React.Dispatch<React.SetStateAction<number>>
  ) => {
    setter((prev) => Math.max(BIG_BLIND_SIZE, prev - BIG_BLIND_SIZE));
  };

  return (
    <div className="flex flex-wrap gap-2">
      <Button
        onClick={() => handleAction("fold")}
        disabled={isLoading}
        className="bg-blue-400 hover:bg-blue-500 text-white"
      >
        Fold
      </Button>

      <Button
        onClick={() => handleAction("check")}
        disabled={isLoading || !canCheck}
        className="bg-green-400 hover:bg-green-500 text-white"
      >
        Check
      </Button>

      <Button
        onClick={() => handleAction("call")}
        disabled={isLoading || !canCall}
        className="bg-green-400 hover:bg-green-500 text-white"
      >
        Call
      </Button>

      <Button
        onClick={() => handleAction("bet", betAmount)}
        disabled={isLoading || !canBet}
        className="bg-orange-300 hover:bg-orange-400 text-white"
      >
        Bet {betAmount}
      </Button>

      <Button
        onClick={() => decrementAmount(setBetAmount)}
        disabled={isLoading || !canBet || betAmount <= BIG_BLIND_SIZE}
        variant="outline"
        size="icon"
        className="px-2"
      >
        -
      </Button>

      <Button
        onClick={() => incrementAmount(setBetAmount)}
        disabled={isLoading || !canBet}
        variant="outline"
        size="icon"
        className="px-2"
      >
        +
      </Button>

      <Button
        onClick={() => handleAction("raise", raiseAmount)}
        disabled={isLoading || !canRaise}
        className="bg-orange-300 hover:bg-orange-400 text-white"
      >
        Raise {raiseAmount}
      </Button>

      <Button
        onClick={() => decrementAmount(setRaiseAmount)}
        disabled={
          isLoading || !canRaise || raiseAmount <= lastBet + BIG_BLIND_SIZE
        }
        variant="outline"
        size="icon"
        className="px-2"
      >
        -
      </Button>

      <Button
        onClick={() => incrementAmount(setRaiseAmount)}
        disabled={isLoading || !canRaise}
        variant="outline"
        size="icon"
        className="px-2"
      >
        +
      </Button>

      <Button
        onClick={() => handleAction("allin")}
        disabled={isLoading}
        className="bg-red-500 hover:bg-red-600 text-white"
      >
        ALLIN
      </Button>
    </div>
  );
};

export default ActionControls;
