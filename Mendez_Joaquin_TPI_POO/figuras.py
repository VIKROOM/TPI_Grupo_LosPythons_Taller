"""figuras.py — Dominio completo del TP Integrador de POO.

Resuelve las Partes 1 a 4:

- Parte 1: versión idiomática del dominio, sin getters/setters ceremoniales,
  sin atributos de clase mutables accidentales, sin defaults mutables y sin
  sobrecarga de constructores estilo Java.
- Parte 2: Taller (agregación), Etiqueta (asociación) y copia defensiva en
  Poligono.lados() y Taller.inventario().
- Parte 3: Figura y Poligono son ABC; Triangulo, Cuadrado, Pentagono y
  Hexagono son concretas. PoligonoRegular se reemplaza por la fábrica
  crear_poligono_regular(), que devuelve una subclase concreta.
- Parte 4: Exportable es un Protocol estructural; Poligono y PlanoCAD lo
  cumplen sin que PlanoCAD herede de nada nuestro.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import ClassVar, Protocol, runtime_checkable

from libreria_externa import PlanoCAD

__all__ = [
    "Etiqueta",
    "Exportable",
    "Lado",
    "Figura",
    "Poligono",
    "Triangulo",
    "Cuadrado",
    "Pentagono",
    "Hexagono",
    "Taller",
    "crear_poligono_regular",
    "exportar_todo",
    "PlanoCAD",
]


# ---------------------------------------------------------------------------
# Parte 4 — contrato estructural
# ---------------------------------------------------------------------------
@runtime_checkable
class Exportable(Protocol):
    """Contrato por estructura: alcanza con tener exportar() -> str."""

    def exportar(self) -> str:
        ...


# ---------------------------------------------------------------------------
# Parte 2 — Etiqueta: objeto de valor inmutable, asociado a un Lado
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Etiqueta:
    texto: str

    def __post_init__(self) -> None:
        if not isinstance(self.texto, str) or not self.texto.strip():
            raise ValueError("La etiqueta no puede estar vacía")


# ---------------------------------------------------------------------------
# Parte 1 — Lado: @property solo donde hay lógica de validación
# ---------------------------------------------------------------------------
class Lado:
    def __init__(self, longitud: float, etiqueta: Etiqueta | None = None) -> None:
        if etiqueta is not None and not isinstance(etiqueta, Etiqueta):
            raise TypeError("etiqueta debe ser una Etiqueta o None")
        self.longitud = longitud
        self._etiqueta = etiqueta

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

    @property
    def etiqueta(self) -> Etiqueta | None:
        return self._etiqueta

    def etiquetar(self, etiqueta: Etiqueta | str) -> None:
        if isinstance(etiqueta, str):
            etiqueta = Etiqueta(etiqueta)
        if not isinstance(etiqueta, Etiqueta):
            raise TypeError("La etiqueta debe ser una Etiqueta o un str")
        self._etiqueta = etiqueta

    def escalar(self, factor: float) -> None:
        if isinstance(factor, bool) or not isinstance(factor, (int, float)):
            raise TypeError("El factor debe ser numérico")
        if not math.isfinite(factor) or factor <= 0:
            raise ValueError("El factor debe ser positivo y finito")
        nueva_longitud = self._longitud * factor
        if not math.isfinite(nueva_longitud):
            raise ValueError("La longitud resultante debe ser finita")
        self.longitud = nueva_longitud

    def __repr__(self) -> str:
        etiqueta = f", etiqueta={self._etiqueta.texto!r}" if self._etiqueta else ""
        return f"Lado({self._longitud:.2f}{etiqueta})"


# ---------------------------------------------------------------------------
# Parte 1 y 3 — Figura y Poligono: ABC y sin estado de clase mutable
# ---------------------------------------------------------------------------
class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not isinstance(color, str) or not color.strip():
            raise ValueError("El color no puede estar vacío")
        self.nombre = nombre
        self.color = color

    @abstractmethod
    def area(self) -> float:
        """Toda figura concreta debe calcular su área."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nombre={self.nombre!r}, color={self.color!r})"


