import sys
import os

sys.path.append(os.path.abspath("src"))

from game import GameState, Player, GRID_SIZE


def test_player_can_move_right():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("d")
    assert player.x == 6
    assert player.y == 5


def test_player_can_move_left():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("a")
    assert player.x == 4
    assert player.y == 5


def test_player_can_move_up():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("w")
    assert player.x == 5
    assert player.y == 4


def test_player_can_move_down():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("s")
    assert player.x == 5
    assert player.y == 6


def test_player_cannot_move_outside_top_left():
    player = Player("p1", "Test Player", "T", 0, 0)
    player.move("a")
    player.move("w")
    assert player.x == 0
    assert player.y == 0


def test_player_cannot_move_outside_bottom_right():
    player = Player("p1", "Test Player", "T", GRID_SIZE - 1, GRID_SIZE - 1)
    player.move("d")
    player.move("s")
    assert player.x == GRID_SIZE - 1
    assert player.y == GRID_SIZE - 1


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
    assert len(game.gold_positions) == 1


def test_unknown_player_does_not_crash():
    game = GameState()
    game.apply_move("unknown", "d")
    assert True