import copy
import sys
from collections import defaultdict

import pygame as pg

from board_state import BoardState
from constants import WIDTH, HEIGHT, GRID_SIZE, WINDOW_SIZE, KEYBOARD_CONFIGURATION, PIECES, BASE_COLOR, \
    LIGHT_COLOR, DARK_COLOR
from enums.cell_state import CellState
from enums.game_phase import GamePhase
from enums.text_alignment import TextAlignment
from enums.user_input_state import UserInputState
from piece_state import PieceState
from tetris_game_state import TetrisGameState


class Game:
    def __init__(self, frame_rate):
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.frame_rate = frame_rate
        self.font = pg.font.SysFont('Calibri', 36)
        self.is_running = True
        self.game_objects = []
        self.keydown_event_handlers = defaultdict(list)

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.is_running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                keyboard_input = KEYBOARD_CONFIGURATION.get(event.key, UserInputState.D_NONE)
                for handler in self.keydown_event_handlers[keyboard_input]:
                    handler(keyboard_input)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

            pg.display.flip()
            self.clock.tick(self.frame_rate)

    def update(self):
        for game_object in self.game_objects:
            game_object.update()

    def render(self):
        # refactor this
        render(self.screen, self.font, self, HEIGHT, WIDTH)


# region RENDER
def draw_cell(surface: pg.Surface, cell: CellState, col: int, row: int, offset_x: int, offset_y: int,
              outline: bool = False):
    edge = GRID_SIZE // 8
    x = offset_x + col * GRID_SIZE
    y = offset_y + row * GRID_SIZE

    outer_rect = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)
    nested_rect = pg.Rect(x + edge, y, GRID_SIZE - edge, GRID_SIZE - edge)
    inner_rect = pg.Rect(x + edge, y + edge, GRID_SIZE - 2 * edge, GRID_SIZE - 2 * edge)

    if outline:
        pg.draw.rect(surface, BASE_COLOR[cell], outer_rect, 1)
        return

    pg.draw.rect(surface, DARK_COLOR[cell], outer_rect)
    pg.draw.rect(surface, LIGHT_COLOR[cell], nested_rect)
    pg.draw.rect(surface, BASE_COLOR[cell], inner_rect)


def draw_piece(surface: pg.Surface, piece_state: PieceState,
               offset_col: int, offset_row: int, offset_x: int, offset_y: int, outline: bool = False):
    piece = PIECES[piece_state.piece_type]
    for row in range(0, piece.side):
        for col in range(0, piece.side):
            board_col = offset_col + col
            board_row = offset_row + row
            piece_cell = piece.get_piece_cell(row, col, piece_state.rotation)
            if piece_cell != CellState.EMPTY:
                draw_cell(surface, piece_cell, board_col, board_row, offset_x, offset_y, outline)


def draw_board(surface: pg.Surface, board_state: BoardState, height: int, width: int, offset_x: int, offset_y: int):
    for row in range(0, height):
        for col in range(0, width):
            cell = board_state.get_matrix_cell(row, col)
            draw_cell(surface, cell, col, row, offset_x, offset_y)


def draw_text(surface: pg.Surface, font: pg.font.Font, text: str, x: int, y: int,
              text_align: TextAlignment = TextAlignment.LEFT):
    dst_surface_rect = surface.get_rect()
    text_surface = font.render(text, True, (220, 220, 220))
    match text_align:
        case TextAlignment.CENTER:
            text_rect = text_surface.get_rect(center=(dst_surface_rect.width // 2, y))
        case TextAlignment.RIGHT:
            text_rect = text_surface.get_rect(topright=(x, y))
        case _:
            # TextAlignment.LEFT
            text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)


def render(surface: pg.Surface, font: pg.font.Font, game_state: TetrisGameState, height: int, width: int):
    surface.fill((0, 0, 0))
    padding_y = 120
    draw_board(surface, game_state.board_state, height, width, 0, padding_y)
    match game_state.game_phase:
        case GamePhase.PLAYING:
            draw_piece(surface, game_state.piece_state,
                       game_state.piece_state.offset_col, game_state.piece_state.offset_row, 0, padding_y)
            shadow_piece_state = copy.copy(game_state.piece_state)
            while game_state.board_state.check_piece_valid(shadow_piece_state):
                shadow_piece_state.offset_row += 1
            shadow_piece_state.offset_row -= 1
            draw_piece(surface, shadow_piece_state,
                       shadow_piece_state.offset_col, shadow_piece_state.offset_row, 0, padding_y, True)

        case GamePhase.CLEARING_LINE:
            for row in range(HEIGHT):
                if game_state.board_state.pending_lines[row]:
                    pg.draw.rect(surface, (255, 255, 255), pg.Rect(0, padding_y + row * GRID_SIZE,
                                                                   WIDTH * GRID_SIZE, GRID_SIZE))

        case GamePhase.GAME_OVER:
            rect = surface.get_rect()
            x, y = rect.center
            draw_text(surface, font, 'GAME OVER', x, padding_y + y, TextAlignment.CENTER)

        case GamePhase.START:
            rect = surface.get_rect()
            x, y = rect.center
            draw_text(surface, font, 'PRESS START', x, padding_y + y, TextAlignment.CENTER)
            draw_text(surface, font, f'Select level: {game_state.start_level}',
                      x, padding_y + y + 40, TextAlignment.CENTER)

    draw_text(surface, font, f'LEVEL {game_state.level}', 5, 5)
    draw_text(surface, font, f'Score: {game_state.score}', 5, 40)
    draw_text(surface, font, f'Lines count: {game_state.cleared_lines_count}', 5, 80)
# endregion RENDER
