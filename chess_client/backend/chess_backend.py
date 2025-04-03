import requests
import socketio
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty

from chess_utils.player import Player
from chess_client.models.chess_game_model import ChessGameModel
from chess_client.models.web_socket_chess_game import WebSocketChessGame

class ChessBackend(QObject):
    """
    Backend de l'application d'échecs gérant la communication entre l'interface utilisateur et le serveur.
    
    Cette classe gère l'authentification des utilisateurs, la recherche de parties et
    les connexions WebSocket pour le jeu d'échecs en temps réel.
    """

    # Signaux pour la modification du front en temps réel
    userChanged = pyqtSignal()
    loginResult = pyqtSignal(bool, arguments=['success'])
    chessGameChanged = pyqtSignal()
    matchFound = pyqtSignal(dict)

    def __init__(self):
        """
        Initialise le ChessBackend avec les données du joueur, les connexions au serveur et les gestionnaires WebSocket.
        """
        super().__init__()
        self._user = Player()
        self.server_url = "http://localhost:5000/api"
        self._chess_game_model = ChessGameModel()
        
        # Créer une seule instance de socketio.Client
        self.sio = socketio.Client(logger=False, engineio_logger=False)
        self._chess_game = WebSocketChessGame(self.sio)
        
        # Configurer les handlers avant la connexion
        @self.sio.on('connect')
        def on_connect():
            """Gère l'événement de connexion WebSocket."""
            print("Connecté au serveur WebSocket")
            if self._user.id != 0:
                self.sio.emit("register", {'user': self._user.to_dict()})

        @self.sio.on('disconnect')
        def on_disconnect():
            """Gère l'événement de déconnexion WebSocket."""
            print("Déconnecté du serveur WebSocket")

        @self.sio.on('play_confirmation')
        def on_play_confirmation(data):
            """Gère la confirmation du serveur pour une demande de matchmaking."""
            print(f"Confirmation du serveur : {data['message']}")

        @self.sio.on("match")
        def on_match(data):
            """
            Gère l'événement de match trouvé depuis le serveur.
            Configure les détails du jeu et notifie l'interface qu'un match a été trouvé.
            
            Args:
                data (dict): Détails du match incluant match_id, color et opponent_id
            """
            print("Événement de match trouvé reçu:", data)
            game_id = data.get('match_id')
            player_color = data.get('color')
            opponent_id = data.get('opponent_id')
            
            print(f"Configuration de la partie: id={game_id}, couleur={player_color}, adversaire={opponent_id}")
            self._chess_game.set_game_details(game_id, player_color, opponent_id)
            self.chessGameChanged.emit()
            print("Émission du signal matchFound")
            self.matchFound.emit(data)
        
        @self.sio.on("move")
        def on_move(data):
            """
            Gère le mouvement reçu de l'adversaire via WebSocket.
            
            Args:
                data (dict): Détails du mouvement incluant les cases de départ et d'arrivée
            """
            print(f"Mouvement reçu: {data}")
            self._chess_game.receive_opponent_move(
                data.get('from'),
                data.get('to')
            )
            self.chessGameChanged.emit()

        # Se connecter au serveur
        try:
            self.sio.connect('http://localhost:5000', wait_timeout=10)
            print("Connecté au serveur WebSocket")
        except Exception as e:
            print(f"Erreur de connexion WebSocket : {e}")
            self.sio = None

    @pyqtSlot()
    def play(self):
        """
        Commence la recherche d'un adversaire.
        
        Réinitialise le plateau d'échecs et envoie une requête au serveur pour trouver un adversaire.
        L'utilisateur doit être connecté pour utiliser cette fonction.
        """
        if self._user.id == 0:
            print("Vous devez être connecté pour jouer")
            return
        try: 
            # Réinitialiser l'état du jeu avant de chercher une nouvelle partie
            self._chess_game.reset_game()
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
        """
        Récupère l'instance de jeu d'échecs actuelle.
        
        Returns:
            WebSocketChessGame: Le jeu d'échecs actuel
        """
        return self._chess_game
    
    @pyqtSlot(str, str)
    def makeMove(self, from_square, to_square):
        """
        Effectue un mouvement sur l'échiquier.
        
        Args:
            from_square (str): Notation de la case de départ (ex: 'e2')
            to_square (str): Notation de la case d'arrivée (ex: 'e4')
            
        Returns:
            bool: True si le mouvement a réussi, False sinon
        """
        success = self._chess_game.make_move(from_square, to_square)
        if success:
            self.chessGameChanged.emit()
        return success
    
    @pyqtSlot(str, str)
    def login(self, username, password):
        """
        Authentifie l'utilisateur auprès du serveur.
        
        Envoie les identifiants au serveur et traite la réponse.
        En cas de connexion réussie, met à jour les données utilisateur et émet des signaux pour mettre à jour l'interface.
        
        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe
        """
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
                        password_hash='',  # Ne pas stocker le hash du mot de passe côté client
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
            print(f"Erreur de connexion: {e}")
        
        # Si nous arrivons ici, la connexion a échoué
        self._user = Player()
        self.loginResult.emit(False)
        self.userChanged.emit()

    @pyqtSlot()
    def cancelMatchmaking(self):
        """
        Annule la demande de matchmaking en cours.
        
        Notifie le serveur de retirer le joueur de la file d'attente de matchmaking.
        """
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
        """
        Déconnecte l'utilisateur actuel.
        
        Réinitialise les données utilisateur aux valeurs par défaut et notifie l'interface du changement.
        """
        print("Déconnexion")
        self._user = Player()
        self.userChanged.emit()
    
    @pyqtProperty(Player, notify=userChanged)
    def user(self):
        """
        Récupère les données de l'utilisateur actuel.
        
        Returns:
            Player: Objet joueur actuel
        """
        return self._user
        
    @pyqtProperty(bool, notify=userChanged)
    def isLoggedIn(self):
        """
        Vérifie si un utilisateur est actuellement connecté.
        
        Returns:
            bool: True si l'utilisateur est connecté, False sinon
        """
        return self._user.username != ""
