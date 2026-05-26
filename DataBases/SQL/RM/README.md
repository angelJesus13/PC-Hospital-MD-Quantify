# MER — Modelo Relacional (SQL)

> **Proyecto:** PC-Hospital-MD-Quantify  
> **Motor:** MySQL 8.0+  
> **API de referencia:** [MEDICAL_REGISTER_API](https://github.com/AngelJdev/MEDICAL_REGISTER_API)  
> **Versión:** 2.0.0

---

## 1. Descripción General

El **Modelo Relacional (MER)** representa la implementación física de la base de datos del subsistema SQL de `PC-Hospital-MD-Quantify`. Traduce el modelo conceptual (MERE) en estructuras concretas: tablas, tipos de dato nativos de MySQL, llaves primarias, llaves foráneas, índices y restricciones de integridad referencial.

---

## 2. Esquema Relacional

### Notación

```
TABLA(PK: campo_pk, campo1: TIPO, campo2: TIPO, FK: campo_fk -> TABLA_REF.campo_ref)
```

---

### 2.1 `md_usuarios`

```
md_usuarios(
  PK: id INT AUTO_INCREMENT,
  username VARCHAR(80) NOT NULL UNIQUE,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(200) NOT NULL,
  role ENUM('admin','medico','enfermero') NOT NULL DEFAULT 'medico',
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  updated_at DATETIME ON UPDATE NOW()
)

Índices:
  PRIMARY KEY (id)
  UNIQUE INDEX idx_usuarios_username (username)
  UNIQUE INDEX idx_usuarios_email (email)
  INDEX idx_usuarios_role (role)
```

---

### 2.2 `md_pacientes`

```
md_pacientes(
  PK: id INT AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  curp CHAR(18) NOT NULL UNIQUE,
  fecha_nacimiento DATE,
  sexo ENUM('M','F','NB'),
  telefono VARCHAR(15),
  fecha_registro DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT NOW()
)

Índices:
  PRIMARY KEY (id)
  UNIQUE INDEX idx_pacientes_curp (curp)
  INDEX idx_pacientes_nombre (nombre)
  INDEX idx_pacientes_fecha_registro (fecha_registro)
```

---

### 2.3 `md_notas_medicas`

```
md_notas_medicas(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL -> md_pacientes.id ON DELETE CASCADE ON UPDATE CASCADE,
  FK: medico_id INT NOT NULL -> md_usuarios.id ON DELETE RESTRICT ON UPDATE CASCADE,
  contenido TEXT NOT NULL,
  tipo_nota ENUM('ingreso','evolucion','egreso','interconsulta','urgencias') NOT NULL,
  fecha DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT NOW()
)

Índices:
  PRIMARY KEY (id)
  INDEX idx_notas_paciente_fecha (paciente_id, fecha)
  INDEX idx_notas_medico (medico_id)
  INDEX idx_notas_tipo (tipo_nota)
  FOREIGN KEY fk_notas_paciente (paciente_id) REFERENCES md_pacientes(id)
  FOREIGN KEY fk_notas_medico (medico_id) REFERENCES md_usuarios(id)
```

---

### 2.4 `md_signos_vitales`

```
md_signos_vitales(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL -> md_pacientes.id ON DELETE CASCADE,
  tension_arterial VARCHAR(20),
  frecuencia_cardiaca INT UNSIGNED,
  temperatura DECIMAL(5,2),
  frecuencia_respiratoria INT UNSIGNED,
  saturacion_o2 INT UNSIGNED,
  escala_consciencia VARCHAR(30),
  score_mews INT UNSIGNED DEFAULT 0,
  fecha DATETIME NOT NULL
)

Restricciones de dominio:
  CHECK (frecuencia_cardiaca BETWEEN 0 AND 300)
  CHECK (temperatura BETWEEN 30.0 AND 45.0)
  CHECK (saturacion_o2 BETWEEN 0 AND 100)
  CHECK (frecuencia_respiratoria BETWEEN 0 AND 60)

Índices:
  PRIMARY KEY (id)
  INDEX idx_sv_paciente_fecha (paciente_id, fecha DESC)
  INDEX idx_sv_score_mews (score_mews)
  FOREIGN KEY fk_sv_paciente (paciente_id) REFERENCES md_pacientes(id)
```

---

### 2.5 `md_diagnostico`

```
md_diagnostico(
  PK: id INT AUTO_INCREMENT,
  FK: nota_id INT NOT NULL -> md_notas_medicas.id ON DELETE CASCADE,
  descripcion TEXT NOT NULL,
  codigo_cie CHAR(7),
  severidad ENUM('leve','moderado','grave','critico') DEFAULT 'leve',
  activo BOOLEAN NOT NULL DEFAULT TRUE
)

Restricciones:
  CHECK (codigo_cie REGEXP '^[A-Z][0-9]{2}(\\.[0-9]{1,2})?$')

Índices:
  PRIMARY KEY (id)
  INDEX idx_dx_nota (nota_id)
  INDEX idx_dx_codigo_cie (codigo_cie)
  INDEX idx_dx_severidad (severidad)
  FOREIGN KEY fk_dx_nota (nota_id) REFERENCES md_notas_medicas(id)
```

---

### 2.6 `md_tratamientos`

```
md_tratamientos(
  PK: id INT AUTO_INCREMENT,
  FK: diagnostico_id INT NOT NULL -> md_diagnostico.id ON DELETE CASCADE,
  medicamento VARCHAR(200) NOT NULL,
  dosis VARCHAR(50) NOT NULL,
  frecuencia VARCHAR(50) NOT NULL,
  duracion VARCHAR(30) NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  fecha_inicio DATETIME,
  fecha_fin DATETIME
)

Índices:
  PRIMARY KEY (id)
  INDEX idx_tx_diagnostico (diagnostico_id)
  INDEX idx_tx_activo (activo)
  INDEX idx_tx_medicamento (medicamento)
  FOREIGN KEY fk_tx_dx (diagnostico_id) REFERENCES md_diagnostico(id)
```

---

### 2.7 `md_nacimientos`

```
md_nacimientos(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL UNIQUE -> md_pacientes.id ON DELETE RESTRICT,
  fecha_nacimiento DATE NOT NULL,
  lugar VARCHAR(200) NOT NULL,
  nombre_madre VARCHAR(100),
  nombre_padre VARCHAR(100),
  peso_al_nacer DECIMAL(5,2),
  talla_al_nacer DECIMAL(5,2)
)

Índices:
  PRIMARY KEY (id)
  UNIQUE INDEX idx_nac_paciente (paciente_id)
  FOREIGN KEY fk_nac_paciente (paciente_id) REFERENCES md_pacientes(id)
```

---

### 2.8 `md_defunciones`

```
md_defunciones(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL UNIQUE -> md_pacientes.id ON DELETE RESTRICT,
  fecha_defuncion DATETIME NOT NULL,
  causa TEXT NOT NULL,
  causa_basica TEXT,
  certificador VARCHAR(50)
)

Índices:
  PRIMARY KEY (id)
  UNIQUE INDEX idx_def_paciente (paciente_id)
  INDEX idx_def_fecha (fecha_defuncion)
  FOREIGN KEY fk_def_paciente (paciente_id) REFERENCES md_pacientes(id)
```

---

### 2.9 `md_documentos_oficiales`

```
md_documentos_oficiales(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL -> md_pacientes.id ON DELETE CASCADE,
  tipo_documento ENUM('ine','curp','nss','pasaporte','acta_nacimiento') NOT NULL,
  numero_documento VARCHAR(60) NOT NULL,
  fecha_emision DATE,
  fecha_vencimiento DATE,
  vigente BOOLEAN NOT NULL DEFAULT TRUE
)

Índices:
  PRIMARY KEY (id)
  INDEX idx_docs_paciente (paciente_id)
  INDEX idx_docs_tipo (tipo_documento)
  UNIQUE INDEX idx_docs_numero (tipo_documento, numero_documento)
  FOREIGN KEY fk_docs_paciente (paciente_id) REFERENCES md_pacientes(id)
```

---

### 2.10 `md_domicilios`

```
md_domicilios(
  PK: id INT AUTO_INCREMENT,
  calle VARCHAR(200) NOT NULL,
  colonia VARCHAR(100) NOT NULL,
  municipio VARCHAR(100) NOT NULL,
  estado VARCHAR(60) NOT NULL,
  cp CHAR(5) NOT NULL,
  latitud DECIMAL(10,7),
  longitud DECIMAL(10,7)
)

Índices:
  PRIMARY KEY (id)
  INDEX idx_dom_municipio (municipio)
  INDEX idx_dom_estado (estado)
  INDEX idx_dom_cp (cp)
```

---

### 2.11 `md_personas_tiene_domicilio` (Tabla Intermedia N:M)

```
md_personas_tiene_domicilio(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL -> md_pacientes.id ON DELETE CASCADE,
  FK: domicilio_id INT NOT NULL -> md_domicilios.id ON DELETE CASCADE,
  tipo_domicilio ENUM('principal','temporal','referencia') NOT NULL DEFAULT 'principal',
  activo BOOLEAN NOT NULL DEFAULT TRUE
)

Índices:
  PRIMARY KEY (id)
  UNIQUE INDEX idx_ptd_unique (paciente_id, domicilio_id, tipo_domicilio)
  INDEX idx_ptd_paciente (paciente_id)
  INDEX idx_ptd_domicilio (domicilio_id)
  FOREIGN KEY fk_ptd_paciente (paciente_id) REFERENCES md_pacientes(id)
  FOREIGN KEY fk_ptd_domicilio (domicilio_id) REFERENCES md_domicilios(id)
```

---

### 2.12 `md_valoraciones`

```
md_valoraciones(
  PK: id INT AUTO_INCREMENT,
  FK: paciente_id INT NOT NULL -> md_pacientes.id ON DELETE CASCADE,
  escala VARCHAR(50) NOT NULL,
  resultado VARCHAR(10),
  observaciones TEXT,
  fecha DATETIME NOT NULL,
  FK: registrado_por INT -> md_usuarios.id ON DELETE SET NULL
)

Restricciones:
  CHECK (escala IN ('Glasgow','MEWS','APGAR','Braden','Norton','SOFA'))

Índices:
  PRIMARY KEY (id)
  INDEX idx_val_paciente_fecha (paciente_id, fecha DESC)
  INDEX idx_val_escala (escala)
  FOREIGN KEY fk_val_paciente (paciente_id) REFERENCES md_pacientes(id)
  FOREIGN KEY fk_val_usuario (registrado_por) REFERENCES md_usuarios(id)
```

---

## 3. Dependencias Funcionales

| Tabla | Dependencia Principal | Tipo |
| :--- | :--- | :--- |
| `md_notas_medicas` | `paciente_id`, `medico_id` | Multi-FK |
| `md_diagnostico` | `nota_id` | FK Cascada |
| `md_tratamientos` | `diagnostico_id` | FK Cascada |
| `md_signos_vitales` | `paciente_id` | FK Cascada |
| `md_valoraciones` | `paciente_id`, `registrado_por` | Multi-FK |
| `md_personas_tiene_domicilio` | `paciente_id`, `domicilio_id` | Pivot N:M |

---

## 4. Estrategia de Indexación

| Índice | Tabla | Propósito |
| :--- | :--- | :--- |
| `idx_pacientes_curp` | `md_pacientes` | Búsqueda por CURP (O(1)) |
| `idx_notas_paciente_fecha` | `md_notas_medicas` | Timeline de expediente |
| `idx_sv_paciente_fecha` | `md_signos_vitales` | Historial de signos (más reciente primero) |
| `idx_dx_codigo_cie` | `md_diagnostico` | Reportes epidemiológicos por CIE-10 |
| `idx_dom_municipio` | `md_domicilios` | Análisis geográfico |
| `idx_val_escala` | `md_valoraciones` | Consultas por tipo de escala |

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
