"""Genera la presentación de storytelling del proyecto.

Uso:
    python -m src.generar_storytelling_pptx
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from src.config import REPORTS

# --- Paleta -----------------------------------------------------------------
AZUL = RGBColor(0x12, 0x3A, 0x5C)
AZUL_MEDIO = RGBColor(0x1F, 0x4F, 0x73)
AZUL_CLARO = RGBColor(0xE8, 0xEE, 0xF4)
GRIS = RGBColor(0x5B, 0x67, 0x70)
GRIS_CLARO = RGBColor(0xD5, 0xDD, 0xE5)
NARANJA = RGBColor(0xC0, 0x50, 0x2D)
NARANJA_CLARO = RGBColor(0xF4, 0xE3, 0xDA)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
VERDE = RGBColor(0x2E, 0x7D, 0x5B)

FONT = "Arial"
ANCHO = 13.333
ALTO = 7.5


def fondo(slide, color: RGBColor) -> None:
    forma = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(ANCHO), Inches(ALTO)
    )
    forma.fill.solid()
    forma.fill.fore_color.rgb = color
    forma.line.fill.background()
    forma.shadow.inherit = False


def caja(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    relleno: RGBColor,
    linea: RGBColor | None = None,
    radio: float = 0.06,
):
    forma = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
    )
    forma.fill.solid()
    forma.fill.fore_color.rgb = relleno
    if linea is None:
        forma.line.fill.background()
    else:
        forma.line.color.rgb = linea
        forma.line.width = Pt(1)
    forma.shadow.inherit = False
    try:
        forma.adjustments[0] = radio
    except Exception:
        pass
    return forma


def texto(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    contenido: str,
    *,
    tam: float = 18,
    color: RGBColor = AZUL,
    negrita: bool = False,
    cursiva: bool = False,
    alineacion=PP_ALIGN.LEFT,
    anclaje=MSO_ANCHOR.TOP,
    interlineado: float = 1.0,
    espacio: float = 0,
):
    caja_texto = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    tf = caja_texto.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anclaje
    p = tf.paragraphs[0]
    p.alignment = alineacion
    p.line_spacing = interlineado
    p.space_after = Pt(espacio)
    r = p.add_run()
    r.text = contenido
    r.font.name = FONT
    r.font.size = Pt(tam)
    r.font.bold = negrita
    r.font.italic = cursiva
    r.font.color.rgb = color
    return caja_texto


def vinetas(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    elementos: list[str],
    *,
    tam: float = 18,
    color: RGBColor = AZUL,
    color_vineta: RGBColor = NARANJA,
    espacio: float = 12,
):
    caja_texto = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    tf = caja_texto.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, elemento in enumerate(elementos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(espacio)
        p.line_spacing = 1.05
        r1 = p.add_run()
        r1.text = "•  "
        r1.font.name = FONT
        r1.font.size = Pt(tam)
        r1.font.bold = True
        r1.font.color.rgb = color_vineta
        r2 = p.add_run()
        r2.text = elemento
        r2.font.name = FONT
        r2.font.size = Pt(tam)
        r2.font.color.rgb = color
    return caja_texto


def linea(slide, x1: float, y1: float, x2: float, y2: float, color=GRIS_CLARO, grosor=1):
    from pptx.enum.shapes import MSO_CONNECTOR

    conector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    conector.line.color.rgb = color
    conector.line.width = Pt(grosor)
    return conector


def encabezado(slide, kicker: str, titulo: str, numero: int) -> None:
    texto(slide, 0.8, 0.45, 8.0, 0.3, kicker.upper(), tam=11, color=NARANJA, negrita=True)
    texto(slide, 0.8, 0.82, 11.5, 0.9, titulo, tam=30, color=AZUL, negrita=True)
    linea(slide, 0.8, 1.72, 12.5, 1.72, GRIS_CLARO, 1)
    texto(slide, 12.1, 7.05, 0.6, 0.25, f"{numero:02d}", tam=9, color=GRIS, alineacion=PP_ALIGN.RIGHT)
    texto(
        slide,
        0.8,
        7.05,
        9.5,
        0.25,
        "Mercado de motos, bicicletas y patinetas en Cuba · Revolico, 2026",
        tam=9,
        color=GRIS,
    )


def barra_apilada(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    proporcion: float,
    etiqueta_izq: str,
    etiqueta_der: str,
    color_izq: RGBColor,
    color_der: RGBColor,
) -> None:
    ancho_izq = w * proporcion
    caja(slide, x, y, ancho_izq, h, color_izq, radio=0.0)
    caja(slide, x + ancho_izq, y, w - ancho_izq, h, color_der, radio=0.0)
    # Medias columnas para que las etiquetas no se partan en dos líneas.
    texto(slide, x, y + h + 0.08, w / 2, 0.3, etiqueta_izq, tam=11, color=color_izq, negrita=True)
    texto(
        slide,
        x + w / 2,
        y + h + 0.08,
        w / 2,
        0.3,
        etiqueta_der,
        tam=11,
        color=GRIS,
        negrita=True,
        alineacion=PP_ALIGN.RIGHT,
    )


def imagen_ajustada(slide, ruta: Path, x: float, y: float, w: float, h: float) -> None:
    from PIL import Image

    with Image.open(ruta) as im:
        ancho, alto = im.size
    escala = min(w / ancho, h / alto)
    ancho_final = ancho * escala
    alto_final = alto * escala
    slide.shapes.add_picture(
        str(ruta),
        Inches(x + (w - ancho_final) / 2),
        Inches(y + (h - alto_final) / 2),
        Inches(ancho_final),
        Inches(alto_final),
    )


def agregar_notas(slide, texto_notas: str) -> None:
    slide.notes_slide.notes_text_frame.text = texto_notas


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(ANCHO)
    prs.slide_height = Inches(ALTO)
    blanca = prs.slide_layouts[6]

    # ------------------------------------------------------------------ 1
    s = prs.slides.add_slide(blanca)
    fondo(s, AZUL)
    # Círculos decorativos
    for cx, cy, d, color in [
        (10.7, -1.1, 4.8, NARANJA),
        (12.1, 4.7, 2.6, AZUL_MEDIO),
        (1.0, 5.8, 1.2, NARANJA),
    ]:
        circulo = s.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(cx), Inches(cy), Inches(d), Inches(d)
        )
        circulo.fill.background()
        circulo.line.color.rgb = color
        circulo.line.width = Pt(2)
        circulo.shadow.inherit = False

    texto(s, 0.9, 0.8, 7.0, 0.3, "STORYTELLING DEL PROYECTO", tam=12, color=NARANJA, negrita=True)
    texto(
        s,
        0.9,
        1.55,
        8.6,
        2.4,
        "El mapa de un mercado\nque no tenía mapa",
        tam=44,
        color=BLANCO,
        negrita=True,
        interlineado=0.95,
    )
    texto(
        s,
        0.9,
        4.25,
        7.6,
        0.9,
        "Mercado de motos, bicicletas y patinetas en Cuba",
        tam=20,
        color=AZUL_CLARO,
    )
    linea(s, 0.9, 5.35, 5.2, 5.35, NARANJA, 3)
    texto(
        s,
        0.9,
        5.65,
        8.0,
        0.4,
        "Un análisis exploratorio de anuncios clasificados · Revolico, 2026",
        tam=13,
        color=AZUL_CLARO,
    )
    texto(
        s,
        0.9,
        6.65,
        8.0,
        0.4,
        "Brigitte Hernández Romero · Ciencia de Datos · Universidad de La Habana",
        tam=11,
        color=GRIS_CLARO,
    )
    agregar_notas(
        s,
        "Abrir con la idea del mercado sin memoria: en Cuba el precio no se consulta, se pregunta. "
        "Este proyecto construye una base reproducible de anuncios para mirar ese mercado con datos.",
    )

    # ------------------------------------------------------------------ 2
    s = prs.slides.add_slide(blanca)
    encabezado(s, "01 · El problema", "Un precio que se pregunta, no se consulta", 2)
    texto(
        s,
        0.8,
        2.05,
        6.3,
        0.9,
        "En Cuba no hay un registro público de precios. El mercado vive en la conversación: "
        "el barrio, el grupo de WhatsApp, el mecánico, el vecino que acaba de vender.",
        tam=18,
        color=AZUL,
        interlineado=1.15,
    )
    vinetas(
        s,
        0.8,
        3.45,
        6.2,
        2.3,
        [
            "Cada anuncio de Revolico es una ventana a esa memoria.",
            "Miles de ventanas leídas a la vez pueden revelar un patrón.",
            "La pregunta: ¿cómo se comporta el mercado cuando se mira con datos?",
        ],
        tam=16,
        espacio=14,
    )
    caja(s, 7.55, 1.95, 4.95, 4.2, AZUL_CLARO)
    texto(s, 7.95, 2.15, 0.8, 0.8, "“", tam=86, color=NARANJA, negrita=True)
    texto(
        s,
        7.95,
        3.0,
        4.1,
        1.6,
        "El mercado existe sin memoria.\nEste proyecto le construyó una.",
        tam=24,
        color=AZUL,
        negrita=True,
        interlineado=1.05,
    )
    texto(
        s,
        7.95,
        4.9,
        4.1,
        0.8,
        "Una base reproducible para describir la oferta, no para adivinar la demanda.",
        tam=13,
        color=GRIS,
        cursiva=True,
    )
    agregar_notas(
        s,
        "El problema no es que no haya mercado, sino que no hay memoria. "
        "Revolico es la ventana pública; el reto es convertir esos anuncios en evidencia ordenada.",
    )

    # ------------------------------------------------------------------ 3
    s = prs.slides.add_slide(blanca)
    encabezado(s, "02 · La apuesta", "Convertir anuncios en evidencia", 3)
    texto(s, 0.8, 1.95, 4.8, 0.3, "DE LA RECOLECCIÓN A LA BASE LIMPIA", tam=10, color=GRIS, negrita=True)
    texto(s, 0.8, 2.3, 4.8, 0.8, "13 446", tam=46, color=NARANJA, negrita=True)
    texto(s, 0.8, 3.0, 4.8, 0.4, "anuncios únicos recolectados", tam=14, color=GRIS)
    texto(s, 0.8, 3.55, 4.8, 0.4, "↓", tam=28, color=GRIS_CLARO, negrita=True)
    texto(s, 0.8, 3.95, 4.8, 0.8, "9 841", tam=46, color=AZUL, negrita=True)
    texto(s, 0.8, 4.65, 4.8, 0.4, "anuncios limpios", tam=14, color=GRIS)
    texto(
        s,
        0.8,
        5.25,
        4.7,
        1.2,
        "Filtro de relevancia, deduplicación y descarte de precios nulos o señuelo.",
        tam=13,
        color=GRIS,
        interlineado=1.1,
    )

    datos = CategoryChartData()
    datos.categories = ["Combustión", "Bicicletas", "Eléctricas", "Patinetas"]
    datos.add_series("Anuncios", (3349, 3146, 2807, 539))
    marco = s.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, Inches(6.2), Inches(1.95), Inches(6.3), Inches(4.55), datos
    )
    grafico = marco.chart
    grafico.has_legend = False
    grafico.has_title = True
    grafico.chart_title.text_frame.text = "Composición del dataset limpio"
    for p in grafico.chart_title.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = AZUL
    colores = [AZUL, AZUL_MEDIO, RGBColor(0x7F, 0xA3, 0xC2), NARANJA]
    serie = grafico.series[0]
    for i, color in enumerate(colores):
        punto = serie.points[i]
        punto.format.fill.solid()
        punto.format.fill.fore_color.rgb = color
        punto.format.line.fill.background()
    grafico.plots[0].has_data_labels = True
    etiquetas = grafico.plots[0].data_labels
    etiquetas.font.size = Pt(12)
    etiquetas.font.bold = True
    etiquetas.font.name = FONT
    etiquetas.font.color.rgb = AZUL
    etiquetas.position = XL_LABEL_POSITION.OUTSIDE_END
    grafico.value_axis.maximum_scale = 4000
    grafico.value_axis.major_unit = 1000
    grafico.value_axis.has_major_gridlines = True
    grafico.value_axis.major_gridlines.format.line.color.rgb = GRIS_CLARO
    grafico.value_axis.tick_labels.font.size = Pt(10)
    grafico.value_axis.tick_labels.font.name = FONT
    grafico.value_axis.tick_labels.font.color.rgb = GRIS
    grafico.category_axis.tick_labels.font.size = Pt(12)
    grafico.category_axis.tick_labels.font.name = FONT
    grafico.category_axis.tick_labels.font.color.rgb = AZUL
    agregar_notas(
        s,
        "La base no nace limpia: 13 446 anuncios únicos pasan por filtros y quedan 9 841. "
        "La composición muestra el peso de combustión, bicicletas y eléctricas; las patinetas son el segmento más pequeño.",
    )

    # ------------------------------------------------------------------ 4
    s = prs.slides.add_slide(blanca)
    encabezado(s, "03 · Los hallazgos", "Dólar, capital y segmentación", 4)
    # Tarjetas superiores
    caja(s, 0.8, 1.95, 5.65, 1.35, AZUL_CLARO)
    texto(s, 1.05, 2.08, 2.3, 0.7, "97,4 %", tam=34, color=NARANJA, negrita=True)
    texto(s, 1.05, 2.72, 5.1, 0.4, "de los anuncios con moneda están en USD", tam=13, color=AZUL)
    caja(s, 6.7, 1.95, 5.8, 1.35, AZUL_CLARO)
    texto(s, 6.95, 2.08, 2.8, 0.7, "94,8 %", tam=34, color=NARANJA, negrita=True)
    texto(s, 6.95, 2.72, 5.3, 0.4, "de los anuncios se concentran en La Habana", tam=13, color=AZUL)

    datos = CategoryChartData()
    datos.categories = ["Combustión", "Eléctricas", "Patinetas", "Bicicletas"]
    datos.add_series("Mediana USD", (2200, 1485, 720, 160))
    marco = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(3.65), Inches(7.8), Inches(2.95), datos
    )
    grafico = marco.chart
    grafico.has_legend = False
    grafico.has_title = True
    grafico.chart_title.text_frame.text = "Precio mediano pedido (USD)"
    for p in grafico.chart_title.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = AZUL
    serie = grafico.series[0]
    for i, color in enumerate([AZUL, AZUL_MEDIO, RGBColor(0x7F, 0xA3, 0xC2), NARANJA]):
        punto = serie.points[i]
        punto.format.fill.solid()
        punto.format.fill.fore_color.rgb = color
        punto.format.line.fill.background()
    grafico.plots[0].has_data_labels = True
    etiquetas = grafico.plots[0].data_labels
    etiquetas.font.size = Pt(12)
    etiquetas.font.bold = True
    etiquetas.font.name = FONT
    etiquetas.font.color.rgb = AZUL
    etiquetas.position = XL_LABEL_POSITION.OUTSIDE_END
    grafico.value_axis.maximum_scale = 2500
    grafico.value_axis.major_unit = 500
    grafico.value_axis.has_major_gridlines = True
    grafico.value_axis.major_gridlines.format.line.color.rgb = GRIS_CLARO
    grafico.value_axis.tick_labels.font.size = Pt(9)
    grafico.value_axis.tick_labels.font.name = FONT
    grafico.value_axis.tick_labels.font.color.rgb = GRIS
    grafico.category_axis.tick_labels.font.size = Pt(10)
    grafico.category_axis.tick_labels.font.name = FONT
    grafico.category_axis.tick_labels.font.color.rgb = AZUL

    texto(
        s,
        8.9,
        3.75,
        3.6,
        0.3,
        "LA LECTURA",
        tam=10,
        color=NARANJA,
        negrita=True,
    )
    texto(
        s,
        8.9,
        4.1,
        3.6,
        1.9,
        "La bicicleta es la puerta de entrada más barata.\n\n"
        "La combustión es el segmento más caro.\n\n"
        "La eléctrica queda en medio: accesible, pero muy dispersa.",
        tam=14,
        color=AZUL,
        interlineado=1.05,
    )
    agregar_notas(
        s,
        "Tres hallazgos: el mercado está dolarizado, concentrado en La Habana y segmentado por categoría. "
        "La mediana de combustión es 2 200 USD; la de bicicleta, 160 USD. La eléctrica es la opción motorizada más barata, pero la más heterogénea.",
    )

    # ------------------------------------------------------------------ 5
    s = prs.slides.add_slide(blanca)
    encabezado(s, "04 · La grieta", "El silencio de los títulos", 5)
    texto(s, 0.8, 1.95, 6.0, 0.3, "MUESTRA ALEATORIA DE 200 TÍTULOS", tam=10, color=GRIS, negrita=True)
    texto(s, 0.8, 2.25, 6.0, 1.1, "84,5 %", tam=78, color=NARANJA, negrita=True)
    texto(
        s,
        0.8,
        3.45,
        5.8,
        0.9,
        "no menciona ninguno de los seis temas analizados: estado, batería, papeles, "
        "motivo de venta, urgencia o negociación.",
        tam=17,
        color=AZUL,
        interlineado=1.05,
    )
    barra_apilada(s, 0.8, 4.65, 5.8, 0.28, 0.845, "169 de 200", "31 con tema", NARANJA, GRIS_CLARO)
    texto(
        s,
        0.8,
        5.4,
        5.8,
        0.8,
        "El anuncio describe el vehículo, pero casi no explica la operación.",
        tam=15,
        color=GRIS,
        cursiva=True,
    )

    caja(s, 7.3, 1.95, 5.25, 4.35, AZUL_CLARO)
    texto(s, 7.7, 2.2, 0.8, 0.8, "“", tam=80, color=NARANJA, negrita=True)
    texto(
        s,
        7.7,
        3.05,
        4.4,
        1.3,
        "El silencio\ntambién es un dato.",
        tam=30,
        color=AZUL,
        negrita=True,
        interlineado=1.0,
    )
    texto(
        s,
        7.7,
        4.55,
        4.35,
        1.3,
        "La información que falta —por qué vende, si tiene papeles, si acepta negociar— "
        "se resuelve en la conversación privada, fuera del anuncio.",
        tam=13,
        color=GRIS,
        interlineado=1.1,
    )
    agregar_notas(
        s,
        "La grieta es la escasez de información: 169 de 200 títulos no mencionan ninguno de los seis temas. "
        "El título no es el mercado, es la puerta de entrada. El silencio también es un dato.",
    )

    # ------------------------------------------------------------------ 6
    s = prs.slides.add_slide(blanca)
    encabezado(s, "05 · El método", "Dos lecturas, una misma dirección", 6)
    # Columna izquierda
    texto(s, 0.8, 1.95, 5.5, 0.4, "200 títulos · 6 temas", tam=18, color=AZUL, negrita=True)
    texto(s, 0.8, 2.4, 5.5, 0.3, "Muestra aleatoria, semilla 2026", tam=11, color=GRIS)
    barra_apilada(s, 0.8, 2.95, 5.2, 0.32, 0.845, "84,5 % sin tema", "15,5 % con tema", NARANJA, GRIS_CLARO)
    texto(
        s,
        0.8,
        3.75,
        5.1,
        1.5,
        "Lectura título por título. La mayoría de los anuncios no aporta ninguna señal "
        "de estado, batería, papeles, urgencia o negociación.",
        tam=14,
        color=GRIS,
        interlineado=1.1,
    )
    # Columna derecha
    texto(s, 6.9, 1.95, 5.6, 0.4, "9 841 títulos · 8 temas", tam=18, color=AZUL, negrita=True)
    texto(s, 6.9, 2.4, 5.6, 0.3, "Taxonomía más amplia", tam=11, color=GRIS)
    barra_apilada(s, 6.9, 2.95, 5.3, 0.32, 0.54, "54,0 % sin tema", "46,0 % con tema", AZUL_MEDIO, GRIS_CLARO)
    texto(
        s,
        6.9,
        3.75,
        5.2,
        1.5,
        "Incluye especificaciones técnicas, uso, precio, contacto y accesorios: "
        "señales más frecuentes que el motivo de venta o la negociación.",
        tam=14,
        color=GRIS,
        interlineado=1.1,
    )
    caja(s, 0.8, 5.45, 11.7, 1.0, NARANJA_CLARO)
    texto(
        s,
        1.05,
        5.6,
        11.2,
        0.7,
        "La diferencia no es contradicción: la taxonomía amplia capta más señales. "
        "Ambas lecturas apuntan a lo mismo: el título describe el vehículo, no la operación.",
        tam=14,
        color=AZUL,
        negrita=True,
        interlineado=1.05,
    )
    agregar_notas(
        s,
        "Dos formas de mirar el mismo corpus. La muestra de 200 títulos usa seis temas y da 84,5 % sin tema. "
        "El total de 9 841 usa ocho temas y da 54,0 % sin tema. La diferencia se explica por la taxonomía, no por una contradicción.",
    )

    # ------------------------------------------------------------------ 7
    s = prs.slides.add_slide(blanca)
    encabezado(s, "06 · El mapa", "Lo que sí y lo que no", 7)
    # Columna sí
    caja(s, 0.8, 1.95, 5.7, 3.65, AZUL_CLARO)
    texto(s, 1.1, 2.15, 0.5, 0.5, "✓", tam=24, color=VERDE, negrita=True)
    texto(s, 1.55, 2.15, 4.6, 0.4, "Sí podemos decir", tam=18, color=AZUL, negrita=True)
    vinetas(
        s,
        1.1,
        2.75,
        5.0,
        2.5,
        [
            "El mercado está dolarizado: 97,4 % en USD.",
            "La Habana concentra el 94,8 % de los anuncios.",
            "Los precios medianos segmentan: 2 200 / 1 485 / 720 / 160 USD.",
        ],
        tam=14,
        espacio=13,
    )
    # Columna no
    caja(s, 6.8, 1.95, 5.7, 3.65, NARANJA_CLARO)
    texto(s, 7.1, 2.15, 0.5, 0.5, "✕", tam=22, color=NARANJA, negrita=True)
    texto(s, 7.55, 2.15, 4.6, 0.4, "No podemos afirmar", tam=18, color=AZUL, negrita=True)
    vinetas(
        s,
        7.1,
        2.75,
        5.0,
        2.5,
        [
            "Son precios pedidos, no precios de transacción.",
            "La muestra no es representativa del país.",
            "La cobertura de marca, año y cilindrada es baja.",
            "La clasificación automática puede tener falsos positivos.",
        ],
        tam=13,
        espacio=9,
        color_vineta=NARANJA,
    )
    texto(
        s,
        0.8,
        5.9,
        11.7,
        0.5,
        "Esta entrega describe el discurso de la oferta, no la demanda ni la experiencia de los compradores.",
        tam=14,
        color=GRIS,
        cursiva=True,
        alineacion=PP_ALIGN.CENTER,
    )
    agregar_notas(
        s,
        "Cerrar la parte de hallazgos con honestidad: lo que sí se puede afirmar y lo que no. "
        "El alcance es el discurso de la oferta; no se miden precios de transacción ni experiencia de compradores.",
    )

    # ------------------------------------------------------------------ 8
    s = prs.slides.add_slide(blanca)
    fondo(s, AZUL)
    for cx, cy, d, color in [
        (-0.9, -0.9, 3.8, NARANJA),
        (11.4, 5.2, 3.0, AZUL_MEDIO),
    ]:
        circulo = s.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(cx), Inches(cy), Inches(d), Inches(d)
        )
        circulo.fill.background()
        circulo.line.color.rgb = color
        circulo.line.width = Pt(2)
        circulo.shadow.inherit = False
    texto(s, 0.9, 1.35, 8.5, 0.3, "EL CIERRE", tam=12, color=NARANJA, negrita=True)
    texto(
        s,
        0.9,
        1.95,
        9.8,
        2.2,
        "No es un retrato completo;\nes un mapa honesto.",
        tam=44,
        color=BLANCO,
        negrita=True,
        interlineado=0.95,
    )
    texto(
        s,
        0.9,
        4.55,
        9.5,
        0.9,
        "La siguiente fase: ampliar la muestra, leer el cuerpo completo de los anuncios "
        "y cruzar los precios con otras fuentes.",
        tam=17,
        color=AZUL_CLARO,
        interlineado=1.1,
    )
    linea(s, 0.9, 5.85, 4.8, 5.85, NARANJA, 3)
    texto(s, 0.9, 6.1, 6.0, 0.5, "Gracias", tam=24, color=NARANJA, negrita=True)
    texto(
        s,
        0.9,
        6.7,
        8.0,
        0.3,
        "Brigitte Hernández Romero · Ciencia de Datos · Universidad de La Habana",
        tam=10,
        color=GRIS_CLARO,
    )
    agregar_notas(
        s,
        "Cerrar con la idea del mapa honesto: no es un retrato completo, pero sí una línea base reproducible. "
        "El siguiente paso es ampliar la muestra y leer el cuerpo completo de los anuncios.",
    )

    salida = REPORTS / "storytelling_proyecto.pptx"
    prs.save(salida)
    print(f"Presentación generada: {salida}")
    print(f"Diapositivas: {len(prs.slides)}")


if __name__ == "__main__":
    main()
