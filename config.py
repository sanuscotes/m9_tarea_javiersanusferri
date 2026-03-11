import os
from dotenv import load_dotenv

# cargar variables del .env
load_dotenv()

class Config:

    # autenticación
    APP_USER = os.getenv("APP_USER")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    # seguridad
    SECRET_KEY = os.getenv("SECRET_KEY")

    # rutas
    DATA_PATH = os.getenv("DATA_PATH")

    # cache
    CACHE_TYPE = os.getenv("CACHE_TYPE", "simple")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))