from .piece import Piece

class Rook(Piece):
    """Rook piece implementation"""
    
    @property
    def symbol(self):
        return "♜" if self.color == "black" else "♖"
    
    @property
    def notation_symbol(self):
        return "R"
    
    @property
    def value(self):
        return 5
    
    def is_valid_move(self, board, to_position):
        if not super().is_valid_move(board, to_position):
            return False
        
        from_row, from_col = self.position
        to_row, to_col = to_position
        
        # Rook can only move horizontally or vertically
        if from_row != to_row and from_col != to_col:
            return False
        
        # Check if path is clear
        return self._is_path_clear(board, from_row, from_col, to_row, to_col)
    
    def _is_path_clear(self, board, from_row, from_col, to_row, to_col):
        # Moving vertically
        if from_col == to_col:
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if board.get_piece((row, from_col)) is not None:
                    return False
        
        # Moving horizontally
        else:
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if board.get_piece((from_row, col)) is not None:
                    return False
        
        return True
    
    def get_possible_moves(self, board):
        """Get all possible horizontal and vertical moves for the rook"""
        moves = []
        row, col = self.position
        
        # Horizontal moves (left and right)
        for c in range(col-1, -1, -1):  # Left
            pos = (row, c)
            piece_at_pos = board.get_piece(pos)
            if piece_at_pos is None:
                moves.append(pos)
            elif piece_at_pos.color != self.color:
                moves.append(pos)
                break
            else:
                break
        
        for c in range(col+1, 8):  # Right
            pos = (row, c)
            piece_at_pos = board.get_piece(pos)
            if piece_at_pos is None:
                moves.append(pos)
            elif piece_at_pos.color != self.color:
                moves.append(pos)
                break
            else:
                break
        
        # Vertical moves (up and down)
        for r in range(row-1, -1, -1):  # Up
            pos = (r, col)
            piece_at_pos = board.get_piece(pos)
            if piece_at_pos is None:
                moves.append(pos)
            elif piece_at_pos.color != self.color:
                moves.append(pos)
                break
            else:
                break
        
        for r in range(row+1, 8):  # Down
            pos = (r, col)
            piece_at_pos = board.get_piece(pos)
            if piece_at_pos is None:
                moves.append(pos)
            elif piece_at_pos.color != self.color:
                moves.append(pos)
                break
            else:
                break
        
        return moves
