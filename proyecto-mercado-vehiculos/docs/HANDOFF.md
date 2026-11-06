# Handoff — Mercado de motos, bicicletas y patinetas en Cuba

> **Última actualización:** 2026-11-06 00:06 EST
> **Sesión:** Opción B, PDF final, carpeta de entrega, storytelling y presentación
> **Estado:** informe de 18 páginas con 9 841 anuncios; análisis de 200 títulos + contraste con 9 841; 0 entrevistas válidas; entrega y presentación en `entrega/`; narrativa en `docs/STORYTELLING.md`; PPTX de 8 diapositivas

## 1. TL;DR

El proyecto está en `/home/bri/proyectos/proyecto-mercado-vehiculos`. La
recolección completa de Revolico terminó: **13 446 anuncios únicos**. El filtro
de relevancia dejó **11 621 relacionados** y, tras quitar duplicados,
**10 804 anuncios únicos** de motos, bicicletas y patinetas. La limpieza con
pandas ya se ejecutó y dejó **9 841 anuncios limpios** en
`data/processed/anuncios_limpios.csv`. También se generaron **18 figuras** en
`reports/figures/` y Jupyter quedó instalado en `.venv`. Los notebooks
`02_limpieza.ipynb` y `03_eda.ipynb` ya se ejecutaron con salidas guardadas.
El informe está redactado y exportado en `reports/informe.pdf` (**18 páginas**),
con un análisis de contenido de una muestra aleatoria de **200 títulos** y un
contraste con los **9 841** títulos del dataset. En entrevistas **no hay ninguna
fila utilizable**: E01 está en el CSV pero **excluida** por no tener
consentimiento firmado, y de las 10 personas solo quedan nombres y fotos, sin
respuestas registradas. La meta de **30 entrevistas cortas nuevas** queda para
una segunda fase; para esta entrega se usó la Opción B (análisis de los
anuncios, sin entrevistas). El campo se reinicia con
`docs/PROTOCOLO_TRABAJO_CAMPO.md`. La presentación de storytelling
(**8 diapositivas**, 16:9, sin menciones a entrevistas) está en
`reports/storytelling_proyecto.pptx` y `entrega/storytelling_proyecto.pptx`.

## 2. Objetivo y alcance

- **Objetivo:** analizar el mercado de motos, bicicletas y patinetas en Cuba a
  partir de anuncios clasificados de Revolico.
- **Alcance actual:** dataset reproducible + notebooks de limpieza/EDA +
  informe con análisis de contenido de los anuncios. El estudio cualitativo de
  30 personas queda para una segunda fase.
- **Muestra cualitativa prevista:** 30 entrevistas cortas nuevas (E01–E30), no
  probabilística y por conveniencia. **No completada:** 0 válidas al cierre.
- **Incluye:** motos de combustión, motos eléctricas, bicicletas y patinetas.
- **Excluye por decisión:** cualquier vehículo que no sea moto, bicicleta o
  patineta.
- **Fuera de alcance de la parte pública:** datos personales, imágenes de
  personas, transacciones reales y scraping masivo sin límites. Los nombres y
  las fotos de vehículos solo existen en la carpeta privada
  `data/raw/entrevistas/`, con consentimiento escrito.

## 3. Estado actual

### Funciona
- `src/scraper.py`: recolección completa terminada. 13 446 anuncios únicos:
  `motos_electricas` 4 300, `motos_combustion` 4 299, `bicicletas` 4 204,
  `patinetas` 643.
- `src/relevancia.py`: filtro heurístico en tres clases (`si`, `revisar`,
  `no`). Genera las copias de anuncios relacionados y los archivos de revisión.
- `src/analisis_basico.py`: análisis descriptivo sin pandas. Lee por defecto
  `data/processed/anuncios_relacionados_unicos.csv` y escribe
  `reports/analisis_basico.txt`.
- `src/enriquecer.py`: añade `marca`, `anio`, `condicion`, `cilindrada_cc` y
  `tipo` al dataset relacionado; escribe `anuncios_enriquecidos.csv`.
- `src/clean.py`: **ejecutado**. Lee el dataset relacionado único, descarta
  precios nulos/señuelo, deduplica, deriva variables y escribe
  `data/processed/anuncios_limpios.csv` (9 841 filas).
- `src/figuras.py`: **ejecutado**. Genera 10 PNG en `reports/figures/` a partir
  de `anuncios_limpios.csv`.
- `src/temas_anuncios.py`: **ejecutado**. Clasifica los 9 841 títulos en ocho
  temas y genera `reports/analisis_temas.txt` y `07_temas_anuncios.png`.
