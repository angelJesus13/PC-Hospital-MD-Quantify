# Interfaces Gráficas (GUIs) - PC-Hospital-MD

El repositorio incluye el diseño de los tableros gráficos para interactuar con el Expediente Clínico de forma remota. Todas las interfaces web están desarrolladas con **React** y estilizadas con **Tailwind CSS**.

## Principios de Diseño Visual Clínico
Dado que es un sistema médico, las interfaces priorizan la rápida interpretación de datos:
*   **Colores de Estado:** El uso de métricas rojas indica una alerta crítica (taquicardia, baja oxigenación), mientras que los tonos verdes demuestran estabilidad.
*   **Paneles de Alto Contraste:** Para mejorar la legibilidad en entornos clínicos (computadoras de consultorio o tabletas móviles de guardia), la WebApp implementa tipografía clara y distribución en tarjetas (Cards).

> El detalle de cada interfaz está en sus respectivas subcarpetas:
> 1. `WebApp/Interfaces_WebApp.md` (Para uso de Administradores y Médicos)
> 2. `WearableApp/Interfaces_WearableApp.md` (Para uso de Pacientes)
