"""
Can parse:
'[FEN "B:W18,24,27,28,K10,K15:B12,16,20,K22,K25,K29"]'
'[FEN "B:W18,19,21,23,24,26,29,30,31,32:B1,2,3,4,6,7,9,10,11,12"]'
'[FEN "W:W32,27,24,22:B20,15,10,7"]'
But also:
'a7, b6, b8, c7, d6, d8, e7, f6, f8, g7, h6, h8'
"""
import re
from piece import Piece
from tile import Tile
from board import Board


PIECE_REGEXP = re.compile(r'(?P<is_king>K)?(?P<vertical>[A-H])?(?P<number>\d+)')
POSITION_REGEXP = re.compile(r'\[FEN\s"(?P<turn>[BW]):W(?P<whites_str>[0-9K,]+):B(?P<blacks_str>[0-9K,]+)"]')


def parse_piece(piece: str) -> tuple[bool, Tile]:
    m = PIECE_REGEXP.match(piece)
    return bool(m.group('is_king')), Tile.from_string((m.group('vertical') or '') + m.group('number'))


def parse_pieces(pieces_str: str, board: Board, is_black: bool):
    ret_dict = {}
    for piece in pieces_str.split(','):
        piece = piece.strip().upper()
        is_king, tile = parse_piece(piece)
        ret_dict[board[str(tile)]] = Piece(board[str(tile)], is_black, is_king)
    return ret_dict


def parse_position(position_str):
    m = POSITION_REGEXP.match(position_str)
    return m.group('whites_str'), m.group('blacks_str'), m.group('turn')
