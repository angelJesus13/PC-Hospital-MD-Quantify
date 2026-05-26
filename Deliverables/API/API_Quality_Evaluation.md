# Evaluacion de Calidad de la API

## Descripcion general

Este documento concentra la evaluacion de calidad de la API del proyecto **PC-Hospital-MD-Quantify**. Su objetivo es servir como evidencia para la revision intergrupal entre pares, considerando aspectos funcionales, tecnicos, de seguridad, documentacion y mantenibilidad.

La evaluacion permite identificar fortalezas, riesgos y areas de mejora antes de integrar la API con las aplicaciones WebApp y WearableApp.

## Datos de la revision

| Campo | Valor |
| --- | --- |
| Proyecto | PC-Hospital-MD-Quantify |
| Modulo evaluado | API |
| Tipo de evaluacion | Intergrupal - Entre pares |
| Fecha de revision | 19 de mayo de 2026 |
| Estado | En revision |
| Equipo evaluador | Pendiente de asignacion |
| Equipo evaluado | Equipo Quantify |

## Alcance de la evaluacion

La evaluacion se enfoca en verificar que la API cumpla con criterios minimos de calidad para un sistema orientado al registro, consulta y procesamiento de informacion clinica, operativa y de monitoreo.

Se consideran los siguientes componentes:

- estructura del proyecto backend;
- endpoints principales;
- validacion de entradas;
- manejo de errores;
- seguridad basica;
- consistencia de respuestas;
- conexion con bases de datos;
- documentacion tecnica;
- facilidad de despliegue;
- preparacion para pruebas y mantenimiento.

## Criterios de calidad

| Criterio | Descripcion | Peso |
| --- | --- | --- |
| Funcionalidad | La API cumple con las operaciones esperadas y responde correctamente a los flujos definidos. | 20% |
| Confiabilidad | La API maneja errores, entradas invalidas y condiciones inesperadas sin fallar de forma critica. | 15% |
| Seguridad | La API protege informacion sensible, valida accesos y evita exposicion innecesaria de datos. | 15% |
| Rendimiento | La API mantiene tiempos de respuesta adecuados en operaciones comunes. | 10% |
| Mantenibilidad | El codigo y la estructura permiten entender, modificar y ampliar el servicio. | 15% |
| Documentacion | La API cuenta con instrucciones, rutas, parametros y respuestas documentadas. | 15% |
| Integracion | La API puede conectarse con la base de datos y otros modulos del sistema. | 10% |

## Escala de evaluacion

| Puntaje | Nivel | Interpretacion |
| --- | --- | --- |
| 5 | Excelente | Cumple completamente y no requiere cambios importantes. |
| 4 | Bueno | Cumple correctamente, con detalles menores por mejorar. |
| 3 | Aceptable | Cumple parcialmente, pero requiere ajustes visibles. |
| 2 | Deficiente | Presenta fallas importantes que afectan el uso esperado. |
| 1 | Critico | No cumple o impide validar el funcionamiento del componente. |

## Checklist de revision

| ID | Aspecto revisado | Evidencia esperada | Puntaje | Observaciones |
| --- | --- | --- | --- | --- |
| API-01 | La API cuenta con estructura clara de carpetas. | Separacion de rutas, controladores, servicios o archivos equivalentes. | Pendiente | Pendiente |
| API-02 | Los endpoints principales estan definidos. | Rutas para crear, consultar, actualizar o eliminar informacion segun aplique. | Pendiente | Pendiente |
| API-03 | Las respuestas son consistentes. | Uso uniforme de codigos HTTP, mensajes y formato JSON. | Pendiente | Pendiente |
| API-04 | Existe validacion de datos de entrada. | Validacion de campos obligatorios, tipos de datos y rangos permitidos. | Pendiente | Pendiente |
| API-05 | El manejo de errores es claro. | Respuestas controladas para errores 400, 401, 404 y 500. | Pendiente | Pendiente |
| API-06 | La API protege datos sensibles. | No expone contrasenas, tokens, credenciales ni configuraciones privadas. | Pendiente | Pendiente |
| API-07 | La conexion a base de datos esta documentada. | Instrucciones o variables necesarias para conectar SQL o NoSQL. | Pendiente | Pendiente |
| API-08 | La API puede desplegarse con instrucciones reproducibles. | Manual de despliegue disponible en `DeployManual`. | Pendiente | Pendiente |
| API-09 | Se incluyen pruebas o evidencias de simulacion. | Capturas, logs, colecciones o resultados de pruebas. | Pendiente | Pendiente |
| API-10 | La API esta preparada para integracion con WebApp/WearableApp. | Endpoints o contratos claros para consumo desde frontend. | Pendiente | Pendiente |

## Matriz de resultado

| Criterio | Peso | Puntaje obtenido | Calculo | Resultado |
| --- | --- | --- | --- | --- |
| Funcionalidad | 20% | Pendiente | Puntaje x 0.20 | Pendiente |
| Confiabilidad | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Seguridad | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Rendimiento | 10% | Pendiente | Puntaje x 0.10 | Pendiente |
| Mantenibilidad | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Documentacion | 15% | Pendiente | Puntaje x 0.15 | Pendiente |
| Integracion | 10% | Pendiente | Puntaje x 0.10 | Pendiente |
| **Total** | **100%** | **Pendiente** | **Suma ponderada** | **Pendiente** |

## Evidencia solicitada

Para completar la evaluacion entre pares se recomienda anexar o referenciar:

- capturas de ejecucion de endpoints;
- coleccion de pruebas en Postman, Thunder Client o herramienta equivalente;
- logs de respuestas correctas y errores controlados;
- archivo de variables de entorno de ejemplo;
- instrucciones de ejecucion local;
- resultados de pruebas de carga o simulacion si estan disponibles;
- comentarios del equipo evaluador.

## Riesgos detectables durante la revision

| Riesgo | Impacto | Mitigacion sugerida |
| --- | --- | --- |
| Falta de validacion en endpoints | Puede permitir datos incompletos o incorrectos. | Agregar validadores por ruta y mensajes claros. |
| Respuestas inconsistentes | Dificulta la integracion con frontend. | Definir formato estandar para respuestas exitosas y errores. |
| Credenciales expuestas | Compromete la seguridad del proyecto. | Usar variables de entorno y excluir archivos sensibles. |
| Manual incompleto | Complica el despliegue por terceros. | Actualizar `DeployManual` con requisitos y pasos verificables. |
| Ausencia de pruebas | Reduce confianza en la estabilidad de la API. | Documentar casos minimos y resultados esperados. |

## Formato sugerido de observaciones intergrupales

| Revisor | Hallazgo | Severidad | Recomendacion | Estado |
| --- | --- | --- | --- | --- |
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Conclusiones preliminares

La API cuenta con una estructura de entregables preparada para integrar codigo fuente, build y manual de despliegue. La evaluacion final dependera de la revision directa de endpoints, pruebas ejecutadas, evidencias tecnicas y documentacion disponible al momento de la entrega.

## Equipo de desarrollo

| Integrante | Rol | Observaciones |
| --- | --- | --- |
| Angel de Jesus Baños Tellez | Lider de desarrollo | Revisado y aprobado |
| Francisco Garcia Garcia | Desarrollador | Revisado y aprobado |
| Jesus Alejandro Artiaga Morales | Desarrollador | Revisado y aprobado |
| Al Farias Leyva | Desarrollador | Revisado y aprobado |
| Brian Jesus Mendoza Marquez | Desarrollador | Revisado y aprobado |
