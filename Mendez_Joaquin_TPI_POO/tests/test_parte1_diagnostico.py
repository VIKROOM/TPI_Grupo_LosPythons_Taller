from __future__ import annotations

import math

import pytest

from parte1_diagnostico import Lado, Triangulo, crear_poligono_regular


@pytest.mark.parametrize("valor", [0, -1, float("nan"), float("inf")])
def test_lado_rechaza_longitudes_invalidas(valor: float) -> None:
    with pytest.raises(ValueError):
        Lado(valor)


@pytest.mark.parametrize("valor", ["3", None, True])
def test_lado_rechaza_tipos_invalidos(valor: object) -> None:
    with pytest.raises(TypeError):
        Lado(valor)  # type: ignore[arg-type]


def test_triangulo_corregido_calcula_area() -> None:
    triangulo = Triangulo("T", "rojo", [Lado(3), Lado(4), Lado(5)])
    assert triangulo.perimetro() == 12
    assert math.isclose(triangulo.area(), 6.0)


def test_fabrica_corregida_valida_entradas() -> None:
    with pytest.raises(TypeError):
        crear_poligono_regular(True)

    with pytest.raises(TypeError):
        crear_poligono_regular(3.0)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        crear_poligono_regular(7)

    with pytest.raises(ValueError):
        crear_poligono_regular(3, 0)
