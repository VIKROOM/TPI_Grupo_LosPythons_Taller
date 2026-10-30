from __future__ import annotations

import math
from dataclasses import FrozenInstanceError

import pytest

from figuras import (
    Cuadrado,
    Etiqueta,
    Exportable,
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


def test_poligono_es_abstracto() -> None:
    with pytest.raises(TypeError):
        Poligono(  # type: ignore[abstract]
            "genérico", "gris", [Lado(1), Lado(2), Lado(3)]
        )


def test_composicion_y_copia_defensiva() -> None:
    entrada = [Lado(3), Lado(4), Lado(5)]
    triangulo = Triangulo("T", "rojo", entrada)

    entrada.append(Lado(100))

    assert triangulo.perimetro() == 12
    assert isinstance(triangulo.lados(), tuple)
    with pytest.raises(AttributeError):
        triangulo.lados().append(Lado(1))  # type: ignore[attr-defined]


def test_agregacion_taller() -> None:
    cuadrado = Cuadrado("C", "azul", [Lado(2) for _ in range(4)])
    taller = Taller()
    taller.recibir(cuadrado)

    assert taller.inventario() == (cuadrado,)

    restaurado = taller.restaurar(cuadrado)

    assert restaurado is cuadrado
    assert taller.inventario() == ()
    assert cuadrado.perimetro() == 8


def test_asociacion_etiqueta() -> None:
    triangulo = Triangulo("T", "rojo", [Lado(3), Lado(4), Lado(5)])
    triangulo.lados()[0].etiquetar("A")
    triangulo.lados()[1].etiquetar(Etiqueta("B"))

    assert triangulo.lados()[0].etiqueta == Etiqueta("A")
    assert triangulo.lados()[1].etiqueta == Etiqueta("B")
    assert triangulo.lados()[2].etiqueta is None

    with pytest.raises(FrozenInstanceError):
        triangulo.lados()[0].etiqueta.texto = "C"  # type: ignore[misc, union-attr]


def test_exportable_es_estructural() -> None:
    triangulo = Triangulo("T", "rojo", [Lado(3), Lado(4), Lado(5)])
    plano = PlanoCAD("PL-1")

    assert isinstance(triangulo, Exportable)
    assert isinstance(plano, Exportable)

    salida = exportar_todo([triangulo, plano])

    assert salida == [triangulo.exportar(), plano.exportar()]
    assert salida[1] == "PlanoCAD[PL-1 @ 1:100]"


def test_areas_y_perimetros() -> None:
    triangulo = Triangulo("T", "rojo", [Lado(3), Lado(4), Lado(5)])
    assert triangulo.perimetro() == 12
    assert math.isclose(triangulo.area(), 6.0)

    cuadrado = Cuadrado("C", "azul", [Lado(2) for _ in range(4)])
    assert cuadrado.area() == 4

    pentagono = Pentagono("P", "verde", [Lado(4) for _ in range(5)])
    assert math.isclose(
        pentagono.area(), (5 * 4**2) / (4 * math.tan(math.pi / 5))
    )

    hexagono = Hexagono("H", "amarillo", [Lado(3) for _ in range(6)])
    assert math.isclose(
        hexagono.area(), (6 * 3**2) / (4 * math.tan(math.pi / 6))
    )


def test_validaciones_y_fabrica() -> None:
    with pytest.raises(ValueError):
        Triangulo("T", "rojo", [Lado(1), Lado(1)])

    with pytest.raises(ValueError):
        Cuadrado("C", "azul", [Lado(1), Lado(2), Lado(1), Lado(1)])

    with pytest.raises(ValueError):
        crear_poligono_regular(7, 2)

    poligono = crear_poligono_regular(5, 4, "Penta", "verde")

    assert isinstance(poligono, Pentagono)
    assert poligono.perimetro() == 20


@pytest.mark.parametrize("valor", [0, -1, float("nan"), float("inf")])
def test_lado_rechaza_longitudes_invalidas(valor: float) -> None:
    with pytest.raises(ValueError):
        Lado(valor)


@pytest.mark.parametrize("valor", ["3", None, True])
def test_lado_rechaza_tipos_invalidos(valor: object) -> None:
    with pytest.raises(TypeError):
        Lado(valor)  # type: ignore[arg-type]


def test_lado_escala_y_valida_factor() -> None:
    lado = Lado(2)
    lado.escalar(1.5)
    assert lado.longitud == 3

    for factor in (0, -1, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            lado.escalar(factor)

    with pytest.raises(TypeError):
        lado.escalar(True)


def test_etiqueta_valida_texto() -> None:
    for texto in ("", "   "):
        with pytest.raises(ValueError):
            Etiqueta(texto)

    lado = Lado(1)
    assert lado.etiqueta is None
    lado.etiquetar("A")
    assert lado.etiqueta == Etiqueta("A")

    with pytest.raises(ValueError):
        lado.etiquetar("   ")

    with pytest.raises(TypeError):
        lado.etiquetar(3)  # type: ignore[arg-type]


def test_cantidad_de_lados_por_subclase() -> None:
    with pytest.raises(ValueError):
        Triangulo("T", "rojo", [Lado(1), Lado(1)])
    with pytest.raises(ValueError):
        Cuadrado("C", "azul", [Lado(1) for _ in range(3)])
    with pytest.raises(ValueError):
        Pentagono("P", "verde", [Lado(1) for _ in range(4)])
    with pytest.raises(ValueError):
        Hexagono("H", "amarillo", [Lado(1) for _ in range(5)])


def test_poligonos_validan_forma() -> None:
    with pytest.raises(ValueError):
        Triangulo("T", "rojo", [Lado(1), Lado(2), Lado(10)])

    with pytest.raises(ValueError):
        Cuadrado("C", "azul", [Lado(1), Lado(2), Lado(1), Lado(1)])

    with pytest.raises(ValueError):
        Pentagono("P", "verde", [Lado(1), Lado(2), Lado(1), Lado(1), Lado(1)])

    with pytest.raises(ValueError):
        Hexagono(
            "H",
            "amarillo",
            [Lado(1), Lado(2), Lado(1), Lado(1), Lado(1), Lado(1)],
        )


def test_composicion_copia_instancias_de_lado() -> None:
    original = Lado(3, Etiqueta("A"))
    triangulo = Triangulo("T", "rojo", [original, Lado(4), Lado(5)])

    copia = triangulo.lados()[0]

    assert copia is not original
    assert copia.longitud == original.longitud
    assert copia.etiqueta == original.etiqueta


def test_taller_rechaza_duplicados_y_restauracion_invalida() -> None:
    cuadrado = Cuadrado("C", "azul", [Lado(2) for _ in range(4)])
    otro = Cuadrado("D", "azul", [Lado(2) for _ in range(4)])
    taller = Taller()
    taller.recibir(cuadrado)

    with pytest.raises(ValueError):
        taller.recibir(cuadrado)

    with pytest.raises(ValueError):
        taller.restaurar(otro)

    with pytest.raises(TypeError):
        taller.recibir("cuadrado")  # type: ignore[arg-type]


def test_fabrica_valida_entradas() -> None:
    with pytest.raises(TypeError):
        crear_poligono_regular(True)

    with pytest.raises(TypeError):
        crear_poligono_regular(3.0)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        crear_poligono_regular(7)

    for medida in (0, -1, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            crear_poligono_regular(3, medida)


@pytest.mark.parametrize(
    ("cantidad", "clase"),
    [(3, Triangulo), (4, Cuadrado), (5, Pentagono), (6, Hexagono)],
)
def test_fabrica_devuelve_la_subclase_correcta(
    cantidad: int, clase: type[Poligono]
) -> None:
    poligono = crear_poligono_regular(cantidad, 2)
    assert isinstance(poligono, clase)
    assert poligono.perimetro() == cantidad * 2


def test_constructor_regular_respeta_cantidad_de_lados() -> None:
    triangulo = Triangulo.regular(2)
    cuadrado = Cuadrado.regular(2)
    pentagono = Pentagono.regular(2)
    hexagono = Hexagono.regular(2)

    assert isinstance(triangulo, Triangulo)
    assert triangulo.perimetro() == 6
    assert cuadrado.perimetro() == 8
    assert pentagono.perimetro() == 10
    assert hexagono.perimetro() == 12


def test_exportable_acepta_objetos_sin_herencia() -> None:
    class ExportableManual:
        def exportar(self) -> str:
            return "manual"

    manual = ExportableManual()

    assert isinstance(manual, Exportable)
    assert exportar_todo([manual]) == ["manual"]
    assert exportar_todo((manual,)) == ["manual"]
