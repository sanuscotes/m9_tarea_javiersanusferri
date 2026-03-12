# Importación de librerías necesarias
import pandas as pd
import sqlite3
from config import Config
from utils.cache import cache

# Optimización mediante cache
@cache.memoize()
def load_performance_data():
    """
    Carga los datos de rendimiento de jugadores desde un archivo CSV.

    Descripción
    -----------
    Esta función lee el archivo `performance.csv` ubicado en la ruta definida en la configuración 
    de la aplicación y devuelve los datos en forma de DataFrame de pandas.

    Optimización mediante cache
    ----------------------------
    Esto mejora significativamente el rendimiento del dashboard.

    Devuelve
    --------
    pandas.DataFrame
        DataFrame que contiene los datos de rendimiento de jugadores.
    """
    df = pd.read_csv(Config.DATA_PATH + "performance.csv")
    return df

# Optimización mediante cache
@cache.memoize()
def load_market_value_data():
    """
    Carga los datos de valor de mercado de jugadores desde una base de datos SQLite.

    Descripción
    -----------
    Esta función se conecta a la base de datos `players.db`, consulta la tabla `players_market_value` 
    y devuelve los resultados en forma de DataFrame de pandas.

    Optimización mediante cache
    ----------------------------
    Esto evita repetir consultas SQL innecesarias y mejora el rendimiento del dashboard.

    Devuelve
    --------
    pandas.DataFrame
        DataFrame con los datos de valor de mercado de los jugadores.
    """
    conn = sqlite3.connect(Config.DATA_PATH + "players.db")
    df = pd.read_sql("SELECT * FROM players_market_value", conn)
    conn.close()
    return df