- `src/analisis_200_titulos.py`: **ejecutado**. Toma una muestra aleatoria de
  200 títulos (semilla 2026), los clasifica en seis temas, extrae 8 ejemplos y
  genera `reports/analisis_200_titulos.txt`,
  `reports/muestra_200_titulos.csv` y `08_temas_200_titulos.png`.
- `src/generar_informe.py`: **creado**. Convierte `reports/informe.md` en HTML
  con la hoja de estilo del informe y ajusta las imágenes para LibreOffice.
- `src/privacidad.py`: redacta teléfonos, correos y enlaces de contacto.
- `src/details.py`: muestreo para descripciones (no ejecutado sobre el dataset
  completo).
- `src/transcribir.py`: transcripción local de audios con `faster-whisper`.
  El audio que estaba fuera del proyecto (`/home/bri/Recording 9.flac`) se
  copió a `data/raw/entrevistas/SIN_ASIGNAR_2026-11-01.flac`. La transcripción
  quedó pendiente: la descarga del modelo `base` avanzó solo 2,7 MB en 6 min y
  se canceló; reintentar con mejor conexión o con `--modelo tiny`.
- `src/entrevistas.py`: resume `data/processed/entrevistas.csv` y escribe
  `reports/entrevistas_resumen.txt`; incluye triangulación con los precios de
  `anuncios_limpios.csv`. Probado con E01.
- Materiales de campo: `docs/PROTOCOLO_TRABAJO_CAMPO.md`,
  `docs/CONSENTIMIENTO_INFORMADO.md`, `docs/CONSENTIMIENTO_CORTO.md`,
  `docs/GUION_ENTREVISTA_CORTA.md`, `docs/FICHA_ENTREVISTA_RAPIDA.md`,
  `docs/KIT_1_2_ENTREVISTAS.md`, `docs/PLANTILLA_CITA_TEXTUAL.md`,
  `docs/GUION_RECONTACTO.md` y `docs/VACIADO_ENTREVISTAS.md`.
- Carpeta privada `data/raw/entrevistas/` (ignorada por Git): `README.md` con
  las reglas, `indice_privado.csv` para nombres/contactos autorizados y las
  subcarpetas `fotos/` y `transcripciones/`.
- `notebooks/02_limpieza.ipynb`: **ejecutado** con el kernel del `.venv`
  (9 celdas de código, 0 errores); salidas guardadas en el propio notebook.
- `notebooks/03_eda.ipynb`: **ejecutado** (9 celdas, 0 errores); genera 6
  figuras en `reports/figures/` y deja tablas de resultados en el notebook.
- `reports/informe.pdf`: **regenerado** (18 páginas) con la muestra de 200
  títulos como análisis principal, el contraste con los 9 841 y la limitación
  de las entrevistas declarada.
- `src/generar_storytelling_pptx.py`: **creado y ejecutado**. Genera
  `reports/storytelling_proyecto.pptx` (8 diapositivas, 16:9) con gráficos
  nativos; revisado visualmente y sin menciones a entrevistas.
- `entrega/`: **creada** con las copias finales `informe.pdf`, `informe.docx`,
  `storytelling_proyecto.pptx`, `NOTA_AL_PROFESOR.md`, `LEEME.md` y el paquete
  `entrega_proyecto_mercado_vehiculos.zip`. El PDF de `entrega/` coincide byte a
  byte con `reports/informe.pdf`; el PPTX también es copia idéntica.
- `~/Desktop/Proyecto-Mercado-Vehiculos/`: copia de la entrega para guardar en
  el PC, con el PDF, el DOCX, el PPTX, la nota, el LEEME y el ZIP.
- `README.md`: sección **“Informe final”** con enlaces al PDF, al DOCX y a la
  copia de entrega.
- `python -m py_compile src/*.py` → OK.

### Entorno
- `.venv` con Python **3.13.5**.
- Instalados: `pandas` 3.1.1, `numpy` 2.5.4, `matplotlib` 3.11.2,
  `seaborn` 0.13.2 y `faster-whisper` 1.2.1.
- **Jupyter instalado** en `.venv`: `jupyterlab` 4.6.5, `notebook` 7.6.4,
  `ipykernel` 7.4.0 y `nbformat` 5.11.1. Kernel `python3` registrado en
  `.venv/share/jupyter/kernels/python3`.
- **Presentación:** `python-pptx` 1.0.2, `lxml` 6.1.3 y `XlsxWriter` 3.3.1
  instalados en `.venv`.

### No funciona / bloqueado
- Entrevistas: **0 válidas de 30**. E01 está en el CSV pero excluida por falta
  de consentimiento firmado. Las 10 personas con nombre y foto no tienen
  respuestas registradas ni consentimiento escrito; no se usan.
