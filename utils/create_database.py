import pandas as pd
import sqlite3

# rutas
csv_path = "data/market_value.csv"
db_path = "data/players.db"

# cargar csv
df = pd.read_csv(csv_path, sep=";")

# conectar a sqlite
conn = sqlite3.connect(db_path)

# guardar tabla
df.to_sql(
    "players_market_value",
    conn,
    if_exists="replace",
    index=False
)

# cerrar conexión
conn.close()

print("Base de datos creada correctamente")