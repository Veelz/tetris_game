from enum import Enum


class GamePhase(Enum):
    PLAYING = 0
    CLEARING_LINE = 1
    GAME_OVER = 2
    START = 3
