from enums.cell_state import CellState
from enums.rotation import Rotation


class PieceState:
    piece_type: CellState
    offset_row: int
    offset_col: int
    rotation: Rotation

    def __init__(self, piece_type: CellState, offset_row: int, offset_col: int, rotation: Rotation):
        self.piece_type = piece_type
        self.offset_row = offset_row
        self.offset_col = offset_col
        self.rotation = rotation
