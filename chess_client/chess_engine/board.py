# Import directly from the pieces package
from .pieces import create_piece_from_symbol

class ChessBoard:
    """Chess board representation"""
    
    def __init__(self):
        """Initialize an empty chess board"""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
    
    def setup_default_position(self):
        """Set up the default starting position"""
        self.setup_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    
    def setup_from_fen(self, fen):
        """
        Set up the board from a FEN string
        
        Args:
            fen: FEN string (just the position part)
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Parse the board position
        rows = fen.split('/')
        for i, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if (char.isdigit()):
                    col_idx += int(char)
                else:
                    position = (i, col_idx)
                    self.board[i][col_idx] = create_piece_from_symbol(char, position)
                    col_idx += 1
    
    def get_piece(self, position):
        """
        Get the piece at the given position
        
        Args:
            position: tuple of (row, col)
            
        Returns:
            Piece object or None if empty
        """
        row, col = position
        if self.is_valid_position(position):
            return self.board[row][col]
        return None
    
    def set_piece(self, position, piece):
        """
        Place a piece at the given position
        
        Args:
            position: tuple of (row, col)
            piece: Piece object or None
        """
        row, col = position
        if self.is_valid_position(position):
            self.board[row][col] = piece
            if piece is not None:
                piece.position = position
    
    def move_piece(self, from_position, to_position):
        """
        Move a piece from one position to another
        
        Args:
            from_position: tuple of (row, col)
            to_position: tuple of (row, col)
            
        Returns:
            True if move was successful, False otherwise
        """
        piece = self.get_piece(from_position)
        if piece is None:
            return False
        
        if not piece.is_valid_move(self, to_position):
            return False
        
        # Record move before making it
        captured_piece = self.get_piece(to_position)
        move = {
            'piece': piece,
            'from': from_position,
            'to': to_position,
            'captured': captured_piece
        }
        
        # Make the move
        self.set_piece(to_position, piece)
        self.set_piece(from_position, None)
        piece.has_moved = True
        
        # Add to history
        self.move_history.append(move)
        
        return True
    
    def undo_last_move(self):
        """Undo the last move"""
        if not self.move_history:
            return False
        
        move = self.move_history.pop()
        piece = move['piece']
        
        # Restore the board state
        self.set_piece(move['from'], piece)
        self.set_piece(move['to'], move['captured'])
        
        # Reset has_moved flag if this was the piece's only move
        # This is a simplistic approach - in a real chess engine, you'd need to track this properly
        if not any(m['piece'] == piece for m in self.move_history):
            piece.has_moved = False
        
        return True
    
    def is_valid_position(self, position):
        """Check if a position is on the board"""
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_possible_moves(self, position):
        """Get all possible moves for a piece at the given position"""
        piece = self.get_piece(position)
        if piece is None:
            return []
        
        return piece.get_possible_moves(self)
        
    def get_all_pieces(self):
        """Get all pieces on the board with their positions"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    pieces.append((piece, (row, col)))
        return pieces
    
    def to_array_representation(self):
        """
        Convert board to 2D array of piece symbols
        
        Returns:
            2D array of strings (empty string for empty squares)
        """
        result = []
        for row in range(8):
            row_data = []
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    row_data.append("")
                else:
                    symbol = piece.notation_symbol
                    if piece.__class__.__name__ == "Pawn":
                        symbol = "P"  # Use P for pawns in this representation
                    
                    # Lowercase for black pieces
                    if piece.color == "black":
                        symbol = symbol.lower()
                        
                    row_data.append(symbol)
            result.append(row_data)
        return result
