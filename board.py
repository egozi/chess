"""
board.py — STUDENT TASK

Implement the Board class, which owns the 8×8 grid and all game logic.
"""

import copy
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from pieces.piece import Piece


class Board:
    """Represents the chess board and enforces all game rules.

    Grid layout:
        self._grid[0]  → black's back rank  (row 0 = top of the screen)
        self._grid[7]  → white's back rank  (row 7 = bottom of the screen)
        self._grid[r][c] is a Piece object or None.

    Important attributes:
        current_turn (str)          — "white" or "black"; whose move it is
        en_passant_target (tuple|None) — (row, col) of the square a pawn just
                                         skipped over after a double push, or
                                         None if en-passant is not available.
                                         Reset to None after every move except
                                         the double pawn push that creates it.

    Public API consumed by Game and Renderer (you must implement these):
        get_piece(row, col)         → Piece | None
        get_valid_moves(row, col)   → list[tuple[int,int]]
        make_move(from_sq, to_sq)   → None
        is_in_check(color)          → bool
        is_checkmate(color)         → bool
        is_stalemate(color)         → bool

    Private helpers you will also implement:
        _place_pieces()
        _would_leave_in_check(from_sq, to_sq)
        _get_all_attacked_squares(color)
        _has_any_legal_move(color)
        _find_king(color)
    """

    def __init__(self) -> None:
        """Initialise the board.

        Tasks:
          1. Create self._grid as an 8×8 list of lists filled with None.
          2. Set self.current_turn = "white".
          3. Set self.en_passant_target = None.
          4. Call self._place_pieces() to populate the grid.
        """
        self._grid: list[list[Piece | None]] = [[None] * 8 for _ in range(8)]
        self.current_turn: str = "white"
        self.en_passant_target: tuple[int, int] | None = None
        self._place_pieces()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_piece(self, row: int, col: int) -> Piece | None:
        """Return the piece at (row, col), or None if the square is empty.

        Args:
            row: 0–7
            col: 0–7
        """
        return self._grid[row][col]

    def get_valid_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        """Return fully legal moves for the piece at (row, col).

        Steps:
          1. Get the piece at (row, col). If None, return [].
          2. Ask the piece for its pseudo-legal moves:
                piece.get_valid_moves(self, row, col)
          3. Filter out any move that would leave the current player's king
             in check, using self._would_leave_in_check(from_sq, to_sq).
          4. Return the filtered list.

        Args:
            row: row of the piece
            col: column of the piece

        Returns:
            List of legal (row, col) destination squares.
        """
        # TODO: replace this stub with the full implementation
        piece = self._grid[row][col]
        if piece is None:
            return []
        # Milestone 2: call piece.get_valid_moves then filter with _would_leave_in_check
        raise NotImplementedError

    def make_move(self, from_sq: tuple[int, int], to_sq: tuple[int, int]) -> None:
        """Execute a move on the board, updating all relevant state.

        from_sq: (row, col) of the moving piece
        to_sq:   (row, col) of the destination

        Steps to implement (in order):
          1.  Unpack coordinates:
                fr, fc = from_sq
                tr, tc = to_sq
                piece  = self._grid[fr][fc]

          2.  En-passant capture:
                If the moving piece is a Pawn and to_sq == self.en_passant_target,
                remove the captured pawn.  The captured pawn sits on the SAME ROW
                as the moving pawn but the SAME COLUMN as the destination:
                    self._grid[fr][tc] = None

          3.  Castling — move the rook:
                If the moving piece is a King and abs(tc - fc) == 2, it's a castle.
                Kingside  (tc == 6): move rook from (fr, 7) to (fr, 5)
                Queenside (tc == 2): move rook from (fr, 0) to (fr, 3)
                Don't forget to set the rook's has_moved = True.

          4.  Move the piece:
                self._grid[tr][tc] = piece
                self._grid[fr][fc] = None
                piece.has_moved = True

          5.  Pawn promotion:
                If the moving piece is a Pawn and it has reached the far rank
                (row 0 for white, row 7 for black), replace it with a Queen:
                    self._grid[tr][tc] = Queen(piece.color)
                    self._grid[tr][tc].has_moved = True

          6.  Update en_passant_target:
                If a Pawn just made a double push (abs(tr - fr) == 2), set:
                    self.en_passant_target = ((fr + tr) // 2, tc)
                Otherwise set self.en_passant_target = None.

          7.  Flip the turn:
                self.current_turn = "black" if self.current_turn == "white" else "white"
        """
        # TODO: implement make_move following the steps above
        raise NotImplementedError

    def is_in_check(self, color: str) -> bool:
        """Return True if the king of the given color is currently in check.

        Steps:
          1. Find the king's position with self._find_king(color).
          2. Get all squares attacked by the opponent:
                attacked = self._get_all_attacked_squares(opponent_color)
          3. Return True if the king's square is in attacked.

        Args:
            color: "white" or "black"
        """
        # TODO: implement is_in_check (Milestone 2)
        return False

    def is_checkmate(self, color: str) -> bool:
        """Return True if the given color is in checkmate.

        Checkmate = in check AND no legal moves remain.

        Args:
            color: "white" or "black"
        """
        # TODO: implement is_checkmate (Milestone 3)
        return False

    def is_stalemate(self, color: str) -> bool:
        """Return True if the given color is in stalemate.

        Stalemate = NOT in check AND no legal moves remain.

        Args:
            color: "white" or "black"
        """
        # TODO: implement is_stalemate (Milestone 3)
        return False

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _place_pieces(self) -> None:
        """Populate self._grid with pieces in their starting positions.

        Starting layout (standard chess):

            Row 0 (black back rank):  R N B Q K B N R
            Row 1 (black pawns):      P P P P P P P P
            Rows 2–5:                 empty
            Row 6 (white pawns):      P P P P P P P P
            Row 7 (white back rank):  R N B Q K B N R

        The column order for the back rank is:
            col 0=Rook, 1=Knight, 2=Bishop, 3=Queen, 4=King, 5=Bishop, 6=Knight, 7=Rook

        Hint — one way to fill the back ranks:
            back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
            self._grid[0] = [cls("black") for cls in back_rank]
            self._grid[7] = [cls("white") for cls in back_rank]
        """
        # TODO: implement _place_pieces (Milestone 1 — do this after your pieces work)
        pass  # remove this line when you implement _place_pieces

    def _would_leave_in_check(
        self, from_sq: tuple[int, int], to_sq: tuple[int, int]
    ) -> bool:
        """Return True if making this move would leave the mover's king in check.

        Use copy.deepcopy(self) to simulate the move on a throwaway board,
        then call is_in_check on the copy.

        Steps:
          1. Determine the color of the moving piece.
          2. Deep-copy the board: test_board = copy.deepcopy(self)
          3. Simulate the move on test_board (minimal simulation is fine —
             just move the piece without worrying about en-passant/castling
             side effects, since we only need to check whether the king is safe):
                fr, fc = from_sq
                tr, tc = to_sq
                test_board._grid[tr][tc] = test_board._grid[fr][fc]
                test_board._grid[fr][fc] = None
          4. Return test_board.is_in_check(color).

        Args:
            from_sq: (row, col) of the moving piece
            to_sq:   (row, col) of the destination

        Returns:
            True if the king of the moving piece's color would be in check
            after this move.

        Note:
            This method intentionally does NOT call make_move (which has side
            effects). A direct grid manipulation is sufficient here because we
            only need to know whether the king ends up attacked.
        """
        # TODO: implement _would_leave_in_check using copy.deepcopy (Milestone 3)
        raise NotImplementedError

    def _get_all_attacked_squares(self, color: str) -> set[tuple[int, int]]:
        """Return the set of all squares attacked by pieces of the given color.

        CRITICAL: call piece.get_valid_moves(self, r, c) directly — do NOT
        call self.get_valid_moves(r, c).

        Why?  self.get_valid_moves filters moves with _would_leave_in_check,
        which calls is_in_check, which calls _get_all_attacked_squares — an
        infinite loop.  Using the piece's pseudo-legal moves directly breaks
        the cycle.

        Steps:
          1. Iterate every square on the board.
          2. If a piece of the given color is there, call:
                piece.get_valid_moves(self, r, c)
             and add all returned squares to a set.
          3. Return the set.

        Args:
            color: "white" or "black" — whose attacked squares to collect

        Returns:
            Set of (row, col) tuples.
        """
        # TODO: implement _get_all_attacked_squares (Milestone 2)
        raise NotImplementedError

    def _has_any_legal_move(self, color: str) -> bool:
        """Return True if the given color has at least one legal move.

        Steps:
          1. Temporarily set self.current_turn = color so that get_valid_moves
             works correctly for this color.
          2. Iterate all squares; for each piece of the given color call
             self.get_valid_moves(r, c).
          3. If any call returns a non-empty list, restore current_turn and
             return True.
          4. After the loop, restore current_turn and return False.

        Args:
            color: "white" or "black"
        """
        # TODO: implement _has_any_legal_move (Milestone 3)
        raise NotImplementedError

    def _find_king(self, color: str) -> tuple[int, int] | None:
        """Return the (row, col) of the king of the given color, or None.

        Scan self._grid and return the first square containing a King instance
        with the matching color.

        Args:
            color: "white" or "black"
        """
        # TODO: scan the grid for a King of the given color (Milestone 2)
        return None
