#!/usr/bin/env python3
"""Limpieza y enriquecimiento del CSV de anuncios.

Lee ``data/processed/anuncios_relacionados_unicos.csv``, aplica reglas de
calidad, deriva variables útiles (año, cilindrada, marca, condición, tipo) y
guarda ``data/processed/anuncios_limpios.csv``.

Uso:

    python -m src.clean
    python -m src.clean --tasa-cup 320   # opcional: convierte CUP a USD
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DATA_PROCESSED, TASA_CUP_USD_DEFECTO
from src.extraccion import (
    extraer_anio,
    extraer_cilindrada,
    extraer_condicion,
    extraer_marca,
    extraer_tipo,
)
from src.privacidad import redactar

REQUERIDAS = {
    "id",
    "categoria",
    "titulo",
    "precio",
    "moneda",
    "provincia",
    "municipio",
    "fecha_publicacion",
}


def limpiar(df: pd.DataFrame, tasa_cup_usd: float | None = None) -> pd.DataFrame:
    """Aplica el pipeline de limpieza y devuelve un DataFrame nuevo."""
    faltantes = REQUERIDAS - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas obligatorias: {sorted(faltantes)}")

    limpio = df.copy()

    for columna in ["titulo", "moneda", "provincia", "municipio", "categoria", "url"]:
        if columna in limpio.columns:
            limpio[columna] = limpio[columna].fillna("").astype(str).str.strip()
    # No guardar teléfonos ni correos en el dataset publicable.
    limpio["titulo"] = limpio["titulo"].map(redactar)

    limpio["precio"] = pd.to_numeric(limpio["precio"], errors="coerce")
    limpio["moneda"] = limpio["moneda"].str.upper()
    limpio["fecha_publicacion"] = pd.to_datetime(
        limpio["fecha_publicacion"], errors="coerce", utc=True
    )
    limpio["fecha_captura"] = pd.to_datetime(
        limpio["fecha_captura"], errors="coerce", utc=True
    )

    # 1) Precios nulos o señuelo (1 USD suele ser un placeholder).
    validos = limpio["precio"].notna() & limpio["precio"].between(5, 1_000_000)
    descartados_precio = int((~validos).sum())
    limpio = limpio[validos].copy()

    # 2) Duplicados exactos por id y por título + precio + municipio.
    limpio = limpio.sort_values(
        "fecha_publicacion", ascending=False, na_position="last"
    )
    limpio = limpio.drop_duplicates(subset="id", keep="first")
    clave = (
        limpio["titulo"].str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
        + "|"
        + limpio["precio"].round(2).astype(str)
        + "|"
        + limpio["municipio"].str.lower()
    )
    limpio["_clave_duplicado"] = clave
    limpio = limpio.drop_duplicates("_clave_duplicado").drop(
        columns="_clave_duplicado"
    )

    # 3) Variables derivadas del texto.
    limpio["anio"] = pd.to_numeric(limpio["titulo"].map(extraer_anio), errors="coerce")
    limpio["cilindrada_cc"] = pd.to_numeric(
        limpio["titulo"].map(extraer_cilindrada), errors="coerce"
    )
    limpio["condicion"] = limpio["titulo"].map(extraer_condicion)
    limpio["tipo"] = [
        extraer_tipo(titulo, categoria)
        for titulo, categoria in zip(limpio["titulo"], limpio["categoria"])
    ]
    limpio["marca"] = limpio["titulo"].map(extraer_marca)

    # 4) Precio comparable en USD (opcional).
    limpio["precio_usd"] = np.where(
        limpio["moneda"].eq("USD"), limpio["precio"], np.nan
    )
    if tasa_cup_usd:
        en_cup = limpio["moneda"].eq("CUP")
        limpio.loc[en_cup, "precio_usd"] = limpio.loc[en_cup, "precio"] / tasa_cup_usd

    limpio = limpio.reset_index(drop=True)
    limpio.attrs["descartados_precio"] = descartados_precio
    return limpio


def resumen(df: pd.DataFrame) -> None:
    """Imprime un chequeo rápido del dataset limpio."""
    print(f"Anuncios limpios: {len(df)}")
    print(f"Descartados por precio nulo/señuelo: {df.attrs.get('descartados_precio', 0)}")
    print("\nPor categoría:")
    print(df["categoria"].value_counts().to_string())
    print("\nPor moneda:")
    print(df["moneda"].value_counts(dropna=False).to_string())
    print("\nNulos por columna (top 12):")
    print(df.isna().sum().sort_values(ascending=False).head(12).to_string())

    if df["precio_usd"].notna().any():
        print("\nPrecio en USD:")
        print(df["precio_usd"].describe().to_string())
    else:
        print("\nNo hay precios en USD; revisa la columna 'moneda'.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios_relacionados_unicos.csv",
        help="CSV de entrada (por defecto, el dataset del mercado).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_PROCESSED / "anuncios_limpios.csv",
        help="CSV de salida.",
    )
    parser.add_argument(
        "--tasa-cup",
        type=float,
        default=TASA_CUP_USD_DEFECTO,
        help="CUP por 1 USD. Si se indica, convierte los anuncios en CUP.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(
            f"No existe {args.input}. Ejecuta primero el scraper:\n"
            "  python -m src.scraper --max-pages 1"
        )

    df = pd.read_csv(args.input)
    limpio = limpiar(df, tasa_cup_usd=args.tasa_cup)
    resumen(limpio)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    limpio.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"\nGuardado en {args.output}")


if __name__ == "__main__":
    main()
