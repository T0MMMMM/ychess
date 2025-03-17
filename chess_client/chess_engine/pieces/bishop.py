from .piece import Piece

class Bishop(Piece):
    """Bishop piece implementation"""
    
    @property
    def symbol(self):
        return "♝" if self.color == "black" else "♗"
    
    @property
    def notation_symbol(self):
        return "B"
    
    @property
    def value(self):
        return 3
    
    def is_valid_move(self, board, to_position):
        if not super().is_valid_move(board, to_position):
            return False
        
        from_row, from_col = self.position
        to_row, to_col = to_position
        
        # Bishop can only move diagonally
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        if row_diff != col_diff:
            return False
        
        # Check if path is clear
        return self._is_path_clear(board, from_row, from_col, to_row, to_col)
    
    def _is_path_clear(self, board, from_row, from_col, to_row, to_col):
        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1
        
        row, col = from_row + row_step, from_col + col_step
        # Fixed loop condition for diagonal movement
        while row != to_row:
            if board.get_piece((row, col)) is not None:
                return False
            row += row_step
            col += col_step
        
        return True
    
    def get_possible_moves(self, board):
        """Get all possible diagonal moves for the bishop"""
        moves = []
        row, col = self.position
        
        # Check all four diagonal directions
        directions = [
            (1, 1),   # down-right
            (1, -1),  # down-left
            (-1, 1),  # up-right
            (-1, -1)  # up-left
        ]
        
        for row_step, col_step in directions:
            r, c = row + row_step, col + col_step
            while 0 <= r < 8 and 0 <= c < 8:
                pos = (r, c)
                piece_at_pos = board.get_piece(pos)
                
                # Empty square - valid move
                if piece_at_pos is None:
                    moves.append(pos)
                # Occupied by opponent - valid move (capture), but can't go further
                elif piece_at_pos.color != self.color:
                    moves.append(pos)
                    break
                # Occupied by own piece - can't move here or beyond
                else:
                    break
                    
                r += row_step
                c += col_step
                
        return moves
