#!/usr/bin/env python3
"""Redacción de datos personales en los textos de los anuncios.

Los títulos de Revolico a veces incluyen teléfonos, correos o enlaces de
WhatsApp. El proyecto no debe publicar datos personales, así que se sustituyen
por ``[contacto]`` antes de guardar cualquier archivo derivado.

Uso:

    python -m src.privacidad                       # limpia anuncios.csv in place
    python -m src.privacidad --input otro.csv --output limpio.csv
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from src.config import DATA_PROCESSED

# Móviles cubanos: 8 dígitos que empiezan por 5, con prefijo +53 opcional.
_TELEFONO_RE = re.compile(
    r"(?<!\d)(?:\+?53[\s\-]?)?5\d{7}(?!\d)(?!\s*(?:cup|usd|mn|cuc|mlc))",
    re.IGNORECASE,
)
_ENLACE_CONTACTO_RE = re.compile(
    r"(?:https?://)?(?:wa\.me|api\.whatsapp\.com|t\.me)/\S+", re.IGNORECASE
)
_CORREO_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def redactar(texto: object) -> str:
    """Sustituye teléfonos, correos y enlaces de contacto por ``[contacto]``."""
    limpio = str(texto)
    limpio = _ENLACE_CONTACTO_RE.sub("[contacto]", limpio)
    limpio = _CORREO_RE.sub("[contacto]", limpio)
    limpio = _TELEFONO_RE.sub("[contacto]", limpio)
    return limpio


def _leer(ruta: Path) -> tuple[list[str], list[dict]]:
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector.fieldnames or []), list(lector)


def _guardar(ruta: Path, campos: list[str], filas: list[dict]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def limpiar_csv(entrada: Path, salida: Path) -> int:
    """Redacta la columna ``titulo``. Devuelve cuántas filas cambiaron."""
    campos, filas = _leer(entrada)
    if "titulo" not in campos:
        raise SystemExit(f"{entrada} no tiene columna 'titulo'.")

    cambiadas = 0
    for fila in filas:
        original = fila.get("titulo") or ""
        fila["titulo"] = redactar(original)
        if fila["titulo"] != original:
            cambiadas += 1

    _guardar(salida, campos, filas)
    return cambiadas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios.csv",
        help="CSV de entrada.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="CSV de salida. Si se omite, sobrescribe la entrada.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"No existe {args.input}.")

    salida = args.output or args.input
    cambiadas = limpiar_csv(args.input, salida)
    print(f"Filas redactadas: {cambiadas}")
    print(f"Guardado en: {salida}")


if __name__ == "__main__":
    main()
