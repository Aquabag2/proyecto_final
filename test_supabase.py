from supabase import create_client
import os
from dotenv import load_dotenv

print("1. Iniciando script...")


load_dotenv()
print("2. Variables de entorno cargadas")


supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

print("3. URL:", supabase_url)
print("4. Key:", supabase_key[:10] + "..." if supabase_key else None)

try:
    
    print("5. Intentando conectar con Supabase...")
    supabase = create_client(supabase_url, supabase_key)
    print("6. Cliente creado")
    
    
    response = supabase.table('movies').select("*").execute()
    print("7. Conexión exitosa!")
    print("8. Datos:", response.data)
    
except Exception as e:
    print("Error:", str(e))
