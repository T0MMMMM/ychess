import chess
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QTimer

class WebSocketChessGame(QObject):
    """
    Chess game implementation that communicates moves via WebSockets.
    Local board state is updated when the player makes a move or
    when an opponent's move is received from the server.
    """
    boardChanged = pyqtSignal()
    
    def __init__(self, socket_client=None):
        super().__init__()
        self._board = chess.Board()
        self._socket_client = socket_client
        self._player_color = "white"  # Valeur par défaut
        self._game_id = None
        self._opponent_id = None
        self._is_my_turn = True
        self._match_id = None
        print("Game initialized")
        self.boardChanged.emit()

        # Décaler l'émission du signal après l'initialisation complète
        QTimer.singleShot(0, self.boardChanged.emit)
    
    @pyqtProperty(str, notify=boardChanged)  # Change to property instead of constant
    def player_color(self):
        return self._player_color

    @pyqtProperty(bool, notify=boardChanged)  # Change to property instead of constant
    def is_my_turn(self):
        return self._is_my_turn
    
    def set_game_details(self, game_id, player_color, opponent_id):
        """Set game ID and player color when a match is found"""
        print(f"Setting game details - color: {player_color}, id: {game_id}")
        self._game_id = game_id
        self._player_color = player_color
        self._opponent_id = opponent_id
        self._is_my_turn = (player_color == "white")
        self._match_id = game_id
        self._board = chess.Board()
        print(f"Game details set - color: {self._player_color}, is_my_turn: {self._is_my_turn}")
        # Signal une seule fois que tout est initialisé
        QTimer.singleShot(0, self.boardChanged.emit)
    
    @pyqtSlot(str, str)
    def make_move(self, from_square, to_square):
        if not self._is_my_turn:
            return False
            
        try:
            from_sq = chess.parse_square(from_square)
            to_sq = chess.parse_square(to_square)
            move = chess.Move(from_sq, to_sq)
            
            if self._board.piece_at(from_sq).piece_type == chess.PAWN:
                if (self._player_color == "white" and to_square[1] == '8') or \
                   (self._player_color == "black" and to_square[1] == '1'):
                    move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
            
            if move in self._board.legal_moves:
                self._board.push(move)
                self._is_my_turn = False
                
                if self._socket_client:
                    self._socket_client.emit('move', {
                        'match_id': self._match_id,
                        'move': {
                            'from': from_square,
                            'to': to_square
                        },
                        'opponent_id': self._opponent_id
                    })
                
                self.boardChanged.emit()
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
            from_sq = chess.parse_square(from_square)
            to_sq = chess.parse_square(to_square)
            
            # Create and make move
            move = chess.Move(from_sq, to_sq)
            if move in self._board.legal_moves:
                self._board.push(move)
                self._is_my_turn = True  # C'est maintenant notre tour
                print(f"Opponent move processed, is_my_turn: {self._is_my_turn}")
                self.boardChanged.emit()
                return True
            else:
                print("Invalid move received")
                return False
        except Exception as e:
            print(f"Error processing opponent's move: {e}")
            return False

    @pyqtSlot(str, result=bool)
    def is_valid_move_source(self, square_name):
        """Check if the square contains a piece that can be moved"""
        try:
            if not self._is_my_turn:
                print("Not player's turn")
                return False

            print(f"Checking square {square_name}")
            square = chess.parse_square(square_name)
            piece = self._board.piece_at(square)
            
            if not piece:
                print("No piece at square")
                return False
                
            is_white_piece = piece.color == chess.WHITE
            is_white_turn = self._player_color == "white"
            
            # La pièce peut être bougée si elle est de la même couleur que le joueur
            result = is_white_piece == is_white_turn
            print(f"Can move piece: {result}")
            return result
            
        except Exception as e:
            print(f"Error checking move source: {e}")
            return False

    def _check_game_state(self):
        """Check if the game has ended"""
        if self._board.is_checkmate():
            winner = "black" if self._board.turn == chess.WHITE else "white"
            self.gameOver.emit(winner, "checkmate")
        elif self._board.is_stalemate():
            self.gameOver.emit("draw", "stalemate")
        elif self._board.is_insufficient_material():
            self.gameOver.emit("draw", "insufficient material")
        elif self._board.is_fifty_moves():
            self.gameOver.emit("draw", "fifty-move rule")
        elif self._board.is_repetition():
            self.gameOver.emit("draw", "threefold repetition")
    
    @pyqtProperty(str, notify=boardChanged)
    def fen(self):
        """Get current position in FEN notation"""
        return self._board.fen()
    
    @pyqtProperty(list, notify=boardChanged)
    def legal_moves(self):
        """Get list of legal moves in UCI format"""
        return [move.uci() for move in self._board.legal_moves]
    
    @pyqtProperty(bool, notify=boardChanged)
    def is_check(self):
        """Is the current player in check?"""
        return self._board.is_check()
    
    @pyqtProperty(list, notify=boardChanged)
    def piece_positions(self):
        try:
            if not self._board:
                return []
                
            result = []
            for square in chess.SQUARES:
                piece = self._board.piece_at(square)
                if piece:
                    color = "w" if piece.color == chess.WHITE else "b"
                    piece_type = {
                        chess.PAWN: "pawn",
                        chess.KNIGHT: "knight",
                        chess.BISHOP: "bishop",
                        chess.ROOK: "rook",
                        chess.QUEEN: "queen",
                        chess.KING: "king"
                    }[piece.piece_type]
                    
                    square_name = chess.square_name(square)
                    result.append({
                        "piece": f"{color}_{piece_type}",
                        "square": square_name
                    })
            return result
        except Exception as e:
            print(f"Error getting piece positions: {e}")
            return []

    @pyqtSlot(str, result="QVariantList")
    def get_legal_destinations(self, from_square):
        """Get list of legal destination squares for a piece"""
        try:
            print(f"Getting legal moves from {from_square}")
            from_sq = chess.parse_square(from_square)
            moves = [chess.square_name(move.to_square)
                    for move in self._board.legal_moves
                    if move.from_square == from_sq]
            print(f"Legal moves: {moves}")
            return moves
        except Exception as e:
            print(f"Error getting legal moves: {e}")
            return []

    def reset_game(self):
        """Reset the game to initial state"""
        self._board = chess.Board()
        self._is_my_turn = self._player_color == "white"
        self.boardChanged.emit()