- **Para esta entrega se usó la Opción B**: análisis de contenido de 200
  títulos y contraste con los 9 841. Las **30 entrevistas cortas** quedan para
  una segunda fase; no bloquean el PDF actual.
- Transcripción del audio: la descarga del modelo `base` de Whisper fue demasiado
  lenta (2,7 MB en 6 min) y se canceló. Reintentar con mejor conexión o con
  `--modelo tiny`.

### Sin verificar
- Calidad real de `marca`, `condicion`, `tipo` y `anio` sobre el dataset
  completo (cobertura baja de año, marca y cilindrada).
- Comportamiento de la conversión CUP→USD con una tasa real.
- Vehículos fuera de alcance que no se nombren en el título.

## 4. Números del dataset

Recolección: 2026-11-04 22:27–22:36 EST. Ventana de publicación observada:
2026-09-05 → 2026-11-05.

| Etapa | Anuncios |
|---|---|
| Recolectados únicos | 13 446 |
| Relacionados (`si`) | 11 621 |
| Para revisar | 295 |
| Excluidos | 1 530 |
| Duplicados por título+precio+municipio | 817 |
| **Relacionados únicos** | **10 804** |
| Descartados en limpieza (precio nulo/señuelo) | 963 |
| **Anuncios limpios** | **9 841** |

Relacionados únicos por categoría (antes de limpiar):

| Categoría | Anuncios |
|---|---|
| `motos_combustion` | 3 621 |
| `bicicletas` | 3 593 |
| `motos_electricas` | 3 018 |
| `patinetas` | 572 |

Dataset limpio por categoría:

| Categoría | Anuncios |
|---|---|
| `motos_combustion` | 3 349 |
| `bicicletas` | 3 146 |
| `motos_electricas` | 2 807 |
| `patinetas` | 539 |

Calidad del dataset limpio:

- Moneda: USD 9 589, CUP 251, MLC 1.
- `precio`/`moneda` vacíos: 0 (los 963 con precio nulo o señuelo se
  descartaron).
- Precio en USD: mediana **1 100**, media 1 398,6, mínimo 5, máximo 111 111.
- Mediana por categoría (USD): bicicletas 160; patinetas 720; motos eléctricas
  1 485; motos de combustión 2 200.
- Cobertura de variables derivadas: `anio` 8,4 %; `marca` 31,3 %;
  `cilindrada_cc` 13,6 %; `condicion` 100 % (8 763 `no_especificada`);
  `tipo` 100 % (3 352 eléctrica, 3 346 combustión, 3 143 no especificada).
- Provincia: 16 provincias; La Habana 9 326 (94,8 %).

### Hallazgos preliminares del EDA

- **Precios por categoría (USD, mediana):** combustión 2 200; eléctricas 1 490;
  patinetas 720; bicicletas 160.
- **Eléctricas vs. combustión:** las eléctricas son más baratas en mediana
  (1 490 vs 2 200), pero tienen mayor dispersión (desv. típ. 3 115 vs 2 258),
  consistente con la hipótesis de partida.
- **Geografía:** La Habana concentra 9 080 de los 9 589 anuncios en USD y tiene
  mediana de 1 000 USD. Las provincias con mediana más alta son Pinar del Río
  (2 000) y Holguín (1 850); las más bajas, Cienfuegos (210) y Santiago de Cuba
  (280), aunque con pocos anuncios.
- **Año y cilindrada:** solo 829 de 9 589 anuncios USD tienen año y 1 343 tienen
  cilindrada, así que los cruces son exploratorios y no concluyentes.
- **Patinetas:** 535 anuncios USD con mediana de 720; la categoría tiene ruido
  (carriolas, scooters infantiles, sets de protección), que hay que declarar.

### Análisis de contenido (Opción B)

- Muestra aleatoria de **200 títulos** (semilla 2026): 68 bicicletas,
  65 motos de combustión, 58 eléctricas y 9 patinetas.
- **31 títulos (15,5 %)** mencionan al menos uno de los seis temas;
  **169 (84,5 %)** no mencionan ninguno.
- Frecuencias en la muestra: nueva o usada 17 (8,5 %), batería o autonomía
  11 (5,5 %), papeles o garantía 3 (1,5 %), motivo de venta 0 (0,0 %),
  urgente 1 (0,5 %) y negociable 1 (0,5 %).
- Comparación con el total de 9 841: 8,6 %, 6,5 %, 3,2 %, 0,1 %, 0,1 % y
  0,4 %, respectivamente.
- Contraste con ocho temas sobre los 9 841: 54,0 % sin tema; especificaciones
  técnicas 22,1 %, estado o novedad 16,4 %, precio 6,8 %, uso 5,5 %, urgencia
  4,7 % y papeles 1,6 %.
