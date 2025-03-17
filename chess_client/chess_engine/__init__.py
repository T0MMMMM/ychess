# Chess engine package

# Import the main components so they can be imported directly from chess_engine
from .pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, create_piece_from_symbol
from .board import ChessBoard
from .game import ChessGame

# Export the most important classes
__all__ = [
    'Piece', 'Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King',
    'create_piece_from_symbol', 'ChessBoard', 'ChessGame'
]
