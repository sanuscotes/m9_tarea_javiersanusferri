# Importación de librerías
import os
# Librería para cargar variables de entorno
from dotenv import load_dotenv



# Carga de variables de entorno
load_dotenv()

# Directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Clase de configuración global que centraliza todas las configuraciones de la aplicación
class Config:

    # Configuración de autenticación
    APP_USER = os.getenv("APP_USER")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    # Configuración de seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    # Configuración de rutas de acceso a datos
    DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "data"))

    # Configuración del sistema de cache
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))