- Limitación: clasificación automática por palabras clave; hay falsos
  positivos (por ejemplo, “Autonomía 35 KM/L” en una moto de combustión). No
  sustituye a las entrevistas.

### Estado de las entrevistas

| Concepto | Valor |
|---|---|
| Meta | 30 personas |
| Personas contactadas antes | 10, sin respuestas ni consentimiento escrito |
| Entrevistas válidas | 0 |
| Filas en el CSV | 1 (E01, excluida) |
| Entrevistas cortas pendientes | 30 (E01–E30) |
| Consentimiento | formulario listo; sin firma la fila no cuenta |
| Materiales | protocolo, consentimiento corto, guion, ficha y kit de 1–2 entrevistas |
| Carpeta privada | `data/raw/entrevistas/` con README e `indice_privado.csv` |
| Audio disponible | `SIN_ASIGNAR_2026-11-01.flac` (11 MB), pendiente de asignar a un E__ y de transcribir |

> No se inventan respuestas ni personas. Si no se llega a 30, se documenta la
> limitación y se negocia con el profesor.

## 5. Cómo ejecutar

```bash
cd /home/bri/proyectos/proyecto-mercado-vehiculos

# Requisitos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Recolección completa (ya hecha)
python -m src.scraper --max-pages 43

# Filtro de relevancia
python -m src.relevancia

# Enriquecimiento (marca, año, condición, cilindrada, tipo)
python -m src.enriquecer

# Limpieza (genera anuncios_limpios.csv)
python -m src.clean

# Figuras (usar el dataset limpio)
python -m src.figuras --input data/processed/anuncios_limpios.csv

# Análisis de contenido de los anuncios
python -m src.temas_anuncios
python -m src.analisis_200_titulos

# Regenerar el informe HTML y luego el PDF con LibreOffice
python -m src.generar_informe
soffice --headless --convert-to pdf --outdir reports reports/informe.html

# Regenerar la presentación de storytelling
python -m src.generar_storytelling_pptx

# Resumen y triangulación de entrevistas
python -m src.entrevistas

# Notebooks
jupyter lab
```

## 6. Estructura relevante

```text
proyecto-mercado-vehiculos/
├── AGENTS.md                      # instrucciones para OpenCode
├── EMPIEZA_AQUI.md                # primeros pasos
├── README.md                      # reproducción
├── requirements.txt
├── entrega/                       # copias finales para entregar
│   ├── informe.pdf
│   ├── informe.docx
│   ├── storytelling_proyecto.pptx
│   ├── NOTA_AL_PROFESOR.md
│   ├── LEEME.md
│   └── entrega_proyecto_mercado_vehiculos.zip
├── data/
│   ├── README.md                  # diccionario de datos
│   ├── raw/                       # HTML crudo + scrape.log
│   └── processed/                 # anuncios.csv y derivados
├── docs/
│   ├── metodologia.md             # fuente, método, ética, registro
│   ├── CRITERIOS_RELEVANCIA.md    # reglas del filtro
│   ├── PLAN_DE_TRABAJO.md         # ruta paso a paso
│   ├── PLAN_ANALISIS.md           # datos y análisis previstos
│   ├── ENTREVISTAS.md             # diseño del estudio cualitativo
│   ├── PROTOCOLO_TRABAJO_CAMPO.md # plan para completar 30 entrevistas
│   ├── CONSENTIMIENTO_INFORMADO.md # formulario de consentimiento
│   ├── GUION_ENTREVISTA_CORTA.md  # guion imprimible de 8 preguntas
│   ├── GUION_RECONTACTO.md        # recuperar E01–E10
│   ├── VACIADO_ENTREVISTAS.md     # de las notas al CSV, columna por columna
│   ├── cuestionario_entrevistas.json  # 63 preguntas + plantillas E01–E10
│   ├── prompt-handoff-journal.md  # prompt reutilizable
│   ├── HANDOFF.md                 # este documento
│   ├── STORYTELLING.md            # narrativa del proyecto para exponer
│   └── JOURNAL.md                 # bitácora
├── notebooks/
│   ├── 01_scraping.ipynb
│   ├── 02_limpieza.ipynb
│   └── 03_eda.ipynb
├── reports/
│   ├── informe.md                 # informe final redactado
│   ├── informe.html               # versión HTML intermedia
│   ├── informe.pdf                # versión para entrega (18 páginas)
│   ├── informe.docx               # versión editable
│   ├── storytelling_proyecto.pptx # presentación de 8 diapositivas
│   ├── analisis_200_titulos.txt   # muestra de 200 títulos (Opción B)
│   ├── muestra_200_titulos.csv    # títulos clasificados, sin datos personales
│   ├── analisis_temas.txt         # contraste con los 9 841 títulos
│   ├── relevancia_resumen.txt
│   ├── analisis_basico.txt
│   └── figures/                   # 18 PNG generados
└── src/
    ├── config.py
    ├── scraper.py
    ├── details.py
    ├── clean.py
    ├── relevancia.py
    ├── analisis_basico.py
    ├── extraccion.py
    ├── privacidad.py
    ├── enriquecer.py
    ├── figuras.py
    ├── temas_anuncios.py
    ├── analisis_200_titulos.py
    ├── generar_informe.py
    ├── generar_storytelling_pptx.py
    ├── entrevistas.py
    └── transcribir.py
```

