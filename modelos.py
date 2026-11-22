"""
Módulo: modelos.py
Descripción: Contiene la arquitectura orientada a objetos del sistema Software FJ:
- Clase abstracta EntidadSistema (abstracción base).
- Clase Cliente (encapsulación y validaciones estrictas).
- Clase abstracta Servicio y tres clases derivadas (ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
  con polimorfismo y sobrecarga de métodos mediante parámetros opcionales / despacho.
- Clase Reserva con ciclo de vida completo (pendiente, confirmada, procesada, cancelada).
"""

from abc import ABC, abstractmethod
from typing import Optional
from excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)


class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad identificable del sistema Software FJ."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena vacía
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise DatoInvalidoError("El identificador de la entidad no puede estar vacío.")
        # Encapsula el identificador único de la entidad
        self._id_entidad = id_entidad.strip()
        # Establece el estado activo por defecto
        self._activo = True

    @property
    def id_entidad(self) -> str:
        """Propiedad de solo lectura para obtener el ID de la entidad."""
        return self._id_entidad

    @property
    def activo(self) -> bool:
        """Propiedad que indica si la entidad se encuentra activa."""
        return self._activo

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Método abstracto obligatorio para validar las reglas de negocio de cada entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio que devuelve una descripción textual de la entidad."""
        pass


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Invoca al constructor de la clase abstracta EntidadSistema
        super().__init__(id_cliente)
        # Asigna atributos mediante setters encapsulados para aplicar validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Lista interna para almacenar el historial de IDs de reservas del cliente
        self._historial_reservas: list[str] = []

    @property
    def nombre(self) -> str:
        """Devuelve el nombre completo del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Devuelve el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida formato básico de correo electrónico antes de asignarlo."""
        if not valor or not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono de contacto del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga solo dígitos y tenga longitud mínima."""
        if not valor or not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) < 7:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}'. Debe contener al menos 7 dígitos numéricos.")
        self._telefono = valor.strip()

    def agregar_reserva_historial(self, id_reserva: str) -> None:
        """Registra el identificador de una reserva en la lista interna del cliente."""
        self._historial_reservas.append(id_reserva)

    def validar_integridad(self) -> bool:
        """Verifica que todos los atributos esenciales del cliente sean consistentes."""
        return bool(self._id_entidad and self._nombre and self._correo and self._telefono)

    def obtener_resumen(self) -> str:
        """Retorna una cadena descriptiva con los datos principales del cliente."""
        return f"Cliente [{self.id_entidad}] - {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


