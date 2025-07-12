"""Tests for the hands API endpoints."""
import pytest
from fastapi.testclient import TestClient
import json
from unittest.mock import patch, MagicMock

from app.main import app
from app.models.hand import Hand, PokerHand
from app.repositories.hand_repository import HandRepository
from app.services.poker_service import PokerService

client = TestClient(app)


@pytest.fixture
def mock_repository():
    """Mock repository for testing."""
    with patch("app.api.endpoints.hands.get_repository") as mock:
        repo = MagicMock(spec=HandRepository)
        mock.return_value = repo
        yield repo


@pytest.fixture
def mock_poker_service():
    """Mock poker service for testing."""
    with patch("app.api.endpoints.hands.get_poker_service") as mock:
        service = MagicMock(spec=PokerService)
        mock.return_value = service
        yield service


def test_create_hand(mock_repository, mock_poker_service):
    """Test creating a hand."""
    # Setup mocks
    mock_poker_service.evaluate_hand.return_value = {
        "hand_type": "Straight Flush",
        "rank": 9
    }
    
    hand = Hand(cards=["As", "Ks", "Qs", "Js", "Ts"], hand_type="Straight Flush", rank=9, id=1)
    mock_repository.create_hand.return_value = hand
    
    # Test API call
    response = client.post(
        "/api/v1/poker/hands/",
        json={"cards": ["As", "Ks", "Qs", "Js", "Ts"]}
    )
    
    # Verify response
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["cards"] == ["As", "Ks", "Qs", "Js", "Ts"]
    assert data["hand_type"] == "Straight Flush"
    assert data["rank"] == 9
    
    # Verify mocks were called correctly
    mock_poker_service.evaluate_hand.assert_called_once_with(["As", "Ks", "Qs", "Js", "Ts"])
    mock_repository.create_hand.assert_called_once()


def test_create_hand_invalid(mock_repository, mock_poker_service):
    """Test creating an invalid hand."""
    # Setup mocks
    mock_poker_service.evaluate_hand.side_effect = ValueError("A hand must contain at least 5 cards")
    
    # Test API call
    response = client.post(
        "/api/v1/poker/hands/",
        json={"cards": ["As", "Ks"]}  # Not enough cards
    )
    
    # Verify response
    assert response.status_code == 400
    assert "A hand must contain at least 5 cards" in response.json()["detail"]
    
    # Verify mocks were called correctly
    mock_poker_service.evaluate_hand.assert_called_once_with(["As", "Ks"])
    mock_repository.create_hand.assert_not_called()


def test_get_hands(mock_repository):
    """Test getting all hands."""
    # Setup mocks
    hands = [
        Hand(id=1, cards=["As", "Ks", "Qs", "Js", "Ts"], hand_type="Straight Flush", rank=9),
        Hand(id=2, cards=["Ah", "Kh", "Qh", "Jh", "Th"], hand_type="Straight Flush", rank=9)
    ]
    mock_repository.get_all_hands.return_value = hands
    
    # Test API call
    response = client.get("/api/v1/poker/hands/")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["cards"] == ["As", "Ks", "Qs", "Js", "Ts"]
    assert data[0]["hand_type"] == "Straight Flush"
    assert data[0]["rank"] == 9
    
    # Verify mocks were called correctly
    mock_repository.get_all_hands.assert_called_once()


def test_get_hand(mock_repository):
    """Test getting a specific hand."""
    # Setup mocks
    hand = Hand(id=1, cards=["As", "Ks", "Qs", "Js", "Ts"], hand_type="Straight Flush", rank=9)
    mock_repository.get_hand.return_value = hand
    
    # Test API call
    response = client.get("/api/v1/poker/hands/1")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["cards"] == ["As", "Ks", "Qs", "Js", "Ts"]
    assert data["hand_type"] == "Straight Flush"
    assert data["rank"] == 9
    
    # Verify mocks were called correctly
    mock_repository.get_hand.assert_called_once_with(1)


def test_get_hand_not_found(mock_repository):
    """Test getting a hand that doesn't exist."""
    # Setup mocks
    mock_repository.get_hand.return_value = None
    
    # Test API call
    response = client.get("/api/v1/poker/hands/999")
    
    # Verify response
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    
    # Verify mocks were called correctly
    mock_repository.get_hand.assert_called_once_with(999)


