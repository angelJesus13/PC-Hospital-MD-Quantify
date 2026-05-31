from fastapi import APIRouter, Request
from pydantic import BaseModel
from config.db_mongo import get_mongo_db, log_bitacora_mongo
from config.db_mysql import get_db_connection
from faker import Faker
import random
from tests.nosql.clinical_simulator import compilar_caso_clinico_maestro
from bson.objectid import ObjectId

router = APIRouter(prefix="/api/nosql", tags=["NoSQL Pruebas de Volumen"])

class PoblarNotasRequest(BaseModel):
    cantidad: int
    foco_clinico: list[str] = ["Estable", "Trauma", "Paro", "Hipertensiva", "Infeccioso", "Pediátrica"]

@router.post("/poblar-notas/")
def poblar_notas(payload: PoblarNotasRequest, request: Request):
    """
    Endpoint masivo. Inyecta la cantidad literal de notas ingresadas en la variable "cantidad" mediante un body JSON.
    """
    cantidad = payload.cantidad
    if cantidad <= 0:
        return {"error": "La cantidad debe ser mayor a 0"}
    
    # === Extracción de Llaves Foráneas de MySQL ===
    try:
        mysql_conn = get_db_connection()
        cursor = mysql_conn.cursor()
        
        cursor.execute("SELECT ID FROM tbb_md_pacientes")
        ids_pacientes = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT ID FROM tbb_hr_personal_medico")
        ids_medicos = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT ID FROM tbb_md_expedientes_medicos")
        ids_expedientes = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        mysql_conn.close()
        
        if not ids_pacientes or not ids_medicos or not ids_expedientes:
            return {"error": "Error de Dependencia: Las tablas MySQL enlazadas (Pacientes, Personal Médico o Expedientes) están vacías. Poblar MySQL primero."}
            
    except Exception as e:
        return {"error": f"Fallo al conectar con MySQL para validación de FKs: {str(e)}"}
    
    db = get_mongo_db()
    coleccion = db["NotasMedicas"]
    
    # Capturando la IP del compañero que lanzó la prueba
    ip_cliente = request.client.host if request.client else "IP_Desconocida"
    usuario_bitacora = f"Usuario_IP_{ip_cliente}"
    
    batch_size = 10000 
    insertados = 0
    notas_batch = []
    
    try:
        # Generamos en Batch mediante CCH Clínico Procedural
        for i in range(cantidad):
            notas_batch.append(compilar_caso_clinico_maestro(
                foco_clinico=payload.foco_clinico,
                ids_pacientes=ids_pacientes,
                ids_personal_medico=ids_medicos,
                ids_expedientes=ids_expedientes
            ))
            
            # Insertar en bloques de 10,000 o al final
            if len(notas_batch) == batch_size or i == (cantidad - 1):
                coleccion.insert_many(notas_batch)
                insertados += len(notas_batch)
                notas_batch = []
                
        # Registro en Bitácora (Solo Mongo)
        descripcion_log = f"Carga Masiva completada. Se inyectaron {insertados} registros."
        log_bitacora_mongo("NotasMedicas", usuario_bitacora, "Insert", descripcion_log)

        return {
            "mensaje": f"¡Éxito! Tu IP ({ip_cliente}) inyectó un total de {insertados} registros médicos aleatorios.",
            "registros_creados": insertados
        }
    except Exception as e:
        return {"error": f"Ocurrió un error general: {str(e)}"}

@router.delete("/borrar-notas")
def borrar_todas_notas(request: Request):
    """
    Endpoint para vaciar la población simulada de MongoDB.
    """
    db = get_mongo_db()
    coleccion = db["NotasMedicas"]
    
    # Contamos antes de borrar para registro exacto
    resultado = coleccion.delete_many({})
    
    # Capturando la IP del compañero que borró todo
    ip_cliente = request.client.host if request.client else "IP_Desconocida"
    usuario_bitacora = f"Usuario_IP_{ip_cliente}"
    
    descripcion_log = f"Limpieza masiva: Se vaciaron {resultado.deleted_count} Notas Médicas."
    
    # Registro en Bitácora Mongo
    log_bitacora_mongo("NotasMedicas", usuario_bitacora, "Delete", descripcion_log)
    
    return {
        "mensaje": f"Se eliminaron {resultado.deleted_count} documentos de Notas Médicas. La IP {ip_cliente} fue guardada de testigo.",
        "registros_eliminados": resultado.deleted_count
    }

@router.delete("/borrar-bitacora")
def borrar_bitacora(request: Request):
    """
    Endpoint masivo para purgar (vaciar) su tabla de Bitácora.
    """
    db = get_mongo_db()
    coleccion = db["Bitacora"]
    
    # Contamos y borramos absolutamente toda la historia previa
    resultado = coleccion.delete_many({})
    
    # Capturamos quién ordenó borrar la bitácora
    ip_cliente = request.client.host if request.client else "IP_Desconocida"
    usuario_bitacora = f"Usuario_IP_{ip_cliente}"
    
    descripcion_log = f"ALERTA: Purgado de Registros. Se borraron {resultado.deleted_count} registros previos en la Bitácora."
    
    # Como la bitácora quedó vacía, guardamos este evento como el ÚNICO registro nuevo inicial
    log_bitacora_mongo("Bitacora", usuario_bitacora, "Delete", descripcion_log)
    
    return {
        "mensaje": f"¡Éxito! Se purgó la Bitácora ({resultado.deleted_count} eventos viejos borrados) por instrucción de la IP: {ip_cliente}",
        "registros_eliminados": resultado.deleted_count
    }
