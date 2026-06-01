# Documentacion de Modelos de Datos

> **Proyecto:** PC-Hospital-MD-Quantify
> **Version:** 2.0.0
> **Alcance:** Modelos analiticos y trazabilidad de datos clinicos
> **Estado:** Diseno documentado; entrenamiento pendiente

## 1. Proposito

Este documento define los modelos analiticos que pueden construirse con la
informacion disponible en `PC-Hospital-MD-Quantify`. Describe el objetivo de
cada modelo, sus fuentes de datos, variables de entrada, salida esperada,
metricas y consideraciones de uso.

El repositorio ya implementa reglas clinicas deterministas para calcular MEWS,
clasificar valoraciones y detectar algunas interacciones farmacologicas. No se
encontraron modelos de aprendizaje automatico entrenados, notebooks, datasets
procesados ni artefactos serializados. Por esa razon, los modelos supervisados
y no supervisados descritos aqui se presentan como propuestas trazables para
las siguientes etapas del proyecto.

## 2. Arquitectura de Datos Disponible

La aplicacion utiliza una arquitectura hibrida:

| Capa | Tecnologia | Datos disponibles |
| --- | --- | --- |
| Persistencia transaccional | MySQL | Usuarios, pacientes, notas, signos vitales, diagnosticos, tratamientos, valoraciones, documentos y domicilios |
| Persistencia flexible | MongoDB | Logs de auditoria, telemetria de sesiones, detalles de valoraciones y alertas |
| API | FastAPI | Validacion, reglas clinicas, consultas y sincronizacion SQL + NoSQL |
| DataModels | Documentacion analitica | Diseno de modelos, variables, metricas y trazabilidad |

### 2.1 Tablas SQL relevantes

| Tabla | Uso analitico principal |
| --- | --- |
| `md_pacientes` | Identificador del paciente y variables demograficas |
| `md_notas_medicas` | Cronologia clinica y tipo de atencion |
| `md_signos_vitales` | Variables fisiologicas y puntaje MEWS |
| `md_diagnostico` | Codigos CIE-10, severidad y estado |
| `md_tratamientos` | Medicamentos prescritos y tratamientos activos |
| `md_valoraciones` | Resultados resumidos de escalas clinicas |
| `md_domicilios` | Variables geograficas para analisis epidemiologico |
| `md_personas_tiene_domicilio` | Vinculo entre paciente y ubicacion |

### 2.2 Colecciones MongoDB relevantes

| Coleccion | Uso analitico principal |
| --- | --- |
| `valoraciones_flexibles` | Componentes de escalas, alertas vitales e interacciones farmacologicas |
| `logs_auditoria` | Eventos, errores, emergencias y actividad por usuario |
| `telemetria_sesion` | Uso por turno, area clinica, endpoint y duracion de sesion |

### 2.3 Esquema de pruebas de volumen

El modulo `Deliverables/API/source/volume_tests` crea tablas `tbb_*` y
`tbi_bitacora` para simulaciones masivas. Estos datos pueden servir para
pruebas de rendimiento y prototipos, pero deben etiquetarse como sinteticos y
mantenerse separados de cualquier conjunto de datos clinico real.

## 3. Funcionalidad Analitica ya Implementada

Las siguientes funciones forman parte de la API actual. Son reglas
deterministas, no modelos entrenados.

| Funcion | Ubicacion | Entradas | Salida |
| --- | --- | --- | --- |
| Calculo MEWS | `Deliverables/API/source/utils/helpers.py` | Frecuencia cardiaca, frecuencia respiratoria, saturacion O2, temperatura y consciencia | Puntaje y nivel de riesgo |
| Clasificacion Glasgow | `Deliverables/API/source/utils/helpers.py` | Puntaje total Glasgow | `Leve`, `Moderado` o `Grave` |
| Clasificacion de valoraciones | `Deliverables/API/source/routes/valoraciones.py` | Escala, total y componentes | Nivel de alerta |
| Alerta vital automatica | `Deliverables/API/source/routes/signos_vitales.py` | Puntaje MEWS | Documento MongoDB cuando `MEWS >= 5` |
| Deteccion de interacciones | `Deliverables/API/source/routes/tratamientos.py` | Medicamento nuevo y tratamientos activos | Advertencia de interaccion conocida |

