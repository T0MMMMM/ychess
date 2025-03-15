import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from chess_server.crud import db_login, get_user_by_id
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Permet les connexions WebSocket


users_file = {}
users_server = {}


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
    users_file[user["id"]] = users_server.get(user["id"])
    return jsonify({"success": True, "message": "User added to list"})
    
@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    data = request.json
    user = data.get('user')
    users_file.pop(user['id'])
    return jsonify({"success": True, "message": "User removed to list"})

def matchmaking():
    if len(users_file) >= 2:
        print("Matchmaking successful")
    else:
        print("Matchmaking failed")
        print(users_file)



def matchmaking_loop():
    while True:
        time.sleep(5)  # Vérifier toutes les 5 secondes
        matchmaking()

if __name__ == '__main__':
    matchmaking_thread = threading.Thread(target=matchmaking_loop)
    matchmaking_thread.daemon = True  # Le thread s'arrêtera quand le programme principal s'arrête
    matchmaking_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
