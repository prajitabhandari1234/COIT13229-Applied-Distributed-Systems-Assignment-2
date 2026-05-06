import json
import os
import uuid
import zmq

GRID_SIZE = 20
SERVER_HOST = "127.0.0.1"
PUSH_PORT = "5555"
SUB_PORT = "5556"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def render_state(state, my_player_id):
    clear_screen()

    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for x, y in state["gold_positions"]:
        grid[y][x] = "$"

    for player_id, player in state["players"].items():
        symbol = player["symbol"]
        grid[player["y"]][player["x"]] = symbol

    print("========== GOLD MINER ==========")
    print(f'Players connected: {state["player_count"]}/{state["max_players"]}')

    if my_player_id in state["players"]:
        my_symbol = state["players"][my_player_id]["symbol"]
        print(f"Your player is shown as: {my_symbol}")
    else:
        print("Waiting for server to add your player...")

    print("+" + "---" * GRID_SIZE + "+")

    for row in grid:
        print("|", end="")
        for cell in row:
            print(f" {cell} ", end="")
        print("|")

    print("+" + "---" * GRID_SIZE + "+")

    print("\nScores:")
    for player_id, player in state["players"].items():
        label = "YOU" if player_id == my_player_id else player["name"]
        print(f'{label} ({player["symbol"]}): {player["score"]}')

    print("\nControls: W/A/S/D then Enter | Q then Enter to quit")


def receive_state(subscriber):
    try:
        message = subscriber.recv_string()
        return json.loads(message)

    except zmq.Again:
        print("Server not responding — possible crash or network lag.")
        return None


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

    sender = context.socket(zmq.PUSH)
    sender.connect(f"tcp://{SERVER_HOST}:{PUSH_PORT}")

    subscriber = context.socket(zmq.SUB)
    subscriber.setsockopt(zmq.RCVTIMEO, 3000)
    subscriber.connect(f"tcp://{SERVER_HOST}:{SUB_PORT}")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    player_id = str(uuid.uuid4())
    player_name = input("Enter your player name: ").strip()

    if player_name == "":
        player_name = "Player"

    sender.send_json({
        "action": "join",
        "player_id": player_id,
        "name": player_name
    })

    print("Connected to server. Waiting for game state...")

    move_seq = 0

    while True:
        state = receive_state(subscriber)

        if state is None:
            continue

        render_state(state, player_id)

        move = input("Enter move: ").lower().strip()

        if move == "q":
            sender.send_json({
                "action": "quit",
                "player_id": player_id
            })
            print("Client closed.")
            break

        for key in move:
            if key in ["w", "a", "s", "d"]:
                move_seq += 1

                sender.send_json({
                    "player_id": player_id,
                    "direction": key,
                    "seq": move_seq
                })

                state = wait_for_my_move(subscriber, player_id, move_seq)

                if state is None:
                    print("Skipping render because no game state was received.")
                    continue

                render_state(state, player_id)


if __name__ == "__main__":
    main()