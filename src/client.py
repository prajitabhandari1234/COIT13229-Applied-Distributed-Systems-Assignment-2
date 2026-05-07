import json
import os
import uuid
import zmq

# Game and network configuration
GRID_SIZE = 20
SERVER_HOST = "127.0.0.1"
PUSH_PORT = "5555"
SUB_PORT = "5556"


# Clear terminal screen for cleaner game display
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Display the latest game state received from the server
def render_state(state, my_player_id):
    clear_screen()

    # Create an empty 20x20 grid
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Place gold items on the grid
    for x, y in state["gold_positions"]:
        grid[y][x] = "$"

    # Place all players and bots on the grid
    for player_id, player in state["players"].items():
        symbol = player["symbol"]
        grid[player["y"]][player["x"]] = symbol

    print("========== GOLD MINER ==========")
    print(f'Players connected: {state["player_count"]}/{state["max_players"]}')

    # Show the symbol assigned to this client by the server
    if my_player_id in state["players"]:
        my_symbol = state["players"][my_player_id]["symbol"]
        print(f"Your player is shown as: {my_symbol}")
    else:
        print("Waiting for server to add your player...")

    print("+" + "---" * GRID_SIZE + "+")

    # Print the grid with borders
    for row in grid:
        print("|", end="")
        for cell in row:
            print(f" {cell} ", end="")
        print("|")

    print("+" + "---" * GRID_SIZE + "+")

    # Print current scores
    print("\nScores:")
    for player_id, player in state["players"].items():
        label = "YOU" if player_id == my_player_id else player["name"]
        print(f'{label} ({player["symbol"]}): {player["score"]}')

    print("\nControls: W/A/S/D then Enter | Q then Enter to quit")


# Receive game state from server with timeout handling
def receive_state(subscriber):
    try:
        message = subscriber.recv_string()
        return json.loads(message)

    except zmq.Again:
        print("Server not responding — possible crash or network lag.")
        return None


# Wait until the server confirms that this client's move sequence was processed
def wait_for_my_move(subscriber, player_id, seq):
    while True:
        state = receive_state(subscriber)

        if state is None:
            return None

        last_seq = state.get("last_move_seq", {}).get(player_id, 0)

        if last_seq >= seq:
            return state


def main():
    context = zmq.Context()

    # PUSH socket sends this client's movement commands to the server
    sender = context.socket(zmq.PUSH)
    sender.connect(f"tcp://{SERVER_HOST}:{PUSH_PORT}")

    # SUB socket receives updated game states from the server
    subscriber = context.socket(zmq.SUB)

    # Timeout prevents the client from hanging forever if the server crashes
    subscriber.setsockopt(zmq.RCVTIMEO, 3000)
    subscriber.connect(f"tcp://{SERVER_HOST}:{SUB_PORT}")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    # Generate unique player ID for this client
    player_id = str(uuid.uuid4())
    player_name = input("Enter your player name: ").strip()

    if player_name == "":
        player_name = "Player"

    # Register this client with the server
    sender.send_json({
        "action": "join",
        "player_id": player_id,
        "name": player_name
    })

    print("Connected to server. Waiting for game state...")

    # Sequence number confirms that player moves are processed in order
    move_seq = 0

    while True:
        state = receive_state(subscriber)

        if state is None:
            continue

        render_state(state, player_id)

        move = input("Enter move: ").lower().strip()

        # Send quit action to server before closing client
        if move == "q":
            sender.send_json({
                "action": "quit",
                "player_id": player_id
            })
            print("Client closed.")
            break

        # Allow one or more movement keys to be entered
        for key in move:
            if key in ["w", "a", "s", "d"]:
                move_seq += 1

                # Send movement command with sequence number
                sender.send_json({
                    "player_id": player_id,
                    "direction": key,
                    "seq": move_seq
                })

                # Wait for server confirmation before rendering final state
                state = wait_for_my_move(subscriber, player_id, move_seq)

                if state is None:
                    print("Skipping render because no game state was received.")
                    continue

                render_state(state, player_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient closed by user.")