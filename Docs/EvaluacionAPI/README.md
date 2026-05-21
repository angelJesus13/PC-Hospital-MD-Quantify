# Evaluación de Calidad de la API — Intergrupal (Entre Pares)

> **Versión:** 1.0.0  
> **Proyecto Evaluador:** PC-Hospital-MD-Quantify  
> **API Evaluada:** [MEDICAL_REGISTER_API](https://github.com/AngelJdev/MEDICAL_REGISTER_API)  
> **Autor:** AngelJdev  
> **Metodología:** Peer Review Técnico — Evaluación Intergrupal  
> **Fecha:** 2026-05-21

---

## 1. Resumen Ejecutivo

| Categoría | Puntaje | Calificación |
| :--- | :---: | :---: |
| Estilo Arquitectónico REST | 22/25 | ⭐⭐⭐⭐ |
| Seguridad (JWT/Bcrypt) | 20/25 | ⭐⭐⭐⭐ |
| Integridad de Datos (ORM/Pydantic) | 22/25 | ⭐⭐⭐⭐ |
| Rendimiento y Escalabilidad | 16/25 | ⭐⭐⭐ |
| Mantenibilidad y Documentación | 18/25 | ⭐⭐⭐⭐ |
| **TOTAL** | **98/125** | **⭐⭐⭐⭐ (78.4%)** |

**Dictamen general:** La API `MEDICAL_REGISTER_API` presenta una arquitectura sólida y bien estructurada para un entorno clínico. Cumple con los estándares de seguridad fundamentales y tiene una buena separación de responsabilidades. Las oportunidades de mejora se concentran en el área de rendimiento bajo carga concurrente y la falta de tests automatizados formales.

---

## 2. Criterios de Evaluación

### Rúbrica general

| Nivel | Puntaje | Descripción |
| :--- | :---: | :--- |
| Excelente | 23–25 | Supera el estándar esperado para el nivel del proyecto |
| Bueno | 18–22 | Cumple el estándar con detalles menores por mejorar |
| Aceptable | 13–17 | Cumple lo mínimo pero requiere mejoras significativas |
| Deficiente | 0–12 | No cumple el estándar, requiere rediseño |

---

## 3. Evaluación Detallada por Categoría

### 3.1 Estilo Arquitectónico REST (22/25)

#### ✅ Fortalezas

**Estructura modular clara:**
El proyecto organiza el código en capas bien definidas:
```
MEDICAL_REGISTER_API/
├── config/          # Configuración de app
├── controllers/     # Lógica de negocio
├── middlewares/     # Guardianes de autenticación
├── models/          # Modelos ORM (SQLAlchemy)
├── routes/          # Definición de endpoints
├── utils/           # Funciones auxiliares
├── main.py          # Entry point FastAPI
├── database.py      # Gestión de sesión SQL
└── schemas.py       # Validación Pydantic
```

**Uso correcto de verbos HTTP:**
- `POST /pacientes` → Crear nuevo paciente (HTTP 201)
- `GET /pacientes/{id}` → Obtener paciente por ID (HTTP 200)
- `PUT /pacientes/{id}` → Actualizar paciente (HTTP 200)
- `DELETE /pacientes/{id}` → Eliminar (HTTP 204)

**Pydantic para validación de entrada:** La separación entre `models.py` (ORM) y `schemas.py` (Pydantic) es una práctica moderna correcta que evita exposición directa del modelo de base de datos.

#### ⚠️ Áreas de mejora

**Versionado de API ausente:**
```python
# Actual — sin versionado
app.include_router(pacientes_router, prefix="/pacientes")

# Recomendado
app.include_router(pacientes_router, prefix="/api/v1/pacientes")
```

**Códigos de respuesta inconsistentes:** En algunos endpoints se retorna HTTP 200 para creaciones en lugar de HTTP 201. Se recomienda estandarizar.

**Sin HATEOAS:** Las respuestas no incluyen links de navegación, lo que limita la auto-descriptividad de la API.

**Puntaje:** 22/25 — Buen cumplimiento. Falta versionado y algunos códigos de respuesta por estandarizar.

---

### 3.2 Seguridad (20/25)

#### ✅ Fortalezas

**JWT con algoritmo HS256:**
```python
# auth.py — Implementación detectada
SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**Bcrypt para hashing de contraseñas:** El uso de `bcrypt` con salt automático es la práctica correcta y resistente a ataques de diccionario y rainbow tables.

**Diferenciación de roles:** La API implementa roles `admin` y `medico` para controlar el acceso a rutas sensibles.

**Variables de entorno:** Credenciales externalizadas en `.env`:
```env
SECRET_KEY=tu_secreto_para_jwt
DB_PASSWORD=tu_password
```

#### ⚠️ Áreas de mejora

**Token Refresh ausente:** No existe endpoint `POST /auth/refresh`. Los tokens expiran sin posibilidad de renovación, forzando re-login frecuente en sesiones médicas largas (turnos de 12h).

**Sin rate limiting:** La API no implementa limitación de intentos de autenticación, haciéndola vulnerable a ataques de fuerza bruta en `/auth/login`.

```python
# Recomendado — agregar rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, form_data: LoginSchema):
    ...
```

**HTTPS no configurado:** No se detecta configuración de TLS/SSL en el servidor Uvicorn. En producción médica, HTTPS es obligatorio (HIPAA/LGPD).

**Sin blacklist de tokens:** Al cerrar sesión no se invalida el token JWT activo, lo que puede ser un riesgo si el token es interceptado antes de su expiración.

**Puntaje:** 20/25 — Seguridad básica bien implementada. Faltan rate limiting, token refresh y configuración HTTPS.

---

### 3.3 Integridad de Datos — ORM / Pydantic (22/25)

#### ✅ Fortalezas

**Modelo relacional robusto (11 tablas):**
El diagrama ERD muestra una arquitectura de datos coherente con el dominio clínico:
- Integridad referencial mediante FKs: `paciente_id → md_pacientes.id`
- Uso de ENUMs para campos con valores controlados: `tipo_nota`
- Timestamps de auditoría: `created_at` en entidades principales

**Pydantic con tipado estricto:**
```python
class PacienteCreate(BaseModel):
    nombre: str
    curp: str  # Debería validar formato CURP (18 chars, patrón regex)
    fecha_registro: datetime

class PacienteResponse(BaseModel):
    id: int
    nombre: str
    curp: str
    class Config:
        from_attributes = True  # orm_mode en Pydantic v1
```

**SQLAlchemy con relaciones declarativas:** Las relaciones `relationship()` permiten navegación entre entidades sin queries adicionales.

#### ⚠️ Áreas de mejora

**Validación de CURP sin regex:**
La CURP mexicana tiene un formato estrictamente definido (18 caracteres). Se recomienda:
```python
from pydantic import validator
import re

class PacienteCreate(BaseModel):
    curp: str

    @validator('curp')
    def validar_curp(cls, v):
        patron = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$'
        if not re.match(patron, v.upper()):
            raise ValueError('CURP inválida — debe tener formato oficial mexicano')
        return v.upper()
```

**Sin migraciones Alembic:** El uso de `Base.metadata.create_all()` no es adecuado para producción. Se necesita Alembic para migraciones versionadas.

**Sin índices explícitos en columnas de alta consulta:**
```python
# Recomendado
class MdPacientes(Base):
    curp = Column(String(18), unique=True, nullable=False, index=True)
    # También: índice compuesto para búsquedas frecuentes
```

**Puntaje:** 22/25 — Muy buena estructura. Mejorar con validaciones de dominio (CURP) y migraciones Alembic.

---

### 3.4 Rendimiento y Escalabilidad (16/25)

#### ✅ Fortalezas

**Uvicorn como servidor ASGI:** Elección correcta para FastAPI, soporta async/await nativamente.

**FastAPI con endpoints async:** La mayoría de los endpoints pueden aprovechar operaciones asíncronas.

#### ⚠️ Áreas de mejora (críticas)

**Sin connection pooling configurado:**
```python
# Detectado en database.py (estimado)
engine = create_engine(DATABASE_URL)

# Recomendado para entorno hospitalario
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

**Sin caché para datos frecuentes:** Consultas de catálogos (códigos CIE-10, medicamentos, escalas) se ejecutan en cada request. Se recomienda Redis o caché en memoria.

**N+1 query problem potencial:** Las relaciones ORM sin `joinedload()` pueden generar consultas N+1 al cargar expedientes completos:
```python
# Problemático — genera N queries adicionales
notas = db.query(MdNotasMedicas).filter_by(paciente_id=id).all()
# Para cada nota: accede a .diagnostico (query extra)

# Correcto
from sqlalchemy.orm import joinedload
notas = db.query(MdNotasMedicas)\
    .options(joinedload(MdNotasMedicas.diagnostico))\
    .filter_by(paciente_id=id).all()
```

**Sin paginación en endpoints de lista:** `GET /pacientes` sin límite puede retornar miles de registros.

**Sin tests de carga documentados:** No se encuentran benchmarks ni scripts de carga (`locust`, `k6`).

**Puntaje:** 16/25 — Rendimiento aceptable para prototipo. Requiere connection pooling, caché y paginación para producción.

---

### 3.5 Mantenibilidad y Documentación (18/25)

#### ✅ Fortalezas

**FastAPI auto-genera Swagger UI** en `/docs` y ReDoc en `/redoc`.

**README.md completo** con instrucciones de instalación, tecnologías y diagrama ERD en Mermaid.

**ERD en Mermaid inline:** La inclusión del diagrama directamente en el README es una práctica excelente para documentación viva.

**Estructura de carpetas descriptiva:** Los nombres de carpetas (`controllers`, `routes`, `models`) siguen convenciones bien reconocidas.

#### ⚠️ Áreas de mejora

**Sin comentarios en código fuente:** Los modelos ORM y controladores no tienen docstrings que expliquen la lógica de negocio clínica.

**Sin archivo CHANGELOG.md:** No hay registro de cambios entre versiones.

**Sin archivo CONTRIBUTING.md:** Falta guía para contribuidores externos.

**Tests unitarios limitados:** Se detecta `test_endpoints.py` pero no un suite completo con pytest + fixtures.

```python
# Recomendado — estructura de tests
tests/
├── conftest.py          # Fixtures globales (DB de prueba, tokens)
├── test_auth.py         # Tests de autenticación y roles
├── test_pacientes.py    # CRUD de pacientes
├── test_notas.py        # Notas médicas y diagnósticos
└── test_integridad.py   # Tests de rollback transaccional
```

**Puntaje:** 18/25 — Buena documentación técnica. Mejorar con tests formales y documentación de código.

---

## 4. Checklist de Cumplimiento

| Criterio | Estado | Observación |
| :--- | :---: | :--- |
| Endpoints REST con verbos HTTP correctos | ✅ | Correcto en la mayoría |
| Versionado de API (`/api/v1/`) | ❌ | No implementado |
| Autenticación JWT | ✅ | Implementado con HS256 |
| Hash de contraseñas con bcrypt | ✅ | Implementado |
| Diferenciación de roles | ✅ | `admin` y `medico` |
| Rate limiting en `/auth/login` | ❌ | Ausente |
| Token Refresh | ❌ | Ausente |
| Validación de CURP con regex | ⚠️ | Sin validación de formato |
| Migraciones con Alembic | ❌ | Usa `create_all()` directo |
| Connection pooling configurado | ⚠️ | Sin configuración explícita |
| Paginación en endpoints de lista | ❌ | Sin implementar |
| Tests unitarios con pytest | ⚠️ | Parcial (`test_endpoints.py`) |
| Caché para datos estáticos | ❌ | Sin implementar |
| HTTPS/TLS configurado | ❌ | Solo HTTP |
| Documentación Swagger/OpenAPI | ✅ | Auto-generada por FastAPI |
| ERD / Diagrama de datos | ✅ | Mermaid en README |
| Variables de entorno con `.env` | ✅ | Implementado |
| Seed de datos de prueba | ✅ | `seed_db.py` presente |

---

## 5. Recomendaciones Prioritarias

### 🔴 Alta Prioridad (Riesgo de Seguridad/Producción)

1. **Implementar rate limiting** en `POST /auth/login` — máximo 5 intentos/minuto por IP.
2. **Configurar HTTPS** — certificado SSL/TLS obligatorio para datos médicos.
3. **Agregar token blacklist** — Redis para invalidar tokens al hacer logout.
4. **Implementar migraciones Alembic** — control de versiones del schema SQL.

### 🟡 Media Prioridad (Rendimiento/Calidad)

5. **Configurar connection pooling** en SQLAlchemy con pool_size=20.
6. **Agregar paginación** en todos los endpoints de lista (`?pagina=1&limite=20`).
7. **Resolver N+1 queries** con `joinedload()` en relaciones frecuentes.
8. **Validar CURP** con regex oficial mexicano en Pydantic.

### 🟢 Baja Prioridad (Mantenibilidad)

9. **Implementar versionado de API** (`/api/v1/`).
10. **Ampliar suite de tests** con pytest, fixtures y cobertura > 80%.
11. **Agregar docstrings** en controladores y modelos.
12. **Crear CHANGELOG.md** para seguimiento de versiones.

---

## 6. Comparativa con Estándar FHIR (Referencia)

> HL7 FHIR es el estándar internacional para interoperabilidad de datos médicos.

| Aspecto FHIR | MEDICAL_REGISTER_API | Cubierto |
| :--- | :--- | :---: |
| Recurso `Patient` | `md_pacientes` | ✅ Parcial |
| Recurso `Observation` (signos vitales) | `md_signos_vitales` | ✅ Parcial |
| Recurso `DiagnosticReport` | `md_diagnostico` | ✅ Parcial |
| Recurso `MedicationRequest` | `md_tratamientos` | ✅ Parcial |
| Codificación CIE-10 | `codigo_cie` field | ✅ Presente |
| Formato FHIR JSON nativo | No implementado | ❌ |
| OAuth2 / SMART on FHIR | Solo JWT básico | ⚠️ Parcial |

---

## 7. Conclusión del Par Evaluador

La `MEDICAL_REGISTER_API` demuestra un diseño técnico competente para el nivel académico del proyecto. La separación de capas (routes → controllers → models), el uso de herramientas modernas (FastAPI, SQLAlchemy, Pydantic, JWT, Bcrypt) y la documentación básica del README muestran madurez en el desarrollo.

**Puntos diferenciadores positivos:**
- El diagrama ERD Mermaid directamente en el README es una práctica profesional destacable.
- La elección del stack tecnológico (FastAPI + SQLAlchemy + MySQL) es adecuada y moderna.
- El archivo `seed_db.py` facilita enormemente la reproducibilidad del entorno.

**Para alcanzar nivel producción hospitalaria**, el equipo debería enfocarse en: implementar HTTPS obligatorio, agregar rate limiting, usar Alembic para migraciones, y ampliar la cobertura de tests unitarios.

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Completado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | En revisión |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En revisión |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En revisión |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | En revisión |
