"""
renderer.py — PROVIDED (do not modify)

Draws the board, pieces, overlays, and status bar using pygame.
No game logic lives here — it reads from game.board and game state only.

Unicode chess symbols used (renders correctly with Segoe UI Symbol / Noto fonts):
    White: ♔♕♖♗♘♙   Black: ♚♛♜♝♞♟
"""

import pygame

SQUARE_SIZE = 80
BOARD_SIZE = 8

LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOR = (255, 255, 0, 120)       # yellow, semi-transparent
CHECK_COLOR = (220, 50, 50, 160)          # red, semi-transparent
MOVE_DOT_COLOR = (100, 100, 100, 160)     # grey dot for empty squares
MOVE_RING_COLOR = (100, 100, 100, 160)    # grey ring for capture squares
STATUS_BG = (30, 30, 30)
STATUS_TEXT = (230, 230, 230)

# Map piece class name → unicode symbol for each color
PIECE_SYMBOLS: dict[str, dict[str, str]] = {
    "white": {
        "King":   "♔",
        "Queen":  "♕",
        "Rook":   "♖",
        "Bishop": "♗",
        "Knight": "♘",
        "Pawn":   "♙",
    },
    "black": {
        "King":   "♚",
        "Queen":  "♛",
        "Rook":   "♜",
        "Bishop": "♝",
        "Knight": "♞",
        "Pawn":   "♟",
    },
}


class Renderer:
    """Stateless renderer — call draw(game) every frame."""

    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._piece_font = self._load_piece_font(52)
        self._status_font = pygame.font.SysFont("sans", 22)

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def draw(self, game) -> None:
        self._draw_board()
        self._draw_overlays(game)
        self._draw_pieces(game.board)
        self._draw_status(game)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_piece_font(self, size: int) -> pygame.font.Font:
        """Try several font names that render Unicode chess glyphs well."""
        candidates = [
            "segoeuisymbol", "seguisym",           # Windows
            "notosans", "dejavusans",               # Linux
            "applesymbols", "helvetica",            # macOS
        ]
        for name in candidates:
            font = pygame.font.SysFont(name, size)
            # Quick sanity check: does it render a king glyph wider than a dot?
            w, _ = font.size("♔")
            if w > 10:
                return font
        return pygame.font.SysFont(None, size)  # fallback

    def _draw_board(self) -> None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                   SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self._screen, color, rect)

    def _draw_overlays(self, game) -> None:
        board = game.board

        # Highlight selected square
        if game.selected_square:
            self._draw_transparent_rect(*game.selected_square, SELECTED_COLOR)

        # Highlight king in check
        if board.is_in_check(board.current_turn):
            king_sq = board._find_king(board.current_turn)
            if king_sq:
                self._draw_transparent_rect(*king_sq, CHECK_COLOR)

        # Valid move indicators
        for (r, c) in game.valid_moves:
            target = board.get_piece(r, c)
            cx = c * SQUARE_SIZE + SQUARE_SIZE // 2
            cy = r * SQUARE_SIZE + SQUARE_SIZE // 2
            if target is None:
                # Dot for empty squares
                dot_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(dot_surf, MOVE_DOT_COLOR,
                                   (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 12)
                self._screen.blit(dot_surf, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            else:
                # Ring for capture squares
                ring_surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(ring_surf, MOVE_RING_COLOR,
                                   (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 2, 6)
                self._screen.blit(ring_surf, (c * SQUARE_SIZE, r * SQUARE_SIZE))

    def _draw_pieces(self, board) -> None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece(row, col)
                if piece is None:
                    continue
                symbol = PIECE_SYMBOLS.get(piece.color, {}).get(
                    type(piece).__name__, "?"
                )
                self._draw_piece_symbol(symbol, piece.color, row, col)

    def _draw_piece_symbol(self, symbol: str, color: str, row: int, col: int) -> None:
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        text_color = (255, 255, 255) if color == "white" else (30, 20, 10)

        # Black outline for contrast (render offset copies)
        outline_color = (0, 0, 0)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            outline = self._piece_font.render(symbol, True, outline_color)
            rect = outline.get_rect(center=(x + dx, y + dy))
            self._screen.blit(outline, rect)

        # Main glyph
        surf = self._piece_font.render(symbol, True, text_color)
        rect = surf.get_rect(center=(x, y))
        self._screen.blit(surf, rect)

    def _draw_transparent_rect(self, row: int, col: int,
                                color: tuple[int, int, int, int]) -> None:
        surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        surf.fill(color)
        self._screen.blit(surf, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def _draw_status(self, game) -> None:
        bar_rect = pygame.Rect(0, BOARD_SIZE * SQUARE_SIZE,
                               BOARD_SIZE * SQUARE_SIZE, 40)
        pygame.draw.rect(self._screen, STATUS_BG, bar_rect)
        text = self._status_font.render(game.status_message, True, STATUS_TEXT)
        self._screen.blit(text, (10, BOARD_SIZE * SQUARE_SIZE + 9))
