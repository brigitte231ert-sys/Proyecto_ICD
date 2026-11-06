# Mercado de motos, bicicletas y patinetas en Cuba

Proyecto de análisis de datos basado en anuncios clasificados de
[Revolico](https://www.revolico.com). El objetivo es describir el mercado
(precios pedidos, oferta por marca, distribución geográfica y diferencias entre
tipos de vehículo) usando un pipeline reproducible de **extracción → limpieza →
análisis → informe**.

> **Autor:** estudiante de primer año de Ciencia de Datos, Universidad de La Habana
> **Fuente:** Revolico (anuncios públicos)
> **Ventana de captura:** ver `fecha_captura` en `data/processed/anuncios.csv`

---

## Informe final

- [Informe en PDF](reports/informe.pdf) — versión de entrega, 18 páginas, A4.
- [Informe en DOCX](reports/informe.docx) — versión editable.
- [Copia para entregar](entrega/informe.pdf) — misma versión, dentro de
  `entrega/`, junto con la nota para el profesor.

El informe incluye el análisis de contenido de una muestra aleatoria de
**200 títulos** y su contraste con los **9 841 anuncios** del dataset. El
componente de entrevistas se declara explícitamente como no completado
(**0 entrevistas válidas**).

## Presentación de storytelling

- [PowerPoint de 8 diapositivas](reports/storytelling_proyecto.pptx) — versión
  para exponer, con las cifras y gráficos del proyecto.
- [Copia para entregar](entrega/storytelling_proyecto.pptx) — misma
  presentación, dentro de `entrega/`.
- [Guion narrativo](docs/STORYTELLING.md) — texto completo y versión corta.
- [Generador](src/generar_storytelling_pptx.py) — regenera el PPTX con
  `.venv/bin/python -m src.generar_storytelling_pptx`.

La presentación no menciona entrevistas: cuenta el problema, la base de 9 841
anuncios, los hallazgos y el análisis de 200 títulos. El informe conserva la
limitación declarada.

---

## 1. Pregunta de investigación

**General:** ¿cómo se comporta el mercado de motos, bicicletas y patinetas en
Cuba según los anuncios clasificados?

> **Alcance:** solo motos, bicicletas y patinetas. Cualquier otro vehículo que
> Revolico mezcle en esas categorías se descarta. Ver
> `docs/CRITERIOS_RELEVANCIA.md`.

**Específicas:**

1. ¿Cómo se distribuyen los precios pedidos por categoría y por marca?
2. ¿Qué relación tienen el año, la cilindrada y la condición con el precio?
3. ¿Qué marcas y tipos (eléctrico vs. combustión) dominan la oferta?
4. ¿Existen diferencias de precios entre provincias?
5. ¿Qué tan disperso es el mercado y qué señales de “ruido” hay en los anuncios?

**Hipótesis de trabajo (a contrastar, no a confirmar):**

- Las motos eléctricas tienen una dispersión de precio mayor que las de combustión.
- El precio cae con la antigüedad del vehículo, pero el efecto es menor en bicicletas.
- La oferta se concentra en La Habana.

---

## 2. Estructura del repositorio

```
proyecto-mercado-vehiculos/
├── AGENTS.md                    # instrucciones para OpenCode
├── EMPIEZA_AQUI.md              # primeros pasos
├── entrega/                     # copias finales para entregar
│   ├── informe.pdf
│   ├── informe.docx
│   ├── storytelling_proyecto.pptx
│   ├── NOTA_AL_PROFESOR.md
│   ├── LEEME.md
│   └── entrega_proyecto_mercado_vehiculos.zip
├── data/
│   ├── raw/                     # HTML crudo por página (no versionado)
│   ├── processed/               # CSV generados (no versionado)
│   └── README.md                # diccionario de datos
├── docs/
│   ├── metodologia.md           # fuente, método, reglas de limpieza, ética
│   ├── prompt-handoff-journal.md  # prompt y plantillas de cierre de sesión
│   ├── HANDOFF.md               # estado actual del proyecto
│   └── JOURNAL.md               # bitácora append-only
├── notebooks/
│   ├── 01_scraping.ipynb        # recolección paso a paso
│   ├── 02_limpieza.ipynb        # limpieza y variables derivadas
│   └── 03_eda.ipynb             # análisis exploratorio y figuras
├── reports/
│   ├── figures/                 # gráficos exportados
│   ├── informe.md               # texto fuente del informe
│   ├── informe.html             # HTML intermedio
│   ├── informe.pdf              # informe final (18 páginas)
│   ├── informe.docx             # versión editable
│   └── storytelling_proyecto.pptx # presentación de 8 diapositivas
├── src/
│   ├── config.py                # rutas, URLs, categorías, cabeceras
│   ├── scraper.py               # recolector de anuncios (listado)
│   ├── details.py               # descripciones de una submuestra (opcional)
│   └── clean.py                 # limpieza y enriquecimiento con pandas
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 3. Instalación

Requiere **Python 3.10+** (probado con 3.13).

```bash
cd proyecto-mercado-vehiculos

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

Si solo quieres ejecutar el scraper, basta con `pip install requests`.

> **Si `python3 -m venv` falla** con “ensurepip is not available” en Linux,
> instala el paquete del sistema (`sudo apt install python3-venv`) o usa
> `python3 -m pip install --user -r requirements.txt`.

---

## 4. Cómo reproducir en 5 pasos

Todos los comandos se ejecutan **desde la raíz del proyecto**.

### Paso 1 — Prueba el scraper con una sola página

```bash
python -m src.scraper --max-pages 1 --categorias bicicletas
```

Salida esperada: `data/processed/anuncios.csv` con ~100 filas y el HTML crudo en
`data/raw/bicicletas_p001.html`.

### Paso 2 — Recolecta el dataset completo

```bash
python -m src.scraper --max-pages 43
```

Esto recorre todas las categorías (motos de combustión, motos eléctricas,
bicicletas y patinetas) con una pausa de 2–4 s entre peticiones. Puede tardar
20–40 minutos. El CSV se reescribe de forma incremental tras cada categoría, así
que una interrupción no pierde todo el trabajo.

Opciones útiles:

```bash
python -m src.scraper --help
python -m src.scraper --max-pages 10 --categorias bicicletas patinetas
python -m src.scraper --max-pages 1 --sin-raw     # no guarda HTML
```

### Paso 3 — (Opcional) Descarga descripciones de una submuestra

```bash
python -m src.details --n 300
```

Genera `data/processed/descripciones.csv` con el texto completo de 300 anuncios
elegidos al azar y estratificados por categoría.

### Paso 4 — Limpia y enriquece

```bash
python -m src.clean
```

Genera `data/processed/anuncios_limpios.csv` con variables derivadas
(`anio`, `cilindrada_cc`, `condicion`, `tipo`, `marca`, `precio_usd`).

Si decides convertir CUP a USD (opcional y documentado):

```bash
python -m src.clean --tasa-cup 320
```

### Paso 5 — Abre los notebooks

```bash
jupyter lab        # o: jupyter notebook
```

Orden recomendado: `01_scraping.ipynb` → `02_limpieza.ipynb` → `03_eda.ipynb`.

---

## 5. Notebooks

| Notebook | Qué hace |
|---|---|
| `01_scraping.ipynb` | Explica la fuente, inspecciona el HTML crudo y ejecuta el scraper. |
| `02_limpieza.ipynb` | Aplica `src.clean`, revisa nulos, duplicados y outliers; exporta el dataset limpio. |
| `03_eda.ipynb` | Análisis univariado y bivariado, figuras guardadas en `reports/figures/`. |

Cada notebook incluye una celda inicial que añade la raíz del proyecto a
`sys.path`, de modo que `from src... import ...` funciona sin instalar nada.

---

## 6. Metodología (resumen)

- **Fuente:** búsquedas públicas de Revolico. `robots.txt` permite el acceso
  salvo checkout, cuenta, autenticación y favoritos.
- **Extracción:** el sitio es *server-side* e incrusta un JSON en
  `<script id="__NEXT_DATA__">`. Se parsea ese JSON (`requests` + `json`), sin
  Selenium ni selectores CSS frágiles.
- **Paginación:** `&cu=1&page=N`, 100 anuncios por página.
- **Ética:** `User-Agent` identificable, pausa de 2–4 s, sin peticiones en
  paralelo, sin datos personales, sin republicar imágenes.
- **Datos sensibles:** se descartan `phoneInfo`, `name` y `userId`.

Detalle completo en [`docs/metodologia.md`](docs/metodologia.md).

---

## 7. Limitaciones que debes declarar en el informe

1. Son **precios pedidos**, no precios de transacción.
2. La muestra es **no probabilística**: solo anuncia quien usa Revolico.
3. Hay **precios señuelo** (p. ej. `1 USD`) y anuncios con el precio en el texto.
4. Conviven **USD y CUP**; promediar sin convertir es un error.
5. Hay **contaminación de categoría** (repuestos, electrodomésticos, gasolina).
6. Existen **duplicados** por republicación del mismo producto.
7. La ventana de captura es corta y el sitio cambia con el tiempo.

---

## 8. Ética y uso responsable

- Revisa las condiciones de uso de Revolico antes de recolectar.
- Identifícate en el `User-Agent` y deja un contacto real.
- No reduzcas la pausa por debajo de 2 s ni paralelices peticiones.
- No publiques teléfonos, nombres, identificadores ni imágenes de terceros.
- Cita la fuente y la fecha de captura en cualquier publicación derivada.
- Usa los datos solo con fines académicos.

---

## 9. Próximos pasos

- [ ] Ejecutar la recolección completa y registrar fecha y número de anuncios.
- [ ] Revisar manualmente 30–50 títulos para validar reglas de limpieza.
- [ ] Ampliar el diccionario de marcas en `src/clean.py`.
- [ ] Cerrar las preguntas de investigación con resultados del EDA.
- [ ] Redactar el informe en `reports/informe.md` y exportar a PDF.
- [ ] (Opcional) Añadir un modelo de precio o un dashboard.
