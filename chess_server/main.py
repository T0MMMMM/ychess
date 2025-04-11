import time
import threading
from itertools import permutations
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from chess_server.crud import (
    add_move_to_match, create_match, db_login, 
    get_elo_by_id, get_user_by_id, get_match_by_id, update_match_winner, update_elo, add_win_to_user, add_loss_to_user
)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

users_file = []  # Liste des joueurs en attente de matchmaking
users_server = {}  # Association des ID utilisateurs avec leurs SID

# -------------------------------- WebSockets Handlers --------------------------------
@socketio.on("move")
def handle_move(data):
    match_id, move, opponent_id = data["match_id"], data["move"], data["opponent_id"]
    add_move_to_match(match_id, move)
    socketio.emit("move", move, room=find_SID_by_user_id(opponent_id))

@socketio.on('connect')
def on_connect():
    print(f"Client connecté avec SID : {request.sid}")

@socketio.on('register')
def handle_register(data):
    user = data.get('user')
    if user:
        users_server[user.get("id")] = request.sid
        print(f"Utilisateur {user.get('id')} enregistré avec SID {request.sid}")

@socketio.on("resign")
def handle_resignation(data):
    match_id, opponent_id, resigning_player = data["match_id"], data["opponent_id"], data["resigning_player"]
    winner = "black" if resigning_player == "white" else "white"
    socketio.emit("opponent_resigned", {"match_id": match_id, "winner": winner}, room=find_SID_by_user_id(opponent_id))


@socketio.on('game_over')
def handle_game_over(data):
    print(f"[Server] Fin de partie")
    print("→ Données :", data)
    print(data["winner"])
    print(data["match_id"])
    game_over(data)


def game_over(data):
    match = get_match_by_id(data["match_id"])
    id_winner = match.player1_id if data["winner"] == "white" else match.player2_id
    id_loser = match.player2_id if data["winner"] == "white" else match.player1_id
    update_match_winner(match.id, id_winner)
    update_elo_players(id_winner, id_loser, 1)
    update_elo_players(id_loser, id_winner, 0)


def update_elo_players(player_id, opponent_id, resultat):
    elo_player = get_elo_by_id(player_id)
    elo_opponent = get_elo_by_id(opponent_id)
    win_probability = calculate_win_probability(elo_player, elo_opponent)

    new_elo = elo_player + 50 * (resultat - win_probability)
    if resultat == 1:
        add_win_to_user(player_id)
    else:
        add_loss_to_user(player_id)
    update_elo(player_id, new_elo)

def calculate_win_probability(elo_joueur, elo_adversaire, scale=700):
    probability = 1 / (1 + 10 ** ((elo_adversaire - elo_joueur) / scale))
    return round(probability, 1)

# -------------------------------- API Routes --------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    success, player = db_login(data.get('username'), data.get('password'))
    return jsonify({"success": success, "player": player if success else "Invalid credentials"}), 200 if success else 401

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    player = get_user_by_id(user_id)
    return jsonify({"success": bool(player), "player": player or "User not found"}), 200 if player else 404

@app.route('/api/play', methods=['POST'])
def play():
    users_file.append(request.json.get('user')['id'])
    return jsonify({"success": True, "message": "User added to list"})

@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    users_file.remove(request.json.get('user')['id'])
    return jsonify({"success": True, "message": "User removed from list"})



# -------------------------------- Matchmaking Logic --------------------------------
def find_SID_by_user_id(user_id):
    return users_server.get(user_id)

def matchmaking():
    sort_by_elo()
    matches = matchmaking_optimal()
    if matches:
        for match in matches:
            new_match(match)
        matches.clear()
        print("Matchmaking successful")
    else:
        print("Pas assez de joueurs")

def sort_by_elo():
    users_file.sort(key=get_elo_by_id)

def matchmaking_optimal():
    if len(users_file) < 2:
        return None
    best_match, min_total_gap = None, float('inf')
    for perm in permutations(users_file):
        total_gap = sum(abs(get_elo_by_id(perm[i]) - get_elo_by_id(perm[i + 1])) for i in range(0, len(perm) - 1, 2))
        if total_gap < min_total_gap:
            min_total_gap, best_match = total_gap, [(perm[i], perm[i+1]) for i in range(0, len(perm) - 1, 2)]
    return best_match

def new_match(tab):
    user1_id, user2_id = tab
    match_id = create_match(user1_id, user2_id)
    socketio.emit("match", {"match_id": match_id, "color": "white", "opponent_id": user2_id}, room=find_SID_by_user_id(user1_id))
    socketio.emit("match", {"match_id": match_id, "color": "black", "opponent_id": user1_id}, room=find_SID_by_user_id(user2_id))
    users_file.remove(user1_id)
    users_file.remove(user2_id)

def matchmaking_loop():
    while True:
        time.sleep(5)
        matchmaking()



if __name__ == '__main__':
    threading.Thread(target=matchmaking_loop, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
