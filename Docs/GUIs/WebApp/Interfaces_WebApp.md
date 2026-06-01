# Interfaces Gráficas - WebApp (Panel Médico)

La aplicación web provee el acceso completo al sistema de registros médicos y gestión de expedientes.

## 1. Dashboard de Monitorización (Médico)
*   **Alerta Temprana:** Notificaciones destacadas en rojo (top bar) cuando un paciente asignado envía biometría crítica.
*   **Lista de Pacientes Activos:** Tabla (creada en React) que lista pacientes, su edad, sexo y fecha de la última medición vital.
*   **Filtros de Asignación:** Un menú lateral que muestra solo los expedientes bajo la supervisión directa del profesional logueado.

## 2. Vista de Expediente Clínico (EHR)
*   **Detalle Demográfico:** Panel lateral con datos fijos provenientes de la base de datos relacional (MySQL).
*   **Visualizador Biométrico:** Gráficas de líneas y barras representando el historial de ritmo cardíaco o niveles de oxígeno a lo largo del tiempo, extraídos velozmente desde MongoDB.

## 3. Panel Administrativo (Administrador)
*   **Gestión de Alta (CRUD):** Formularios administrativos para el alta, baja o modificación de médicos y pacientes.
*   **Asignador de Wearables:** Vista especial para registrar el identificador físico (UUID) de un nuevo reloj médico inteligente a la cuenta de un paciente de la base de datos.
