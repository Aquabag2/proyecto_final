from flask import jsonify, request
from routes import app, supabase_client

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        user = supabase_client.auth.sign_up({
            'email': data['email'],
            'password': data['password']
        })
        
        supabase_client.table('profiles').insert({
            'id': user.user.id,
            'username': data['username'],
            'favorite_movies': []
        }).execute()
        
        return jsonify({"message": "Usuario registrado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        response = supabase_client.auth.sign_in_with_password({
            'email': data['email'],
            'password': data['password']
        })
        return jsonify({
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401 