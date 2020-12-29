import math
import random

import numpy
from typing import List


class Game:
    _col: int
    _row: int
    _board: List[List[int]]

    def __init__(self, row: int, col: int):
        self._col = col
        self._row = row
        self._board = numpy.zeros((self._row, self._col), dtype=int)

    def get_board(self) -> List[List[int]]:
        return self._board

    def is_location_valid(self, col: int) -> bool:
        return self._board[0][col] == 0

    def make_move(self, row: int, col: int, player: int) -> List[List[int]]:
        self._board[row][col] = player
        return self._board

    def get_available_row(self, board: List[List[int]], col: int) -> int:
        n = self._row - 1
        if board is None:
            board = self._board
        while n >= 0:
            if board[n][col] == 0:
                return n
            else:
                n -= 1
        return n

    """Determine if there's a winner and return the winner code if there is
    Returns: -1 if there's no winner yet or winner code if there's a winner"""
    def is_there_winner(self, board: List[List[int]]) -> int:
        if board is None:
            board = self._board

        # horizontal
        for row in range(self._row):
            row_array = list(self._board[row])
            for col in range(0, self._col-3):
                window = row_array[col: col+4]
                if window.count(1)==4:
                    return 1
                if window.count(2)==4:
                    return 2

        # vertical
        for col in range(self._col):
            col_array = [int(i) for i in list(self._board[:, col])]
            for row in range(self._row-3):
                window = col_array[row: row+4]
                if window.count(1)==4:
                    return 1
                if window.count(2)==4:
                    return 2

        # diagonal
        for row in range(self._row-3):
            for col in range(self._col-3):
                window1 = [self._board[row+i][col+i] for i in range(4)]
                window2 = [self._board[row+3-i][col+i] for i in range(4)]
                if window1.count(1) == 4 or window2.count(1) == 4:
                    return 1
                if window1.count(2) == 4 or window2.count(2) == 4:
                    return 2

        return -1

    '''returns column number - the best move'''
    def pick_best_move(self, player: int) -> int:
        return self.minimax(self._board, 4, True)[1]

    def get_available_col(self) -> List[int]:
        available = []
        for col in range(self._col):
            if self.is_location_valid(col):
                available.append(col)
        return available

    def position_score(self, temp_board: List[List[int]], player: int) -> int:
        score = 0

        # center
        center_array = [int(i) for i in list(temp_board[:, self._col//2])]
        score += center_array.count(player)*6

        # horizontal
        for row in range(self._row):
            row_array = list(temp_board[row])
            for col in range(0, self._col-3):
                window = row_array[col: col+4]
                score += self.score_calculator(window, player)

        # vertical
        for col in range(self._col):
            col_array = list(temp_board[:, col])
            for row in range(self._row-3):
                window = col_array[row: row+4]
                score += self.score_calculator(window, player)

        # diagonal / \
        for row in range(self._row-3):
            for col in range(self._col-3):
                window1 = [temp_board[row+3-i][col+i] for i in range(4)]
                window2 = [temp_board[row+i][col+i] for i in range(4)]
                score += self.score_calculator(window1, player)
                score += self.score_calculator(window2, player)

        return score

    def score_calculator(self, window: List[int], player: int) -> int:
        score = 0
        if window.count(player) == 4:
            score += 1000
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 5

        opponent = (player % 2)+1
        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 800

        return score

    '''minimax algorithm'''
    def minimax(self, board:List[List[int]], depth:int, maximizing_player:bool):
        valid_locations = self.get_available_col()  # children nodes

        # Heuristic value of node
        if depth == 0:
            return self.position_score(board, 2), None
        if self.is_terminal_node(board):
            if self.is_there_winner() == 1:
                return 10000000000000, None
            elif self.is_there_winner() == 2:
                return -10000000000000, None
            else:  # no more moves possible
                return 0, None
        if maximizing_player:
            max_value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row(board, col)
                temp_board = board.copy()
                temp_board[row][col] = 2
                new_score = self.minimax(temp_board, depth-1, False)[0]
                if max_value < new_score:
                    max_value = new_score
                    best_col = col
            return max_value, best_col
        else:  # minimizing player
            min_value = math.inf
            for col in valid_locations:
                row = self.get_available_row(board, col)
                temp_board = board.copy()
                temp_board[row][col] = 1
                new_score = self.minimax(temp_board, depth-1, False)[0]
                if min_value > new_score:
                    min_value = new_score
                    best_col = col
            return min_value, best_col

    '''used for minimax method. Tells whether the game is over
    Game is over when there are no more columns to drop a piece in or if there 
    is a winner
    @return whether the game is over'''
    def is_terminal_node(self, board: List[List[int]]):
        return len(self.get_available_col()) == 0 or self.is_there_winner(board) != -1
