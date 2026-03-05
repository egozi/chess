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

# Optional LLM opponent — gracefully disabled if .env / package is missing
try:
    from llm_opponent import LLMOpponent
    _llm_available = True
except Exception:
    _llm_available = False


class Game:
    """Manages click handling and the high-level game state machine."""

    def __init__(self) -> None:
        self.board = Board()
        self.selected_square: tuple[int, int] | None = None
        self.valid_moves: list[tuple[int, int]] = []
        self.game_over: bool = False
        self.status_message: str = ""

        # LLM opponent (Black). None when unavailable or API key not set.
        self._llm: "LLMOpponent | None" = None
        if _llm_available:
            try:
                self._llm = LLMOpponent()
            except ValueError as e:
                print(f"[Game] LLM opponent disabled: {e}")

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
                from_sq = self.selected_square
                to_sq   = (row, col)
                if self._llm:
                    self._llm.record_move(from_sq, to_sq)
                self.board.make_move(from_sq, to_sq)
                self.selected_square = None
                self.valid_moves = []
                self._update_status()
                # If the game is still running and it's now Black's turn, ask the LLM
                if self._llm and not self.game_over and self.board.current_turn == "black":
                    self.status_message = "Claude is thinking..."
                    self._llm.request_move(self.board)
            elif clicked_piece and clicked_piece.color == self.board.current_turn:
                # Re-select a different friendly piece
                self.selected_square = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)
            else:
                # Click on empty square or enemy with no valid move → deselect
                self.selected_square = None
                self.valid_moves = []

    def apply_llm_move(self, from_sq: tuple | None, to_sq: tuple | None) -> None:
        """Apply a move received from the LLM opponent (called from main loop)."""
        if self.game_over:
            return
        if from_sq is None or to_sq is None:
            self.status_message = "Claude couldn't find a move. Your turn."
            return
        legal = self.board.get_valid_moves(*from_sq)
        if to_sq in legal:
            self.board.make_move(from_sq, to_sq)
            self._update_status()
        else:
            self.status_message = "Claude made an illegal move. Your turn."

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
