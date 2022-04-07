import pygame  # type: ignore
from constants import COLOR_WHITE, COLOR_BLACK, COLOR_GREY, SQUARE_SIZE, \
    PIECE_PADDING, PIECE_OUTLINE, CROWN_SIZE, CROWN_IMG, CHECKERS_IMG, BOARD_WIDTH

CROWN = pygame.image.load(CROWN_IMG)


def draw_board(window, board):
    window.fill(COLOR_WHITE, (0, 0, BOARD_WIDTH, BOARD_WIDTH))
    bg = pygame.image.load(CHECKERS_IMG)
    window.blit(bg, (0, 0))
    for tile in board.tiles.values():
        sign_tile(window, tile)


def sign_tile(win, tile):
    if tile.black:
        font = pygame.font.SysFont("Calibri", 12)
        img = font.render('%s' % (tile.name,), True, COLOR_GREY)
        win.blit(img, (tile.x * (SQUARE_SIZE + 1), tile.y * (SQUARE_SIZE + 1)))


def draw_piece(win, piece, bounce=0):
    radius = SQUARE_SIZE // 2 - PIECE_PADDING
    bounce = -bounce if piece.black else bounce
    pygame.draw.circle(win, COLOR_GREY,
                       (piece.x * SQUARE_SIZE + SQUARE_SIZE // 2, piece.y * SQUARE_SIZE + SQUARE_SIZE // 2 + bounce),
                       radius + PIECE_OUTLINE)
    pygame.draw.circle(win, COLOR_BLACK if piece.black else COLOR_WHITE,
                       (piece.x * SQUARE_SIZE + SQUARE_SIZE // 2, piece.y * SQUARE_SIZE + SQUARE_SIZE // 2 + bounce),
                       radius)
    if piece.king:
        win.blit(CROWN, (piece.x * SQUARE_SIZE + SQUARE_SIZE // 2 - CROWN_SIZE // 2,
                         piece.y * SQUARE_SIZE + SQUARE_SIZE // 2 - CROWN_SIZE // 2 + bounce))
