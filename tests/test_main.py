"""Pruebas de los modos de inicio del punto de entrada."""
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.services.data_manager import DataManager


class TestPuntoDeEntrada(unittest.TestCase):
    def setUp(self):
        self.main_path = Path(__file__).resolve().parents[1] / "src" / "main.py"
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data_manager = DataManager(self.tmp.name)

    def test_inicio_directo_en_modo_cli(self):
        with patch("src.services.data_manager.DataManager", return_value=self.data_manager), \
                patch.object(sys, "argv", [str(self.main_path), "--cli"]), \
                patch("builtins.input", return_value="0"):
            runpy.run_path(str(self.main_path), run_name="__main__")

    def test_inicio_directo_abre_la_gui(self):
        with patch("src.services.data_manager.DataManager", return_value=self.data_manager), \
                patch.object(sys, "argv", [str(self.main_path)]), \
                patch("src.ui.main_window.iniciar_gui") as iniciar_gui:
            runpy.run_path(str(self.main_path), run_name="__main__")

        iniciar_gui.assert_called_once()

if __name__ == "__main__":
    unittest.main()
# Practica de contribución realizada por Fernando Medina Morales
