import pygame
import pygame_gui
import logging
import copy
from pygame_gui.elements.ui_text_box import UITextBox

from constants import COLOR_WHITE, COLOR_BLACK, BOARD_WIDTH, SQUARE_SIZE, TEXTBOX_WIDTH, INITIAL_TEXT
from board import Position, Board, Piece, Move, Tile
from drawing import draw_board


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger()


def get_tile_from_mouse(mouse_pos, board):
    x, y = mouse_pos
    y = BOARD_WIDTH - y
    return board.get(x // SQUARE_SIZE, y // SQUARE_SIZE)


def print_moves(moves):
    return ''.join(['<p><font color="#%02x%02x%02x">%d. %s</font></p>' %
                    (*(COLOR_WHITE if i % 2 else COLOR_BLACK), i, m) for i, m in enumerate(moves, 1)])


def move_piece(board: Board, piece: Piece, new_tile: Tile, moves: list[Move]):
    prev_position = board.current_position
    LOGGER.info("Move %s to %s", piece, new_tile)
    moves.append(Move(piece.position, new_tile))
    new_position = copy.copy(prev_position)
    new_position.move_piece(piece, new_tile)
    board.positions.append(new_position)


class Game:
    def __init__(self):
        self.running = True
        self.prev_clicked_tile = None
        self.prev_clicked_piece = None
        self.moves = []
        self.board = Board()
        self.board.set_initial_position(Position(self.board))

        pygame.init()
        pygame.display.set_caption("Checkers")
        self.board_ui = pygame.display.set_mode((BOARD_WIDTH + TEXTBOX_WIDTH, BOARD_WIDTH))
        self.board_ui.fill(COLOR_WHITE)
        draw_board(self.board_ui, self.board)

        self.ui_manager = pygame_gui.UIManager((BOARD_WIDTH + TEXTBOX_WIDTH, BOARD_WIDTH))
        self.logger_ui = UITextBox(html_text=INITIAL_TEXT,
                                   relative_rect=pygame.Rect(BOARD_WIDTH, 0, TEXTBOX_WIDTH, BOARD_WIDTH),
                                   manager=self.ui_manager)
        self.ui_manager.update(0.01)
        self.ui_manager.draw_ui(window_surface=self.board_ui)
        pygame.display.update()

    def handle_piece_move(self, clicked_tile):
        move_piece(self.board, self.prev_clicked_piece, clicked_tile, self.moves)
        draw_board(self.board_ui, self.board)
        self.logger_ui.set_text(INITIAL_TEXT + print_moves(self.moves))
        self.ui_manager.draw_ui(self.board_ui)
        pygame.display.update()
        self.prev_clicked_piece = self.prev_clicked_tile = None

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    tile = get_tile_from_mouse(pygame.mouse.get_pos(), self.board)
                    if self.player_wants_to_move_piece(tile):
                        self.handle_piece_move(tile)
                    else:
                        self.prev_clicked_tile = tile
                        self.prev_clicked_piece = self.board.current_position.pieces.get(tile)

                elif event.type == pygame.MOUSEBUTTONUP:
                    tile = get_tile_from_mouse(pygame.mouse.get_pos(), self.board)
                    if self.player_wants_to_move_piece(tile):
                        self.handle_piece_move(tile)

    def player_wants_to_move_piece(self, tile):
        if pygame.mouse.get_pos()[0] > BOARD_WIDTH:
            return False
        piece = self.board.current_position.pieces.get(tile)
        LOGGER.debug("Released on tile %s, on piece %s", tile, piece)
        LOGGER.debug("self.prev_clicked_tile = %s and self.prev_clicked_piece = %s",
                     self.prev_clicked_tile, self.prev_clicked_piece)
        return self.prev_clicked_tile and self.prev_clicked_piece and tile != self.prev_clicked_tile


if __name__ == "__main__":
    game = Game()
    game.start()
