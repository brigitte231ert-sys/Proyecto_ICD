#!/usr/bin/env python3
"""Recolector de anuncios de Revolico.

Extrae los datos estructurados que el sitio incrusta en el bloque
``__NEXT_DATA__`` (estado de Apollo). No usa Selenium ni selectores CSS.

Uso (desde la raíz del proyecto):

    python -m src.scraper --max-pages 1 --categorias bicicletas
    python -m src.scraper --max-pages 43

Buenas prácticas implementadas:
- pausa aleatoria entre peticiones;
- reintentos con espera exponencial;
- guardado del HTML crudo para reproducibilidad;
- ausencia total de datos personales (teléfonos, nombres, IDs de usuario).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode

import requests

from src.config import (
    BASE_URL,
    CATEGORIAS,
    COLUMNAS,
    DATA_PROCESSED,
    DATA_RAW,
    DEFAULT_MAX_PAGES,
    DELAY_RANGE,
    HEADERS,
)

logger = logging.getLogger(__name__)

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
    re.DOTALL,
)


def fetch(url: str, session: requests.Session, tries: int = 4) -> str:
    """Descarga una URL con reintentos y espera exponencial."""
    last_error: Exception | None = None
    for intento in range(tries):
        try:
            respuesta = session.get(url, timeout=30)
            respuesta.raise_for_status()
            return respuesta.text
        except requests.RequestException as error:  # pragma: no cover
            last_error = error
            espera = 2**intento + random.random()
            logger.warning("Error %s; reintento en %.1f s", error, espera)
            time.sleep(espera)
    raise RuntimeError(f"No se pudo descargar {url}") from last_error


def parse_state(html: str) -> dict:
    """Devuelve el estado de Apollo embebido en la página."""
    match = NEXT_DATA_RE.search(html)
    if not match:
        raise ValueError(
            "No se encontró __NEXT_DATA__. "
            "El sitio pudo cambiar: revisa docs/metodologia.md."
        )
    data = json.loads(match.group(1))
    return data["props"]["pageProps"]["__APOLLO_STATE__"]


def _mapas_geograficos(state: dict) -> tuple[dict, dict]:
    provincias = {
        clave.split(":")[1]: valor["name"]
        for clave, valor in state.items()
        if clave.startswith("ProvinceType:")
    }
    municipios = {
        clave.split(":")[1]: valor["name"]
        for clave, valor in state.items()
        if clave.startswith("MunicipalityType:")
    }
    return provincias, municipios


def _conexion_ads(state: dict) -> dict:
    """Localiza el objeto adsPerPage(...) dentro de ROOT_QUERY."""
    for clave, valor in state.items():
        if not clave.startswith("ROOT_QUERY"):
            continue
        for subclave, subvalor in valor.items():
            if subclave.startswith("adsPerPage"):
                return subvalor
    raise ValueError("No se encontró adsPerPage en ROOT_QUERY")


def extraer_anuncios(
    state: dict,
    categoria: str,
    fecha_captura: str,
) -> list[dict]:
    """Convierte el estado de Apollo en filas tabulares."""
    provincias, municipios = _mapas_geograficos(state)
    filas: list[dict] = []

    for clave, ad in state.items():
        if not clave.startswith("AdType:"):
            continue
        filas.append(
            {
                "id": ad.get("id"),
                "categoria": categoria,
                "titulo": ad.get("title"),
                "precio": ad.get("price"),
                "moneda": ad.get("currency"),
                "provincia": provincias.get(ad.get("provinceId")),
                "municipio": municipios.get(ad.get("municipalityId")),
                "fecha_publicacion": ad.get("updatedOnToOrder"),
                "vistas": ad.get("viewCount"),
                "n_imagenes": ad.get("imagesCount"),
                "destacado": ad.get("isPromoted"),
                "url": BASE_URL + (ad.get("permalink") or ""),
                "fecha_captura": fecha_captura,
            }
        )
    return filas


def scrape_category(
    categoria: str,
    params: dict,
    max_pages: int = 1,
    session: requests.Session | None = None,
    raw_dir: Path | None = None,
    delay_range: tuple[float, float] = DELAY_RANGE,
    guardar_raw: bool = True,
) -> list[dict]:
    """Recorre las páginas de una categoría y devuelve sus anuncios."""
    if categoria not in CATEGORIAS:
        raise ValueError(f"Categoría desconocida: {categoria}")

    session = session or requests.Session()
    session.headers.update(HEADERS)
    raw_dir = raw_dir or DATA_RAW
    raw_dir.mkdir(parents=True, exist_ok=True)
    fecha_captura = datetime.now().astimezone().isoformat(timespec="seconds")

    filas: list[dict] = []
    for page in range(1, max_pages + 1):
        query = urlencode({**params, "cu": "1", "page": page})
        url = f"{BASE_URL}/search?{query}"
        logger.info("[%s] página %s → %s", categoria, page, url)

        html = fetch(url, session)

        if guardar_raw:
            destino = raw_dir / f"{categoria}_p{page:03d}.html"
            destino.write_text(html, encoding="utf-8")

        state = parse_state(html)
        filas.extend(extraer_anuncios(state, categoria, fecha_captura))

        conexion = _conexion_ads(state)
        page_info = conexion.get("pageInfo", {})
        if not page_info.get("hasNextPage", False):
            logger.info("[%s] última página alcanzada (%s)", categoria, page)
            break

        time.sleep(random.uniform(*delay_range))

    logger.info("[%s] %s anuncios recolectados", categoria, len(filas))
    return filas


def deduplicar(filas: Iterable[dict]) -> list[dict]:
    """Elimina anuncios repetidos conservando el primero visto."""
    unicos: dict[str, dict] = {}
    for fila in filas:
        unicos.setdefault(str(fila["id"]), fila)
    return list(unicos.values())


def guardar_csv(filas: list[dict], destino: Path) -> None:
    """Guarda las filas en CSV (UTF-8, compatible con Excel)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(filas)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--categorias",
        nargs="+",
        choices=list(CATEGORIAS),
        default=list(CATEGORIAS),
        help="Categorías a recolectar (por defecto: todas).",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help=f"Máximo de páginas por categoría (por defecto: {DEFAULT_MAX_PAGES}).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DATA_PROCESSED / "anuncios.csv",
        help="Ruta del CSV de salida.",
    )
    parser.add_argument(
        "--delay-min", type=float, default=DELAY_RANGE[0], help="Pausa mínima (s)."
    )
    parser.add_argument(
        "--delay-max", type=float, default=DELAY_RANGE[1], help="Pausa máxima (s)."
    )
    parser.add_argument(
        "--sin-raw",
        action="store_true",
        help="No guardar el HTML crudo de cada página.",
    )
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.max_pages < 1:
        raise SystemExit("--max-pages debe ser mayor o igual a 1.")

    session = requests.Session()
    session.headers.update(HEADERS)

    todas: list[dict] = []
    for categoria in args.categorias:
        try:
            filas = scrape_category(
                categoria=categoria,
                params=CATEGORIAS[categoria],
                max_pages=args.max_pages,
                session=session,
                delay_range=(args.delay_min, args.delay_max),
                guardar_raw=not args.sin_raw,
            )
            todas.extend(filas)
            guardar_csv(deduplicar(todas), args.out)
        except Exception:  # noqa: BLE001
            logger.exception("Falló la categoría %s; continúo con las demás", categoria)

    if not todas:
        raise SystemExit("No se recolectó ningún anuncio.")

    finales = deduplicar(todas)
    guardar_csv(finales, args.out)
    logger.info("Listo: %s anuncios únicos en %s", len(finales), args.out)


if __name__ == "__main__":
    main()
