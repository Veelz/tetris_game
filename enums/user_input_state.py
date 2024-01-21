from enum import Enum


class UserInputState(Enum):
    D_NONE = -1
    D_LEFT = 0
    D_RIGHT = 1
    D_DOWN = 2
    D_ROTATE = 3
    D_HARD_DROP = 4
