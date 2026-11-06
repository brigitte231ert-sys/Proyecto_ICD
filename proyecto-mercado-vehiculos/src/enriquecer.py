#!/usr/bin/env python3
"""Añade marca, año, condición, cilindrada y tipo al dataset del mercado.

Lee ``data/processed/anuncios_relacionados_unicos.csv`` y escribe
``data/processed/anuncios_enriquecidos.csv`` con las columnas derivadas. No
modifica el archivo de entrada.

Uso:

    python -m src.enriquecer
    python -m src.enriquecer --input data/processed/anuncios_relacionados.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from src.config import DATA_PROCESSED
from src.extraccion import CAMPOS_DERIVADOS, enriquecer_fila
from src.privacidad import redactar


def leer_filas(ruta: Path) -> tuple[list[str], list[dict]]:
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector.fieldnames or []), list(lector)


def enriquecer(filas: list[dict]) -> list[dict]:
    resultado: list[dict] = []
    for fila in filas:
        fila = {**fila, "titulo": redactar(fila.get("titulo", ""))}
        resultado.append({**fila, **enriquecer_fila(fila)})
    return resultado


def guardar(ruta: Path, campos: list[str], filas: list[dict]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def resumen(filas: list[dict]) -> str:
    total = len(filas)
    lineas = [f"Anuncios enriquecidos: {total}", "", "Cobertura:"]
    for campo in CAMPOS_DERIVADOS:
        llenos = sum(1 for f in filas if f.get(campo) not in (None, ""))
        lineas.append(f"  {campo:<15} {llenos:>6} ({llenos / total:.1%})")

    lineas.append("")
    lineas.append("Condición:")
    for valor, n in Counter(f["condicion"] for f in filas).most_common():
        lineas.append(f"  {valor:<15} {n:>6}")

    lineas.append("")
    lineas.append("Top 15 marcas:")
    marcas = Counter(f["marca"] for f in filas if f.get("marca"))
    for marca, n in marcas.most_common(15):
        lineas.append(f"  {marca:<16} {n:>6}")
    return "\n".join(lineas)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios_relacionados_unicos.csv",
        help="CSV de entrada.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_PROCESSED / "anuncios_enriquecidos.csv",
        help="CSV de salida.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(
            f"No existe {args.input}. Ejecuta primero:\n  python -m src.relevancia"
        )

    campos, filas = leer_filas(args.input)
    enriquecidas = enriquecer(filas)
    campos_salida = campos + [c for c in CAMPOS_DERIVADOS if c not in campos]

    guardar(args.output, campos_salida, enriquecidas)
    print(resumen(enriquecidas))
    print(f"\nGuardado en: {args.output}")


if __name__ == "__main__":
    main()
