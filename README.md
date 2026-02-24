# Chess — OOP Assignment

A working chess game built with pygame. The engine, rendering, and input handling are already provided. **Your job is to implement the pieces and the board.**

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## What's provided (do not modify)

| File | Description |
|------|-------------|
| `main.py` | pygame initialisation and main loop |
| `game.py` | Click handling and game-state transitions |
| `renderer.py` | Draws the board, pieces, highlights, and status bar |
| `pieces/piece.py` | Abstract `Piece` base class |
| `pieces/__init__.py` | Re-exports all six piece classes |

## What you need to implement

### 1. Piece classes (`pieces/`)

Each file has a class skeleton with `TODO` comments. All six classes inherit from `Piece` and must implement:

- `__init__(self, color)` — call the parent constructor with `super().__init__(color)`
- `get_valid_moves(self, board, row, col)` — return a list of `(row, col)` tuples for every square this piece can legally move to (pseudo-legal; check-filtering is handled by the Board)

#### `pawn.py`
- Single push: one square forward if empty
- Double push: two squares forward from the starting rank if both squares are empty and the pawn has not moved yet (`self.has_moved == False`)
- Diagonal capture: one square diagonally forward if an enemy piece is there
- En-passant capture: diagonal forward to `board.en_passant_target` if it is not `None`
- Direction: white moves up (row decreases), black moves down (row increases)

#### `rook.py`
- Slides any number of squares up, down, left, or right
- Stops when it hits the edge, a friendly piece (don't add), or an enemy piece (add, then stop)

#### `knight.py`
- Jumps in an L-shape — 8 possible offsets: `(±1, ±2)` and `(±2, ±1)`
- Can jump over other pieces
- Valid destination: on the board and empty or enemy-occupied

#### `bishop.py`
- Slides any number of squares diagonally (4 directions)
- Same blocking rules as the rook

#### `queen.py`
- Combines rook + bishop movement
- **Use composition**: create a `Rook` and a `Bishop` helper, call their `get_valid_moves`, and combine the results — do not copy-paste sliding logic

#### `king.py`
- Moves one square in any of the 8 directions (if on the board and not friendly-occupied)
- **Castling** (implement in `_get_castling_moves`): legal when all of these hold:
  1. The king has not moved (`self.has_moved == False`)
  2. The king is not currently in check
  3. The rook in the corner exists and has not moved
  4. All squares between king and rook are empty
  5. The king does not pass through an attacked square
  - Kingside destination: `(row, 6)`; queenside destination: `(row, 2)`

---

### 2. `board.py`

The `Board` class owns the 8×8 grid and enforces all game rules.

**Grid layout:**
- `_grid[0]` = black's back rank (top of the screen)
- `_grid[7]` = white's back rank (bottom of the screen)

#### Methods to implement

| Method | Milestone | Description |
|--------|-----------|-------------|
| `_place_pieces()` | 1 | Fill the grid with pieces in their starting positions |
| `get_valid_moves(row, col)` | 2 | Get pseudo-legal moves from the piece, filter out moves that leave the king in check |
| `is_in_check(color)` | 2 | Return `True` if the king of the given color is attacked |
| `_find_king(color)` | 2 | Scan the grid and return the king's `(row, col)` |
| `_get_all_attacked_squares(color)` | 2 | Return all squares attacked by pieces of the given color — **call `piece.get_valid_moves` directly, not `self.get_valid_moves`** (avoid infinite recursion) |
| `make_move(from_sq, to_sq)` | 2 | Move a piece; handle en-passant capture, castling rook move, pawn promotion, en-passant target update, and turn flip |
| `_would_leave_in_check(from_sq, to_sq)` | 3 | Deep-copy the board, simulate the move, check if own king is in check |
| `_has_any_legal_move(color)` | 3 | Return `True` if the given color has at least one legal move |
| `is_checkmate(color)` | 3 | In check **and** no legal moves |
| `is_stalemate(color)` | 3 | Not in check **and** no legal moves |

#### Suggested milestones

**Milestone 1 — pieces move:**
Implement all six piece classes and `_place_pieces`. Run the game; pieces should appear and clicking a piece should (eventually) show its moves.

**Milestone 2 — legal moves & basic play:**
Implement `get_valid_moves`, `make_move`, `is_in_check`, `_find_king`, and `_get_all_attacked_squares`. Pieces should move correctly and the board should track whose turn it is.

**Milestone 3 — check, checkmate & stalemate:**
Implement `_would_leave_in_check`, `_has_any_legal_move`, `is_checkmate`, and `is_stalemate`. The game should now detect and display the end of the game.

---

## Key concepts practiced

| Concept | Where |
|---------|-------|
| **Inheritance** | All piece classes extend `Piece` |
| **Abstraction** | `Piece.get_valid_moves` is an `@abstractmethod` |
| **Encapsulation** | `Piece._color` is private; exposed via `@property` |
| **Polymorphism** | `Board` calls `piece.get_valid_moves()` without knowing the concrete type |
| **Composition** | `Queen` delegates to `Rook` and `Bishop` helper objects |

## Running the tests

```bash
python -m pytest test_place_piece.py
```