Estas reglas son una linea base util: cualquier modelo posterior debe
compararse contra ellas antes de integrarse en la API.

## 4. Catalogo de Modelos Propuestos

| ID | Modelo | Tipo | Objetivo | Carpeta futura | Estado |
| --- | --- | --- | --- | --- | --- |
| `SUP-01` | Riesgo de deterioro clinico | Supervisado: clasificacion | Estimar riesgo de alerta vital en la siguiente ventana de observacion | `Supervised_LMs/` | Propuesto |
| `SUP-02` | Priorizacion de severidad diagnostica | Supervisado: clasificacion | Apoyar la revision de severidad registrada en diagnosticos | `Supervised_LMs/` | Propuesto |
| `UNS-01` | Segmentacion de perfiles clinicos | No supervisado: clustering | Agrupar pacientes por patrones fisiologicos y clinicos | `Unsupervised_LMs/` | Propuesto |
| `UNS-02` | Deteccion de patrones atipicos | No supervisado: deteccion de anomalias | Identificar tomas fisiologicas o sesiones operativas fuera del comportamiento habitual | `Unsupervised_LMs/` | Propuesto |

## 5. Modelos Supervisados

### 5.1 `SUP-01`: Riesgo de deterioro clinico

**Objetivo:** estimar si un paciente presentara una alerta vital en una ventana
temporal posterior a una toma de signos vitales.

**Unidad de analisis:** una toma de `md_signos_vitales` asociada con un
paciente.

**Variable objetivo propuesta:** presencia de un documento
`valoraciones_flexibles.tipo = "alerta_vital"` para el mismo paciente dentro
de una ventana definida, por ejemplo 6, 12 o 24 horas.

| Variable | Fuente | Tipo | Tratamiento sugerido |
| --- | --- | --- | --- |
| `frecuencia_cardiaca` | `md_signos_vitales` | Numerica | Imputacion controlada y escalado |
| `frecuencia_respiratoria` | `md_signos_vitales` | Numerica | Imputacion controlada y escalado |
| `saturacion_o2` | `md_signos_vitales` | Numerica | Imputacion controlada y escalado |
| `temperatura` | `md_signos_vitales` | Numerica | Imputacion controlada y escalado |
| `tension_arterial` | `md_signos_vitales` | Texto estructurado | Separar sistolica y diastolica |
| `escala_consciencia` | `md_signos_vitales` | Categorica o texto corto | Normalizar categorias |
| `score_mews` | `md_signos_vitales` | Numerica | Usar como linea base y evaluar fuga de informacion |
| `sexo` | `md_pacientes` | Categorica | Codificacion categorica |
| `edad` | `md_pacientes.fecha_nacimiento` | Numerica derivada | Calcular respecto a la fecha de la toma |
| `diagnosticos_activos` | `md_diagnostico` | Categorica multiple | Agrupar por codigo CIE-10 o severidad |

**Algoritmos iniciales sugeridos:**

- regresion logistica como linea base interpretable;
- arboles de decision o random forest para relaciones no lineales;
- gradient boosting si el volumen y la calidad del dataset lo justifican.

**Metricas recomendadas:**

| Metrica | Motivo |
| --- | --- |
| `recall` de la clase de riesgo | Reducir alertas clinicas no detectadas |
| `precision` | Controlar falsas alarmas |
| `F1-score` | Equilibrar precision y cobertura |
| `PR-AUC` | Evaluar clases potencialmente desbalanceadas |
| Matriz de confusion | Revisar errores de forma comprensible |

