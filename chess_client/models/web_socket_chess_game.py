from ..chess_engine.board import ChessBoard
from ..chess_engine.chess_game import ChessGame
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QTimer

class WebSocketChessGame(QObject):
    """
    Chess game implementation that communicates moves via WebSockets.
    Local board state is updated when the player makes a move or
    when an opponent's move is received from the server.
    """
    boardChanged = pyqtSignal()
    gameOver = pyqtSignal(str, str, arguments=['winner', 'reason'])
    
    def __init__(self, socket_client=None):
        super().__init__()
        self._chess_game = ChessGame()
        self._chess_game.start_new_game()
        self._socket_client = socket_client
        self._player_color = "white"  # Default value
        self._game_id = None
        self._opponent_id = None
        self._is_my_turn = True
        self._match_id_value = None  # Changed attribute name to avoid conflict
        self._game_result = None  # Store the game result
        print("Game initialized")

        # Delay signal emission until after initialization
        QTimer.singleShot(0, self.boardChanged.emit)
    
    @pyqtProperty(str, notify=boardChanged)
    def player_color(self):
        return self._player_color

    @pyqtProperty(bool, notify=boardChanged)
    def is_my_turn(self):
        return self._is_my_turn
    
    # Fix: Ensure match_id always returns a string
    @pyqtProperty(str)
    def match_id(self):
        # Convert to string to avoid type conversion errors
        return str(self._match_id_value) if self._match_id_value is not None else None
    
    def set_game_details(self, game_id, player_color, opponent_id):
        """Set game ID and player color when a match is found"""
        print(f"Setting game details - color: {player_color}, id: {game_id}")
        self._game_id = game_id
        self._player_color = player_color
        self._opponent_id = opponent_id
        self._is_my_turn = (player_color == "white")
        self._match_id_value = game_id
        
        # Reset chess game for a new match
        self._chess_game = ChessGame()
        self._chess_game.start_new_game()
        
        print(f"Game details set - color: {self._player_color}, is_my_turn: {self._is_my_turn}")
        # Signal once that everything is initialized
        QTimer.singleShot(0, self.boardChanged.emit)
    
    @pyqtSlot(str, str)
    def make_move(self, from_square, to_square):
        """Make a move and send it to the server"""
        if not self._is_my_turn:
            return False
            
        try:
            # Let chess_game handle all the logic
            from_pos = self._algebraic_to_position(from_square)
            to_pos = self._algebraic_to_position(to_square)
            
            # Execute the move on the chess game
            if self._chess_game.select_piece(from_pos) and self._chess_game.move_selected_piece(to_pos):
                # If the move is valid, update our state and notify the server
                self._is_my_turn = False
                
                # Send move to server if socket client is available
                if self._socket_client:
                    self._socket_client.emit('move', {
                        'match_id': str(self._match_id_value),  # Convert to string
                        'move': {
                            'from': from_square,
                            'to': to_square
                        },
                        'opponent_id': self._opponent_id
                    })
                
                # Notify UI that the board has changed
                self.boardChanged.emit()
                
                # Check if the game has ended
                self._check_game_state()
                return True
            
            return False
        except Exception as e:
            print(f"Error making move: {e}")
            return False
    
    @pyqtSlot(str, str, str)
    def receive_opponent_move(self, from_square, to_square, promotion=None):
        """Process a move received from the opponent via server"""
        try:
            print(f"Processing opponent move from {from_square} to {to_square}")
            
            # Convert algebraic notation to board positions
            from_pos = self._algebraic_to_position(from_square)
            to_pos = self._algebraic_to_position(to_square)
            
            # In our engine, we need to select the piece first
            if self._chess_game.select_piece(from_pos):
                # Then move it
                if self._chess_game.move_selected_piece(to_pos):
                    self._is_my_turn = True  # Now it's our turn
                    print(f"Opponent move processed, is_my_turn: {self._is_my_turn}")
                    self.boardChanged.emit()
                    # Check if opponent's move resulted in checkmate
                    self._check_game_state()
                    return True
            
            print("Invalid move received")
            return False
        except Exception as e:
            print(f"Error processing opponent's move: {e}")
            return False

    def _check_game_state(self):
        """Check if the game has ended"""
        # Check for checkmate, stalemate, or other game-ending conditions
        if self._chess_game.status == "checkmate":
            # The winner is the player who just moved (not the current player in chess_game)
            winner_color = "black" if self._chess_game.current_player == "white" else "white"
            self._game_result = "victory" if winner_color == self._player_color else "defeat"
            self.gameOver.emit(winner_color, "checkmate")
            print(f"Game over: {self._game_result} by checkmate!")
        
        # Check for draws
        elif self._chess_game.status == "stalemate":
            self._game_result = "draw"
            self.gameOver.emit("draw", "stalemate")
            print("Game over: draw by stalemate!")

    def _algebraic_to_position(self, algebraic):
        """Convert algebraic notation (e.g. 'e4') to (row, col) position"""
        return self._chess_game._algebraic_to_position(algebraic)
    
    def _position_to_algebraic(self, position):
        """Convert (row, col) position to algebraic notation (e.g. 'e4')"""
        return self._chess_game._position_to_algebraic(position)
    
    @pyqtProperty(list, notify=boardChanged)
    def piece_positions(self):
        """
        Get all piece positions for UI representation
        Returns a list of objects with 'piece' and 'square' properties
        """
        try:
            result = []
            board_pieces = self._chess_game.board.get_all_pieces()
            
            for piece, position in board_pieces:
                # Use first character of color (w/b) plus piece name in lowercase
                piece_name = f"{piece.color[0]}_{piece.__class__.__name__.lower()}"
                square = self._position_to_algebraic(position)
                result.append({"piece": piece_name, "square": square})
            
            return result
        except Exception as e:
            print(f"Error getting piece positions: {e}")
            return []

    @pyqtSlot(str, result="QVariantList")
    def get_legal_destinations(self, from_square):
        """Get list of legal destination squares for a piece"""
        try:
            print(f"Getting legal moves from {from_square}")
            from_pos = self._algebraic_to_position(from_square)
            
            # Get possible moves as positions - this now includes check validation
            possible_moves = self._chess_game.get_possible_moves(from_pos)
            
            # Convert to algebraic notation
            destinations = [self._position_to_algebraic(pos) for pos in possible_moves]
            
            print(f"Legal moves: {destinations}")
            return destinations
        except Exception as e:
            print(f"Error getting legal moves: {e}")
            return []

    @pyqtSlot(str, result=bool)
    def is_valid_move_source(self, square):
        """Check if the square contains a piece that can be moved by the current player"""
        try:
            position = self._algebraic_to_position(square)
            piece = self._chess_game.board.get_piece(position)
            
            # It's a valid move source if there's a piece and it's the current player's piece
            return piece is not None and piece.color == self._chess_game.current_player
        except Exception as e:
            print(f"Error checking valid move source: {e}")
            return False

    def reset_game(self):
        """Reset the game to initial state"""
        self._chess_game.start_new_game()
        self._is_my_turn = self._player_color == "white"
        self._game_result = None
        self.boardChanged.emit()

    @pyqtProperty(str, notify=boardChanged)
    def game_result(self):
        """Get the game result from the player's perspective: victory, defeat, or draw"""
        return self._game_result
