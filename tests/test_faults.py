import os
import sys
import time

sys.path.append(os.path.abspath("src"))

from game import GameState, Player


def test_lagged_move_still_applied():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    time.sleep(0.2)
    collected = game.apply_move("human", "d")

    assert (player.x, player.y) == (6, 5)
    assert collected in [True, False]


def test_lost_message_simulation():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    sent_moves = ["d", "d", "s", "s"]
    delivered_moves = ["d", "s"]

    for move in delivered_moves:
        game.apply_move("human", move)

    assert (player.x, player.y) == (6, 6)
    assert len(delivered_moves) < len(sent_moves)


def test_sequential_order_is_applied_correctly():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    moves = ["d", "d", "s", "a"]

    for move in moves:
        game.apply_move("human", move)

    assert (player.x, player.y) == (6, 6)


def test_reordered_messages_can_change_result():
    game_one = GameState()
    game_two = GameState()

    player_one = Player("human", "Human", "H", 0, 0)
    player_two = Player("human", "Human", "H", 0, 0)

    game_one.add_player(player_one)
    game_two.add_player(player_two)

    order_one = ["d", "s", "a"]
    order_two = ["a", "d", "s"]

    for move in order_one:
        game_one.apply_move("human", move)

    for move in order_two:
        game_two.apply_move("human", move)

    assert (player_one.x, player_one.y) != (player_two.x, player_two.y)


def test_multiple_players_have_independent_positions():
    game = GameState()

    player_one = Player("p1", "Player 1", "H", 5, 5)
    player_two = Player("p2", "Player 2", "J", 10, 10)

    game.add_player(player_one)
    game.add_player(player_two)

    game.apply_move("p1", "d")
    game.apply_move("p2", "s")

    assert (player_one.x, player_one.y) == (6, 5)
    assert (player_two.x, player_two.y) == (10, 11)


def test_node_crash_manual_limitation():
    server_recovery_implemented = False
    assert server_recovery_implemented is False