import sys
import os

sys.path.append(os.path.abspath("src"))

from game import GameState, Player


def test_player_can_move_right():
    player = Player("p1", "Test Player", "T", 0, 0)
    player.move("d")
    assert player.x == 1
    assert player.y == 0


def test_player_cannot_move_outside_grid():
    player = Player("p1", "Test Player", "T", 0, 0)
    player.move("a")
    player.move("w")
    assert player.x == 0
    assert player.y == 0


def test_game_adds_player():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)
    game.add_player(player)
    assert "p1" in game.players


def test_player_collects_gold():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)
    game.add_player(player)

    game.gold_positions = [(1, 0)]
    game.apply_move("p1", "d")

    assert player.score == 1