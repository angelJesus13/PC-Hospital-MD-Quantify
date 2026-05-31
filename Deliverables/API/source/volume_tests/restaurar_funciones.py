import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "hospital_hibrido_md")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

conn = mysql.connector.connect(
    host=MYSQL_HOST, port=int(MYSQL_PORT),
    user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB
)
cursor = conn.cursor()

funciones = [
    ("fn_generar_auditoria", "tests/sql/config/fn_generar_auditoria.sql"),
    ("fn_generar_antecedentes", "tests/sql/config/fn_generar_antecedentes.sql"),
    ("fn_generar_sintomas", "tests/sql/config/fn_generar_sintomas.sql"),
    ("fn_generar_interrogatorio", "tests/sql/config/fn_generar_interrogatorio.sql"),
    ("fn_generar_signos_vitales", "tests/sql/config/fn_generar_signos_vitales.sql")
]

for nombre, ruta in funciones:
    with open(ruta, "r", encoding="utf-8") as f:
        # Purgamos el texto especial de delimitadores de linea de comandos SQL
        sql_fn = f.read().replace("DELIMITER $$", "").replace("DELIMITER ;", "").replace("$$", "").strip()
        
    cursor.execute(f"DROP FUNCTION IF EXISTS {nombre}")
    cursor.execute(sql_fn)
    print(f"[OK] Función {nombre} restaurada.")

conn.commit()
cursor.close()
conn.close()
print("Todas las funciones auxiliares se inyectaron exitosamente al servidor MySQL.")
