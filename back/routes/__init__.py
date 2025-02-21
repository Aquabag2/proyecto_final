from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify, g
from flask_cors import CORS
from config import Config
from supabase import create_client, Client
import os
import requests

print("Inicializando Flask...")
app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static')
CORS(app)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

print("Conectando con Supabase...")
try:
    supabase_client = create_client(
        app.config['SUPABASE_URL'],
        app.config['SUPABASE_KEY']
    )
    print("Conexión con Supabase exitosa")
except Exception as e:
    print(f"Error al conectar con Supabase: {str(e)}")

# Configuración TMDB
TMDB_API_KEY = "tu_api_key_aquí"  # Reemplaza con tu API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_movies_by_genre():
    # Lista de géneros populares
    genres = [
        {"id": 28, "name": "Acción"},
        {"id": 27, "name": "Terror"},
        {"id": 35, "name": "Comedia"},
        {"id": 18, "name": "Drama"},
        {"id": 878, "name": "Ciencia ficción"},
        {"id": 10749, "name": "Romance"}
    ]
    
    movies_by_genre = []
    
    for genre in genres:
        try:
            # Obtener películas por género
            response = requests.get(
                f"{TMDB_BASE_URL}/discover/movie",
                params={
                    "api_key": TMDB_API_KEY,
                    "with_genres": genre["id"],
                    "language": "es-ES",
                    "sort_by": "popularity.desc",
                    "page": 1
                }
            )
            
            if response.status_code == 200:
                movies_data = response.json()["results"]
                movies = []
                
                for movie in movies_data[:10]:  # Limitamos a 10 películas por género
                    movies.append({
                        "id": movie["id"],
                        "title": movie["title"],
                        "poster_url": f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}" if movie['poster_path'] else "/static/images/no-poster.jpg",
                        "rating": round(movie["vote_average"], 1),
                        "overview": movie["overview"],
                        "release_date": movie["release_date"]
                    })
                
                movies_by_genre.append({
                    "name": genre["name"],
                    "movies": movies
                })
                
        except Exception as e:
            print(f"Error fetching {genre['name']} movies: {str(e)}")
            continue
    
    return movies_by_genre

# Ruta principal
@app.route('/')
def home():
    try:
        print("Intentando renderizar index.html...")
        return render_template('index.html')
    except Exception as e:
        print(f"Error al renderizar: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Simplificado: solo login y redirección
            auth_response = supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                session['email'] = email
                session['user_id'] = auth_response.user.id
                return redirect(url_for('user_dashboard'))
                
        except Exception as e:
            print(f"Error: {str(e)}")
            flash('Error en login', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')  # Agregamos el campo nombre
        
        if not email or not password or not name:  # Validamos que exista el nombre
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('register'))
            
        try:
            # Registrar usuario en Supabase
            response = supabase_client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Crear perfil con nombre
                supabase_client.table('profiles').insert({
                    "id": response.user.id,
                    "email": email,
                    "name": name,  # Guardamos el nombre
                    "role": "user"
                }).execute()
                
                flash('¡Registro exitoso! Ya puedes iniciar sesión', 'success')
                return redirect(url_for('login'))
                
        except Exception as e:
            print(f"Error en registro: {str(e)}")
            flash('Error al registrar usuario', 'error')
            
        return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('user_dashboard.html')

@app.route('/moderator-dashboard')
def moderator_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('role') != 'moderator':
        return redirect(url_for('user_dashboard'))
    return render_template('moderator_dashboard.html')

@app.route('/api/rate-movie', methods=['POST'])
def rate_movie():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    data = request.get_json()
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    user_id = g.user.id  # Asumiendo que tienes el usuario en g

    try:
        # Guardar la calificación en Supabase
        supabase_client.table('ratings').upsert({
            'user_id': user_id,
            'movie_id': movie_id,
            'rating': rating,
            'created_at': 'now()'
        }).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/submit-review', methods=['POST'])
def submit_review():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    data = request.get_json()
    movie_id = data.get('movie_id')
    review_text = data.get('review')
    user_id = g.user.id

    try:
        # Guardar la reseña en Supabase
        supabase_client.table('reviews').insert({
            'user_id': user_id,
            'movie_id': movie_id,
            'text': review_text,
            'created_at': 'now()'
        }).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-reviews/<movie_id>')
def get_reviews(movie_id):
    try:
        # Obtener reseñas de Supabase
        response = supabase_client.table('reviews')\
            .select('*, profiles(name, avatar_url)')\
            .eq('movie_id', movie_id)\
            .order('created_at', desc=True)\
            .execute()
        
        reviews = [{
            'user_name': review['profiles']['name'],
            'user_avatar': review['profiles']['avatar_url'],
            'text': review['text'],
            'rating': review['rating'],
            'date': review['created_at']
        } for review in response.data]
        
        return jsonify({'success': True, 'reviews': reviews})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    if 'email' not in session:
        return redirect(url_for('login'))
        
    try:
        # Obtener detalles de la película
        response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "es-ES"
            }
        )
        
        if response.status_code == 200:
            movie_data = response.json()
            movie = {
                "id": movie_data["id"],
                "title": movie_data["title"],
                "overview": movie_data["overview"],
                "poster_url": f"{TMDB_IMAGE_BASE_URL}{movie_data['poster_path']}" if movie_data['poster_path'] else "/static/images/no-poster.jpg",
                "rating": round(movie_data["vote_average"], 1),
                "release_date": movie_data["release_date"],
                "genres": [genre["name"] for genre in movie_data["genres"]],
                "runtime": movie_data["runtime"]
            }
            
            return render_template('movie_detail.html', movie=movie)
            
    except Exception as e:
        print(f"Error fetching movie details: {str(e)}")
        flash('Error al cargar los detalles de la película', 'error')
        
    return redirect(url_for('user_dashboard'))

print("Flask inicializado correctamente") 