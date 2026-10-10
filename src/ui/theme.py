"""Tema visual y paleta ACDC para la ventana principal."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ACDCTheme:
    """Contiene los colores base y la configuración del estilo."""

    BG = "#061C2D"
    BG_LIGHT = "#0D2B42"
    PANEL = "#0B2238"
    NAVY = "#0F3557"
    BLUE = "#075D8C"
    BLUE_LIGHT = "#8FB0E0"
    CYAN = "#CFE6FF"
    ORANGE = "#FF8A3D"
    ORANGE_DARK = "#E96D22"
    WHITE = "#FFFFFF"
    MUTED = "#9DB7D2"
    SURFACE = "#DDEAF9"
    SUCCESS = "#1F9D75"
    DANGER = "#D94B4B"
    SHADOW = "#0A1D30"


def configurar_estilo(root: tk.Misc) -> None:
    """Configura ttk.Style con la identidad visual ACDC."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    colors = ACDCTheme()
    style.configure("TFrame", background=colors.SURFACE)
    style.configure("TLabel", background=colors.SURFACE, foreground=colors.BG)
    style.configure("Header.TLabel", background=colors.BG, foreground=colors.WHITE,
                    font=("Segoe UI", 18, "bold"))
    style.configure("Brand.TLabel", background=colors.BG, foreground=colors.BLUE_LIGHT,
                    font=("Segoe UI", 18, "bold"))
    style.configure("Title.TLabel", background=colors.SURFACE, foreground=colors.BG,
                    font=("Segoe UI", 22, "bold"))
    style.configure("Subtitle.TLabel", background=colors.SURFACE, foreground=colors.BG_LIGHT,
                    font=("Segoe UI", 10, "normal"))

    style.configure("Accent.TButton",
                    background=colors.ORANGE,
                    foreground=colors.WHITE,
                    font=("Segoe UI", 10, "bold"),
                    padding=(14, 8),
                    borderwidth=0)
    style.map("Accent.TButton",
              background=[("active", colors.ORANGE_DARK), ("pressed", colors.ORANGE_DARK)])

    style.configure("Primary.TButton",
                    background=colors.BLUE,
                    foreground=colors.WHITE,
                    font=("Segoe UI", 10, "bold"),
                    padding=(12, 8),
                    borderwidth=0)
    style.map("Primary.TButton",
              background=[("active", colors.NAVY), ("pressed", colors.NAVY)])

    style.configure("Secondary.TButton",
                    background=colors.WHITE,
                    foreground=colors.BG,
                    font=("Segoe UI", 10, "bold"),
                    padding=(10, 7),
                    borderwidth=0)

    style.configure("Card.TFrame", background=colors.WHITE)
    style.configure("Nav.TButton",
                    background=colors.BG_LIGHT,
                    foreground=colors.WHITE,
                    font=("Segoe UI", 10, "bold"),
                    padding=(14, 10),
                    borderwidth=0)
    style.map("Nav.TButton",
              background=[("active", colors.BLUE), ("selected", colors.BLUE), ("pressed", colors.BLUE)])

    style.configure("Panel.TLabelframe", background=colors.WHITE, foreground=colors.BG)
    style.configure("Panel.TLabelframe.Label", background=colors.WHITE, foreground=colors.BG,
                    font=("Segoe UI", 10, "bold"))

    style.configure("TEntry",
                    fieldbackground=colors.WHITE,
                    foreground=colors.BG,
                    bordercolor=colors.BLUE_LIGHT,
                    lightcolor=colors.BLUE_LIGHT,
                    darkcolor=colors.BLUE_LIGHT)

    style.configure("TCombobox",
                    fieldbackground=colors.WHITE,
                    foreground=colors.BG,
                    bordercolor=colors.BLUE_LIGHT)

    style.configure("Treeview", background=colors.WHITE, foreground=colors.BG,
                    fieldbackground=colors.WHITE, rowheight=28)
    style.map("Treeview", background=[("selected", colors.BLUE_LIGHT)])
    style.configure("Treeview.Heading", background=colors.BG_LIGHT, foreground=colors.WHITE,
                    font=("Segoe UI", 9, "bold"))
    style.map("Treeview.Heading", background=[("active", colors.BLUE)])