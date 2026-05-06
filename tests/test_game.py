import os
import sys

sys.path.append(os.path.abspath("src"))

from game import GameState, Player, GRID_SIZE, MAX_PLAYERS


def test_player_can_move_right():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("d")
    assert (player.x, player.y) == (6, 5)


def test_player_can_move_left():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("a")
    assert (player.x, player.y) == (4, 5)


def test_player_can_move_up():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("w")
    assert (player.x, player.y) == (5, 4)


def test_player_can_move_down():
    player = Player("p1", "Test Player", "T", 5, 5)
    player.move("s")
    assert (player.x, player.y) == (5, 6)


def test_player_cannot_move_outside_top_left():
    player = Player("p1", "Test Player", "T", 0, 0)
    player.move("a")
    player.move("w")
    assert (player.x, player.y) == (0, 0)


def test_player_cannot_move_outside_bottom_right():
    player = Player("p1", "Test Player", "T", GRID_SIZE - 1, GRID_SIZE - 1)
    player.move("d")
    player.move("s")
    assert (player.x, player.y) == (GRID_SIZE - 1, GRID_SIZE - 1)


def test_game_adds_player():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)

    result = game.add_player(player)

    assert result is True
    assert "p1" in game.players


def test_game_removes_player():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)

    game.add_player(player)
    game.remove_player("p1")

    assert "p1" not in game.players


def test_game_supports_maximum_100_players():
    game = GameState()

    for i in range(MAX_PLAYERS):
        result = game.add_player(Player(f"p{i}", f"Player {i}", "P", 0, 0))
        assert result is True

    extra_result = game.add_player(Player("extra", "Extra", "E", 0, 0))

    assert extra_result is False
    assert len(game.players) == MAX_PLAYERS


def test_player_collects_gold():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)
    game.add_player(player)

    game.gold_positions = [(1, 0)]

    collected = game.apply_move("p1", "d")

    assert collected is True
    assert player.score == 1
    assert len(game.gold_positions) == 1


def test_move_without_gold_returns_false():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)
    game.add_player(player)

    game.gold_positions = [(5, 5)]

    collected = game.apply_move("p1", "d")

    assert collected is False
    assert player.score == 0


def test_unknown_player_does_not_crash():
    game = GameState()

    result = game.apply_move("unknown", "d")

    assert result is False
    
def test_gold_respawns_after_collection():
    game = GameState()
    player = Player("p1", "Test Player", "T", 0, 0)
    game.add_player(player)

    game.gold_positions = [(1, 0)]
    old_gold_position = (1, 0)

    collected = game.apply_move("p1", "d")

    assert collected is True
    assert player.score == 1
    assert len(game.gold_positions) == 1
    assert old_gold_position not in game.gold_positions


def test_bot_moves_toward_nearest_gold():
    game = GameState()
    bot = Player("bot1", "Bot 1", "B", 5, 5, is_bot=True)
    game.add_player(bot)

    game.gold_positions = [(7, 5)]

    direction = game.get_bot_direction("bot1")

    assert direction == "d"