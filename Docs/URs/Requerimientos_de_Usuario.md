# Requerimientos de Usuario (URs) y Perfiles - PC-Hospital-MD

Este documento profundiza en las necesidades diferenciadas de nuestros usuarios, basándose en la metodología de **Diseño Centrado en el Usuario (UCD)** mediante la técnica de "User Personas" y Mapas de Empatía.

## Metodología de Levantamiento
Los requerimientos fueron extraídos mediante entrevistas semi-estructuradas con profesionales clínicos y pacientes piloto, apoyados en bitácoras de feedback semanales para garantizar que el sistema MERN (WebApp/WearableApp) resuelva problemas reales de atención médica remota.

---

## 1. User Persona: Dr. Roberto (Médico Internista)
*   **Perfil:** 45 años, saturado de pacientes diarios, experto en clínica pero no en tecnología avanzada.
*   **Objetivo Principal:** Reducir el tiempo que gasta revisando expedientes en papel y prevenir crisis de pacientes crónicos ambulatorios.
*   **Mapa de Empatía (Empathy Map):**
    *   **Piensa/Siente:** Siente frustración cuando los datos de un paciente están desactualizados; piensa que la tecnología debería trabajar para él, no al revés.
    *   **Ve:** Muchos pacientes que olvidan llevar sus bitácoras manuales de signos vitales.
    *   **Dice/Hace:** "¿Cómo está el paciente X de la cama 3? Necesito su historial de ritmo cardíaco de ayer".
    *   **Puntos de Dolor (Pains):** Interfaces clínicas complejas y lentas. No enterarse a tiempo de un evento crítico.
*   **Requerimiento Directo (UR-01):** "Necesito un Dashboard web en mi consultorio que, al instante de abrirlo, me muestre un listado claro de mis pacientes y coloree en rojo a aquellos cuyos dispositivos Wearables detectaron anomalías, para priorizar su atención". (Traza hacia UH-04).

## 2. User Persona: Doña Carmen (Paciente Monitoreada)
*   **Perfil:** 68 años, hipertensa, usuaria básica de smartphone, vive sola.
*   **Objetivo Principal:** Sentirse segura en casa sabiendo que su doctor "está pendiente" de ella.
*   **Mapa de Empatía:**
    *   **Piensa/Siente:** Siente ansiedad por sufrir un ataque sin que nadie lo note.
    *   **Ve:** Sus hijos le compraron un smartwatch para cuidarla, pero no sabe interpretar los datos.
    *   **Dice/Hace:** Trata de ser disciplinada, pero a veces olvida tomarse el pulso.
    *   **Puntos de Dolor (Pains):** Frustración ante aplicaciones con letras pequeñas o configuraciones complejas.
*   **Requerimiento Directo (UR-02):** "Quiero usar una aplicación en mi reloj que automáticamente mida mi pulso todo el día y lo envíe a mi doctor en el hospital sin que yo deba picarle a botones difíciles". (Traza hacia UH-02).

## 3. User Persona: Ing. Laura (Administradora de Sistemas Hospitalarios)
*   **Perfil:** 35 años, jefa de TI de la clínica.
*   **Objetivo Principal:** Garantizar que el sistema no colapse, asignar perfiles de acceso correctos y proteger los datos privados (cumplimiento normativo).
*   **Mapa de Empatía:**
    *   **Piensa/Siente:** Preocupación constante por brechas de ciberseguridad o caídas del servidor.
    *   **Puntos de Dolor (Pains):** Bases de datos monolíticas que se traban cuando hay demasiados pacientes simultáneos.
*   **Requerimiento Directo (UR-03):** "Necesito una plataforma segura donde pueda dar de alta a los médicos, vincular el ID de sus pacientes y asegurar que los respaldos híbridos (MySQL/MongoDB) ocurran cada madrugada". (Traza hacia UH-01).

---
## Bitácora de Feedback (Resumen Iterativo)
*   **Sprint 1:** El panel médico mostraba demasiada información. *Acción:* Se implementó un Dashboard minimalista (Engineering Aesthetic).
*   **Sprint 2:** Las consultas a MySQL para biometría causaban latencia. *Acción:* Migración de `wearable_logs` hacia MongoDB (NoSQL) para agilizar lecturas.
