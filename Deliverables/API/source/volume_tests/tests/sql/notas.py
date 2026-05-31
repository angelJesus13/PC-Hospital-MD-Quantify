from fastapi import APIRouter, HTTPException, Request # type: ignore
from pydantic import BaseModel, conlist # type: ignore
import mysql.connector # type: ignore
import os
from typing import List, Optional

router = APIRouter(prefix="/api/sql", tags=["SQL Pruebas de Volumen (Parametrizadas)"])

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "hospital_hibrido_md")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=int(MYSQL_PORT),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

class ParametrosPrueba(BaseModel):
    cantidad: int
    tipos_nota: conlist(str, min_length=1) # type: ignore # Ej: ["Ingreso", "Evolución"]
    incluir_pediatria: bool = False
    incluir_uci: bool = False
    incluir_paciente_zero: bool = False
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cantidad": 80000,
                    "tipos_nota": ["Ingreso", "Evolución"],
                    "incluir_pediatria": False,
                    "incluir_uci": False,
                    "incluir_paciente_zero": False
                }
            ]
        }
    }


@router.post("/poblar-notas")
def poblar_notas_param(params: ParametrosPrueba, request: Request):
    """
    Endpoint masivo alimentado por JSON. 
    Permite configurar dinámicamente el comportamiento de la prueba en MySQL.
    """
    if params.cantidad <= 0:
        return {"error": "La cantidad debe ser mayor a 0"}
        
    try:
        ip_cliente = request.client.host if request.client else "IP_Desconocida"
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Parse arguments para MySQL
        tipos_csv = ",".join(params.tipos_nota)
        
        # Ejecutamos el Store Procedure Parametrizado
        cursor.execute(
            f"CALL sp_poblar_notas_dinamico({params.cantidad}, '{tipos_csv}', "
            f"{int(params.incluir_pediatria)}, {int(params.incluir_uci)}, "
            f"{int(params.incluir_paciente_zero)}, '{ip_cliente}');"
        )
        
        for _ in cursor.stored_results():
            _.fetchall()
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "mensaje": f"¡Éxito! Tu IP ({ip_cliente}) inyectó un total de {params.cantidad} registros médicos (SQL).",
            "parametros_usados": params.model_dump(),
            "registros_creados": params.cantidad
        }
    except Exception as e:
        return {"error": f"Ocurrió un error general en SQL: {str(e)}"}

@router.delete("/borrar-notas")
def borrar_todas_notas(request: Request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        ip_cliente = request.client.host if request.client else "IP_Desconocida"
        usuario_bitacora = f"Usuario_IP_{ip_cliente}"
        
        cursor.execute("SELECT COUNT(1) FROM tbb_md_notas_medicas;")
        cantidad_previa = cursor.fetchone()[0]
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE tbb_md_notas_medicas;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        descripcion_log = f"Limpieza masiva: Se vaciaron {cantidad_previa} Notas Médicas."
        cursor.execute(
            "INSERT INTO tbi_bitacora (NombreTabla, Operacion, Descripcion, usuario) VALUES (%s, %s, %s, %s)",
            ("tbb_md_notas_medicas", "Delete", descripcion_log, usuario_bitacora)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "mensaje": f"Se eliminaron {cantidad_previa} registros de Notas Médicas. La IP {ip_cliente} fue guardada de testigo.",
            "registros_eliminados": cantidad_previa
        }
    except Exception as e:
        return {"error": f"Error limpiando notas SQL: {str(e)}"}

@router.delete("/borrar-bitacora")
def borrar_bitacora(request: Request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        ip_cliente = request.client.host if request.client else "IP_Desconocida"
        usuario_bitacora = f"Usuario_IP_{ip_cliente}"
        
        cursor.execute("SELECT COUNT(1) FROM tbi_bitacora;")
        cantidad_previa = cursor.fetchone()[0]
        
        cursor.execute("TRUNCATE TABLE tbi_bitacora;")
        
        descripcion_log = f"ALERTA: Purgado de Registros. Se borraron {cantidad_previa} registros previos en la Bitácora."
        cursor.execute(
            "INSERT INTO tbi_bitacora (NombreTabla, Operacion, Descripcion, usuario) VALUES (%s, %s, %s, %s)",
            ("tbi_bitacora", "Delete", descripcion_log, usuario_bitacora)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "mensaje": f"¡Éxito! Se purgó la Bitácora ({cantidad_previa} eventos viejos borrados)",
            "registros_eliminados": cantidad_previa
        }
    except Exception as e:
        return {"error": f"Error limpiando bitácora SQL: {str(e)}"}
