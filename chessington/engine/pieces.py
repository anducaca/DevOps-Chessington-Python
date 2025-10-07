from __future__ import annotations
from abc import ABC, abstractmethod
from chessington.engine.data import Player, Square
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from chessington.engine.board import Board

class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player: Player):
        self.player = player

    def to_json(self) -> dict[str, Any]:
        return {
            "piece": self.__class__.__name__,
            "player": self.player._name_.lower()
        }

    @abstractmethod
    def get_available_moves(self, board: Board) -> List[Square]:
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board: Board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """
    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        if self.player == Player.WHITE:
            direction = 1   # White moves down
            starting_row = 1
        else:
            direction = -1  # Black moves up
            starting_row = 6

        # One square forward if empty
        one_forward = Square.at(current_square.row + direction, current_square.col)
        if board.get_piece(one_forward) is None:
            moves.append(one_forward)

            # Two squares forward if on starting row and both squares empty
            if current_square.row == starting_row:
                two_forward = Square.at(current_square.row + 2 * direction, current_square.col)
                if board.get_piece(two_forward) is None:
                    moves.append(two_forward)

        return moves

class Knight(Piece):
    """
    A class representing a chess knight.
    """
    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        # All 8 possible knight moves (row, col offsets)
        jumps = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]

        for dr, dc in jumps:
            new_row = current_square.row + dr
            new_col = current_square.col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8:  # stay on board
                target_square = Square.at(new_row, new_col)
                piece_at_target = board.get_piece(target_square)

                # Knight can move if square is empty or occupied by opponent
                if piece_at_target is None or piece_at_target.player != self.player:
                    moves.append(target_square)

        return moves


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """
    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        # Four diagonal directions (row, col offsets)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row = current_square.row
            new_col = current_square.col

            while True:
                new_row += dr
                new_col += dc

                # Stop if off the board
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target_square = Square.at(new_row, new_col)
                piece_at_target = board.get_piece(target_square)

                if piece_at_target is None:
                    moves.append(target_square)
                else:
                    # Can capture enemy, but stop afterwards
                    if piece_at_target.player != self.player:
                        moves.append(target_square)
                    break

        return moves





class Queen(Piece):
    """
    A class representing a chess queen.
    """
    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        # 8 directions: rook (straight) + bishop (diagonal)
        directions = [
            (-1, 0), (1, 0),   # vertical
            (0, -1), (0, 1),   # horizontal
            (-1, -1), (-1, 1), # diagonals
            (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            new_row = current_square.row
            new_col = current_square.col

            while True:
                new_row += dr
                new_col += dc

                # Stop if off the board
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target_square = Square.at(new_row, new_col)
                piece_at_target = board.get_piece(target_square)

                if piece_at_target is None:
                    moves.append(target_square)
                else:
                    # Can capture enemy, but stop afterwards
                    if piece_at_target.player != self.player:
                        moves.append(target_square)
                    break

        return moves


class King(Piece):
    """
    A class representing a chess king.
    """
    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        # All 8 possible directions (row, col offsets)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            new_row = current_square.row + dr
            new_col = current_square.col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8:  # stay on board
                target_square = Square.at(new_row, new_col)
                piece_at_target = board.get_piece(target_square)

                # Can move if square is empty or occupied by opponent
                if piece_at_target is None or piece_at_target.player != self.player:
                    moves.append(target_square)

        return moves
    
class Rook(Piece):
    """
    A class representing a chess rook.
    """
    def get_available_moves(self, board) -> List[Square]:
        current_square = board.find_piece(self)
        moves = []

        # Four straight directions (row, col offsets)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row = current_square.row
            new_col = current_square.col

            while True:
                new_row += dr
                new_col += dc

                # Stop if off the board
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target_square = Square.at(new_row, new_col)
                piece_at_target = board.get_piece(target_square)

                if piece_at_target is None:
                    moves.append(target_square)
                else:
                    # Can capture enemy, but stop afterwards
                    if piece_at_target.player != self.player:
                        moves.append(target_square)
                    break

        return moves    
    
