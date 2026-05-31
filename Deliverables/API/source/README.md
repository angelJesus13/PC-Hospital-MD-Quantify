# Quantify Medical Hybrid API

API REST híbrida (MySQL + MongoDB) para gestión de expedientes clínicos.

## Stack

- **Framework**: FastAPI + Uvicorn
- **SQL**: MySQL 8 + SQLAlchemy 2.0 + PyMySQL
- **NoSQL**: MongoDB + Motor (async driver)
- **Auth**: JWT + bcrypt

## Requisitos

- Python 3.14+
- MySQL 8 (XAMPP recomendado, puerto por defecto 3306)
- MongoDB (Community Server, puerto por defecto 27017)

## Instalación

```bash
cd Deliverables/API/source

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Copia `.env.example` a `.env` y ajusta las variables:

```env
DB_USER=root
DB_PASSWORD=tu_password        # Vacío si XAMPP default
DB_HOST=localhost
DB_PORT=3306                   # XAMPP: 3306, Workbench config: 3307
DB_NAME=quantify_medical_db

MONGO_URL=mongodb://localhost:27017
```

## Base de datos

### MySQL

Opción A — Crear desde MySQL Workbench:
```sql
CREATE DATABASE IF NOT EXISTS quantify_medical_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Opción B — El seed y la app la crean automáticamente si existe conexión.

### MongoDB

Debe estar corriendo en segundo plano (servicio `MongoDB` o `mongod.exe`).

## Poblar datos de prueba

```bash
cd Deliverables/API/source
$env:PYTHONIOENCODING='utf-8'
python seed_db.py
```

Crea: 4 usuarios, 5 pacientes, domicilios, notas, diagnósticos, tratamientos y valoraciones.

### Usuarios de prueba

| Username | Password | Rol |
|---|---|---|
| admin.quantify | Admin2026! | admin |
| dr.garcia | Medico2026! | medico |
| dra.lopez | Medico2026! | medico |
| enf.morales | Enfermero2026! | enfermero |

## Ejecutar servidor

```bash
cd Deliverables/API/source
uvicorn main:app --reload
```

Servidor en: **http://localhost:8000**

| URL | Descripción |
|---|---|
| http://localhost:8000/health | Health check |
| http://localhost:8000/api/v1/docs | Swagger UI |
| http://localhost:8000/api/v1/redoc | ReDoc |
| http://localhost:8000/api/v1/openapi.json | OpenAPI spec |

## Endpoints principales

Prefix: `/api/v1`

### Autenticación

| Método | Ruta | Descripción |
|---|---|---|
| POST | /auth/login | Login, retorna JWT |

### Usuarios (requiere admin)

| Método | Ruta | Descripción |
|---|---|---|
| GET | /usuarios | Listar usuarios |
| POST | /usuarios | Crear usuario |
| GET | /usuarios/me | Perfil actual |
| GET | /usuarios/{id} | Obtener usuario |
| PUT | /usuarios/{id} | Actualizar usuario |
| DELETE | /usuarios/{id} | Eliminar usuario |

### Pacientes

| Método | Ruta | Descripción |
|---|---|---|
| GET | /pacientes | Listar pacientes |
| POST | /pacientes | Crear paciente |
| GET | /pacientes/{id} | Obtener paciente |
| PUT | /pacientes/{id} | Actualizar paciente |
| GET | /pacientes/{id}/expediente | Expediente completo |
| GET | /pacientes/{id}/alertas-activas | Alertas del paciente |
| GET | /pacientes/{id}/tratamientos-activos | Tratamientos activos |

### Notas médicas

| Método | Ruta | Descripción |
|---|---|---|
| GET | /notas-medicas | Listar notas |
| POST | /notas-medicas | Crear nota |
| GET | /notas-medicas/{id} | Obtener nota |
| PUT | /notas-medicas/{id} | Actualizar nota |

### Signos vitales

| Método | Ruta | Descripción |
|---|---|---|
| GET | /signos-vitales | Listar signos |
| POST | /signos-vitales | Registrar signos |
| GET | /signos-vitales/{id} | Obtener registro |

### Diagnósticos

| Método | Ruta | Descripción |
|---|---|---|
| GET | /diagnostico | Listar diagnósticos |
| POST | /diagnostico | Crear diagnóstico |
| GET | /diagnostico/{id} | Obtener diagnóstico |
| PATCH | /diagnostico/{id}/desactivar | Desactivar diagnóstico |

### Tratamientos

| Método | Ruta | Descripción |
|---|---|---|
| GET | /tratamientos | Listar tratamientos |
| POST | /tratamientos | Crear tratamiento |
| GET | /tratamientos/{id} | Obtener tratamiento |
| PATCH | /tratamientos/{id}/suspender | Suspender tratamiento |

### Valoraciones

| Método | Ruta | Descripción |
|---|---|---|
| GET | /valoraciones | Listar valoraciones |
| POST | /valoraciones | Crear valoración |
| GET | /valoraciones/{id} | Obtener valoración |
| GET | /valoraciones/{id}/detalle | Detalle completo |

### Auditoría (MongoDB)

| Método | Ruta | Descripción |
|---|---|---|
| GET | /auditoria | Logs de auditoría |
| GET | /auditoria/emergencias | Eventos críticos |
| GET | /auditoria/estadisticas | Estadísticas |

### Telemetría (MongoDB)

| Método | Ruta | Descripción |
|---|---|---|
| GET | /telemetria/sesiones | Sesiones de usuario |
| GET | /telemetria/sesiones-activas | Sesiones activas |
| GET | /telemetria/uso-por-turno | Uso por turno |
| GET | /telemetria/endpoints-mas-usados | Top endpoints |

## Autenticación

Obtén un token JWT:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin.quantify", "password": "Admin2026!"}'
```

Úsalo en el header:

```bash
curl http://localhost:8000/api/v1/pacientes \
  -H "Authorization: Bearer <TOKEN>"
```

## Tests

```bash
cd Deliverables/API/source
pytest -v
```

159 tests que corren 100% con SQLite in-memory y MongoDB mockeado (sin necesidad de MySQL o MongoDB reales).

## Notas técnicas

- **Python 3.14 + bcrypt**: El módulo `auth.py` usa `bcrypt` directamente en vez de `passlib` (incompatible con Python 3.14).
- **MongoDB opcional en tests**: Los tests parchean MongoDB con `AsyncMock`.
- **Las tablas SQL se crean automáticamente** al iniciar la app en modo `development`.
