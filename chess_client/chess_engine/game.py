from .board import ChessBoard
import chess
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty

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

# class WebSocketChessGame(QObject):
#     """
#     Chess game implementation that communicates moves via WebSockets.
#     Local board state is updated when the player makes a move or
#     when an opponent's move is received from the server.
#     """
#     boardChanged = pyqtSignal()
#     gameOver = pyqtSignal(str, str)  # result, reason
    
#     def __init__(self, socket_client=None):
#         super().__init__()
#         self._board = chess.Board()
#         self._socket_client = socket_client
#         self._player_color = None
#         self._game_id = None
#         self._is_my_turn = False
#         self.boardChanged.emit()
#         print("______________________________________" + self.piece_positions)
    
#     @pyqtProperty(str, notify=boardChanged)
#     def player_color(self):
#         return self._player_color or "white"
    
#     @pyqtProperty(list, notify=boardChanged)
#     def piece_positions(self):
#         """Get list of all pieces on the board with their positions"""
#         result = []
#         for square in chess.SQUARES:
#             piece = self._board.piece_at(square)
#             if piece:
#                 color = "w" if piece.color == chess.WHITE else "b"
#                 piece_type = {
#                     chess.PAWN: "pawn",
#                     chess.KNIGHT: "knight",
#                     chess.BISHOP: "bishop",
#                     chess.ROOK: "rook",
#                     chess.QUEEN: "queen",
#                     chess.KING: "king"
#                 }[piece.piece_type]
                
#                 square_name = chess.square_name(square)
#                 result.append({
#                     "piece": f"{color}_{piece_type}",
#                     "square": square_name
#                 })
#         return result
        
#     @pyqtSlot(str)
#     def is_valid_move_source(self, square_name):
#         """Check if the square contains a piece that can be moved"""
#         try:
#             square = chess.parse_square(square_name)
#             piece = self._board.piece_at(square)
            
#             if not piece:
#                 return False
                
#             # Check if it's a piece of the player's color
#             piece_color = chess.WHITE if piece.color else chess.BLACK
#             player_color = chess.WHITE if self._player_color == "white" else chess.BLACK
            
#             return piece_color == player_color and self._is_my_turn
#         except:
#             return False
            
#     @pyqtSlot(str, result=list)
#     def get_legal_destinations(self, from_square):
#         """Get list of legal destination squares for a piece"""
#         try:
#             from_sq = chess.parse_square(from_square)
#             legal_destinations = []
            
#             for move in self._board.legal_moves:
#                 if move.from_square == from_sq:
#                     legal_destinations.append(chess.square_name(move.to_square))
                    
#             return legal_destinations
#         except:
#             return []
            
#     @pyqtProperty(str, notify=boardChanged)
#     def game_status(self):
#         """Get current game status as a human-readable string"""
#         if self._board.is_checkmate():
#             return "Checkmate"
#         elif self._board.is_stalemate():
#             return "Stalemate"
#         elif self._board.is_check():
#             return "Check"
#         elif self._board.is_insufficient_material():
#             return "Draw (insufficient material)"
#         elif self._board.is_fifty_moves():
#             return "Draw (fifty-move rule)"
#         elif self._board.is_repetition():
#             return "Draw (threefold repetition)"
#         else:
#             return "In progress"
