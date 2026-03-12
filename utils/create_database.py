# Importamos las librerías necesarias
import pandas as pd
import sqlite3

# Definimos las rutas
csv_path = "data/market_value.csv"
db_path = "data/players.db"

# Cargar csv
df = pd.read_csv(csv_path, sep=";")

# Conectar a sqlite
conn = sqlite3.connect(db_path)

# Guardar tabla
df.to_sql(
    "players_market_value",
    conn,
    if_exists="replace",
    index=False
)

# Cerramos la conexión
conn.close()

print("Base de datos creada correctamente")