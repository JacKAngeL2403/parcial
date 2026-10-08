"""Entidades del dominio del taller de servicios técnicos.

Representa los principales elementos del negocio: clientes, equipos,
órdenes de servicio y el flujo de estados que sigue cada reparación.
"""
from __future__ import annotations

import re
from datetime import date
from enum import Enum
from typing import Optional

from .exceptions import TransicionInvalidaError, ValidacionError

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _texto_obligatorio(valor: object, campo: str) -> str:
    """Valida que el valor sea texto no vacío y lo normaliza."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValidacionError(f"El campo '{campo}' es obligatorio y no puede quedar vacío.")
    return valor.strip()


class EstadoOrden(Enum):
    """Estados permitidos en el ciclo de vida de una orden de servicio."""

    RECIBIDO = "RECIBIDO"
    EN_DIAGNOSTICO = "EN_DIAGNOSTICO"
    EN_REPARACION = "EN_REPARACION"
    REPARADO = "REPARADO"
    NO_REPARABLE = "NO_REPARABLE"
    ENTREGADO = "ENTREGADO"


TRANSICIONES: dict[EstadoOrden, set[EstadoOrden]] = {
    EstadoOrden.RECIBIDO: {EstadoOrden.EN_DIAGNOSTICO},
    EstadoOrden.EN_DIAGNOSTICO: {EstadoOrden.EN_REPARACION, EstadoOrden.NO_REPARABLE},
    EstadoOrden.EN_REPARACION: {EstadoOrden.REPARADO},
    EstadoOrden.REPARADO: {EstadoOrden.ENTREGADO},
    EstadoOrden.NO_REPARABLE: set(),
    EstadoOrden.ENTREGADO: set(),
}


class Cliente:
    """Representa a un cliente registrado en el sistema."""

    def __init__(self, id_cliente: str, nombre: str, telefono: str, correo: str) -> None:
        self._id_cliente = _texto_obligatorio(id_cliente, "id_cliente")
        self._nombre = _texto_obligatorio(nombre, "nombre")
        self._telefono = self._validar_telefono(telefono)
        self._correo = self._validar_correo(correo)

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        telefono = _texto_obligatorio(telefono, "teléfono")
        if not telefono.isdigit() or not 6 <= len(telefono) <= 15:
            raise ValidacionError(
                "El teléfono debe contener únicamente números y tener entre 6 y 15 dígitos."
            )
        return telefono

    @staticmethod
    def _validar_correo(correo: str) -> str:
        correo = _texto_obligatorio(correo, "correo")
        if not _PATRON_CORREO.match(correo):
            raise ValidacionError("El correo ingresado no tiene un formato válido.")
        return correo

    @property
    def id_cliente(self) -> str:
        return self._id_cliente

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def correo(self) -> str:
        return self._correo

    def __str__(self) -> str:
        return f"Cliente {self._id_cliente}: {self._nombre}"


class Equipo:
    """Representa un equipo que llega al taller para revisión o reparación."""

    def __init__(self, id_equipo: str, cliente_id: str, tipo: str, marca: str,
                 modelo: str, falla_reportada: str) -> None:
        self._id_equipo = _texto_obligatorio(id_equipo, "id_equipo")
        self._cliente_id = _texto_obligatorio(cliente_id, "cliente_id")
        self._tipo = _texto_obligatorio(tipo, "tipo")
        self._marca = _texto_obligatorio(marca, "marca")
        self._modelo = _texto_obligatorio(modelo, "modelo")
        self._falla_reportada = _texto_obligatorio(falla_reportada, "falla reportada")

    @property
    def id_equipo(self) -> str:
        return self._id_equipo

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def marca(self) -> str:
        return self._marca

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def falla_reportada(self) -> str:
        return self._falla_reportada

    def __str__(self) -> str:
        return f"Equipo {self._id_equipo}: {self._tipo} {self._marca} {self._modelo}"


class OrdenServicio:
    """Representa la orden de servicio asociada a un cliente y a un equipo."""

    def __init__(self, id_orden: str, cliente_id: str, equipo_id: str,
                 falla_reportada: str, fecha: Optional[str] = None,
                 diagnostico: Optional[str] = None, costo: Optional[float] = None,
                 estado: EstadoOrden = EstadoOrden.RECIBIDO,
                 fecha_entrega: Optional[str] = None) -> None:
        if not isinstance(estado, EstadoOrden):
            raise ValidacionError("El estado ingresado no es válido.")
        self._id_orden = _texto_obligatorio(id_orden, "id_orden")
        self._cliente_id = _texto_obligatorio(cliente_id, "cliente_id")
        self._equipo_id = _texto_obligatorio(equipo_id, "equipo_id")
        self._falla_reportada = _texto_obligatorio(falla_reportada, "falla reportada")
        self._fecha = fecha or date.today().isoformat()
        self._diagnostico = diagnostico
        self._costo = None if costo is None else self._validar_costo(costo)
        self._estado = estado
        self._fecha_entrega = fecha_entrega

    @staticmethod
    def _validar_costo(costo: object) -> float:
        if isinstance(costo, bool):
            raise ValidacionError("El costo debe ser un valor numérico válido.")
        try:
            valor = float(costo)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            raise ValidacionError("El costo debe ser un valor numérico válido.") from None
        if valor < 0:
            raise ValidacionError("El costo no puede ser un valor negativo.")
        return valor

    @property
    def id_orden(self) -> str:
        return self._id_orden

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @property
    def equipo_id(self) -> str:
        return self._equipo_id

    @property
    def fecha(self) -> str:
        return self._fecha

    @property
    def falla_reportada(self) -> str:
        return self._falla_reportada

    @property
    def diagnostico(self) -> Optional[str]:
        return self._diagnostico

    @property
    def costo(self) -> Optional[float]:
        return self._costo

    @property
    def estado(self) -> EstadoOrden:
        return self._estado

    @property
    def fecha_entrega(self) -> Optional[str]:
        return self._fecha_entrega

    def __str__(self) -> str:
        return f"Orden {self._id_orden} - Estado: {self._estado.value}"

    def puede_pasar_a(self, nuevo_estado: EstadoOrden) -> bool:
        """Verifica si la transición de estado es válida según el flujo del taller."""
        return nuevo_estado in TRANSICIONES[self._estado]

    def registrar_diagnostico(self, diagnostico: str, costo: float) -> None:
        """Registra el diagnóstico y el costo asociado; solo en EN_DIAGNOSTICO."""
        if self._estado is not EstadoOrden.EN_DIAGNOSTICO:
            raise TransicionInvalidaError(
                "El diagnóstico solo puede registrarse cuando la orden está en estado EN_DIAGNOSTICO."
            )
        texto = _texto_obligatorio(diagnostico, "diagnóstico")
        self._costo = self._validar_costo(costo)
        self._diagnostico = texto

    def cambiar_estado(self, nuevo_estado: EstadoOrden) -> None:
        """Cambia el estado respetando las reglas de negocio definidas por el taller."""
        if nuevo_estado is EstadoOrden.ENTREGADO:
            raise TransicionInvalidaError(
                "La entrega debe registrarse con 'registrar_entrega', no cambiando el estado directamente."
            )
        if not self.puede_pasar_a(nuevo_estado):
            raise TransicionInvalidaError(
                f"No es posible cambiar de {self._estado.value} a {nuevo_estado.value}."
            )
        if nuevo_estado is EstadoOrden.EN_REPARACION and (
                self._diagnostico is None or self._costo is None):
            raise TransicionInvalidaError(
                "Para pasar a EN_REPARACION se requiere un diagnóstico y un costo registrados."
            )
        self._estado = nuevo_estado

    def registrar_entrega(self, fecha: Optional[str] = None) -> None:
        """Registra la entrega final; solo se permite cuando la orden está REPARADO."""
        if self._estado is not EstadoOrden.REPARADO:
            raise TransicionInvalidaError(
                "Solo se puede entregar una orden que esté en estado REPARADO."
            )
        self._estado = EstadoOrden.ENTREGADO
        self._fecha_entrega = fecha or date.today().isoformat()

