import random

GRID_SIZE = 20
GOLD_COUNT = 8
MAX_PLAYERS = 100


class Player:
    def __init__(self, player_id, name, symbol, x, y, is_bot=False):
        self.player_id = player_id
        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y
        self.score = 0
        self.is_bot = is_bot

    def move(self, direction):
        direction = direction.lower()

        if direction == "w":
            self.y = max(0, self.y - 1)
        elif direction == "s":
            self.y = min(GRID_SIZE - 1, self.y + 1)
        elif direction == "a":
            self.x = max(0, self.x - 1)
        elif direction == "d":
            self.x = min(GRID_SIZE - 1, self.x + 1)


class GameState:
    def __init__(self):
        self.players = {}
        self.gold_positions = []
        self.create_gold()

    def add_player(self, player):
        if len(self.players) >= MAX_PLAYERS:
            return False

        self.players[player.player_id] = player
        return True

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def create_gold(self):
        self.gold_positions = []

        while len(self.gold_positions) < GOLD_COUNT:
            position = self.random_empty_position()
            if position not in self.gold_positions:
                self.gold_positions.append(position)

    def random_position(self):
        return (
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1),
        )

    def random_empty_position(self):
        while True:
            position = self.random_position()
            occupied = [(p.x, p.y) for p in self.players.values()]

            if position not in self.gold_positions and position not in occupied:
                return position

    def apply_move(self, player_id, direction):
        if player_id not in self.players:
            return False

        player = self.players[player_id]
        player.move(direction)

        if (player.x, player.y) in self.gold_positions:
            player.score += 1
            self.gold_positions.remove((player.x, player.y))
            self.gold_positions.append(self.random_empty_position())
            return True

        return False

    def get_bot_direction(self, bot_id):
        if bot_id not in self.players:
            return random.choice(["w", "a", "s", "d"])

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