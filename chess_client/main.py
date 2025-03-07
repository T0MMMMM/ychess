import sys
import os
import requests

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, pyqtProperty
from chess_utils.player import Player

class ChessBackend(QObject):
    # Ces deux signaux sont nécessaires mais pour des raisons différentes:
    userChanged = pyqtSignal()  # Pour les liaisons QML automatiques
    loginResult = pyqtSignal(bool, arguments=['success'])  # Pour la navigation explicite

    def __init__(self):
        super().__init__()
        self._user = Player()
        self.server_url = "http://localhost:5000/api"
    
    @pyqtSlot()
    def play(self):
        if self._user.id == 0:
            print("Vous devez être connecté pour jouer")
            return
        try: 
            response = requests.post(f'{self.server_url}/play', json={'user': self._user.to_dict()})
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print("Joueur ajouté à la liste")
        except Exception as e:
            print(f"Erreur lors de la tentative de connexion: {e}")
            
    
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
    # Création de l'application
    app = QGuiApplication(sys.argv)
    
    # Register the Player type with QML before creating the engine
    # This enables exposing Player objects directly to QML
    qmlRegisterType(Player, "ChessTypes", 1, 0, "Player")
    
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
    sys.exit(qml_loader())

if __name__ == "__main__":
    main()
