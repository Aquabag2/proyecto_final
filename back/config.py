import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Asignación directa de valores
    SUPABASE_URL = "https://yhjkkqtnrddcmfodnukk.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InloamtrcXRucmRkY21mb2RudWtrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODM2NjM3NiwiZXhwIjoyMDUzOTQyMzc2fQ.kMNM6pDlpjarhQFrffH05sFH3O9OoRnjkm9BFpGbcIU"
    SUPABASE_JWT_SECRET = "vSshJBceS2vZCnm4eg83rEuQ5Gtk/VPYdT6X4HYKAQkJIWoKY2cuM+BMRAHLbulEnYrkEpOXnTxXfDRV" 