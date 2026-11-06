# Entrega final

Esta carpeta reúne las copias listas para entregar del informe y de la
presentación. La fuente de trabajo sigue estando en `reports/` y `docs/`.

## Contenido

- `informe.pdf` — informe final (18 páginas, A4), con el análisis de contenido
  de una muestra de 200 títulos y el contraste con los 9 841 anuncios.
- `informe.docx` — versión editable del mismo informe.
- `storytelling_proyecto.pptx` — presentación de 8 diapositivas (16:9) con el
  storytelling del proyecto, cifras y gráficos nativos.
- `NOTA_AL_PROFESOR.md` — nota de acompañamiento; ajústala con el nombre del
  profesor antes de enviarla.
- `entrega_proyecto_mercado_vehiculos.zip` — paquete con el PDF, el DOCX, el
  PPTX, la nota y este LEEME, listo para descargar o enviar.
- `LEEME.md` — este archivo.

## Cómo abrir cada archivo

- **PDF:** doble clic; se abre en el visor de PDF del sistema.
- **PPTX:** doble clic si tienes PowerPoint o LibreOffice Impress. También se
  puede subir a Google Slides.
- **DOCX:** doble clic si tienes Word o LibreOffice Writer.

## Estado del componente cualitativo

- **0 entrevistas válidas** registradas.
- Las 30 entrevistas previstas quedan para una segunda fase.
- Para esta entrega se usó la **Opción B**: análisis del discurso de la oferta
  a partir de los anuncios, no entrevistas.
- No se usaron nombres, fotos ni respuestas de los 10 contactos sin
  consentimiento escrito.

## Archivos fuente

- `reports/informe.md` — texto fuente del informe.
- `reports/informe.html` — HTML intermedio.
- `reports/informe.pdf` — PDF canónico.
- `reports/informe.docx` — DOCX canónico.
- `reports/storytelling_proyecto.pptx` — PPTX canónico de la presentación.
- `docs/STORYTELLING.md` — narrativa y guion de la presentación.
- `src/generar_storytelling_pptx.py` — genera la presentación.
- `reports/analisis_200_titulos.txt` — resultados de la muestra de 200 títulos.
- `reports/muestra_200_titulos.csv` — muestra auditable.
- `reports/analisis_temas.txt` — contraste con los 9 841 títulos.
- `reports/figures/` — 18 figuras PNG.
- `src/analisis_200_titulos.py` — genera la muestra y su análisis.
- `src/temas_anuncios.py` — clasifica los 9 841 títulos.
- `src/generar_informe.py` — regenera el HTML del informe.
- `docs/HANDOFF.md` — estado actual del proyecto.
- `docs/JOURNAL.md` — registro de sesiones.

## Regenerar el informe

```bash
cd /home/bri/proyectos/proyecto-mercado-vehiculos
.venv/bin/python -m src.analisis_200_titulos
.venv/bin/python -m src.generar_informe
soffice --headless --convert-to pdf --outdir reports reports/informe.html
soffice --headless --convert-to 'docx:MS Word 2007 XML' --outdir reports reports/informe.html
```

## Regenerar la presentación

```bash
cd /home/bri/proyectos/proyecto-mercado-vehiculos
.venv/bin/python -m src.generar_storytelling_pptx
```

Después de regenerar, vuelve a copiar `reports/informe.pdf`,
`reports/informe.docx` y `reports/storytelling_proyecto.pptx` a esta carpeta.
