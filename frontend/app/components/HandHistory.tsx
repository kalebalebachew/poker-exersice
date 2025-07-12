"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { usePoker } from "../contexts/PokerContext";
import { formatCard } from '../utils/poker';

const HandHistory = () => {
  const { handHistories, formatActionShort } = usePoker();

  // Format the action sequence in short format
  const formatActionSequence = (history: any) => {
    return history.actions.map(formatActionShort).join(" ");
  };

  // Format player positions
  const formatPositions = (history: any) => {
    return `Stack ${history.stacks[0]}: Dealer: Player ${
      history.positions.dealer + 1
    }, Player ${history.positions.sb + 1} Small blind, Player ${
      history.positions.bb + 1
    } Big blind`;
  };

  // Format player hands
  const formatHands = (history: any) => {
    return Object.entries(history.player_cards)
      .map(([playerIndex, cards]) => {
        const formattedCards = (cards as string[]).map(formatCard).join('');
        return `Player ${parseInt(playerIndex) + 1}: ${formattedCards}`;
      })
      .join("; ");
  };

  // Format winnings
  const formatWinnings = (history: any) => {
    return Object.entries(history.results)
      .map(([playerIndex, amount]) => {
        return `Player ${parseInt(playerIndex) + 1}: ${
          amount > 0 ? "+" : ""
        }${amount}`;
      })
      .join("; ");
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Hand history</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {handHistories.map((history) => (
            <div key={history.id} className="bg-muted p-4 rounded-md">
              <div className="text-sm font-medium">{history.id}</div>
              <div className="text-sm">{formatPositions(history)}</div>
              <div className="text-sm">Hands: {formatHands(history)}</div>
              <div className="text-sm">
                Actions: {formatActionSequence(history)}
              </div>
              <div className="text-sm">Winnings: {formatWinnings(history)}</div>
            </div>
          ))}

          {handHistories.length === 0 && (
            <div className="text-center text-muted-foreground">
              No hand history yet. Play some hands to see them here.
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default HandHistory;

