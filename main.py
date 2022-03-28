import pygame
import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox

import logging

from constants import COLOR_WHITE, COLOR_BLACK, BOARD_WIDTH, SQUARE_SIZE, TEXTBOX_WIDTH, INITIAL_TEXT, BOUNCE, FPS
from board import Position, Board, Move
from drawing import draw_board, draw_piece
from referee import Referee, move_piece

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def get_tile_from_mouse(mouse_pos, board):
    return board.get(mouse_pos[0] // SQUARE_SIZE, (BOARD_WIDTH - mouse_pos[1]) // SQUARE_SIZE)


def print_moves(moves):
    return ''.join(['<p><font color="#%02x%02x%02x">%d. %s</font></p>' %
                    (*(COLOR_WHITE if i % 2 else COLOR_BLACK), i, m) for i, m in enumerate(moves, 1)])


class Game:
    def __init__(self):
        self.running = True
        self.prev_clicked_tile = None
        self.prev_clicked_piece = None
        self.moves = []
        self.board = Board()
        self.board.set_initial_position(Position(self.board))
        self.referee = Referee(self.board)
        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption("Checkers")
        self.board_ui = pygame.display.set_mode((BOARD_WIDTH + TEXTBOX_WIDTH, BOARD_WIDTH))

        self.ui_manager = pygame_gui.UIManager((BOARD_WIDTH + TEXTBOX_WIDTH, BOARD_WIDTH))
        self.logger_ui = UITextBox(html_text=INITIAL_TEXT,
                                   relative_rect=pygame.Rect(BOARD_WIDTH, 0, TEXTBOX_WIDTH, BOARD_WIDTH),
                                   manager=self.ui_manager)
        self.ui_manager.update(0.01)
        self.ui_manager.draw_ui(window_surface=self.board_ui)

    def handle_piece_move(self, clicked_tile):
        proposed_move = Move(self.prev_clicked_piece.position, clicked_tile)
        LOGGER.info('Proposed move - %s' % (proposed_move,))
        for move in self.referee.get_all_possible_moves():
            if move == proposed_move:
                move_piece(self.board, move, self.moves)
                self.logger_ui.set_text(INITIAL_TEXT + print_moves(self.moves))
                self.ui_manager.draw_ui(self.board_ui)
                break
        self.prev_clicked_piece = self.prev_clicked_tile = None

    def start(self):
        while self.running:
            draw_board(self.board_ui, self.board)
            pieces_that_can_move = self.referee.get_all_pieces_that_can_move()
            pieces_that_cant_move = set(self.board.current_position.all_pieces()) - pieces_that_can_move
            for piece in pieces_that_cant_move:
                draw_piece(self.board_ui, piece)
            bounce = next(BOUNCE)
            for piece in pieces_that_can_move:
                draw_piece(self.board_ui, piece, bounce)
            pygame.display.update()
            self.clock.tick(FPS)
            self.handle_events()

    def handle_events(self):
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
        LOGGER.debug("Currently on tile %s, on piece %s", tile, piece)
        return self.prev_clicked_tile and self.prev_clicked_piece and tile != self.prev_clicked_tile


if __name__ == "__main__":
    game = Game()
    game.start()
