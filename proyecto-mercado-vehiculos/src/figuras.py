#!/usr/bin/env python3
"""Genera las figuras del informe a partir del dataset enriquecido.

Lee ``data/processed/anuncios_enriquecidos.csv`` y guarda PNG en
``reports/figures/``. No modifica los datos.

Uso:

    python -m src.figuras
    python -m src.figuras --input data/processed/anuncios_enriquecidos.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.config import DATA_PROCESSED, FIGURES

PRECIO_MINIMO = 5
PRECIO_MAXIMO = 1_000_000
MONEDA = "USD"

COLOR_MOTO = "#c0392b"
COLOR_BICI = "#2471a3"
COLOR_PATINETA = "#e67e22"

PALETA = {
    "motos_combustion": COLOR_MOTO,
    "motos_electricas": "#e74c3c",
    "bicicletas": COLOR_BICI,
    "patinetas": COLOR_PATINETA,
}

ETIQUETAS = {
    "motos_combustion": "Motos combustión",
    "motos_electricas": "Motos eléctricas",
    "bicicletas": "Bicicletas",
    "patinetas": "Patinetas",
}


def cargar(ruta: Path) -> pd.DataFrame:
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df.loc[
        (df["precio"] < PRECIO_MINIMO) | (df["precio"] >= PRECIO_MAXIMO), "precio"
    ] = pd.NA
    df["anio"] = pd.to_numeric(df.get("anio"), errors="coerce")
    df["cilindrada_cc"] = pd.to_numeric(df.get("cilindrada_cc"), errors="coerce")
    df["categoria_etiqueta"] = df["categoria"].map(ETIQUETAS).fillna(df["categoria"])
    return df


def guardar(fig: plt.Figure, nombre: str, figuras: Path) -> None:
    figuras.mkdir(parents=True, exist_ok=True)
    ruta = figuras / nombre
    fig.tight_layout()
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  {ruta.name}")


def fig_anuncios_categoria(df: pd.DataFrame, figuras: Path) -> None:
    conteo = df["categoria_etiqueta"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4))
    colores = [PALETA.get(c, "#7f8c8d") for c in df["categoria"].value_counts().index]
    ax.bar(conteo.index, conteo.values, color=colores)
    for i, valor in enumerate(conteo.values):
        ax.text(i, valor + max(conteo.values) * 0.01, f"{valor:,}", ha="center", fontsize=9)
    ax.set_title("Anuncios por categoría")
    ax.set_ylabel("Anuncios")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=15)
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig01_anuncios_categoria.png", figuras)


def fig_provincia(df: pd.DataFrame, figuras: Path) -> None:
    conteo = df["provincia"].fillna("(sin provincia)").value_counts().head(10)[::-1]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(conteo.index, conteo.values, color="#5d6d7e")
    for i, valor in enumerate(conteo.values):
        ax.text(valor, i, f" {valor:,}", va="center", fontsize=8)
    ax.set_title("Anuncios por provincia (top 10)")
    ax.set_xlabel("Anuncios")
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig02_provincia.png", figuras)


def fig_precio_categoria(df: pd.DataFrame, figuras: Path) -> None:
    datos = df[(df["moneda"] == MONEDA) & df["precio"].notna()]
    orden = [c for c in ETIQUETAS if c in datos["categoria"].unique()]
    grupos = [datos.loc[datos["categoria"] == c, "precio"] for c in orden]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    caja = ax.boxplot(
        grupos,
        tick_labels=[ETIQUETAS[c] for c in orden],
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for parche, categoria in zip(caja["boxes"], orden):
        parche.set_facecolor(PALETA[categoria])
        parche.set_alpha(0.75)
    ax.set_yscale("log")
    ax.set_title(f"Distribución del precio pedido por categoría ({MONEDA})")
    ax.set_ylabel(f"Precio ({MONEDA}, escala log)")
    ax.tick_params(axis="x", rotation=15)
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig03_precio_categoria.png", figuras)


def fig_precio_histograma(df: pd.DataFrame, figuras: Path) -> None:
    datos = df[(df["moneda"] == MONEDA) & df["precio"].notna()]["precio"]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bins = pd.Series(datos).apply("log10").pipe(
        lambda s: pd.np.linspace(s.min(), s.max(), 40)
    ) if hasattr(pd, "np") else None
    # Sin depender de pd.np: construimos los bordes en escala logarítmica.
    import numpy as np

    bordes = np.logspace(
        np.log10(max(datos.min(), 1)), np.log10(datos.max()), 40
    )
    ax.hist(datos, bins=bordes, color="#34495e", edgecolor="white")
    ax.set_xscale("log")
    ax.set_title(f"Distribución del precio pedido en {MONEDA} (escala log)")
    ax.set_xlabel(f"Precio ({MONEDA}, escala log)")
    ax.set_ylabel("Anuncios")
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig04_precio_histograma.png", figuras)


def fig_precio_anio(df: pd.DataFrame, figuras: Path) -> None:
    motos = df[
        df["categoria"].str.startswith("motos")
        & (df["moneda"] == MONEDA)
        & df["precio"].notna()
        & df["anio"].notna()
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(
        motos["anio"],
        motos["precio"],
        s=18,
        alpha=0.45,
        color=COLOR_MOTO,
        edgecolor="none",
    )
    ax.set_yscale("log")
    ax.set_title("Precio pedido vs. año en motos")
    ax.set_xlabel("Año")
    ax.set_ylabel(f"Precio ({MONEDA}, escala log)")
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig05_precio_anio.png", figuras)


def fig_precio_condicion(df: pd.DataFrame, figuras: Path) -> None:
    motos = df[
        df["categoria"].str.startswith("motos")
        & (df["moneda"] == MONEDA)
        & df["precio"].notna()
        & df["condicion"].ne("no_especificada")
    ]
    orden = [c for c in ("nueva", "seminueva", "usada") if c in motos["condicion"].unique()]
    if not orden:
        return
    grupos = [motos.loc[motos["condicion"] == c, "precio"] for c in orden]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    caja = ax.boxplot(
        grupos,
        tick_labels=orden,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for parche in caja["boxes"]:
        parche.set_facecolor("#95a5a6")
        parche.set_alpha(0.8)
    ax.set_title(f"Precio pedido por condición en motos ({MONEDA})")
    ax.set_ylabel(f"Precio ({MONEDA})")
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig06_precio_condicion.png", figuras)


def fig_marcas(df: pd.DataFrame, figuras: Path) -> None:
    conteo = df["marca"].dropna().value_counts().head(15)[::-1]
    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.barh(conteo.index, conteo.values, color="#2874a6")
    for i, valor in enumerate(conteo.values):
        ax.text(valor, i, f" {valor:,}", va="center", fontsize=8)
    ax.set_title("Marcas con más anuncios (top 15)")
    ax.set_xlabel("Anuncios")
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig07_marcas.png", figuras)


def fig_precio_marca(df: pd.DataFrame, figuras: Path) -> None:
    datos = df[(df["moneda"] == MONEDA) & df["precio"].notna() & df["marca"].notna()]
    resumen = (
        datos.groupby("marca")["precio"]
        .agg(["median", "count"])
        .query("count >= 20")
        .sort_values("median")
    )
    if resumen.empty:
        return
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    ax.barh(resumen.index, resumen["median"], color="#16a085")
    for i, valor in enumerate(resumen["median"]):
        ax.text(valor, i, f" {valor:,.0f}", va="center", fontsize=8)
    ax.set_title(f"Precio mediano por marca ({MONEDA}, n ≥ 20)")
    ax.set_xlabel(f"Precio mediano ({MONEDA})")
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig08_precio_marca.png", figuras)


def fig_precio_provincia(df: pd.DataFrame, figuras: Path) -> None:
    datos = df[(df["moneda"] == MONEDA) & df["precio"].notna() & df["provincia"].notna()]
    resumen = (
        datos.groupby("provincia")["precio"]
        .agg(["median", "count"])
        .query("count >= 10")
        .sort_values("median")
    )
    if resumen.empty:
        return
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.barh(resumen.index, resumen["median"], color="#8e44ad")
    for i, valor in enumerate(resumen["median"]):
        ax.text(valor, i, f" {valor:,.0f}", va="center", fontsize=8)
    ax.set_title(f"Precio mediano por provincia ({MONEDA}, n ≥ 10)")
    ax.set_xlabel(f"Precio mediano ({MONEDA})")
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig09_precio_provincia.png", figuras)


def fig_precio_cilindrada(df: pd.DataFrame, figuras: Path) -> None:
    motos = df[
        df["categoria"].str.startswith("motos")
        & (df["moneda"] == MONEDA)
        & df["precio"].notna()
        & df["cilindrada_cc"].notna()
    ].copy()
    if motos.empty:
        return
    bordes = [0, 100, 150, 200, 250, 10_000]
    etiquetas = ["<100", "100-149", "150-199", "200-249", "250+"]
    motos["tramo"] = pd.cut(
        motos["cilindrada_cc"], bins=bordes, labels=etiquetas, right=False
    )
    orden = [e for e in etiquetas if (motos["tramo"] == e).any()]
    grupos = [motos.loc[motos["tramo"] == e, "precio"] for e in orden]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    caja = ax.boxplot(
        grupos,
        tick_labels=[f"{e} cc" for e in orden],
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for parche in caja["boxes"]:
        parche.set_facecolor(COLOR_MOTO)
        parche.set_alpha(0.7)
    ax.set_title(f"Precio pedido por cilindrada en motos ({MONEDA})")
    ax.set_xlabel("Cilindrada")
    ax.set_ylabel(f"Precio ({MONEDA})")
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    guardar(fig, "fig10_precio_cilindrada.png", figuras)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios_enriquecidos.csv",
        help="CSV enriquecido de entrada.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=FIGURES,
        help="Carpeta de figuras.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(
            f"No existe {args.input}. Ejecuta primero:\n  python -m src.enriquecer"
        )

    df = cargar(args.input)
    print(f"Anuncios: {len(df)}")
    print("Generando figuras:")
    fig_anuncios_categoria(df, args.out)
    fig_provincia(df, args.out)
    fig_precio_categoria(df, args.out)
    fig_precio_histograma(df, args.out)
    fig_precio_anio(df, args.out)
    fig_precio_condicion(df, args.out)
    fig_marcas(df, args.out)
    fig_precio_marca(df, args.out)
    fig_precio_provincia(df, args.out)
    fig_precio_cilindrada(df, args.out)
    print(f"Guardadas en: {args.out}")


if __name__ == "__main__":
    main()
