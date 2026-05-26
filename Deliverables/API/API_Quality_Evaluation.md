# Evaluación de Calidad de la API

## Descripción general

Este documento concentra la evaluación de calidad de la API del proyecto **PC-Hospital-MD-Quantify**. Su objetivo es servir como evidencia para la revisión intergrupal entre pares, considerando aspectos funcionales, técnicos, de seguridad, documentación y mantenibilidad.

La evaluación permite identificar fortalezas, riesgos y áreas de mejora antes de integrar la API con las aplicaciones WebApp y WearableApp.

## Datos de la revisión

| Campo | Valor |
| --- | --- |
| Proyecto | PC-Hospital-MD-Quantify |
| Módulo evaluado | API |
| Tipo de evaluación | Intergrupal - Entre pares |
| Fecha de revisión | 19 de mayo de 2026 |
| Estado | En revisión |
| Equipo evaluador | Pendiente de asignación |
| Equipo evaluado | Equipo Quantify |

## Alcance de la evaluación

La evaluación se enfoca en verificar que la API cumpla con criterios mínimos de calidad para un sistema orientado al registro, consulta y procesamiento de información clínica, operativa y de monitoreo.

Se consideran los siguientes componentes:

- estructura del proyecto backend;
- endpoints principales;
- validación de entradas;
- manejo de errores;
- seguridad básica;
- consistencia de respuestas;
- conexión con bases de datos;
- documentación técnica;
- facilidad de despliegue;
- preparación para pruebas y mantenimiento.

## Criterios de calidad

| Criterio | Descripción | Peso |
| --- | --- | --- |
| Funcionalidad | La API cumple con las operaciones esperadas y responde correctamente a los flujos definidos. | 20% |
| Confiabilidad | La API maneja errores, entradas inválidas y condiciones inesperadas sin fallar de forma crítica. | 15% |
| Seguridad | La API protege información sensible, valida accesos y evita exposición innecesaria de datos. | 15% |
| Rendimiento | La API mantiene tiempos de respuesta adecuados en operaciones comunes. | 10% |
| Mantenibilidad | El código y la estructura permiten entender, modificar y ampliar el servicio. | 15% |
| Documentación | La API cuenta con instrucciones, rutas, parámetros y respuestas documentadas. | 15% |
| Integración | La API puede conectarse con la base de datos y otros módulos del sistema. | 10% |

## Escala de evaluación

| Puntaje | Nivel | Interpretación |
| --- | --- | --- |
| 5 | Excelente | Cumple completamente y no requiere cambios importantes. |
| 4 | Bueno | Cumple correctamente, con detalles menores por mejorar. |
| 3 | Aceptable | Cumple parcialmente, pero requiere ajustes visibles. |
| 2 | Deficiente | Presenta fallas importantes que afectan el uso esperado. |
| 1 | Crítico | No cumple o impide validar el funcionamiento del componente. |

## Checklist de revisión

| ID | Aspecto revisado | Evidencia esperada | Puntaje | Observaciones |
| --- | --- | --- | --- | --- |
| API-01 | La API cuenta con estructura clara de carpetas. | Separación de rutas, controladores, servicios o archivos equivalentes. | Pendiente | Pendiente |
| API-02 | Los endpoints principales están definidos. | Rutas para crear, consultar, actualizar o eliminar información según aplique. | Pendiente | Pendiente |
| API-03 | Las respuestas son consistentes. | Uso uniforme de códigos HTTP, mensajes y formato JSON. | Pendiente | Pendiente |
| API-04 | Existe validación de datos de entrada. | Validación de campos obligatorios, tipos de datos y rangos permitidos. | Pendiente | Pendiente |
| API-05 | El manejo de errores es claro. | Respuestas controladas para errores 400, 401, 404 y 500. | Pendiente | Pendiente |
| API-06 | La API protege datos sensibles. | No expone contraseñas, tokens, credenciales ni configuraciones privadas. | Pendiente | Pendiente |
| API-07 | La conexión a base de datos está documentada. | Instrucciones o variables necesarias para conectar SQL o NoSQL. | Pendiente | Pendiente |
| API-08 | La API puede desplegarse con instrucciones reproducibles. | Manual de despliegue disponible en `DeployManual`. | Pendiente | Pendiente |
| API-09 | Se incluyen pruebas o evidencias de simulación. | Capturas, logs, colecciones o resultados de pruebas. | Pendiente | Pendiente |
| API-10 | La API está preparada para integración con WebApp/WearableApp. | Endpoints o contratos claros para consumo desde frontend. | Pendiente | Pendiente |

## Matriz de resultado

| Criterio | Peso | Puntaje obtenido | Cálculo | Resultado |
| --- | --- | --- | --- | --- |
| Funcionalidad | 20% | Pendiente | Puntaje x 0.20 | Pendiente |
| Confiabilidad | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Seguridad | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Rendimiento | 10% | Pendiente | Puntaje x 0.10 | Pendiente |
| Mantenibilidad | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Documentación | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Integración | 10% | Pendiente | Puntaje x 0.10 | Pendiente |
| **Total** | **100%** | **Pendiente** | **Suma ponderada** | **Pendiente** |

## Evidencia solicitada

Para completar la evaluación entre pares se recomienda anexar o referenciar:

- capturas de ejecución de endpoints;
- colección de pruebas en Postman, Thunder Client o herramienta equivalente;
- logs de respuestas correctas y errores controlados;
- archivo de variables de entorno de ejemplo;
- instrucciones de ejecución local;
- resultados de pruebas de carga o simulación si están disponibles;
- comentarios del equipo evaluador.

## Riesgos detectables durante la revisión

| Riesgo | Impacto | Mitigación sugerida |
| --- | --- | --- |
| Falta de validación en endpoints | Puede permitir datos incompletos o incorrectos. | Agregar validadores por ruta y mensajes claros. |
| Respuestas inconsistentes | Dificulta la integracion con frontend. | Definir formato estandar para respuestas exitosas y errores. |
| Credenciales expuestas | Compromete la seguridad del proyecto. | Usar variables de entorno y excluir archivos sensibles. |
| Manual incompleto | Complica el despliegue por terceros. | Actualizar `DeployManual` con requisitos y pasos verificables. |
| Ausencia de pruebas | Reduce confianza en la estabilidad de la API. | Documentar casos minimos y resultados esperados. |

## Formato sugerido de observaciones intergrupales

| Revisor | Hallazgo | Severidad | Recomendación | Estado |
| --- | --- | --- | --- | --- |
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Conclusiones preliminares

La API cuenta con una estructura de entregables preparada para integrar código fuente, build y manual de despliegue. La evaluación final dependerá de la revisión directa de endpoints, pruebas ejecutadas, evidencias técnicas y documentación disponible al momento de la entrega.

## Equipo de desarrollo

| Integrante | Rol | Observaciones |
| --- | --- | --- |
| Ángel de Jesús Baños Téllez | Líder de desarrollo | Revisado y aprobado |
| Francisco García García | Desarrollador | Revisado y aprobado |
| Jesús Alejandro Artiaga Morales | Desarrollador | Revisado y aprobado |
| Al Farias Leyva | Desarrollador | Revisado y aprobado |
| Brian Jesús Mendoza Márquez | Desarrollador | Revisado y aprobado |
