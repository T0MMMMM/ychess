import sys
import os
import requests
from pathlib import Path

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, pyqtProperty
from chess_utils.player import Player
from chess_client.utils import download_chess_pieces
from chess_client.models.chess_game_model import ChessGameModel

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

    def __init__(self):
        super().__init__()
        self._user = Player()
        self.server_url = "http://localhost:5000/api"
        self._chess_game_model = ChessGameModel()
    
    @pyqtProperty(ChessGameModel, notify=chessGameChanged)  # Add the notify signal here
    def chessGame(self):
        """Get the chess game model"""
        return self._chess_game_model
    
    @pyqtSlot(str, str)
    def login(self, username, password):
        print(f"Tentative de connexion avec username: {username}")
        # En production, ne jamais afficher les mots de passe en clair dans les logs
        print(f"Mot de passe (longueur: {len(password)}): {password[:1]}****")
        
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
                    return
        except Exception as e:
            print(f"Login error: {e}")
        
        # If we get here, login failed
        self._user = Player()
        self.loginResult.emit(False)
        self.userChanged.emit()
    
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
    # Création de l'application
    app = QGuiApplication(sys.argv)
    
    # Register the Player type with QML before creating the engine
    qmlRegisterType(Player, "ChessTypes", 1, 0, "Player")
    
    # Register our ChessGameModel with QML
    qmlRegisterType(ChessGameModel, "ChessTypes", 1, 0, "ChessGameModel")
    
    # Création du moteur QML
    engine = QQmlApplicationEngine()
    
    # Ajout du répertoire de l'application au chemin de recherche QML
    # Cela permet au StackView de trouver login.qml
    engine.addImportPath(os.path.dirname(os.path.abspath(__file__)))
    
    # Instanciation du backend
    backend = ChessBackend()
    
    # Exposition du backend dans le contexte QML
    engine.rootContext().setContextProperty("backend", backend)
    
    # Charger la page principale
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    engine.load(QUrl.fromLocalFile(qml_file))
    
    # Vérification que le fichier QML a bien été chargé
    if not engine.rootObjects():
        sys.exit(-1)
    
    return app.exec()

def main():
    ensure_chess_pieces_exist()
    sys.exit(qml_loader())

if __name__ == "__main__":
    main()
