import sys
import os
from pathlib import Path

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtCore import QUrl

from chess_utils.player import Player
from chess_client.models.chess_game_model import ChessGameModel
from chess_client.models.web_socket_chess_game import WebSocketChessGame
from chess_client.backend.chess_backend import ChessBackend

def qml_loader():
    """
    Initialise le moteur d'application QML et charge le fichier QML principal.
    
    Returns:
        int: Code de sortie de l'application
    """
    app = QGuiApplication(sys.argv)
    
    # Enregistrement des types
    qmlRegisterType(Player, "ChessTypes", 1, 0, "Player")
    qmlRegisterType(ChessGameModel, "ChessTypes", 1, 0, "ChessGameModel")
    qmlRegisterType(WebSocketChessGame, "ChessTypes", 1, 0, "WebSocketChessGame")
    
    engine = QQmlApplicationEngine()
    
    # Définir les chemins d'importation corrects
    qml_path = Path(__file__).parent
    engine.addImportPath(str(qml_path))
    
    # Définir la propriété de contexte racine pour le chemin des ressources
    engine.rootContext().setContextProperty(
        "assetsPath", 
        str(qml_path / "assets")
    )
    
    # Créer le backend et l'exposer à QML
    backend = ChessBackend()
    engine.rootContext().setContextProperty("backend", backend)
    
    # Charger le fichier QML principal (depuis le nouveau dossier qml)
    qml_file = os.path.join(os.path.dirname(__file__), 'qml', 'main.qml')
    engine.load(QUrl.fromLocalFile(qml_file))
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    return app.exec()

def main():
    """
    Point d'entrée principal de l'application.
    """
    sys.exit(qml_loader())

if __name__ == "__main__":
    main()
