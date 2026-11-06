#!/usr/bin/env python3
"""Análisis descriptivo del mercado de motos, bicicletas y patinetas.

Lee por defecto ``data/processed/anuncios_relacionados_unicos.csv``, deriva
marca, año, condición, cilindrada y tipo, y escribe un informe de texto en
``reports/analisis_basico.txt``.

Solo usa la librería estándar: sirve para explorar el dataset antes de instalar
pandas o abrir los notebooks.

Uso:

    python -m src.analisis_basico
    python -m src.analisis_basico --input data/processed/anuncios_enriquecidos.csv
"""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from src.config import DATA_PROCESSED, REPORTS
from src.extraccion import CAMPOS_DERIVADOS, enriquecer_fila, normalizar
from src.privacidad import redactar

# Precios fuera de este rango se excluyen de los estadísticos:
# por debajo de 5 son señuelos; por encima de un millón, errores de captura.
PRECIO_MINIMO = 5
PRECIO_MAXIMO = 1_000_000
GRUPO_MINIMO = 10
MONEDA_ANALISIS = "USD"

PALABRAS_RUIDO = [
    "repuesto",
    "pieza",
    "casco",
    "gasolina",
    "carro",
    "extractor",
    "lavadora",
    "nevera",
    "aire acondicionado",
    "planta",
    "bomba",
]


# --- Utilidades ------------------------------------------------------------


