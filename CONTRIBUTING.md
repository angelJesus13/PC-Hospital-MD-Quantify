# Guía de Contribución y Estándares (PC-Hospital-MD)

Este documento define el flujo de trabajo, las convenciones de código y los estándares de revisión (Pull Requests) para el equipo multidisciplinario (Frontend, Backend, DBAs y Documentación).

## 1. Flujo de Ramas (Git Flow Adaptado)
Para mantener la estabilidad del ecosistema clínico, utilizamos una estrategia basada en ramas de características (*Feature Branches*):
*   **`main`**: Rama de producción. Solo acepta código a través de Pull Requests (PRs) previamente aprobados. Nunca se hace commit directo aquí.
*   **`develop`**: Rama de integración. Todas las ramas de características nacen y se fusionan aquí.
*   **Ramas de trabajo**: Deben seguir la nomenclatura:
    *   `feat/nombre-caracteristica` (Ej. `feat/alertas-socket`)
    *   `fix/nombre-correccion` (Ej. `fix/documentation-upgrade`)
    *   `docs/nombre-documento` (Ej. `docs/manual-pruebas`)

## 2. Convenciones de Commits (Conventional Commits)
Nuestros mensajes de commit deben estar automatizados o seguir estrictamente el estándar:
*   `feat: [Módulo] Descripción corta` (Añade una funcionalidad)
*   `fix: [Módulo] Descripción de la corrección` (Repara un bug)
*   `docs: Descripción` (Actualización de documentación)
*   `test: Añade mocks o pruebas de estrés`
*   *Ejemplo:* `feat: [API] Añade endpoint de ingesta biométrica`

## 3. Estándares de Código y Linting
Para asegurar la coherencia en un equipo multidisciplinario (React, Node, Bases de Datos):
*   **JavaScript/Node (API y WebApp):** Todo el código debe pasar por **ESLint** (configuración recomendada de Airbnb) y **Prettier** para el formato automático. Se recomienda el uso de Husky para ejecutar linting antes de cada commit (`pre-commit hook`).
*   **Bases de Datos (SQL):** Las variables, tablas y columnas deben utilizar `snake_case` (ej. `paciente_profesional`).
*   **Bases de Datos (MongoDB):** Las colecciones y documentos en BSON utilizarán `camelCase` (ej. `wearableLogs`).

## 4. Criterios de Aprobación de Pull Requests (PRs)
Antes de que un PR pueda integrarse a `develop` o `main`, debe cumplir:
1.  **Revisión por pares (Code Review):** Al menos 1 aprobación de un miembro distinto al autor (idealmente del Lead Developer de esa capa).
2.  **Pruebas Exitosas:** Si aplica, evidencia de que el código pasa las pruebas unitarias o de integración (captura de Thunder Client/Postman).
3.  **Linting sin Errores:** No debe haber advertencias rojas de ESLint.
4.  **Documentación Actualizada:** Si se modificó la API, `openapi.yaml` y la Trazabilidad deben reflejar el cambio.
