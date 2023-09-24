from gymnasium import spaces
import numpy as np
import gymnasium
import random

class Connect4(gymnasium.Env):
    """Custom Environment that follows gym interface"""
    def __init__(self, rows=6, cols=7, connect_length=4, validity_mode=False, win_mode=False):
        super(Connect4, self).__init__()

        # unchanging variables, won't change between resets
        self.win_reward = 0 # 10
        self.lose_reward = 0 #-10
        self.tie_reward = 0 # 5

        self.hero_checker = 1
        self.other_checker = 2
        self.validity_mode = validity_mode
        self.rows = rows
        self.cols = cols
        self.connect_length = connect_length

        # defined action and observation space
        self.action_space = spaces.Discrete(rows)
        self.observation_space = spaces.Box(0, 2, shape=(self.rows * self.cols, ), dtype=np.int8)

    def step(self, action):
        open_columns = self.give_open_cols()
        self.reward = 0

        # ensures the current move is valid
        if action in open_columns:
            # when evaluating for validity, rewards making a valid move
            self.reward += 1

            # adds the hero's checker
            self.add_checker(action, self.hero_checker)
            win_situation = self.check_for_winner()

            # checks if the game has ended after the hero's move with a win
            if self.hero_checker == win_situation:
                self.reward += self.win_reward
                self.terminated = True
            # checks if the game has ended after hero's move with a lose
            elif 3 == win_situation:
                self.reward += self.tie_reward
            # continues with the op's move
            else:
                # adds the op's checker
                self.add_checker(random.choice(self.give_open_cols()), self.other_checker)
                win_situation = self.check_for_winner()

                if self.other_checker == win_situation:
                    self.reward += self.lose_reward
                    self.terminated = True
                elif 3 == win_situation:
                    self.reward += self.tie_reward
            # if the move is not correct, then nothing happens and returns a negative reward
        else:
            self.reward -= 10

        self.observation = np.ndarray.flatten(self.board)

        return self.observation, self.reward, self.terminated, self.truncated, {}

    def reset(self, seed=0):
        self.terminated = False
        self.truncated = False
        self.board = np.zeros(shape=(self.rows, self.cols), dtype=np.int8)
        self.observation = np.ndarray.flatten(self.board)

        return self.observation, {}  # reward, done, info can't be included

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

    # returns ann int, 0 with no winner, 1 or 2 depending on who won, and 3 for a tie
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
            return 3

        for current_player in [1, 2]:
            checks = [check_vertical(), check_horizontal(), check_diagonal()]
            if any(checks):
                return current_player

        return 0

    # returns a list of open columns indexes
    def give_open_cols(self) -> list[int]:
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
            return 3

        for current_player in [1, 2]:
            checks = [check_vertical(), check_horizontal(), check_diagonal()]
            if any(checks):
                return current_player

        return 0

    # returns a list of open columns
    def give_open_cols(self) -> list:
        return [x for x in range(len(self.board[0])) if self.board[0][x] == 0]
