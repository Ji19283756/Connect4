class Board:
    def __init__(self, rows=6, cols=7, connect_length=4):
        # creates a board, each row should be a new reference
        self.board = [[0 for col in range(cols)] for row in range(rows)]
        self.connect_length = connect_length

    def print(self):
        for row in self.board:
            print(f"| {' '.join(list(map(str, row)))} |")
        print("_" * (2 + 2 * len(self.board[0])))

    # adds a checker to a specific column
    def add_checker(self, col: int, insert_value: int) -> None:
        # error handling
        if insert_value != 1 or insert_value != 2:
            raise Exception(f"Insert Value should not be {insert_value} of type {type(insert_value)}")

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

        for current_player in [1, 2]:
            if check_vertical() or check_horizontal() or check_diagonal():
                return current_player

        return 0

    # returns a list of open columns
    def give_open_cols(self) -> list:
        open_cols = []

        # iterates through the columns of the board
        for x_col in range(len(self.board[0])):
            # if the top value is 0, then that means that there's still spaces
            if self.board[0][x_col] == 0:
                open_cols += [x_col]

        return open_cols