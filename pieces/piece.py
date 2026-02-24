"""
pieces/piece.py — PROVIDED (do not modify)

Abstract base class for all chess pieces.

OOP concepts demonstrated here:
  • Abstraction  — Piece is an ABC; get_valid_moves is @abstractmethod
  • Encapsulation — _color is private; exposed read-only via @property
  • Inheritance   — every piece subclass calls super().__init__(color)
  • Polymorphism  — Board calls piece.get_valid_moves() without knowing
                    which concrete class it has
"""

from abc import ABC, abstractmethod


class Piece(ABC):
    """Abstract base for all chess pieces.

    Subclasses MUST implement get_valid_moves.
    They should NOT store their own position — the Board is the source of
    truth for where a piece is.
    """

    def __init__(self, color: str) -> None:
        """
        Args:
            color: "white" or "black"
        """
        self._color = color          # private — use the property below
        self.has_moved: bool = False  # intentionally public; used for castling & pawns

    # ------------------------------------------------------------------
    # Encapsulation: read-only property
    # ------------------------------------------------------------------

    @property
    def color(self) -> str:
        """The piece's color: "white" or "black".  Read-only."""
        return self._color

    # ------------------------------------------------------------------
    # Abstract method — every subclass must override this
    # ------------------------------------------------------------------

    @abstractmethod
    def get_valid_moves(self, board, row: int, col: int) -> list[tuple[int, int]]:
        """Return all pseudo-legal destination squares for this piece.

        "Pseudo-legal" means geometrically valid (correct movement pattern,
        on the board, not blocked by a friendly piece) but NOT filtered for
        leaving the king in check — that filtering is done by the Board.

        Args:
            board: the Board instance (use board.get_piece(r, c) to inspect squares)
            row:   current row of this piece (0 = top / black back rank)
            col:   current column (0 = left / a-file)

        Returns:
            List of (row, col) tuples this piece can move to.
        """

    # ------------------------------------------------------------------
    # Concrete helpers available to all subclasses
    # ------------------------------------------------------------------

    def opponent_color(self) -> str:
        """Return the opposite color to this piece."""
        return "black" if self._color == "white" else "white"

    def is_on_board(self, row: int, col: int) -> bool:
        """Return True if (row, col) is a valid board square."""
        return 0 <= row < 8 and 0 <= col < 8
