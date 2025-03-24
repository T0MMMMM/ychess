from itertools import permutations
import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from chess_server.crud import add_move_to_match, create_match, db_login, get_elo_by_id, get_user_by_id
import threading

app = Flask(__name__)
# Modifier la configuration de SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=True, async_mode='threading')

users_file = []
users_server = {}

def find_SID_by_user_id(user_id):
    return users_server.get(user_id)


@socketio.on("move")
def handle_move(data):
    match_id = data["match_id"]
    move = data["move"]
    opponent_id = data["opponent_id"]
    add_move_to_match(match_id, move)
    socketio.emit("move", move, room=find_SID_by_user_id(opponent_id))


@socketio.on('connect')
def on_connect():
    print(f"Un client s'est connecté avec SID : {request.sid}")

@socketio.on('register')
def handle_register(data):
    user = data.get('user')
    if not user:
        return 
    id = user.get("id")
    print(f"L'utilisateur {id} est enregistré avec SID {request.sid}")
    users_server[id] = request.sid

@socketio.on("resign")
def handle_resignation(data):
    match_id = data["match_id"]
    opponent_id = data["opponent_id"]
    resigning_player = data["resigning_player"]
    
    # Émettre l'événement de résignation à l'adversaire
    socketio.emit("opponent_resigned", {
        "match_id": match_id,
        "winner": "black" if resigning_player == "white" else "white"
    }, room=find_SID_by_user_id(opponent_id))

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    success, player = db_login(username, password)
    
    if success and player:
        # Convert Player object to dictionary for JSON serialization
        return jsonify({"success": True, "player": player})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    player = get_user_by_id(user_id)
    
    if player:
        # Convert Player object to dictionary for JSON serialization
        return jsonify({"success": True, "player": player})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404
    


@app.route('/api/play', methods=['POST'])
def play():
    data = request.json
    user = data.get('user')
    users_file.append(user["id"])
    return jsonify({"success": True, "message": "User added to list"})
    
@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    data = request.json
    user = data.get('user')
    users_file.remove(user['id'])
    return jsonify({"success": True, "message": "User removed to list"})

def matchmaking():
    sort_by_elo()
    matches = matchmaking_optimal()
    if matches != None:
        for match in matches:
            new_match(match)
        matches.clear()
        print("Matchmaking successful")
    else:
        print("Pas assez de joueurs")



def sort_by_elo():
    for i in range(len(users_file)):
        for j in range(len(users_file)-1):
            if get_elo_by_id(users_file[i]) < get_elo_by_id(users_file[j]):
                users_file[i], users_file[j] = users_file[j], users_file[i]


def matchmaking_optimal():
    if len(users_file) < 2:
        return None  

    best_match = None
    min_total_gap: float = float('inf')

    for perm in permutations(users_file):
        total_gap = calcul_total_gap(perm)

        if total_gap < min_total_gap:
            min_total_gap = total_gap
            best_match = [(perm[i], perm[i+1]) for i in range(0, len(perm) - 1, 2)]
    return best_match


def calcul_total_gap(perm):
    total_gap = 0
    for i in range(0, len(perm) - 1, 2):
        joueur1, joueur2 = perm[i], perm[i + 1]
        gap = abs(get_elo_by_id(joueur1) - get_elo_by_id(joueur2))  # Différence de niveau entre les deux joueurs
        total_gap += gap  # On additionne cet écart au total
    return total_gap


def new_match(tab):
    print("Creating new match between players:", tab)
    user1_id = tab[0]
    user2_id = tab[1]
    match_id = create_match(user1_id, user2_id)
    
    # Premier joueur en blanc, second en noir
    print(f"Player {user1_id} is white, {user2_id} is black")

    # Envoyer les détails du match aux joueurs
    socketio.emit("match", {
        "match_id": match_id,
        "color": "white",  # Premier joueur est blanc
        "opponent_id": user2_id 
    }, room=find_SID_by_user_id(tab[0]))
    
    socketio.emit("match", {
        "match_id": match_id,
        "color": "black",  # Second joueur est noir
        "opponent_id": user1_id 
    }, room=find_SID_by_user_id(tab[1]))

    users_file.remove(user1_id)
    users_file.remove(user2_id)



def matchmaking_loop():
    while True:
        time.sleep(5)  # Vérifier toutes les 5 secondes
        matchmaking()

if __name__ == '__main__':
    matchmaking_thread = threading.Thread(target=matchmaking_loop)
    matchmaking_thread.daemon = True  # Le thread s'arrêtera quand le programme principal s'arrête
    matchmaking_thread.start()
    # Modifier le lancement du serveur
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)