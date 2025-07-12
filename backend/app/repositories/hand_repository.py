"""Repository for poker hands data access."""
import uuid
from typing import List, Optional
from fastapi import Depends
from psycopg2.extras import Json

from app.core.database import get_db_cursor
from app.models.hand import Hand, PokerHand


class HandRepository:
    """Repository for poker hands."""

    def __init__(self):
        """Initialize the repository."""
        self._ensure_tables_exist()

    def _ensure_tables_exist(self):
        """Ensure that the required tables exist."""
        with get_db_cursor() as cursor:
            # Create hands table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hands (
                    id SERIAL PRIMARY KEY,
                    cards TEXT[],
                    hand_type TEXT NOT NULL,
                    rank INTEGER NOT NULL
                )
            """)
            
            # Create poker_hands table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS poker_hands (
                    id TEXT PRIMARY KEY,
                    stacks INTEGER[] NOT NULL,
                    positions JSONB NOT NULL,
                    player_cards JSONB NOT NULL,
                    board_cards TEXT[] NOT NULL,
                    actions JSONB NOT NULL,
                    results JSONB NOT NULL
                )
            """)

    def create_hand(self, hand: Hand) -> Hand:
        """Create a new hand."""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO hands (cards, hand_type, rank)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (hand.cards, hand.hand_type, hand.rank)
            )
            hand.id = cursor.fetchone()["id"]
            return hand

    def get_hand(self, hand_id: int) -> Optional[Hand]:
        """Get a hand by ID."""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, cards, hand_type, rank
                FROM hands
                WHERE id = %s
                """,
                (hand_id,)
            )
            result = cursor.fetchone()
            if result is None:
                return None
            return Hand(
                id=result["id"],
                cards=result["cards"],
                hand_type=result["hand_type"],
                rank=result["rank"]
            )

    def get_all_hands(self) -> List[Hand]:
        """Get all hands."""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, cards, hand_type, rank
                FROM hands
                ORDER BY id DESC
                """
            )
            results = cursor.fetchall()
            return [
                Hand(
                    id=result["id"],
                    cards=result["cards"],
                    hand_type=result["hand_type"],
                    rank=result["rank"]
                )
                for result in results
            ]

    def create_poker_hand(self, poker_hand: PokerHand) -> PokerHand:
        """Create or update a poker hand."""
        if not poker_hand.id:
            poker_hand.id = str(uuid.uuid4())
            
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO poker_hands (id, stacks, positions, player_cards, board_cards, actions, results)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    stacks = EXCLUDED.stacks,
                    positions = EXCLUDED.positions,
                    player_cards = EXCLUDED.player_cards,
                    board_cards = EXCLUDED.board_cards,
                    actions = EXCLUDED.actions,
                    results = EXCLUDED.results
                """,
                (
                    poker_hand.id,
                    poker_hand.stacks,
                    Json(poker_hand.positions),
                    Json(poker_hand.player_cards),
                    poker_hand.board_cards,
                    Json(poker_hand.actions),
                    Json(poker_hand.results)
                )
            )
            return poker_hand

    def get_poker_hand(self, hand_id: str) -> Optional[PokerHand]:
        """Get a poker hand by ID."""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, stacks, positions, player_cards, board_cards, actions, results
                FROM poker_hands
                WHERE id = %s
                """,
                (hand_id,)
            )
            result = cursor.fetchone()
            if result is None:
                return None
            return PokerHand(
                id=result["id"],
                stacks=result["stacks"],
                positions=result["positions"],
                player_cards=result["player_cards"],
                board_cards=result["board_cards"],
                actions=result["actions"],
                results=result["results"]
            )

    def get_all_poker_hands(self) -> List[PokerHand]:
        """Get all poker hands."""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, stacks, positions, player_cards, board_cards, actions, results
                FROM poker_hands
                ORDER BY id DESC
                """
            )
            results = cursor.fetchall()
            return [
                PokerHand(
                    id=result["id"],
                    stacks=result["stacks"],
                    positions=result["positions"],
                    player_cards=result["player_cards"],
                    board_cards=result["board_cards"],
                    actions=result["actions"],
                    results=result["results"]
                )
                for result in results
            ] 
            
    def clear_all_poker_hands(self) -> int:
        """Clear all poker hands from the database.
        
        Returns:
            int: Number of deleted records
        """
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM poker_hands")
            return cursor.rowcount 