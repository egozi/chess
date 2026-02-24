"""
pieces/__init__.py — PROVIDED (do not modify)

Convenience re-exports so the rest of the codebase can write:
    from pieces import Pawn, Rook, Knight, Bishop, Queen, King
"""

from .pawn import Pawn
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King

__all__ = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
