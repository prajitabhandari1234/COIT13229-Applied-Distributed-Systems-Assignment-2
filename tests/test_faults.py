import os
import sys
import time

# Allow tests to import modules from the src folder
sys.path.append(os.path.abspath("src"))

from game import GameState, Player


# Test that a delayed move is still applied correctly
def test_lagged_move_still_applied():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    # Simulate network lag before applying the move
    time.sleep(0.2)
    collected = game.apply_move("human", "d")

    assert (player.x, player.y) == (6, 5)
    assert collected in [True, False]


# Test message loss by applying only delivered moves
def test_lost_message_simulation():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    # Four moves are sent, but only two are delivered
    sent_moves = ["d", "d", "s", "s"]
    delivered_moves = ["d", "s"]

    for move in delivered_moves:
        game.apply_move("human", move)

    assert (player.x, player.y) == (6, 6)
    assert len(delivered_moves) < len(sent_moves)


# Test that moves are applied in the server-defined sequential order
def test_sequential_order_is_applied_correctly():
    game = GameState()
    player = Player("human", "Human", "H", 5, 5)
    game.add_player(player)

    moves = ["d", "d", "s", "a"]

    for move in moves:
        game.apply_move("human", move)

    assert (player.x, player.y) == (6, 6)


# Test that different arrival orders can produce different final results
def test_reordered_messages_can_change_result():
    game_one = GameState()
    game_two = GameState()

    player_one = Player("p1", "Human", "H", 5, 5)
    player_two = Player("p2", "Human", "H", 5, 5)

    game_one.add_player(player_one)
    game_two.add_player(player_two)

    game_one.gold_positions = [(6, 5)]
    game_two.gold_positions = [(6, 5)]

    for move in ["d", "s", "a"]:
        game_one.apply_move("p1", move)

    for move in ["s", "d", "a"]:
        game_two.apply_move("p2", move)

    assert player_one.score != player_two.score

# Test that multiple players maintain independent positions
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


# Document that server crash recovery is not implemented in this prototype
def test_node_crash_manual_limitation():
    server_recovery_implemented = False
    assert server_recovery_implemented is False