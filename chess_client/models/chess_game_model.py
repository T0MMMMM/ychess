from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant
from ..chess_engine.game import ChessGame

class ChessGameModel(QObject):
    """Chess game model for QML"""
    
    # Signals for QML binding
    boardChanged = pyqtSignal()
    currentPlayerChanged = pyqtSignal()
    gameStatusChanged = pyqtSignal()
    movesChanged = pyqtSignal()
    capturedPiecesChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._game = ChessGame()
        self._game.start_new_game()
        
    @pyqtProperty(list, notify=boardChanged)
    def board(self):
        """Get the current board state as a 2D array"""
        return self._game.get_board_state()
    
    @pyqtProperty(str, notify=currentPlayerChanged)
    def currentPlayer(self):
        """Get the current player (white/black)"""
        return self._game.current_player
    
    @pyqtProperty(str, notify=gameStatusChanged)
    def gameStatus(self):
        """Get the current game status"""
        return self._game.status
    
    @pyqtProperty(list, notify=movesChanged)
    def moves(self):
        """Get the list of moves in algebraic notation"""
        return self._game.moves
    
    @pyqtProperty(dict, notify=capturedPiecesChanged)
    def capturedPieces(self):
        """Get the captured pieces for both players"""
        return self._game.get_captured_pieces()
    
    @pyqtSlot(str, result='QVariantList')
    def getCapturedPieces(self, color):
        """
        Get captured pieces for a specific player
        
        Args:
            color: 'white' or 'black'
            
        Returns:
            List of captured piece symbols
        """
        captured = self._game.get_captured_pieces().get(color, [])
        return captured
    
    @pyqtSlot(int, int, result=bool)
    def selectPiece(self, row, col):
        """
        Select a piece at the given position
        
        Args:
            row: Board row (0-7)
            col: Board column (0-7)
            
        Returns:
            True if piece was selected, False otherwise
        """
        result = self._game.select_piece((row, col))
        return result
    
    @pyqtSlot(int, int, result=bool)
    def movePiece(self, row, col):
        """
        Move the selected piece to the given position
        
        Args:
            row: Board row (0-7)
            col: Board column (0-7)
            
        Returns:
            True if move was successful, False otherwise
        """
        success = self._game.move_selected_piece((row, col))
        
        if success:
            # Emit all signals in case any of these changed
            self.boardChanged.emit()
            self.currentPlayerChanged.emit()
            self.gameStatusChanged.emit()
            self.movesChanged.emit()
            self.capturedPiecesChanged.emit()  # Add this signal
        
        return success
    
    @pyqtSlot(int, int, result='QVariantList')
    def getPossibleMoves(self, row, col):
        """
        Get all valid moves for a piece at the given position
        
        Args:
            row: Board row (0-7)
            col: Board column (0-7)
            
        Returns:
            List of valid move positions as [row, col] lists
        """
        moves = self._game.get_possible_moves((row, col))
        # Convert to list of lists for QML
        return [[move[0], move[1]] for move in moves]
    
    @pyqtSlot()
    def resetGame(self):
        """Start a new game"""
        self._game.start_new_game()
        self.boardChanged.emit()
        self.currentPlayerChanged.emit()
        self.gameStatusChanged.emit()
        self.movesChanged.emit()
        self.capturedPiecesChanged.emit()  # Add this signal
