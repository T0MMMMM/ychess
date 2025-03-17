from .piece import Piece

class Pawn(Piece):
    """Pawn piece implementation"""
    
    @property
    def symbol(self):
        return "♟" if self.color == "black" else "♙"
    
    @property
    def notation_symbol(self):
        return ""  # Pawn has no symbol in algebraic notation
    
    @property
    def value(self):
        return 1
    
    def is_valid_move(self, board, to_position):
        if not super().is_valid_move(board, to_position):
            return False
        
        from_row, from_col = self.position
        to_row, to_col = to_position
        
        # Direction depends on color (white pawns move up, black pawns move down)
        direction = -1 if self.color == "white" else 1
        
        # Basic forward movement
        if from_col == to_col and to_row == from_row + direction:
            return board.get_piece(to_position) is None
        
        # Double move from starting position
        if from_col == to_col and to_row == from_row + 2 * direction:
            if (self.color == "white" and from_row == 6) or (self.color == "black" and from_row == 1):
                intermediate = (from_row + direction, from_col)
                return (board.get_piece(intermediate) is None and 
                        board.get_piece(to_position) is None)
            
        # Capture diagonally
        if (to_col == from_col - 1 or to_col == from_col + 1) and to_row == from_row + direction:
            captured_piece = board.get_piece(to_position)
            return captured_piece is not None and captured_piece.color != self.color
        
        return False

    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == "white" else 1
        
        # Forward move
        forward = (row + direction, col)
        if board.is_valid_position(forward) and board.get_piece(forward) is None:
            moves.append(forward)
            
            # Double move from starting position
            if ((self.color == "white" and row == 6) or 
                (self.color == "black" and row == 1)):
                double_forward = (row + 2 * direction, col)
                if board.get_piece(double_forward) is None:
                    moves.append(double_forward)
        
        # Captures
        for capture_col in [col - 1, col + 1]:
            capture_pos = (row + direction, capture_col)
            if board.is_valid_position(capture_pos):
                piece = board.get_piece(capture_pos)
                if piece is not None and piece.color != self.color:
                    moves.append(capture_pos)
        
        return moves
