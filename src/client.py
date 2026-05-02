import json
import os
import zmq

GRID_SIZE = 20
SERVER_HOST = "127.0.0.1"
PUSH_PORT = "5555"
SUB_PORT = "5556"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def render_state(state):
    clear_screen()

    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for x, y in state["gold_positions"]:
        grid[y][x] = "$"

    for player in state["players"].values():
        grid[player["y"]][player["x"]] = player["symbol"]

    print("====== GOLD MINER ======")

    print("+" + "---" * GRID_SIZE + "+")

    for row in grid:
        print("|", end="")
        for cell in row:
            print(f" {cell} ", end="")
        print("|")

    print("+" + "---" * GRID_SIZE + "+")

    print("\nScores:")
    for player in state["players"].values():
        print(f'{player["name"]}: {player["score"]}')

    print("\nMove: W/A/S/D | Quit: Q")


def main():
    context = zmq.Context()

    sender = context.socket(zmq.PUSH)
    sender.connect(f"tcp://{SERVER_HOST}:{PUSH_PORT}")

    subscriber = context.socket(zmq.SUB)
    subscriber.connect(f"tcp://{SERVER_HOST}:{SUB_PORT}")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Connected to server. Waiting for game state...")

    while True:
        message = subscriber.recv_string()
        state = json.loads(message)
        render_state(state)

        move = input("Enter move: ").lower()

        if move == "q":
            sender.send_json({
                "player_id": "human",
                "action": "quit"
            })
            print("Client closed.")
            break

        if move in ["w", "a", "s", "d"]:
            sender.send_json({
                "player_id": "human",
                "direction": move
            })


if __name__ == "__main__":
    main()