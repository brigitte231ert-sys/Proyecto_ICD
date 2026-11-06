"""Análisis de contenido de una muestra de 200 títulos.

Sigue el plan acordado:
1. Tomar 200 títulos al azar de ``anuncios_limpios.csv``.
2. Clasificarlos por lo que destaca el vendedor.
3. Contar frecuencias y sacar 8 ejemplos textuales.
4. Presentarlo como análisis de contenido de la oferta, no como entrevistas.

La clasificación es automática por palabras clave. Se compara la muestra con
el total de los 9 841 anuncios para comprobar que el patrón se sostiene.

Uso:
    python -m src.analisis_200_titulos
"""

from __future__ import annotations

import random
import re
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.config import DATA_PROCESSED, FIGURES, REPORTS

SEMILLA = 2026
TAMANO_MUESTRA = 200

# Categorías pedidas: qué destaca el vendedor en el título.
TEMAS: dict[str, list[str]] = {
    "Nueva o usada": [
        r"\bnuev[oa]s?\b",
        r"\busad[oa]s?\b",
        r"\bseminuev[oa]s?\b",
        r"\bpoco uso\b",
        r"\bsin estrenar\b",
        r"\bestrenar\b",
    ],
    "Batería o autonomía": [
        r"\bbaterias?\b",
        r"\bautonomia\b",
        r"\blitio\b",
        r"\blifepo4\b",
        r"\bcargador\b",
        r"\bcarga\b",
        # Potencia y capacidad eléctrica. No se incluye "km" porque "0km"
        # suele indicar kilometraje y no autonomía.
        r"\b\d+\s*(?:v|ah|w|kw)\b",
    ],
    "Papeles o garantía": [
        r"\bpapeles?\b",
        r"\bdocumentos?\b",
        r"\bdocumentacion\b",
        r"\bfactura\b",
        r"\bcontrato\b",
        r"\bgarantia\b",
        r"\blegal\b",
        r"\blegalizad[oa]\b",
        r"\bnacionalizacion\b",
        r"\bplaca\b",
        r"\bchapa\b",
        r"\bmatricula\b",
        r"\btraspaso\b",
        r"\bcirculacion\b",
        r"\bcertificad[oa]\b",
        r"\bcertifico\b",
    ],
    "Motivo de venta": [
        r"\bme voy\b",
        r"\bviajo\b",
        r"\bpor viaje\b",
        r"\bmudanza\b",
        r"\bme mudo\b",
        r"\bpermuto\b",
        r"\bme ajusto\b",
        r"\bnecesito\b",
        r"\bpor falta de uso\b",
        r"\bno la uso\b",
    ],
    "Urgente": [
        r"\burgente\b",
        r"\burgencia\b",
        r"\binmediato\b",
        r"\brapido\b",
        r"\blo antes posible\b",
        r"\bpara hoy\b",
    ],
    "Negociable": [
        r"\bnegociable\b",
        r"\bnegociar\b",
        r"\ba convenir\b",
        r"\bconversable\b",
        r"\brebaja\b",
        r"\bdescuento\b",
        r"\bescucho ofertas\b",
        r"\bse acepta\b",
    ],
}


def miles(numero: int) -> str:
    """Formatea un entero con espacio como separador de miles."""
    return f"{numero:,}".replace(",", " ")


def normalizar(texto: str) -> str:
    """Pasa a minúsculas, quita tildes y colapsa espacios."""
    texto = str(texto or "").lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip()


def limpiar_para_publicar(texto: str) -> str:
    """Quita enlaces, correos y teléfonos de un título antes de publicarlo."""
    texto = str(texto or "")
    texto = re.sub(r"https?://\S+|www\.\S+", "[enlace]", texto)
    texto = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[correo]", texto)
    # Teléfonos cubanos: 8 dígitos que empiezan por 5 o 7, con separadores
    # opcionales y prefijo +53. Se evita tocar precios de 6 o 7 dígitos.
    texto = re.sub(
        r"(?<!\d)(?:\+?53[\s.-]?)?[57]\d(?:[\s.-]?\d){6}(?!\d)",
        "[contacto]",
        texto,
    )
    return " ".join(texto.split())


