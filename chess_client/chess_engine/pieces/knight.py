from .piece import Piece

class Knight(Piece):
    """Knight piece implementation"""
    
    @property
    def symbol(self):
        return "♞" if self.color == "black" else "♘"
    
    @property
    def notation_symbol(self):
        return "N"
    
    @property
    def value(self):
        return 3
    
    def is_valid_move(self, board, to_position):
        if not super().is_valid_move(board, to_position):
            return False
        
        from_row, from_col = self.position
        to_row, to_col = to_position
        
        # Knight moves in L-shape: 2 squares in one direction and 1 in the other
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # All possible knight moves
        knight_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]
        
        for move in knight_moves:
            if self.is_valid_move(board, move):
                moves.append(move)
        
        return moves
