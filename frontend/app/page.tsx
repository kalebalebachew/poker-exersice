"use client";

import React from "react";
import { PokerProvider } from "./contexts/PokerContext";
import PlayingField from "./components/PlayingField";
import ActionControls from "./components/ActionControls";
import HandHistory from "./components/HandHistory";

export default function Home() {
  return (
    <PokerProvider>
      <div className="h-screen bg-gray-50 p-3 flex flex-col">
        <h1 className="text-xl font-bold mb-2 text-center text-gray-800">
          Poker Game - Kaleb Alebachew
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 flex-grow overflow-hidden">
          <div className="flex flex-col h-full space-y-3">
            <div className="flex-grow overflow-hidden">
              <PlayingField />
            </div>
            <div className="mt-auto">
              <ActionControls />
            </div>
          </div>
          <div className="h-full overflow-hidden">
            <HandHistory />
          </div>
        </div>
      </div>
    </PokerProvider>
  );
}
