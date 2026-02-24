"""
pieces/king.py — STUDENT TASK

Implement the King class.
"""

from .piece import Piece


class King(Piece):
    """A king — moves one square in any direction, plus castling.

    Basic movement (implement in get_valid_moves):
      • 8 offsets: (dr, dc) for dr in [-1,0,1] for dc in [-1,0,1], skip (0,0)
      • A destination is valid if it is on the board AND is either empty or
        occupied by an enemy piece.

    Castling (implement in _get_castling_moves):
      Castling is legal when ALL of the following are true:
        1. self.has_moved == False  (king has never moved)
        2. The king is NOT currently in check
           (use board.is_in_check(self.color))
        3. A rook is in the corner square:
              kingside  → (row, 7)
              queenside → (row, 0)
        4. That rook has has_moved == False
        5. All squares between the king and the rook are empty
        6. The king does NOT pass through a square that is under attack
           (use board._get_all_attacked_squares(self.opponent_color()))

      Castling destinations:
        Kingside:  king moves to (row, 6)
        Queenside: king moves to (row, 2)

      Squares the king passes through (must not be attacked):
        Kingside:  (row, 5) and (row, 6)
        Queenside: (row, 3) and (row, 2)

      Squares that must be empty between king and rook:
        Kingside:  (row, 5) and (row, 6)
        Queenside: (row, 1), (row, 2), and (row, 3)

    Hint — how Board handles the rook after castling:
        You only return the king's destination square from get_valid_moves.
        Board.make_move detects castling (king moves 2 squares) and
        automatically moves the rook to its correct square.
    """

    def __init__(self, color: str) -> None:
        # TODO: call the parent constructor
        raise NotImplementedError

    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal moves for this king.

        Includes normal one-square moves AND castling moves.

        Args:
            board: Board instance — use board.get_piece(r, c),
                   board.is_in_check(color),
                   board._get_all_attacked_squares(color)
            row:   current row
            col:   current column

        Returns:
            List of (row, col) destination squares.
        """
        moves: list[tuple[int, int]] = []

        # TODO: add all 8 adjacent squares that are on the board and not
        #       occupied by a friendly piece

        # Add castling moves
        moves += self._get_castling_moves(board, row, col)

        return moves

    def _get_castling_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return castling destination squares (0, 1, or 2 entries).

        This is a private helper — called only by get_valid_moves.
        Keep the six castling conditions listed in the class docstring
        in mind as you implement this.

        Args:
            board: Board instance
            row:   king's current row
            col:   king's current column (should be 4 for a non-moved king)

        Returns:
            List of castling destination squares, e.g. [(row, 6)] or
            [(row, 2), (row, 6)] or [].
        """
        # TODO: implement castling detection
        return []
