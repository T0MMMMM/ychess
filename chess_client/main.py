import sys
import os
import requests
import chess  # Ajouter cet import
from pathlib import Path
import socketio

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, pyqtProperty

from chess_utils.player import Player
from chess_client.utils import download_chess_pieces
from chess_client.models.chess_game_model import ChessGameModel
from chess_engine.game import WebSocketChessGame

def ensure_chess_pieces_exist():
    """Make sure chess piece images are available"""
    assets_dir = Path(__file__).parent / "assets" / "pieces"
    
    # Check if directory and a few pieces exist
    if not assets_dir.exists() or not (assets_dir / "w_king.png").exists():
        print("Chess piece images not found. Downloading...")
        download_chess_pieces()
    else:
        print("Chess piece images found.")



class ChessBackend(QObject):
    # Add signals
    userChanged = pyqtSignal()
    loginResult = pyqtSignal(bool, arguments=['success'])
    chessGameChanged = pyqtSignal()  # Add this signal for the chessGame property
    matchFound = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._user = Player()
        self.server_url = "http://localhost:5000/api"
        self._chess_game_model = ChessGameModel()
        
        # Créer une seule instance de socketio.Client
        self.sio = socketio.Client(logger=True, engineio_logger=True)
        self._chess_game = WebSocketChessGame(self.sio)
        
        # Configurer les handlers avant la connexion
        @self.sio.on('connect')
        def on_connect():
            print("Connecté au serveur WebSocket")
            if self._user.id != 0:
                self.sio.emit("register", {'user': self._user.to_dict()})

        @self.sio.on('disconnect')
        def on_disconnect():
            print("Déconnecté du serveur WebSocket")

        @self.sio.on('play_confirmation')
        def on_play_confirmation(data):
            print(f"Confirmation du serveur : {data['message']}")

        @self.sio.on("match")
        def on_match(data):
            print("Match found event received:", data)
            game_id = data.get('match_id')
            player_color = data.get('color')
            opponent_id = data.get('opponent_id')
            
            print(f"Setting up game: id={game_id}, color={player_color}, opponent={opponent_id}")
            self._chess_game.set_game_details(game_id, player_color, opponent_id)
            self.chessGameChanged.emit()
            print("Emitting matchFound signal")
            self.matchFound.emit(data)
        
        @self.sio.on("move")
        def on_move(data):
            print(f"Move received: {data}")
            self._chess_game.receive_opponent_move(
                data.get('from'),
                data.get('to')
            )
            self.chessGameChanged.emit()

        # Supprimer le handler de résignation
        # @self.sio.on("opponent_resigned")
        # def on_opponent_resigned(data):
        #     print("Opponent resigned")
        #     self._chess_game.handle_opponent_resignation()

        # Se connecter au serveur
        try:
            self.sio.connect('http://localhost:5000', wait_timeout=10)
            print("Connecté au serveur WebSocket")
        except Exception as e:
            print(f"Erreur de connexion WebSocket : {e}")
            self.sio = None

    
    @pyqtSlot()
    def play(self):
        if self._user.id == 0:
            print("Vous devez être connecté pour jouer")
            return
        try: 
            # Réinitialiser l'état du jeu avant de chercher une nouvelle partie
            self._chess_game._board = chess.Board()
            self._chess_game.boardChanged.emit()

            response = requests.post(f'{self.server_url}/play', json={'user': self._user.to_dict()})
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print("En attente d'un adversaire...")
        except Exception as e:
            print(f"Erreur lors de la recherche de partie: {e}")
            
    @pyqtProperty(WebSocketChessGame, notify=chessGameChanged)
    def chessGame(self):
        """Get the chess game"""
        return self._chess_game
    
    @pyqtSlot(str, str)
    def makeMove(self, from_square, to_square):
        success = self._chess_game.make_move(from_square, to_square)
        if success:
            self.chessGameChanged.emit()
        return success
    
    @pyqtSlot(str, str)
    def login(self, username, password):
        print(f"Tentative de connexion avec username: {username}")
        # En production, ne jamais afficher les mots de passe en clair dans les logs
        print(f"Mot de passe (longueur: {len(password)}): {password[:1]}****")
        print(self.server_url)
        try:
            response = requests.post(f'{self.server_url}/login', 
                                    json={'username': username, 'password': password})
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    player_data = data['player']
                    self._user = Player(
                        id=player_data.get('id', 0),
                        username=player_data.get('username', ''),
                        password_hash='',  # Don't store password hash on client
                        email=player_data.get('email', ''),
                        elo=player_data.get('elo', 0),
                        matches_played=player_data.get('matches_played', 0),
                        wins=player_data.get('wins', 0),
                        losses=player_data.get('losses', 0),
                        registration_date=player_data.get('registration_date'),
                        last_login=player_data.get('last_login')
                    )
                    self.loginResult.emit(True)
                    self.userChanged.emit()
                    # Modification de l'émission du register
                    if self.sio and self.sio.connected:
                        self.sio.emit("register", {'user': self._user.to_dict()})
                    else:
                        print("Socket.IO non connecté")

                    return
        except Exception as e:
            print(f"Login error: {e}")
        
        # If we get here, login failed
        self._user = Player()
        self.loginResult.emit(False)
        self.userChanged.emit()

    @pyqtSlot()
    def cancelMatchmaking(self):
        print("Matchmaking annulé")
        try: 
            response = requests.post(f'{self.server_url}/disconnect', json={'user': self._user.to_dict()})
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print("Joueur enlevé de la liste")
        except Exception as e:
            print(f"Erreur lors de la tentative de connexion: {e}")
            

    
    @pyqtSlot()
    def logout(self):
        print("Déconnexion")
        self._user = Player()
        self.userChanged.emit()
    
    # Use Player as the return type now that we properly register it
    @pyqtProperty(Player, notify=userChanged)
    def user(self):
        return self._user
        
    @pyqtProperty(bool, notify=userChanged)
    def isLoggedIn(self):
        return self._user.username != ""




def qml_loader():
    app = QGuiApplication(sys.argv)
    
    # Register types
    qmlRegisterType(Player, "ChessTypes", 1, 0, "Player")
    qmlRegisterType(ChessGameModel, "ChessTypes", 1, 0, "ChessGameModel")
    qmlRegisterType(WebSocketChessGame, "ChessTypes", 1, 0, "WebSocketChessGame")
    
    engine = QQmlApplicationEngine()
    
    # Set the correct import paths
    qml_path = Path(__file__).parent
    engine.addImportPath(str(qml_path))
    
    # Set the root context property for assets path
    engine.rootContext().setContextProperty(
        "assetsPath", 
        str(qml_path / "assets")
    )
    
    # Create backend and expose to QML
    backend = ChessBackend()
    engine.rootContext().setContextProperty("backend", backend)
    
    # Load main QML file
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    engine.load(QUrl.fromLocalFile(qml_file))
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    return app.exec()

def main():
    ensure_chess_pieces_exist()
    sys.exit(qml_loader())

if __name__ == "__main__":
    main()
