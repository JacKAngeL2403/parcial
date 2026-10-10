"""Pruebas de servicios y persistencia (usan carpeta temporal)."""
import tempfile
import unittest

from src.domain.exceptions import (EntidadNoEncontradaError, TransicionInvalidaError,
                                   ValidacionError)
from src.services.app_service import AppService
from src.services.data_manager import DataManager


class TestAppService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.app = AppService(DataManager(self.tmp.name))
        self.c = self.app.registrar_cliente("Ana", "987654321", "ana@mail.com")
        self.e = self.app.registrar_equipo(self.c.id_cliente, "Laptop", "HP", "X1", "No enciende")

    def test_ids_secuenciales(self):
        c2 = self.app.registrar_cliente("Luis", "912345678", "luis@mail.com")
        self.assertEqual((self.c.id_cliente, c2.id_cliente), ("C-001", "C-002"))

    def test_busquedas(self):
        self.assertEqual(len(self.app.buscar_cliente("ana")), 1)
        self.assertEqual(len(self.app.buscar_equipo("hp")), 1)
        self.assertEqual(self.app.buscar_cliente("zzz"), [])

    def test_equipo_cliente_inexistente(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.app.registrar_equipo("C-999", "TV", "LG", "A", "x")

    def test_crear_orden_equipo_ajeno(self):
        c2 = self.app.registrar_cliente("Luis", "912345678", "luis@mail.com")
        with self.assertRaises(ValidacionError):
            self.app.crear_orden(c2.id_cliente, self.e.id_equipo, "falla")

    def test_flujo_completo_y_filtros(self):
        o = self.app.crear_orden(self.c.id_cliente, self.e.id_equipo, "No enciende")
        self.app.actualizar_estado(o.id_orden, "EN_DIAGNOSTICO")
        self.app.registrar_diagnostico(o.id_orden, "Fuente", 90)
        self.app.actualizar_estado(o.id_orden, "EN_REPARACION")
        self.app.actualizar_estado(o.id_orden, "REPARADO")
        self.assertEqual(len(self.app.buscar_orden(estado="REPARADO")), 1)
        self.app.registrar_entrega(o.id_orden)
        self.assertEqual(self.app.obtener_orden(o.id_orden).estado.value, "ENTREGADO")
        self.assertEqual(len(self.app.buscar_orden(cliente="ana", codigo="OS-001")), 1)

    def test_errores_de_estado(self):
        o = self.app.crear_orden(self.c.id_cliente, self.e.id_equipo, "x")
        with self.assertRaises(ValidacionError):
            self.app.actualizar_estado(o.id_orden, "INVENTADO")
        with self.assertRaises(TransicionInvalidaError):
            self.app.actualizar_estado(o.id_orden, "ENTREGADO")
        with self.assertRaises(EntidadNoEncontradaError):
            self.app.obtener_orden("OS-999")

    def test_persistencia(self):
        o = self.app.crear_orden(self.c.id_cliente, self.e.id_equipo, "x")
        self.app.actualizar_estado(o.id_orden, "EN_DIAGNOSTICO")
        otra = AppService(DataManager(self.tmp.name))
        self.assertEqual(len(otra.listar_clientes()), 1)
        self.assertEqual(len(otra.listar_equipos()), 1)
        self.assertEqual(otra.obtener_orden("OS-001").estado.value, "EN_DIAGNOSTICO")

    def test_estadisticas_y_crud(self):
        c = self.app.registrar_cliente("Luis", "900000000", "luis@mail.com")
        e = self.app.registrar_equipo(c.id_cliente, "TV", "Samsung", "Q7", "Sin imagen")
        o = self.app.crear_orden(c.id_cliente, e.id_equipo, "Sin imagen")
        self.app.actualizar_estado(o.id_orden, "EN_DIAGNOSTICO")
        self.app.registrar_diagnostico(o.id_orden, "Panel dañado", 125.0)
        self.app.actualizar_estado(o.id_orden, "EN_REPARACION")
        self.app.actualizar_estado(o.id_orden, "REPARADO")
        self.app.registrar_entrega(o.id_orden)

        stats = self.app.estadisticas()
        self.assertEqual(stats["clientes_totales"], 2)
        self.assertEqual(stats["equipos_totales"], 2)
        self.assertEqual(stats["ordenes_totales"], 1)
        self.assertEqual(stats["ordenes_activas"], 0)

        self.app.actualizar_cliente(c.id_cliente, "Luis Torres", "911111111", "luis.nuevo@mail.com")
        self.assertEqual(self.app.obtener_cliente(c.id_cliente).nombre, "Luis Torres")

        self.app.actualizar_equipo(e.id_equipo, c.id_cliente, "TV", "Samsung", "Q8", "Sin voz")
        self.assertEqual(self.app.obtener_equipo(e.id_equipo).modelo, "Q8")

        self.app.eliminar_orden(o.id_orden)
        self.app.eliminar_equipo(e.id_equipo)
        self.app.eliminar_cliente(c.id_cliente)
        self.assertEqual(len(self.app.listar_clientes()), 1)
        self.assertEqual(len(self.app.listar_equipos()), 1)
        self.assertEqual(len(self.app.listar_ordenes()), 0)


if __name__ == "__main__":
    unittest.main()

