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
    const bettingActions = gameState.actions.filter(
      (action) => action.type === "bet" || action.type === "raise"
    );
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
    setter: React.Dispatch<React.SetStateAction<number>>,
    value: number
  ) => {
    setter((prev) => prev + BIG_BLIND_SIZE);
  };

  const decrementAmount = (
    setter: React.Dispatch<React.SetStateAction<number>>,
    value: number
  ) => {
    setter((prev) => Math.max(BIG_BLIND_SIZE, prev - BIG_BLIND_SIZE));
  };

  return (
    <div className="flex flex-col space-y-4">
      <div className="flex space-x-2">
        <Button
          onClick={() => handleAction("fold")}
          disabled={isLoading}
          variant="destructive"
        >
          Fold
        </Button>

        <Button
          onClick={() => handleAction("check")}
          disabled={isLoading || !canCheck}
          variant="outline"
        >
          Check
        </Button>

        <Button
          onClick={() => handleAction("call")}
          disabled={isLoading || !canCall}
          variant="outline"
        >
          Call
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <Button
          onClick={() => handleAction("bet", betAmount)}
          disabled={isLoading || !canBet}
          variant="secondary"
        >
          Bet {betAmount}
        </Button>

        <Button
          onClick={() => decrementAmount(setBetAmount, betAmount)}
          disabled={isLoading || !canBet || betAmount <= BIG_BLIND_SIZE}
          variant="outline"
          size="icon"
        >
          -
        </Button>

        <Button
          onClick={() => incrementAmount(setBetAmount, betAmount)}
          disabled={isLoading || !canBet}
          variant="outline"
          size="icon"
        >
          +
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <Button
          onClick={() => handleAction("raise", raiseAmount)}
          disabled={isLoading || !canRaise}
          variant="secondary"
        >
          Raise {raiseAmount}
        </Button>

        <Button
          onClick={() => decrementAmount(setRaiseAmount, raiseAmount)}
          disabled={
            isLoading || !canRaise || raiseAmount <= lastBet + BIG_BLIND_SIZE
          }
          variant="outline"
          size="icon"
        >
          -
        </Button>

        <Button
          onClick={() => incrementAmount(setRaiseAmount, raiseAmount)}
          disabled={isLoading || !canRaise}
          variant="outline"
          size="icon"
        >
          +
        </Button>
      </div>

      <Button
        onClick={() => handleAction("allin")}
        disabled={isLoading}
        variant="default"
      >
        ALLIN
      </Button>
    </div>
  );
};

export default ActionControls;
