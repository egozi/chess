"""
llm_opponent.py

LLM chess opponent using the Anthropic API.
Claude plays as Black; the human plays as White.

Requires:
    ANTHROPIC_API_KEY set in a .env file (see .env.example).
"""

import os
import threading

import pygame
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Custom pygame event fired when Claude's move arrives from the background thread
LLM_MOVE_EVENT = pygame.USEREVENT + 1

# Piece → single-character notation  (uppercase = White, lowercase = Black)
_PIECE_CHAR: dict[tuple[str, str], str] = {
    ("white", "King"):   "K",
    ("white", "Queen"):  "Q",
    ("white", "Rook"):   "R",
    ("white", "Bishop"): "B",
    ("white", "Knight"): "N",
    ("white", "Pawn"):   "P",
    ("black", "King"):   "k",
    ("black", "Queen"):  "q",
    ("black", "Rook"):   "r",
    ("black", "Bishop"): "b",
    ("black", "Knight"): "n",
    ("black", "Pawn"):   "p",
}

_FILES = "abcdefgh"


# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------

def _sq_to_alg(row: int, col: int) -> str:
    """Convert (row, col) → algebraic square name, e.g. (6, 4) → 'e2'."""
    return f"{_FILES[col]}{8 - row}"


def _alg_to_sq(s: str) -> tuple[int, int]:
    """Convert algebraic square name → (row, col), e.g. 'e7' → (1, 4)."""
    s = s.strip().lower()
    col = _FILES.index(s[0])
    row = 8 - int(s[1])
    return (row, col)


def _board_to_text(board) -> str:
    """Render the board as a readable ASCII grid for the prompt."""
    lines = ["  a b c d e f g h", "  ---------------"]
    for row in range(8):
        cells = []
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is None:
                cells.append(".")
            else:
                cells.append(_PIECE_CHAR.get((piece.color, type(piece).__name__), "?"))
        lines.append(f"{8 - row}|{' '.join(cells)}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

MOVE_PROMPT_TEMPLATE = """\
You are playing chess as Black against a human opponent who plays White.

Current board position (uppercase = White, lowercase = Black, '.' = empty):
{board}

Move history so far (format: <from>-<to>, alternating White then Black):
{history}

It is Black's turn.

Respond with ONLY your chosen move as two squares separated by a space.
Example valid responses:
    e7 e5
    g8 f6
    b8 c6

Requirements:
- The move must be fully legal for Black.
- Do not move to a square occupied by one of your own pieces.
- Do not leave your king in check after the move.
- Output nothing except the two squares (no explanation, no punctuation).
"""


# ---------------------------------------------------------------------------
# LLMOpponent
# ---------------------------------------------------------------------------

class LLMOpponent:
    """Wraps the Anthropic API to act as the Black player."""

    def __init__(self) -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Create a .env file — see .env.example for the format."
            )
        self._client = anthropic.Anthropic(api_key=api_key)
        self._history: list[str] = []   # full move log for the prompt
        self.thinking: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record_move(self, from_sq: tuple[int, int], to_sq: tuple[int, int]) -> None:
        """Record any move (human or LLM) to keep the prompt history accurate."""
        self._history.append(f"{_sq_to_alg(*from_sq)}-{_sq_to_alg(*to_sq)}")

    def request_move(self, board) -> None:
        """
        Ask Claude for a move asynchronously.

        Fires a ``LLM_MOVE_EVENT`` pygame event when the answer arrives.
        The event carries ``from_sq`` and ``to_sq`` attributes (both None on error).
        """
        self.thinking = True
        thread = threading.Thread(
            target=self._fetch_move, args=(board,), daemon=True
        )
        thread.start()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _fetch_move(self, board) -> None:
        try:
            history_text = (
                "\n".join(self._history) if self._history else "(game just started)"
            )
            prompt = MOVE_PROMPT_TEMPLATE.format(
                board=_board_to_text(board),
                history=history_text,
            )
            response = self._client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=16,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()

            # Tolerate common formats: "e7 e5", "e7e5", "e7-e5"
            normalised = raw.replace("-", " ").replace(",", " ").lower()
            parts = normalised.split()
            if len(parts) < 2:
                raise ValueError(f"Could not parse LLM response: {raw!r}")

            from_sq = _alg_to_sq(parts[0])
            to_sq   = _alg_to_sq(parts[1])
            self.record_move(from_sq, to_sq)

            pygame.event.post(
                pygame.event.Event(LLM_MOVE_EVENT, {"from_sq": from_sq, "to_sq": to_sq})
            )

        except Exception as exc:
            print(f"[LLMOpponent] {exc}")
            # Post a sentinel so the game can handle the failure gracefully
            pygame.event.post(
                pygame.event.Event(LLM_MOVE_EVENT, {"from_sq": None, "to_sq": None})
            )
        finally:
            self.thinking = False
