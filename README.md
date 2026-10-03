# Proyecto Aegis

![Aegis Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange.svg)

## Visión General

**Proyecto Aegis** es una plataforma integral de observabilidad de seguridad, orquestación DevSecOps y gestión de API Gateway bajo el paradigma **Zero-Trust**. Diseñado para operar en entornos Cloud-Native y ecosistemas de microservicios corporativos de alta demanda. 

Esta solución proporciona un plano de control centralizado y de clase mundial que automatiza las políticas de seguridad, empuja alertas de intrusión en tiempo real y gestiona dinámicamente el tráfico a través de un gateway distribuido, asegurando una postura de seguridad robusta e inmutable.

## Arquitectura y Patrones de Diseño

El proyecto se fundamenta en rigurosos principios de ingeniería de software para garantizar la escalabilidad, el bajo acoplamiento y la mantenibilidad a largo plazo:

*   **Clean Architecture:** El backend está estrictamente dividido en capas (Domain, Application, Infrastructure, Presentation/Interfaces), aislando la lógica de negocio de los detalles de implementación (frameworks, bases de datos, APIs de terceros).
*   **Domain-Driven Design (DDD):** El núcleo de la aplicación modela entidades complejas como nodos perimetrales, alertas de seguridad y políticas de certificados (ej. `EndpointNode`, `SecurityAlert`, `SSLCertificatePolicy`).
*   **CQRS (Command Query Responsibility Segregation):** Separación lógica entre los canales de escritura (orquestación de seguridad, actualización de políticas WAF) y los canales de lectura (telemetría en tiempo real y dashboards analíticos).
*   **Zero-Trust Network Access (ZTNA):** Integración nativa con Envoy Proxy para autorizar y cifrar el tráfico lateral y de entrada por defecto, implementando un control de acceso granular y basado en identidad.
*   **Event-Driven & Real-Time Telemetry:** Uso de WebSockets (Socket.IO sobre ASGI) para la transmisión full-duplex de eventos y logs de auditoría en vivo al Security Posture Dashboard.

## Stack Tecnológico

### Backend
*   **Lenguaje:** Python 3.12
*   **Framework:** FastAPI (ASGI)
*   **ORM y Base de Datos:** SQLAlchemy 2.0 (PostgreSQL), Alembic para migraciones.
*   **Validación de Datos:** Pydantic V2
*   **Tiempo Real:** python-socketio

### Frontend
*   **Tecnologías:** React, TypeScript, Vite
*   **Estilizado:** Tailwind CSS
*   **Gestión de Estado:** Zustand (Global State Management)

### Infraestructura & DevSecOps
*   **Contenedores:** Docker & Docker Compose
*   **Gateway / Edge Proxy:** Envoy Proxy (Configuración dinámica y WAF routing)
*   **Bases de Datos:** PostgreSQL 15
*   **Automatización SSL:** CertManager custom worker (Let's Encrypt DNS-01)

## Módulos Principales

1.  **Aegis Gateway Controller:**
    Módulo para la mutación dinámica del plano de control de Envoy. Permite inyectar reglas de enrutamiento y endurecimiento de WAF al vuelo, sin disrupción del tráfico en vivo.
2.  **Telemetry & Audit Stream:**
    Canal de comunicación asíncrona implementado con FastAPI y Socket.IO para propagar métricas de salud de los microservicios y alertas de fuerza bruta directo al dashboard interactivo del operador.
3.  **CertManager (DNS-01):**
    Worker orquestado para la auditoría y renovación ininterrumpida de certificados TLS/SSL en el ecosistema, interactuando con los registros DNS de dominios perimetrales.
4.  **Security Posture Dashboard:**
    Interfaz central de mando que consume WebSockets para proyectar un mapa de calor táctico del tráfico, el estado de los contenedores (via integraciones con Portainer/Proxmox), y la superficie de vulnerabilidad detectada en SAST/DAST pipelines.

---

> **Nota:** Este proyecto forma parte del portafolio profesional de **Javier Andrey Giraldo Rivera**, demostrando capacidades avanzadas en Arquitectura Cloud-Native, DevSecOps e Ingeniería de Software.