**Precaucion:** si `score_mews` se usa como entrada y la etiqueta deriva
directamente de `MEWS >= 5`, el modelo solo aprendera a reproducir la regla
existente. Para evaluar valor adicional deben construirse etiquetas con una
ventana futura y evitar fuga temporal.

### 5.2 `SUP-02`: Priorizacion de severidad diagnostica

**Objetivo:** apoyar la revision de la severidad registrada en
`md_diagnostico.severidad`. No sustituye el criterio medico.

**Unidad de analisis:** un diagnostico asociado con una nota medica.

**Variable objetivo propuesta:** `md_diagnostico.severidad`.

| Variable | Fuente | Tipo | Tratamiento sugerido |
| --- | --- | --- | --- |
| `codigo_cie` | `md_diagnostico` | Categorica | Agrupar por categoria CIE-10 |
| `descripcion` | `md_diagnostico` | Texto | Vectorizacion controlada |
| `tipo_nota` | `md_notas_medicas` | Categorica | Codificacion one-hot |
| `contenido` | `md_notas_medicas` | Texto clinico | Revisar privacidad antes de procesar |
| Ultimos signos vitales | `md_signos_vitales` | Numerica | Seleccionar toma previa a la nota |
| `score_mews` | `md_signos_vitales` | Numerica | Seleccionar valor previo a la nota |
| Escalas recientes | `md_valoraciones` | Categorica y numerica | Agregar por ventana temporal |

**Algoritmos iniciales sugeridos:**

- regresion logistica multiclase como linea base;
- random forest para variables tabulares;
- modelos de texto solo despues de anonimizar y evaluar el corpus clinico.

**Metricas recomendadas:**

| Metrica | Motivo |
| --- | --- |
| `macro F1-score` | Dar peso comparable a cada nivel de severidad |
| `recall` por clase | Revisar particularmente `grave` y `critico` |
| Matriz de confusion | Detectar confusiones entre niveles cercanos |

## 6. Modelos No Supervisados

### 6.1 `UNS-01`: Segmentacion de perfiles clinicos

**Objetivo:** identificar grupos de pacientes con patrones similares para
analisis exploratorio, priorizacion de estudios y generacion de hipotesis.

**Unidad de analisis:** paciente con variables agregadas en una ventana
temporal definida.

| Variable agregada | Fuente |
| --- | --- |
| Promedio, minimo y maximo de frecuencia cardiaca | `md_signos_vitales` |
| Promedio, minimo y maximo de saturacion O2 | `md_signos_vitales` |
| Promedio y maximo de temperatura | `md_signos_vitales` |
| Maximo y promedio de MEWS | `md_signos_vitales` |
| Conteo de notas por tipo | `md_notas_medicas` |
| Conteo de diagnosticos por severidad | `md_diagnostico` |
| Conteo de tratamientos activos | `md_tratamientos` |
| Conteo de alertas e intervenciones | `valoraciones_flexibles` |

**Algoritmos iniciales sugeridos:**

- `K-Means` como linea base;
- clustering jerarquico para exploracion;
- `DBSCAN` si se busca identificar grupos densos y ruido.

**Metricas recomendadas:**

- coeficiente de silueta;
- indice Davies-Bouldin;
- estabilidad de clusters entre ejecuciones;
- revision clinica cualitativa de cada grupo.

### 6.2 `UNS-02`: Deteccion de patrones atipicos

**Objetivo:** identificar observaciones poco frecuentes que ameriten revision.
El resultado representa una senal analitica, no una emergencia clinica
confirmada.

**Casos de uso:**

| Caso | Fuentes | Ejemplos |
| --- | --- | --- |
| Tomas fisiologicas atipicas | `md_signos_vitales` | Combinaciones inusuales de FC, FR, SpO2 y temperatura |
| Uso operativo atipico | `telemetria_sesion` | Duracion, volumen de solicitudes o turnos inusuales |
| Actividad de auditoria atipica | `logs_auditoria` | Frecuencia elevada de errores o accesos no autorizados |

