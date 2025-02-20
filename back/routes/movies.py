from flask import jsonify, request
from routes import app, supabase_client
from jose import jwt
import os

@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        response = supabase_client.table('movies').select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/preferences', methods=['POST'])
def save_preferences():
    try:
        data = request.json
        user_id = data.get('user_id')
        genres = data.get('genres')  # Lista de géneros preferidos

        # Guardar preferencias en Supabase
        response = supabase_client.table('user_preferences').insert({
            "user_id": user_id,
            "genres": genres
        }).execute()

        return jsonify({"message": "Preferencias guardadas exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        # Obtener preferencias del usuario
        preferences = supabase_client.table('user_preferences')\
            .select("genres")\
            .eq('user_id', user_id)\
            .execute()

        if not preferences.data:
            return jsonify({"message": "No se encontraron preferencias"}), 404

        # Obtener películas que coincidan con los géneros preferidos
        user_genres = preferences.data[0]['genres']
        movies = supabase_client.table('movies')\
            .select("*")\
            .contains('genres', user_genres)\
            .execute()

        return jsonify(movies.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 