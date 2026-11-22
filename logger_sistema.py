"""
Módulo: logger_sistema.py
Descripción: Gestiona el registro persistente de eventos y errores en un archivo de texto plano (logs),
sin utilizar bases de datos, cumpliendo con los requisitos del sistema Software FJ.
"""

from datetime import datetime


class LoggerSistema:
    """Clase encargada de escribir eventos operativos y excepciones en un archivo de logs."""

    def __init__(self, ruta_archivo: str = "eventos_software_fj.log"):
        # Define la ruta del archivo donde se almacenarán los registros
        self._ruta_archivo = ruta_archivo
        # Registra el inicio de sesión del sistema en el archivo de logs
        self.registrar_evento("INFO", "Sistema de registro de logs inicializado correctamente.")

    def registrar_evento(self, nivel: str, mensaje: str) -> None:
        """Escribe una línea formateada con fecha y hora en el archivo de logs."""
        # Obtiene la marca de tiempo actual en formato ISO legible
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye la línea de registro estandarizada
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
        # Utiliza bloque try/except/finally para asegurar el cierre correcto del archivo
        archivo = None
        try:
            # Abre el archivo en modo 'append' (agregar al final) con codificación UTF-8
            archivo = open(self._ruta_archivo, mode="a", encoding="utf-8")
            # Escribe la línea en el archivo
            archivo.write(linea)
        except OSError as error_io:
            # Si falla la escritura en disco, informa en consola sin detener el programa
            print(f"[ADVERTENCIA LOG] No se pudo escribir en el archivo de logs: {error_io}")
        finally:
            # Garantiza que el descriptor de archivo se cierre si fue abierto
            if archivo is not None and not archivo.closed:
                archivo.close()

    def registrar_error(self, origen: str, excepcion: Exception) -> None:
        """Registra detalladamente una excepción capturada, incluyendo su causa encadenada si existe."""
        # Construye el mensaje principal con el tipo de excepción y su texto
        detalle = f"Origen: {origen} | Tipo: {type(excepcion).__name__} | Detalle: {excepcion}"
        # Verifica si existe una excepción encadenada (__cause__)
        if excepcion.__cause__ is not None:
            # Añade la información de la causa original al registro
            detalle += f" | Causa original: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}"
        # Delega la escritura al método registrar_evento con nivel ERROR
        self.registrar_evento("ERROR", detalle)
