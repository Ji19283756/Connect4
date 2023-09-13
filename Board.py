class Board:
    def __init__(self, rows=6, cols=7):
        # creates a board, each row should be a new reference
        self.board = [[0 for col in range(cols)] for row in range(rows)]

    def __str__(self):
        pass

    # adds a checker to a specific column
    def add_checker(self, col: int, insert_value: int) -> None:
        # starts from the bottom of the column and goes up
        for x_row in range(len(self.board) - 1, -1, -1):
            # moving up, if the current position is empty, then it will insert the checker value
            if self.board[x_row][col] == 0:
                self.board[x_row][col] = insert_value

        raise IndexError(f"Invalid Column Position {col}")



