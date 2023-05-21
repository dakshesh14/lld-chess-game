# low level design for chess game

import uuid
from abc import ABC, abstractmethod


class MoveStrategy(ABC):

    def __init__(self,):
        pass

    @abstractmethod
    def valid_moves(self, board):
        pass


class BishopMoveDiagonal(MoveStrategy):

    def __init__(self, piece):
        self.piece = piece

    def valid_moves(self, board):
        current_position = board.get_position(self.piece)
        valid_moves = []

        # check top left diagonal
        i = current_position[0] - 1
        j = current_position[1] - 1
        while i >= 0 and j >= 0:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            i -= 1
            j -= 1

        # check top right diagonal
        i = current_position[0] - 1
        j = current_position[1] + 1
        while i >= 0 and j < board.size:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            i -= 1
            j += 1

        # check bottom left diagonal
        i = current_position[0] + 1
        j = current_position[1] - 1
        while i < board.size and j >= 0:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            i += 1
            j -= 1

        # check bottom right diagonal
        i = current_position[0] + 1
        j = current_position[1] + 1
        while i < board.size and j < board.size:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            i += 1
            j += 1

        return valid_moves


class RookeMoveHorizontal(MoveStrategy):

    def __init__(self, piece):
        self.piece = piece

    def valid_moves(self, board):
        current_position = board.get_position(self.piece)
        valid_moves = []

        # check left horizontal
        i = current_position[0]
        j = current_position[1] - 1
        while j >= 0:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            j -= 1

        # check right horizontal
        i = current_position[0]
        j = current_position[1] + 1
        while j < board.size:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            j += 1

        # check top vertical
        i = current_position[0] - 1
        j = current_position[1]
        while i >= 0:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            i -= 1

        # check bottom vertical
        i = current_position[0] + 1
        j = current_position[1]
        while i < board.size:
            if board.is_empty(i, j):
                valid_moves.append((i, j))
            else:
                if board.get_piece(i, j).color != self.piece.color:
                    valid_moves.append((i, j))
                break
            i += 1

        return valid_moves


# queen will use both bishop and rooke move strategies
class QueenMoveStrategy(MoveStrategy):

    def __init__(self, piece):
        self.piece = piece

    def valid_moves(self, board):
        valid_moves = []
        valid_moves.extend(
            BishopMoveDiagonal(self.piece).valid_moves(board)
        )
        valid_moves.extend(
            RookeMoveHorizontal(self.piece).valid_moves(board)
        )
        return valid_moves


class Piece(ABC):
    def __init__(self, color):
        self.id = uuid.uuid4()
        self.color = color

    @abstractmethod
    def move(self, board, destination):
        pass

    @abstractmethod
    def valid_moves(self, board):
        pass


class Rooke(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.move_strategy = RookeMoveHorizontal(self)

    def move(self, board, destination):
        if destination in self.valid_moves(board):
            board.remove_piece(self)
            board.add_piece(self, destination[0], destination[1])
        else:
            raise Exception("Invalid move")

    def valid_moves(self, board):
        return self.move_strategy.valid_moves(board)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.move_strategy = BishopMoveDiagonal(self)

    def move(self, board, destination):
        if destination in self.valid_moves(board):
            board.remove_piece(self)
            board.add_piece(self, destination[0], destination[1])
        else:
            raise Exception("Invalid move")

    def valid_moves(self, board):
        return self.move_strategy.valid_moves(board)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.move_strategy = QueenMoveStrategy(self)

    def move(self, board, destination):
        if destination in self.valid_moves(board):
            board.remove_piece(self)
            board.add_piece(self, destination[0], destination[1])
        else:
            raise Exception("Invalid move")

    def valid_moves(self, board):
        return self.move_strategy.valid_moves(board)


class Board:
    def __init__(self, size=8):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def is_empty(self, i, j):
        return self.board[i][j] is None

    def get_position(self, piece):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    continue

                if self.board[i][j].id == piece.id and self.board[i][j].color == piece.color:
                    return i, j

    def get_piece(self, i, j):
        return self.board[i][j]

    def add_piece(self, piece, i, j):
        self.board[i][j] = piece

    def remove_piece(self, piece):
        i, j = self.get_position(piece)
        self.board[i][j] = None

    def move_piece(self, piece, destination):
        i, j = self.get_position(piece)
        self.board[i][j] = None
        self.board[destination[0]][destination[1]] = piece


if __name__ == '__main__':
    board = Board()

    rooke = Rooke("white")
    board.add_piece(rooke, 0, 0)
    print(f"\n\n For Rooke at {board.get_position(rooke)}")
    print(rooke.valid_moves(board))

    bishop = Bishop("black")
    board.add_piece(bishop, 3, 3)
    print(f"\n\n For Bishop at {board.get_position(bishop)}")
    print(bishop.valid_moves(board))

    queen = Queen("white")
    board.add_piece(queen, 4, 4)
    print(f"\n\n For Queen at {board.get_position(queen)}")
    print(queen.valid_moves(board))