class Poligono(Figura, ABC):
    LADOS_ESPERADOS: ClassVar[int] = 0
    NOMBRE_POR_DEFECTO: ClassVar[str] = "polígono"

    def __init__(
        self,
        nombre: str,
        color: str,
        lados: Sequence[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color)
        # Composición: el polígono copia sus propios Lado; no conserva el alias
        # de la lista que recibe desde afuera.
        self._lados = [Lado(lado.longitud, lado.etiqueta) for lado in (lados or [])]
        self._validar_cantidad()

    @abstractmethod
    def lados_esperados(self) -> int:
        """Cada subclase concreta declara cuántos lados admite."""

    def _validar_cantidad(self) -> None:
        esperados = self.lados_esperados()
        if len(self._lados) != esperados:
            raise ValueError(
                f"{type(self).__name__} requiere {esperados} lados y recibió "
                f"{len(self._lados)}"
            )

    @classmethod
    def regular(
        cls,
        medida: float = 1.0,
        nombre: str | None = None,
        color: str = "negro",
    ) -> "Poligono":
        """Constructor alternativo: polígono regular de N lados iguales."""
        return cls(
            nombre or cls.NOMBRE_POR_DEFECTO,
            color,
            [Lado(medida) for _ in range(cls.LADOS_ESPERADOS)],
        )

    def lados(self) -> tuple[Lado, ...]:
        """Copia defensiva: nunca devuelve la lista interna."""
        return tuple(self._lados)

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def exportar(self) -> str:
        return (
            f"{type(self).__name__}[{self.nombre}] color={self.color} "
            f"lados={len(self._lados)} perímetro={self.perimetro():.2f} "
            f"área={self.area():.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(nombre={self.nombre!r}, "
            f"color={self.color!r}, lados={len(self._lados)})"
        )


def _validar_lados_iguales(lados: Sequence[Lado], nombre: str) -> None:
    medidas = {round(lado.longitud, 9) for lado in lados}
    if len(medidas) != 1:
        raise ValueError(f"Un {nombre} debe tener todos sus lados iguales")


def _area_poligono_regular(cantidad: int, medida: float) -> float:
    return (cantidad * medida**2) / (4 * math.tan(math.pi / cantidad))


class Triangulo(Poligono):
    LADOS_ESPERADOS = 3
    NOMBRE_POR_DEFECTO = "triángulo"

    def __init__(
        self,
        nombre: str = NOMBRE_POR_DEFECTO,
        color: str = "negro",
        lados: Sequence[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)
        a, b, c = (lado.longitud for lado in self._lados)
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Los lados no forman un triángulo")

    def lados_esperados(self) -> int:
        return self.LADOS_ESPERADOS

    def area(self) -> float:
        a, b, c = (lado.longitud for lado in self._lados)
        semiperimetro = self.perimetro() / 2
        return math.sqrt(
            semiperimetro
            * (semiperimetro - a)
            * (semiperimetro - b)
            * (semiperimetro - c)
        )


class Cuadrado(Poligono):
    LADOS_ESPERADOS = 4
    NOMBRE_POR_DEFECTO = "cuadrado"

    def __init__(
        self,
        nombre: str = NOMBRE_POR_DEFECTO,
        color: str = "negro",
        lados: Sequence[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)
        _validar_lados_iguales(self._lados, "cuadrado")

    def lados_esperados(self) -> int:
        return self.LADOS_ESPERADOS

    def area(self) -> float:
        return self._lados[0].longitud**2


class Pentagono(Poligono):
    LADOS_ESPERADOS = 5
    NOMBRE_POR_DEFECTO = "pentágono"

    def __init__(
        self,
        nombre: str = NOMBRE_POR_DEFECTO,
        color: str = "negro",
        lados: Sequence[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)
        _validar_lados_iguales(self._lados, "pentágono")

    def lados_esperados(self) -> int:
        return self.LADOS_ESPERADOS

    def area(self) -> float:
        return _area_poligono_regular(self.LADOS_ESPERADOS, self._lados[0].longitud)


class Hexagono(Poligono):
    LADOS_ESPERADOS = 6
    NOMBRE_POR_DEFECTO = "hexágono"

    def __init__(
        self,
        nombre: str = NOMBRE_POR_DEFECTO,
        color: str = "negro",
        lados: Sequence[Lado] | None = None,
    ) -> None:
        super().__init__(nombre, color, lados)
        _validar_lados_iguales(self._lados, "hexágono")

    def lados_esperados(self) -> int:
        return self.LADOS_ESPERADOS

    def area(self) -> float:
        return _area_poligono_regular(self.LADOS_ESPERADOS, self._lados[0].longitud)


# ---------------------------------------------------------------------------
# Parte 3 — decisión sobre PoligonoRegular: fábrica, no herencia
# ---------------------------------------------------------------------------
_CLASES_REGULARES: dict[int, type[Poligono]] = {
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
    """Reemplaza a PoligonoRegular sin agregar una jerarquía artificial.

    Devuelve la subclase concreta que corresponde a la cantidad de lados.
    """
    if isinstance(cantidad, bool) or not isinstance(cantidad, int):
        raise TypeError("La cantidad de lados debe ser un entero")
    try:
        clase = _CLASES_REGULARES[cantidad]
    except KeyError:
        disponibles = ", ".join(str(n) for n in sorted(_CLASES_REGULARES))
        raise ValueError(
            f"No hay una subclase concreta para {cantidad} lados; "
            f"disponibles: {disponibles}"
        ) from None
    return clase.regular(medida=medida, nombre=nombre, color=color)


# ---------------------------------------------------------------------------
# Parte 2 — Taller: agregación; recibe polígonos ya construidos
# ---------------------------------------------------------------------------
class Taller:
    def __init__(self) -> None:
        self._poligonos: list[Poligono] = []

    def recibir(self, poligono: Poligono) -> None:
        if not isinstance(poligono, Poligono):
            raise TypeError("Taller solo recibe Poligono")
        if any(actual is poligono for actual in self._poligonos):
            raise ValueError("El polígono ya está en el taller")
        self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono) -> Poligono:
        for indice, actual in enumerate(self._poligonos):
            if actual is poligono:
                del self._poligonos[indice]
                return poligono
        raise ValueError("El polígono no pertenece a este taller")

    def inventario(self) -> tuple[Poligono, ...]:
        """Copia defensiva del inventario interno."""
        return tuple(self._poligonos)

    def __len__(self) -> int:
        return len(self._poligonos)

    def __iter__(self) -> Iterator[Poligono]:
        return iter(tuple(self._poligonos))


# ---------------------------------------------------------------------------
# Parte 4 — exportación conjunta de polígonos y planos CAD
# ---------------------------------------------------------------------------
def exportar_todo(items: Sequence[Exportable]) -> list[str]:
    """Funciona con cualquier objeto que tenga exportar(), sin exigir herencia."""
    return [item.exportar() for item in items]
