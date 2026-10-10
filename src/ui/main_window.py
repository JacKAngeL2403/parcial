"""Ventana principal de ACDC SERVICE MANAGER."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from .forms import (ClientesFrame, DiagnosticoFrame, EntregaFrame, EquiposFrame,
                    OrdenesFrame)
from .theme import ACDCTheme, configurar_estilo


class VentanaPrincipal(tk.Tk):
    """Ventana principal con navegación lateral y pantallas del MVP."""

    def __init__(self, app_service: Any) -> None:
        super().__init__()
        self.app_service = app_service
        self.title("ACDC SERVICE MANAGER")
        self.geometry("1120x700")
        self.minsize(980, 620)
        self.configure(bg=ACDCTheme.BG)
        configurar_estilo(self)

        self._build_topbar()
        self._build_navigation()
        self._build_content()
        self._build_pages()
        self._current_page = "inicio"
        self.show_page("inicio")

    def _build_topbar(self) -> None:
        topbar = tk.Frame(self, bg=ACDCTheme.BG, height=72)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        brand = tk.Label(topbar, text="ACDC", bg=ACDCTheme.BG, fg=ACDCTheme.BLUE_LIGHT,
                         font=("Segoe UI", 24, "bold"), padx=18, pady=12)
        brand.pack(side="left")

        title = tk.Label(topbar, text="Service Manager",
                         bg=ACDCTheme.BG, fg=ACDCTheme.WHITE, font=("Segoe UI", 16, "bold"))
        title.pack(side="left", padx=(0, 12))

        subtitle = tk.Label(topbar, text="APLICACIÓN DE ESCRITORIO • MVP",
                            bg=ACDCTheme.BG, fg=ACDCTheme.MUTED, font=("Segoe UI", 10, "bold"))
        subtitle.pack(side="right", padx=18, pady=18)

    def _build_navigation(self) -> None:
        nav = tk.Frame(self, bg=ACDCTheme.BG_LIGHT, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        self.nav_buttons: dict[str, ttk.Button] = {}
        for idx, name in enumerate(["inicio", "clientes", "equipos", "nueva orden", "órdenes", "entrega"]):
            btn = ttk.Button(nav, text=name.upper(), style="Nav.TButton",
                             command=lambda page=name: self.show_page(page))
            btn.pack(side="left", padx=(12, 0), pady=(8, 8))
            self.nav_buttons[name] = btn

    def _build_content(self) -> None:
        self.content = tk.Frame(self, bg=ACDCTheme.SURFACE)
        self.content.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _build_pages(self) -> None:
        self.pages = {
            "inicio": self._crear_home_page(),
            "clientes": ClientesFrame(self.content, self.app_service),
            "equipos": EquiposFrame(self.content, self.app_service),
            "nueva orden": OrdenesFrame(self.content, self.app_service),
            "órdenes": DiagnosticoFrame(self.content, self.app_service),
            "entrega": EntregaFrame(self.content, self.app_service),
        }
        self.pages["órdenes"].refrescar()
        self.pages["entrega"].refrescar()

    def _crear_home_page(self) -> tk.Frame:
        frame = tk.Frame(self.content, bg=ACDCTheme.SURFACE)

        hero = tk.Frame(frame, bg=ACDCTheme.WHITE, bd=0, highlightthickness=0)
        hero.pack(fill="x", padx=18, pady=(18, 10))

        title = tk.Label(hero, text="ACDC\nDiagnostica. Repara. Entrega.",
                         bg=ACDCTheme.WHITE, fg=ACDCTheme.BG,
                         font=("Segoe UI", 26, "bold"), justify="left", anchor="w")
        title.pack(anchor="w", padx=20, pady=(20, 10))

        text = (
            "ACDC Service Manager registra clientes, equipos y órdenes de servicio, "
            "y permite seguir cada reparación hasta la entrega."
        )
        tk.Label(hero, text=text, bg=ACDCTheme.WHITE, fg=ACDCTheme.BG_LIGHT,
                 font=("Segoe UI", 11), justify="left", wraplength=720,
                 anchor="w").pack(anchor="w", padx=20, pady=(0, 20))

        actions = tk.Frame(hero, bg=ACDCTheme.WHITE)
        actions.pack(anchor="w", padx=20, pady=(0, 22))
        ttk.Button(actions, text="NUEVA ORDEN", style="Accent.TButton",
                   command=lambda: self.show_page("nueva orden")).pack(side="left", padx=(0, 10))
        ttk.Button(actions, text="CONSULTAR ÓRDENES", style="Primary.TButton",
                   command=lambda: self.show_page("órdenes")).pack(side="left")

        stats_frame = tk.Frame(frame, bg=ACDCTheme.SURFACE)
        stats_frame.pack(fill="x", padx=18, pady=(5, 8))
        self.stat_labels = {}
        for idx, label in enumerate(["CLIENTES REGISTRADOS", "EQUIPOS REGISTRADOS",
                                     "ESTADOS DE SERVICIO", "DATOS GUARDADOS"]):
            card = tk.Frame(stats_frame, bg=ACDCTheme.WHITE, width=220, height=132)
            card.grid(row=0, column=idx, padx=8, pady=6, sticky="nsew")
            card.grid_propagate(False)
            title_label = tk.Label(card, text=label, bg=ACDCTheme.WHITE,
                                   fg=ACDCTheme.BG_LIGHT, font=("Segoe UI", 9, "bold"))
            title_label.pack(anchor="w", padx=16, pady=(16, 6))
            value = tk.Label(card, text="0", bg=ACDCTheme.WHITE, fg=ACDCTheme.BG,
                             font=("Segoe UI", 20, "bold"))
            value.pack(anchor="w", padx=16)
            self.stat_labels[label] = value

        footer = tk.Frame(frame, bg=ACDCTheme.SURFACE)
        footer.pack(fill="x", padx=18, pady=(10, 0))
        info = tk.Label(footer, text="Órdenes activas: 0   •   Órdenes totales: 0",
                        bg=ACDCTheme.SURFACE, fg=ACDCTheme.BG_LIGHT,
                        font=("Segoe UI", 11, "bold"))
        info.pack(anchor="w")
        self.home_summary = info

        return frame

    def show_page(self, page_name: str) -> None:
        for name, frame in self.pages.items():
            if hasattr(frame, "refrescar"):
                frame.refrescar()
            frame.pack_forget()

        if page_name in self.pages:
            self.pages[page_name].pack(fill="both", expand=True)
            self._current_page = page_name

        self._refresh_home_stats()

    def _refresh_home_stats(self) -> None:
        stats = self.app_service.estadisticas()
        self.stat_labels["CLIENTES REGISTRADOS"].config(text=str(stats["clientes_totales"]))
        self.stat_labels["EQUIPOS REGISTRADOS"].config(text=str(stats["equipos_totales"]))
        self.stat_labels["ESTADOS DE SERVICIO"].config(
            text=str(len(self.app_service.listar_estados())))
        self.stat_labels["DATOS GUARDADOS"].config(text="JSON")
        self.home_summary.config(
            text=(
                f"Órdenes activas: {stats['ordenes_activas']}   •   "
                f"Órdenes totales: {stats['ordenes_totales']}"
            )
        )


def iniciar_gui(app_service: Any) -> None:
    VentanaPrincipal(app_service).mainloop()
