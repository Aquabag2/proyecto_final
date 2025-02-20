from supabase import create_client
import os
from dotenv import load_dotenv

print("1. Iniciando script...")

# Cargar variables de entorno
load_dotenv()
print("2. Variables de entorno cargadas")

# Obtener credenciales
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

print("3. URL:", supabase_url)
print("4. Key:", supabase_key[:10] + "..." if supabase_key else None)

try:
    # Intentar conectar con Supabase
    print("5. Intentando conectar con Supabase...")
    supabase = create_client(supabase_url, supabase_key)
    print("6. Cliente creado")
    
    # Intentar una consulta simple
    response = supabase.table('movies').select("*").execute()
    print("7. Conexión exitosa!")
    print("8. Datos:", response.data)
    
except Exception as e:
    print("Error:", str(e))