def test_create_game(mock_poker_service):
    """Test creating a new game."""
    # Setup mocks
    game = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
        "positions": {"dealer": 0, "sb": 1, "bb": 2},
        "player_cards": {
            "0": ["Ah", "Kd"],
            "1": ["Qc", "Js"],
            "2": ["Td", "9h"],
            "3": ["8c", "7s"],
            "4": ["6d", "5h"],
            "5": ["4c", "3s"]
        },
        "board_cards": ["As", "Ks", "Qs", "Js", "Ts"],
        "actions": []
    }
    mock_poker_service.create_new_game.return_value = game
    
    # Test API call
    response = client.post("/api/v1/poker/games/")
    
    # Verify response
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert data["stacks"] == [1000, 1000, 1000, 1000, 1000, 1000]
    assert data["positions"] == {"dealer": 0, "sb": 1, "bb": 2}
    assert len(data["player_cards"]) == 6
    assert len(data["board_cards"]) == 5
    assert data["actions"] == []
    
    # Verify mocks were called correctly
    mock_poker_service.create_new_game.assert_called_once()


def test_evaluate_game(mock_repository, mock_poker_service):
    """Test evaluating a complete poker game."""
    # Setup mocks
    results = {"0": 100, "1": -50, "2": -50, "3": 0, "4": 0, "5": 0}
    mock_poker_service.evaluate_poker_game.return_value = results
    
    game_data = {
        "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
        "positions": {"dealer": 0, "sb": 1, "bb": 2},
        "player_cards": {
            "0": ["Ah", "Kd"],
            "1": ["Qc", "Js"],
            "2": ["Td", "9h"],
            "3": ["8c", "7s"],
            "4": ["6d", "5h"],
            "5": ["4c", "3s"]
        },
        "board_cards": ["As", "Ks", "Qs", "Js", "Ts"],
        "actions": [
            {"type": "call", "player": 3},
            {"type": "call", "player": 4},
            {"type": "call", "player": 5},
            {"type": "call", "player": 0},
            {"type": "check", "player": 1},
            {"type": "check", "player": 2},
            {"type": "deal_flop"},
            {"type": "check", "player": 1},
            {"type": "check", "player": 2},
            {"type": "check", "player": 3},
            {"type": "check", "player": 4},
            {"type": "check", "player": 5},
            {"type": "check", "player": 0},
            {"type": "deal_turn"},
            {"type": "check", "player": 1},
            {"type": "check", "player": 2},
            {"type": "check", "player": 3},
            {"type": "check", "player": 4},
            {"type": "check", "player": 5},
            {"type": "check", "player": 0},
            {"type": "deal_river"},
            {"type": "check", "player": 1},
            {"type": "check", "player": 2},
            {"type": "check", "player": 3},
            {"type": "check", "player": 4},
            {"type": "check", "player": 5},
            {"type": "check", "player": 0}
        ]
    }
    
    # Test API call
    response = client.post(
        "/api/v1/poker/games/evaluate/",
        json=game_data
    )
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data == {"0": 100, "1": -50, "2": -50, "3": 0, "4": 0, "5": 0}
    
    # Verify mocks were called correctly
    mock_poker_service.evaluate_poker_game.assert_called_once()
    mock_repository.create_poker_hand.assert_called_once()


def test_get_games(mock_repository):
    """Test getting all games."""
    # Setup mocks
    games = [
        PokerHand(
            id="123e4567-e89b-12d3-a456-426614174000",
            stacks=[1000, 1000, 1000, 1000, 1000, 1000],
            positions={"dealer": 0, "sb": 1, "bb": 2},
            player_cards={
                0: ["Ah", "Kd"],
                1: ["Qc", "Js"],
                2: ["Td", "9h"],
                3: ["8c", "7s"],
                4: ["6d", "5h"],
                5: ["4c", "3s"]
            },
            board_cards=["As", "Ks", "Qs", "Js", "Ts"],
            actions=[],
            results={0: 100, 1: -50, 2: -50, 3: 0, 4: 0, 5: 0}
        )
    ]
    mock_repository.get_all_poker_hands.return_value = games
    
    # Test API call
    response = client.get("/api/v1/poker/games/")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert data[0]["stacks"] == [1000, 1000, 1000, 1000, 1000, 1000]
    assert data[0]["positions"] == {"dealer": 0, "sb": 1, "bb": 2}
    assert data[0]["results"] == {"0": 100, "1": -50, "2": -50, "3": 0, "4": 0, "5": 0}
    
    # Verify mocks were called correctly
    mock_repository.get_all_poker_hands.assert_called_once()


@pytest.mark.integration
def test_full_poker_hand_flow():
    """Integration test for a full poker hand flow."""
    # This test would use the actual database and services
    # For a real integration test, we would:
    # 1. Create a new game
    # 2. Add actions to the game
    # 3. Evaluate the game
    # 4. Verify the results
    # However, for this test file, we'll just check that the endpoints exist
    
    # Create a new game
    response = client.post("/api/v1/poker/games/")
    assert response.status_code in [200, 201]
    game_id = response.json()["id"]
    
    # Get the game
    response = client.get(f"/api/v1/poker/games/{game_id}")
    assert response.status_code == 200 