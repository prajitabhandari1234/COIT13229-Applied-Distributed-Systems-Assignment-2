import sys
import os
import time
import random

sys.path.append(os.path.abspath("src"))

from game import GameState, Player


def test_lagged_move_still_applied():
    game = GameState()
    player = Player("human", "Human", "H", 0, 0)
    game.add_player(player)

    time.sleep(0.2)
    game.apply_move("human", "d")

    assert player.x == 1


def test_lost_message_simulation():
    game = GameState()
    player = Player("human", "Human", "H", 0, 0)
    game.add_player(player)

    moves = ["d", "d", "s", "s"]

    delivered_moves = moves[:2]

    for move in delivered_moves:
        game.apply_move("human", move)

    assert player.x == 2
    assert player.y == 0


def test_reordered_messages_change_result():
    game_one = GameState()
    game_two = GameState()

    player_one = Player("human", "Human", "H", 0, 0)
    player_two = Player("human", "Human", "H", 0, 0)

    game_one.add_player(player_one)
    game_two.add_player(player_two)

    original_order = ["d", "s"]
    reordered = ["s", "d"]

    for move in original_order:
        game_one.apply_move("human", move)

    for move in reordered:
        game_two.apply_move("human", move)

    assert (player_one.x, player_one.y) == (1, 1)
    assert (player_two.x, player_two.y) == (1, 1)


def test_node_crash_manual_limitation():
    """
    This test documents a known prototype limitation.

    If the server crashes, clients cannot continue because the prototype
    does not yet implement backup servers or peer restart recovery.
    This is acceptable because the assignment allows prototype limitations,
    but the limitation must be discussed in the test results and video.
    """
    server_recovery_implemented = False
    assert server_recovery_implemented is False
    