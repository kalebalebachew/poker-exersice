"use client";

import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { usePoker } from "../contexts/PokerContext";
import { formatCards, formatActionForLog } from "../utils/poker";
import { Action } from "../services/api";

const PlayingField = () => {
  const {
    gameState,
    stackSize,
    setStackSize,
    startNewGame,
    resetGame,
    isLoading,
  } = usePoker();
  const [logEntries, setLogEntries] = useState<string[]>([]);

  // Add log entries when actions are performed
  useEffect(() => {
    if (gameState && gameState.actions.length > 0) {
      const lastAction = gameState.actions[gameState.actions.length - 1];
      const playerIndex =
        lastAction.player !== undefined ? lastAction.player : 0;
      const logEntry = formatActionForLog(lastAction, playerIndex);
      setLogEntries((prev) => [...prev, logEntry]);
    }
  }, [gameState?.actions.length]);

  const handleStackChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value > 0) {
      setStackSize(value);
    }
  };

  const handleReset = () => {
    resetGame();
    setLogEntries([]);
  };

  const handleStart = () => {
    startNewGame();
    setLogEntries([]);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Playing field log</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center space-x-4 mb-4">
          <div className="flex items-center space-x-2">
            <span>Stacks</span>
            <Input
              type="number"
              value={stackSize}
              onChange={handleStackChange}
              className="w-24"
              min={1}
            />
          </div>
          <Button
            onClick={gameState ? handleReset : handleStart}
            disabled={isLoading}
            variant="outline"
          >
            {gameState ? "Reset" : "Start"}
          </Button>
        </div>

        {gameState && (
          <div className="space-y-2">
            {/* Player information */}
            {gameState.stacks.map((stack, index) => (
              <div key={index} className="text-sm">
                Player {index + 1} is dealt{" "}
                {formatCards(gameState.player_cards[index.toString()])}
              </div>
            ))}

            {/* Positions */}
            <div className="text-sm">
              Player {gameState.positions.dealer + 1} is the dealer
              {gameState.positions.sb !== undefined && (
                <span>
                  , Player {gameState.positions.sb + 1} is Small blind
                </span>
              )}
              {gameState.positions.bb !== undefined && (
                <span>, Player {gameState.positions.bb + 1} is Big blind</span>
              )}
            </div>

            {/* Log entries */}
            {logEntries.map((entry, index) => (
              <div key={index} className="text-sm">
                {entry}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default PlayingField;
