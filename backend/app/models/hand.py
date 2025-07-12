"""Hand model for the poker application."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pydantic import BaseModel


@dataclass
class Hand:
    """Hand data class for database storage."""
    
    cards: List[str]
    hand_type: str
    rank: int
    id: Optional[int] = None


class HandCreate(BaseModel):
    """Schema for creating a hand."""
    
    cards: List[str]


class HandResponse(BaseModel):
    """Schema for hand response."""
    
    id: Optional[int] = None
    cards: List[str]
    hand_type: str
    rank: int


@dataclass
class PokerHand:
    """Full poker hand data class for database storage."""
    
    id: Optional[str] = None
    stacks: List[int] = field(default_factory=list)
    positions: Dict[str, int] = field(default_factory=dict)
    player_cards: Dict[int, List[str]] = field(default_factory=dict)
    board_cards: List[str] = field(default_factory=list)
    actions: List[Dict] = field(default_factory=list)
    results: Dict[int, int] = field(default_factory=dict)


class PokerHandCreate(BaseModel):
    """Schema for creating a poker hand."""
    
    stacks: List[int]
    positions: Dict[str, int]
    player_cards: Dict[str, List[str]]
    board_cards: List[str]
    actions: List[Dict]


class PokerHandResponse(BaseModel):
    """Schema for poker hand response."""
    
    id: str
    stacks: List[int]
    positions: Dict[str, int]
    player_cards: Dict[str, List[str]]
    board_cards: List[str]
    actions: List[Dict]
    results: Dict[str, int] 