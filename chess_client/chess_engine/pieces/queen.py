from .piece import Piece
from .rook import Rook
from .bishop import Bishop

class Queen(Piece):
    """Queen piece implementation"""
    
    @property
    def symbol(self):
        return "♛" if self.color == "black" else "♕"
    
    @property
    def notation_symbol(self):
        return "Q"
    
    @property
    def value(self):
        return 9
    
    def is_valid_move(self, board, to_position):
        if not super().is_valid_move(board, to_position):
            return False
        
        from_row, from_col = self.position
        to_row, to_col = to_position
        
        # Queen combines rook and bishop movement
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        # Moving like a rook (horizontally or vertically)
        if from_row == to_row or from_col == to_col:
            rook = Rook(self.color, self.position)
            return rook._is_path_clear(board, from_row, from_col, to_row, to_col)
            
        # Moving like a bishop (diagonally)
        elif row_diff == col_diff:
            bishop = Bishop(self.color, self.position)
            return bishop._is_path_clear(board, from_row, from_col, to_row, to_col)
            
        return False
    
    def get_possible_moves(self, board):
        """Get all possible moves for the queen (combination of rook and bishop moves)"""
        # Create temporary rook and bishop at this position to reuse their move logic
        rook = Rook(self.color, self.position)
        bishop = Bishop(self.color, self.position)
        
        # Combine the moves from both pieces
        moves = rook.get_possible_moves(board) + bishop.get_possible_moves(board)
        return moves
