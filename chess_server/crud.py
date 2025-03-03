import sqlite3

from chess_utils.player import Player


def get_player_by_id(player_id):
    conn = sqlite3.connect("chess_server/database.db")
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE id = ?", (player_id,))
    row = cursor.fetchone()
    conn.close()
    if row: return Player(**dict(row))  # Création d'un objet Player
    return None

def db_login(username, password):
    conn = sqlite3.connect("chess_server/database.db")
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    cursor = conn.cursor()

    # Récupérer l'utilisateur par son username
    cursor.execute("SELECT * FROM player WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Comparer le hash stocké avec le mot de passe entré
        if password == row["password_hash"]:
            return (True, Player(**dict(row)))
        return (False, None)
    return (False, None)

def get_user_by_id(user_id):
    conn = sqlite3.connect("chess_server/database.db")
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row: return Player(**dict(row))  # Création d'un objet Player
    return None