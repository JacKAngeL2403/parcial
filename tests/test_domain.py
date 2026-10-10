"""Pruebas unitarias del dominio."""
import unittest

from src.domain.exceptions import TransicionInvalidaError, ValidacionError
from src.domain.models import Cliente, Equipo, EstadoOrden, OrdenServicio


def nueva_orden() -> OrdenServicio:
    return OrdenServicio("OS-001", "C-001", "E-001", "No enciende")


class TestCliente(unittest.TestCase):
    def test_creacion_correcta(self):
        c = Cliente("C-001", " Ana ", "987654321", "ana@mail.com")
        self.assertEqual(c.nombre, "Ana")
        self.assertEqual(c.id_cliente, "C-001")

    def test_nombre_vacio(self):
        with self.assertRaises(ValidacionError):
            Cliente("C-001", "  ", "987654321", "a@b.com")

    def test_telefono_invalido(self):
        with self.assertRaises(ValidacionError):
            Cliente("C-001", "Ana", "abc", "a@b.com")

    def test_correo_invalido(self):
        with self.assertRaises(ValidacionError):
            Cliente("C-001", "Ana", "987654321", "sin-arroba")

    def test_encapsulamiento(self):
        c = Cliente("C-001", "Ana", "987654321", "a@b.com")
        with self.assertRaises(AttributeError):
            c.nombre = "Otro"


class TestEquipo(unittest.TestCase):
    def test_creacion_correcta(self):
        e = Equipo("E-001", "C-001", "Laptop", "HP", "Pavilion", "No carga")
        self.assertEqual(e.marca, "HP")

    def test_campo_vacio(self):
        with self.assertRaises(ValidacionError):
            Equipo("E-001", "C-001", "Laptop", "", "Pavilion", "No carga")


class TestOrden(unittest.TestCase):
    def test_estado_inicial(self):
        o = nueva_orden()
        self.assertEqual(o.estado, EstadoOrden.RECIBIDO)
        self.assertIsNone(o.diagnostico)
        self.assertIsNone(o.costo)

    def test_falla_vacia(self):
        with self.assertRaises(ValidacionError):
            OrdenServicio("OS-001", "C-001", "E-001", " ")

    def test_flujo_completo(self):
        o = nueva_orden()
        o.cambiar_estado(EstadoOrden.EN_DIAGNOSTICO)
        o.registrar_diagnostico("Fuente quemada", 80)
        o.cambiar_estado(EstadoOrden.EN_REPARACION)
        o.cambiar_estado(EstadoOrden.REPARADO)
        o.registrar_entrega()
        self.assertEqual(o.estado, EstadoOrden.ENTREGADO)
        self.assertIsNotNone(o.fecha_entrega)

    def test_flujo_no_reparable(self):
        o = nueva_orden()
        o.cambiar_estado(EstadoOrden.EN_DIAGNOSTICO)
        o.cambiar_estado(EstadoOrden.NO_REPARABLE)
        self.assertEqual(o.estado, EstadoOrden.NO_REPARABLE)

    def test_transicion_invalida(self):
        with self.assertRaises(TransicionInvalidaError):
            nueva_orden().cambiar_estado(EstadoOrden.REPARADO)

    def test_no_reparable_es_final(self):
        o = nueva_orden()
        o.cambiar_estado(EstadoOrden.EN_DIAGNOSTICO)
        o.cambiar_estado(EstadoOrden.NO_REPARABLE)
        with self.assertRaises(TransicionInvalidaError):
            o.cambiar_estado(EstadoOrden.EN_REPARACION)

    def test_reparacion_requiere_diagnostico(self):
        o = nueva_orden()
        o.cambiar_estado(EstadoOrden.EN_DIAGNOSTICO)
        with self.assertRaises(TransicionInvalidaError):
            o.cambiar_estado(EstadoOrden.EN_REPARACION)

    def test_diagnostico_fuera_de_estado(self):
        with self.assertRaises(TransicionInvalidaError):
            nueva_orden().registrar_diagnostico("x", 10)

    def test_costo_negativo_o_no_numerico(self):
        o = nueva_orden()
        o.cambiar_estado(EstadoOrden.EN_DIAGNOSTICO)
        with self.assertRaises(ValidacionError):
            o.registrar_diagnostico("x", -5)
        with self.assertRaises(ValidacionError):
            o.registrar_diagnostico("x", "abc")

    def test_entrega_solo_si_reparado(self):
        with self.assertRaises(TransicionInvalidaError):
            nueva_orden().registrar_entrega()

    def test_entregado_no_por_cambiar_estado(self):
        o = nueva_orden()
        for est in (EstadoOrden.EN_DIAGNOSTICO,):
            o.cambiar_estado(est)
        o.registrar_diagnostico("ok", 10)
        o.cambiar_estado(EstadoOrden.EN_REPARACION)
        o.cambiar_estado(EstadoOrden.REPARADO)
        with self.assertRaises(TransicionInvalidaError):
            o.cambiar_estado(EstadoOrden.ENTREGADO)


if __name__ == "__main__":
    unittest.main()