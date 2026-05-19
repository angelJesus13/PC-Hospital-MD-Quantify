# build

## Descripcion general

La carpeta `build` almacena los artefactos generados a partir del proceso de compilacion, empaquetado o preparacion de la API para su entrega o despliegue.

## Objetivo

Su funcion es reunir en un solo lugar los archivos derivados del codigo fuente que ya se encuentran listos para distribucion, publicacion o ejecucion en un entorno destino.

## Contenido esperado

En esta carpeta pueden encontrarse:

- binarios o paquetes compilados;
- archivos comprimidos para distribucion;
- resultados del proceso de build;
- recursos generados automaticamente por herramientas de construccion.

## Consideraciones

- El contenido puede variar dependiendo de la tecnologia empleada.
- No sustituye a la carpeta `source/`, ya que aqui solo deben ubicarse productos generados.
- Se recomienda conservar unicamente versiones relevantes para la entrega o despliegue.
