#!/usr/bin/env python3
"""Identifica anuncios relacionados con motos, bicicletas y patinetas.

El scraper recorre categorías que pueden contener ruido: repuestos, accesorios,
gasolina, otros vehículos o electrodomésticos. Este script clasifica cada
anuncio en tres grupos:

- ``si``: relacionado con el tema.
- ``revisar``: ambiguo; conviene mirarlo a mano.
- ``no``: claramente ajeno.

Además, crea una copia de los anuncios relacionados y una versión sin
duplicados:

- ``data/processed/anuncios_relacionados.csv``
- ``data/processed/anuncios_relacionados_unicos.csv``
- ``data/processed/anuncios_revisar.csv``
- ``data/processed/anuncios_excluidos.csv``
- ``reports/relevancia_resumen.txt``

Uso:

    python -m src.relevancia
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

from src.config import DATA_PROCESSED, REPORTS
from src.extraccion import normalizar
from src.privacidad import redactar

# --- Vocabulario -----------------------------------------------------------

PRODUCTOS = {
    "moto": [
        "moto",
        "motocicleta",
        "motoneta",
        "motico",
        "bimoto",
        "bicimoto",
        "velomotor",
        "ciclomotor",
    ],
    "bicicleta": [
        "bici",
        "bicicleta",
        "rodada",
        "mtb",
        "bmx",
        "montana",
        "montaña",
        "ruta",
        "fixie",
        "urbana",
        "paseo",
        "infantil",
    ],
    "patineta": [
        "patineta",
        "parineta",
        "patinenta",
        "patinete",
        "scooter",
        "skate",
        "longboard",
        "monopatin",
        "monopatín",
    ],
}

MARCAS = [
    "harley",
    "specialized",
    "motorstreck",
    "mishozuki",
    "silver bike",
    "kawasaki",
    "yamaha",
    "suzuki",
    "honda",
    "lifan",
    "krathos",
    "trapper",
    "xmotors",
    "flamingo",
    "lexzuki",
    "benelli",
    "piaggio",
    "hongli",
    "unison",
    "topman",
    "topmaq",
    "katzu",
    "italy",
    "rali",
    "huffy",
    "muniao",
    "myniao",
    "vivamax",
    "jinghan",
    "giant",
    "trek",
    "xiaomi",
    "werhy",
    "yoazaky",
    "haojue",
    "zontes",
    "ducati",
    "vespa",
    "bera",
    "ava",
    "tank",
    "jin",
    "jmd",
    "ktm",
    "bmw",
    "izuki",
    "isuki",
    "galactica",
    "jupiter",
    "aquila",
    "halcon",
    "restrepa",
    "panther",
    "zusuki",
]

RUIDO_FUERTE = [
    "repuesto",
    "repuestos",
    "lavadora",
    "nevera",
    "aire acondicionado",
    "planta",
    "generador",
    "inversor",
    "extractor",
    "adorno",
    "adornos",
    "juguete",
    "camion",
    "trailer",
    "carreta",
]

# Palabras que pueden ser una característica del vehículo o un ruido.
# Solo se tratan como ruido cuando el título no nombra el producto.
RUIDO_CONTEXTUAL = [
    "gasolina",
    "bateria",
    "baterias",
    "motor",
    "aceite",
    "lubricante",
    "bujia",
    "carburador",
    "escape",
    "espejo",
    "espejos",
    "cubierta",
    "cubiertas",
    "llanta",
    "llantas",
    "rin",
    "rines",
    "aro",
    "rayo",
    "cadena",
    "freno",
    "frenos",
    "sillin",
    "manubrio",
    "horquilla",
    "amortiguador",
    "casco",
    "cascos",
    "accesorio",
    "accesorios",
    "pieza",
    "piezas",
    "carro",
    "auto",
    "autos",
    "pila",
    "pilas",
    "cargador",
    "cargadores",
    "luz",
    "luces",
    "bocina",
    "mppt",
    "controlador",
    "cable",
    "cables",
    "goma",
    "gomas",
    "camara",
    "camaras",
    "pedal",
    "pedales",
    "timbre",
    "asiento",
    "forro",
    "guantilla",
    "guantillas",
    "candado",
    "candados",
    "triplato",
    "triplatos",
    "biela",
    "bielas",
    "pedalier",
    "pinon",
    "pinones",
    "cassette",
    "desviador",
]

CATEGORIA_A_PRODUCTO = {
    "motos_combustion": "moto",
    "motos_electricas": "moto",
    "bicicletas": "bicicleta",
    "patinetas": "patineta",
}

# El alcance del proyecto son motos, bicicletas y patinetas. Los triciclos y
# cuatriciclos quedan fuera aunque aparezcan en las mismas categorías.
FUERA_DE_ALCANCE = [
    "triciclo",
    "triciclos",
    "trisiclo",
    "trisiclos",
    "trisiculo",
    "trimoto",
    "trimotos",
    "cuatriciclo",
    "cuatriciclos",
    "cuadriciclo",
    "cuadriciclos",
]

CAMPOS_SALIDA = [
    "id",
    "categoria",
    "titulo",
    "precio",
    "moneda",
    "provincia",
    "municipio",
    "fecha_publicacion",
    "vistas",
    "n_imagenes",
    "destacado",
    "url",
    "fecha_captura",
    "producto_detectado",
    "relevante",
    "motivo",
]


def contiene(texto: str, palabras: list[str]) -> str | None:
    """Devuelve la primera palabra encontrada, respetando límites de palabra.

    Acepta plurales simples (``moto``/``motos``, ``rin``/``rines``), porque los
    títulos de Revolico casi nunca respetan la concordancia.
    """
    for palabra in palabras:
        patron = rf"\b{re.escape(palabra)}(?:s|es)?\b"
        if re.search(patron, texto):
            return palabra
    return None


def primeras_palabras(texto: str, n: int = 2) -> list[str]:
    """Devuelve las primeras ``n`` palabras alfanuméricas del título.

    Sirve para distinguir un vehículo de un repuesto: quien vende una batería
    suele empezar el título con "Batería...", no con "Moto...".
    """
    tokens = re.findall(r"[a-z0-9]+", texto)
    return tokens[:n]


def detectar_producto_explicito(texto: str, categoria: str) -> str | None:
    """Detecta el producto nombrado en el título, sin usar la categoría."""
    # "Scooter" es ambiguo: moto o patineta según la categoría.
    if re.search(r"\bscooter\b", texto):
        if categoria == "patinetas":
            return "patineta"
        if categoria.startswith("motos"):
            return "moto"

    for producto, palabras in PRODUCTOS.items():
        if producto == "patineta":
            palabras = [p for p in palabras if p != "scooter"]
        if contiene(texto, palabras):
            return producto

    if contiene(texto, MARCAS):
        return CATEGORIA_A_PRODUCTO.get(categoria)
    return None


def clasificar(fila: dict) -> tuple[str, str, str | None]:
    """Devuelve (relevante, motivo, producto_detectado)."""
    categoria = fila.get("categoria", "")
    texto = normalizar(fila.get("titulo", ""))

    # El alcance son motos, bicicletas y patinetas: el resto se descarta.
    if contiene(texto, FUERA_DE_ALCANCE):
        return "no", "fuera de alcance", None

    esperado = CATEGORIA_A_PRODUCTO.get(categoria)
    explicito = detectar_producto_explicito(texto, categoria)
    producto = explicito or esperado
    ruido_fuerte = contiene(texto, RUIDO_FUERTE)
    ruido_contextual = contiene(texto, RUIDO_CONTEXTUAL)
    # "para moto", "para bicicleta" delata un accesorio o repuesto.
    para_vehiculo = bool(
        re.search(
            r"\bpara\s+(?:motos?|bicis?|bicicletas?|patinetas?|triciclos?|scooters?)\b",
            texto,
        )
    )
    inicio = primeras_palabras(texto, 1)
    empieza_con_ruido = bool(inicio) and contiene(
        inicio[0], RUIDO_FUERTE + RUIDO_CONTEXTUAL
    ) is not None

    # En Cuba "motor" también significa moto. Si hay cilindrada, es un vehículo.
    if categoria.startswith("motos") and inicio and inicio[0] in {"motor", "motores"}:
        if explicito or re.search(r"\b\d{2,4}\s*(?:cc|ccm)\b", texto):
            explicito = explicito or "moto"
            producto = explicito
        else:
            return "revisar", "título 'motor' ambiguo (¿moto o repuesto?)", "moto"

    # 1. Repuesto o accesorio que menciona el vehículo: "Batería para moto".
    if para_vehiculo and (ruido_contextual or ruido_fuerte):
        return (
            "revisar",
            f"posible accesorio para {producto}: {ruido_contextual or ruido_fuerte}",
            producto,
        )

    # 2. El título empieza con el nombre de una pieza: "Batería 12V", "Motor 150cc".
    #    Solo si no se nombró un vehículo: "Motor Krathos 200cc" es una moto.
    if empieza_con_ruido and explicito is None:
        return "no", f"repuesto o accesorio: {inicio[0]}", producto

    # 3. Ruido fuerte: lavadora, carro, extractor, adorno, etc.
    if ruido_fuerte:
        if explicito:
            return "revisar", f"producto {explicito} con posible ruido: {ruido_fuerte}", explicito
        return "no", f"ruido: {ruido_fuerte}", producto

    # 4. Producto explícito: pertenece al tema aunque esté en otra categoría.
    if explicito:
        if esperado and explicito != esperado:
            return "si", f"producto {explicito} en categoría {categoria}", explicito
        return "si", "producto explícito y categoría compatible", explicito

    # 5. Sin producto explícito en el título.
    if ruido_contextual:
        return "revisar", f"sin producto explícito; menciona {ruido_contextual}", producto

    if categoria == "patinetas":
        return "revisar", "categoría patinetas sin palabra clave", producto

    return "si", "categoría específica sin ruido", producto


def leer_filas(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def deduplicar(filas: list[dict]) -> tuple[list[dict], int, int]:
    """Elimina duplicados por id y por título+precio+municipio."""
    por_id: dict[str, dict] = {}
    for fila in filas:
        por_id.setdefault(fila.get("id", ""), fila)
    duplicados_id = len(filas) - len(por_id)

    unicos: dict[tuple[str, str, str], dict] = {}
    for fila in por_id.values():
        clave = (
            normalizar(fila.get("titulo", "")),
            str(fila.get("precio", "")),
            normalizar(fila.get("municipio", "")),
        )
        unicos.setdefault(clave, fila)
    duplicados_clave = len(por_id) - len(unicos)
    return list(unicos.values()), duplicados_id, duplicados_clave


def guardar(filas: list[dict], ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS_SALIDA, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(filas)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "anuncios.csv",
        help="CSV de anuncios recolectados.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DATA_PROCESSED,
        help="Carpeta de salida.",
    )
    parser.add_argument(
        "--resumen",
        type=Path,
        default=REPORTS / "relevancia_resumen.txt",
        help="Archivo de resumen.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"No existe {args.input}. Ejecuta primero el scraper.")

    filas = leer_filas(args.input)
    if not filas:
        raise SystemExit("El CSV está vacío.")

    clasificados: list[dict] = []
    for fila in filas:
        fila["titulo"] = redactar(fila.get("titulo", ""))
        relevante, motivo, producto = clasificar(fila)
        clasificados.append(
            {
                **fila,
                "producto_detectado": producto or "",
                "relevante": relevante,
                "motivo": motivo,
            }
        )

    relacionados = [f for f in clasificados if f["relevante"] == "si"]
    revisar = [f for f in clasificados if f["relevante"] == "revisar"]
    excluidos = [f for f in clasificados if f["relevante"] == "no"]

    unicos, dup_id, dup_clave = deduplicar(relacionados)

    guardar(relacionados, args.out_dir / "anuncios_relacionados.csv")
    guardar(unicos, args.out_dir / "anuncios_relacionados_unicos.csv")
    guardar(revisar, args.out_dir / "anuncios_revisar.csv")
    guardar(excluidos, args.out_dir / "anuncios_excluidos.csv")

    lineas = [
        "=" * 60,
        "RESUMEN DE RELEVANCIA",
        "=" * 60,
        f"Anuncios de entrada: {len(filas)}",
        f"Relacionados (sí): {len(relacionados)}",
        f"Para revisar: {len(revisar)}",
        f"Excluidos: {len(excluidos)}",
        f"Duplicados por id: {dup_id}",
        f"Duplicados por título+precio+municipio: {dup_clave}",
        f"Relacionados únicos: {len(unicos)}",
        "",
        "Relacionados por categoría:",
    ]
    for categoria, n in Counter(f.get("categoria", "") for f in relacionados).most_common():
        lineas.append(f"  {categoria:<20} {n:>5}")

    lineas.append("\nExcluidos por motivo (top 10):")
    for motivo, n in Counter(f["motivo"] for f in excluidos).most_common(10):
        lineas.append(f"  {n:>5}  {motivo}")

    lineas.append("\nPara revisar: ejemplos")
    for fila in revisar[:15]:
        lineas.append(
            f"  {fila.get('categoria', ''):<18} | {fila.get('titulo', '')[:60]} | {fila['motivo']}"
        )

    resumen = "\n".join(lineas) + "\n"
    args.resumen.parent.mkdir(parents=True, exist_ok=True)
    args.resumen.write_text(resumen, encoding="utf-8")
    print(resumen)
    print(f"Archivos guardados en: {args.out_dir}")


if __name__ == "__main__":
    main()
