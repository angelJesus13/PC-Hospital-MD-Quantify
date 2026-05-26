# build

En esta carpeta se almacenan los archivos generados de la **WearableApp**, como versiones compiladas, paquetes listos para instalacion, artefactos de distribucion o cualquier archivo resultante del proceso de construccion de la aplicacion.

## Estructura de Archivos

```text
WearableApp
|-- build
|   |-- .gitkeep
```

## Contenido Esperado

| Elemento | Descripcion |
| --- | --- |
| Archivos compilados | Versiones generadas de la aplicacion wearable listas para pruebas o entrega. |
| Paquetes de instalacion | Archivos preparados para instalar la aplicacion en un dispositivo compatible. |
| Artefactos de build | Resultados tecnicos del proceso de construccion, como bundles, binarios o archivos empaquetados. |
| `.gitkeep` | Archivo temporal utilizado para conservar la carpeta dentro del repositorio cuando aun no contiene builds. |

## Proposito

La carpeta `build` permite separar los archivos finales generados del codigo fuente. Esto facilita identificar que archivos pertenecen al desarrollo y cuales corresponden a una version lista para revisar, probar o distribuir.

## Recomendaciones

- Mantener solo builds necesarios para entrega o revision.
- Nombrar los archivos generados con version, fecha o identificador claro.
- Evitar mezclar codigo fuente dentro de esta carpeta.
- Verificar que cada build corresponda con una version documentada del codigo.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |  Revisado y Aprobado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En Revision |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |


## Estado

La carpeta se encuentra preparada para recibir los artefactos generados de la WearableApp.
