from .piece import Piece

class King(Piece):
    """King piece implementation"""
    
    @property
    def symbol(self):
        return "♚" if self.color == "black" else "♔"
    
    @property
    def notation_symbol(self):
        return "K"
    
    @property
    def value(self):
        return 0  # Kings have infinite value
    
    def is_valid_move(self, board, to_position):
        if not super().is_valid_move(board, to_position):
            return False
        
        from_row, from_col = self.position
        to_row, to_col = to_position
        
        # King can move one square in any direction
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        # Regular king move (one square in any direction)
        return row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0)
    
    def get_possible_moves(self, board):
        """Get all possible moves for the king (one square in any direction)"""
        moves = []
        row, col = self.position
        
        # Check all 8 surrounding squares
        for r in range(max(0, row-1), min(8, row+2)):
            for c in range(max(0, col-1), min(8, col+2)):
                # Skip the square where the king is already at
                if (r, c) != (row, col) and self.is_valid_move(board, (r, c)):
                    moves.append((r, c))
        
        return moves
