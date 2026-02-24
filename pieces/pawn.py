"""
pieces/pawn.py — STUDENT TASK

Implement the Pawn class.
"""

from .piece import Piece


class Pawn(Piece):
    """A pawn — the most complex piece despite its simple movement.

    Movement rules to implement in get_valid_moves:
      1. Single push  — one square forward if that square is empty.
      2. Double push  — two squares forward from the starting rank if BOTH
                        squares ahead are empty AND the pawn has not moved yet
                        (check self.has_moved).
      3. Diagonal capture — one square diagonally forward if an enemy piece
                            occupies that square.
      4. En-passant capture — diagonal forward to board.en_passant_target if
                              that attribute is not None.

    Direction hint:
        White pawns move UP the board (row decreases): direction = -1
        Black pawns move DOWN the board (row increases): direction = +1
        You can compute this with:
            direction = -1 if self.color == "white" else 1

    En-passant hint:
        board.en_passant_target is either None or a (row, col) tuple that
        marks the square a pawn just skipped over (the square "behind" a
        double-pushed pawn).  If your diagonal forward square equals
        board.en_passant_target, it is a valid capture — add it to your moves.
        The Board.make_move method handles actually removing the captured pawn.
    """

    def __init__(self, color: str) -> None:
        # TODO: call the parent constructor
        raise NotImplementedError

    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal moves for this pawn.

        Args:
            board: Board instance — use board.get_piece(r, c) and
                   board.en_passant_target
            row:   current row of this pawn
            col:   current column of this pawn

        Returns:
            List of (row, col) destination squares.
        """
        # TODO: implement pawn movement
        raise NotImplementedError
