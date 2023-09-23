from Board import Board
from random import choice
# from stable_baselines3 import A2C


for x in range(10):
    board = Board()
    while not board.done:
        for player in [1, 2]:
            board.add_checker(choice(board.give_open_cols()), player)
            winner = board.check_for_winner()

            if board.done:
                board.print()
                break

print(winner)
