import pygame
import pygame_gui
import logging
import copy
from pygame_gui.elements.ui_text_box import UITextBox

from constants import COLOR_WHITE, COLOR_BLACK, COLOR_GREY, BOARD_WIDTH, SQUARE_SIZE, \
    PIECE_PADDING, PIECE_OUTLINE, CROWN_SIZE, TEXTBOX_WIDTH
from board import Position, Board, Piece, Move


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

CROWN = pygame.image.load('assets/crown.gif')


def draw_board(window, board, position):
    bg = pygame.image.load("assets/checkers.png")
    window.blit(bg, (0, 0))
    for tile in board.tiles.values():
        sign_tile(window, tile)
    for piece in position.all_pieces():
        draw_piece(window, piece)


def sign_tile(win, tile):
    if tile.black:
        font = pygame.font.SysFont("Calibri", 12)
        img = font.render('%s' % (tile.name,), True, COLOR_GREY)
        win.blit(img, (tile.x * (SQUARE_SIZE + 1), tile.y * (SQUARE_SIZE + 1)))


def draw_piece(win, piece):
    radius = SQUARE_SIZE // 2 - PIECE_PADDING
    pygame.draw.circle(win, COLOR_GREY,
                       (piece.x * SQUARE_SIZE + SQUARE_SIZE // 2, piece.y * SQUARE_SIZE + SQUARE_SIZE // 2),
                       radius + PIECE_OUTLINE)
    pygame.draw.circle(win, COLOR_BLACK if piece.black else COLOR_WHITE,
                       (piece.x * SQUARE_SIZE + SQUARE_SIZE // 2, piece.y * SQUARE_SIZE + SQUARE_SIZE // 2),
                       radius)
    if piece.king:
        win.blit(CROWN, (piece.x * SQUARE_SIZE + SQUARE_SIZE // 2 - CROWN_SIZE // 2,
                         piece.y * SQUARE_SIZE + SQUARE_SIZE // 2 - CROWN_SIZE // 2))


def get_tile_from_mouse(mouse_pos, position):
    x, y = mouse_pos
    y = BOARD_WIDTH - y
    board = position.board
    return board.get(x // SQUARE_SIZE, y // SQUARE_SIZE)


def print_moves(moves):
    return '<br>'.join(['%d. %s' % (i, m) for i, m in enumerate(moves, 1)])


def move_piece(window, text_box, piece: Piece, new_tile, positions, moves):
    prev_position = positions[-1]
    LOGGER.info("Move %s to %s", piece, new_tile)
    new_position = copy.copy(prev_position)
    moves.append(Move(piece.position, new_tile))
    new_position.move_piece(piece, new_tile)
    positions.append(new_position)
    draw_board(window, positions[-1].board, positions[-1])
    text_box.set_text('Welcome!<br>' + print_moves(moves))


def start_game():
    pygame.init()
    window = pygame.display.set_mode((BOARD_WIDTH + TEXTBOX_WIDTH, BOARD_WIDTH))
    pygame.display.set_caption("Checkers")

    board = Board()
    positions = [Position(board)]
    moves = []

    window.fill(COLOR_WHITE)
    draw_board(window, board, positions[-1])

    ui_manager = pygame_gui.UIManager((BOARD_WIDTH + TEXTBOX_WIDTH, BOARD_WIDTH))
    text_box = UITextBox(
        html_text="Welcome!",
        relative_rect=pygame.Rect(BOARD_WIDTH, 0, TEXTBOX_WIDTH, BOARD_WIDTH),
        manager=ui_manager)
    ui_manager.update(0.01)
    ui_manager.draw_ui(window_surface=window)
    pygame.display.update()

    running = True
    prev_clicked_tile = None
    prev_clicked_piece = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] > BOARD_WIDTH:
                    continue
                clicked_tile = get_tile_from_mouse(pygame.mouse.get_pos(), positions[-1])
                clicked_piece = positions[-1].pieces.get(clicked_tile)
                LOGGER.debug("Clicked on tile %s, on piece %s", clicked_tile, clicked_piece)
                if prev_clicked_tile and prev_clicked_piece and prev_clicked_tile != clicked_tile:
                    move_piece(window, text_box, prev_clicked_piece, clicked_tile, positions, moves)
                    ui_manager.draw_ui(window)
                    pygame.display.update()
                    prev_clicked_piece = prev_clicked_tile = None
                elif prev_clicked_tile is None:
                    prev_clicked_tile = clicked_tile
                    prev_clicked_piece = clicked_piece
                else:
                    prev_clicked_piece = prev_clicked_tile = None
            elif event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pos()[0] > BOARD_WIDTH:
                    continue
                released_tile = get_tile_from_mouse(pygame.mouse.get_pos(), positions[-1])
                released_piece = positions[-1].pieces.get(released_tile)
                LOGGER.debug("Released on tile %s, on piece %s", released_tile, released_piece)

                if prev_clicked_tile and released_tile != prev_clicked_tile and prev_clicked_piece:
                    move_piece(window, text_box, prev_clicked_piece, released_tile, positions, moves)
                    ui_manager.draw_ui(window)
                    pygame.display.update()
                    prev_clicked_piece = prev_clicked_tile = None


if __name__ == "__main__":
    start_game()

