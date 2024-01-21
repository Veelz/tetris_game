import copy
import random

from board_state import BoardState
from constants import WIDTH, HEIGHT, PIECES_TYPES, ROTATION_ORDER, PIECES, FRAMES_PER_DROP, SECONDS_PER_FRAME
from enums.cell_state import CellState
from enums.game_phase import GamePhase
from enums.user_input_state import UserInputState
from game import Game
from piece_state import PieceState


class TetrisGameState(Game):
    # game data
    board_state: BoardState
    lines: list[bool]
    piece_state: PieceState
    game_phase: GamePhase
    user_input_state: UserInputState
    # score system and level
    start_level: int
    level: int
    cleared_lines_count: int
    score: int
    # timing
    time: float
    next_time_to_drop: float
    highlight_end_time: float

    def __init__(self, frame_rate: int = 60):
        super().__init__(frame_rate)
        self.initialize_board().initialize_timers()

    # region INITIALIZATION
    def initialize_board(self, start_level=0) -> 'TetrisGameState':
        self.board_state = BoardState(WIDTH, HEIGHT)
        self.game_phase = GamePhase.START
        self.start_level = start_level
        self.level = self.start_level
        self.cleared_lines_count = 0
        self.score = 0
        self.user_input_state = UserInputState.D_NONE

        self.keydown_event_handlers[UserInputState.D_NONE].append(self._handle_key_down)
        self.keydown_event_handlers[UserInputState.D_LEFT].append(self._handle_key_down)
        self.keydown_event_handlers[UserInputState.D_RIGHT].append(self._handle_key_down)
        self.keydown_event_handlers[UserInputState.D_DOWN].append(self._handle_key_down)
        self.keydown_event_handlers[UserInputState.D_ROTATE].append(self._handle_key_down)
        self.keydown_event_handlers[UserInputState.D_HARD_DROP].append(self._handle_key_down)

        return self

    def initialize_timers(self) -> 'TetrisGameState':
        self.time = 0.0
        self.next_time_to_drop = self.time + self._get_time_to_next_drop()
        self.highlight_end_time = self.time + 0.2
        return self
    # endregion END INITIALIZATION

    # region Public methods
    def spawn_piece(self):
        cell_type = random.choice(PIECES_TYPES)
        self.piece_state = PieceState(cell_type, 0, WIDTH // 2, ROTATION_ORDER[0])
        self.next_time_to_drop = self.time + self._get_time_to_next_drop()

    def merge_piece(self):
        piece = PIECES[self.piece_state.piece_type]
        for row in range(0, piece.side):
            for col in range(0, piece.side):
                piece_cell = piece.get_piece_cell(row, col, self.piece_state.rotation)
                if piece_cell != CellState.EMPTY:
                    board_row = self.piece_state.offset_row + row
                    board_col = self.piece_state.offset_col + col
                    self.board_state.set_matrix_cell(board_row, board_col, piece_cell)

    def soft_drop(self) -> bool:
        self.piece_state.offset_row += 1
        if not self.board_state.check_piece_valid(self.piece_state):
            self.piece_state.offset_row -= 1
            self.merge_piece()
            self.spawn_piece()
            return False
        self.next_time_to_drop = self.time + self._get_time_to_next_drop()
        return True

    def update(self):
        self.time += self.clock.get_time() / 1000.0
        match self.game_phase:
            case GamePhase.PLAYING:
                self._update_game_state(self.user_input_state)
            case GamePhase.CLEARING_LINE:
                self._update_game_line()
            case GamePhase.GAME_OVER:
                self._update_game_over(self.user_input_state)
            case GamePhase.START:
                self._update_game_start(self.user_input_state)
        super().update()
        self.user_input_state = UserInputState.D_NONE
    # endregion Public methods

    # region Protected methods
    def _get_time_to_next_drop(self):
        max_available_level = max(FRAMES_PER_DROP.keys())
        if self.level > max_available_level:
            self.level = max_available_level
        return FRAMES_PER_DROP[self.level] * SECONDS_PER_FRAME

    def _update_game_state(self, user_input_state: UserInputState):
        current_piece = copy.deepcopy(self.piece_state)
        match user_input_state:
            # Process rotation and movement
            case UserInputState.D_LEFT:
                current_piece.offset_col -= 1
            case UserInputState.D_RIGHT:
                current_piece.offset_col += 1
            case UserInputState.D_ROTATE:
                new_rotation_idx = (ROTATION_ORDER.index(current_piece.rotation) + 1) % len(ROTATION_ORDER)
                current_piece.rotation = ROTATION_ORDER[new_rotation_idx]

        if self.board_state.check_piece_valid(current_piece):
            self.piece_state = current_piece

        match user_input_state:
            # Process soft and hard drops
            case UserInputState.D_DOWN:
                self.soft_drop()
            case UserInputState.D_HARD_DROP:
                while self.soft_drop():
                    pass

        while self.time >= self.next_time_to_drop:
            self.soft_drop()

        self.board_state.find_filled_rows()
        if any(self.board_state.pending_lines):
            self.game_phase = GamePhase.CLEARING_LINE
            self.highlight_end_time = self.time + 0.2

        game_over_row = 0
        if not self.board_state.check_row_empty(game_over_row):
            self.game_phase = GamePhase.GAME_OVER

    def _compute_score(self, level: int, cleared_line_count: int):
        match cleared_line_count:
            case 1:
                return 40 * (level + 1)
            case 2:
                return 100 * (level + 1)
            case 3:
                return 300 * (level + 1)
            case 4:
                return 1200 * (level + 1)
            case _:
                return 0

    def _get_lines_for_next_level(self, start_level: int, level: int):
        level_up_limit = min(start_level * 10 + 1, max(100, start_level * 10 - 50))
        if level == start_level:
            return level_up_limit
        diff = level - start_level
        return level_up_limit + diff * 10

    def _update_game_line(self):
        if self.time >= self.highlight_end_time:
            pending_lines = self.board_state.clear_lines()
            self.cleared_lines_count += pending_lines
            self.score += self._compute_score(self.level, pending_lines)

            if self.cleared_lines_count >= self._get_lines_for_next_level(self.start_level, self.level):
                self.level += 1

            self.game_phase = GamePhase.PLAYING

    def _update_game_over(self, user_input_state: UserInputState):
        match user_input_state:
            case UserInputState.D_HARD_DROP:
                self.game_phase = GamePhase.START

    def _update_game_start(self, user_input_state: UserInputState):
        match user_input_state:
            case UserInputState.D_ROTATE:
                self.start_level += 1
            case UserInputState.D_DOWN:
                if self.start_level > 0:
                    self.start_level -= 1
            case UserInputState.D_HARD_DROP:
                self.initialize_board(self.start_level)
                self.spawn_piece()
                self.game_phase = GamePhase.PLAYING

    def _handle_key_down(self, user_input_state: UserInputState):
        self.user_input_state = user_input_state
    # endregion Protected methods


if __name__ == '__main__':
    TetrisGameState().run()
