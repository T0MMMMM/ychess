from flask import Flask, request, jsonify
from chess_server.crud import db_login, get_user_by_id

app = Flask(__name__)

users_in_file = []

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
    if not user in users_in_file:
        users_in_file.append(user)
    print(users_in_file)
    return jsonify({"success": True, "message": "User added to list"})
    #if success and player:
    #    # Convert Player object to dictionary for JSON serialization
#  return jsonify({"success": True, "player": player})
   # else:
    #    return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    data = request.json
    user = data.get('user')
    if user in users_in_file:
        users_in_file.remove(user)
    print(users_in_file)
    return jsonify({"success": True, "message": "User removed to list"})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
