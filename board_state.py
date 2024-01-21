from constants import PIECES
from enums.cell_state import CellState
from piece_state import PieceState


class BoardState:
    board: list[CellState]
    width: int
    height: int
    pending_lines: list[bool]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [CellState.EMPTY for _ in range(width * height)]
        self.pending_lines = []

    def get_matrix_cell(self, row: int, col: int) -> CellState:
        return self.board[col + row * self.width]

    def set_matrix_cell(self, row: int, col: int, new_state: CellState):
        self.board[col + row * self.width] = new_state

    def check_row_filled(self, row: int) -> bool:
        return all([self.get_matrix_cell(row, col) != CellState.EMPTY
                    for col in range(0, self.width)])

    def check_row_empty(self, row: int) -> bool:
        return all([self.get_matrix_cell(row, col) == CellState.EMPTY
                    for col in range(0, self.width)])

    def find_filled_rows(self):
        self.pending_lines = [self.check_row_filled(row)
                              for row in range(0, self.height)]

    def clear_lines(self) -> int:
        src_row = self.height - 1
        for dst_row in reversed(range(self.height)):
            while src_row >= 0 and self.pending_lines[src_row]:
                src_row -= 1

            dst_start = dst_row * self.width
            src_start = src_row * self.width
            if src_row < 0:
                self.board[dst_start:dst_start + self.width] = [CellState.EMPTY] * self.width
            else:
                self.board[dst_start:dst_start + self.width] = self.board[src_start:src_start + self.width]
                src_row -= 1
        return self.pending_lines.count(True)

    def check_piece_valid(self, piece_state: PieceState) -> bool:
        piece = PIECES[piece_state.piece_type]
        for row in range(0, piece.side):
            for col in range(0, piece.side):
                cell_state = piece.get_piece_cell(row, col, piece_state.rotation)
                if cell_state != CellState.EMPTY:
                    board_row = piece_state.offset_row + row
                    board_col = piece_state.offset_col + col
                    if (board_row < 0) or (board_row >= self.height) or (board_col < 0) or (board_col >= self.width):
                        return False
                    if self.get_matrix_cell(board_row, board_col) != CellState.EMPTY:
                        return False
        return True
