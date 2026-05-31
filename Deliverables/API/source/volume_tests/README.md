# API Híbrida: Hospital MD (MySQL + MongoDB)

Sistema diseñado para la simulación, inserción, sincronización y manejo volumétrico de **Notas Médicas** para un flujo hospitalario masivo, validando integridad clínica, auditoría normativa y arquitectura híbrida estructurada y no estructurada.

---

## 🚀 Requisitos y Configuración Inicial de Base de Datos

### 1. Entorno
El sistema ocupa controladores nativos tanto para infraestructuras relacionales (MySQL) como para NoSQL (MongoDB). Crea un archivo **`.env`** en la carpeta principal `ABD_Hospital_MD_MongoDB` con las siguientes credenciales:

```ini
# ====== MySQL Configuracion ======
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tulaclave_aqui
MYSQL_DB=hospital_hibrido_md

# ====== MongoDB Configuracion ======
MONGO_URI=mongodb+srv://TuUsuario:TuPass@cluster...
MONGO_DB_NAME=hospital_hibrido_md
```

### 2. Dependencias del Servidor
Instala los paquetes obligatorios de Python usando el archivo provisto:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Inicialización y Arranque

FastAPI se encarga de autoconstruir **automáticamente** las tablas/colecciones vírgenes si no existen al iniciar el servidor (como `tbb_md_notas_medicas`, `tbi_bitacora` y los Procedimientos Almacenados Dinámicos de MySQL).

Abre tu terminal en la ruta principal y ejecuta Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Verás en consola las conexiones exitosas tanto a MySQL como a MongoDB. 

---

## 📖 Swagger UI y Ejecución Dinámica

Toda la interacción con el poblado masivo o limpieza general se efectúa a través de los **Endpoints REST** creados de forma reflexiva tanto para NoSQL como SQL. 

Ingresa a tu navegador: 👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 📊 Las 5 Pruebas de Volumen Clínico (523,346 registros)

La API cuenta con endpoints `POST /api/sql/poblar-notas` y `POST /api/nosql/poblar-notas/{cantidad}`.
Para inyectar el entorno relacional de SQL, debes ingresar los siguientes **JSONs de configuración clínica** en la caja del Swagger al momento de ejecutar la simulación paramétrica. Estas mismas cantidades y conceptos se aplican para las peticiones a la ruta NoSQL:

### Prueba 1: Ingreso y Evolución (Adultos Generales)
*Total: 80,000 registros*
Se inyectan pacientes al flujo hospitalario común sin gravedad crítica.
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
*Total: 120,000 registros*
Simulación de alto volumen de triaje. Se habilita el `paciente_zero` para forzar identidades anónimas y falta de interrogatorios (llegadas por urgencias traumáticas).
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
*Total: 43,346 registros*
Trafico lateral de diagnósticos y opiniones especializadas (Cardiología, Neurología, etc.).
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
*Total: 50,000 registros*
Flujo de dadas de alta médicas del hospital con ligeras anomalías programadas (correcciones y cancelaciones en el estatus administrativo).
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
*Total: 230,000 registros*
La prueba de estrés máxima. Habilita Unidades de Cuidados Intensivos (UCI), Cuidados Pediátricos (alterando métricas corporales y FK's al bloque de pediatría), y Urgencias extremas simultáneas.
```json
{
  "cantidad": 230000,
  "tipos_nota": ["Ingreso", "Evolución", "Urgencia", "Egreso", "Interconsulta"],
  "incluir_pediatria": true,
  "incluir_uci": true,
  "incluir_paciente_zero": true
}
```

---
*NOTA: Cada prueba SQL ejecutada hará el commit seguro progresivamente a la DB y generará estrictamente **1 sola inserción auditora** en `tbi_bitacora` (SQL) o colecciones Bitacora (Mongo) con el resumen del test ejecutado.*

---

## 🟢 Las 5 Pruebas de Volumen Híbridas NoSQL (283,462 registros)

El endpoint `POST /api/nosql/poblar-notas/` ha sido orquestado para replicar arquitectónicamente las 5 pasadas de alta concurrencia pero forzando el motor de MongoDB. Introduce los siguientes JSONs en Swagger:

### Prueba 1: Carga Base Estacionaria (Consulta Externa)
*Total: 86,512 registros*
Pacientes estables, evolución rutinaria.
```json
{
  "cantidad": 86512,
  "foco_clinico": ["Estable"]
}
```

### Prueba 2: Sobrecarga Infecciosa Cíclica
*Total: 63,141 registros*
Cuadros de fiebres, sepsias y afecciones respiratorias.
```json
{
  "cantidad": 63141,
  "foco_clinico": ["Infeccioso"]
}
```

### Prueba 3: Politraumatismos Médicos
*Total: 58,493 registros*
Choques hipovolémicos, traumatismos craneoencefálicos y hemorragias.
```json
{
  "cantidad": 58493,
  "foco_clinico": ["Trauma"]
}
```

### Prueba 4: Ala Pediátrica y Neonatología UCIN
*Total: 44,115 registros*
Saturación en recién nacidos. El motor calculará automáticamente la viabilidad de Apgar en los diccionarios anidados.
```json
{
  "cantidad": 44115,
  "foco_clinico": ["Pediátrica"]
}
```

### Prueba 5: Pacientes Críticos Absolutos
*Total: 31,201 registros*
La prueba de estrés NoSQL más alta. Genera sub-documentos asimétricos masivos de paros cardiorrespiratorios y crisis letales.
```json
{
  "cantidad": 31201,
  "foco_clinico": ["Paro", "Hipertensiva"]
}
```
