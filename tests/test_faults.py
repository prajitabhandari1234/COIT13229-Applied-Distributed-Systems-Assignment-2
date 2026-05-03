import sys
import os
import time

sys.path.append(os.path.abspath("src"))

from game import GameState, Player


def test_lagged_move_still_applied():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    time.sleep(0.2)
    game.apply_move("human", "d")

    assert player.x == 6
    assert player.y == 5


def test_lost_message_simulation():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    sent_moves = ["d", "d", "s", "s"]
    delivered_moves = ["d", "s"]

    for move in delivered_moves:
        game.apply_move("human", move)

    assert player.x == 6
    assert player.y == 6
    assert len(delivered_moves) < len(sent_moves)


def test_sequential_order_is_applied_correctly():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    moves = ["d", "d", "s", "a"]

    for move in moves:
        game.apply_move("human", move)

    assert player.x == 6
    assert player.y == 6


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


def test_node_crash_manual_limitation():
    """
    Manual test:
    1. Start server: python src/server.py
    2. Start client: python src/client.py
    3. Stop server using CTRL + C
    4. Observe that client stops receiving game updates.

    This prototype does not implement backup server recovery.
    """
    server_recovery_implemented = False
    assert server_recovery_implemented is False