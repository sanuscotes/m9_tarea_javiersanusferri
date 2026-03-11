import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:

    # autenticación
    APP_USER = os.getenv("APP_USER")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    # seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    # rutas
    DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "data"))

    # cache
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))