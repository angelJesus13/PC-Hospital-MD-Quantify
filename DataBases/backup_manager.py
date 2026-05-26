import os
import subprocess
import datetime
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / "Deliverables" / "API" / "source" / ".env"
SQL_BACKUP_DIR = BASE_DIR / "SQL" / "Backups"
NOSQL_BACKUP_DIR = BASE_DIR / "NoSQL" / "Backups"

def setup_environment():
    """Carga las variables de entorno y verifica que existan las carpetas de backup."""
    if not ENV_PATH.exists():
        print(f"❌ Error: No se encontró el archivo .env en {ENV_PATH}")
        return False

    load_dotenv(ENV_PATH)
    
    # Crear carpetas si no existen
    SQL_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    NOSQL_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    return True

def get_timestamp():
    """Devuelve un string con el formato YYYYMMDD_HHMM."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M")

def backup_mysql(timestamp):
    """Ejecuta el volcado de la base de datos MySQL usando mysqldump."""
    print("⏳ Iniciando backup de MySQL...")
    
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_user, db_password, db_name]):
        print("❌ Error: Faltan variables de entorno para MySQL (DB_USER, DB_PASSWORD, DB_NAME).")
        return False
        
    filename = SQL_BACKUP_DIR / f"db_backup_{timestamp}.sql"
    
    # Construir comando mysqldump
    # NOTA: En Windows, omitimos el espacio entre -p y la contraseña
    command = [
        "mysqldump",
        f"-h{db_host}",
        f"-u{db_user}",
        f"-p{db_password}",
        db_name
    ]
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            subprocess.run(command, stdout=f, stderr=subprocess.PIPE, check=True, text=True)
        print(f"✅ Backup de MySQL completado con éxito: {filename.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar mysqldump: {e.stderr}")
        if filename.exists():
            filename.unlink()  # Eliminar archivo vacío o corrupto
        return False
    except FileNotFoundError:
        print("❌ Error: 'mysqldump' no está instalado o no se encuentra en el PATH del sistema.")
        return False

def backup_mongodb(timestamp):
    """Ejecuta el volcado de la base de datos MongoDB usando mongodump."""
    print("⏳ Iniciando backup de MongoDB...")
    
    mongo_url = os.getenv("MONGO_URL")
    mongo_db = os.getenv("MONGO_DB")
    
    if not all([mongo_url, mongo_db]):
        print("❌ Error: Faltan variables de entorno para MongoDB (MONGO_URL, MONGO_DB).")
        return False
        
    filename = NOSQL_BACKUP_DIR / f"backup_{timestamp}.archive"
    
    command = [
        "mongodump",
        f"--uri={mongo_url}",
        f"--db={mongo_db}",
        f"--archive={filename}"
    ]
    
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        print(f"✅ Backup de MongoDB completado con éxito: {filename.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar mongodump: {e.stderr}")
        if filename.exists():
            filename.unlink()
        return False
    except FileNotFoundError:
        print("❌ Error: 'mongodump' no está instalado o no se encuentra en el PATH del sistema.")
        return False

def main():
    print("=========================================")
    print("🚀 Quantify Medical - Gestor de Backups 🚀")
    print("=========================================\n")
    
    if not setup_environment():
        return
        
    timestamp = get_timestamp()
    
    sql_success = backup_mysql(timestamp)
    print("-" * 40)
    nosql_success = backup_mongodb(timestamp)
    
    print("=========================================")
    if sql_success and nosql_success:
        print("🎉 ¡Todos los respaldos se han completado correctamente!")
    else:
        print("⚠️ Hubo errores durante el proceso de respaldo. Revisa los logs arriba.")
    print("=========================================")

if __name__ == "__main__":
    main()