class Servicio(EntidadSistema, ABC):
    """Clase abstracta que modela un servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, disponible: bool = True):
        # Inicializa la clase padre EntidadSistema
        super().__init__(id_servicio)
        # Valida el nombre del servicio
        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        # Valida que la tarifa base sea un número positivo
        if not isinstance(tarifa_base_hora, (int, float)) or tarifa_base_hora <= 0:
            raise DatoInvalidoError(f"La tarifa base por hora debe ser mayor a 0 (recibido: {tarifa_base_hora}).")
        # Encapsula los atributos del servicio
        self._nombre = nombre.strip()
        self._tarifa_base_hora = float(tarifa_base_hora)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        """Devuelve el nombre comercial del servicio."""
        return self._nombre

    @property
    def tarifa_base_hora(self) -> float:
        """Devuelve la tarifa base por hora del servicio."""
        return self._tarifa_base_hora

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Permite habilitar o deshabilitar la disponibilidad del servicio."""
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> bool:
        """Método abstracto para validar reglas específicas de duración o uso del servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Método abstracto polimórfico que calcula el costo según el tipo de servicio."""
        pass

    def calcular_costo_total(
        self,
        duracion_horas: int,
        porcentaje_impuesto: float = 0.19,
        descuento: Optional[float] = None,
    ) -> float:
        """
        Método sobrecargado funcionalmente mediante parámetros opcionales:
        - Variante 1: calcular_costo_total(duracion) -> aplica IVA estándar (19%) sin descuento.
        - Variante 2: calcular_costo_total(duracion, impuesto) -> aplica impuesto personalizado.
        - Variante 3: calcular_costo_total(duracion, impuesto, descuento) -> aplica impuesto y descuento.
        """
        # Verifica que el servicio esté disponible antes de cotizar
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no se encuentra disponible.")
        # Ejecuta las validaciones polimórficas propias de cada subclase
        self.validar_parametros(duracion_horas)
        # Valida que el porcentaje de impuesto no sea negativo ni excesivo
        if porcentaje_impuesto < 0 or porcentaje_impuesto > 1:
            raise CalculoInconsistenteError(f"Porcentaje de impuesto inválido: {porcentaje_impuesto}.")
        # Calcula el subtotal llamando al método polimórfico de la subclase
        subtotal = self.calcular_costo_base(duracion_horas)
        # Aplica el descuento si fue suministrado
        if descuento is not None:
            if descuento < 0 or descuento >= subtotal:
                raise CalculoInconsistenteError(
                    f"El descuento ({descuento}) no puede ser negativo ni mayor o igual al subtotal ({subtotal})."
                )
            subtotal -= descuento
        # Calcula el total sumando el impuesto correspondiente
        total = round(subtotal * (1 + porcentaje_impuesto), 2)
        # Verificación final de consistencia matemática
        if total <= 0:
            raise CalculoInconsistenteError("El cálculo total arrojó un valor menor o igual a cero.")
        return total

    def validar_integridad(self) -> bool:
        """Valida que el servicio tenga nombre y tarifa positiva."""
        return bool(self._nombre and self._tarifa_base_hora > 0)

    def obtener_resumen(self) -> str:
        """Retorna la descripción general del servicio y su estado."""
        estado_txt = "Disponible" if self._disponible else "No disponible"
        return f"Servicio [{self.id_entidad}] {self.nombre} | Tarifa/h: ${self.tarifa_base_hora:,.2f} | Estado: {estado_txt}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, capacidad_personas: int, disponible: bool = True):
        # Inicializa atributos heredados de Servicio
        super().__init__(id_servicio, nombre, tarifa_base_hora, disponible)
        # Valida que la capacidad de personas sea al menos 2
        if not isinstance(capacidad_personas, int) or capacidad_personas < 2:
            raise DatoInvalidoError(f"La capacidad de la sala debe ser al menos de 2 personas (recibido: {capacidad_personas}).")
        self._capacidad_personas = capacidad_personas

    def validar_parametros(self, duracion_horas: int) -> bool:
        """Las salas requieren una reserva mínima de 1 hora y máxima de 12 horas continuas."""
        if not isinstance(duracion_horas, int) or duracion_horas < 1 or duracion_horas > 12:
            raise ReservaInvalidaError(
                f"Duración inválida para sala ({duracion_horas}h). Debe estar entre 1 y 12 horas."
            )
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Calcula el costo base de la sala; aplica un recargo del 10% si la capacidad supera 20 personas."""
        costo = self.tarifa_base_hora * duracion_horas
        # Si es un auditorio o sala grande (>20 personas), añade cargo logístico
        if self._capacidad_personas > 20:
            costo *= 1.10
        return round(costo, 2)

    def obtener_resumen(self) -> str:
        """Sobrescribe la descripción incluyendo la capacidad de la sala."""
        return f"{super().obtener_resumen()} | Tipo: Sala (Capacidad: {self._capacidad_personas} personas)"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos (portátiles, servidores, proyectores)."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, cantidad_unidades: int, disponible: bool = True):
        # Inicializa atributos heredados de Servicio
        super().__init__(id_servicio, nombre, tarifa_base_hora, disponible)
        # Valida que exista al menos 1 unidad del equipo
        if not isinstance(cantidad_unidades, int) or cantidad_unidades < 1:
            raise DatoInvalidoError(f"La cantidad de equipos debe ser al menos 1 (recibido: {cantidad_unidades}).")
        self._cantidad_unidades = cantidad_unidades

    def validar_parametros(self, duracion_horas: int) -> bool:
        """El alquiler de equipos requiere un mínimo de 2 horas."""
        if not isinstance(duracion_horas, int) or duracion_horas < 2:
            raise ReservaInvalidaError(
                f"El alquiler de equipos exige mínimo 2 horas (solicitado: {duracion_horas}h)."
            )
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Multiplica tarifa por hora, duración y cantidad de equipos solicitados."""
        costo = self.tarifa_base_hora * duracion_horas * self._cantidad_unidades
        return round(costo, 2)

    def obtener_resumen(self) -> str:
        """Sobrescribe la descripción incluyendo la cantidad de equipos."""
        return f"{super().obtener_resumen()} | Tipo: Alquiler Equipos ({self._cantidad_unidades} unds)"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría y asesoría técnica por expertos de Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base_hora: float, especialidad: str, disponible: bool = True):
        # Inicializa atributos heredados de Servicio
        super().__init__(id_servicio, nombre, tarifa_base_hora, disponible)
        # Valida que se especifique el área de especialidad
        if not especialidad or not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("Debe indicar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: int) -> bool:
        """Las asesorías especializadas permiten bloques entre 1 y 8 horas."""
        if not isinstance(duracion_horas, int) or duracion_horas < 1 or duracion_horas > 8:
            raise ReservaInvalidaError(
                f"Las asesorías deben durar entre 1 y 8 horas (solicitado: {duracion_horas}h)."
            )
        return True

    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Calcula el costo base sumando un honorario fijo de preparación técnica de $25,000 COP."""
        cargo_preparacion = 25000.0
        costo = (self.tarifa_base_hora * duracion_horas) + cargo_preparacion
        return round(costo, 2)

    def obtener_resumen(self) -> str:
        """Sobrescribe la descripción incluyendo el área de especialidad."""
        return f"{super().obtener_resumen()} | Tipo: Asesoría ({self._especialidad})"


class Reserva(EntidadSistema):
    """Integra Cliente, Servicio, duración y estado, gestionando confirmación, cancelación y procesamiento."""

    # Estados válidos del ciclo de vida de una reserva
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_PROCESADA = "PROCESADA"
    ESTADO_CANCELADA = "CANCELADA"

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int,
        descuento: Optional[float] = None,
    ):
        # Inicializa el ID de la reserva en EntidadSistema
        super().__init__(id_reserva)
        # Valida que el cliente sea una instancia válida de Cliente
        if not isinstance(cliente, Cliente) or not cliente.validar_integridad():
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")
        # Valida que el servicio sea una instancia válida de Servicio
        if not isinstance(servicio, Servicio) or not servicio.validar_integridad():
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")
        # Verifica disponibilidad del servicio al momento de reservar
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"No se puede reservar '{servicio.nombre}' porque no está disponible.")

        # Encapsula cliente, servicio y duración
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._descuento = descuento
        # Inicia en estado PENDIENTE
        self._estado = self.ESTADO_PENDIENTE

        # Calcula el costo total aplicando encadenamiento de excepciones si falla la cotización
        try:
            self._costo_total = self._servicio.calcular_costo_total(
                duracion_horas=self._duracion_horas,
                descuento=self._descuento,
            )
        except Exception as err:
            # Encadena la excepción original (raise ... from err) dentro de ReservaInvalidaError
            raise ReservaInvalidaError(
                f"Fallo al calcular el costo de la reserva '{id_reserva}' para el servicio '{servicio.nombre}'."
            ) from err

        # Vincula la reserva al historial interno del cliente
        self._cliente.agregar_reserva_historial(self.id_entidad)

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Devuelve el valor total calculado de la reserva."""
        return self._costo_total

    def confirmar(self) -> None:
        """Cambia el estado de la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != self.ESTADO_PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva '{self.id_entidad}' en estado '{self._estado}'."
            )
        self._estado = self.ESTADO_CONFIRMADA

    def cancelar(self) -> None:
        """Cancela la reserva siempre que no haya sido procesada previamente."""
        if self._estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva '{self.id_entidad}' porque ya fue PROCESADA."
            )
        if self._estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError(
                f"La reserva '{self.id_entidad}' ya se encuentra CANCELADA."
            )
        self._estado = self.ESTADO_CANCELADA

    def procesar(self) -> float:
        """Finaliza la ejecución del servicio reservado si está CONFIRMADA y retorna el monto facturado."""
        if self._estado != self.ESTADO_CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS. Estado actual de '{self.id_entidad}': '{self._estado}'."
            )
        self._estado = self.ESTADO_PROCESADA
        return self._costo_total

    def validar_integridad(self) -> bool:
        """Verifica que la reserva mantenga referencias válidas y costo positivo."""
        return self._cliente.validar_integridad() and self._servicio.validar_integridad() and self._costo_total > 0

    def obtener_resumen(self) -> str:
        """Retorna el detalle completo de la reserva."""
        return (
            f"Reserva [{self.id_entidad}] | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion_horas}h | "
            f"Total (IVA inc.): ${self._costo_total:,.2f} | Estado: {self._estado}"
        )
