"""Widgets reutilizables de la GUI (solo presentación)."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable, Optional

from ..domain.exceptions import ACDCError  # única dependencia permitida hacia Domain


def mostrar_error(mensaje: str) -> None:
    messagebox.showerror("Error", mensaje)


def mostrar_info(mensaje: str) -> None:
    messagebox.showinfo("ACDC Service Manager", mensaje)


def ejecutar(accion: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[bool, Any]:
    """Ejecuta una acción del AppService mostrando errores controlados."""
    try:
        return True, accion(*args, **kwargs)
    except ACDCError as exc:
        mostrar_error(str(exc))
        return False, None


def crear_campos(parent: tk.Misc, campos: list[tuple[str, tk.StringVar]]) -> None:
    """Crea filas 'etiqueta + Entry' dentro de un contenedor."""
    for fila, (texto, variable) in enumerate(campos):
        ttk.Label(parent, text=texto).grid(row=fila, column=0, sticky="w", padx=4, pady=3)
        ttk.Entry(parent, textvariable=variable, width=40).grid(row=fila, column=1, padx=4, pady=3)


def etiqueta_cliente(c: Any) -> str:
    return f"{c.id_cliente} - {c.nombre}"


def etiqueta_equipo(e: Any) -> str:
    return f"{e.id_equipo} - {e.tipo} {e.marca} {e.modelo}"


def id_de_etiqueta(etiqueta: str) -> str:
    """Extrae el ID de una etiqueta 'ID - descripción'."""
    return etiqueta.split(" - ")[0].strip()


def fila_orden(o: Any) -> tuple:
    costo = "" if o.costo is None else f"{o.costo:.2f}"
    return (o.id_orden, o.cliente_id, o.equipo_id, o.fecha, o.estado.value,
            o.diagnostico or "", costo, o.fecha_entrega or "")


COLUMNAS_ORDEN = [("Orden", 70), ("Cliente", 70), ("Equipo", 70), ("Fecha", 90),
                  ("Estado", 120), ("Diagnóstico", 200), ("Costo", 70), ("Entrega", 90)]


def texto_orden(o: Any) -> str:
    costo = "-" if o.costo is None else f"S/ {o.costo:.2f}"
    return (f"Orden {o.id_orden} | Cliente {o.cliente_id} | Equipo {o.equipo_id}\n"
            f"Fecha: {o.fecha} | Estado: {o.estado.value} | Costo: {costo}\n"
            f"Falla: {o.falla_reportada}\nDiagnóstico: {o.diagnostico or '-'}\n"
            f"Entrega: {o.fecha_entrega or '-'}")


class Tabla(ttk.Frame):
    """Treeview con scrollbar."""

    def __init__(self, parent: tk.Misc, columnas: list[tuple[str, int]], altura: int = 8) -> None:
        super().__init__(parent)
        nombres = [c for c, _ in columnas]
        self.tree = ttk.Treeview(self, columns=nombres, show="headings", height=altura)
        for nombre, ancho in columnas:
            self.tree.heading(nombre, text=nombre)
            self.tree.column(nombre, width=ancho, anchor="w")
        barra = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=barra.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def cargar(self, filas: list[tuple]) -> None:
        self.tree.delete(*self.tree.get_children())
        for fila in filas:
            self.tree.insert("", "end", values=fila)

    def seleccionado(self) -> Optional[tuple]:
        seleccion = self.tree.selection()
        return tuple(self.tree.item(seleccion[0], "values")) if seleccion else None