"""demo_sintomas.py — Síntomas reproducibles de la Parte 1.

La primera mitad reproduce, con una copia mínima del código de partida, los
síntomas que el diseño con acento de Java deja ver en runtime. La segunda mitad
muestra el mismo escenario con figuras.py ya corregido.
"""

from __future__ import annotations

from typing import Any


class LadoRoto:
    def __init__(self, longitud: float) -> None:
        self._longitud = longitud

    def getLongitud(self) -> float:
        return self._longitud


class PoligonoRoto:
    catalogo: list["PoligonoRoto"] = []

    def __init__(
        self,
        nombre: str,
        color: str,
        lados: list[LadoRoto] = [],
        observaciones: list[str] = [],
    ) -> None:
        self._nombre = nombre
        self._color = color
        self._lados = lados
        self._observaciones = observaciones
        PoligonoRoto.catalogo.append(self)

    def perimetro(self) -> float:
        total = 0.0
        for lado in self._lados:
            total = total + lado.getLongitud()
        return total

    def area(self) -> int:
        return "area sin calcular"  # type: ignore[return-value]

    def getLados(self) -> list[LadoRoto]:
        return self._lados


class TrianguloRoto(PoligonoRoto):
    def __init__(self, *args: object) -> None:
        if len(args) == 3:
            super().__init__(*args)  # type: ignore[arg-type]
        elif len(args) == 1 and isinstance(args[0], list):
            super().__init__("triángulo", "negro", args[0])
        else:
            super().__init__("triángulo", "negro", [])


def main() -> None:
    print("=== ANTES DEL ARREGLO (código de partida) ===")

    p1 = PoligonoRoto("A", "rojo")
    p2 = PoligonoRoto("B", "azul")
    print(
        "1) Defaults mutables compartidos:",
        p1._observaciones is p2._observaciones,
    )
    p1._observaciones.append("revisar el vértice")
    print("   p2 ve la observación de p1:", p2._observaciones)

    print(
        "2) Catálogo de clase compartido:",
        PoligonoRoto.catalogo is p1.catalogo,
        "| longitud:",
        len(PoligonoRoto.catalogo),
    )

    lados = [LadoRoto(3), LadoRoto(4), LadoRoto(5)]
    triangulo = TrianguloRoto("T", "rojo", lados)
    print(
        "3) Alias de la lista:",
        triangulo.getLados() is lados,
        "| perímetro antes:",
        triangulo.perimetro(),
    )
    lados.append(LadoRoto(100))
    print("   perímetro después de mutar la lista externa:", triangulo.perimetro())

    print(
        "4) Type hint mentiroso: anotado -> int, devuelve",
        type(triangulo.area()).__name__,
        repr(triangulo.area()),
    )

    print("\n=== GETTER -> @PROPERTY: EL CLIENTE NO CAMBIA ===")

    class LadoPublico:
        def __init__(self, longitud: float) -> None:
            self.longitud = longitud

    def usar_lado(lado: Any) -> float:
        lado.longitud = 5  # misma línea para el atributo público y la property
        return lado.longitud

    publico = LadoPublico(1)
    print("Antes (atributo público):", usar_lado(publico))

    from figuras import Lado, Poligono, Triangulo

    propiedad = Lado(1)
    print("Después (@property):", usar_lado(propiedad))
    try:
        propiedad.longitud = -1
    except ValueError as error:
        print("La misma asignación ahora valida:", error)

    print("\n=== DESPUÉS DEL ARREGLO (figuras.py) ===")

    entrada = [Lado(3), Lado(4), Lado(5)]
    triangulo_ok = Triangulo("T", "rojo", entrada)
    entrada.append(Lado(100))
    print("Lista externa mutada; perímetro del triángulo:", triangulo_ok.perimetro())
    print("lados() devuelve:", type(triangulo_ok.lados()).__name__)
    print("area() devuelve:", type(triangulo_ok.area()).__name__, triangulo_ok.area())

    try:
        Poligono(  # type: ignore[abstract]
            "Genérico", "gris", [Lado(1), Lado(2), Lado(3)]
        )
    except TypeError as error:
        print(
            "Poligono abstracto revienta al construir:",
            type(error).__name__,
            f"({error})",
        )


if __name__ == "__main__":
    main()
