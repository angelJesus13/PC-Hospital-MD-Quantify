# Manual de Despliegue — API Híbrida Hospital MD (MySQL + MongoDB)

> **Versión:** 3.0.0  
> **Stack:** FastAPI + MySQL (mysql-connector-python) + MongoDB (PyMongo)  
> **Puerto:** `8000` (desarrollo) | `443` (producción HTTPS)  
> **Área:** Registros Médicos (MD) — PC-Hospital

---

## Tabla de Contenidos

1. [Requisitos Previos](#1-requisitos-previos)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Instalación — Entorno Local](#3-instalación--entorno-local-desarrollo)
4. [Configuración de Bases de Datos](#4-configuración-de-bases-de-datos)
5. [Despliegue de la API Principal (CRUD)](#5-despliegue-de-la-api-principal-crud)
6. [Despliegue de la API de Pruebas de Volumen](#6-despliegue-de-la-api-de-pruebas-de-volumen)
7. [Endpoints — API Principal](#7-endpoints--api-principal)
8. [Endpoints — Pruebas de Volumen SQL](#8-endpoints--pruebas-de-volumen-sql)
9. [Endpoints — Pruebas de Volumen NoSQL](#9-endpoints--pruebas-de-volumen-nosql)
10. [Las 5 Pruebas de Volumen SQL (523,346 registros)](#10-las-5-pruebas-de-volumen-sql-523346-registros)
11. [Las 5 Pruebas de Volumen NoSQL (283,462 registros)](#11-las-5-pruebas-de-volumen-nosql-283462-registros)
12. [Funciones y Procedimientos Almacenados SQL](#12-funciones-y-procedimientos-almacenados-sql)
13. [Scripts Python Equivalentes para MongoDB](#13-scripts-python-equivalentes-para-mongodb)
14. [Estructura de Documentos MongoDB](#14-estructura-de-documentos-mongodb)
15. [Producción](#15-producción-guía-rápida)
16. [Solución de Problemas](#16-solución-de-problemas)
17. [Equipo de Desarrollo](#17-equipo-de-desarrollo)

---

## 1. Requisitos Previos

| Componente | Versión mínima | Instalación |
| :--- | :--- | :--- |
| Python | 3.11+ | [python.org](https://python.org) |
| MySQL | 8.0+ | [mysql.com](https://mysql.com) |
| MongoDB | 7.0+ (o Atlas) | [mongodb.com](https://mongodb.com) |
| pip | 23+ | Incluido con Python |

> **Nota:** MongoDB puede ser una instancia local (`mongodb://localhost:27017`) o un cluster en Atlas (`mongodb+srv://...`). Ambos son soportados.

---

## 2. Arquitectura del Sistema

El proyecto contiene **dos APIs independientes** bajo `Deliverables/API/source/`:

```
Deliverables/API/source/
│
├── (API Principal - CRUD Operativo)
│   ├── main.py              ← FastAPI + SQLAlchemy + Motor (async)
│   ├── models.py            ← 12 tablas ORM
│   ├── schemas.py           ← Validación Pydantic v2
│   ├── routes/              ← Endpoints CRUD por entidad
│   ├── auth.py              ← JWT con roles
│   └── ...
│
└── volume_tests/            ← API de Pruebas de Volumen
    ├── main.py              ← FastAPI (población masiva)
    ├── config/
    │   ├── db_mysql.py      ← Conexión MySQL + DDL + Seeds
    │   └── db_mongo.py      ← Conexión MongoDB + Colecciones
    ├── tests/
    │   ├── sql/
    │   │   ├── notas.py     ← Router /api/sql (3 endpoints)
    │   │   └── config/      ← 1 SP + 6 funciones .sql
    │   └── nosql/
    │       ├── notas.py     ← Router /api/nosql (3 endpoints)
    │       ├── clinical_simulator.py
    │       └── config/      ← 7 scripts Python equivalentes
    ├── insertar_catalogos.py
    └── restaurar_funciones.py
```

### Diferencias entre las dos APIs

| Aspecto | API Principal | API Volume Tests |
| :--- | :--- | :--- |
| **Propósito** | CRUD operativo del hospital | Pruebas de volumen y estrés |
| **MySQL driver** | SQLAlchemy + PyMySQL (ORM) | mysql-connector-python (raw SQL) |
| **MongoDB driver** | Motor (async) | PyMongo (sync) |
| **Tablas SQL** | 12 tablas (`md_*`) | 5 tablas (`tbb_md_*`, `tbi_*`) |
| **Autenticación** | JWT con roles | Sin autenticación |
| **BD MySQL** | `quantify_medical_db` | `hospital_hibrido_md` |

> ⚠️ **IMPORTANTE:** Ambas APIs operan sobre bases de datos independientes. No comparten esquemas ni datos.

---

## 3. Instalación — Entorno Local (Desarrollo)

### 3.1 Clonar el repositorio

```bash
git clone https://github.com/angelJesus13/PC-Hospital-MD-Quantify.git
cd PC-Hospital-MD-Quantify
```

### 3.2 Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### 3.3 Instalar dependencias — API Principal

```bash
cd Deliverables/API/source
pip install -r requirements.txt
```

### 3.4 Instalar dependencias — API de Pruebas de Volumen

```bash
cd Deliverables/API/source/volume_tests
pip install -r requirements.txt
```

**Dependencias de volume_tests:**
```
fastapi==0.110.0
uvicorn==0.27.1
mysql-connector-python==8.3.0
pymongo==4.6.2
python-dotenv==1.0.1
pydantic==2.6.3
faker==24.4.0
```

---

## 4. Configuración de Bases de Datos

### 4.1 API Principal — `.env`

Crear el archivo `.env` en `Deliverables/API/source/`:

```bash
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

Editar con tus credenciales:
```ini
# ---- Base de Datos MySQL (SQL) ----
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=quantify_medical_db

# ---- Base de Datos MongoDB (NoSQL) ----
MONGO_URL=mongodb://localhost:27017
MONGO_DB=quantify_nosql

# ---- Seguridad JWT ----
SECRET_KEY=clave_segura_minimo_32_caracteres
```

### 4.2 API de Pruebas de Volumen — `.env`

Crear el archivo `.env` en `Deliverables/API/source/volume_tests/`:

```ini
# ====== MySQL Configuracion ======
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password_mysql
MYSQL_DB=hospital_hibrido_md

# ====== MongoDB Configuracion ======
MONGO_URI=mongodb+srv://TuUsuario:TuPass@cluster0.xxxxx.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=hospital_hibrido_md
```

> **Nota sobre MongoDB Atlas:** Si usas Atlas, la URI debe ser formato `mongodb+srv://`. Si usas MongoDB local, usa `mongodb://localhost:27017/`.

### 4.3 Crear la base de datos MySQL para Volume Tests

Antes de arrancar la API de pruebas, crea la base de datos en MySQL:

```sql
CREATE DATABASE IF NOT EXISTS hospital_hibrido_md;
```

O desde terminal:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hospital_hibrido_md;"
```

---

## 5. Despliegue de la API Principal (CRUD)

### 5.1 Inicializar base de datos MySQL

**Opción A — Script SQL directo:**
```bash
cd Deliverables/API/source
mysql -u root -p < init_db.sql
```

**Opción B — SQLAlchemy automático:**
```bash
python -c "from database import create_tables; create_tables()"
```

### 5.2 Poblar datos de prueba

```bash
python seed_db.py
```

### 5.3 Iniciar servidor

```bash
cd Deliverables/API/source
python main.py
# o con uvicorn:
uvicorn main:app --reload --port 8000
```

**API disponible en:** `http://localhost:8000`  
**Swagger UI:** `http://localhost:8000/api/v1/docs`  
**ReDoc:** `http://localhost:8000/api/v1/redoc`

---

## 6. Despliegue de la API de Pruebas de Volumen

> ⚠️ **IMPORTANTE:** Si la API Principal ya está corriendo en el puerto 8000, detenla antes o usa un puerto diferente (`--port 8001`).

### Paso 1 — Restaurar funciones SQL en MySQL

Este script lee los 5 archivos `.sql` de `tests/sql/config/` y los despliega como funciones en MySQL:

```bash
cd Deliverables/API/source/volume_tests
python restaurar_funciones.py
```

**Salida esperada:**
```
[OK] Función fn_generar_auditoria restaurada.
[OK] Función fn_generar_antecedentes restaurada.
[OK] Función fn_generar_sintomas restaurada.
[OK] Función fn_generar_interrogatorio restaurada.
[OK] Función fn_generar_signos_vitales restaurada.
Todas las funciones auxiliares se inyectaron exitosamente al servidor MySQL.
```

### Paso 2 — Insertar catálogos semilla (seeds)

Este script purga las tablas, recrea el esquema DDL, inserta 350 registros base y despliega el Stored Procedure:

```bash
python insertar_catalogos.py
```

**Salida esperada:**
```
====== PURGANDO TABLAS Y RECONSTRUYENDO RELACIONES ======
[OK] Tablas desintegradas limpiamente.
Console.log: Schema relacional fusionado sin EAV inyectado.

====== INSERTANDO 50 MÉDICOS ======
[OK] 50 Médicos insertados en tbb_hr_personal_medico.

====== INSERTANDO 150 PACIENTES ======
[OK] 150 Pacientes insertados en tbb_md_pacientes.

====== INSERTANDO 150 EXPEDIENTES (1 a 1) ======
[OK] 150 Expedientes clínicos fusionados insertados en tbb_md_expedientes_medicos.

¡ÉXITO TOTAL! EL ECOSISTEMA MYSQL ESTÁ 100% PREPARADO PARA LAS 500K NOTAS.
```

### Paso 3 — Iniciar el servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Salida esperada en consola:**
```
Iniciando API Híbrida...
====================================
Console.log: Conexión exitosa a MySQL verificada.
====================================
Console.log: Schema relacional fusionado sin EAV inyectado.
====================================
Console.log: Conexión exitosa a MongoDB verificada.
====================================
Console.log: Colecciones MongoDB verificadas e inicializadas.
====================================
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Paso 4 — Acceder al Swagger UI

Abrir en el navegador: 👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

Desde ahí se ejecutan todas las pruebas de volumen mediante los endpoints REST.

---

## 7. Endpoints — API Principal

| Método | Ruta | Rol requerido | Descripción |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Público | Autenticación JWT |
| `POST` | `/api/v1/auth/logout` | Cualquiera | Cierre de sesión |
| `GET` | `/api/v1/pacientes` | Cualquiera | Lista de pacientes |
| `POST` | `/api/v1/pacientes` | Cualquiera | Crear paciente |
| `GET` | `/api/v1/pacientes/{id}/expediente` | Cualquiera | Expediente completo |
| `POST` | `/api/v1/notas-medicas` | Médico/Admin | Crear nota clínica |
| `POST` | `/api/v1/signos-vitales` | Cualquiera | Registrar signos (auto MEWS) |
| `POST` | `/api/v1/diagnostico` | Médico/Admin | Crear diagnóstico CIE-10 |
| `POST` | `/api/v1/tratamientos` | Médico/Admin | Prescribir tratamiento |
| `POST` | `/api/v1/valoraciones` | Médico/Admin | Escala clínica Glasgow/MEWS |
| `GET` | `/api/v1/auditoria` | Admin | Logs de auditoría |
| `GET` | `/api/v1/telemetria/sesiones-activas` | Admin | Sesiones JWT activas |
| `GET` | `/health` | Público | Health check |

---

## 8. Endpoints — Pruebas de Volumen SQL

Base URL: `http://localhost:8000/api/sql`

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/sql/poblar-notas` | Población masiva parametrizada de notas médicas en MySQL |
| `DELETE` | `/api/sql/borrar-notas` | Vaciar todas las notas médicas (TRUNCATE) |
| `DELETE` | `/api/sql/borrar-bitacora` | Purgar la tabla de bitácora SQL |

### POST `/api/sql/poblar-notas` — Body JSON

```json
{
  "cantidad": 80000,
  "tipos_nota": ["Ingreso", "Evolución"],
  "incluir_pediatria": false,
  "incluir_uci": false,
  "incluir_paciente_zero": false
}
```

**Parámetros:**

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `cantidad` | `int` | Número de registros a generar (obligatorio, > 0) |
| `tipos_nota` | `list[str]` | Tipos de nota permitidos. Valores: `"Ingreso"`, `"Evolución"`, `"Urgencia"`, `"Interconsulta"`, `"Egreso"` |
| `incluir_pediatria` | `bool` | Si `true`, genera edades de 1–14 años en vez de 18–77 |
| `incluir_uci` | `bool` | Si `true`, fuerza signos vitales críticos (FC:130, SpO2:88%) |
| `incluir_paciente_zero` | `bool` | Si `true`, simula pacientes desconocidos (sin interrogatorio ni antecedentes) |

**Respuesta exitosa:**
```json
{
  "mensaje": "¡Éxito! Tu IP (127.0.0.1) inyectó un total de 80000 registros médicos (SQL).",
  "parametros_usados": {
    "cantidad": 80000,
    "tipos_nota": ["Ingreso", "Evolución"],
    "incluir_pediatria": false,
    "incluir_uci": false,
    "incluir_paciente_zero": false
  },
  "registros_creados": 80000
}
```

---

## 9. Endpoints — Pruebas de Volumen NoSQL

Base URL: `http://localhost:8000/api/nosql`

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/nosql/poblar-notas/` | Población masiva de documentos en MongoDB |
| `DELETE` | `/api/nosql/borrar-notas` | Vaciar la colección NotasMedicas |
| `DELETE` | `/api/nosql/borrar-bitacora` | Purgar la colección Bitacora |

### POST `/api/nosql/poblar-notas/` — Body JSON

```json
{
  "cantidad": 86512,
  "foco_clinico": ["Estable"]
}
```

**Parámetros:**

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `cantidad` | `int` | Número de documentos a generar (obligatorio, > 0) |
| `foco_clinico` | `list[str]` | Focos clínicos permitidos. Valores: `"Estable"`, `"Trauma"`, `"Paro"`, `"Hipertensiva"`, `"Infeccioso"`, `"Pediátrica"` |

**Respuesta exitosa:**
```json
{
  "mensaje": "¡Éxito! Tu IP (127.0.0.1) inyectó un total de 86512 registros médicos aleatorios.",
  "registros_creados": 86512
}
```

> **Nota técnica:** Los documentos NoSQL contienen **subdocumentos anidados** (SignosVitales como dict, Auditoría como dict) a diferencia de SQL donde son strings planos. Además, las llaves foráneas (`Paciente_ID`, `Medico_ID`, `Expediente_ID`) se extraen dinámicamente de MySQL para mantener integridad referencial cruzada.

---

## 10. Las 5 Pruebas de Volumen SQL (523,346 registros)

Ejecutar desde Swagger UI (`/docs`) en el endpoint `POST /api/sql/poblar-notas`. Ingresar cada JSON en la caja de request body:

### Prueba 1: Ingreso y Evolución (Adultos Generales)
**Total: 80,000 registros** — Pacientes al flujo hospitalario común sin gravedad crítica.
```json
{
  "cantidad": 80000,
  "tipos_nota": ["Ingreso", "Evolución"],
  "incluir_pediatria": false,
  "incluir_uci": false,
  "incluir_paciente_zero": false
}
```

### Prueba 2: Urgencias (Trauma y Choque)
**Total: 120,000 registros** — Alto volumen de triaje. `paciente_zero` fuerza identidades anónimas.
```json
{
  "cantidad": 120000,
  "tipos_nota": ["Urgencia"],
  "incluir_pediatria": false,
  "incluir_uci": false,
  "incluir_paciente_zero": true
}
```

### Prueba 3: Interconsultas de Especialistas
**Total: 43,346 registros** — Tráfico lateral de diagnósticos especializados.
```json
{
  "cantidad": 43346,
  "tipos_nota": ["Interconsulta"],
  "incluir_pediatria": false,
  "incluir_uci": false,
  "incluir_paciente_zero": false
}
```

### Prueba 4: Egreso y Seguimiento Postoperatorio
**Total: 50,000 registros** — Altas médicas con anomalías programadas.
```json
{
  "cantidad": 50000,
  "tipos_nota": ["Egreso", "Evolución"],
  "incluir_pediatria": false,
  "incluir_uci": false,
  "incluir_paciente_zero": false
}
```

### Prueba 5: Casos Especiales y Límite Clínico
**Total: 230,000 registros** — Prueba de estrés máxima. UCI + Pediatría + Urgencias simultáneas.
```json
{
  "cantidad": 230000,
  "tipos_nota": ["Ingreso", "Evolución", "Urgencia", "Egreso", "Interconsulta"],
  "incluir_pediatria": true,
  "incluir_uci": true,
  "incluir_paciente_zero": true
}
```

> **NOTA:** Cada prueba ejecutada genera **1 sola inserción auditora** en la tabla `tbi_bitacora` con el resumen del test.

---

## 11. Las 5 Pruebas de Volumen NoSQL (283,462 registros)

Ejecutar desde Swagger UI (`/docs`) en el endpoint `POST /api/nosql/poblar-notas/`:

### Prueba 1: Carga Base Estacionaria (Consulta Externa)
**Total: 86,512 registros** — Pacientes estables, evolución rutinaria.
```json
{
  "cantidad": 86512,
  "foco_clinico": ["Estable"]
}
```

### Prueba 2: Sobrecarga Infecciosa Cíclica
**Total: 63,141 registros** — Cuadros de fiebres, sepsias y afecciones respiratorias.
```json
{
  "cantidad": 63141,
  "foco_clinico": ["Infeccioso"]
}
```

### Prueba 3: Politraumatismos Médicos
**Total: 58,493 registros** — Choques hipovolémicos, traumatismos craneoencefálicos.
```json
{
  "cantidad": 58493,
  "foco_clinico": ["Trauma"]
}
```

### Prueba 4: Ala Pediátrica y Neonatología UCIN
**Total: 44,115 registros** — Saturación en recién nacidos, cálculo automático de Apgar.
```json
{
  "cantidad": 44115,
  "foco_clinico": ["Pediátrica"]
}
```

### Prueba 5: Pacientes Críticos Absolutos
**Total: 31,201 registros** — Estrés NoSQL máximo. Paros cardiorrespiratorios y crisis letales.
```json
{
  "cantidad": 31201,
  "foco_clinico": ["Paro", "Hipertensiva"]
}
```

---

## 12. Funciones y Procedimientos Almacenados SQL

Ubicados en `Deliverables/API/source/volume_tests/tests/sql/config/` y referenciados en `DataBases/SQL/`.

### Stored Procedure

| Nombre | Archivo | Descripción |
| :--- | :--- | :--- |
| `sp_poblar_notas_dinamico` | `sp_poblar_notas_dinamico.sql` | Orquestador principal. Recibe cantidad, tipos_nota (CSV), flags de pediatría/UCI/zero, e IP del usuario. Itera N veces, llama las 6 funciones, inserta en `tbb_md_notas_medicas`, commit cada 5000, registra en bitácora |

### Funciones Auxiliares

| Nombre | Archivo | Parámetros | Descripción |
| :--- | :--- | :--- | :--- |
| `fn_generar_antecedentes` | `fn_generar_antecedentes.sql` | `(p_es_paciente_zero BOOLEAN)` | Genera antecedentes clínicos: crónicos (8 variantes), alergias (5), cirugías previas (5). NULL si paciente_zero. 40% sin antecedentes |
| `fn_generar_auditoria` | `fn_generar_auditoria.sql` | `(p_usuario_ip VARCHAR)` | Genera estatus de auditoría MECIC/NOM-004. Distribución: 50% Pendiente, 20% Aprobado, 15% Obs. Menor, 10% Obs. Mayor, 3% No Cumple, 2% Crítico |
| `fn_generar_interrogatorio` | `fn_generar_interrogatorio.sql` | `(p_es_paciente_zero, p_genero, p_edad)` | Genera anamnesis con género, edad, tiempo de evolución (6 variantes) y estado clínico (5 variantes). Texto emergente para paciente_zero |
| `fn_generar_signos_vitales` | `fn_generar_signos_vitales.sql` | `(p_es_paciente_zero, p_escenario)` | Retorna ENUM de signos vitales según escenario: `general` (3 perfiles), `urgencia` (FC:110, SpO2:92%), `critico/uci` (FC:130, SpO2:88%), `zero` → "No recabados" |
| `fn_generar_sintomas` | `fn_generar_sintomas.sql` | `(p_es_paciente_zero BOOLEAN)` | 15 variantes de síntomas clínicos + intensidad EVA (1–10) + evolución temporal (8 periodos). Texto de trauma con Glasgow < 8 para paciente_zero |
| `fn_generar_tipo_nota` | `fn_generar_tipo_nota.sql` | *(ninguno)* | Distribución ponderada: 10% Ingreso, 35% Evolución, 20% Urgencia, 15% Interconsulta, 20% Egreso |

### Flujo de ejecución del SP

```
sp_poblar_notas_dinamico(cantidad, tipos_csv, pediatria, uci, zero, ip)
│
├── LOOP i = 0 → cantidad
│   ├── Tipo nota ← PARSE CSV aleatorio
│   ├── IDs FK ← RAND(1, 50/150)
│   ├── Edad ← pediatría ? [1-14] : [18-77]
│   ├── Género ← RAND(hombre/mujer)
│   │
│   ├── CALL fn_generar_antecedentes(zero)
│   ├── CALL fn_generar_sintomas(zero | uci)
│   ├── CALL fn_generar_signos_vitales(zero, escenario)
│   ├── CALL fn_generar_interrogatorio(zero, genero, edad)
│   ├── CALL fn_generar_auditoria(ip)
│   │
│   ├── INSERT INTO tbb_md_notas_medicas (...)
│   └── COMMIT cada 5000 registros
│
└── INSERT INTO tbi_bitacora (resumen del test)
```

---

## 13. Scripts Python Equivalentes para MongoDB

Ubicados en `Deliverables/API/source/volume_tests/tests/nosql/config/`. Cada script replica **exactamente** la lógica de su equivalente SQL pero adaptado para MongoDB:

| Script Python | Equivale a (SQL) | Diferencia NoSQL |
| :--- | :--- | :--- |
| `fn_generar_antecedentes.py` | `fn_generar_antecedentes.sql` | Misma lógica: None si zero, 40% sin datos, concat crónicos+alergias+cx |
| `fn_generar_auditoria.py` | `fn_generar_auditoria.sql` | Retorna **dict** (subdocumento) con firma digital, fechas, calificación, hallazgos |
| `fn_generar_interrogatorio.py` | `fn_generar_interrogatorio.sql` | Misma lógica: 6 tiempos, 5 estados, texto especial para zero |
| `fn_generar_signos_vitales.py` | `fn_generar_signos_vitales.sql` | Retorna **dict** con campos individuales (presion_arterial, fc, temp, sat, glucosa) en vez de string ENUM |
| `fn_generar_sintomas.py` | `fn_generar_sintomas.sql` | Misma lógica: 15 síntomas, EVA 1–10, 8 tiempos, Glasgow < 8 para zero |
| `fn_generar_tipo_nota.py` | `fn_generar_tipo_nota.sql` | Misma distribución: 10% Ingreso, 35% Evolución, 20% Urgencia, 15% Interconsulta, 20% Egreso |
| `sp_poblar_notas_dinamico.py` | `sp_poblar_notas_dinamico.sql` | Orquestador: genera N docs llamando las 6 funciones, `insert_many` en batch de 10k, registra en bitácora |

### Ejemplo de uso directo (sin API)

```python
from tests.nosql.config.fn_generar_antecedentes import fn_generar_antecedentes
from tests.nosql.config.fn_generar_signos_vitales import fn_generar_signos_vitales

# Generar antecedentes para paciente normal
print(fn_generar_antecedentes(False))
# → "Crónicos: HAS + DM2 de 10 años | Alergias: Alérgico a Penicilina | Cx previas: Colecistectomía"

# Generar signos vitales de urgencia
print(fn_generar_signos_vitales(False, "urgencia"))
# → {"presion_arterial": "140/90", "frecuencia_cardiaca": 110, ...}
```

---

## 14. Estructura de Documentos MongoDB

Cada documento insertado en la colección `NotasMedicas` tiene la siguiente estructura:

```json
{
  "_id": "ObjectId('...')",
  "FechaRegistro": "2026-05-30T12:00:00Z",
  "Estatus": 1,
  "TipoNota": "Urgencia",
  "AntecedentesRelevantes": "Crónicos: HAS controlada | Alergias: Sin alergias | Cx previas: Apendicectomía",
  "SintomasActuales": "Paciente ingresa en camilla rígida refiriendo dolor incontrolable...",
  "InterrogatorioAnamnesis": "Paciente hombre de 45 años. Inicia su padecimiento actual hace 3 días...",
  "ExploracionFisica": "EXPLORACIÓN CEFALOCAUDAL: Cráneo normocéfalo...",
  "SignosVitales": {
    "presion_arterial": "140/90",
    "frecuencia_cardiaca": 110,
    "frecuencia_respiratoria": 24,
    "temperatura_c": 38.5,
    "saturacion_o2": 92,
    "recabados": true,
    "nivel_gravedad": "Alterado"
  },
  "Auditoria": {
    "firma_digital_medico": "a3f8c2d1e5b9...",
    "fecha_emision": "2026-05-30T12:00:00Z",
    "estatus_auditoria": "Aprobado: Cumple con todos los dominios normativos...",
    "fecha_auditoria": "2026-05-31T06:00:00Z",
    "auditor_medico_id": "AUDITOR-456",
    "calificacion_calidad_100": 87
  },
  "Paciente_ID": 42,
  "Medico_ID": 15,
  "Expediente_ID": 42
}
```

### Colecciones MongoDB

| Colección | Descripción |
| :--- | :--- |
| `NotasMedicas` | Documentos de notas médicas con subdocumentos anidados |
| `Bitacora` | Registros de auditoría de operaciones (inserts, deletes) |

---

## 15. Producción (Guía Rápida)

```bash
# Instalar con Gunicorn
pip install gunicorn

# Iniciar con múltiples workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 --access-logfile - --error-logfile -
```

**Checklist de producción:**
- [ ] `DEBUG=False` en `.env`
- [ ] `SECRET_KEY` con mínimo 64 caracteres aleatorios
- [ ] HTTPS configurado (Nginx + Let's Encrypt)
- [ ] Rate limiting habilitado
- [ ] Backups MySQL automáticos (cron daily)
- [ ] Índices MongoDB verificados

---

## 16. Solución de Problemas

### Error: `Can't connect to MySQL server`
- Verificar que MySQL esté corriendo: `mysql -u root -p -e "SELECT 1;"`
- Verificar que el puerto en `.env` coincida con tu instalación (default: `3306`)
- Verificar que la base de datos `hospital_hibrido_md` exista

### Error: `ServerSelectionTimeoutError` (MongoDB)
- Si usas Atlas: verificar que tu IP esté en la whitelist del cluster
- Si usas local: verificar que `mongod` esté corriendo
- Verificar que la URI en `.env` sea correcta

### Error: `FUNCTION fn_generar_* does not exist`
- Ejecutar `python restaurar_funciones.py` antes de arrancar la API
- Verificar que los archivos `.sql` existen en `tests/sql/config/`

### Error: `PROCEDURE sp_poblar_notas_dinamico does not exist`
- Ejecutar `python insertar_catalogos.py` que despliega el SP automáticamente
- O ejecutar el SP manualmente desde el archivo `tests/sql/config/sp_poblar_notas_dinamico.sql`

### Error: `Foreign key constraint fails`
- Asegurar que `insertar_catalogos.py` fue ejecutado (crea 50 médicos, 150 pacientes, 150 expedientes)
- Los endpoints de borrar notas usan `SET FOREIGN_KEY_CHECKS = 0` para evitar este problema

### La API NoSQL marca `Error de Dependencia: Las tablas MySQL enlazadas están vacías`
- El endpoint NoSQL extrae IDs de pacientes/médicos/expedientes de MySQL
- Ejecutar `python insertar_catalogos.py` para poblar las tablas base

### Puerto 8000 ya en uso
- Buscar y matar el proceso: `netstat -ano | findstr :8000` → `taskkill /PID <PID> /F`
- O usar un puerto diferente: `uvicorn main:app --port 8001`

---

## 17. Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |
