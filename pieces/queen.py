"""
pieces/queen.py — STUDENT TASK

Implement the Queen class.
"""

from .piece import Piece
from .rook import Rook
from .bishop import Bishop


class Queen(Piece):
    """A queen — combines the movement of a rook and a bishop.

    OOP concept: COMPOSITION
        Instead of re-implementing sliding logic, the Queen creates helper
        Rook and Bishop instances and delegates to their get_valid_moves.
        This is "composition" — building complex behaviour by combining
        simpler objects — rather than copy-pasting code.

    Implementation hint:
        Create a Rook and a Bishop of the same color as helper objects.
        Call get_valid_moves on each with the same (board, row, col) arguments,
        then combine the two lists.

        self._rook_helper   = Rook(self.color)
        self._bishop_helper = Bishop(self.color)

        You can create these helpers in __init__ for reuse, or directly inside
        get_valid_moves — both approaches work.
    """

    def __init__(self, color: str) -> None:
        # TODO: call the parent constructor
        # TODO: optionally create self._rook_helper and self._bishop_helper here
        raise NotImplementedError

    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal moves for this queen.

        Delegate to Rook and Bishop helpers and combine their results.

        Args:
            board: Board instance
            row:   current row
            col:   current column

        Returns:
            List of (row, col) destination squares.
        """
        # TODO: delegate to Rook and Bishop helpers
        raise NotImplementedError
