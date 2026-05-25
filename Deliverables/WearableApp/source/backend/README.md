# backend

En esta carpeta se organiza el backend de la **WearableApp**. Aqui se deben ubicar los archivos relacionados con la logica de procesamiento, manejo de datos, comunicacion con servicios externos, validaciones y posibles conexiones con APIs o bases de datos.

## Estructura de Archivos

```text
WearableApp
|-- source
|   |-- backend
|   |   |-- .gitkeep
```

## Contenido Esperado

| Elemento | Descripcion |
| --- | --- |
| Servicios | Funciones o modulos encargados de obtener, procesar o enviar informacion. |
| Controladores | Archivos que coordinan acciones entre la aplicacion y la logica interna. |
| Modelos | Estructuras utilizadas para representar datos del paciente, mediciones o registros. |
| Configuracion | Variables, rutas, credenciales de entorno o parametros necesarios para la ejecucion. |
| Integraciones | Conexion con APIs, servicios del sistema o componentes externos del proyecto. |

## Proposito

El backend permite que la WearableApp gestione correctamente la informacion capturada o consultada desde el dispositivo wearable. Esta capa debe encargarse de mantener la logica ordenada y preparar los datos para que puedan ser utilizados por la interfaz o por otros modulos del sistema.

## Responsabilidades

- Procesar datos obtenidos desde el wearable.
- Validar informacion antes de enviarla o almacenarla.
- Preparar respuestas para el frontend.
- Gestionar integraciones con APIs o servicios del proyecto.
- Mantener la seguridad y consistencia de la informacion.

## Recomendaciones

- Separar servicios, modelos y configuraciones cuando el codigo crezca.
- Evitar colocar vistas o componentes visuales en esta carpeta.
- Documentar endpoints, estructuras de datos o funciones importantes.
- Proteger informacion sensible mediante variables de entorno cuando aplique.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | En Revision |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Completado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |


## Estado

La carpeta esta lista para recibir la implementacion backend de la WearableApp.