**Algoritmos iniciales sugeridos:**

- Isolation Forest;
- Local Outlier Factor;
- reglas estadisticas robustas como linea base.

**Metricas y validacion recomendadas:**

- proporcion de observaciones marcadas;
- revision manual de muestras;
- comparacion contra alertas MEWS existentes;
- seguimiento de falsos positivos.

## 7. Preparacion de Datos

El flujo de preparacion debe documentarse y versionarse antes de entrenar:

1. Extraer datos SQL con llaves internas y marcas de tiempo.
2. Incorporar documentos MongoDB mediante `paciente_id`,
   `valoracion_sql_id` o `usuario_id`, segun corresponda.
3. Etiquetar cada fuente como clinica real, semilla de desarrollo o simulacion
   de volumen.
4. Eliminar duplicados y validar rangos fisiologicos.
5. Aplicar anonimizacion o seudonimizacion antes de entrenar.
6. Dividir los datos respetando el tiempo para evitar fuga entre entrenamiento
   y evaluacion.
7. Registrar transformaciones, variables finales y version del dataset.

## 8. Gobierno y Seguridad

Los modelos trabajan con informacion clinica sensible. Antes de usarlos fuera
de un entorno academico o experimental deben aplicarse estas medidas:

- excluir CURP, nombres, correos, telefonos y direcciones del dataset de
  entrenamiento;
- utilizar identificadores seudonimizados;
- conservar trazabilidad de la fuente y fecha de cada observacion;
- separar datos sinteticos de datos reales;
- revisar sesgos por sexo, edad, area clinica y disponibilidad de mediciones;
- mantener supervision humana para decisiones clinicas;
- documentar version, metricas, limitaciones y fecha de evaluacion del modelo.

## 9. Estructura de Artefactos

No se crean carpetas nuevas. La estructura existente cubre el trabajo futuro:

| Ruta | Uso |
| --- | --- |
| `DataModels/README.md` | Portada e indice |
| `DataModels/Data_Model_Documentation.md` | Catalogo general de modelos |
| `DataModels/Supervised_LMs/` | Artefactos futuros de `SUP-01` y `SUP-02` |
| `DataModels/Unsupervised_LMs/` | Artefactos futuros de `UNS-01` y `UNS-02` |

## 10. Evidencia Minima por Modelo

Cuando se implemente un modelo, su carpeta debe incluir:

| Evidencia | Descripcion |
| --- | --- |
| README | Objetivo, autor, fecha, version y limitaciones |
| Dataset manifest | Fuentes, filtros, rango temporal y cantidad de registros |
| Script o notebook | Preparacion, entrenamiento y evaluacion reproducible |
| Metricas | Resultados por clase o cluster |
| Artefacto exportado | Modelo serializado, cuando aplique |
| Registro de cambios | Ajustes de variables, hiperparametros y resultados |

## 11. Archivos de Referencia

| Archivo | Contenido |
| --- | --- |
| `DataBases/SQL/DD/README.md` | Diccionario de datos SQL |
| `DataBases/NoSQL/DD/README.md` | Diccionario de datos MongoDB |
| `Deliverables/API/source/models.py` | Modelos ORM SQLAlchemy |
| `Deliverables/API/source/mongo_database.py` | Colecciones e indices MongoDB |
| `Deliverables/API/source/utils/helpers.py` | Reglas MEWS y Glasgow |
| `Deliverables/API/source/routes/signos_vitales.py` | Alertas vitales |
| `Deliverables/API/source/routes/valoraciones.py` | Valoraciones SQL + MongoDB |
| `Deliverables/API/source/routes/tratamientos.py` | Interacciones farmacologicas |
| `Deliverables/API/source/volume_tests/` | Datos sinteticos para pruebas |

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
