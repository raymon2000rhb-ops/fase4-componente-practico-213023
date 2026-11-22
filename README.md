# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto correspondiente al **Componente Práctico (Fase 4)** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción General
Aplicación desarrollada en **Python 3** bajo el paradigma de **Programación Orientada a Objetos (POO)** sin uso de bases de datos. Gestiona en memoria (mediante objetos y listas internas) los clientes, servicios especializados y reservas de la empresa **Software FJ**, garantizando estabilidad y continuidad operativa mediante manejo avanzado de excepciones y registro persistente en archivo de logs (`eventos_software_fj.log`).

## Estructura del Proyecto
- `excepciones.py`: Jerarquía de excepciones personalizadas (`ErrorSistemaFJ`, `DatoInvalidoError`, `ServicioNoDisponibleError`, `OperacionNoPermitidaError`, `ReservaInvalidaError`, `CalculoInconsistenteError`).
- `logger_sistema.py`: Módulo de auditoría y registro de eventos/errores en archivo plano con manejo seguro de recursos (`try/except/finally`).
- `modelos.py`: Clases abstractas (`EntidadSistema`, `Servicio`), clase `Cliente` con encapsulación, tres servicios especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) con polimorfismo y sobrecarga funcional, y clase `Reserva` con encadenamiento de excepciones.
- `gestor_sistema.py`: Controlador de operaciones y listas internas con bloques `try/except/else/finally`.
- `main.py`: Script principal que simula 12 operaciones completas (válidas e inválidas) demostrando tolerancia a fallos.

## Ejecución
```bash
python main.py
```
