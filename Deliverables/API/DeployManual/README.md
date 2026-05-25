# Manual de Despliegue — Quantify Medical Hybrid API

> **Versión:** 2.0.0  
> **Stack:** FastAPI + MySQL (SQLAlchemy) + MongoDB (Motor)  
> **Puerto:** `8000` (desarrollo) | `443` (producción HTTPS)

---

## 1. Requisitos Previos

| Componente | Versión mínima | Instalación |
| :--- | :--- | :--- |
| Python | 3.11+ | [python.org](https://python.org) |
| MySQL | 8.0+ | [mysql.com](https://mysql.com) |
| MongoDB | 7.0+ | [mongodb.com](https://mongodb.com) |
| pip | 23+ | Incluido con Python |

---

## 2. Instalación — Entorno Local (Desarrollo)

### 2.1 Clonar y preparar entorno virtual

```bash
# Navegar al directorio de la API
cd Deliverables/API/source

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### 2.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2.3 Configurar variables de entorno

```bash
# Copiar template
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# Editar con tus credenciales
notepad .env              # Windows
nano .env                 # Linux/Mac
```

Variables clave a configurar:
```env
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=quantify_medical_db
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=clave_segura_minimo_32_caracteres
```

### 2.4 Inicializar base de datos MySQL

**Opción A — Script SQL directo:**
```bash
mysql -u root -p < init_db.sql
```

**Opción B — SQLAlchemy automático (solo desarrollo):**
```bash
python -c "from database import create_tables; create_tables()"
```

### 2.5 Poblar datos de prueba

```bash
python seed_db.py
```

### 2.6 Iniciar servidor de desarrollo

```bash
python main.py
# o con uvicorn:
uvicorn main:app --reload --port 8000
```

**API disponible en:** `http://localhost:8000`  
**Swagger UI:** `http://localhost:8000/api/v1/docs`  
**ReDoc:** `http://localhost:8000/api/v1/redoc`

---

## 3. Endpoints Principales

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

## 4. Producción (Guía Rápida)

```bash
# Instalar con Gunicorn
pip install gunicorn

# Configurar .env con DEBUG=False y APP_ENV=production

# Iniciar con múltiples workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 --access-logfile - --error-logfile -
```

**Lista de producción:**
- [ ] `DEBUG=False` en `.env`
- [ ] `SECRET_KEY` con mínimo 64 caracteres aleatorios
- [ ] HTTPS configurado (Nginx + Let's Encrypt)
- [ ] Rate limiting habilitado
- [ ] Backups MySQL automáticos (cron daily)
- [ ] Índices MongoDB verificados

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Completado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En Revision |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |
