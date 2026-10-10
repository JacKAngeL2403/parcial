"""AppService: casos de uso y punto único de acceso para la UI."""
from __future__ import annotations

from typing import Optional

from ..domain.exceptions import EntidadNoEncontradaError, ValidacionError
from ..domain.models import Cliente, Equipo, EstadoOrden, OrdenServicio
from .data_manager import DataManager


class AppService:
    """Orquesta la capa de Dominio y la persistencia con DataManager."""

    def __init__(self, data_manager: DataManager) -> None:
        """Inicializa los servicios cargando los datos persistidos."""
        self._dm = data_manager
        self._clientes = self._dm.cargar_clientes()
        self._equipos = self._dm.cargar_equipos()
        self._ordenes = self._dm.cargar_ordenes()

    # ---- Utilidades Internas ----
    @staticmethod
    def _siguiente_id(prefijo: str, existentes: list[str]) -> str:
        """Genera el siguiente identificador correlativo con formato PREFIJO-000."""
        numeros = [
            int(i.split("-")[1])
            for i in existentes
            if i.startswith(f"{prefijo}-") and i.split("-")[1].isdigit()
        ]
        return f"{prefijo}-{max(numeros, default=0) + 1:03d}"

    def _cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por su ID o lanza EntidadNoEncontradaError."""
        for c in self._clientes:
            if c.id_cliente == id_cliente:
                return c
        raise EntidadNoEncontradaError(f"No existe el cliente '{id_cliente}'.")

    def _equipo(self, id_equipo: str) -> Equipo:
        """Busca un equipo por su ID o lanza EntidadNoEncontradaError."""
        for e in self._equipos:
            if e.id_equipo == id_equipo:
                return e
        raise EntidadNoEncontradaError(f"No existe el equipo '{id_equipo}'.")

    def _orden(self, id_orden: str) -> OrdenServicio:
        """Busca una orden de servicio por su ID o lanza EntidadNoEncontradaError."""
        for o in self._ordenes:
            if o.id_orden == id_orden:
                return o
        raise EntidadNoEncontradaError(f"No existe la orden '{id_orden}'.")

    @staticmethod
    def _convertir_estado(texto: str) -> EstadoOrden:
        """Convierte una cadena de texto al Enum EstadoOrden correspondiente."""
        try:
            return EstadoOrden(str(texto).strip().upper())
        except ValueError:
            raise ValidacionError(f"Estado desconocido: '{texto}'.") from None

    # ---- Gestión de Clientes ----
    def registrar_cliente(self, nombre: str, telefono: str, correo: str) -> Cliente:
        """Registra un nuevo cliente y persiste el cambio."""
        nuevo = Cliente(
            self._siguiente_id("C", [c.id_cliente for c in self._clientes]),
            nombre,
            telefono,
            correo,
        )
        self._clientes.append(nuevo)
        self._dm.guardar_clientes(self._clientes)
        return nuevo

    def obtener_cliente(self, id_cliente: str) -> Cliente:
        """Obtiene un cliente específico por su ID."""
        return self._cliente(id_cliente)

    def listar_clientes(self) -> list[Cliente]:
        """Devuelve la lista general de clientes registrados."""
        return list(self._clientes)

    def buscar_cliente(self, texto: str) -> list[Cliente]:
        """Filtra clientes por coincidencia de texto en ID, nombre, teléfono o correo."""
        t = texto.strip().lower()
        return [
            c for c in self._clientes
            if t in c.id_cliente.lower()
            or t in c.nombre.lower()
            or t in c.telefono
            or t in c.correo.lower()
        ]

    def actualizar_cliente(
        self, id_cliente: str, nombre: str, telefono: str, correo: str
    ) -> Cliente:
        """Actualiza los datos de un cliente existente."""
        self._cliente(id_cliente)
        actualizado = Cliente(id_cliente, nombre, telefono, correo)
        for idx, item in enumerate(self._clientes):
            if item.id_cliente == id_cliente:
                self._clientes[idx] = actualizado
                break
        self._dm.guardar_clientes(self._clientes)
        return actualizado

    def eliminar_cliente(self, id_cliente: str) -> None:
        """Elimina un cliente y desvincula sus equipos y órdenes asociadas."""
        self._cliente(id_cliente)
        self._clientes = [c for c in self._clientes if c.id_cliente != id_cliente]
        self._equipos = [e for e in self._equipos if e.cliente_id != id_cliente]
        self._ordenes = [o for o in self._ordenes if o.cliente_id != id_cliente]
        self._dm.guardar_clientes(self._clientes)
        self._dm.guardar_equipos(self._equipos)
        self._dm.guardar_ordenes(self._ordenes)

    # ---- Gestión de Equipos ----
    def registrar_equipo(
        self, cliente_id: str, tipo: str, marca: str, modelo: str, falla_reportada: str
    ) -> Equipo:
        """Registra un equipo asociado a un cliente."""
        self._cliente(cliente_id)
        nuevo = Equipo(
            self._siguiente_id("E", [e.id_equipo for e in self._equipos]),
            cliente_id,
            tipo,
            marca,
            modelo,
            falla_reportada,
        )
        self._equipos.append(nuevo)
        self._dm.guardar_equipos(self._equipos)
        return nuevo

    def obtener_equipo(self, id_equipo: str) -> Equipo:
        """Obtiene un equipo por su ID."""
        return self._equipo(id_equipo)

    def listar_equipos(self) -> list[Equipo]:
        """Lista todos los equipos registrados en el sistema."""
        return list(self._equipos)

    def listar_equipos_de_cliente(self, cliente_id: str) -> list[Equipo]:
        """Filtra los equipos que pertenecen a un cliente específico."""
        return [e for e in self._equipos if e.cliente_id == cliente_id]

    def buscar_equipo(self, texto: str) -> list[Equipo]:
        """Busca equipos según coincidencia en sus atributos."""
        t = texto.strip().lower()
        return [
            e for e in self._equipos
            if t in e.id_equipo.lower()
            or t in e.tipo.lower()
            or t in e.marca.lower()
            or t in e.modelo.lower()
            or t in e.cliente_id.lower()
        ]

    def actualizar_equipo(
        self, id_equipo: str, cliente_id: str, tipo: str, marca: str, modelo: str, falla_reportada: str
    ) -> Equipo:
        """Actualiza la información técnica de un equipo."""
        self._cliente(cliente_id)
        self._equipo(id_equipo)
        actualizado = Equipo(id_equipo, cliente_id, tipo, marca, modelo, falla_reportada)
        for idx, item in enumerate(self._equipos):
            if item.id_equipo == id_equipo:
                self._equipos[idx] = actualizado
                break
        for ord_serv in self._ordenes:
            if ord_serv.equipo_id == id_equipo:
                ord_serv._cliente_id = cliente_id  # type: ignore[attr-defined]
        self._dm.guardar_equipos(self._equipos)
        self._dm.guardar_ordenes(self._ordenes)
        return actualizado

    def eliminar_equipo(self, id_equipo: str) -> None:
        """Elimina un equipo y sus órdenes de servicio en cascada."""
        self._equipo(id_equipo)
        self._equipos = [e for e in self._equipos if e.id_equipo != id_equipo]
        self._ordenes = [o for o in self._ordenes if o.equipo_id != id_equipo]
        self._dm.guardar_equipos(self._equipos)
        self._dm.guardar_ordenes(self._ordenes)

    # ---- Gestión de Órdenes ----
    def crear_orden(
        self, cliente_id: str, equipo_id: str, falla_reportada: str
    ) -> OrdenServicio:
        """Crea una nueva orden de servicio validando la pertenencia del equipo."""
        self._cliente(cliente_id)
        if self._equipo(equipo_id).cliente_id != cliente_id:
            raise ValidacionError("El equipo no pertenece al cliente seleccionado.")
        nueva = OrdenServicio(
            self._siguiente_id("OS", [o.id_orden for o in self._ordenes]),
            cliente_id,
            equipo_id,
            falla_reportada,
        )
        self._ordenes.append(nueva)
        self._dm.guardar_ordenes(self._ordenes)
        return nueva

    def actualizar_orden(
        self,
        id_orden: str,
        cliente_id: Optional[str] = None,
        equipo_id: Optional[str] = None,
        falla_reportada: Optional[str] = None,
    ) -> OrdenServicio:
        """Actualiza los datos asociados a una orden existente."""
        orden = self._orden(id_orden)
        nuevo_cliente = cliente_id or orden.cliente_id
        nuevo_equipo = equipo_id or orden.equipo_id
        nueva_falla = falla_reportada or orden.falla_reportada

        if nuevo_cliente and nuevo_equipo:
            self._cliente(nuevo_cliente)
            if self._equipo(nuevo_equipo).cliente_id != nuevo_cliente:
                raise ValidacionError("El equipo no pertenece al cliente seleccionado.")

        orden._cliente_id = nuevo_cliente  # type: ignore[attr-defined]
        orden._equipo_id = nuevo_equipo  # type: ignore[attr-defined]
        orden._falla_reportada = nueva_falla  # type: ignore[attr-defined]
        self._dm.guardar_ordenes(self._ordenes)
        return orden

    def eliminar_orden(self, id_orden: str) -> None:
        """Elimina una orden de servicio."""
        self._orden(id_orden)
        self._ordenes = [o for o in self._ordenes if o.id_orden != id_orden]
        self._dm.guardar_ordenes(self._ordenes)

    def listar_ordenes(self) -> list[OrdenServicio]:
        """Lista todas las órdenes registradas."""
        return list(self._ordenes)

    def obtener_orden(self, id_orden: str) -> OrdenServicio:
        """Obtiene el detalle de una orden específica."""
        return self._orden(id_orden)

    def listar_estados(self) -> list[str]:
        """Retorna la lista de valores de los estados de orden válidos."""
        return [e.value for e in EstadoOrden]

    def buscar_orden(
        self,
        codigo: Optional[str] = None,
        cliente: Optional[str] = None,
        estado: Optional[str] = None,
    ) -> list[OrdenServicio]:
        """Filtra órdenes de servicio por código, cliente o estado del dominio."""
        resultado = list(self._ordenes)
        if codigo and codigo.strip():
            resultado = [o for o in resultado if codigo.strip().lower() in o.id_orden.lower()]
        if cliente and cliente.strip():
            t = cliente.strip().lower()
            ids = {
                c.id_cliente
                for c in self._clientes
                if t in c.id_cliente.lower() or t in c.nombre.lower()
            }
            resultado = [o for o in resultado if o.cliente_id in ids]
        if estado and estado.strip():
            est = self._convertir_estado(estado)
            resultado = [o for o in resultado if o.estado is est]
        return resultado

    def registrar_diagnostico(
        self, id_orden: str, diagnostico: str, costo: float
    ) -> OrdenServicio:
        """Registra el diagnóstico técnico y actualiza la orden a EN_DIAGNOSTICO."""
        orden = self._orden(id_orden)
        orden.registrar_diagnostico(diagnostico, costo)
        self._dm.guardar_ordenes(self._ordenes)
        return orden

    def actualizar_estado(self, id_orden: str, nuevo_estado: str) -> OrdenServicio:
        """Cambia el estado de una orden previa validación de la transición."""
        orden = self._orden(id_orden)
        orden.cambiar_estado(self._convertir_estado(nuevo_estado))
        self._dm.guardar_ordenes(self._ordenes)
        return orden

    def registrar_entrega(self, id_orden: str) -> OrdenServicio:
        """Registra la entrega final del equipo al cliente."""
        orden = self._orden(id_orden)
        orden.registrar_entrega()
        self._dm.guardar_ordenes(self._ordenes)
        return orden

    def estadisticas(self) -> dict[str, int]:
        """Calcula las métricas y resúmenes cuantitativos del sistema."""
        clientes_totales = len(self._clientes)
        equipos_totales = len(self._equipos)
        ordenes_totales = len(self._ordenes)
        ordenes_activas = sum(
            1 for o in self._ordenes
            if o.estado not in {EstadoOrden.ENTREGADO, EstadoOrden.NO_REPARABLE}
        )
        return {
            "clientes_totales": clientes_totales,
            "equipos_totales": equipos_totales,
            "ordenes_totales": ordenes_totales,
            "ordenes_activas": ordenes_activas,
            "ordenes_entregadas": sum(
                1 for o in self._ordenes if o.estado is EstadoOrden.ENTREGADO
            ),
            "ordenes_no_reparables": sum(
                1 for o in self._ordenes if o.estado is EstadoOrden.NO_REPARABLE
            ),
        }