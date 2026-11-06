#!/usr/bin/env python3
"""Descarga descripciones para una submuestra de anuncios.

La página de listado no incluye la descripción completa. Este script toma una
muestra aleatoria (estratificada por categoría) del CSV de anuncios y visita
cada anuncio para extraer solo texto y metadatos públicos.

Uso:

    python -m src.details --n 300

No guarda teléfonos, nombres ni identificadores de usuario.
"""

from __future__ import annotations

import argparse
import csv
import random
import time
from collections import defaultdict
from pathlib import Path

import requests

from src.config import BASE_URL, DATA_PROCESSED, DELAY_RANGE, HEADERS
from src.scraper import fetch, parse_state


def leer_anuncios(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def muestrear_estratificado(
    filas: list[dict], n: int, semilla: int
) -> list[dict]:
    """Toma ~n anuncios repartidos entre categorías."""
    if n >= len(filas):
        return filas

    por_categoria: dict[str, list[dict]] = defaultdict(list)
    for fila in filas:
        por_categoria[fila.get("categoria", "sin_categoria")].append(fila)

    random.seed(semilla)
    cuota = max(1, n // len(por_categoria))
    muestra: list[dict] = []
    for categoria, grupo in por_categoria.items():
        muestra.extend(random.sample(grupo, min(cuota, len(grupo))))

    # Completa hasta n si sobró cupo.
    ids_muestra = {f["id"] for f in muestra}
    restantes = [f for f in filas if f["id"] not in ids_muestra]
    if len(muestra) < n and restantes:
        muestra.extend(random.sample(restantes, min(n - len(muestra), len(restantes))))

    return muestra


def extraer_detalle(html: str, ad_id: str) -> dict | None:
    state = parse_state(html)
    ad = state.get(f"AdType:{ad_id}")
    if ad is None:
        ad = next(
            (valor for clave, valor in state.items() if clave.startswith("AdType:")),
            None,
        )
    if ad is None:
        return None
    return {
        "id": ad.get("id"),
        "descripcion": ad.get("description") or ad.get("shortDescription"),
        "fecha_actualizacion": ad.get("updatedOnByUser"),
        "vendido": ad.get("isSold"),
        "estado": ad.get("status"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios.csv",
        help="CSV con los anuncios recolectados.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DATA_PROCESSED / "descripciones.csv",
        help="CSV de salida.",
    )
    parser.add_argument("--n", type=int, default=300, help="Tamaño de la muestra.")
    parser.add_argument("--semilla", type=int, default=42, help="Semilla aleatoria.")
    parser.add_argument(
        "--delay-min", type=float, default=DELAY_RANGE[0], help="Pausa mínima (s)."
    )
    parser.add_argument(
        "--delay-max", type=float, default=DELAY_RANGE[1], help="Pausa máxima (s)."
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(
            f"No existe {args.input}. Ejecuta primero: python -m src.scraper --max-pages 1"
        )

    filas = leer_anuncios(args.input)
    muestra = muestrear_estratificado(filas, args.n, args.semilla)
    print(f"Anuncios en el CSV: {len(filas)} | muestra: {len(muestra)}")

    session = requests.Session()
    session.headers.update(HEADERS)

    resultados: list[dict] = []
    for i, fila in enumerate(muestra, start=1):
        ad_id = str(fila["id"])
        url = fila.get("url") or f"{BASE_URL}/item/{ad_id}"
        try:
            html = fetch(url, session)
            detalle = extraer_detalle(html, ad_id)
        except Exception as error:  # noqa: BLE001
            print(f"[{i}/{len(muestra)}] error en {ad_id}: {error}")
            continue
        if detalle:
            resultados.append(detalle)
        if i % 25 == 0:
            print(f"[{i}/{len(muestra)}] descargados")

        if i < len(muestra):
            time.sleep(random.uniform(args.delay_min, args.delay_max))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8-sig") as archivo:
        writer = csv.DictWriter(
            archivo,
            fieldnames=["id", "descripcion", "fecha_actualizacion", "vendido", "estado"],
        )
        writer.writeheader()
        writer.writerows(resultados)

    print(f"Guardadas {len(resultados)} descripciones en {args.out}")


if __name__ == "__main__":
    main()
