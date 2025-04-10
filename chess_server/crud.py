import sqlite3
import datetime

from flask import json
import datetime

from flask import json
from chess_utils.player import Player
from chess_utils.match import Match

def get_player_by_id(player_id):
    conn = sqlite3.connect("chess_server/database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE id = ?", (player_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Create Player object with specific parameters instead of unpacking
        row_dict = dict(row)
        return row_dict
    return None

def db_login(username, password):
    conn = sqlite3.connect("chess_server/database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Comparer le hash stocké avec le mot de passe entré
        if password == row["password_hash"]:
            # Create Player object with named parameters
            row_dict = dict(row)
            return (True, row_dict)
        return (False, None)
    return (False, None)

def get_user_by_id(user_id):
    conn = sqlite3.connect("chess_server/database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Create Player object with specific parameters instead of unpacking
        row_dict = dict(row)
        return Player(
            id=row_dict.get("id", 0),
            username=row_dict.get("username", ""),
            password_hash=row_dict.get("password_hash", ""),
            email=row_dict.get("email", ""),
            elo=row_dict.get("elo", 0),
            matches_played=row_dict.get("matches_played", 0),
            wins=row_dict.get("wins", 0),
            losses=row_dict.get("losses", 0),
            registration_date=row_dict.get("registration_date", None),
            last_login=row_dict.get("last_login", None)
        )
    return None

def create_match(player1_id, player2_id):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO match (player1_id, player2_id, winner_id, start_time, end_time, status, moves) \
                   VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (player1_id, player2_id, None, datetime.datetime.now(), None, "en cours", "[]"))  
    match_id = cursor.lastrowid 
    conn.commit()
    conn.close()
    return match_id




def add_move_to_match(match_id, move):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT moves FROM match WHERE id = ?", (match_id,))
    result = cursor.fetchone()
    moves = json.loads(result[0]) if result[0] else []
    moves.append(move)
    cursor.execute("UPDATE match SET moves = ? WHERE id = ?", (json.dumps(moves), match_id))
    conn.commit()
    conn.close()

def get_elo_by_id(user_id):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT elo FROM player WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0]
    return None


def get_match_by_id(match_id):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    
    # Récupérer les noms des colonnes
    cursor.execute("PRAGMA table_info(match)")
    columns = [column[1] for column in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM match WHERE id = ?", (match_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Créer un dictionnaire à partir du tuple et des noms de colonnes
        row_dict = dict(zip(columns, row))
        return Match(
            id = row_dict.get("id", 0),
            player1_id=row_dict.get("player1_id", 0),
            player2_id=row_dict.get("player2_id", 0),
            winner_id=row_dict.get("winner_id", None),
            start_time=row_dict.get("start_time", ""),
            end_time=row_dict.get("end_time", ""),
            status=row_dict.get("status", "en cours"),
            moves=json.loads(row_dict.get("moves", "[]"))
        )
    return None


def update_match_winner(match_id, winner_id):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE match SET winner_id = ?, end_time = ?, status = ? WHERE id = ?", 
                   (winner_id, datetime.datetime.now(), "terminé", match_id))
    conn.commit()
    conn.close()

def create_match(player1_id, player2_id):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO match (player1_id, player2_id, winner_id, start_time, end_time, status, moves) \
                   VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (player1_id, player2_id, None, datetime.datetime.now(), None, "en cours", "[]"))  
    match_id = cursor.lastrowid 
    conn.commit()
    conn.close()
    return match_id

def add_move_to_match(match_id, move):
    conn = sqlite3.connect("chess_server/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT moves FROM match WHERE id = ?", (match_id,))
    result = cursor.fetchone()
    moves = json.loads(result[0]) if result[0] else []
    moves.append(move)
    cursor.execute("UPDATE match SET moves = ? WHERE id = ?", (json.dumps(moves), match_id))
    conn.commit()
    conn.close()