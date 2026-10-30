# Diagrama UML final — TP Integrador POO

```mermaid
classDiagram
    class Exportable {
        <<Protocol>>
        +exportar() str
    }

    class Figura {
        <<abstract>>
        +nombre str
        +color str
        +area()* float
    }

    class Poligono {
        <<abstract>>
        -_lados list~Lado~
        +lados_esperados()* int
        +perimetro() float
        +lados() tuple~Lado~
        +exportar() str
    }

    class Lado {
        -_longitud float
        -_etiqueta Etiqueta
        +longitud float
        +etiqueta Etiqueta
        +etiquetar(etiqueta) void
        +escalar(factor) void
    }

    class Etiqueta {
        <<frozen dataclass>>
        +texto str
    }

    class Taller {
        -_poligonos list~Poligono~
        +recibir(poligono) void
        +restaurar(poligono) Poligono
        +inventario() tuple~Poligono~
    }

    class Triangulo
    class Cuadrado
    class Pentagono
    class Hexagono

    class PlanoCAD {
        <<librería externa>>
        +identificador str
        +escala str
        +exportar() str
    }

    Figura <|-- Poligono : herencia
    Poligono <|-- Triangulo
    Poligono <|-- Cuadrado
    Poligono <|-- Pentagono
    Poligono <|-- Hexagono

    Poligono "1" *-- "3..*" Lado : composición
    Lado "1" --> "0..1" Etiqueta : asociación
    Taller "1" o-- "0..*" Poligono : agregación

    Poligono ..|> Exportable : cumple
    PlanoCAD ..|> Exportable : cumple sin heredar

    note for Poligono "crear_poligono_regular(cantidad, medida, ...)<br/>reemplaza a PoligonoRegular.<br/>Devuelve Triangulo, Cuadrado,<br/>Pentagono o Hexagono."
    note for Exportable "Contrato estructural: no exige herencia."
```

## Decisiones reflejadas

- `Figura` y `Poligono` son abstractas: `area()` y `lados_esperados()` son
  obligatorios. Instanciar `Poligono` falla al construir.
- `Poligono` compone sus `Lado` (los copia en el constructor) y `lados()`
  devuelve una tupla, no la lista interna.
- `Taller` agrega polígonos ya construidos; `inventario()` devuelve una tupla.
- `Lado` tiene una asociación opcional con `Etiqueta`; no la crea.
- `PoligonoRegular` no aparece como subclase: fue reemplazada por la fábrica
  `crear_poligono_regular()`.
- `Exportable` es un `Protocol`; `PlanoCAD` lo cumple sin heredar ni modificarse.
