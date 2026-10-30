"""parte1_diagnostico.py — El dominio de partida, ya corregido.

Este archivo conserva los nombres del módulo original (Figura, Lado, Poligono,
Triangulo, Cuadrado, PoligonoRegular) para que se pueda comparar el antes y el
después. Las correcciones aplicadas son los 8 java-ismos de diseño de la Parte 1:

1. Getters/setters preventivos sin lógica -> atributos públicos; @property solo
   en Lado, donde hay validación real.
2. `_nombre`/`_longitud` no son private: se usan como convención, no como
   modificador de visibilidad.
3. `__init__` que solo asignaba campos y omitía super() -> @dataclass.
4. Atributo de clase mutable (`catalogo = []`) -> se elimina el registro global.
5. Argumentos por defecto mutables (`lados=[]`, `observaciones=[]`) ->
   field(default_factory=list).
6. Bucle for con acumulador en perimetro() -> sum() con generador.
7. Type hint mentiroso (`area() -> int` devolvía str) -> `area() -> float`.
8. Sobrecarga de constructor con *args/isinstance -> @classmethod desde_lados().

PoligonoRegular ya no se modela como subclase: en figuras.py se reemplaza por la
fábrica crear_poligono_regular(). Acá se usa la misma idea para el demo.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class Figura:
    nombre: str
    color: str

    def area(self) -> float:
        raise NotImplementedError("Cada figura concreta implementa area()")


class Lado:
    def __init__(self, longitud: float) -> None:
        self.longitud = longitud

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("La longitud debe ser numérica")
        longitud = float(valor)
        if not math.isfinite(longitud) or longitud <= 0:
            raise ValueError("La longitud debe ser positiva y finita")
        self._longitud = longitud

    def __repr__(self) -> str:
        return f"Lado({self._longitud:.2f})"


@dataclass
class Poligono(Figura):
    lados: list[Lado] = field(default_factory=list)
    observaciones: list[str] = field(default_factory=list)

    def lados_esperados(self) -> int:
        return 0

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self.lados)

    def area(self) -> float:
        raise NotImplementedError("Cada polígono concreto implementa area()")

    def agregar_observacion(self, texto: str) -> None:
        self.observaciones.append(texto)

    def copia_lados(self) -> tuple[Lado, ...]:
        return tuple(self.lados)


@dataclass
class Triangulo(Poligono):
    def __post_init__(self) -> None:
        if len(self.lados) != 3:
            raise ValueError("Un triángulo requiere 3 lados")
        a, b, c = (lado.longitud for lado in self.lados)
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Los lados no forman un triángulo")

    def lados_esperados(self) -> int:
        return 3

    def area(self) -> float:
        a, b, c = (lado.longitud for lado in self.lados)
        semiperimetro = self.perimetro() / 2
        return math.sqrt(
            semiperimetro
            * (semiperimetro - a)
            * (semiperimetro - b)
            * (semiperimetro - c)
        )

    @classmethod
    def desde_lados(cls, lados: Sequence[Lado]) -> "Triangulo":
        return cls("triángulo", "negro", list(lados))


@dataclass
class Cuadrado(Poligono):
    def __post_init__(self) -> None:
        if len(self.lados) != 4:
            raise ValueError("Un cuadrado requiere 4 lados")
        _validar_lados_iguales(self.lados, "cuadrado")

    def lados_esperados(self) -> int:
        return 4

    def area(self) -> float:
        return self.lados[0].longitud**2

    @classmethod
    def desde_lados(cls, lados: Sequence[Lado]) -> "Cuadrado":
        return cls("cuadrado", "negro", list(lados))


@dataclass
class Pentagono(Poligono):
    def __post_init__(self) -> None:
        if len(self.lados) != 5:
            raise ValueError("Un pentágono requiere 5 lados")
        _validar_lados_iguales(self.lados, "pentágono")

    def lados_esperados(self) -> int:
        return 5

    def area(self) -> float:
        return _area_regular(5, self.lados[0].longitud)


@dataclass
class Hexagono(Poligono):
    def __post_init__(self) -> None:
        if len(self.lados) != 6:
            raise ValueError("Un hexágono requiere 6 lados")
        _validar_lados_iguales(self.lados, "hexágono")

    def lados_esperados(self) -> int:
        return 6

    def area(self) -> float:
        return _area_regular(6, self.lados[0].longitud)


def _validar_lados_iguales(lados: Sequence[Lado], nombre: str) -> None:
    if len({round(lado.longitud, 9) for lado in lados}) != 1:
        raise ValueError(f"Un {nombre} debe tener todos sus lados iguales")


def _area_regular(cantidad: int, medida: float) -> float:
    return (cantidad * medida**2) / (4 * math.tan(math.pi / cantidad))


_CLASES_REGULARES = {
    3: Triangulo,
    4: Cuadrado,
    5: Pentagono,
    6: Hexagono,
}


def crear_poligono_regular(
    cantidad: int,
    medida: float = 1.0,
    nombre: str | None = None,
    color: str = "negro",
) -> Poligono:
    if isinstance(cantidad, bool) or not isinstance(cantidad, int):
        raise TypeError("La cantidad de lados debe ser un entero")
    clase = _CLASES_REGULARES.get(cantidad)
    if clase is None:
        raise ValueError(f"No hay subclase concreta para {cantidad} lados")
    nombre_final = nombre or clase.__name__.lower()
    return clase(nombre_final, color, [Lado(medida) for _ in range(cantidad)])


if __name__ == "__main__":
    triangulo = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)])
    cuadrado = Cuadrado("Cuadrado", "azul", [Lado(2) for _ in range(4)])
    print(f"Perímetro del triángulo: {triangulo.perimetro()}")
    print(f"Perímetro del cuadrado: {cuadrado.perimetro()}")
    triangulo.agregar_observacion("revisar el vértice A")
    print(f"Observaciones del triángulo: {triangulo.observaciones}")
    print(f"Lados del triángulo (copia): {triangulo.copia_lados()}")
    pentagono = crear_poligono_regular(5, 4, "Pentágono", "verde")
    print(f"Perímetro del pentágono: {pentagono.perimetro()}")
