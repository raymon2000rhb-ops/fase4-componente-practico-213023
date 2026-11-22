"""
Módulo: gestor_sistema.py
Descripción: Controlador principal que administra las listas internas de clientes, servicios y reservas
de Software FJ sin bases de datos, integrando manejo avanzado de excepciones (try/except/else/finally)
y registro automático en el archivo de logs.
"""

from typing import Optional
from excepciones import ErrorSistemaFJ, DatoInvalidoError, ReservaInvalidaError
from logger_sistema import LoggerSistema
from modelos import Cliente, Servicio, Reserva


class GestorSoftwareFJ:
    """Clase coordinadora de operaciones del sistema Software FJ."""

    def __init__(self, ruta_log: str = "eventos_software_fj.log"):
        # Inicializa el sistema de logs en archivo plano
        self._logger = LoggerSistema(ruta_log)
        # Listas internas en memoria (reemplazan cualquier motor de base de datos)
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> Optional[Cliente]:
        """Crea y almacena un nuevo cliente validando duplicados y capturando errores de datos."""
        try:
            # Verifica que no exista otro cliente con el mismo ID
            if any(c.id_entidad == id_cliente for c in self._clientes):
                raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{id_cliente}'.")
            # Instancia el objeto Cliente (dispara validaciones en setters)
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSistemaFJ as err:
            # Registra la excepción controlada en el log y mantiene el programa activo
            self._logger.registrar_error("GestorSoftwareFJ.registrar_cliente", err)
            print(f"[ERROR CONTROLADO] Registro de cliente fallido -> {err}")
            return None
        else:
            # Si no hubo excepciones, agrega el cliente a la lista interna y registra éxito
            self._clientes.append(nuevo_cliente)
            self._logger.registrar_evento("INFO", f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        finally:
            # Bloque de auditoría que siempre se ejecuta al finalizar el intento
            self._logger.registrar_evento("AUDIT", f"Intento de registro de cliente procesado (ID: {id_cliente}).")

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Agrega un servicio especializado al catálogo interno validando unicidad."""
        try:
            # Valida que no exista un servicio duplicado por ID
            if any(s.id_entidad == servicio.id_entidad for s in self._servicios):
                raise DatoInvalidoError(f"El servicio con ID '{servicio.id_entidad}' ya está registrado.")
            # Verifica integridad del objeto Servicio
            if not servicio.validar_integridad():
                raise DatoInvalidoError("El servicio no cumple con las reglas de integridad.")
        except ErrorSistemaFJ as err:
            self._logger.registrar_error("GestorSoftwareFJ.registrar_servicio", err)
            print(f"[ERROR CONTROLADO] Registro de servicio fallido -> {err}")
            return False
        else:
            self._servicios.append(servicio)
            self._logger.registrar_evento("INFO", f"Servicio agregado al catálogo: {servicio.obtener_resumen()}")
            print(f"[OK] {servicio.obtener_resumen()}")
            return True

    def crear_reserva(
        self,
        id_reserva: str,
        cliente: Optional[Cliente],
        servicio: Optional[Servicio],
        duracion_horas: int,
        descuento: Optional[float] = None,
    ) -> Optional[Reserva]:
        """Crea una reserva vinculando cliente y servicio con manejo de excepciones encadenadas."""
        try:
            # Verifica duplicidad de ID de reserva
            if any(r.id_entidad == id_reserva for r in self._reservas):
                raise ReservaInvalidaError(f"Ya existe una reserva con el ID '{id_reserva}'.")
            # Crea la instancia de Reserva (puede lanzar ReservaInvalidaError o ServicioNoDisponibleError)
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion_horas, descuento)
        except ErrorSistemaFJ as err:
            # Registra tanto el error principal como la excepción encadenada (__cause__)
            self._logger.registrar_error("GestorSoftwareFJ.crear_reserva", err)
            causa_msg = f" (Causa: {err.__cause__})" if err.__cause__ else ""
            print(f"[ERROR CONTROLADO] Reserva fallida -> {err}{causa_msg}")
            return None
        else:
            self._reservas.append(nueva_reserva)
            self._logger.registrar_evento("INFO", f"Reserva creada: {nueva_reserva.obtener_resumen()}")
            print(f"[OK] {nueva_reserva.obtener_resumen()}")
            return nueva_reserva

    def ejecutar_accion_reserva(self, reserva: Optional[Reserva], accion: str) -> None:
        """Ejecuta confirmar, procesar o cancelar sobre una reserva protegiendo el flujo ante estados inválidos."""
        try:
            if reserva is None:
                raise ReservaInvalidaError("No se puede operar sobre una reserva inexistente (None).")
            # Selecciona la operación solicitada
            accion_norm = accion.strip().lower()
            if accion_norm == "confirmar":
                reserva.confirmar()
            elif accion_norm == "procesar":
                monto = reserva.procesar()
                self._logger.registrar_evento("INFO", f"Facturación generada para {reserva.id_entidad}: ${monto:,.2f}")
            elif accion_norm == "cancelar":
                reserva.cancelar()
            else:
                raise DatoInvalidoError(f"Acción de reserva desconocida: '{accion}'.")
        except ErrorSistemaFJ as err:
            self._logger.registrar_error(f"GestorSoftwareFJ.ejecutar_accion_reserva({accion})", err)
            print(f"[ERROR CONTROLADO] Acción '{accion}' rechazada -> {err}")
        else:
            self._logger.registrar_evento("INFO", f"Acción '{accion}' ejecutada sobre {reserva.id_entidad}. Nuevo estado: {reserva.estado}")
            print(f"[OK] Acción '{accion}' aplicada -> {reserva.obtener_resumen()}")

    def mostrar_resumen_general(self) -> None:
        """Imprime en consola el consolidado de entidades almacenadas en memoria."""
        print("\n" + "=" * 80)
        print("RESUMEN GENERAL DEL SISTEMA - SOFTWARE FJ")
        print(f"Total Clientes activos : {len(self._clientes)}")
        print(f"Total Servicios activos: {len(self._servicios)}")
        print(f"Total Reservas en lista: {len(self._reservas)}")
        print("=" * 80)
