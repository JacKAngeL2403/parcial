"""Interfaz CLI mínima; solo usa AppService."""
from __future__ import annotations

from typing import Any

from ..domain.exceptions import ACDCError

MENU = """
=== ACDC SERVICE MANAGER (CLI) ===
1. Registrar cliente      2. Listar clientes
3. Registrar equipo       4. Listar equipos
5. Crear orden            6. Listar órdenes
7. Registrar diagnóstico  8. Cambiar estado
9. Registrar entrega      0. Salir
"""


class CLI:
    def __init__(self, app: Any) -> None:
        self.app = app

    def _p(self, texto: str) -> str:
        return input(texto + ": ").strip()

    def _opcion(self, opcion: str) -> None:
        a = self.app
        if opcion == "1":
            c = a.registrar_cliente(self._p("Nombre"), self._p("Teléfono"), self._p("Correo"))
            print(f"Cliente {c.id_cliente} registrado.")
        elif opcion == "2":
            for c in a.listar_clientes():
                print(f"{c.id_cliente} | {c.nombre} | {c.telefono} | {c.correo}")
        elif opcion == "3":
            e = a.registrar_equipo(self._p("ID cliente"), self._p("Tipo"), self._p("Marca"),
                                   self._p("Modelo"), self._p("Falla"))
            print(f"Equipo {e.id_equipo} registrado.")
        elif opcion == "4":
            for e in a.listar_equipos():
                print(f"{e.id_equipo} | {e.cliente_id} | {e.tipo} {e.marca} {e.modelo} | {e.falla_reportada}")
        elif opcion == "5":
            o = a.crear_orden(self._p("ID cliente"), self._p("ID equipo"), self._p("Falla"))
            print(f"Orden {o.id_orden} creada ({o.estado.value}).")
        elif opcion == "6":
            for o in a.listar_ordenes():
                print(f"{o.id_orden} | {o.cliente_id} | {o.equipo_id} | {o.estado.value} | "
                      f"costo={o.costo} | entrega={o.fecha_entrega}")
        elif opcion == "7":
            id_orden = self._p("ID orden")
            diagnostico = self._p("Diagnóstico")
            try:
                costo = float(self._p("Costo"))
            except ValueError:
                return print("El costo debe ser numérico.")
            a.registrar_diagnostico(id_orden, diagnostico, costo)
            print("Diagnóstico registrado.")
        else:
            self._opcion_estado(opcion)

    def _opcion_estado(self, opcion: str) -> None:
        a = self.app
        if opcion == "8":
            print("Estados:", ", ".join(a.listar_estados()))
            o = a.actualizar_estado(self._p("ID orden"), self._p("Nuevo estado"))
            print(f"Orden {o.id_orden} ahora está {o.estado.value}.")
        elif opcion == "9":
            o = a.registrar_entrega(self._p("ID orden"))
            print(f"Orden {o.id_orden} entregada el {o.fecha_entrega}.")
        else:
            print("Opción no válida.")

    def ejecutar(self) -> None:
        while True:
            print(MENU)
            opcion = input("Opción: ").strip()
            if opcion == "0":
                print("Hasta luego.")
                return
            try:
                self._opcion(opcion)
            except ACDCError as exc:
                print(f"Error: {exc}")