Archivos de datos generados:

- `data/processed/anuncios.csv` — 13 446 anuncios crudos.
- `data/processed/anuncios_relacionados.csv` — 11 621 `si`.
- `data/processed/anuncios_relacionados_unicos.csv` — 10 804 sin duplicados.
- `data/processed/anuncios_enriquecidos.csv` — 10 804 con variables derivadas.
- `data/processed/anuncios_limpios.csv` — **9 841** anuncios limpios.
- `data/processed/anuncios_revisar.csv` — 295 ambiguos.
- `data/processed/entrevistas.csv` — plantilla de 53 columnas con E01 migrada.
- `data/raw/entrevistas/` — **privada**: audios, fotos de vehículos,
  consentimientos e índice de nombres (ignorada por Git).
- `data/processed/anuncios_excluidos.csv` — 1 530 con motivo.

Figuras generadas en `reports/figures/`:

`fig01_anuncios_categoria.png`, `fig02_provincia.png`,
`fig03_precio_categoria.png`, `fig04_precio_histograma.png`,
`fig05_precio_anio.png`, `fig06_precio_condicion.png`, `fig07_marcas.png`,
`fig08_precio_marca.png`, `fig09_precio_provincia.png`,
`fig10_precio_cilindrada.png`.

Figuras del notebook 03 (nombres distintos, conviven con las anteriores):

`01_composicion.png`, `02_precios.png`, `03_precio_caracteristicas.png`,
`04_marcas.png`, `05_provincias.png`, `06_tipo_moto.png`.

Total en `reports/figures/`: **18 PNG** (las 16 anteriores más
`07_temas_anuncios.png`, del análisis de contenido de los 9 841 títulos, y
`08_temas_200_titulos.png`, de la muestra de 200 títulos).

## 7. Decisiones tomadas

| Fecha | Decisión | Motivo | Consecuencia |
|---|---|---|---|
| 2026-11-04 | Usar Revolico como fuente | Mercado cubano y acceso permitido por `robots.txt` | Dependencia de un sitio que puede cambiar |
| 2026-11-04 | Parsear `__NEXT_DATA__` en vez de CSS | JSON estructurado y estable | Si cambia el estado de Apollo, ajustar `parse_state` |
| 2026-11-04 | No usar Selenium | El HTML llega renderizado del servidor | Menos peso y más velocidad |
| 2026-11-04 | No guardar datos personales | Ética y privacidad | Se descartan teléfono, nombre y `userId` |
| 2026-11-04 | No convertir CUP a USD por defecto | Evitar conclusiones inválidas | El análisis separa monedas |
| 2026-11-04 | Patinetas por búsqueda de texto | No tienen subcategoría propia | Requieren filtrado posterior |
| 2026-11-04 | Excluir vehículos fuera de alcance | Decisión del alcance del proyecto | Se descartan y no se analizan; ver `docs/CRITERIOS_RELEVANCIA.md` |
| 2026-11-04 | Mantener un tercio de anuncios en `revisar` | El filtro es heurístico | Auditoría manual posible sin bloquear el dataset |
| 2026-11-05 | Descartar precios nulos y señuelo en `clean` | Evitar sesgar medias y distribuciones | 963 anuncios fuera; medianas más realistas |
| 2026-11-05 | Generar figuras desde `anuncios_limpios.csv` | Coherencia con el dataset depurado | Conteos y precios no incluyen señuelos |
| 2026-11-05 | Diseño mixto: 10 profundas + 20 cortas | Llegar a 30 sin alargar cada entrevista | Quedó sin efecto: las 10 no tienen respuestas ni consentimiento |
| 2026-11-05 | Nombres y fotos solo con consentimiento escrito | Privacidad y ética | Informe público con códigos; anexo privado opcional |
| 2026-11-05 | Descartar las 10 personas sin respuestas ni consentimiento | No se puede analizar ni publicar sin datos y autorización | Se reinicia el campo con 30 entrevistas cortas nuevas |
| 2026-11-05 | El análisis excluye filas con `consentimiento != si` | Evitar contar datos no autorizados | `src/entrevistas.py` muestra 0 válidas y 1 excluida |
| 2026-11-05 | Opción B: análisis de contenido de 200 títulos | No hay entrevistas válidas y no se deben inventar | El informe describe el discurso de la oferta, no la demanda; la limitación se declara |
| 2026-11-05 | La muestra de 200 títulos es el análisis principal; los 9 841 son contraste | La muestra permite leer título por título y el total verifica el patrón | Se presentan dos taxonomías y se explica la diferencia |
| 2026-11-05 | Fijar `width` y `height` en píxeles a las imágenes del HTML | LibreOffice ignora `max-width` y reserva altura natural | El PDF queda en 18 páginas, sin figuras recortadas ni páginas vacías |

