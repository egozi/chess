"""
game.py — PROVIDED (do not modify)

The Game class handles mouse input and drives state transitions.
It owns a Board instance and exposes the data that Renderer needs.

Public interface consumed by Renderer:
    game.board          — Board instance
    game.selected_square  — (row, col) | None
    game.valid_moves    — list[tuple[int,int]]
    game.game_over      — bool
    game.status_message — str
"""

from board import Board


class Game:
    """Manages click handling and the high-level game state machine."""

    def __init__(self) -> None:
        self.board = Board()
        self.selected_square: tuple[int, int] | None = None
        self.valid_moves: list[tuple[int, int]] = []
        self.game_over: bool = False
        self.status_message: str = ""
        self._update_status()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def handle_click(self, pos: tuple[int, int]) -> None:
        """Convert a pixel position to a board square and act on it."""
        if self.game_over:
            return

        col = pos[0] // 80
        row = pos[1] // 80
        if not (0 <= row < 8 and 0 <= col < 8):
            return  # click in status bar area

        clicked_piece = self.board.get_piece(row, col)

        if self.selected_square is None:
            # First click: select a piece that belongs to the current player
            if clicked_piece and clicked_piece.color == self.board.current_turn:
                self.selected_square = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)
        else:
            if (row, col) in self.valid_moves:
                # Second click on a legal destination: make the move
                self.board.make_move(self.selected_square, (row, col))
                self.selected_square = None
                self.valid_moves = []
                self._update_status()
            elif clicked_piece and clicked_piece.color == self.board.current_turn:
                # Re-select a different friendly piece
                self.selected_square = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)
            else:
                # Click on empty square or enemy with no valid move → deselect
                self.selected_square = None
                self.valid_moves = []

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _update_status(self) -> None:
        """Refresh status_message and game_over after each move."""
        turn = self.board.current_turn

        if self.board.is_checkmate(turn):
            winner = "White" if turn == "black" else "Black"
            self.status_message = f"Checkmate! {winner} wins."
            self.game_over = True
        elif self.board.is_stalemate(turn):
            self.status_message = "Stalemate! It's a draw."
            self.game_over = True
        elif self.board.is_in_check(turn):
            self.status_message = f"{turn.capitalize()} is in check!"
        else:
            self.status_message = f"{turn.capitalize()}'s turn"
