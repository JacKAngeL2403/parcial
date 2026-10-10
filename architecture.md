## Diagrama de clases

```mermaid
classDiagram
    direction TB

    %% ---------- DOMINIO ----------
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
        -str _id_cliente
        -str _nombre
        -str _telefono
        -str _correo
        +id_cliente() str
        +nombre() str
        +telefono() str
        +correo() str
        +to_dict() dict
        +from_dict(datos) Cliente
    }

    class Equipo {
        -str _id_equipo
        -str _cliente_id
        -str _tipo
        -str _marca
        -str _modelo
        -str _falla_reportada
        +id_equipo() str
        +cliente_id() str
        +tipo() str
        +marca() str
        +modelo() str
        +falla_reportada() str
        +to_dict() dict
        +from_dict(datos) Equipo
    }

    class OrdenServicio {
        -str _id_orden
        -str _cliente_id
        -str _equipo_id
        -str _fecha
        -str _falla_reportada
        -str _diagnostico
        -float _costo
        -EstadoOrden _estado
        -str _fecha_entrega
        +id_orden() str
        +estado() EstadoOrden
        +diagnostico() str
        +costo() float
        +fecha_entrega() str
        +puede_pasar_a(nuevo) bool
        +cambiar_estado(nuevo) void
        +registrar_diagnostico(texto, costo) void
        +registrar_entrega() void
        +to_dict() dict
        +from_dict(datos) OrdenServicio
    }

    class ACDCError {
        <<exception>>
    }
    class ValidacionError {
        <<exception>>
    }
    class EntidadNoEncontradaError {
        <<exception>>
    }
    class TransicionInvalidaError {
        <<exception>>
    }

    %% ---------- SERVICIOS ----------
    class DataManager {
        -Path ruta_datos
        +cargar_clientes() list~Cliente~
        +cargar_equipos() list~Equipo~
        +cargar_ordenes() list~OrdenServicio~
        +guardar_clientes(clientes) void
        +guardar_equipos(equipos) void
        +guardar_ordenes(ordenes) void
    }

    class AppService {
        -DataManager data_manager
        +registrar_cliente(nombre, telefono, correo) Cliente
        +actualizar_cliente(id, nombre, telefono, correo) Cliente
        +eliminar_cliente(id) void
        +buscar_cliente(texto) list~Cliente~
        +listar_clientes() list~Cliente~
        +registrar_equipo(cliente_id, tipo, marca, modelo, falla) Equipo
        +actualizar_equipo(id, cliente_id, tipo, marca, modelo, falla) Equipo
        +eliminar_equipo(id) void
        +buscar_equipo(texto) list~Equipo~
        +listar_equipos_de_cliente(cliente_id) list~Equipo~
        +crear_orden(cliente_id, equipo_id, falla) OrdenServicio
        +registrar_diagnostico(id_orden, diagnostico, costo) OrdenServicio
        +actualizar_estado(id_orden, estado) OrdenServicio
        +registrar_entrega(id_orden) OrdenServicio
        +buscar_orden(codigo, cliente, estado) list~OrdenServicio~
        +listar_ordenes() list~OrdenServicio~
        +listar_estados() list~str~
        +estadisticas() dict
    }

    %% ---------- INTERFAZ ----------
    class ACDCTheme {
        <<constantes>>
        BG
        BG_LIGHT
        SURFACE
        WHITE
        MUTED
    }

    class VentanaPrincipal {
        -AppService app_service
        -dict pages
        +show_page(nombre) void
        -_refresh_home_stats() void
    }

    class ClientesFrame
    class EquiposFrame
    class OrdenesFrame
    class DiagnosticoFrame
    class EntregaFrame
    class Tabla {
        +cargar(filas) void
        +seleccionado() tuple
    }
    class CLI {
        -AppService app
        +ejecutar() void
    }

    %% ---------- RELACIONES ----------
    ValidacionError --|> ACDCError
    EntidadNoEncontradaError --|> ACDCError
    TransicionInvalidaError --|> ACDCError

    OrdenServicio --> EstadoOrden : tiene estado
    Equipo "0..*" --> "1" Cliente : pertenece a
    OrdenServicio "0..*" --> "1" Cliente : solicitada por
    OrdenServicio "0..*" --> "1" Equipo : atiende

    OrdenServicio ..> ValidacionError : lanza
    OrdenServicio ..> TransicionInvalidaError : lanza
    AppService ..> EntidadNoEncontradaError : lanza

    AppService --> DataManager : persiste con
    AppService o-- Cliente
    AppService o-- Equipo
    AppService o-- OrdenServicio
    DataManager ..> Cliente : serializa
    DataManager ..> Equipo : serializa
    DataManager ..> OrdenServicio : serializa

    VentanaPrincipal --> AppService : usa
    VentanaPrincipal *-- ClientesFrame
    VentanaPrincipal *-- EquiposFrame
    VentanaPrincipal *-- OrdenesFrame
    VentanaPrincipal *-- DiagnosticoFrame
    VentanaPrincipal *-- EntregaFrame
    VentanaPrincipal ..> ACDCTheme : estilos
    ClientesFrame --> AppService
    EquiposFrame --> AppService
    OrdenesFrame --> AppService
    DiagnosticoFrame --> AppService
    EntregaFrame --> AppService
    ClientesFrame *-- Tabla
    EquiposFrame *-- Tabla
    OrdenesFrame *-- Tabla
    DiagnosticoFrame *-- Tabla
    EntregaFrame *-- Tabla
    CLI --> AppService : usa
```

**Lectura rápida del diagrama:**
- **Dominio:** `Cliente`, `Equipo` y `OrdenServicio` encapsulan sus datos. `EstadoOrden` controla el flujo de estados.
- **Servicios:** `AppService` es la única puerta de entrada para la interfaz, y `DataManager` es el único que toca los JSON.
- **Interfaz:** `VentanaPrincipal` contiene los cinco formularios, que comparten la clase `Tabla`. `CLI` es la alternativa en consola.
- **Excepciones:** las tres heredan de `ACDCError`.
