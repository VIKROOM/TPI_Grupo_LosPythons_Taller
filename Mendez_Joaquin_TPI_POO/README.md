# TPI POO — Unidad 3

Trabajo Práctico Integrador de Programación IV: dominio `Figura / Poligono /
Lado` resuelto con POO idiomática en Python.

## Archivos

| Archivo | Qué resuelve |
|---|---|
| `figuras.py` | Dominio completo de las Partes 1 a 4: ABC, relaciones, copia defensiva, `Exportable` y fábrica de polígonos regulares. |
| `parte1_diagnostico.py` | Versión corregida del archivo de partida; conserva los nombres originales para comparar el antes y el después. |
| `demo_sintomas.py` | Reproduce síntomas del código de partida (defaults mutables, alias de listas, catálogo compartido y type hint mentiroso) y muestra la corrección. |
| `libreria_externa.py` | Clase `PlanoCAD` de un tercero. **No se modifica.** |
| `main.py` | Demo ejecutable: taller, etiquetas, exportación conjunta, composición, agregación y falla temprana. |
| `informe.md` | Informe de la entrega (máximo 1 carilla). |
| `mypy.ini` | Configuración de mypy para el proyecto. |
| `uml/modelo_final.md` | Diagrama UML final en Mermaid. |
| `tests/test_figuras.py` y `tests/test_parte1_diagnostico.py` | Suite de 36 tests con pytest. |

## Cómo ejecutar

```bash
python main.py
python demo_sintomas.py
python parte1_diagnostico.py
python -m pytest -q
```

Requiere Python 3.10 o superior. Para los tests, `pip install pytest`.
Para el chequeo estático opcional: `pip install mypy` y `python -m mypy .`.

## Decisiones principales

- `Figura` y `Poligono` son clases abstractas; `Poligono` no se puede instanciar.
- `Poligono` compone sus `Lado` y devuelve una tupla en `lados()`.
- `Taller` agrega polígonos ya construidos y devuelve una tupla en `inventario()`.
- `Etiqueta` es un `@dataclass(frozen=True)` asociado opcionalmente a un `Lado`.
- `PoligonoRegular` se reemplazó por `crear_poligono_regular()`.
- `Exportable` es un `typing.Protocol`; `PlanoCAD` lo cumple sin heredar.

## Entrega

Comprimir la carpeta raíz `Mendez_Joaquin_TPI_POO/` como
`Mendez_Joaquin_TPI_POO.zip`, eliminando antes `__pycache__/`, `.venv/`,
`.mypy_cache/` y `.pytest_cache/`.
