import os
from dotenv import load_dotenv
import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore
from faker import Faker
import random

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "hospital_hibrido_md")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=int(MYSQL_PORT),
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise e

def test_mysql_connection():
    try:
        connection = get_db_connection()
        if connection.is_connected():
            print("====================================")
            print("Console.log: Conexión exitosa a MySQL verificada.")
            print("====================================")
            connection.close()
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")

def init_mysql_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS tbb_md_pacientes (
            ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            status_medico VARCHAR(150) NULL,
            status_vida ENUM('Vivo', 'Finado', 'Coma', 'Vegetativo', 'Desconocido') NOT NULL DEFAULT 'Desconocido',
            fecha_ultima_citamedica DATETIME NULL,
            fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion DATETIME NULL,
            estatus BIT(1) NOT NULL DEFAULT b'1'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tbb_hr_personal_medico (
            ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            Turno ENUM('MATUTINO', 'VESPERTINO', 'NOCTURNO A', 'NOCTURNO B', 'JORNADA ACUMULADA') NULL,
            Area_ID INT UNSIGNED NOT NULL,
            Fecha_Registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            Fecha_Actualizacion DATETIME NULL,
            Estatus BIT(1) NOT NULL DEFAULT b'1',
            Cedula_Profesional VARCHAR(30) NOT NULL UNIQUE,
            Especialidad VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tbb_md_expedientes_medicos (
            ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            numero_expediente VARCHAR(50) NOT NULL UNIQUE,
            Paciente_ID INT UNSIGNED NOT NULL UNIQUE,
            Medico_ID_Apertura INT UNSIGNED NOT NULL,
            Seguro_Proveedor_ID INT UNSIGNED NULL COMMENT 'FK hacia tbb_proveedores (< 500 simulado)',
            
            fecha_apertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            estatus_expediente ENUM('Activo', 'Inactivo', 'Archivo Muerto', 'Retenido Legalmente') DEFAULT 'Activo',
            nivel_confidencialidad ENUM('Normal', 'Restringido', 'Estricto') DEFAULT 'Normal',
            
            antecedentes_historial_clinico TEXT COMMENT 'Fusión de HeredoFamiliares, Patológicos y No Patológicos',
            evaluacion_inicial_ingreso TEXT COMMENT 'Fusión de padecimiento actual y exploración inicial',
            
            tiene_consentimiento_informado BIT(1) NOT NULL DEFAULT b'0',
            detalles_seguro_poliza VARCHAR(200) COMMENT 'Fusión de Folio, Aseguradora y Tipo de Seguro',
            alertas_medicas_criticas VARCHAR(255),
            
            FOREIGN KEY (Paciente_ID) REFERENCES tbb_md_pacientes(ID) ON DELETE RESTRICT,
            FOREIGN KEY (Medico_ID_Apertura) REFERENCES tbb_hr_personal_medico(ID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tbb_md_notas_medicas (
            ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            FechaRegistro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            Estatus BIT(1) NOT NULL DEFAULT b'1',
            TipoNota VARCHAR(50) NOT NULL,
            AntecedentesRelevantes TEXT,
            SintomasActuales TEXT NOT NULL,
            InterrogatorioAnamnesis TEXT NOT NULL,
            SignosVitales ENUM(
                'FC:80 lpm, FR:16 rpm, TA:120/80 mmHg, Temp:36.5°C, SpO2:98%',
                'FC:110 lpm, FR:24 rpm, TA:140/90 mmHg, Temp:38.5°C, SpO2:92%',
                'FC:60 lpm, FR:14 rpm, TA:100/60 mmHg, Temp:36.0°C, SpO2:95%',
                'FC:130 lpm, FR:28 rpm, TA:160/100 mmHg, Temp:39.0°C, SpO2:88%',
                'FC:95 lpm, FR:20 rpm, TA:130/85 mmHg, Temp:37.2°C, SpO2:96%',
                'No recabados'
            ) NOT NULL DEFAULT 'No recabados',
            Auditoria VARCHAR(255) NOT NULL DEFAULT 'Sistema',
            Paciente_ID INT UNSIGNED NOT NULL,
            Medico_ID INT UNSIGNED NOT NULL,
            Expediente_ID INT UNSIGNED NOT NULL,
            FOREIGN KEY (Paciente_ID) REFERENCES tbb_md_pacientes(ID),
            FOREIGN KEY (Medico_ID) REFERENCES tbb_hr_personal_medico(ID),
            FOREIGN KEY (Expediente_ID) REFERENCES tbb_md_expedientes_medicos(ID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tbi_bitacora (
            ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(100) NOT NULL,
            NombreTabla VARCHAR(100) NOT NULL,
            Operacion VARCHAR(50) NOT NULL,
            Descripcion TEXT,
            fechaHora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            for query in queries:
                cursor.execute(query)
            connection.commit()
            print("====================================")
            print("Console.log: Schema relacional fusionado sin EAV inyectado.")
            print("====================================")
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error al inicializar tablas en MySQL: {e}")

def seed_mysql_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(1) FROM tbb_hr_personal_medico;")
        if cursor.fetchone()[0] == 0:
            print("====================================")
            print("Sembrando 350 registros pivote con Metadatos Clínicos integrados...")
            fake = Faker('es_MX')
            
            medicos = []
            turnos = ['MATUTINO', 'VESPERTINO', 'NOCTURNO A', 'NOCTURNO B', 'JORNADA ACUMULADA']
            especialidades = ['Medicina General', 'Urgenciología', 'Cardiología', 'Cirugía General', 'Pediatría', 'Neurología', 'Traumatología', 'Ginecología', 'Anestesiología', 'Oncología']
            for _ in range(50):
                turno = random.choice(turnos)
                area_id = random.randint(1, 20)
                cedula = str(random.randint(1000000, 9999999))
                especialidad = random.choice(especialidades)
                medicos.append((turno, area_id, cedula, especialidad))
                
            cursor.executemany(
                "INSERT INTO tbb_hr_personal_medico (Turno, Area_ID, Cedula_Profesional, Especialidad) VALUES (%s, %s, %s, %s)", 
                medicos
            )
            
            pacientes = []
            vidas = ['Vivo', 'Coma', 'Vegetativo', 'Desconocido'] # SIN FINADO
            clinicos = ['Paciente estable y consciente', 'Pronóstico reservado', 'Bajo observación', 'Recuperación favorable', 'En valoración diagnóstica']
            for _ in range(150):
                status_vida = random.choice(vidas)
                status_medico = random.choice(clinicos)
                fecha_ult = fake.date_time_between(start_date='-2y', end_date='now')
                pacientes.append((status_medico, status_vida, fecha_ult))
                
            cursor.executemany(
                "INSERT INTO tbb_md_pacientes (status_medico, status_vida, fecha_ultima_citamedica) VALUES (%s, %s, %s)", 
                pacientes
            )
            
            expedientes = []
            historiales = ['Sin antecedentes patológicos de importancia.', 'Antecedentes heredofamiliares de DM2.', 'Hipertensión arterial bajo tratamiento.', 'Cirugía previa hace 2 años.', 'Alergias negadas. Sedentarismo.']
            evaluaciones = ['Paciente ingresa refiriendo dolor moderado.', 'Exploración física dentro de parámetros normales.', 'Se observa inflamación y signos de infección local.', 'FC y TA ligeramente elevados por estrés agudo.']
            for i in range(1, 151):
                num_exp = f"EXP-2026-{fake.random_int(min=1000, max=9999)}-{i}"
                med_apt = random.randint(1, 50)
                historial = random.choice(historiales)
                eval_ini = random.choice(evaluaciones)
                poliza = f"{random.choice(['GNP', 'IMSS', 'AXA', 'MetLife'])} - POL-{random.randint(10000, 99999)}"
                alertas = random.choice(['Alergia a Penicilina', 'Alergia a AINEs', 'Portador de Marcapasos', 'Hipertensión Severa', 'Ninguna'])
                expedientes.append((num_exp, i, med_apt, historial, eval_ini, poliza, alertas))
                
            cursor.executemany(
                "INSERT INTO tbb_md_expedientes_medicos (numero_expediente, Paciente_ID, Medico_ID_Apertura, antecedentes_historial_clinico, evaluacion_inicial_ingreso, detalles_seguro_poliza, alertas_medicas_criticas) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                expedientes
            )
            
            # Autodespliega el SP híbrido 
            with open("tests/sql/config/sp_poblar_notas_dinamico.sql", "r", encoding="utf-8") as f:
                sql_sp = f.read().replace("DELIMITER $$", "").replace("DELIMITER ;", "").replace("$$", "").strip()
            cursor.execute("DROP PROCEDURE IF EXISTS sp_poblar_notas_dinamico")
            cursor.execute(sql_sp)
            
            conn.commit()
            print("Seed completado: 50 Médicos, 150 Pacientes, 150 Expedientes Fusionados Verticalmente.")
            print("====================================")
            
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error sembrando BD principal: {e}")