def leer_filas(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def precio_valido(fila: dict) -> float | None:
    """Precio utilizable para estadísticos, o ``None`` si es nulo o atípico."""
    try:
        precio = float(fila.get("precio") or "")
    except ValueError:
        return None
    if PRECIO_MINIMO <= precio < PRECIO_MAXIMO:
        return precio
    return None


def precios(filas: list[dict], moneda: str) -> list[float]:
    valores = []
    for fila in filas:
        if (fila.get("moneda") or "") != moneda:
            continue
        precio = precio_valido(fila)
        if precio is not None:
            valores.append(precio)
    return valores


def percentil(valores: list[float], p: float) -> float:
    ordenados = sorted(valores)
    if len(ordenados) == 1:
        return ordenados[0]
    posicion = (len(ordenados) - 1) * p
    inferior = int(posicion)
    superior = min(inferior + 1, len(ordenados) - 1)
    if inferior == superior:
        return ordenados[inferior]
    return ordenados[inferior] + (ordenados[superior] - ordenados[inferior]) * (
        posicion - inferior
    )


def describir(valores: list[float]) -> dict:
    return {
        "n": len(valores),
        "min": min(valores),
        "p25": percentil(valores, 0.25),
        "mediana": statistics.median(valores),
        "p75": percentil(valores, 0.75),
        "max": max(valores),
    }


def formatear(estadisticos: dict) -> str:
    return (
        f"n={estadisticos['n']:<4} "
        f"mín={estadisticos['min']:>8,.0f} "
        f"p25={estadisticos['p25']:>8,.0f} "
        f"mediana={estadisticos['mediana']:>8,.0f} "
        f"p75={estadisticos['p75']:>8,.0f} "
        f"máx={estadisticos['max']:>9,.0f}"
    )


def pearson(xs: list[float], ys: list[float]) -> float | None:
    """Correlación de Pearson; ``None`` si no hay suficientes datos."""
    n = len(xs)
    if n < 3:
        return None
    media_x = sum(xs) / n
    media_y = sum(ys) / n
    numerador = sum((x - media_x) * (y - media_y) for x, y in zip(xs, ys))
    varianza_x = sum((x - media_x) ** 2 for x in xs)
    varianza_y = sum((y - media_y) ** 2 for y in ys)
    denominador = (varianza_x * varianza_y) ** 0.5
    return numerador / denominador if denominador else None


def tabla_precios_por_grupo(
    filas: list[dict],
    campo: str,
    moneda: str = MONEDA_ANALISIS,
    minimo: int = GRUPO_MINIMO,
    transformar=None,
) -> list[tuple[str, dict]]:
    """Mediana de precio por grupo, solo con grupos de tamaño suficiente."""
    grupos: dict[str, list[float]] = defaultdict(list)
    for fila in filas:
        valor = fila.get(campo)
        if valor in (None, ""):
            continue
        precio = precio_valido(fila)
        if precio is None or (fila.get("moneda") or "") != moneda:
            continue
        clave = transformar(valor) if transformar else str(valor)
        grupos[clave].append(precio)

    resultado = [
        (clave, describir(valores))
        for clave, valores in grupos.items()
        if len(valores) >= minimo
    ]
    return sorted(resultado, key=lambda par: par[1]["mediana"], reverse=True)


def tramo_anio(anio: int) -> str:
    if anio <= 2015:
        return "≤2015"
    if anio <= 2019:
        return "2016-2019"
    if anio <= 2022:
        return "2020-2022"
    if anio <= 2025:
        return "2023-2025"
    return "2026"


def tramo_cilindrada(cc: int) -> str:
    if cc < 100:
        return "<100 cc"
    if cc < 150:
        return "100-149 cc"
    if cc < 200:
        return "150-199 cc"
    if cc < 250:
        return "200-249 cc"
    return "250+ cc"


# Categorías de Revolico agrupadas por producto. "motos" incluye combustión y
# eléctricas; bicicletas y patinetas van aparte porque sus precios no son
# comparables con los de una moto.
GRUPOS_PRODUCTO: list[tuple[str, tuple[str, ...]]] = [
    ("motos", ("motos_combustion", "motos_electricas")),
    ("bicicletas", ("bicicletas",)),
    ("patinetas", ("patinetas",)),
]

# Valores que indican "no se pudo extraer", no un dato real.
SIN_DATO = {"", "no_especificada", "otra/no identificada"}


def filas_del_grupo(filas: list[dict], categorias: tuple[str, ...]) -> list[dict]:
    return [f for f in filas if f.get("categoria") in categorias]


def es_informativo(campo: str, valor: object) -> bool:
    """``True`` si la variable derivada aporta información real.

    ``condicion`` y ``tipo`` valen ``no_especificada`` cuando el título no da
    señal: eso es un hueco, no una categoría observada.
    """
    if valor in (None, ""):
        return False
    return normalizar(valor) not in SIN_DATO


# --- Informe ---------------------------------------------------------------


def generar_reporte(filas: list[dict], ruta: Path) -> str:
    lineas: list[str] = []
    agregar = lineas.append

    filas = [{**f, "titulo": redactar(f.get("titulo", "")), **enriquecer_fila(f)} for f in filas]
    total = len(filas)

    agregar("=" * 78)
    agregar("ANÁLISIS DESCRIPTIVO DEL MERCADO")
    agregar("Motos, bicicletas y patinetas · Revolico")
    agregar("=" * 78)
    agregar(f"Archivo: {ruta}")
    agregar(f"Anuncios: {total}")
    if not filas:
        return "\n".join(lineas)

    fechas = sorted(f.get("fecha_publicacion", "") for f in filas if f.get("fecha_publicacion"))
    capturas = sorted(f.get("fecha_captura", "") for f in filas if f.get("fecha_captura"))
    if fechas:
        agregar(f"Publicación: {fechas[0][:10]} → {fechas[-1][:10]}")
    if capturas:
        agregar(f"Captura: {capturas[0]} → {capturas[-1]}")

    # --- Composición ---
    agregar("\n--- COMPOSICIÓN ---")
    agregar("Por categoría:")
    for nombre, n in Counter(f.get("categoria", "") for f in filas).most_common():
        agregar(f"  {nombre:<20} {n:>6} ({n / total:.1%})")
    agregar("Por moneda:")
    for nombre, n in Counter(f.get("moneda") or "(vacía)" for f in filas).most_common():
        agregar(f"  {nombre:<20} {n:>6} ({n / total:.1%})")
    agregar("Top 10 provincias:")
    for nombre, n in Counter(f.get("provincia") or "(sin provincia)" for f in filas).most_common(10):
        agregar(f"  {nombre:<20} {n:>6} ({n / total:.1%})")
    agregar("Top 10 municipios:")
    for nombre, n in Counter(f.get("municipio") or "(sin municipio)" for f in filas).most_common(10):
        agregar(f"  {nombre:<20} {n:>6} ({n / total:.1%})")

    # --- Calidad ---
    agregar("\n--- CALIDAD DE DATOS ---")
    agregar("Nulos por columna:")
    for columna in filas[0].keys():
        if columna in CAMPOS_DERIVADOS:
            continue
        nulos = sum(1 for f in filas if not (f.get(columna) or "").strip())
        if nulos:
            agregar(f"  {columna:<20} {nulos:>6} ({nulos / total:.1%})")

    ids = Counter(f.get("id") for f in filas)
    claves = Counter(
        (normalizar(f.get("titulo")), str(f.get("precio", "")), normalizar(f.get("municipio")))
        for f in filas
    )
    agregar(f"IDs duplicados: {sum(1 for n in ids.values() if n > 1)}")
    agregar(f"Duplicados por título+precio+municipio: {sum(1 for n in claves.values() if n > 1)}")

    sospechosos = [f for f in filas if (f.get("precio") or "").isdigit() and int(f["precio"]) < PRECIO_MINIMO]
    absurdos = [f for f in filas if (f.get("precio") or "").isdigit() and int(f["precio"]) >= PRECIO_MAXIMO]
    agregar(f"Precios < {PRECIO_MINIMO} (posibles señuelo): {len(sospechosos)}")
    agregar(f"Precios ≥ {PRECIO_MAXIMO:,} (posibles errores): {len(absurdos)}")

    agregar("\nRuido en títulos:")
    for palabra in PALABRAS_RUIDO:
        n = sum(1 for f in filas if palabra in normalizar(f.get("titulo")))
        if n:
            agregar(f"  '{palabra}': {n}")

    # --- Cobertura de variables derivadas ---
    agregar("\n--- COBERTURA DE VARIABLES DERIVADAS ---")
    for campo in CAMPOS_DERIVADOS:
        llenos = sum(1 for f in filas if es_informativo(campo, f.get(campo)))
        agregar(f"  {campo:<15} {llenos:>6} / {total} ({llenos / total:.1%})")
    agregar("  (solo valores informativos: 'no_especificada' cuenta como nulo)")

    # --- Precios ---
    agregar("\n--- PRECIOS ---")
    for moneda in sorted({f.get("moneda") or "" for f in filas}):
        valores = precios(filas, moneda)
        if valores:
            agregar(f"{moneda or '(sin moneda)'}: {formatear(describir(valores))}")

    agregar(f"\nPrecios por categoría y moneda ({MONEDA_ANALISIS} y CUP):")
    for moneda in (MONEDA_ANALISIS, "CUP"):
        for categoria in sorted({f.get("categoria", "") for f in filas}):
            valores = [
                precio_valido(f)
                for f in filas
                if f.get("categoria") == categoria and (f.get("moneda") or "") == moneda
            ]
            valores = [v for v in valores if v is not None]
            if len(valores) >= GRUPO_MINIMO:
                agregar(f"  {categoria:<18} {moneda:<4} {formatear(describir(valores))}")

    # --- Marcas ---
    agregar("\n--- MARCAS ---")
    marcas = Counter(f["marca"] for f in filas if f.get("marca"))
    agregar(f"Marcas identificadas: {sum(marcas.values())} de {total} ({sum(marcas.values()) / total:.1%})")
    for marca, n in marcas.most_common(20):
        agregar(f"  {marca:<18} {n:>6}")

    agregar(f"\nTop 5 marcas por producto (precio mediano en {MONEDA_ANALISIS}, n ≥ {GRUPO_MINIMO}):")
    for categoria in ("motos_combustion", "motos_electricas", "bicicletas", "patinetas"):
        del_producto = [f for f in filas if f.get("categoria") == categoria]
        conteo = Counter(f["marca"] for f in del_producto if f.get("marca")).most_common(5)
        if not conteo:
            continue
        agregar(f"  {categoria}:")
        for marca, n in conteo:
            valores = [
                precio_valido(f)
                for f in del_producto
                if f.get("marca") == marca and (f.get("moneda") or "") == MONEDA_ANALISIS
            ]
            valores = [v for v in valores if v is not None]
            mediana = f"{statistics.median(valores):,.0f}" if valores else "s/d"
            agregar(f"    {marca:<16} n={n:<4} mediana={mediana}")

    agregar(f"\nPrecio mediano por marca ({MONEDA_ANALISIS}, n ≥ 20):")
    tabla = tabla_precios_por_grupo(filas, "marca", minimo=20)
    if not tabla:
        agregar("  (sin grupos suficientes)")
    for marca, est in tabla[:15]:
        agregar(f"  {marca:<18} {formatear(est)}")

    # --- Condición ---
    agregar("\n--- CONDICIÓN ---")
    agregar("Con condición declarada en el título:")
    condiciones = Counter(
        f["condicion"] for f in filas if es_informativo("condicion", f.get("condicion"))
    )
    declaradas = sum(condiciones.values())
    agregar(f"  declaradas: {declaradas} de {total} ({declaradas / total:.1%})")
    for condicion, n in condiciones.most_common():
        agregar(f"  {condicion:<18} {n:>6}")

    # La condición mezcla motos de 60 USD con bicicletas de 160 USD, así que
    # solo tiene sentido compararla dentro de cada producto.
    for grupo, categorias in GRUPOS_PRODUCTO:
        del_grupo = filas_del_grupo(filas, categorias)
        tabla = tabla_precios_por_grupo(del_grupo, "condicion")
        if not tabla:
            continue
        agregar(f"\nPrecio mediano por condición en {grupo} ({MONEDA_ANALISIS}, n ≥ {GRUPO_MINIMO}):")
        for condicion, est in tabla:
            agregar(f"  {condicion:<18} {formatear(est)}")

    # --- Tipo ---
    agregar("\n--- TIPO DE PROPULSIÓN ---")
    for tipo, n in Counter(f["tipo"] for f in filas).most_common():
        agregar(f"  {tipo:<18} {n:>6} ({n / total:.1%})")

    # Igual que la condición: comparar combustión con bicicletas no dice nada.
    for grupo, categorias in GRUPOS_PRODUCTO:
        del_grupo = filas_del_grupo(filas, categorias)
        tabla = tabla_precios_por_grupo(del_grupo, "tipo")
        if not tabla:
            continue
        agregar(f"\nPrecio mediano por tipo en {grupo} ({MONEDA_ANALISIS}, n ≥ {GRUPO_MINIMO}):")
        for tipo, est in tabla:
            agregar(f"  {tipo:<18} {formatear(est)}")

    # --- Año ---
    # El año solo se extrae de forma fiable en motos: en bicicletas y patinetas
    # los números de 4 cifras suelen ser precios o modelos, no años.
    agregar("\n--- AÑO ---")
    motos = filas_del_grupo(filas, ("motos_combustion", "motos_electricas"))
    anios = [int(f["anio"]) for f in motos if f.get("anio") not in (None, "")]
    agregar(f"Con año extraído en motos: {len(anios)} de {len(motos)} ({len(anios) / len(motos):.1%})")
    if anios:
        agregar(f"Rango: {min(anios)} → {max(anios)} | mediana: {statistics.median(anios):.0f}")

    agregar(f"\nPrecio mediano por tramo de año en motos ({MONEDA_ANALISIS}, n ≥ {GRUPO_MINIMO}):")
    orden_anios = ["≤2015", "2016-2019", "2020-2022", "2023-2025", "2026"]
    tabla_anios = dict(tabla_precios_por_grupo(motos, "anio", transformar=tramo_anio))
    if not tabla_anios:
        agregar("  (sin grupos suficientes)")
    for tramo in orden_anios:
        if tramo in tabla_anios:
            agregar(f"  {tramo:<12} {formatear(tabla_anios[tramo])}")

    # --- Cilindrada ---
    agregar("\n--- CILINDRADA ---")
    cilindradas = [int(f["cilindrada_cc"]) for f in motos if f.get("cilindrada_cc") not in (None, "")]
    agregar(f"Con cilindrada extraída en motos: {len(cilindradas)} de {len(motos)} ({len(cilindradas) / len(motos):.1%})")
    if cilindradas:
        agregar(f"Rango: {min(cilindradas)} → {max(cilindradas)} cc | mediana: {statistics.median(cilindradas):.0f}")

    agregar(f"\nPrecio mediano por cilindrada en motos ({MONEDA_ANALISIS}, n ≥ {GRUPO_MINIMO}):")
    orden_cc = ["<100 cc", "100-149 cc", "150-199 cc", "200-249 cc", "250+ cc"]
    tabla_cc = dict(tabla_precios_por_grupo(motos, "cilindrada_cc", transformar=tramo_cilindrada))
    if not tabla_cc:
        agregar("  (sin grupos suficientes)")
    for tramo in orden_cc:
        if tramo in tabla_cc:
            agregar(f"  {tramo:<14} {formatear(tabla_cc[tramo])}")

    # --- Relaciones ---
    agregar("\n--- RELACIONES (Pearson, solo motos en USD) ---")
    pares = [
        ("año", "anio"),
        ("cilindrada", "cilindrada_cc"),
    ]
    for etiqueta, campo in pares:
        xs, ys = [], []
        for fila in motos:
            valor = fila.get(campo)
            precio = precio_valido(fila)
            if valor in (None, "") or precio is None:
                continue
            if (fila.get("moneda") or "") != MONEDA_ANALISIS:
                continue
            xs.append(float(valor))
            ys.append(precio)
        r = pearson(xs, ys)
        if r is None:
            agregar(f"  {etiqueta:<12} sin datos suficientes")
        else:
            agregar(f"  {etiqueta:<12} r={r:+.3f}  n={len(xs)}")

    # --- Interés ---
    agregar("\n--- INTERÉS Y EXPOSICIÓN ---")
    vistas = [int(f["vistas"]) for f in filas if (f.get("vistas") or "").isdigit()]
    imagenes = [int(f["n_imagenes"]) for f in filas if (f.get("n_imagenes") or "").isdigit()]
    if vistas:
        agregar(f"Vistas: mediana={statistics.median(vistas):.0f} | máx={max(vistas)}")
    if imagenes:
        agregar(f"Imágenes: mediana={statistics.median(imagenes):.0f} | máx={max(imagenes)}")
    destacados = sum(1 for f in filas if (f.get("destacado") or "").lower() == "true")
    agregar(f"Anuncios destacados: {destacados} ({destacados / total:.1%})")

    agregar("\n--- NOTAS ---")
    agregar("- Son precios pedidos, no precios de transacción.")
    agregar("- Los estadísticos usan un rango de 5 a 1 000 000 para excluir señuelos y errores.")
    agregar("- No mezclar USD y CUP sin una tasa documentada; los cruces usan USD.")
    agregar("- Los grupos con n < 10 no son concluyentes.")
    agregar("- La muestra es no probabilística y está concentrada en La Habana.")

    return "\n".join(lineas)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios_relacionados_unicos.csv",
        help="CSV de anuncios del mercado.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPORTS / "analisis_basico.txt",
        help="Archivo de salida.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(
            f"No existe {args.input}. Ejecuta primero:\n  python -m src.relevancia"
        )

    filas = leer_filas(args.input)
    reporte = generar_reporte(filas, args.input)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(reporte, encoding="utf-8")
    print(reporte)
    print(f"\nGuardado en: {args.out}")


if __name__ == "__main__":
    main()
