"""
pieces/knight.py — STUDENT TASK

Implement the Knight class.
"""

from .piece import Piece


class Knight(Piece):
    """A knight — jumps in an L-shape, ignoring pieces in between.

    Movement rules to implement in get_valid_moves:
      • 8 possible offsets (±1, ±2) and (±2, ±1) from the current square.
      • A destination is valid if it is on the board AND is either empty or
        occupied by an enemy piece.
      • Knights are the only piece that can jump over other pieces — no
        sliding loop needed.

    Offset hint:
        OFFSETS = [
            (-2, -1), (-2,  1),
            (-1, -2), (-1,  2),
            ( 1, -2), ( 1,  2),
            ( 2, -1), ( 2,  1),
        ]
        For each (dr, dc) in OFFSETS, check (row + dr, col + dc).
    """

    def __init__(self, color: str) -> None:
        # TODO: call the parent constructor
        raise NotImplementedError

    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal moves for this knight.

        Args:
            board: Board instance — use board.get_piece(r, c)
            row:   current row
            col:   current column

        Returns:
            List of (row, col) destination squares.
        """
        # TODO: implement knight L-shape movement (8 offsets, no blocking)
        raise NotImplementedError
