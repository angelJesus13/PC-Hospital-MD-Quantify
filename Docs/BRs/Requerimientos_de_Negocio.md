# Requerimientos de Negocio (BRs) - PC-Hospital-MD

Este documento contiene la especificación de los **Requerimientos de Negocio (Business Requirements - BRs)** para la plataforma **PC-Hospital-MD**, un sistema integral de registros médicos (EHR) y monitoreo de salud.

## Objetivos de Negocio Estratégicos

### BR-01: Monitoreo Remoto de Salud
El sistema debe permitir el monitoreo continuo de los pacientes mediante la integración de dispositivos tipo *wearable*. Esto habilitará a los profesionales de la salud para supervisar signos vitales fuera de las instalaciones del hospital, mejorando la atención preventiva y reduciendo los reingresos hospitalarios.

### BR-02: Sistema Inteligente de Alertas Médicas
La plataforma debe contar con la capacidad de procesar biometría en tiempo real. Ante cualquier anomalía en signos vitales (ej. ritmo cardíaco o niveles de oxigenación críticos), se deben disparar alertas automatizadas que notifiquen inmediatamente al perfil del Profesional de Salud asignado, permitiendo una intervención oportuna.

### BR-03: Viabilidad Operativa mediante Arquitectura Híbrida
Para asegurar el soporte del inmenso volumen de datos generado por los biosensores, la plataforma adoptará una base de datos híbrida:
*   **MySQL (Transaccional):** Asegura la integridad relacional de expedientes clínicos, credenciales de usuarios, perfiles médicos y asignaciones de pacientes.
*   **MongoDB (NoSQL):** Almacenamiento optimizado para la retención a alta frecuencia de biometría diaria (`wearable_logs`) e historiales de los pacientes.

---

## Equipo de Desarrollo (Equipo Quantify)

| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús Baños Téllez** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Jesus Alejandro Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |
