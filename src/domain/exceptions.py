"""Excepciones personalizadas del dominio."""


class ACDCError(Exception):
    """Excepción base del sistema; permite a la UI capturar errores controlados."""
    def __init__(self, mensaje: str = "Ha ocurrido un error en el sistema ACDC."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ValidacionError(ACDCError):
    """Datos inválidos en una entidad o parámetro."""
    def __init__(self, campo: str = "", mensaje_detalle: str = "Datos proporcionados no válidos."):
        self.campo = campo
        if campo:
            mensaje = f"Error de validación en el campo '{campo}': {mensaje_detalle}"
        else:
            mensaje = f"Error de validación: {mensaje_detalle}"
        super().__init__(mensaje)


class EntidadNoEncontradaError(ACDCError):
    """Cliente, equipo u orden inexistente."""
    def __init__(self, tipo_entidad: str = "Entidad", id_entidad: str = ""):
        self.tipo_entidad = tipo_entidad
        self.id_entidad = id_entidad
        if id_entidad:
            mensaje = f"{tipo_entidad} con ID '{id_entidad}' no fue encontrado(a)."
        else:
            mensaje = f"{tipo_entidad} no encontrado(a)."
        super().__init__(mensaje)


class TransicionInvalidaError(ACDCError):
    """Cambio de estado o entrega no permitidos."""
    def __init__(self, estado_origen: str = "", estado_destino: str = "", motivo: str = ""):
        self.estado_origen = estado_origen
        self.estado_destino = estado_destino
        
        if estado_origen and estado_destino:
            mensaje = f"Transición de estado no permitida de '{estado_origen}' a '{estado_destino}'."
        else:
            mensaje = "Transición o cambio de estado no permitido."
            
        if motivo:
            mensaje += f" Motivo: {motivo}"
            
        super().__init__(mensaje)
