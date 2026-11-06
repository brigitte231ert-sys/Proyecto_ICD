"""Genera el HTML del informe a partir de ``reports/informe.md``.

El HTML usa una hoja de estilo sencilla, pensada para convertirse a PDF con
LibreOffice. Las imágenes se referencian con rutas relativas a ``reports/``.

Uso:
    python -m src.generar_informe
    python -m src.generar_informe --input reports/informe.md --salida reports/informe.html
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import markdown
from PIL import Image

from src.config import REPORTS

CSS = """
@page { size: A4; margin: 2.2cm 2.2cm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 20pt; margin-bottom: 0.2em; color: #123a5c; }
h2 { font-size: 14pt; margin-top: 1.4em; color: #123a5c;
     border-bottom: 1px solid #c9d6e2; padding-bottom: 2px; }
h3 { font-size: 12pt; margin-top: 1.1em; color: #1f4f73; }
p { text-align: justify; margin: 0.5em 0; }
img { width: 100%; max-width: 100%; height: auto; display: block;
      margin: 0.6em auto; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0;
        font-size: 9.5pt; page-break-inside: avoid; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #b9c6d2; padding: 4px 6px; text-align: left; }
th { background: #e8eef4; }
h2, h3 { page-break-after: avoid; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt;
            background: #f4f6f8; }
pre { padding: 8px; border: 1px solid #dde3e8; white-space: pre-wrap;
      page-break-inside: avoid; }
blockquote { border-left: 3px solid #7fa3c2; margin-left: 0; padding-left: 1em;
             color: #33475b; }
hr { border: none; border-top: 1px solid #d5dde5; margin: 1.2em 0; }
"""

PLANTILLA = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Informe — Mercado de motos, bicicletas y patinetas en Cuba</title>
<style>{css}</style></head><body>
{cuerpo}
</body></html>
"""


ANCHO_UTIL_PX = 627  # 16,6 cm de caja de texto a 96 ppp


def ajustar_imagenes(html: str) -> str:
    """Añade ancho y alto en píxeles a cada imagen local.

    LibreOffice ignora ``max-width`` y, si solo se le da ``width="100%"``,
    reserva la altura natural de la imagen y empuja el contenido a otra
    página. Con ancho y alto explícitos, el flujo del documento es estable.
    """

    def reemplazar(coincidencia: re.Match[str]) -> str:
        etiqueta = coincidencia.group(0)
        fuente = re.search(r'src="([^"]+)"', etiqueta)
        if not fuente:
            return etiqueta

        ruta = (REPORTS / fuente.group(1)).resolve()
        if not ruta.is_file():
            return etiqueta

        with Image.open(ruta) as imagen:
            ancho, alto = imagen.size
        alto_util = round(ANCHO_UTIL_PX * alto / ancho)

        etiqueta = re.sub(r'\s(?:width|height)="[^"]*"', "", etiqueta)
        return etiqueta.replace(
            "<img ",
            f'<img width="{ANCHO_UTIL_PX}" height="{alto_util}" ',
            1,
        )

    return re.sub(r"<img\b[^>]*>", reemplazar, html)


def convertir(markdown_texto: str) -> str:
    """Convierte Markdown a HTML con tablas y bloques de código."""
    html = markdown.markdown(
        markdown_texto,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )
    return ajustar_imagenes(html)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera el HTML del informe desde Markdown."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=REPORTS / "informe.md",
        help="Archivo Markdown de entrada.",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=REPORTS / "informe.html",
        help="Archivo HTML de salida.",
    )
    args = parser.parse_args()

    texto = args.input.read_text(encoding="utf-8")
    cuerpo = convertir(texto)
    html = PLANTILLA.format(css=CSS, cuerpo=cuerpo)
    args.salida.write_text(html, encoding="utf-8")

    print(f"HTML generado: {args.salida}")
    print(f"Palabras:      {len(texto.split()):,}".replace(",", " "))


if __name__ == "__main__":
    main()
