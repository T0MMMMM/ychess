import sys
import os

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, pyqtProperty
from chess_server.crud import db_login
from chess_utils.player import Player

class ChessBackend(QObject):
    # Ces deux signaux sont nécessaires mais pour des raisons différentes:
    userChanged = pyqtSignal()  # Pour les liaisons QML automatiques
    loginResult = pyqtSignal(bool, arguments=['success'])  # Pour la navigation explicite

    def __init__(self):
        super().__init__()
        self._user = Player()
    
    @pyqtSlot()
    def jouer(self):
        print("Fonction jouer appelée depuis Python")
        # Ajoutez ici votre logique pour le bouton Jouer
    
    @pyqtSlot(str, str)
    def login(self, username, password):
        print(f"Tentative de connexion avec username: {username}")
        # En production, ne jamais afficher les mots de passe en clair dans les logs
        print(f"Mot de passe (longueur: {len(password)}): {password[:1]}****")
        
        success, user = db_login(username, password)
        self._user = user if success else Player()
        
        # Émettre le signal avec le résultat
        self.loginResult.emit(success)
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