## 8. Cambios recientes

- `src/clean.py` — ejecutado sobre `anuncios_relacionados_unicos.csv`:
  9 841 anuncios limpios; 963 descartados por precio nulo/señuelo.
- `src/figuras.py` — ejecutado con `--input data/processed/anuncios_limpios.csv`;
  10 figuras PNG generadas.
- `src/figuras.py` — corregida incompatibilidad con Matplotlib 3.11: los tres
  `boxplot()` usaban `labels=`, eliminado en esa versión; ahora usan
  `tick_labels=`.
- `data/processed/anuncios_limpios.csv` — nuevo archivo con 21 columnas.
- `reports/figures/` — 10 PNG nuevos.
- Instalado Jupyter en `.venv` (`jupyterlab` 4.6.5, `notebook` 7.6.4,
  `ipykernel` 7.4.0, `nbformat` 5.11.1) y registrado el kernel `python3`.
- `notebooks/02_limpieza.ipynb` — ejecutado en modo `nbconvert --execute
  --inplace`: 9 celdas de código, 0 errores, salidas guardadas. Se cambió su
  entrada de `anuncios.csv` (13 446 crudos) a
  `anuncios_relacionados_unicos.csv` (10 804 del alcance) para no reintroducir
  vehículos fuera de alcance. El CSV resultante (9 841 filas) coincide con el
  generado por `src.clean`.
- `notebooks/03_eda.ipynb` — ejecutado en modo `nbconvert --execute --inplace`:
  9 celdas, 0 errores; 6 figuras nuevas (`01_composicion.png` …
  `06_tipo_moto.png`) y tablas de resultados guardadas en el notebook.
- `src/entrevistas.py` — nuevo script de resumen y triangulación; probado con
  E01. Genera `reports/entrevistas_resumen.txt`.
- `data/processed/entrevistas.csv` — plantilla nueva de 53 columnas; E01
  migrada desde el esquema anterior.
- `docs/PROTOCOLO_TRABAJO_CAMPO.md`, `docs/CONSENTIMIENTO_INFORMADO.md` y
  `docs/GUION_ENTREVISTA_CORTA.md` — materiales para completar las 30.
- Trabajo intermedio ya presente pero no registrado antes en el journal:
  `src/extraccion.py`, `src/privacidad.py`, `src/enriquecer.py`,
  `src/figuras.py`, `src/transcribir.py`, `docs/ENTREVISTAS.md`,
  `docs/cuestionario_entrevistas.json` y `anuncios_enriquecidos.csv`.
- `src/analisis_200_titulos.py` — ejecutado: muestra aleatoria de 200 títulos
  (semilla 2026), 31 con al menos un tema (15,5 %), 169 sin tema (84,5 %),
  8 ejemplos y figura `08_temas_200_titulos.png`.
- `src/temas_anuncios.py` — ejecutado: 9 841 títulos clasificados en ocho
  temas; 54,0 % sin tema; figura `07_temas_anuncios.png`.
- `reports/informe.md` — reescrita la sección 4: 4.1 intento de entrevistas,
  4.2 muestra de 200 títulos, 4.3 contraste con los 9 841 y 4.4 limitación.
  Actualizados resumen, discusión, limitaciones, conclusiones,
  recomendaciones, referencias y anexos.
- `src/generar_informe.py` — creado: Markdown → HTML con hoja de estilo,
  `attr_list` para el salto de página y cálculo de ancho/alto de cada figura.
- `reports/informe.pdf` — regenerado (18 páginas) y revisado visualmente;
  `reports/informe.docx` e `reports/informe.html` regenerados.
- `docs/NOTA_AL_PROFESOR.md` — actualizada con la Opción B y el estado real
  del componente cualitativo.
