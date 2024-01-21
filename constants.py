import pygame as pg

from enums.cell_state import CellState
from enums.rotation import Rotation
from enums.user_input_state import UserInputState
from piece import Piece

WIDTH = 10
HEIGHT = 22
VISIBLE_HEIGHT = 20
GRID_SIZE = 30
WINDOW_SIZE = (300, 780)

KEYBOARD_CONFIGURATION = {
    pg.K_RIGHT: UserInputState.D_RIGHT,
    pg.K_LEFT: UserInputState.D_LEFT,
    pg.K_DOWN: UserInputState.D_DOWN,
    pg.K_UP: UserInputState.D_ROTATE,
    pg.K_SPACE: UserInputState.D_HARD_DROP
}

PIECES = {
    CellState.T_PIECE: Piece([0, 0, 0,
                              1, 1, 1,
                              0, 1, 0], 3),
    CellState.O_PIECE: Piece([2, 2,
                              2, 2], 2),
    CellState.L_PIECE: Piece([0, 3, 0,
                              0, 3, 0,
                              0, 3, 3], 3),
    CellState.J_PIECE: Piece([0, 4, 0,
                              0, 4, 0,
                              4, 4, 0], 3),
    CellState.Z_PIECE: Piece([5, 5, 0,
                              0, 5, 5,
                              0, 0, 0], 3),
    CellState.S_PIECE: Piece([0, 6, 6,
                              6, 6, 0,
                              0, 0, 0], 3),
    CellState.I_PIECE: Piece([0, 0, 0, 0,
                              7, 7, 7, 7,
                              0, 0, 0, 0,
                              0, 0, 0, 0], 4)
}

PIECES_TYPES = list(PIECES.keys())

ROTATION_ORDER = (Rotation.ZERO, Rotation.CLOCKWISE_90, Rotation.CLOCKWISE_180, Rotation.CLOCKWISE_270)

BASE_COLOR = {
    CellState.EMPTY: (40, 40, 40),
    CellState.T_PIECE: (45, 153, 153),
    CellState.O_PIECE: (153, 153, 45),
    CellState.L_PIECE: (153, 45, 153),
    CellState.J_PIECE: (45, 153, 81),
    CellState.Z_PIECE: (153, 45, 45),
    CellState.S_PIECE: (45, 99, 153),
    CellState.I_PIECE: (153, 99, 45)
}
LIGHT_COLOR = {
    CellState.EMPTY: (40, 40, 40),
    CellState.T_PIECE: (68, 229, 229),
    CellState.O_PIECE: (229, 229, 68),
    CellState.L_PIECE: (229, 68, 229),
    CellState.J_PIECE: (68, 229, 122),
    CellState.Z_PIECE: (229, 68, 68),
    CellState.S_PIECE: (68, 149, 229),
    CellState.I_PIECE: (229, 149, 68)
}
DARK_COLOR = {
    CellState.EMPTY: (40, 40, 40),
    CellState.T_PIECE: (30, 102, 102),
    CellState.O_PIECE: (102, 102, 30),
    CellState.L_PIECE: (102, 30, 102),
    CellState.J_PIECE: (30, 102, 54),
    CellState.Z_PIECE: (102, 30, 30),
    CellState.S_PIECE: (30, 66, 102),
    CellState.I_PIECE: (102, 66, 30)
}

# https://tetris.wiki/Tetris_(NES,_Nintendo)
FRAMES_PER_DROP = {
    0: 48,
    1: 43,
    2: 38,
    3: 33,
    4: 28,
    5: 23,
    6: 18,
    7: 13,
    8: 8
}
SECONDS_PER_FRAME = 1 / 60
