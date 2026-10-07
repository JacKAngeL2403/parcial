# ⚡ ACDC Electronics – Gestión de Servicios Técnicos

Proyecto de **Construcción de Software** – equipo **Roshan coders**.

Sistema para que el técnico administrador de ACDC Electronics registre y consulte las solicitudes de servicio técnico de forma organizada, reemplazando el registro manual.

## Ejecución (Python 3.x, sin instalar dependencias)
```bash
git clone <URL_DEL_REPO>
cd <carpeta del repo>          # la que contiene la carpeta src
python -m src.main             # interfaz gráfica web (se abre en el navegador)
python -m src.main --cli       # interfaz de consola
python -m unittest discover tests
```

## Historias del Sprint
| HU | Descripción |
|---|---|
| HU01 | Registrar solicitud (cliente, equipo, servicio) con estado inicial `PENDIENTE` |
| HU02 | Consultar solicitudes ordenadas, con ID correlativo, o aviso si no hay registros |

## Equipo y responsabilidades
| Integrante | Tarea | Ruta |
|---|---|---|
| Benyamin Gutiérrez Pareja | T01 Definir datos de la solicitud | `src/domain/models.py` |
| Raul Mayta Mollo | T03 Validaciones del registro | `src/domain/exceptions.py` |
| Aldair Noe Escalante Barboza | T02 Registro de solicitudes | `src/services/`, `src/ui/web_interface.py` |
| Fernando Medina Morales | T04 Consulta de solicitudes | `src/services/app_service.py`, `src/ui/cli_interface.py` |
| Yuraldi Castelo Torre | T05 Casos de prueba + GitMaster | `tests/`, `src/main.py`, `architecture.md`, `.github/` |

## Flujo de trabajo
Feature Branch Workflow: `git pull` → `git checkout -b feature/...` → commits (`feat:`, `fix:`, `docs:`) → Pull Request con la plantilla → revisión → merge. Ver [architecture.md](architecture.md).
