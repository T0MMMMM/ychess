from .piece import Piece
from .pawn import Pawn
from .knight import Knight
from .bishop import Bishop
from .rook import Rook
from .queen import Queen
from .king import King

def create_piece_from_symbol(symbol, position):
    """Create a piece instance from a FEN symbol"""
    color = "white" if symbol.isupper() else "black"
    symbol = symbol.lower()
    
    if symbol == 'p':
        return Pawn(color, position)
    elif symbol == 'r':
        return Rook(color, position)
    elif symbol == 'n':
        return Knight(color, position)
    elif symbol == 'b':
        return Bishop(color, position)
    elif symbol == 'q':
        return Queen(color, position)
    elif symbol == 'k':
        return King(color, position)
    else:
        return None
