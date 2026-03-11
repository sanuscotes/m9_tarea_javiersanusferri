import pandas as pd
import sqlite3
from config import Config
from utils.cache import cache


@cache.memoize()
def load_performance_data():

    df = pd.read_csv(Config.DATA_PATH + "performance.csv")

    return df


@cache.memoize()
def load_market_value_data():

    conn = sqlite3.connect(Config.DATA_PATH + "players.db")

    df = pd.read_sql("SELECT * FROM players_market_value", conn)

    conn.close()

    return df