"""Análisis de contenido de los títulos de los anuncios.

Cuenta qué temas menciona el vendedor en el título: estado, especificaciones,
garantía, precio, uso, urgencia, contacto y accesorios. No sustituye una
entrevista: describe el discurso de la oferta con las palabras que el propio
anunciante eligió.

Uso:
    python -m src.temas_anuncios
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.config import DATA_PROCESSED, FIGURES, REPORTS

# Cada tema es una lista de patrones sobre el título normalizado (sin tildes,
# en minúsculas). Un título puede caer en varios temas.
TEMAS: dict[str, list[str]] = {
    "Estado o novedad": [
        r"\bnuev[oa]s?\b",
        r"\bpoco uso\b",
        r"\busad[oa]s?\b",
        r"\bseminuev[oa]\b",
        r"\bestrenar\b",
        r"\bimpecable\b",
        r"\bperfecto estado\b",
        r"\b202[3-6]\b",
    ],
    "Especificaciones técnicas": [
        r"\b\d+\s*(?:w|kw|v|ah|cc|km)\b",
        r"\blitio\b",
        r"\blifepo4\b",
        r"\bautonomia\b",
        r"\bbateria\b",
        r"\bmotor\b",
        r"\bwatt",
    ],
    "Garantía, papeles o trámites": [
        r"\bgarantia\b",
        r"\bfactura\b",
        r"\bcontrato\b",
        r"\bpapeles\b",
        r"\bdocumentos?\b",
        r"\blegal\b",
        r"\bimportadora\b",
        r"\btramite\b",
        r"\bplaca\b",
        r"\bmatricula\b",
        r"\bregistro\b",
    ],
    "Precio, oferta o negociación": [
        r"\bprecio\b",
        r"\boferta\b",
        r"\bbarat[oa]\b",
        r"\bnegociable\b",
        r"\brebaja\b",
        r"\bdescuento\b",
        r"\busd\b",
        r"\bdolar(?:es)?\b",
        r"\bcup\b",
        r"\beconomic[oa]\b",
    ],
    "Uso, trabajo o destinatario": [
        r"\bmensajer[oa]\b",
        r"\bdelivery\b",
        r"\breparto\b",
        r"\btrabajo\b",
        r"\bmensajeria\b",
        r"\bestudiante\b",
        r"\bnin[oa]s?\b",
        r"\binfantil\b",
        r"\bmujer\b",
        r"\bhombre\b",
        r"\bfamiliar\b",
        r"\bpaseo\b",
    ],
    "Urgencia o motivo de venta": [
        r"\burgente\b",
        r"\bvendo\b",
        r"\bse vende\b",
        r"\bme voy\b",
        r"\bviajo\b",
        r"\bpermuto\b",
        r"\bme ajusto\b",
        r"\bnecesito\b",
        r"\bajusto\b",
    ],
    "Contacto o ubicación": [
        r"\bwhatsapp\b",
        r"\btelefono\b",
        r"\bllamar\b",
        r"\bescribir\b",
        r"\bprivado\b",
        r"\bmp\b",
        r"\bl[ao] habana\b",
        r"\bmunicipio\b",
        r"\bplaya\b",
        r"\bcerro\b",
        r"\bboyeros\b",
    ],
    "Accesorios o extras": [
        r"\bcasco\b",
        r"\bcargador\b",
        r"\balarma\b",
        r"\bcanasta\b",
        r"\bportaequipaje\b",
        r"\bkit\b",
        r"\baccesorio\b",
        r"\bregalo\b",
        r"\bincluye\b",
    ],
}


def miles(numero: int) -> str:
    """Formatea un entero con espacio fino como separador de miles."""
    return f"{numero:,}".replace(",", " ")


def normalizar(texto: str) -> str:
    """Pasa a minúsculas, quita tildes y colapsa espacios."""
    texto = str(texto or "").lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip()


def clasificar(df: pd.DataFrame) -> pd.DataFrame:
    """Añade una columna booleana por tema y cuenta temas por título."""
    titulos = df["titulo"].map(normalizar)
    for tema, patrones in TEMAS.items():
        regex = re.compile("|".join(patrones))
        df[tema] = titulos.str.contains(regex, regex=True).fillna(False)
    df["n_temas"] = df[list(TEMAS)].sum(axis=1)
    df["titulo_norm"] = titulos
    return df


def tabla_resumen(df: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for tema in TEMAS:
        filas.append(
            {
                "tema": tema,
                "anuncios": int(df[tema].sum()),
                "porcentaje": round(df[tema].mean() * 100, 1),
            }
        )
    return pd.DataFrame(filas).sort_values("anuncios", ascending=False)


def ejemplos(df: pd.DataFrame, tema: str, n: int = 3) -> list[str]:
    """Devuelve títulos reales que mencionan el tema, sin repetir."""
    vistos: set[str] = set()
    salida: list[str] = []
    for titulo in df.loc[df[tema], "titulo"].dropna():
        limpio = " ".join(str(titulo).split())
        if limpio.lower() in vistos:
            continue
        vistos.add(limpio.lower())
        salida.append(limpio[:120])
        if len(salida) == n:
            break
    return salida


def figura(resumen: pd.DataFrame, df: pd.DataFrame, ruta: Path) -> None:
    fig, ejes = plt.subplots(1, 2, figsize=(14, 5.5))

    orden = resumen.sort_values("porcentaje")
    ejes[0].barh(orden["tema"], orden["porcentaje"], color="#4c72b0")
    ejes[0].set_xlabel("% de anuncios que mencionan el tema")
    ejes[0].set_title("Temas en los títulos (n = {:,})".format(len(df)).replace(",", " "))
    for i, valor in enumerate(orden["porcentaje"]):
        ejes[0].text(valor + 0.4, i, f"{valor:.1f} %", va="center", fontsize=8)

    conteo = df["n_temas"].value_counts().sort_index()
    ejes[1].bar(conteo.index, conteo.values, color="#dd8452")
    ejes[1].set_xlabel("Cantidad de temas mencionados en el título")
    ejes[1].set_ylabel("Anuncios")
    ejes[1].set_title("Densidad de información del título")
    for x, y in zip(conteo.index, conteo.values):
        ejes[1].text(x, y, f"{y:,}".replace(",", " "), ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ruta = DATA_PROCESSED / "anuncios_limpios.csv"
    df = pd.read_csv(ruta)
    df = clasificar(df)
    resumen = tabla_resumen(df)

    lineas = [
        "=" * 78,
        "ANÁLISIS DE CONTENIDO DE LOS TÍTULOS",
        "Motos, bicicletas y patinetas · Revolico",
        "=" * 78,
        f"Archivo: {ruta}",
        f"Anuncios: {miles(len(df))}",
        "",
        "Este análisis describe qué destaca el vendedor en el título.",
        "No son respuestas de personas: es el discurso de la oferta.",
        "",
        "--- FRECUENCIA DE TEMAS ---",
    ]
    for _, fila in resumen.iterrows():
        lineas.append(
            f"  {fila['tema']:<32} {miles(int(fila['anuncios'])):>6} "
            f"({fila['porcentaje']:>5.1f} %)"
        )

    lineas += [
        "",
        f"  Títulos con al menos un tema: "
        f"{miles(int((df['n_temas'] > 0).sum()))} "
        f"({(df['n_temas'] > 0).mean() * 100:.1f} %)",
        f"  Títulos sin ningún tema:      "
        f"{miles(int((df['n_temas'] == 0).sum()))} "
        f"({(df['n_temas'] == 0).mean() * 100:.1f} %)",
        "",
        "--- TEMAS POR CATEGORÍA (% de anuncios de cada categoría) ---",
    ]

    por_categoria = df.groupby("categoria")[list(TEMAS)].mean().mul(100).round(1)
    encabezado = "  " + "Tema".ljust(32) + "".join(
        c[:12].rjust(13) for c in por_categoria.index
    )
    lineas.append(encabezado)
    for tema in resumen["tema"]:
        fila = "  " + tema.ljust(32)
        for categoria in por_categoria.index:
            fila += f"{por_categoria.loc[categoria, tema]:>12.1f}%"
        lineas.append(fila)

    lineas += ["", "--- EJEMPLOS TEXTUALES (títulos reales, sin editar) ---"]
    for tema in resumen["tema"]:
        lineas.append(f"\n  [{tema}]")
        for ejemplo in ejemplos(df, tema):
            lineas.append(f"    - {ejemplo}")

    lineas += [
        "",
        "--- NOTAS ---",
        "- La clasificación es automática por palabras clave; puede haber falsos",
        "  positivos (por ejemplo, 'nueva' referido a la batería).",
        "- Los porcentajes describen los títulos, no la intención real del vendedor.",
        "- Un título puede mencionar varios temas.",
        "- Esta tabla no reemplaza las entrevistas: las complementa desde la oferta.",
        "",
    ]

    salida = REPORTS / "analisis_temas.txt"
    salida.write_text("\n".join(lineas), encoding="utf-8")
    figura(resumen, df, FIGURES / "07_temas_anuncios.png")

    print("\n".join(lineas[:40]))
    print(f"\nGuardado: {salida}")
    print(f"Figura:  {FIGURES / '07_temas_anuncios.png'}")


if __name__ == "__main__":
    main()
