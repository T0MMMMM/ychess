from .board import ChessBoard

class ChessGame:
    """Chess game manager"""
    
    def __init__(self):
        self.board = ChessBoard()
        self.current_player = "white"
        self.status = "waiting"  # waiting, active, check, checkmate, stalemate
        self.selected_piece_position = None
        self.white_time = 600  # 10 minutes in seconds
        self.black_time = 600
        self.moves = []  # List of moves in algebraic notation
        self.captured_pieces = {"white": [], "black": []}  # Track captured pieces
        
    def start_new_game(self):
        """Start a new game"""
        self.board.setup_default_position()
        self.current_player = "white"
        self.status = "active"
        self.moves = []
        self.white_time = 600
        self.black_time = 600
        self.captured_pieces = {"white": [], "black": []}  # Reset captured pieces
    
    def select_piece(self, position):
        """
        Select a piece at the given position
        
        Args:
            position: tuple of (row, col)
            
        Returns:
            True if piece was selected, False otherwise
        """
        piece = self.board.get_piece(position)
        
        # Can only select your own pieces
        if piece and piece.color == self.current_player:
            self.selected_piece_position = position
            return True
        
        return False
    
    def move_selected_piece(self, to_position):
        """
        Move the selected piece to the given position
        
        Args:
            to_position: tuple of (row, col)
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.selected_piece_position:
            return False
        
        # Check for capture before moving
        captured_piece = self.board.get_piece(to_position)
        
        # Try to move the piece
        success = self.board.move_piece(self.selected_piece_position, to_position)
        
        if success:
            # Handle captured piece
            if captured_piece:
                # The opponent's color is the current player's color (we capture opponent's pieces)
                self.captured_pieces[self.current_player].append(captured_piece.notation_symbol or "P")
            
            # Record the move in algebraic notation
            piece = self.board.get_piece(to_position)
            from_pos = self._position_to_algebraic(self.selected_piece_position)
            to_pos = self._position_to_algebraic(to_position)
            
            # Format depends on piece type
            notation = f"{piece.notation_symbol}{from_pos}{to_pos}"
            if piece.__class__.__name__ == "Pawn":
                notation = f"{to_pos}"  # Pawns just use the destination square
                
            self.moves.append(notation)
            
            # Switch player
            self.current_player = "black" if self.current_player == "white" else "white"
            
            # Reset selection
            self.selected_piece_position = None
        
        return success
    
    def get_possible_moves(self, position):
        """
        Get all valid moves for a piece at the given position
        
        Args:
            position: tuple of (row, col)
            
        Returns:
            List of valid move positions as (row, col) tuples
        """
        return self.board.get_possible_moves(position)
    
    def get_board_state(self):
        """
        Get the current board state
        
        Returns:
            2D array representation of the board
        """
        return self.board.to_array_representation()
    
    def _position_to_algebraic(self, position):
        """Convert (row, col) position to algebraic notation (e.g. 'e4')"""
        row, col = position
        return f"{chr(97 + col)}{8 - row}"
    
    def _algebraic_to_position(self, algebraic):
        """Convert algebraic notation (e.g. 'e4') to (row, col) position"""
        col = ord(algebraic[0]) - 97
        row = 8 - int(algebraic[1])
        return (row, col)
    
    def get_captured_pieces(self):
        """
        Get captured pieces for both players
        
        Returns:
            Dictionary with 'white' and 'black' keys, each containing a list of captured piece symbols
        """
        return self.captured_pieces
