from enums.cell_state import CellState
from enums.rotation import Rotation


class Piece:
    data: list[CellState]
    side: int

    def __init__(self, data: list[int], side: int):
        self.data = [CellState(cell) for cell in data]
        self.side = side

    def get_piece_cell(self, row: int, col: int, rotation: Rotation) -> CellState:
        match rotation:
            case Rotation.CLOCKWISE_90:
                return self.data[(self.side - col - 1) * self.side + row]
            case Rotation.CLOCKWISE_180:
                return self.data[(self.side - row - 1) * self.side + (self.side - col - 1)]
            case Rotation.CLOCKWISE_270:
                return self.data[col * self.side + (self.side - row - 1)]
            case _:
                return self.data[col + row * self.side]
