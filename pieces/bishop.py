"""
pieces/bishop.py — STUDENT TASK

Implement the Bishop class.
"""

from .piece import Piece


class Bishop(Piece):
    """A bishop — slides any number of squares diagonally.

    Movement rules to implement in get_valid_moves:
      • Slide in 4 diagonal directions:
          up-left   (dr=-1, dc=-1)
          up-right  (dr=-1, dc=+1)
          down-left (dr=+1, dc=-1)
          down-right(dr=+1, dc=+1)
      • Same blocking rules as the Rook:
          - Stop (don't add) if you hit a friendly piece.
          - Add and stop if you hit an enemy piece.
          - Add and continue if the square is empty.

    Sliding hint:
        A clean approach is to loop over the four (dr, dc) direction pairs
        using a nested while loop — very similar to your Rook implementation.
    """

    def __init__(self, color: str) -> None:
        # TODO: call the parent constructor
        raise NotImplementedError

    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal moves for this bishop.

        Args:
            board: Board instance — use board.get_piece(r, c)
            row:   current row
            col:   current column

        Returns:
            List of (row, col) destination squares.
        """
        # TODO: implement bishop diagonal sliding movement (4 directions)
        raise NotImplementedError
