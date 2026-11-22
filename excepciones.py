"""
Módulo: excepciones.py
Descripción: Define la jerarquía de excepciones personalizadas para el Sistema Integral
de Gestión de Clientes, Servicios y Reservas de Software FJ.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base de la aplicación Software FJ para capturar errores del dominio."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-GEN-000"):
        # Almacena el mensaje descriptivo del error
        self.mensaje = mensaje
        # Almacena un código identificador único para trazabilidad en el log
        self.codigo_error = codigo_error
        # Llama al constructor de la clase padre Exception con formato estructurado
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados (nombre, correo, documento, valores) son inválidos o faltantes."""

    def __init__(self, mensaje: str):
        # Inicializa con código específico de validación de datos
        super().__init__(mensaje, codigo_error="ERR-VAL-001")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio no está disponible o no cumple condiciones de capacidad/estado."""

    def __init__(self, mensaje: str):
        # Inicializa con código específico de disponibilidad de servicio
        super().__init__(mensaje, codigo_error="ERR-SRV-002")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar ejecutar una acción inválida sobre el estado actual de una reserva o entidad."""

    def __init__(self, mensaje: str):
        # Inicializa con código específico de regla de negocio / operación no permitida
        super().__init__(mensaje, codigo_error="ERR-OPR-003")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un fallo al crear, confirmar, cancelar o procesar una reserva."""

    def __init__(self, mensaje: str):
        # Inicializa con código específico de gestión de reservas
        super().__init__(mensaje, codigo_error="ERR-RES-004")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo financiero (tarifa, impuesto, descuento) arroja un resultado incoherente."""

    def __init__(self, mensaje: str):
        # Inicializa con código específico de inconsistencia matemática o financiera
        super().__init__(mensaje, codigo_error="ERR-CAL-005")
