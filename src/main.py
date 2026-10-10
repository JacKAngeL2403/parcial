"""Punto de entrada: python -m src.main  (o --cli para la interfaz de consola)."""
import os
import sys

if _package_ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from src.services.app_service import AppService
    from src.services.data_manager import DataManager
else:
    from .services.app_service import AppService
    from .services.data_manager import DataManager


def main() -> None:
    app = AppService(DataManager())
    if "--cli" in sys.argv:
        if _package_ in (None, ""):
            from src.ui.cli_interface import CLI
        else:
            from .ui.cli_interface import CLI
        CLI(app).ejecutar()
    else:
        if _package_ in (None, ""):
            from src.ui.main_window import iniciar_gui
        else:
            from .ui.main_window import iniciar_gui
        iniciar_gui(app)


if _name_ == "_main_":
    main()