- `entrega/` — creada con el PDF final, el DOCX, la nota para el profesor y
  `LEEME.md`; el PDF es copia idéntica de `reports/informe.pdf`.
- `README.md` — añadida la sección “Informe final” con enlaces a
  `reports/informe.pdf`, `reports/informe.docx` y `entrega/informe.pdf`.
- `reports/informe.md` — anexos simplificados: la reproducibilidad remite a
  `README.md` y `docs/HANDOFF.md`; las cuatro figuras adicionales quedan
  agrupadas a partir de una página nueva.
- `docs/STORYTELLING.md` — narrativa completa, versión corta para exponer,
  estructura de diapositivas y frases ancla. No menciona entrevistas.
- `src/generar_storytelling_pptx.py` — creado: genera una presentación de 8
  diapositivas con la paleta azul/naranja, gráficos nativos y notas del orador.
- `reports/storytelling_proyecto.pptx` — generado y revisado visualmente:
  8 diapositivas, 16:9, sin desbordes ni menciones a entrevistas.
- `entrega/storytelling_proyecto.pptx` — copia idéntica del PPTX canónico.
- `entrega/entrega_proyecto_mercado_vehiculos.zip` — paquete con PDF, DOCX,
  PPTX, nota y LEEME.
- `~/Desktop/Proyecto-Mercado-Vehiculos/` — copia de la entrega para el PC.

## 9. Próximo paso exacto

1. Revisar y entregar `entrega/informe.pdf` (**18 páginas**) y
   `entrega/storytelling_proyecto.pptx` (**8 diapositivas**) junto con
   `entrega/NOTA_AL_PROFESOR.md`. El PDF canónico sigue siendo
   `reports/informe.pdf` y el PPTX canónico
   `reports/storytelling_proyecto.pptx`; las copias de `entrega/` deben
   regenerarse si se modifican.
2. Si se quiere reforzar la parte cualitativa, hacer **1 o 2 entrevistas**
   con `docs/KIT_1_2_ENTREVISTAS.md`, `docs/CONSENTIMIENTO_CORTO.md` y
   `docs/FICHA_ENTREVISTA_RAPIDA.md`, y añadirlas como estudio piloto.
3. Para una segunda fase: hacer las **30 entrevistas cortas nuevas** (E01–E30)
   siguiendo `docs/PROTOCOLO_TRABAJO_CAMPO.md` y
   `docs/GUION_ENTREVISTA_CORTA.md`, 6 por día durante 5 días.
4. Firmar el consentimiento antes de cada entrevista. Sin firma, la fila no
   cuenta.
5. Pasar las respuestas al CSV con `docs/VACIADO_ENTREVISTAS.md` y ejecutar
   `.venv/bin/python -m src.entrevistas`.
6. Regenerar el informe con `python -m src.generar_informe` y convertir el HTML
   a PDF con LibreOffice. Regenerar la presentación con
   `python -m src.generar_storytelling_pptx`.

## 10. Contexto que no debe perderse

- `robots.txt` permite el acceso salvo checkout, cuenta, auth y favoritos.
- Pausa obligatoria de 2–4 s entre peticiones; no paralelizar.
- Los datos son **precios pedidos**, no precios de transacción.
- La muestra es **no probabilística** y está concentrada en La Habana.
- No mezclar USD y CUP sin una tasa documentada.
- El HTML crudo de cada página se guarda en `data/raw/`; no borrarlo.
- `data/` y `reports/figures/` están ignorados por Git salvo los `.gitkeep`.
- El `User-Agent` de `src/config.py` aún tiene un correo placeholder.
- Las entrevistas son 30 casos de conveniencia (todas cortas): describen
  patrones, no proporciones poblacionales.
- El análisis de contenido de los anuncios describe la **oferta** y su
  discurso; no mide demanda, precios de transacción ni experiencia de usuarios.
- La clasificación de títulos es automática por palabras clave y solo usa el
  título: puede tener falsos positivos y no capta lo que ocurre en la
  conversación privada.
- Las 10 personas anteriores no cuentan: solo hay nombres y fotos, sin
  respuestas ni consentimiento escrito. E01 está en el CSV pero excluida.
- El PDF canónico es `reports/informe.pdf`; `entrega/informe.pdf` es una copia
  idéntica. Si se regenera el informe, volver a copiarlo a `entrega/`.
- El PPTX canónico es `reports/storytelling_proyecto.pptx`; `entrega/` y el
  Escritorio tienen copias idénticas. Se regenera con
  `.venv/bin/python -m src.generar_storytelling_pptx`.
- La presentación y `docs/STORYTELLING.md` **no mencionan entrevistas** ni
  sugieren que se realizaron; el informe sí declara la limitación con 0 válidas.
