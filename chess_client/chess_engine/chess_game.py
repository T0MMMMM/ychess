from .board import ChessBoard
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty

class ChessGame:
    """Chess game manager that handles all chess logic"""
    
    def __init__(self):
        self.board = ChessBoard()
        self.current_player = "white"
        self.status = "waiting"  # waiting, active, check, checkmate, stalemate
        self.selected_piece_position = None
        self.white_time = 600  # 10 minutes in seconds
        self.black_time = 600
        self.moves = []  # List of moves in algebraic notation
        self.captured_pieces = {"white": [], "black": []}  # Track captured pieces
        self.in_check = False  # Flag to track if the current player is in check
    
    def start_new_game(self):
        """Start a new game"""
        self.board.setup_default_position()
        self.current_player = "white"
        self.status = "active"
        self.moves = []
        self.selected_piece_position = None
        self.white_time = 600
        self.black_time = 600
        self.captured_pieces = {"white": [], "black": []}  # Reset captured pieces
        self.in_check = False
    
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
        
        # Check if this move would leave our king in check
        if not self._is_move_legal(self.selected_piece_position, to_position):
            print("Move would leave or put king in check - not allowed")
            return False
        
        # Check for capture before moving
        captured_piece = self.board.get_piece(to_position)
        
        # Try to move the piece
        success = self.board.move_piece(self.selected_piece_position, to_position)
        
        if success:
            # Handle captured piece
            if captured_piece:
                # The current player's color is the one making the capture
                self.captured_pieces[self.current_player].append(captured_piece.notation_symbol or "P")
            
            # Record the move in algebraic notation
            piece = self.board.get_piece(to_position)
            from_pos = self._position_to_algebraic(self.selected_piece_position)
            to_pos = self._position_to_algebraic(to_position)
            
            # Format depends on piece type
            if piece.notation_symbol:
                notation = f"{piece.notation_symbol}{from_pos}{to_pos}"
            else:
                notation = f"{to_pos}"  # Pawns just use the destination square
                
            self.moves.append(notation)
            
            # Check if opponent is now in check/checkmate
            self._update_game_status()
            
            # Switch player
            self.current_player = "black" if self.current_player == "white" else "white"
            
            # Check if the new current player is in check
            self.in_check = self._is_king_in_check(self.current_player)
            
            # Reset selection
            self.selected_piece_position = None
        
        return success
    
    def _is_move_legal(self, from_position, to_position):
        """
        Check if a move is legal - it doesn't put or leave own king in check
        
        Args:
            from_position: tuple of (row, col)
            to_position: tuple of (row, col)
            
        Returns:
            True if the move is legal, False otherwise
        """
        # Make a copy of the board to simulate the move
        original_piece = self.board.get_piece(from_position)
        captured_piece = self.board.get_piece(to_position)
        
        # Temporarily make the move
        self.board.set_piece(to_position, original_piece)
        self.board.set_piece(from_position, None)
        
        # Check if our king is in check after this move
        is_legal = not self._is_king_in_check(self.current_player)
        
        # Restore the board
        self.board.set_piece(from_position, original_piece)
        self.board.set_piece(to_position, captured_piece)
        
        return is_legal
    
    def get_possible_moves(self, position):
        """
        Get all valid moves for a piece at the given position,
        taking into account if the king is in check
        
        Args:
            position: tuple of (row, col)
            
        Returns:
            List of valid move positions as (row, col) tuples
        """
        piece = self.board.get_piece(position)
        if not piece or piece.color != self.current_player:
            return []
            
        raw_moves = self.board.get_possible_moves(position)
        legal_moves = []
        
        # Filter moves that would leave our king in check
        for move in raw_moves:
            if self._is_move_legal(position, move):
                legal_moves.append(move)
        
        return legal_moves
    
    def _update_game_status(self):
        """Update the game status after a move"""
        opponent_color = "black" if self.current_player == "white" else "white"
        
        # First, check if the opponent's king is in check
        is_in_check = self._is_king_in_check(opponent_color)
        
        if is_in_check:
            print(f"{opponent_color}'s king is in check!")
            
            # Check if the opponent has any legal moves to get out of check
            has_legal_moves = False
            for piece, position in self.board.get_all_pieces():
                if piece.color == opponent_color:
                    # For each piece, check if any of its moves would get out of check
                    for move in self.board.get_possible_moves(position):
                        # Temporarily set current_player to opponent to check if their move would be legal
                        original_player = self.current_player
                        self.current_player = opponent_color
                        
                        if self._is_move_legal(position, move):
                            has_legal_moves = True
                            self.current_player = original_player
                            break
                            
                        self.current_player = original_player
                    
                    if has_legal_moves:
                        break
            
            if not has_legal_moves:
                print(f"CHECKMATE! {opponent_color} has no legal moves.")
                self.status = "checkmate"
            else:
                self.status = "check"
        else:
            # If not in check, check for stalemate
            has_legal_moves = False
            for piece, position in self.board.get_all_pieces():
                if piece.color == opponent_color:
                    for move in self.board.get_possible_moves(position):
                        original_player = self.current_player
                        self.current_player = opponent_color
                        
                        if self._is_move_legal(position, move):
                            has_legal_moves = True
                            self.current_player = original_player
                            break
                            
                        self.current_player = original_player
                    
                    if has_legal_moves:
                        break
            
            if not has_legal_moves:
                print("STALEMATE! Player not in check but has no legal moves.")
                self.status = "stalemate"
            else:
                self.status = "active"
    
    def _is_king_in_check(self, color):
        """Check if the king of the given color is in check"""
        # Find the king position
        king_position = None
        for piece, position in self.board.get_all_pieces():
            if piece.__class__.__name__ == "King" and piece.color == color:
                king_position = position
                break
        
        if not king_position:
            return False
            
        # Check if any opponent piece can attack the king
        opponent_color = "black" if color == "white" else "white"
        for piece, position in self.board.get_all_pieces():
            if piece.color == opponent_color:
                # Use the raw board method to get moves, ignoring check status
                possible_moves = self.board.get_possible_moves(position)
                if king_position in possible_moves:
                    print(f"{color}'s king is under attack from {piece.__class__.__name__} at {position}")
                    return True
                    
        return False
    
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
