from gym import spaces
import numpy as np
import gym


class Connect4(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, rows=6, cols=7, connect_length=4):
        super(Connect4, self).__init__()
        self.rows = rows
        self.cols = cols
        self.connect_length = connect_length

        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(rows)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(N_CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)

    def step(self, action):
        return self.observation, self.reward, self.done, self.info

    def reset(self):
        self.done = False
        self.board = [[0] * self.cols for _ in range(self.rows)]

        return self.observation  # reward, done, info can't be included

    def render(self, mode='human'):
        print("\n".join(f"| {' '.join(list(map(str, row)))} |" for row in self.board) +
              f"\n{'_' * (5 + 2 * len(self.board))}")

    def close(self):
        pass

    def add_checker(self, col: int, insert_value: int) -> None:
        # starts from the bottom of the column and goes up
        for x_row in range(len(self.board) - 1, -1, -1):
            # moving up, if the current position is empty, then it will insert the checker value
            if self.board[x_row][col] == 0:
                self.board[x_row][col] = insert_value
                return

    def check_for_winner(self) -> int:
        def check_horizontal():
            for row in self.board:
                for col in range(len(row) - self.connect_length + 1):
                    if all(row[col + i] == current_player for i in range(self.connect_length)):
                        return current_player
            return 0

        def check_vertical():
            for col in range(len(self.board[0])):
                for row in range(len(self.board) - self.connect_length + 1):
                    if all(self.board[row + i][col] == current_player for i in range(self.connect_length)):
                        return current_player
            return 0

        def check_diagonal():
            for row in range(len(self.board) - self.connect_length + 1):
                for col in range(len(self.board[0]) - self.connect_length + 1):
                    if all(self.board[row + i][col + i] == current_player for i in range(self.connect_length)):
                        return current_player

            for row in range(len(self.board) - self.connect_length + 1):
                for col in range(self.connect_length - 1, len(self.board[0])):
                    if all(self.board[row + i][col - i] == current_player for i in range(self.connect_length)):
                        return current_player
            return 0

        if len(self.give_open_cols()) == 0:
            self.done = True
            return 3

        for current_player in [1, 2]:
            checks = [check_vertical(), check_horizontal(), check_diagonal()]
            if any(checks):
                self.done = True
                return current_player

        return 0

    # returns a list of open columns
    def give_open_cols(self) -> list:
        return [x for x in range(len(self.board[0])) if self.board[0][x] == 0]

class Board:
    def __init__(self, rows=6, cols=7, connect_length=4):
        # creates a board, each row should be a new reference
        self.board = [[0] * cols for _ in range(rows)]
        self.connect_length = connect_length
        self.done = False

    def print(self) -> None:
        print("\n".join(f"| {' '.join(list(map(str, row)))} |" for row in self.board) +
             f"\n{'_' * (5 + 2 * len(self.board))}")

    # adds a checker to a specific column
    def add_checker(self, col: int, insert_value: int) -> None:
        # starts from the bottom of the column and goes up
        for x_row in range(len(self.board) - 1, -1, -1):
            # moving up, if the current position is empty, then it will insert the checker value
            if self.board[x_row][col] == 0:
                self.board[x_row][col] = insert_value
                return

        raise IndexError(f"Invalid Column Position {col}")

    # will check the board for any winners, returns 0 if no one, and 1 or 2 depending on
    # the winner
    def check_for_winner(self) -> int:
        def check_horizontal():
            for row in self.board:
                for col in range(len(row) - self.connect_length + 1):
                    if all(row[col + i] == current_player for i in range(self.connect_length)):
                        return current_player
            return 0

        def check_vertical():
            for col in range(len(self.board[0])):
                for row in range(len(self.board) - self.connect_length + 1):
                    if all(self.board[row + i][col] == current_player for i in range(self.connect_length)):
                        return current_player
            return 0

        def check_diagonal():
            for row in range(len(self.board) - self.connect_length + 1):
                for col in range(len(self.board[0]) - self.connect_length + 1):
                    if all(self.board[row + i][col + i] == current_player for i in range(self.connect_length)):
                        return current_player

            for row in range(len(self.board) - self.connect_length + 1):
                for col in range(self.connect_length - 1, len(self.board[0])):
                    if all(self.board[row + i][col - i] == current_player for i in range(self.connect_length)):
                        return current_player
            return 0

        if len(self.give_open_cols()) == 0:
            self.done = True
            return 3

        for current_player in [1, 2]:
            checks = [check_vertical(), check_horizontal(), check_diagonal()]
            if any(checks):
                self.done = True
                return current_player

        return 0

    # returns a list of open columns
    def give_open_cols(self) -> list:
        return [x for x in range(len(self.board[0])) if self.board[0][x] == 0]
