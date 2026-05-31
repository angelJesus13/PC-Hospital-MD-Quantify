import os
import random
import mysql.connector # type: ignore
from mysql.connector import Error
from faker import Faker
from dotenv import load_dotenv

import sys
sys.path.append(os.getcwd())
from config.db_mysql import init_mysql_tables

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "795130")
MYSQL_DB = os.getenv("MYSQL_DB", "hospital_hibrido_md")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

def arrancar_insercion_masiva():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST, port=int(MYSQL_PORT),
            user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB
        )
        cursor = conn.cursor()
        
        print("====== PURGANDO TABLAS Y RECONSTRUYENDO RELACIONES ======")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("DROP TABLE IF EXISTS tbi_bitacora;")
        cursor.execute("DROP TABLE IF EXISTS tbb_md_notas_medicas;")
        cursor.execute("DROP TABLE IF EXISTS tbb_md_expedientes_medicos;")
        cursor.execute("DROP TABLE IF EXISTS tbb_md_pacientes;")
        cursor.execute("DROP TABLE IF EXISTS tbb_hr_personal_medico;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("[OK] Tablas desintegradas limpiamente.")
        
        # Obligar la reconstrucción perfecta del SQL
        init_mysql_tables()

        fake = Faker('es_MX')
        
        print("\n====== INSERTANDO 50 MÉDICOS ======")
        medicos = []
        turnos = ['MATUTINO', 'VESPERTINO', 'NOCTURNO A', 'NOCTURNO B', 'JORNADA ACUMULADA']
        especialidades_reales = ['Medicina General', 'Urgenciología', 'Cardiología', 'Cirugía General', 'Pediatría', 'Neurología', 'Traumatología', 'Ginecología', 'Anestesiología', 'Oncología']
        for _ in range(50):
            turno = random.choice(turnos)
            area_id = random.randint(1, 499)
            cedula = str(random.randint(1000000, 9999999))
            especialidad = random.choice(especialidades_reales)
            medicos.append((turno, area_id, cedula, especialidad))
            
        cursor.executemany(
            "INSERT INTO tbb_hr_personal_medico (Turno, Area_ID, Cedula_Profesional, Especialidad) VALUES (%s, %s, %s, %s)", 
            medicos
        )
        print("[OK] 50 Médicos insertados en tbb_hr_personal_medico.")
        
        print("\n====== INSERTANDO 150 PACIENTES ======")
        pacientes = []
        vidas = ['Vivo', 'Coma', 'Vegetativo', 'Desconocido'] # NUNCA FINADO, porque se les van a crear notas en el futuro
        estados_clinicos = ['Paciente estable y consciente', 'Pronóstico reservado', 'Bajo observación', 'Recuperación favorable', 'En valoración diagnóstica']
        for _ in range(150):
            status_vida = random.choice(vidas)
            status_medico = random.choice(estados_clinicos)
            fecha_ultima = fake.date_time_between(start_date='-2y', end_date='now') # Fecha real pasada
            pacientes.append((status_medico, status_vida, fecha_ultima))
            
        cursor.executemany(
            "INSERT INTO tbb_md_pacientes (status_medico, status_vida, fecha_ultima_citamedica) VALUES (%s, %s, %s)", 
            pacientes
        )
        print("[OK] 150 Pacientes insertados en tbb_md_pacientes.")
        
        print("\n====== INSERTANDO 150 EXPEDIENTES (1 a 1) ======")
        expedientes = []
        historiales_reales = ['Sin antecedentes patológicos de importancia.', 'Antecedentes heredofamiliares de DM2.', 'Hipertensión arterial bajo tratamiento.', 'Cirugía previa hace 2 años.', 'Alergias negadas. Sedentarismo.']
        evaluaciones_reales = ['Paciente ingresa refiriendo dolor moderado.', 'Exploración física dentro de parámetros normales.', 'Se observa inflamación y signos de infección local.', 'FC y TA ligeramente elevados por estrés agudo.']
        for i in range(1, 151):
            num_exp = f"EXP-2026-{fake.random_int(min=1000, max=9999)}-{i}"
            paciente_id = i
            med_apt = random.randint(1, 50)
            seguro_fk = random.randint(1, 499)
            historial = random.choice(historiales_reales)
            eval_ini = random.choice(evaluaciones_reales)
            poliza = f"{random.choice(['GNP', 'IMSS', 'AXA', 'MetLife', 'GNP'])} - POL-{random.randint(10000, 99999)}"
            alertas = random.choice(['Alergia a Penicilina', 'Alergia a AINEs', 'Portador de Marcapasos', 'Hipertensión Severa', 'Ninguna'])
            expedientes.append((num_exp, paciente_id, med_apt, seguro_fk, historial, eval_ini, poliza, alertas))
            
        cursor.executemany(
            "INSERT INTO tbb_md_expedientes_medicos (numero_expediente, Paciente_ID, Medico_ID_Apertura, Seguro_Proveedor_ID, antecedentes_historial_clinico, evaluacion_inicial_ingreso, detalles_seguro_poliza, alertas_medicas_criticas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
            expedientes
        )
        print("[OK] 150 Expedientes clínicos fusionados insertados en tbb_md_expedientes_medicos.")
        
        # Insertando procedimiento SP si no estaba para asegurar integridad
        with open("tests/sql/config/sp_poblar_notas_dinamico.sql", "r", encoding="utf-8") as f:
            sql_sp = f.read().replace("DELIMITER $$", "").replace("DELIMITER ;", "").replace("$$", "").strip()
        cursor.execute("DROP PROCEDURE IF EXISTS sp_poblar_notas_dinamico")
        cursor.execute(sql_sp)

        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n=============================================================")
        print("¡ÉXITO TOTAL! EL ECOSISTEMA MYSQL ESTÁ 100% PREPARADO PARA LAS 500K NOTAS.")
        print("=============================================================\n")
        
    except Error as e:
        print(f"ERROR FATAL DE INSERCIÓN: {e}")

if __name__ == "__main__":
    arrancar_insercion_masiva()
