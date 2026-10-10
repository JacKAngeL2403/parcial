# 🏗️ Arquitectura — ACDC Service Manager

El sistema usa una **arquitectura por capas**. Cada capa solo conoce a la que tiene debajo, así que la interfaz nunca toca los archivos JSON ni las reglas del negocio directamente.

## 1. Capas del sistema

| Capa | Carpeta | Qué hace |
|---|---|---|
| **Interfaz** | `src/ui/` | Ventana Tkinter, formularios, tabla reutilizable y consola (CLI). |
| **Servicios** | `src/services/` | `AppService` (casos de uso) y `DataManager` (lectura/escritura de JSON). |
| **Dominio** | `src/domain/` | Entidades `Cliente`, `Equipo`, `OrdenServicio`, estados y excepciones. |
| **Datos** | `data/` | Archivos `clientes.json`, `equipos.json` y `ordenes.json`. |

```mermaid
flowchart TB
    UI["Interfaz<br/>VentanaPrincipal · Frames · CLI"]
    SV["Servicios<br/>AppService"]
    DM["Persistencia<br/>DataManager"]
    DO["Dominio<br/>Cliente · Equipo · OrdenServicio"]
    JS[("JSON<br/>data/")]

    UI --> SV
    SV --> DO
    SV --> DM
    DM --> JS
```

## 2. Flujo de estados de una orden

```mermaid
stateDiagram-v2
    [*] --> RECIBIDO
    RECIBIDO --> EN_DIAGNOSTICO
    EN_DIAGNOSTICO --> EN_REPARACION: con diagnóstico y costo
    EN_DIAGNOSTICO --> NO_REPARABLE
    EN_REPARACION --> REPARADO
    REPARADO --> ENTREGADO: registrar_entrega()
    NO_REPARABLE --> [*]
    ENTREGADO --> [*]
```

## 3. Diagramas de clases

Para que se lean bien, el diagrama está dividido en tres: **dominio**, **servicios** e **interfaz**.

### 3.1 Dominio

`OrdenServicio` guarda el id del cliente y del equipo (no los objetos), por eso las relaciones van punteadas.

```mermaid
classDiagram
    direction LR

    class EstadoOrden {
        <<enumeration>>
        RECIBIDO
        EN_DIAGNOSTICO
        EN_REPARACION
        REPARADO
        NO_REPARABLE
        ENTREGADO
    }

    class Cliente {
        -id_cliente
        -nombre
        -telefono
        -correo
    }

    class Equipo {
        -id_equipo
        -cliente_id
        -tipo
        -marca
        -modelo
        -falla_reportada
    }

    class OrdenServicio {
        -id_orden
        -cliente_id
        -equipo_id
        -fecha
        -diagnostico
        -costo
        -estado
        -fecha_entrega
        +puede_pasar_a(nuevo) bool
        +cambiar_estado(nuevo)
        +registrar_diagnostico(texto, costo)
        +registrar_entrega(fecha)
    }

    Cliente "1" <.. "0..*" Equipo : cliente_id
    Cliente "1" <.. "0..*" OrdenServicio : cliente_id
    Equipo "1" <.. "0..*" OrdenServicio : equipo_id
    OrdenServicio --> EstadoOrden : estado
```

**Excepciones** (todas heredan de `ACDCError`, así la interfaz captura un solo tipo de error):

```mermaid
classDiagram
    direction LR
    ACDCError <|-- ValidacionError
    ACDCError <|-- EntidadNoEncontradaError
    ACDCError <|-- TransicionInvalidaError
```

### 3.2 Servicios y persistencia

```mermaid
classDiagram
    direction LR

    class AppService {
        +registrar_cliente()
        +actualizar_cliente()
        +eliminar_cliente()
        +buscar_cliente()
        +registrar_equipo()
        +actualizar_equipo()
        +eliminar_equipo()
        +buscar_equipo()
        +crear_orden()
        +registrar_diagnostico()
        +actualizar_estado()
        +registrar_entrega()
        +buscar_orden()
        +estadisticas()
    }

    class DataManager {
        +cargar_clientes()
        +guardar_clientes()
        +cargar_equipos()
        +guardar_equipos()
        +cargar_ordenes()
        +guardar_ordenes()
    }

    class Entidades {
        <<Cliente · Equipo · OrdenServicio>>
    }

    AppService --> DataManager : guarda y carga con
    AppService ..> Entidades : crea y valida
    DataManager ..> Entidades : convierte JSON ↔ objetos
```

### 3.3 Interfaz

```mermaid
classDiagram
    direction TB

    class VentanaPrincipal {
        +show_page(nombre)
    }
    class ClientesFrame
    class EquiposFrame
    class OrdenesFrame
    class DiagnosticoFrame
    class EntregaFrame
    class Tabla {
        +cargar(filas)
        +seleccionado()
    }
    class CLI {
        +ejecutar()
    }
    class AppService

    VentanaPrincipal *-- ClientesFrame
    VentanaPrincipal *-- EquiposFrame
    VentanaPrincipal *-- OrdenesFrame
    VentanaPrincipal *-- DiagnosticoFrame
    VentanaPrincipal *-- EntregaFrame

    ClientesFrame ..> Tabla : usa
    EquiposFrame ..> Tabla : usa
    OrdenesFrame ..> Tabla : usa
    DiagnosticoFrame ..> Tabla : usa
    EntregaFrame ..> Tabla : usa

    VentanaPrincipal ..> AppService : usa
    CLI ..> AppService : usa
```

> Los cinco frames y la `CLI` reciben el mismo `AppService`; por claridad solo se dibuja la flecha de `VentanaPrincipal` y `CLI`.

## 4. Decisiones de diseño

- **Encapsulamiento:** las entidades guardan sus datos en atributos privados y los exponen con `@property`. Todas las validaciones están en el constructor.
- **Una sola puerta de entrada:** la interfaz solo habla con `AppService`.
- **Persistencia aislada:** únicamente `DataManager` lee y escribe JSON. Cambiar el formato no afecta al resto.
- **Excepciones propias:** `ACDCError` y sus hijas permiten mostrar mensajes claros sin que la ventana se cierre.
- **Dos interfaces, un mismo servicio:** `python -m src.main` abre la GUI y `python -m src.main --cli` abre la consola.
