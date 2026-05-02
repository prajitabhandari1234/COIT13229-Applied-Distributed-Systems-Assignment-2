import json
import time
import zmq
from game import GameState, Player

PULL_PORT = "5555"
PUB_PORT = "5556"


def create_new_game():
    game = GameState()
    game.add_player(Player("human", "Human", "H", 0, 0))
    game.add_player(Player("bot1", "Bot 1", "B", 10, 10))
    game.add_player(Player("bot2", "Bot 2", "C", 15, 15))
    return game


def game_to_state(game):
    return {
        "players": {
            player_id: {
                "name": player.name,
                "symbol": player.symbol,
                "x": player.x,
                "y": player.y,
                "score": player.score,
            }
            for player_id, player in game.players.items()
        },
        "gold_positions": game.gold_positions,
    }


def main():
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.bind(f"tcp://*:{PULL_PORT}")

    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://*:{PUB_PORT}")

    game = create_new_game()

    print("Server started.")
    print(f"Receiving moves on port {PULL_PORT}")
    print(f"Publishing game state on port {PUB_PORT}")

    last_bot_move = time.time()

    while True:
        try:
            message = receiver.recv_json(flags=zmq.NOBLOCK)

            player_id = message.get("player_id")
            direction = message.get("direction")
            action = message.get("action")

            if action == "quit":
                print("Human quit. Resetting game...")
                game = create_new_game()

            elif direction in ["w", "a", "s", "d"]:
                print(f"Move received: {player_id} -> {direction}")
                game.apply_move(player_id, direction)

        except zmq.Again:
            pass

        if time.time() - last_bot_move > 3:
            for bot_id in ["bot1", "bot2"]:
                bot_move = game.get_bot_direction(bot_id)
                game.apply_move(bot_id, bot_move)
            last_bot_move = time.time()

        publisher.send_string(json.dumps(game_to_state(game)))
        time.sleep(0.05)


if __name__ == "__main__":
    main()