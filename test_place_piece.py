"""
test_place_piece.py — quick sanity check

Places one piece on a random empty square and prints the result.
Run with: python test_place_piece.py
"""

import random
from board import Board
from pieces import Rook  # swap this import to test other piece classes


piece_class = Rook    # change to Pawn, Knight, Bishop, Queen, or King
piece_color = "white"  # "white" or "black"

board = Board()

row = random.randint(0, 7)
col = random.randint(0, 7)

piece = piece_class(piece_color)
board._grid[row][col] = piece

retrieved = board.get_piece(row, col)

print(f"Placed:    {piece_class.__name__}({piece_color!r})")
print(f"Square:    row={row}, col={col}")
print(f"Retrieved: {retrieved}")
print(f"Color:     {retrieved.color}")
print(f"has_moved: {retrieved.has_moved}")
