"""DataManager: único componente que lee y escribe archivos JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from ..domain.exceptions import ACDCError
from ..domain.models import Cliente, Equipo, EstadoOrden, OrdenServicio


class DataManager:
    """Persistencia en data/clientes.json, equipos.json y ordenes.json."""

    def __init__(self, carpeta: Optional[str | Path] = None) -> None:
        raiz = Path(__file__).resolve().parents[2]
        self._carpeta = Path(carpeta) if carpeta else raiz / "data"
        self._carpeta.mkdir(parents=True, exist_ok=True)
        for nombre in ("clientes", "equipos", "ordenes"):
            archivo = self._ruta(nombre)
            if not archivo.exists():
                archivo.write_text("[]", encoding="utf-8")

    def _ruta(self, nombre: str) -> Path:
        return self._carpeta / f"{nombre}.json"

    def _leer(self, nombre: str) -> list[dict[str, Any]]:
        try:
            datos = json.loads(self._ruta(nombre).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ACDCError(f"El archivo {nombre}.json está dañado.") from exc
        return datos if isinstance(datos, list) else []

    def _escribir(self, nombre: str, datos: list[dict[str, Any]]) -> None:
        self._ruta(nombre).write_text(
            json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- clientes ----
    def cargar_clientes(self) -> list[Cliente]:
        return [Cliente(d["id_cliente"], d["nombre"], d["telefono"], d["correo"])
                for d in self._leer("clientes")]

    def guardar_clientes(self, clientes: list[Cliente]) -> None:
        self._escribir("clientes", [
            {"id_cliente": c.id_cliente, "nombre": c.nombre,
             "telefono": c.telefono, "correo": c.correo} for c in clientes])

    # ---- equipos ----
    def cargar_equipos(self) -> list[Equipo]:
        return [Equipo(d["id_equipo"], d["cliente_id"], d["tipo"], d["marca"],
                       d["modelo"], d["falla_reportada"]) for d in self._leer("equipos")]

    def guardar_equipos(self, equipos: list[Equipo]) -> None:
        self._escribir("equipos", [
            {"id_equipo": e.id_equipo, "cliente_id": e.cliente_id, "tipo": e.tipo,
             "marca": e.marca, "modelo": e.modelo,
             "falla_reportada": e.falla_reportada} for e in equipos])

    # ---- órdenes ----
    def cargar_ordenes(self) -> list[OrdenServicio]:
        return [OrdenServicio(
            d["id_orden"], d["cliente_id"], d["equipo_id"], d["falla_reportada"],
            fecha=d.get("fecha"), diagnostico=d.get("diagnostico"),
            costo=d.get("costo"), estado=EstadoOrden(d["estado"]),
            fecha_entrega=d.get("fecha_entrega")) for d in self._leer("ordenes")]

    def guardar_ordenes(self, ordenes: list[OrdenServicio]) -> None:
        self._escribir("ordenes", [
            {"id_orden": o.id_orden, "cliente_id": o.cliente_id,
             "equipo_id": o.equipo_id, "fecha": o.fecha,
             "falla_reportada": o.falla_reportada, "diagnostico": o.diagnostico,
             "costo": o.costo, "estado": o.estado.value,
             "fecha_entrega": o.fecha_entrega} for o in ordenes])
