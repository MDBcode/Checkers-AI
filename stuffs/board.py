import pygame
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE, GRAY, BLUE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.blue_left = 8
        self.create_board()

    def draw_squares(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, GRAY, (row*SQUARE_SIZE,
                                                col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    if row < 2:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, BLUE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    """def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.blue_left -= 1"""

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        up = piece.row - 2
        down = piece.row + 2
        row = piece.row
        col = piece.col
        if piece.color == BLUE:
            moves.update(self._look_left(
                row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._look_right(
                row-1, max(row-3, -1), -1, piece.color, right))
            moves.update(self._look_forward(up, col))
            moves.update(self._look_backward(down, col))
        if piece.color == RED:
            moves.update(self._look_left(
                row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._look_right(
                row+1, min(row+3, ROWS), 1, piece.color, right))
            moves.update(self._look_forward(down, col))
            moves.update(self._look_backward(up, col))
        return moves

    def _look_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._look_left(
                        r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._look_right(
                        r+step, row, step, color, left+1, skipped=last))
                break
            # elif current.color == color:
                # break
            else:
                last = [current]
            left -= 1
        return moves

    def _look_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._look_left(
                        r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._look_right(
                        r+step, row, step, color, right+1, skipped=last))
                break
            # elif current.color == color:
                # break
            else:
                last = [current]
            right += 1

        return moves

    def _look_forward(self, forward, col):
        moves = {}
        """if color == BLUE:
            if forward < 0:
                return moves
            elif self.board[forward][col] == 0:
                moves[(forward, col)] = [(forward, col)]

        if color == RED:
            if forward >= ROWS:
                return moves
            elif self.board[forward][col] == 0:
                moves[(forward, col)] = [(forward, col)]"""
        if 0 <= forward < ROWS and self.board[forward][col] == 0:
            moves[(forward, col)] = [(forward, col)]

        return moves

    def _look_backward(self, backward, col):
        moves = {}
        if 0 <= backward < ROWS and self.board[backward][col] == 0:
            moves[(backward, col)] = [(backward, col)]
        return moves

    def winner(self):
        blue_count = red_count = 0
        for row in range(2):
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    piece = self.board[row][col]
                    if piece != 0 and piece.color == BLUE:
                        blue_count += 1

        if blue_count == ROWS:
            return "BLUE won!"

        for row in range(6, ROWS):
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    piece = self.board[row][col]
                    if piece != 0 and piece.color == RED:
                        red_count += 1

        if red_count == ROWS:
            return "RED won!"

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def sum_of_rows(self):
        total = 0
        for index, row in enumerate(self.board):
            for piece in row:
                if piece != 0:
                    total += index
        return total

    def evaluate(self):
        # return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
        return self.sum_of_rows()
