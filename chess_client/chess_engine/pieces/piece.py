class Piece:
    """Base class for chess pieces"""
    
    def __init__(self, color, position=None):
        """
        Initialize a chess piece
        
        Args:
            color: 'white' or 'black'
            position: tuple of (row, col) or None
        """
        self.color = color
        self.position = position
        self.has_moved = False
    
    @property
    def symbol(self):
        """Unicode symbol for the piece"""
        return ""
    
    @property
    def notation_symbol(self):
        """Algebraic notation symbol (K, Q, R, B, N, or empty for pawn)"""
        return ""
    
    @property
    def value(self):
        """Numeric value of the piece"""
        return 0
    
    def is_valid_move(self, board, to_position):
        """Check if a move is valid for this piece"""
        if not board.is_valid_position(to_position):
            return False
        
        # Can't move to a square occupied by a piece of the same color
        if board.get_piece(to_position) is not None and board.get_piece(to_position).color == self.color:
            return False
        
        return True
    
    def get_possible_moves(self, board):
        """Get all possible moves for this piece"""
        return []
    
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at {self.position}"
