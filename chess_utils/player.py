from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, QDateTime

class Player(QObject):
    # Signal to notify changes
    dataChanged = pyqtSignal()
    
    def __init__(self, id=0, username="", password_hash="", email="", elo=0, 
                 matches_played=0, wins=0, losses=0, registration_date=None, last_login=None):
        super().__init__()  # Make sure QObject.__init__ is called
        self._id = id
        self._username = username
        self._password_hash = password_hash
        self._email = email
        self._elo = elo
        self._matches_played = matches_played
        self._wins = wins
        self._losses = losses
        self._registration_date = registration_date
        self._last_login = last_login
    
    # Define properties using getters and setters with pyqtProperty
    @pyqtProperty(int, notify=dataChanged)
    def id(self):
        return self._id
        
    @pyqtProperty(str, notify=dataChanged)
    def username(self):
        return self._username
        
    @pyqtProperty(int, notify=dataChanged)
    def elo(self):
        return self._elo
        
    @pyqtProperty(int, notify=dataChanged)
    def matches_played(self):
        return self._matches_played
        
    @pyqtProperty(int, notify=dataChanged)
    def wins(self):
        return self._wins
        
    @pyqtProperty(int, notify=dataChanged)
    def losses(self):
        return self._losses
    
    # Email is not exposed to QML by default for privacy reasons
    # Registration date and last login can be added if needed
