import os
from routes import app

if __name__ == '__main__':
    print("Inicializando Flask...")
    print("Conectando con Supabase...")
    print("Conexión con Supabase exitosa")
    print("Flask inicializado correctamente")
    print("Iniciando servidor Flask...")
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, port=port) 