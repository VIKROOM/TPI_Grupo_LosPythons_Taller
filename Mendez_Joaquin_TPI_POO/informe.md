# Informe — TP Integrador Unidad 3

## 1. Los 8 java-ismos

| # | Java-ismo | Dónde (partida) | Inversión | Síntoma |
|---|---|---|---|---|
| 1 | Getters/setters sin lógica | `Figura.getNombre` (28), `getLongitud` (43), `getLados` (84) | Atributo público; `@property` solo con lógica | Ceremonia sin efecto |
| 2 | `_` como `private` | `_nombre`/`_longitud` (23, 40) | Convención, no protección | `p._nombre` se modifica |
| 3 | `__init__` solo asigna; sin `super()` | (22-25, 58-64) | `@dataclass`/`super()` | `_construida` no existe |
| 4 | Atributo de clase mutable | `catalogo = []` (55) | `static` → instancia/registro | Lista compartida |
| 5 | Defaults mutables | `lados=[], observaciones=[]` (58) | `None`/`default_factory` | Observaciones compartidas |
| 6 | `for` + acumulador | `perimetro` (71-75) | `sum(generador)` | Traducción literal |
| 7 | Type hint mentiroso | `area() -> int` devuelve `str` (78) | Verificación estática | `type()` es `str` |
| 8 | Sobrecarga `*args`/`isinstance` | `Triangulo`/`Cuadrado` (91-110) | Defaults + `@classmethod` | `Triangulo("x","y")` vacío |

## 2. Equivalencias sobre mi código

| Java | Mi Python | ¿Directa o rediseño? | Por qué |
|---|---|---|---|
| `private` + getters/setters | Atributos públicos; `Lado.longitud` con `@property` | Rediseño | Property solo donde valida |
| Campos `List` en constructor | Copia en `Poligono.__init__` (`figuras.py:149`); `default_factory` | Rediseño | Evita alias y defaults compartidos |
| `interface` + `implements` | `Protocol` (`figuras.py:48`) | Rediseño | `PlanoCAD` cumple sin heredar |
| `abstract class` | `ABC` + `@abstractmethod` (`figuras.py:119,136`) | Directa con matiz | Falla temprana explícita |
| Constructores sobrecargados | `@classmethod desde_lados()`/`regular()` | Rediseño | Python no sobrecarga por firma |

## 3. Las tres relaciones

La sintaxis `self._algo = algo` es idéntica; cambia quién construye y controla el ciclo de vida:

- **Composición `Poligono—Lado`:** `Poligono.__init__` copia los lados (`figuras.py:149`); `lados()` devuelve una tupla (`figuras.py:178`). El `Lado` no tiene dueño externo.
- **Agregación `Taller—Poligono`:** `recibir()` solo agrega la referencia (`figuras.py:339`); el taller no construye el polígono y `restaurar()` lo devuelve. `inventario()` devuelve una tupla (`figuras.py:353`).
- **Asociación `Lado—Etiqueta`:** `etiquetar()` asigna una etiqueta externa (`figuras.py:94`); el lado no la crea. `Etiqueta` es `frozen=True` (`figuras.py:59`).

## 4. `PoligonoRegular`

Se elimina como subclase y se reemplaza por `crear_poligono_regular()` (`figuras.py:309`), que devuelve `Triangulo`, `Cuadrado`, `Pentagono` o `Hexagono`. La herencia original existía para tener un tipo común en una lista: necesidad de Java que en Python no existe. El dominio ya tiene las subclases concretas. `Poligono` es ABC: instanciarlo sin `lados_esperados()` lanza `TypeError` al construir.

## 5. ABC vs. Protocol

`Exportable` es `Protocol` porque `PlanoCAD` ya tiene `exportar()` y no hereda de nada nuestro; una ABC exigiría herencia o `register()` y no se puede modificar la librería. `exportar_todo()` (`figuras.py:367`) mezcla polígonos y planos CAD.

La elección no la decide el lenguaje: **la decide el dominio**. “Es-un” con comportamiento compartido → ABC/herencia (`Figura → Poligono`); “sabe hacer” → `Protocol` (`Exportable`).

## 6. Cierre

Cambió el mecanismo (convención, `@property` con lógica, `@dataclass`, `ABC`/`Protocol`, composición explícita); se mantuvo el dominio (`Figura`, `Poligono`, `Lado`, subclases, perímetro, área y relaciones). El diseño de objetos es el mismo; cambia cómo se expresa y cómo se hacen cumplir los contratos.