def clasificar(df: pd.DataFrame) -> pd.DataFrame:
    """Añade una columna booleana por tema y cuenta temas por título."""
    titulos = df["titulo"].map(normalizar)
    for tema, patrones in TEMAS.items():
        regex = re.compile("|".join(patrones))
        df[tema] = titulos.str.contains(regex, regex=True).fillna(False)
    df["n_temas"] = df[list(TEMAS)].sum(axis=1)
    df["titulo_norm"] = titulos
    return df


def resumen(df: pd.DataFrame, etiqueta: str) -> pd.DataFrame:
    filas = []
    for tema in TEMAS:
        filas.append(
            {
                "tema": tema,
                "anuncios": int(df[tema].sum()),
                "porcentaje": round(df[tema].mean() * 100, 1),
                "base": etiqueta,
            }
        )
    return pd.DataFrame(filas)


def candidatos(df: pd.DataFrame, tema: str, n: int = 2) -> list[str]:
    """Devuelve hasta ``n`` títulos reales del tema, limpiados y sin repetir."""
    vistos: set[str] = set()
    salida: list[str] = []
    for titulo in df.loc[df[tema], "titulo"].dropna():
        limpio = limpiar_para_publicar(titulo)[:150]
        clave = limpio.lower()
        if clave in vistos or not limpio:
            continue
        vistos.add(clave)
        salida.append(limpio)
        if len(salida) == n:
            break
    return salida


def seleccionar_ejemplos(
    df: pd.DataFrame, maximo: int = 8
) -> list[tuple[str, str]]:
    """Elige ``maximo`` ejemplos únicos repartidos entre los temas.

    Recorre los temas de más a menos frecuente y toma hasta dos títulos de
    cada uno. Un título que ya salió no se repite, aunque mencione varios
    temas. Devuelve pares ``(tema, título)``.
    """
    usados: set[str] = set()
    seleccion: list[tuple[str, str]] = []
    orden = (
        df[list(TEMAS)]
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )
    for tema in orden:
        agregados = 0
        # Se piden varios candidatos porque algunos ya salieron en otro tema.
        for titulo in candidatos(df, tema, n=8):
            clave = titulo.lower()
            if clave in usados:
                continue
            usados.add(clave)
            seleccion.append((tema, titulo))
            agregados += 1
            if agregados == 2 or len(seleccion) == maximo:
                break
        if len(seleccion) == maximo:
            return seleccion
    return seleccion


