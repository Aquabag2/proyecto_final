from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_cors import CORS
from config import Config
from supabase import create_client, Client
import os

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
        remember = request.form.get('remember')
        
        if not email or not password:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('login'))
        
        try:
            # Iniciar sesión en Supabase
            response = supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            
            session['user_id'] = response.user.id
            session['email'] = email
            
            if remember:
                
                session.permanent = True
            
            flash('¡Bienvenido de vuelta!', 'success')
            return redirect(url_for('menu'))
            
        except Exception as e:
            print(f"Error en login: {str(e)}")
            flash('Email o contraseña incorrectos', 'error')
            return redirect(url_for('login'))
            
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
        confirm_password = request.form.get('confirm_password')
        
        print(f"Intentando registrar email: {email}")  # Debug
        
        
        if not email or not password or not confirm_password:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('register'))
            
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('register'))
            
        try:
            print("Iniciando registro en Supabase...")
            
            response = supabase_client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            print("Respuesta de Supabase:", response)  # Debug
            
            if hasattr(response, 'user') and response.user:
                try:
                    
                    profile_data = {
                        "id": response.user.id,
                        "email": email,
                        "created_at": 'now()'
                    }
                    print("Creando perfil:", profile_data)
                    
                    supabase_client.table('profiles').insert(profile_data).execute()
                    print("Perfil creado exitosamente")
                    
                except Exception as profile_error:
                    print(f"Error al crear perfil: {str(profile_error)}")
                
                flash('Registro exitoso! Por favor verifica tu email', 'success')
                return redirect(url_for('login'))
            else:
                print("No se recibió usuario en la respuesta")
                flash('Error al registrar usuario', 'error')
                
        except Exception as e:
            print(f"Error detallado en registro: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            flash('Error al registrar usuario. Por favor intenta de nuevo.', 'error')
            return redirect(url_for('register'))
            
    return render_template('register.html')



print("Flask inicializado correctamente") 