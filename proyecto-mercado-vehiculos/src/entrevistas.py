#!/usr/bin/env python3
"""Resume las entrevistas y las triangula con los precios de Revolico.

Lee ``data/processed/entrevistas.csv`` (una fila por persona) y, si existe,
``data/processed/anuncios_limpios.csv`` para comparar la mediana de precios
pedidos con lo que declaran las personas entrevistadas.

Solo analiza las filas con ``consentimiento = si``; las demás se excluyen y se
avisa en la salida.

Escribe ``reports/entrevistas_resumen.txt``. No modifica ningún dato.

Uso:

    python -m src.entrevistas
    python -m src.entrevistas --input data/processed/entrevistas.csv
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from src.config import DATA_PROCESSED, REPORTS

MONEDAS = ("USD", "CUP", "MLC")
META_ENTREVISTAS = 30

# Campos de texto libre donde no debe aparecer un teléfono ni un correo.
CAMPOS_TEXTO_LIBRE = (
    "respuesta_abierta",
    "notas",
    "P61_mas_gusta",
    "P61_menos_gusta",
    "P62_detalle",
    "P63_motivo",
)


def columna(df: pd.DataFrame, nombre: str) -> pd.Series:
    """Devuelve la columna como texto limpio; vacía si no existe."""
    if nombre not in df.columns:
        return pd.Series([""] * len(df), index=df.index, dtype="object")
    return df[nombre].fillna("").astype(str).str.strip()


def numerico(df: pd.DataFrame, nombre: str) -> pd.Series:
    """Convierte una columna a número; los valores raros quedan en NaN."""
    return pd.to_numeric(columna(df, nombre).replace("", pd.NA), errors="coerce")


def tabla_frecuencias(df: pd.DataFrame, campos: list[str], titulo: str) -> list[str]:
    """Cuenta valores no vacíos de uno o varios campos."""
    lineas = [titulo]
    for campo in campos:
        serie = columna(df, campo)
        serie = serie[serie.ne("")]
        if serie.empty:
            continue
        lineas.append(f"  {campo}:")
        for valor, n in serie.value_counts().items():
            lineas.append(f"    {valor:<28} {n:>3}")
    return lineas


def mediana_por_moneda(df: pd.DataFrame, monto: str, moneda: str) -> list[str]:
    """Mediana y n por moneda para un par monto/moneda."""
    valores = numerico(df, monto)
    monedas = columna(df, moneda).str.upper()
    lineas = []
    for divisa in MONEDAS:
        mascara = monedas.eq(divisa) & valores.notna()
        if not mascara.any():
            continue
        datos = valores[mascara]
        lineas.append(
            f"    {divisa}: n={len(datos):>2} | mediana={datos.median():,.0f} "
            f"| rango={datos.min():,.0f}–{datos.max():,.0f}"
        )
    if not lineas:
        lineas.append("    (sin datos de monto/moneda)")
    return lineas


def avance(df: pd.DataFrame, meta: int = META_ENTREVISTAS) -> list[str]:
    """Muestra cuántas entrevistas faltan y qué códigos están libres."""
    ids = columna(df, "id_entrevista")
    registrados = set(ids[ids.ne("")])
    esperados = [f"E{n:02d}" for n in range(1, meta + 1)]
    faltan = [codigo for codigo in esperados if codigo not in registrados]
    fuera = sorted(codigo for codigo in registrados if codigo not in esperados)

    lineas = [
        "--- AVANCE HACIA LA META ---",
        f"  Meta: {meta} entrevistas | Registradas: {len(registrados)} "
        f"| Faltan: {len(faltan)}",
    ]
    if faltan:
        lineas.append(f"  Códigos pendientes: {', '.join(faltan)}")
    if fuera:
        lineas.append(f"  Aviso: códigos fuera de la meta: {', '.join(fuera)}")
    return lineas


def revisar_privacidad(df: pd.DataFrame) -> list[str]:
    """Avisa si un campo de texto libre parece contener un correo o un teléfono."""
    correo = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    telefono = re.compile(r"\+?\d[\d\s().-]{6,}\d")
    hallazgos = []

    for campo in CAMPOS_TEXTO_LIBRE:
        if campo not in df.columns:
            continue
        for posicion, valor in columna(df, campo).items():
            if not valor:
                continue
            if correo.search(valor) or telefono.search(valor):
                identificador = columna(df, "id_entrevista").get(posicion, "?")
                hallazgos.append(f"  {identificador} · {campo}: posible dato personal")

    if not hallazgos:
        return []
    return ["--- AVISO DE PRIVACIDAD ---", *hallazgos, ""]


def resumen_entrevistas(df: pd.DataFrame) -> list[str]:
    total = len(df)
    profundas = columna(df, "modalidad").str.lower().eq("profunda").sum()
    cortas = columna(df, "modalidad").str.lower().eq("corta").sum()

    lineas = [
        "=" * 78,
        "RESUMEN DE ENTREVISTAS",
        "Mercado de motos, bicicletas y patinetas · Revolico + campo",
        "=" * 78,
        f"Entrevistas registradas: {total}",
        f"  Profundas: {profundas} | Cortas: {cortas}",
        "",
    ]

    lineas += avance(df)
    lineas.append("")

    lineas += tabla_frecuencias(
        df, ["perfil", "modalidad", "provincia"], "--- PERFIL DE LA MUESTRA ---"
    )
    lineas.append("")

    lineas += tabla_frecuencias(
        df,
        ["P56_tiene_moto", "P13_tipo", "P14_condicion", "P57_condicion"],
        "--- VEHÍCULO Y CONDICIÓN ---",
    )
    lineas.append("")

    lineas += tabla_frecuencias(
        df,
        ["P01_canal", "P58_lugar", "P58_tipo_vendedor"],
        "--- CANALES DE COMPRA ---",
    )
    lineas.append("")

    lineas += tabla_frecuencias(
        df, ["P03_uso", "P09_relacion_mercado", "P28_considero_electrica"],
        "--- USO Y RELACIÓN CON EL MERCADO ---",
    )
    lineas.append("")

    lineas.append("--- PRECIO PAGADO (P16 / P59) ---")
    if columna(df, "P16_monto").ne("").any():
        lineas.append("  P16_monto:")
        lineas += mediana_por_moneda(df, "P16_monto", "P17_moneda")
    if columna(df, "P59_monto").ne("").any():
        lineas.append("  P59_monto:")
        lineas += mediana_por_moneda(df, "P59_monto", "P59_moneda")
    if not (
        columna(df, "P16_monto").ne("").any()
        or columna(df, "P59_monto").ne("").any()
    ):
        lineas.append("  (sin datos de precio pagado)")
    lineas.append("")

    lineas.append("--- GASTO MENSUAL (P60) ---")
    lineas += mediana_por_moneda(df, "P60_gasto_mes", "P60_moneda")
    lineas.append("")

    lineas += tabla_frecuencias(
        df,
        ["P62_problemas", "P62_cual", "P63_recomienda", "P61_mas_gusta"],
        "--- PROBLEMAS Y VALORACIÓN ---",
    )
    lineas.append("")

    km = numerico(df, "P21_km_dia")
    if km.notna().any():
        lineas.append("--- USO DIARIO ---")
        lineas.append(
            f"  P21_km_dia: n={km.notna().sum()} | mediana={km.median():,.0f} "
            f"| rango={km.min():,.0f}–{km.max():,.0f}"
        )
        lineas.append("")

    return lineas


def triangulacion(df: pd.DataFrame, anuncios: Path) -> list[str]:
    lineas = ["--- TRIANGULACIÓN CON ANUNCIOS (USD) ---"]
    if not anuncios.exists():
        lineas.append(f"  No existe {anuncios}; se omite la comparación.")
        return lineas

    anuncios_df = pd.read_csv(anuncios, encoding="utf-8-sig")
    if not {"categoria", "precio", "moneda"}.issubset(anuncios_df.columns):
        lineas.append("  El CSV de anuncios no tiene las columnas esperadas.")
        return lineas

    precios = pd.to_numeric(anuncios_df["precio"], errors="coerce")
    usd = anuncios_df[
        anuncios_df["moneda"].eq("USD") & precios.notna()
    ].copy()
    usd["precio"] = precios[usd.index]
    medianas = usd.groupby("categoria")["precio"].median()

    for categoria, etiqueta in (
        ("motos_combustion", "Motos combustión"),
        ("motos_electricas", "Motos eléctricas"),
    ):
        if categoria in medianas.index:
            lineas.append(
                f"  {etiqueta:<20} mediana anuncios = {medianas[categoria]:,.0f} USD"
            )

    # Entrevistas: P13_tipo + P16/P17, o P59/P59_moneda.
    tipo = columna(df, "P13_tipo").str.lower()
    montos = numerico(df, "P16_monto")
    monedas = columna(df, "P17_moneda").str.upper()
    sin_p16 = montos.isna()
    montos = montos.where(~sin_p16, numerico(df, "P59_monto"))
    monedas = monedas.where(~sin_p16, columna(df, "P59_moneda").str.upper())

    for valor, etiqueta in (
        ("combustion", "Motos combustión"),
        ("electrica", "Motos eléctricas"),
    ):
        mascara = tipo.eq(valor) & montos.notna() & monedas.eq("USD")
        if mascara.any():
            datos = montos[mascara]
            lineas.append(
                f"  {etiqueta:<20} mediana entrevistas = {datos.median():,.0f} USD "
                f"(n={len(datos)})"
            )
        else:
            lineas.append(
                f"  {etiqueta:<20} sin datos de entrevistas en USD para comparar"
            )

    lineas.append("")
    lineas.append(
        "  Recuerda: los anuncios son precios pedidos y las entrevistas son "
        "precios pagados o presupuestos declarados."
    )
    return lineas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "entrevistas.csv",
        help="CSV de entrevistas.",
    )
    parser.add_argument(
        "--anuncios",
        type=Path,
        default=DATA_PROCESSED / "anuncios_limpios.csv",
        help="CSV de anuncios limpios para la triangulación.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPORTS / "entrevistas_resumen.txt",
        help="Archivo de salida.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"No existe {args.input}.")

    df = pd.read_csv(args.input, encoding="utf-8-sig", dtype=str)

    ids = columna(df, "id_entrevista")
    duplicados = ids[ids.ne("")].duplicated().sum()
    if duplicados:
        print(f"Aviso: {duplicados} id_entrevista duplicados.")

    # Solo se analizan las filas con consentimiento firmado.
    consentimiento = columna(df, "consentimiento").str.lower()
    validas = df[consentimiento.eq("si")].copy()
    excluidas = len(df) - len(validas)

    lineas = resumen_entrevistas(validas)
    resumen_filas = [
        f"Filas en el CSV: {len(df)} | Con consentimiento: {len(validas)} "
        f"| Excluidas: {excluidas}",
    ]
    if excluidas:
        resumen_filas.append(
            "Aviso: las filas sin consentimiento firmado no se analizan."
        )
    lineas[6:6] = resumen_filas

    lineas += revisar_privacidad(df)
    lineas += triangulacion(validas, args.anuncios)
    lineas += [
        "",
        "=" * 78,
        "Nota: muestra no probabilística. Con n pequeño, las frecuencias son",
        "ilustrativas y no permiten estimar proporciones poblacionales.",
        "=" * 78,
    ]
    texto = "\n".join(lineas)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(texto + "\n", encoding="utf-8")
    print(texto)
    print(f"\nGuardado en: {args.out}")


if __name__ == "__main__":
    main()