def figura(muestra: pd.DataFrame, total: pd.DataFrame, ruta: Path) -> None:
    fig, ejes = plt.subplots(1, 2, figsize=(14, 5.5))

    orden = muestra.sort_values("porcentaje")
    y = range(len(orden))
    ejes[0].barh(
        [f"{t}" for t in orden["tema"]],
        orden["porcentaje"],
        color="#4c72b0",
        label="Muestra de 200",
    )
    ejes[0].set_xlabel("% de títulos que mencionan el tema")
    ejes[0].set_title("Qué destaca el vendedor (muestra de 200 títulos)")
    for i, valor in enumerate(orden["porcentaje"]):
        ejes[0].text(valor + 0.4, i, f"{valor:.1f} %", va="center", fontsize=8)

    # Comparación muestra vs. total, en el mismo orden.
    total_orden = total.set_index("tema").loc[orden["tema"]]
    x = range(len(orden))
    ancho = 0.38
    ejes[1].bar(
        [i - ancho / 2 for i in x],
        orden["porcentaje"],
        width=ancho,
        color="#4c72b0",
        label="Muestra (200)",
    )
    ejes[1].bar(
        [i + ancho / 2 for i in x],
        total_orden["porcentaje"],
        width=ancho,
        color="#dd8452",
        label="Total (9 841)",
    )
    ejes[1].set_xticks(list(x))
    ejes[1].set_xticklabels(orden["tema"], rotation=30, ha="right")
    ejes[1].set_ylabel("% de títulos")
    ejes[1].set_title("Muestra vs. total del dataset")
    ejes[1].legend(frameon=False)

    plt.tight_layout()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ruta = DATA_PROCESSED / "anuncios_limpios.csv"
    df = pd.read_csv(ruta)
    df = clasificar(df)

    muestra = df.sample(n=TAMANO_MUESTRA, random_state=SEMILLA).copy()
    muestra = muestra.sort_values(["categoria", "id"]).reset_index(drop=True)
    resumen_muestra = resumen(muestra, "muestra")
    resumen_total = resumen(df, "total")

    # Guarda la muestra para auditoría, con los títulos ya limpios.
    auditoria = muestra[
        ["id", "categoria", "titulo", *TEMAS.keys(), "n_temas"]
    ].copy()
    auditoria["titulo"] = auditoria["titulo"].map(limpiar_para_publicar)
    auditoria.to_csv(
        REPORTS / "muestra_200_titulos.csv",
        index=False,
        encoding="utf-8-sig",
    )

    lineas = [
        "=" * 78,
        "ANÁLISIS DE CONTENIDO DE 200 TÍTULOS",
        "Motos, bicicletas y patinetas · Revolico",
        "=" * 78,
        f"Archivo: {ruta}",
        f"Población: {miles(len(df))} anuncios",
        f"Muestra: {TAMANO_MUESTRA} títulos al azar (semilla {SEMILLA})",
        "",
        "Qué destaca el vendedor en el título. No son entrevistas:",
        "es el discurso de la oferta.",
        "",
        "--- FRECUENCIA EN LA MUESTRA ---",
    ]

    for _, fila in resumen_muestra.iterrows():
        lineas.append(
            f"  {fila['tema']:<24} {miles(int(fila['anuncios'])):>4} "
            f"({fila['porcentaje']:>5.1f} %)"
        )

    sin_tema = int((muestra["n_temas"] == 0).sum())
    con_tema = TAMANO_MUESTRA - sin_tema
    lineas += [
        "",
        f"  Con al menos un tema: {miles(con_tema):>4} "
        f"({con_tema / TAMANO_MUESTRA * 100:.1f} %)",
        f"  Sin ningún tema:      {miles(sin_tema):>4} "
        f"({sin_tema / TAMANO_MUESTRA * 100:.1f} %)",
        "",
        "--- COMPARACIÓN CON EL TOTAL (9 841) ---",
        "  Tema                       Muestra   Total",
    ]
    for tema in resumen_muestra["tema"]:
        pm = resumen_muestra.set_index("tema").loc[tema, "porcentaje"]
        pt = resumen_total.set_index("tema").loc[tema, "porcentaje"]
        lineas.append(f"  {tema:<24} {pm:>6.1f}% {pt:>7.1f}%")

    lineas += [
        "",
        "--- COMPOSICIÓN DE LA MUESTRA ---",
    ]
    for categoria, n in muestra["categoria"].value_counts().items():
        lineas.append(f"  {categoria:<20} {miles(int(n)):>4}")

    lineas += [
        "",
        "--- EJEMPLOS TEXTUALES (8 títulos reales, limpiados) ---",
    ]
    for tema, ejemplo in seleccionar_ejemplos(muestra, maximo=8):
        lineas.append(f"  [{tema}]")
        lineas.append(f"    - {ejemplo}")
        lineas.append("")

    lineas += [
        "",
        "--- NOTAS ---",
        "- Clasificación automática por palabras clave; puede haber falsos",
        "  positivos (por ejemplo, 'nueva' referido a la batería).",
        "- Un título puede mencionar varios temas.",
        "- Los teléfonos, correos y enlaces se reemplazaron por [contacto],",
        "  [correo] y [enlace].",
        "- 'Motivo de venta' no tiene ejemplos porque ningún título de la",
        "  muestra declara por qué vende.",
        "- La muestra es aleatoria, pero el dataset no es representativo del",
        "  mercado: está concentrado en La Habana y en Revolico.",
        "- Esta tabla describe la oferta; no reemplaza las entrevistas.",
        "",
    ]

    salida = REPORTS / "analisis_200_titulos.txt"
    salida.write_text("\n".join(lineas), encoding="utf-8")
    figura(
        resumen_muestra,
        resumen_total,
        FIGURES / "08_temas_200_titulos.png",
    )

    print("\n".join(lineas[:38]))
    print(f"\nGuardado: {salida}")
    print(f"Muestra:  {REPORTS / 'muestra_200_titulos.csv'}")
    print(f"Figura:   {FIGURES / '08_temas_200_titulos.png'}")


if __name__ == "__main__":
    main()
