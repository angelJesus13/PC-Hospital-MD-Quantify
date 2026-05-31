import os
from dotenv import load_dotenv # type: ignore
from pymongo import MongoClient # type: ignore
from pymongo.errors import ConnectionFailure # type: ignore
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hospital_hibrido_md")

def test_mongo_connection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Ping para validar conexión
        client.admin.command('ping')
        
        print("====================================")
        print("Console.log: Conexión exitosa a MongoDB verificada.")
        print("====================================")
    except ConnectionFailure as e:
        print(f"Error de red MongoDB: {e}")
    except Exception as e:
        print(f"Error de credenciales/URI MongoDB: {e}")

def init_mongo_collections():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB_NAME]
        existing_collections = db.list_collection_names()
        required_collections = ["NotasMedicas", "Bitacora"]
        
        created = False
        for coll in required_collections:
            if coll not in existing_collections:
                db.create_collection(coll)
                created = True
        
        print("====================================")
        print("Console.log: Colecciones MongoDB verificadas e inicializadas.")
        print("====================================")
    except Exception as e:
        print(f"Error al inicializar colecciones en MongoDB: {e}")

def get_mongo_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[MONGO_DB_NAME]

def log_bitacora_mongo(nombre_tabla: str, usuario: str, operacion: str, descripcion: str):
    try:
        db = get_mongo_db()
        documento = {
            "Nombre_Tabla": nombre_tabla,
            "Usuario": usuario,
            "Operacion": operacion,
            "Descripcion": descripcion,
            "Fecha_Hora": datetime.utcnow()
        }
        db["Bitacora"].insert_one(documento)
    except Exception as e:
        print(f"Error al guardar en bitácora MongoDB: {e}")
