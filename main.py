"""
Módulo: main.py
Descripción: Punto de entrada principal del Sistema Integral de Gestión de Clientes, Servicios y Reservas
para la empresa Software FJ (Curso Programación 213023 - UNAD).
Simula más de 12 operaciones completas (válidas e inválidas) demostrando estabilidad,
polimorfismo, sobrecarga y registro continuo en archivo de logs sin interrupciones.
"""

from excepciones import ErrorSistemaFJ
from gestor_sistema import GestorSoftwareFJ
from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


def ejecutar_simulacion() -> None:
    """Ejecuta de forma secuencial las operaciones de prueba requeridas por la guía."""
    print("=" * 80)
    print("INICIANDO SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 80)

    # Instancia el gestor principal creando el archivo de logs
    gestor = GestorSoftwareFJ("eventos_software_fj.log")

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de Cliente 1
    # -------------------------------------------------------------------------
    print("\n--- Operación 1: Registro válido de Cliente 1 ---")
    cliente_1 = gestor.registrar_cliente("CLI-001", "Laura Gómez", "laura.gomez@empresa.com", "3001234567")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de Cliente 2
    # -------------------------------------------------------------------------
    print("\n--- Operación 2: Registro válido de Cliente 2 ---")
    cliente_2 = gestor.registrar_cliente("CLI-002", "Carlos Mendoza", "cmendoza@techcol.co", "3159876543")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Registro inválido de Cliente (correo mal formado y teléfono corto)
    # -------------------------------------------------------------------------
    print("\n--- Operación 3: Registro inválido de Cliente (Datos erróneos) ---")
    gestor.registrar_cliente("CLI-003", "Andrés Ruiz", "andres_sin_arroba.com", "123")

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Registro inválido de Cliente (ID duplicado)
    # -------------------------------------------------------------------------
    print("\n--- Operación 4: Registro inválido de Cliente (ID duplicado) ---")
    gestor.registrar_cliente("CLI-001", "Duplicado Prueba", "duplicado@correo.com", "3015556677")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Creación válida de 3 Servicios Especializados (Polimorfismo)
    # -------------------------------------------------------------------------
    print("\n--- Operación 5: Creación válida de Servicios Especializados ---")
    sala_juntas = ReservaSala("SRV-001", "Sala Ejecutiva Norte", 80000.0, capacidad_personas=25, disponible=True)
    equipos_dev = AlquilerEquipo("SRV-002", "Workstation Dell Precision", 45000.0, cantidad_unidades=3, disponible=True)
    asesoria_cloud = AsesoriaEspecializada("SRV-003", "Arquitectura Cloud AWS", 120000.0, especialidad="Cloud Computing", disponible=True)
    servicio_inactivo = ReservaSala("SRV-004", "Auditorio Mantenimiento", 150000.0, capacidad_personas=40, disponible=False)

    gestor.registrar_servicio(sala_juntas)
    gestor.registrar_servicio(equipos_dev)
    gestor.registrar_servicio(asesoria_cloud)
    gestor.registrar_servicio(servicio_inactivo)

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Creación incorrecta de Servicio (tarifa negativa y capacidad inválida)
    # -------------------------------------------------------------------------
    print("\n--- Operación 6: Creación incorrecta de Servicio (Parámetros inválidos) ---")
    try:
        # Intenta instanciar una sala con tarifa negativa
        sala_erronea = ReservaSala("SRV-ERR", "Sala Inválida", -50000.0, capacidad_personas=1)
        gestor.registrar_servicio(sala_erronea)
    except ErrorSistemaFJ as err:
        # Registra el fallo directamente en el log del gestor sin detener la ejecución
        gestor._logger.registrar_error("main.Operacion6", err)
        print(f"[ERROR CONTROLADO] Creación de servicio bloqueada -> {err}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Reserva exitosa 1 (Sala Ejecutiva por 4 horas, sin descuento)
    # -------------------------------------------------------------------------
    print("\n--- Operación 7: Reserva exitosa de Sala Ejecutiva ---")
    reserva_1 = gestor.crear_reserva("RES-001", cliente_1, sala_juntas, duracion_horas=4)

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Reserva exitosa 2 (Alquiler de Equipos por 5 horas con descuento)
    # -------------------------------------------------------------------------
    print("\n--- Operación 8: Reserva exitosa de Alquiler de Equipos con descuento ---")
    reserva_2 = gestor.crear_reserva("RES-002", cliente_2, equipos_dev, duracion_horas=5, descuento=50000.0)

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa 3 (Asesoría Especializada por 3 horas)
    # -------------------------------------------------------------------------
    print("\n--- Operación 9: Reserva exitosa de Asesoría Especializada ---")
    reserva_3 = gestor.crear_reserva("RES-003", cliente_1, asesoria_cloud, duracion_horas=3)

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Reserva fallida por servicio no disponible
    # -------------------------------------------------------------------------
    print("\n--- Operación 10: Reserva fallida (Servicio no disponible) ---")
    gestor.crear_reserva("RES-004", cliente_2, servicio_inactivo, duracion_horas=2)

    # -------------------------------------------------------------------------
    # OPERACIÓN 11: Reserva fallida por duración fuera de rango (Encadenamiento de excepciones)
    # -------------------------------------------------------------------------
    print("\n--- Operación 11: Reserva fallida (Duración inválida -> Excepción encadenada) ---")
    gestor.crear_reserva("RES-005", cliente_1, equipos_dev, duracion_horas=1)

    # -------------------------------------------------------------------------
    # OPERACIÓN 12: Ciclo de vida de reservas (Confirmación, Procesamiento y Error de Estado)
    # -------------------------------------------------------------------------
    print("\n--- Operación 12: Confirmación, Procesamiento y Control de Operaciones Inválidas ---")
    # Confirmar y procesar reserva_1 correctamente
    gestor.ejecutar_accion_reserva(reserva_1, "confirmar")
    gestor.ejecutar_accion_reserva(reserva_1, "procesar")
    # Intentar cancelar una reserva que ya fue procesada (debe lanzar OperacionNoPermitidaError)
    gestor.ejecutar_accion_reserva(reserva_1, "cancelar")
    # Intentar procesar reserva_2 sin haberla confirmado primero (debe lanzar OperacionNoPermitidaError)
    gestor.ejecutar_accion_reserva(reserva_2, "procesar")
    # Confirmar y cancelar reserva_3 correctamente
    gestor.ejecutar_accion_reserva(reserva_3, "confirmar")
    gestor.ejecutar_accion_reserva(reserva_3, "cancelar")

    # Muestra resumen final en consola
    gestor.mostrar_resumen_general()
    print("Ejecución finalizada sin interrupciones. Revise 'eventos_software_fj.log' para ver la auditoría.")


if __name__ == "__main__":
    # Punto de arranque seguro de la aplicación
    ejecutar_simulacion()
