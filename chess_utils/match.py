class Match:
    def __init__(self, id=0, player1_id=0, player2_id=0, winner_id=None, start_time = "", end_time="", status="en cours", moves=None):    
        self.id = id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner_id = winner_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.moves = moves 

    def to_dict(self):
        return {
            "id": self.id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "winner_id": self.winner_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "moves": self.moves
        }


