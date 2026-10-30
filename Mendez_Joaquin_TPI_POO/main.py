"""main.py — Demo ejecutable del TP Integrador.

Arma un taller con cuatro polígonos (uno de cada subclase), etiqueta dos lados,
exporta todo junto con un PlanoCAD y deja a la vista:

- Composición: un Lado no sobrevive al borrado de su Poligono.
- Agregación: un Poligono sobrevive al borrado del Taller.
- Falla temprana: instanciar Poligono (ABC) revienta al construir.
- Fábrica: crear_poligono_regular() reemplaza a PoligonoRegular.
"""

from __future__ import annotations

import gc
import weakref

from figuras import (
    Cuadrado,
    Etiqueta,
    Hexagono,
    Lado,
    Pentagono,
    Poligono,
    Taller,
    Triangulo,
    crear_poligono_regular,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def main() -> None:
    triangulo = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)])
    cuadrado = Cuadrado("Cuadrado", "azul", [Lado(2) for _ in range(4)])
    pentagono = Pentagono("Pentágono", "verde", [Lado(4) for _ in range(5)])
    hexagono = Hexagono("Hexágono", "amarillo", [Lado(3) for _ in range(6)])

    triangulo.lados()[0].etiquetar("A")
    triangulo.lados()[1].etiquetar(Etiqueta("B"))

    taller = Taller()
    for figura in (triangulo, cuadrado, pentagono, hexagono):
        taller.recibir(figura)

    print("=== INVENTARIO DEL TALLER ===")
    for poligono in taller.inventario():
        etiquetas = [
            lado.etiqueta.texto for lado in poligono.lados() if lado.etiqueta
        ]
        print(
            f"- {poligono}: perímetro={poligono.perimetro():.2f}, "
            f"área={poligono.area():.2f}, etiquetas={etiquetas}"
        )

    print("\n=== RESTAURAR UN POLÍGONO (AGREGACIÓN) ===")
    restaurado = taller.restaurar(hexagono)
    print(
        f"- Restaurado: {restaurado.nombre}; "
        f"¿sigue en el inventario? {any(p is restaurado for p in taller.inventario())}"
    )
    taller.recibir(restaurado)

    plano = PlanoCAD("PL-001", "1:50")
    print("\n=== EXPORTACIÓN CONJUNTA (PROTOCOL) ===")
    for linea in exportar_todo([*taller.inventario(), plano]):
        print(f"- {linea}")

    print("\n=== AGREGACIÓN: EL POLÍGONO SOBREVIVE AL TALLER ===")
    cuadrado_ref = cuadrado
    del taller
    gc.collect()
    print(
        f"- Taller borrado; el cuadrado sigue vivo: {cuadrado_ref.nombre}, "
        f"perímetro={cuadrado_ref.perimetro():.2f}"
    )

    print("\n=== COMPOSICIÓN: EL LADO NO SOBREVIVE AL POLÍGONO ===")
    efimero = Triangulo("Efímero", "gris", [Lado(3), Lado(4), Lado(5)])
    lado_debil = weakref.ref(efimero.lados()[0])
    print(f"- Lado vivo antes de borrar el polígono: {lado_debil() is not None}")
    del efimero
    gc.collect()
    print(f"- Lado vivo después de borrar el polígono: {lado_debil() is not None}")

    print("\n=== FALLA TEMPRANA ===")
    try:
        Poligono(  # type: ignore[abstract]
            "Genérico", "gris", [Lado(1), Lado(2), Lado(3)]
        )
    except TypeError as error:
        print(f"- Poligono(...) revienta al construir: {type(error).__name__}: {error}")

    print("\n=== FÁBRICA QUE REEMPLAZA A PoligonoRegular ===")
    for cantidad in (3, 4, 5, 6):
        regular = crear_poligono_regular(cantidad, 2, color="cian")
        print(
            f"- {cantidad} lados -> {type(regular).__name__} "
            f"(perímetro={regular.perimetro():.2f})"
        )


if __name__ == "__main__":
    main()
