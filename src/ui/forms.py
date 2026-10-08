"""Formularios (pestañas) de la GUI. Solo usan AppService; sin reglas de negocio."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any

from .widgets import (COLUMNAS_ORDEN, Tabla, crear_campos, ejecutar, etiqueta_cliente,
                      etiqueta_equipo, fila_orden, id_de_etiqueta, mostrar_error,
                      mostrar_info, texto_orden)


def _correo_basico(correo: str) -> bool:
    return "@" in correo and "." in correo.split("@")[-1]


class ClientesFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, app: Any) -> None:
        super().__init__(parent, padding=10)
        self.app = app
        self.id_actual = ""
        self.v_nombre, self.v_tel, self.v_correo = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.v_buscar = tk.StringVar()
        form = ttk.LabelFrame(self, text="Registrar cliente", padding=8)
        form.pack(fill="x")
        crear_campos(form, [("Nombre", self.v_nombre), ("Teléfono", self.v_tel),
                            ("Correo", self.v_correo)])
        botones = ttk.Frame(form)
        botones.grid(row=3, column=1, sticky="w", pady=4)
        ttk.Button(botones, text="Guardar", command=self.guardar).pack(side="left", padx=2)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=2)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=2)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=2)
        busq = ttk.LabelFrame(self, text="Buscar clientes", padding=8)
        busq.pack(fill="x", pady=6)
        ttk.Entry(busq, textvariable=self.v_buscar, width=40).pack(side="left", padx=4)
        ttk.Button(busq, text="Buscar", command=self.buscar).pack(side="left", padx=2)
        ttk.Button(busq, text="Ver todos", command=self.refrescar).pack(side="left", padx=2)
        self.tabla = Tabla(self, [("ID", 80), ("Nombre", 220), ("Teléfono", 110), ("Correo", 220)])
        self.tabla.pack(fill="both", expand=True)
        self.tabla.tree.bind("<<TreeviewSelect>>", lambda _e: self._seleccionar())

    def limpiar(self) -> None:
        self.id_actual = ""
        for v in (self.v_nombre, self.v_tel, self.v_correo):
            v.set("")

    def _seleccionar(self) -> None:
        fila = self.tabla.seleccionado()
        if not fila:
            return
        self.id_actual = fila[0]
        self.v_nombre.set(fila[1])
        self.v_tel.set(fila[2])
        self.v_correo.set(fila[3])

    def guardar(self) -> None:
        nombre, tel, correo = self.v_nombre.get().strip(), self.v_tel.get().strip(), self.v_correo.get().strip()
        if not nombre or not tel or not correo:
            return mostrar_error("Complete nombre, teléfono y correo.")
        if not _correo_basico(correo):
            return mostrar_error("Ingrese un correo con formato válido.")
        if self.id_actual:
            ok, c = ejecutar(self.app.actualizar_cliente, self.id_actual, nombre, tel, correo)
            if ok:
                mostrar_info(f"Cliente {c.id_cliente} actualizado correctamente.")
        else:
            ok, c = ejecutar(self.app.registrar_cliente, nombre, tel, correo)
            if ok:
                mostrar_info(f"Cliente {c.id_cliente} registrado correctamente.")
        if ok:
            self.limpiar()
            self.refrescar()

    def actualizar(self) -> None:
        self.guardar()

    def eliminar(self) -> None:
        if not self.id_actual:
            return mostrar_error("Seleccione un cliente para eliminar.")
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el cliente {self.id_actual}?"):
            return
        ok, _ = ejecutar(self.app.eliminar_cliente, self.id_actual)
        if ok:
            mostrar_info(f"Cliente {self.id_actual} eliminado.")
            self.limpiar()
            self.refrescar()

    def registrar(self) -> None:
        self.guardar()

    def buscar(self) -> None:
        self._mostrar(self.app.buscar_cliente(self.v_buscar.get()))

    def _mostrar(self, clientes: list) -> None:
        self.tabla.cargar([(c.id_cliente, c.nombre, c.telefono, c.correo) for c in clientes])

    def refrescar(self) -> None:
        self._mostrar(self.app.listar_clientes())


class EquiposFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, app: Any) -> None:
        super().__init__(parent, padding=10)
        self.app = app
        self.id_actual = ""
        self.v_cliente, self.v_tipo = tk.StringVar(), tk.StringVar()
        self.v_marca, self.v_modelo = tk.StringVar(), tk.StringVar()
        self.v_falla, self.v_buscar = tk.StringVar(), tk.StringVar()
        form = ttk.LabelFrame(self, text="Registrar equipo", padding=8)
        form.pack(fill="x")
        ttk.Label(form, text="Cliente").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.combo = ttk.Combobox(form, textvariable=self.v_cliente, state="readonly", width=37)
        self.combo.grid(row=0, column=1, padx=4, pady=3)
        crear_campos_desde = [("Tipo de equipo", self.v_tipo), ("Marca", self.v_marca),
                              ("Modelo", self.v_modelo), ("Falla reportada", self.v_falla)]
        for i, (txt, var) in enumerate(crear_campos_desde, start=1):
            ttk.Label(form, text=txt).grid(row=i, column=0, sticky="w", padx=4, pady=3)
            ttk.Entry(form, textvariable=var, width=40).grid(row=i, column=1, padx=4, pady=3)
        botones = ttk.Frame(form)
        botones.grid(row=5, column=1, sticky="w", pady=4)
        ttk.Button(botones, text="Guardar", command=self.guardar).pack(side="left", padx=2)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=2)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=2)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=2)
        busq = ttk.LabelFrame(self, text="Buscar equipos", padding=8)
        busq.pack(fill="x", pady=6)
        ttk.Entry(busq, textvariable=self.v_buscar, width=40).pack(side="left", padx=4)
        ttk.Button(busq, text="Buscar", command=self.buscar).pack(side="left", padx=2)
        ttk.Button(busq, text="Ver todos", command=self.refrescar).pack(side="left", padx=2)
        self.tabla = Tabla(self, [("ID", 70), ("Cliente", 70), ("Tipo", 110), ("Marca", 110),
                                  ("Modelo", 110), ("Falla", 250)])
        self.tabla.pack(fill="both", expand=True)
        self.tabla.tree.bind("<<TreeviewSelect>>", lambda _e: self._seleccionar())

    def limpiar(self) -> None:
        self.id_actual = ""
        self.v_cliente.set("")
        for v in (self.v_tipo, self.v_marca, self.v_modelo, self.v_falla):
            v.set("")

    def _seleccionar(self) -> None:
        fila = self.tabla.seleccionado()
        if not fila:
            return
        self.id_actual = fila[0]
        self.v_cliente.set(etiqueta_cliente(self.app.obtener_cliente(fila[1])))
        self.v_tipo.set(fila[2])
        self.v_marca.set(fila[3])
        self.v_modelo.set(fila[4])
        self.v_falla.set(fila[5])

    def guardar(self) -> None:
        if not self.v_cliente.get():
            return mostrar_error("Seleccione un cliente.")
        datos = [v.get().strip() for v in (self.v_tipo, self.v_marca, self.v_modelo, self.v_falla)]
        if not all(datos):
            return mostrar_error("Complete tipo, marca, modelo y falla reportada.")
        cliente_id = id_de_etiqueta(self.v_cliente.get())
        if self.id_actual:
            ok, e = ejecutar(self.app.actualizar_equipo, self.id_actual, cliente_id, *datos)
            if ok:
                mostrar_info(f"Equipo {e.id_equipo} actualizado correctamente.")
        else:
            ok, e = ejecutar(self.app.registrar_equipo, cliente_id, *datos)
            if ok:
                mostrar_info(f"Equipo {e.id_equipo} registrado correctamente.")
        if ok:
            self.limpiar()
            self.refrescar()

    def actualizar(self) -> None:
        self.guardar()

    def eliminar(self) -> None:
        if not self.id_actual:
            return mostrar_error("Seleccione un equipo para eliminar.")
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el equipo {self.id_actual}?"):
            return
        ok, _ = ejecutar(self.app.eliminar_equipo, self.id_actual)
        if ok:
            mostrar_info(f"Equipo {self.id_actual} eliminado.")
            self.limpiar()
            self.refrescar()

    def registrar(self) -> None:
        self.guardar()

    def buscar(self) -> None:
        self._mostrar(self.app.buscar_equipo(self.v_buscar.get()))

    def _mostrar(self, equipos: list) -> None:
        self.tabla.cargar([(e.id_equipo, e.cliente_id, e.tipo, e.marca, e.modelo,
                            e.falla_reportada) for e in equipos])

    def refrescar(self) -> None:
        self.combo["values"] = [etiqueta_cliente(c) for c in self.app.listar_clientes()]
        self._mostrar(self.app.listar_equipos())


class OrdenesFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, app: Any) -> None:
        super().__init__(parent, padding=10)
        self.app = app
        self.v_cliente, self.v_equipo, self.v_falla = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.v_codigo, self.v_filtro_cli, self.v_filtro_est = tk.StringVar(), tk.StringVar(), tk.StringVar()
        form = ttk.LabelFrame(self, text="Crear orden de servicio", padding=8)
        form.pack(fill="x")
        ttk.Label(form, text="Cliente").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.c_cliente = ttk.Combobox(form, textvariable=self.v_cliente, state="readonly", width=37)
        self.c_cliente.grid(row=0, column=1, padx=4, pady=3)
        self.c_cliente.bind("<<ComboboxSelected>>", lambda _e: self._cargar_equipos())
        ttk.Label(form, text="Equipo").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.c_equipo = ttk.Combobox(form, textvariable=self.v_equipo, state="readonly", width=37)
        self.c_equipo.grid(row=1, column=1, padx=4, pady=3)
        ttk.Label(form, text="Falla reportada").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        ttk.Entry(form, textvariable=self.v_falla, width=40).grid(row=2, column=1, padx=4, pady=3)
        ttk.Button(form, text="Crear orden", command=self.crear).grid(row=3, column=1, sticky="w", pady=4)
        filtros = ttk.LabelFrame(self, text="Consultar órdenes", padding=8)
        filtros.pack(fill="x", pady=6)
        ttk.Label(filtros, text="Código").pack(side="left")
        ttk.Entry(filtros, textvariable=self.v_codigo, width=10).pack(side="left", padx=4)
        ttk.Label(filtros, text="Cliente").pack(side="left")
        ttk.Entry(filtros, textvariable=self.v_filtro_cli, width=16).pack(side="left", padx=4)
        ttk.Label(filtros, text="Estado").pack(side="left")
        self.c_estado = ttk.Combobox(filtros, textvariable=self.v_filtro_est, state="readonly", width=16)
        self.c_estado.pack(side="left", padx=4)
        ttk.Button(filtros, text="Buscar", command=self.buscar).pack(side="left", padx=2)
        ttk.Button(filtros, text="Limpiar filtros", command=self.refrescar).pack(side="left", padx=2)
        self.tabla = Tabla(self, COLUMNAS_ORDEN)
        self.tabla.pack(fill="both", expand=True)

    def _cargar_equipos(self) -> None:
        self.v_equipo.set("")
        cid = id_de_etiqueta(self.v_cliente.get())
        self.c_equipo["values"] = [etiqueta_equipo(e) for e in self.app.listar_equipos_de_cliente(cid)]

    def crear(self) -> None:
        if not self.v_cliente.get() or not self.v_equipo.get():
            return mostrar_error("Seleccione un cliente y un equipo.")
        if not self.v_falla.get().strip():
            return mostrar_error("Registre la falla reportada.")
        ok, o = ejecutar(self.app.crear_orden, id_de_etiqueta(self.v_cliente.get()),
                         id_de_etiqueta(self.v_equipo.get()), self.v_falla.get().strip())
        if ok:
            mostrar_info(f"Orden {o.id_orden} creada en estado {o.estado.value}.")
            self.v_falla.set("")
            self.refrescar()

    def buscar(self) -> None:
        ok, res = ejecutar(self.app.buscar_orden, self.v_codigo.get(),
                           self.v_filtro_cli.get(), self.v_filtro_est.get())
        if ok:
            self.tabla.cargar([fila_orden(o) for o in res])

    def refrescar(self) -> None:
        self.v_codigo.set("")
        self.v_filtro_cli.set("")
        self.v_filtro_est.set("")
        self.c_cliente["values"] = [etiqueta_cliente(c) for c in self.app.listar_clientes()]
        self.c_estado["values"] = [""] + self.app.listar_estados()
        self.tabla.cargar([fila_orden(o) for o in self.app.listar_ordenes()])


class DiagnosticoFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, app: Any) -> None:
        super().__init__(parent, padding=10)
        self.app = app
        self.v_info, self.v_costo, self.v_estado = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.id_orden = ""
        self.tabla = Tabla(self, COLUMNAS_ORDEN, altura=7)
        self.tabla.pack(fill="x")
        self.tabla.tree.bind("<<TreeviewSelect>>", lambda _e: self._seleccionar())
        ttk.Label(self, textvariable=self.v_info, justify="left").pack(anchor="w", pady=6)
        diag = ttk.LabelFrame(self, text="Diagnóstico y costo", padding=8)
        diag.pack(fill="x")
        ttk.Label(diag, text="Diagnóstico").grid(row=0, column=0, sticky="nw", padx=4)
        self.txt = tk.Text(diag, width=50, height=3)
        self.txt.grid(row=0, column=1, padx=4, pady=3)
        ttk.Label(diag, text="Costo (S/)").grid(row=1, column=0, sticky="w", padx=4)
        ttk.Entry(diag, textvariable=self.v_costo, width=15).grid(row=1, column=1, sticky="w", padx=4)
        ttk.Button(diag, text="Registrar diagnóstico", command=self.registrar).grid(
            row=2, column=1, sticky="w", pady=4)
        est = ttk.LabelFrame(self, text="Cambiar estado", padding=8)
        est.pack(fill="x", pady=6)
        self.combo = ttk.Combobox(est, textvariable=self.v_estado, state="readonly", width=22)
        self.combo.pack(side="left", padx=4)
        ttk.Button(est, text="Solicitar cambio", command=self.cambiar).pack(side="left", padx=4)

    def _seleccionar(self) -> None:
        fila = self.tabla.seleccionado()
        if fila:
            self.id_orden = fila[0]
            ok, o = ejecutar(self.app.obtener_orden, self.id_orden)
            if ok:
                self.v_info.set(texto_orden(o))

    def _requiere_orden(self) -> bool:
        if not self.id_orden:
            mostrar_error("Seleccione una orden de la tabla.")
            return False
        return True

    def registrar(self) -> None:
        if not self._requiere_orden():
            return
        diag = self.txt.get("1.0", "end").strip()
        if not diag:
            return mostrar_error("Escriba el diagnóstico.")
        try:
            costo = float(self.v_costo.get().replace(",", "."))
        except ValueError:
            return mostrar_error("El costo debe ser un número.")
        if costo < 0:
            return mostrar_error("El costo debe ser positivo.")
        ok, _ = ejecutar(self.app.registrar_diagnostico, self.id_orden, diag, costo)
        if ok:
            mostrar_info("Diagnóstico y costo registrados.")
            self._recargar()

    def cambiar(self) -> None:
        if not self._requiere_orden():
            return
        if not self.v_estado.get():
            return mostrar_error("Seleccione el nuevo estado.")
        ok, o = ejecutar(self.app.actualizar_estado, self.id_orden, self.v_estado.get())
        if ok:
            mostrar_info(f"La orden {o.id_orden} ahora está {o.estado.value}.")
            self._recargar()

    def _recargar(self) -> None:
        actual = self.id_orden
        self.refrescar()
        self.id_orden = actual
        ok, o = ejecutar(self.app.obtener_orden, actual)
        if ok:
            self.v_info.set(texto_orden(o))

    def refrescar(self) -> None:
        self.id_orden = ""
        self.v_info.set("Seleccione una orden de la tabla.")
        self.v_costo.set("")
        self.v_estado.set("")
        self.txt.delete("1.0", "end")
        self.combo["values"] = self.app.listar_estados()
        self.tabla.cargar([fila_orden(o) for o in self.app.listar_ordenes()])


class EntregaFrame(ttk.Frame):
    def __init__(self, parent: tk.Misc, app: Any) -> None:
        super().__init__(parent, padding=10)
        self.app = app
        self.v_info = tk.StringVar()
        self.id_orden = ""
        ttk.Label(self, text="Órdenes REPARADO listas para entrega").pack(anchor="w")
        self.tabla = Tabla(self, COLUMNAS_ORDEN, altura=8)
        self.tabla.pack(fill="x")
        self.tabla.tree.bind("<<TreeviewSelect>>", lambda _e: self._seleccionar())
        ttk.Label(self, textvariable=self.v_info, justify="left").pack(anchor="w", pady=8)
        ttk.Button(self, text="Confirmar entrega", command=self.entregar).pack(anchor="w")

    def _seleccionar(self) -> None:
        fila = self.tabla.seleccionado()
        if fila:
            self.id_orden = fila[0]
            ok, o = ejecutar(self.app.obtener_orden, self.id_orden)
            if ok:
                self.v_info.set(texto_orden(o))

    def entregar(self) -> None:
        if not self.id_orden:
            return mostrar_error("Seleccione una orden reparada.")
        if not messagebox.askyesno("Confirmar", f"¿Registrar la entrega de {self.id_orden}?"):
            return
        ok, o = ejecutar(self.app.registrar_entrega, self.id_orden)
        if ok:
            mostrar_info(f"Orden {o.id_orden} entregada el {o.fecha_entrega}.")
            self.refrescar()

    def refrescar(self) -> None:
        self.id_orden = ""
        self.v_info.set("Seleccione una orden de la tabla.")
        ok, res = ejecutar(self.app.buscar_orden, estado="REPARADO")
        self.tabla.cargar([fila_orden(o) for o in res] if ok else [])
