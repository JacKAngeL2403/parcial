<div align="center">

# ⚡ ACDC Service Manager

**Sistema de gestión de servicios técnicos para ACDC Electronics (Cusco)**


![Python](https://img.shields.io/badge/Python-3.x-blue)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![Persistencia](https://img.shields.io/badge/Datos-JSON-green)
![Tests](https://img.shields.io/badge/Tests-unittest-brightgreen)

</div>

---

## 📌 Contexto

**ACDC Electronics** es una pequeña empresa ubicada en **Cusco**, dedicada a la reparación, mantenimiento e instalación de equipos eléctricos y electrónicos. Ocasionalmente también vende productos como termas eléctricas.

El análisis de la empresa mostró que gran parte de sus procesos es **manual y poco centralizada**: la información de clientes, equipos, servicios y reparaciones no se gestiona de forma integrada, lo que dificulta su registro, consulta y seguimiento.

## ❗ Problemática

> **La gestión poco centralizada y trazable de los servicios técnicos de ACDC Electronics.**

Esto genera dificultades para:

- 🗂️ Mantener organizada la información de clientes y sus equipos.
- 🔎 Registrar y consultar los servicios técnicos realizados.
- 🔧 Dar seguimiento al estado de las reparaciones.
- 📝 Conservar los diagnósticos y servicios realizados.
- 🧾 Mantener la trazabilidad de cada atención.
- 📦 Gestionar con orden los recursos usados en los servicios.

El problema no es solo la falta de una herramienta tecnológica, sino la oportunidad de **digitalizar procesos dispersos o manuales** y facilitar el acceso a la información.

## 🌱 Oportunidad futura

Algunos equipos pueden **recuperarse** tras el diagnóstico o la reparación. Esto abre la posibilidad de una línea de **reacondicionamiento y reutilización**, con beneficios sociales, económicos y ambientales: menos residuos electrónicos y equipos funcionales a precios más accesibles.

---

## 🎯 Objetivo

Desarrollar una aplicación de escritorio que permita **registrar clientes y equipos, crear órdenes de servicio y seguir cada reparación hasta su entrega**, guardando los datos de forma persistente.

## ✨ Funcionalidades (MVP)

| Módulo | Descripción |
|---|---|
| 👤 Clientes | Registro, búsqueda, edición y eliminación |
| 💻 Equipos | Registro asociado a un cliente |
| 🧾 Órdenes | Creación y consulta con filtros |
| 🩺 Diagnóstico | Registro de diagnóstico y costo estimado |
| 🔄 Estados | Seguimiento del ciclo de la reparación |
| 📦 Entrega | Cierre de la orden entregada |
| 💾 Persistencia | Almacenamiento en archivos JSON |

**Flujo de estados:**
`RECIBIDO → EN_DIAGNOSTICO → EN_REPARACION → REPARADO → ENTREGADO`
(desde `EN_DIAGNOSTICO` también puede pasar a `NO_REPARABLE`).

---

## 🛠️ Tecnologías

- **Python 3** con Programación Orientada a Objetos
- **Tkinter / ttk** para la interfaz gráfica
- **JSON** para la persistencia
- **unittest** para las pruebas
- **Git / GitHub** con Feature Branch Workflow

## 🏗️ Arquitectura

Arquitectura por capas: **UI → Servicios → Dominio**, con persistencia en JSON.
Más detalle en [`architecture.md`](architecture.md).

```text
src/
├── domain/      # Entidades, estados y excepciones
├── services/    # Casos de uso (AppService) y persistencia (DataManager)
├── ui/          # Interfaz gráfica (ventana, formularios, widgets, tema)
├── cli_interface.py
└── main.py
tests/           # Pruebas unitarias
```

## 🚀 Ejecución

```bash
# Clonar el repositorio
git clone https://github.com/JacKAngeL2403/esqueleto.git
cd esqueleto

# Abrir la interfaz gráfica
python -m src.main

# Abrir la interfaz de consola
python -m src.main --cli

# Ejecutar las pruebas
python -m unittest discover tests
```

---

## 👥 Equipo y roles

| Integrante | Rol / Célula | Responsabilidades principales |
|---|---|---|
| **Benyamin Gutiérrez Pareja** | Célula 1 – Dominio | Diseño e implementación de las entidades principales, aplicando POO, encapsulamiento y comportamiento de las clases. |
| **Yuraldi Castelo Torre** | Célula 1 – Dominio | Apoyo en el dominio, validaciones, excepciones personalizadas y pruebas de las entidades. |
| **Fernando Medina Morales** | Célula 2 – Servicios y Datos | Casos de uso y lógica de aplicación mediante los servicios que gestionan las operaciones. |
| **Raul Mayta Mollo** | Célula 2 – Servicios y Datos | Persistencia en JSON y apoyo en consultas, filtros y operaciones de los servicios. |
| **Aldair Noe Escalante Barboza** | GitMaster / Integrador | Administración del repositorio, coordinación de ramas, revisión e integración de Pull Requests, control de `main` e integración final. |
| **Adriana Roque Quispe y todo el equipo** | Célula 3 – Interfaz | Interfaz gráfica, formularios, navegación, presentación de datos y validación básica de entradas. |

## 🔀 Flujo de trabajo en Git

1. `main` está protegida: no se hace commit directo.
2. Cada cambio se trabaja en una rama `feature/<nombre>`.
3. Se abre un **Pull Request** con la plantilla del repositorio (incluye el prompt de IA usado).
4. El GitMaster revisa, comenta y hace el merge.
5. Las ramas se conservan para mantener el historial visible.

---

<div align="center">

**ACDC Electronics · Cusco, Perú**
Proyecto académico de Programación Orientada a Objetos

</div>
