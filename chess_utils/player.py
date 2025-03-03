class Player:
    def __init__(self, id, username, password_hash, email, elo, matches_played, wins, losses, registration_date, last_login):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.elo = elo
        self.matches_played = matches_played
        self.wins = wins
        self.losses = losses
        self.registration_date = registration_date
        self.last_login = last_login
