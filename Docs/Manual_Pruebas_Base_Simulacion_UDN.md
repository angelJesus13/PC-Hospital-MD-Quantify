# Manual de Pruebas Base de Simulación

## 1. Introducción
Este documento describe el Manual de Pruebas Base de Simulación para la Unidad de Desarrollo de Negocio (UDN) del proyecto PC-Hospital-MD-Quantify. Contiene un conjunto de 10 pruebas específicas diseñadas para validar el comportamiento de la plataforma en escenarios de simulación clave.

## 2. Objetivo
Validar funcionalidades críticas del sistema mediante pruebas de simulación que reproduzcan condiciones operativas reales, garantizando:
- Exactitud en los cálculos de indicadores.
- Integridad de los datos de entrada y salida.
- Estabilidad del sistema bajo flujos de trabajo de UDN.
- Confiabilidad de las decisiones automatizadas.

## 3. Alcance
Aplica a la capa de simulación y predicción del sistema, incluyendo:
- Módulos de ingestión de datos.
- Motor de simulación.
- Generación y análisis de resultados.
- Reportes y alertas asociados a la UDN.

No cubre pruebas de integración física de hardware ni pruebas de usuario final fuera del entorno simulado.

## 4. Metodología de prueba
1. Preparar el entorno de simulación con datos de prueba representativos.
2. Ejecutar cada prueba en el orden asignado.
3. Registrar resultados y comparar con los criterios esperados.
4. Documentar incidencias y comportamientos no conformes.

Las pruebas deben ejecutarse en un entorno controlado, idealmente con datos iniciales conocidos y valores esperados definidos.

## 5. Convenciones
- `Entrada`: Datos o condiciones iniciales para la prueba.
- `Acción`: Pasos que se realizan durante la prueba.
- `Resultado esperado`: Comportamiento correcto que debe observarse.
- `Resultado real`: Observación obtenida al ejecutar la prueba.
- `Estado`: Aprobado / Rechazado / Observaciones.

## 6. Pruebas específicas de la UDN

### Prueba 1: Verificación de carga de datos iniciales
- Entrada: Conjunto de datos de pacientes, citas y recursos de hospital.
- Acción: Cargar datos en el motor de simulación.
- Resultado esperado: Datos importados sin errores, sin registros truncados y con todas las tablas relacionadas pobladas.
- Criterio de aprobación: 100% de registros importados, sin conflictos de formato.

### Prueba 2: Simulación de flujo de atención de paciente
- Entrada: Paciente con caso de urgencia y recursos hospitalarios disponibles.
- Acción: Ejecutar simulación de atención desde ingreso hasta egreso.
- Resultado esperado: Flujo lógico completo, tiempos de atención calculados correctamente y estado final del paciente registrado.
- Criterio de aprobación: Coincidencia entre tiempos simulados y los valores de referencia en un margen aceptable.

### Prueba 3: Generación de alertas por saturación de recursos
- Entrada: Escenario con ocupación del 95% de camas y personal médico limitado.
- Acción: Ejecutar simulación y monitorear el motor de reglas.
- Resultado esperado: Se produce alerta de saturación, priorización de pacientes y recomendaciones de reasignación.
- Criterio de aprobación: Alerta registrada y acciones previstas generadas.

### Prueba 4: Validación de cálculos de indicadores clave
- Entrada: Datos de desempeño de la UDN durante un ciclo de simulación.
- Acción: Calcular indicadores como tiempo promedio de espera, tasa de ocupación y ratio de atención.
- Resultado esperado: Indicadores calculados con valores exactos según fórmula.
- Criterio de aprobación: Resultados coinciden con cálculos manuales de prueba.

### Prueba 5: Simulación de escenario extremo de demanda
- Entrada: Incremento repentino de pacientes en un 50%.
- Acción: Ejecutar simulación de demanda alta.
- Resultado esperado: Sistema mantiene estabilidad, registra pérdidas de servicio y propone medidas.
- Criterio de aprobación: No hay fallos críticos, y el informe incluye saturación y recursos insuficientes.

### Prueba 6: Control de integridad de los datos de salida
- Entrada: Resultados generados por una simulación completa.
- Acción: Validar consistencia de reportes y exportaciones.
- Resultado esperado: Salidas contienen todos los campos requeridos, sin valores nulos injustificados.
- Criterio de aprobación: Reportes exportados correctamente y archivos generados sin error.

### Prueba 7: Comprobación de reprogramación de turnos médicos
- Entrada: Agenda médica con cambios de última hora.
- Acción: Simular reprogramación y verificación de efecto en atención.
- Resultado esperado: Ajustes de turnos aplicados y resultados de simulación actualizados.
- Criterio de aprobación: Simulación refleja nuevos horarios y no hay conflictos de recursos.

### Prueba 8: Evaluación de reglas de priorización de pacientes
- Entrada: Lista de pacientes con diferentes niveles de urgencia.
- Acción: Ejecutar motor de decisión para asignar prioridad.
- Resultado esperado: Pacientes con mayor urgencia reciben atención primero según reglas UDN.
- Criterio de aprobación: Orden de atención correcto y documentación de decisiones.

### Prueba 9: Simulación de mantenimiento de infraestructura
- Entrada: Escenario con un servicio hospitalario temporalmente fuera de servicio.
- Acción: Ejecutar simulación con recurso indisponible.
- Resultado esperado: Sistema redirige cargas, ajusta tiempos y actualiza disponibilidad.
- Criterio de aprobación: Resultados reflejan impacto del mantenimiento y las alternativas propuestas.

### Prueba 10: Validación de respuesta a eventos externos
- Entrada: Evento externo como una contingencia masiva o emergencia.
- Acción: Simular emergencia y evaluar respuestas del sistema.
- Resultado esperado: Estrategias de contingencia activadas, prioridades ajustadas y reportes de impacto.
- Criterio de aprobación: Sistema detecta evento, ejecuta respuestas planificadas y registra métricas de impacto.

## 7. Registro de resultados
Crear una tabla de registro para cada prueba con los siguientes campos:
- ID de prueba
- Nombre de prueba
- Fecha de ejecución
- Ejecutado por
- Resultado esperado
- Resultado real
- Estado
- Observaciones

## 8. Conclusiones y seguimiento
- Asegurar la resolución de deficiencias encontradas.
- Repetir las pruebas después de cada cambio significativo en la UDN o en el motor de simulación.
- Actualizar el manual si se introducen nuevos casos de uso o escenarios.

## 9. Anexos
- Datos de prueba usados en las simulaciones.
- Criterios de aceptación de la UDN.
- Definiciones de indicadores y reglas de priorización.
