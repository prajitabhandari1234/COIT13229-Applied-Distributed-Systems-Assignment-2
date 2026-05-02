import random

GRID_SIZE = 20
GOLD_COUNT = 8


class Player:
    def __init__(self, player_id, name, symbol, x, y):
        self.player_id = player_id
        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y
        self.score = 0

    def move(self, direction):
        if direction == "w" and self.y > 0:
            self.y -= 1
        elif direction == "s" and self.y < GRID_SIZE - 1:
            self.y += 1
        elif direction == "a" and self.x > 0:
            self.x -= 1
        elif direction == "d" and self.x < GRID_SIZE - 1:
            self.x += 1


class GameState:
    def __init__(self):
        self.players = {}
        self.gold_positions = []
        self.create_gold()

    def add_player(self, player):
        self.players[player.player_id] = player

    def create_gold(self):
        self.gold_positions = []
        while len(self.gold_positions) < GOLD_COUNT:
            position = (
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1),
            )
            if position not in self.gold_positions:
                self.gold_positions.append(position)

    def apply_move(self, player_id, direction):
        if player_id not in self.players:
            return

        player = self.players[player_id]
        player.move(direction)

        if (player.x, player.y) in self.gold_positions:
            player.score += 1
            self.gold_positions.remove((player.x, player.y))
            self.gold_positions.append(self.random_empty_position())

    def random_empty_position(self):
        while True:
            position = (
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1),
            )
            occupied = [(p.x, p.y) for p in self.players.values()]
            if position not in self.gold_positions and position not in occupied:
                return position

    def render(self):
        grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for x, y in self.gold_positions:
            grid[y][x] = "$"

        for player in self.players.values():
            grid[player.y][player.x] = player.symbol

        print("\n" * 3)
        print("====== GOLD MINER ======")
        for row in grid:
            print(" ".join(row))

        print("\nScores:")
        for player in self.players.values():
            print(f"{player.name}: {player.score}")

    def get_bot_direction(self, bot_id):
        bot = self.players[bot_id]
        if not self.gold_positions:
            return random.choice(["w", "a", "s", "d"])

        nearest_gold = min(
            self.gold_positions,
            key=lambda gold: abs(gold[0] - bot.x) + abs(gold[1] - bot.y),
        )

        gold_x, gold_y = nearest_gold

        if gold_x > bot.x:
            return "d"
        if gold_x < bot.x:
            return "a"
        if gold_y > bot.y:
            return "s"
        if gold_y < bot.y:
            return "w"

        return random.choice(["w", "a", "s", "d"])


def run_local_game():
    game = GameState()

    human = Player("human", "Human", "H", 0, 0)
    bot1 = Player("bot1", "Bot 1", "B", 10, 10)
    bot2 = Player("bot2", "Bot 2", "C", 15, 15)

    game.add_player(human)
    game.add_player(bot1)
    game.add_player(bot2)

    while True:
        game.render()
        move = input("Move with W/A/S/D or Q to quit: ").lower()

        if move == "q":
            print("Game ended.")
            break

        if move in ["w", "a", "s", "d"]:
            game.apply_move("human", move)

            for bot_id in ["bot1", "bot2"]:
                bot_move = game.get_bot_direction(bot_id)
                game.apply_move(bot_id, bot_move)


if __name__ == "__main__":
    run_local_game()