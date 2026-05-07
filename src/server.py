import json
import time
import zmq
from game import GameState, Player, MAX_PLAYERS

# Network ports used by the server
PULL_PORT = "5555"
PUB_PORT = "5556"


# Create a new game state with two server-controlled bots
def create_new_game():
    game = GameState()

    game.add_player(Player("bot1", "Bot 1", "B", 10, 10, is_bot=True))
    game.add_player(Player("bot2", "Bot 2", "C", 15, 15, is_bot=True))

    return game


# Assign a unique display symbol to each new player
def get_next_symbol(game):
    symbols = list("HJKLMNOPQRSTUVWXYZ123456789")
    used_symbols = [player.symbol for player in game.players.values()]

    for symbol in symbols:
        if symbol not in used_symbols:
            return symbol

    return "P"


# Convert the game object into JSON-friendly data for broadcasting
def game_to_state(game, last_move_seq):
    return {
        "players": {
            player_id: {
                "name": player.name,
                "symbol": player.symbol,
                "x": player.x,
                "y": player.y,
                "score": player.score,
                "is_bot": player.is_bot,
            }
            for player_id, player in game.players.items()
        },
        "gold_positions": game.gold_positions,
        "player_count": len(game.players),
        "max_players": MAX_PLAYERS,
        "last_move_seq": last_move_seq,
    }


def main():
    context = zmq.Context()

    # PULL socket receives join, move, and quit messages from clients
    receiver = context.socket(zmq.PULL)
    receiver.bind(f"tcp://*:{PULL_PORT}")

    # PUB socket broadcasts the latest game state to all clients
    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://*:{PUB_PORT}")

    # Store the authoritative game state on the server
    game = create_new_game()

    # Tracks the latest processed move sequence number for each player
    last_move_seq = {}

    print("Server started.")
    print(f"Receiving moves on port {PULL_PORT}")
    print(f"Publishing game state on port {PUB_PORT}")
    print(f"Maximum supported players: {MAX_PLAYERS}")

    last_bot_move = time.time()

    while True:
        try:
            # Non-blocking receive allows the server to keep broadcasting game state
            message = receiver.recv_json(flags=zmq.NOBLOCK)

            action = message.get("action")
            player_id = message.get("player_id")
            player_name = message.get("name", "Player")
            direction = message.get("direction")

            # Add a new human player to the game
            if action == "join":
                if player_id not in game.players:
                    x, y = game.random_empty_position()
                    symbol = get_next_symbol(game)

                    joined = game.add_player(
                        Player(player_id, player_name, symbol, x, y)
                    )

                    if joined:
                        print(f"Player joined: {player_name} ({player_id})")
                    else:
                        print("Join rejected: maximum players reached")
                last_move_seq[player_id] = 0

            # Remove player when client quits
            elif action == "quit":
                print(f"Player quit: {player_id}")
                game.remove_player(player_id)
                last_move_seq.pop(player_id, None)

            # Process movement messages in server arrival order
            elif direction in ["w", "a", "s", "d"]:
                seq = message.get("seq", 0)

                print(f"Move received: {player_id} -> {direction} seq={seq}")
                collected = game.apply_move(player_id, direction)

                # Confirm that this move sequence has been processed
                last_move_seq[player_id] = seq

                if collected:
                    print(f"{player_id} collected gold!")

        except zmq.Again:
            # No client message was available during this loop
            pass

        # Move bots automatically every 1 second
        if time.time() - last_bot_move > 1:
            for bot_id in ["bot1", "bot2"]:
                if bot_id in game.players:
                    bot_move = game.get_bot_direction(bot_id)
                    game.apply_move(bot_id, bot_move)

            last_bot_move = time.time()

        # Broadcast current authoritative game state to all clients
        publisher.send_string(json.dumps(game_to_state(game, last_move_seq)))

        # Small delay prevents the server loop from using too much CPU
        time.sleep(0.05)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")