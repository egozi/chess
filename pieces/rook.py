"""
pieces/rook.py — STUDENT TASK

Implement the Rook class.
"""

from .piece import Piece


class Rook(Piece):
    """A rook — slides any number of squares along ranks and files.

    Movement rules to implement in get_valid_moves:
      • Slide in 4 directions: up, down, left, right.
      • Keep going in each direction until:
          - You hit the edge of the board (stop, don't add), OR
          - You hit a friendly piece (stop, don't add), OR
          - You hit an enemy piece (add that square, then stop).

    Sliding hint:
        Use a loop with a step variable. For example, to slide upward:
            r = row - 1
            while r >= 0:
                piece = board.get_piece(r, col)
                if piece is None:
                    moves.append((r, col))
                elif piece.color != self.color:
                    moves.append((r, col))
                    break
                else:
                    break
                r -= 1
        Repeat for the other three directions.

    has_moved note:
        self.has_moved is inherited from Piece and is used by the King for
        castling detection.  You do not need to update it here — Board.make_move
        sets it to True after the rook moves.
    """

    def __init__(self, color: str) -> None:
        # TODO: call the parent constructor
        raise NotImplementedError

    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal moves for this rook.

        Args:
            board: Board instance — use board.get_piece(r, c)
            row:   current row
            col:   current column

        Returns:
            List of (row, col) destination squares.
        """
        # TODO: implement rook sliding movement (4 directions)
        raise NotImplementedError