- El ZIP `entrega/entrega_proyecto_mercado_vehiculos.zip` contiene el PDF, el
  DOCX, el PPTX, la nota y el LEEME con una carpeta raíz
  `Proyecto-Mercado-Vehiculos/`.
- La copia para el PC está en `~/Desktop/Proyecto-Mercado-Vehiculos/` y también
  incluye el ZIP.
- El informe público usa códigos `E01`…`E30`. Nombres y fotos solo con
  consentimiento escrito; fotos solo del vehículo, sin personas ni matrícula.
- El permiso verbal para conversar no autoriza a publicar nombre ni foto.
- Hay un audio fuera del proyecto: `/home/bri/Recording 9.flac` (11 MB), aún no
  copiado a `data/raw/entrevistas/`.

## 11. Riesgos y advertencias

- **Sitio cambiante:** si `__NEXT_DATA__` desaparece, usar
  `li[data-cy="adGrid"]` como plan B (ver `docs/metodologia.md`).
- **Precios señuelo:** ya se filtran en `src/clean.py`; revisar igualmente una
  muestra.
- **Monedas mixtas:** no promediar USD y CUP sin tasa documentada.
- **Contaminación de categoría:** hay bicicletas y patinetas dentro de
  `motos_electricas`; se conservan porque son del tema, pero hay que declararlo.
- **Duplicados:** deduplicar por `id` y por título+precio+municipio.
- **Cobertura baja:** `anio` (8,4 %), `marca` (31,3 %) y `cilindrada_cc`
  (13,6 %) limitan los cruces; declararlo en el informe.
- **Dependencias:** Matplotlib 3.11 rompió `boxplot(labels=...)`; no
  reintroducir ese argumento.
- **Fabricación de datos:** no inventar entrevistas, nombres ni respuestas. Si
  no se llega a 30, documentarlo y negociar con el profesor.
- **Datos personales:** no publicar nombres, teléfonos, direcciones ni fotos de
  personas. Sin consentimiento escrito no se usa nombre ni foto.
- **Muestra pequeña:** n = 30 no permite inferencia estadística; usar solo
  frecuencias y triangulación.
- **Clasificación automática:** los temas de los títulos se detectan por
  palabras clave; revisar falsos positivos (por ejemplo, “autonomía” en una
  moto de combustión) antes de citar porcentajes como concluyentes.

## 12. Referencias

- `README.md` — cómo reproducir el proyecto.
- `docs/PLAN_DE_TRABAJO.md` — por dónde empezar y plan de 2 semanas.
- `docs/PLAN_ANALISIS.md` — datos y análisis previstos.
- `docs/CRITERIOS_RELEVANCIA.md` — reglas del filtro.
- `docs/ENTREVISTAS.md` — diseño del estudio cualitativo.
- `docs/PROTOCOLO_TRABAJO_CAMPO.md` — plan para completar las 30 entrevistas.
- `docs/VACIADO_ENTREVISTAS.md` — guía para pasar notas al CSV.
- `docs/CONSENTIMIENTO_INFORMADO.md` — consentimiento para firmar.
- `docs/GUION_ENTREVISTA_CORTA.md` — guion corto imprimible.
- `docs/metodologia.md` — fuente, extracción, limpieza y ética.
- `docs/prompt-handoff-journal.md` — plantillas de cierre de sesión.
- `docs/STORYTELLING.md` — narrativa del proyecto, versión corta para exponer,
  estructura de 6 diapositivas y frases ancla.
- `reports/informe.md` — informe final redactado (9 841 anuncios + muestra de
  200 títulos + limitación cualitativa declarada).
- `reports/informe.pdf` — versión PDF para entrega (18 páginas), generada
  desde el HTML.
- `reports/storytelling_proyecto.pptx` — presentación de 8 diapositivas para
  exponer el storytelling.
- `src/generar_storytelling_pptx.py` — regenera la presentación desde cero.
- `entrega/informe.pdf` — copia idéntica del PDF canónico, junto con el DOCX y
  la nota para el profesor.
- `entrega/storytelling_proyecto.pptx` — copia idéntica de la presentación.
- `entrega/entrega_proyecto_mercado_vehiculos.zip` — paquete completo de
  entrega.
- `entrega/LEEME.md` — contenido de la entrega y comandos de reproducción.
- `reports/analisis_200_titulos.txt` — resultados de la muestra de 200 títulos.
- `reports/muestra_200_titulos.csv` — muestra auditable con títulos limpiados.
- `reports/analisis_temas.txt` — contraste con los 9 841 títulos.
- `data/README.md` — diccionario de datos.
