# Journal — Mercado de motos, bicicletas y patinetas en Cuba

Bitácora append-only. Cada sesión añade una entrada al final; no se edita lo
anterior. El estado resumido vive en `docs/HANDOFF.md`.

---

## 2026-11-04 20:31 — Creación del esqueleto y del sistema de handoff

**Objetivo:** crear el esqueleto completo del proyecto de análisis del mercado
de motos, bicicletas y patinetas en Cuba, con scraping de Revolico, y dejar un
sistema de handoff/journaling para continuar en nuevas sesiones.

**Hecho:**
- Estructura de carpetas: `src/`, `notebooks/`, `docs/`, `reports/figures/`,
  `data/raw/`, `data/processed/`.
- `src/config.py` con rutas, URLs, categorías, cabeceras y parámetros.
- `src/scraper.py` con descarga, parseo de `__NEXT_DATA__`, paginación,
  deduplicación, guardado de HTML crudo y CSV.
- `src/details.py` con muestreo estratificado y extracción de descripciones sin
  datos personales.
- `src/clean.py` con reglas de limpieza y variables derivadas (`anio`,
  `cilindrada_cc`, `condicion`, `tipo`, `marca`, `precio_usd`).
- Tres notebooks: `01_scraping.ipynb`, `02_limpieza.ipynb`, `03_eda.ipynb`.
- Documentación: `README.md`, `docs/metodologia.md`, `data/README.md`,
  `reports/informe.md`, `.gitignore`, `requirements.txt`.
- `docs/prompt-handoff-journal.md` con prompt, plantillas e instrucción
  persistente.
- `docs/HANDOFF.md` y esta entrada de journal.
- `AGENTS.md` con convenciones e instrucción de cierre de sesión.

**Decisiones:**
- Usar Revolico como fuente por ser el clasificado local relevante y permitir
  el acceso según `robots.txt`.
- Parsear el JSON de `__NEXT_DATA__` en lugar de selectores CSS: es más estable
  y no requiere Selenium.
- Excluir teléfonos, nombres e identificadores de usuario por privacidad.
- No convertir CUP a USD por defecto: se analizan por separado salvo que se
  documente una tasa.
- Buscar patinetas por texto (`q=patineta`) porque no tienen subcategoría propia.
- Ignorar `data/` y `reports/figures/` en Git, conservando los `.gitkeep`.

**Comandos ejecutados:**
```bash
python3 -m py_compile src/*.py                      # OK
python3 -m src.scraper --help                       # OK
python3 -m src.details --help                       # OK
python3 -m src.scraper --max-pages 1 --categorias bicicletas
# → 100 anuncios únicos, provincia y municipio resueltos
python3 -c "json.load(...)"                         # 3 notebooks válidos
```

**Errores / bloqueos:**
- `pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter` y `nbformat` no están
  instalados en este entorno.
- No hay `pip` ni `ensurepip`, por lo que no se pudo crear `.venv` ni instalar
  dependencias.
- `src/clean.py` y los notebooks 02 y 03 no se pudieron ejecutar; solo se validó
  su sintaxis/JSON.
- Los datos de prueba generados se borraron para dejar el esqueleto limpio.

**Pendiente:**
- [ ] Instalar dependencias en un entorno con `pip`.
- [ ] Cambiar el correo placeholder del `User-Agent` en `src/config.py`.
- [ ] Ejecutar la recolección completa y registrar fecha y volumen.
- [ ] Ejecutar `src.clean` y validar las variables derivadas.
- [ ] Completar el EDA y generar las figuras.
- [ ] Redactar el informe final.

**Siguiente paso:** instalar `requirements.txt` y ejecutar
`python -m src.scraper --max-pages 1 --categorias bicicletas` para confirmar el
flujo completo en un entorno con pandas.

**Archivos tocados:** `README.md`, `requirements.txt`, `.gitignore`,
`src/config.py`, `src/scraper.py`, `src/details.py`, `src/clean.py`,
`notebooks/*.ipynb`, `docs/metodologia.md`, `docs/prompt-handoff-journal.md`,
`docs/HANDOFF.md`, `docs/JOURNAL.md`, `data/README.md`, `reports/informe.md`,
`AGENTS.md`.

---

## 2026-11-04 20:35 — Plan de trabajo para empezar

**Objetivo:** dar al estudiante una ruta concreta para comenzar el proyecto sin
perderse en la teoría.

**Hecho:**
- `docs/PLAN_DE_TRABAJO.md` con meta de primera sesión, checklist, comandos,
  orden de 2 semanas y errores a evitar.
- Actualizado `docs/HANDOFF.md` con la nueva referencia.

**Decisiones:**
- Empezar por el ciclo mínimo “una página → CSV → tres observaciones” en lugar
  de por el informe o un modelo.
- Mantener el alcance en dataset + notebooks + informe.

**Pendiente:**
- [ ] Ejecutar la primera sesión según el plan.
- [ ] Instalar dependencias y validar `src.clean`.

**Siguiente paso:** abrir `docs/PLAN_DE_TRABAJO.md` y completar el Paso 0.

**Archivos tocados:** `docs/PLAN_DE_TRABAJO.md`, `docs/HANDOFF.md`,
`docs/JOURNAL.md`.

---

## 2026-11-04 22:23 — Espacio de trabajo dedicado

**Objetivo:** mover el proyecto a una carpeta de proyectos y dejar un punto de
entrada claro para empezar a trabajar.

**Hecho:**
- Creada `/home/bri/proyectos/`.
- Movido el proyecto a `/home/bri/proyectos/proyecto-mercado-vehiculos`.
- Actualizadas las rutas absolutas en `docs/PLAN_DE_TRABAJO.md` y
  `docs/HANDOFF.md`.
- Creado `EMPIEZA_AQUI.md` con los primeros pasos.
- Actualizado `README.md` con el nuevo archivo.

**Decisiones:**
- Usar `~/proyectos/` como carpeta de trabajo, fuera del escritorio y de
  descargas.
- Mantener el nombre del proyecto para no romper referencias.
- El código sigue funcionando porque `src/config.py` calcula rutas relativas a
  su propia ubicación.

**Comandos ejecutados:**
```bash
mkdir -p /home/bri/proyectos
mv /home/bri/proyecto-mercado-vehiculos /home/bri/proyectos/
```

**Pendiente:**
- [ ] Trasladar la sesión de OpenCode a la nueva carpeta.
- [ ] Ejecutar la primera sesión de trabajo.

**Siguiente paso:** abrir `EMPIEZA_AQUI.md` y continuar con el scraper.

**Archivos tocados:** `EMPIEZA_AQUI.md`, `README.md`, `docs/PLAN_DE_TRABAJO.md`,
`docs/HANDOFF.md`, `docs/JOURNAL.md`.

---

## 2026-11-04 22:45 — Recolección completa, filtro de relevancia y alcance

**Objetivo:** recolectar todo el dataset, identificar los anuncios del tema y
dejar copias separadas; excluir los triciclos por decisión del usuario.

**Hecho:**
- Recolección completa de Revolico: **13 446 anuncios únicos**.
  - `motos_electricas` 4 300, `motos_combustion` 4 299,
    `bicicletas` 4 204, `patinetas` 643.
- Creado y ajustado `src/relevancia.py`.
- Creado `src/analisis_basico.py` (sin pandas) y ejecutado sobre el dataset
  relacionado.
- Generados:
  - `data/processed/anuncios_relacionados.csv` — 11 618.
  - `data/processed/anuncios_relacionados_unicos.csv` — 10 801.
  - `data/processed/anuncios_revisar.csv` — 298.
  - `data/processed/anuncios_excluidos.csv` — 1 530.
  - `reports/relevancia_resumen.txt`.
  - `reports/analisis_relacionados.txt`.
- Excluidos por alcance: 1 296 triciclos y 23 cuatriciclos.

**Decisiones:**
- El mercado son solo motos, bicicletas y patinetas; triciclos y cuatriciclos
  quedan fuera aunque Revolico los mezcle en las mismas categorías.
- Aceptar plurales y variantes ortográficas en el filtro.
- Separar ruido fuerte (lavadora, planta, generador) de ruido contextual
  (gasolina, batería, motor): el segundo solo excluye si el título no nombra el
  vehículo.
- Interpretar `motor` como moto cuando hay cilindrada o marca.
- Conservar anuncios del tema aunque estén en la categoría equivocada y anotar
  la contaminación en `motivo`, en vez de descartarlos.

**Comandos ejecutados:**
```bash
python3 -m src.scraper --max-pages 43 > data/raw/scrape.log 2>&1
python3 -m src.relevancia
python3 -m src.analisis_basico \
  --input data/processed/anuncios_relacionados_unicos.csv \
  --out reports/analisis_relacionados.txt
```

**Errores y aprendizajes:**
- El primer filtro excluía motos reales porque `gasolina` y `batería` se
  trataban como ruido absoluto.
- `\bmoto\b` no capturaba `motos`: faltaban los plurales.
- Los 220 anuncios que empiezan por `Motor ...` eran motos, no repuestos.
- La regla "empieza por pieza" solo debe aplicarse si el título no nombra un
  vehículo.

**Pendiente:**
- [ ] Instalar `pandas` y `matplotlib` para ejecutar `src/clean.py` y los
  notebooks.
- [ ] Revisar a mano una muestra de `anuncios_revisar.csv`.
- [ ] Ejecutar el EDA y generar figuras.
- [ ] Redactar resultados en `reports/informe.md`.

**Siguiente paso:** resolver la instalación de dependencias y ejecutar
`python3 -m src.clean` sobre `data/processed/anuncios_relacionados_unicos.csv`.

**Archivos tocados:** `src/relevancia.py`, `src/analisis_basico.py`,
`docs/CRITERIOS_RELEVANCIA.md`, `docs/PLAN_ANALISIS.md`, `docs/metodologia.md`,
`docs/HANDOFF.md`, `docs/JOURNAL.md`, `README.md`.




---

## 2026-11-04 22:52 — Alcance confirmado y corrección del análisis

**Objetivo:** dejar el mercado limitado a motos, bicicletas y patinetas, sin
analizar ni reportar vehículos fuera de alcance, y corregir el análisis
descriptivo.

**Hecho:**
- El filtro descarta los vehículos fuera de alcance con el motivo genérico
  `fuera de alcance`; no se cuentan ni se analizan.
- `src/analisis_basico.py` lee por defecto
  `data/processed/anuncios_relacionados_unicos.csv`.
- Corregido error: la fila `(sin moneda)` sumaba todas las monedas.
- Añadida detección de precios `>= 1 000 000` (errores de captura).
- Documentación recortada para no detallar los vehículos descartados.

**Comandos ejecutados:**
```bash
python3 -m py_compile src/*.py
python3 -m src.relevancia
python3 -m src.analisis_basico
```

**Pendiente:**
- [ ] Mejorar extracción de marca, año y condición (cobertura baja).
- [ ] Instalar `pandas` y `matplotlib` para la limpieza y las figuras.

**Siguiente paso:** revisar `reports/analisis_basico.txt` y pasar a la limpieza.

**Archivos tocados:** `src/relevancia.py`, `src/analisis_basico.py`,
`docs/CRITERIOS_RELEVANCIA.md`, `docs/PLAN_ANALISIS.md`, `docs/metodologia.md`,
`docs/HANDOFF.md`, `README.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 11:17 — Limpieza, figuras y cierre del estado real

**Objetivo:** ejecutar la limpieza con pandas y generar las figuras del informe;
dejar `HANDOFF.md` y `JOURNAL.md` al día con todo el trabajo guardado.

**Hecho:**
- Se verificó el estado del repositorio y se detectó trabajo posterior a la
  última entrada del journal (23:00–02:24) que no estaba registrado:
  `src/extraccion.py`, `src/privacidad.py`, `src/enriquecer.py`,
  `src/figuras.py`, `src/transcribir.py`, `docs/ENTREVISTAS.md`,
  `docs/cuestionario_entrevistas.json` y `anuncios_enriquecidos.csv`.
- `src/clean.py` ejecutado sobre `data/processed/anuncios_relacionados_unicos.csv`:
  **9 841 anuncios limpios**; **963 descartados** por precio nulo o señuelo
  (<5 o ≥1 000 000).
  - Por categoría: combustión 3 349, bicicletas 3 146, eléctricas 2 807,
    patinetas 539.
  - Moneda: USD 9 589, CUP 251, MLC 1.
  - Precio USD: mediana 1 100, media 1 398,6, mínimo 5, máximo 111 111.
  - Generado `data/processed/anuncios_limpios.csv`.
- `src/figuras.py` ejecutado con `--input data/processed/anuncios_limpios.csv`:
  **10 figuras PNG** en `reports/figures/` (fig01–fig10).
- `src/figuras.py` corregido para Matplotlib 3.11: los tres `boxplot()` usaban
  `labels=`, argumento eliminado en esa versión; se sustituyó por
  `tick_labels=`.
- `python -m py_compile src/*.py` → OK.
- `docs/HANDOFF.md` reescrito con el estado actual y `docs/JOURNAL.md`
  actualizado con esta entrada.

**Decisiones:**
- Generar las figuras desde `anuncios_limpios.csv` y no desde
  `anuncios_enriquecidos.csv`, para que conteos y precios excluyan los señuelos.
- Mantener el journal como append-only: la entrada nueva documenta también el
  trabajo intermedio no registrado, sin editar entradas anteriores.
- No tocar los datos crudos de `data/raw/` ni los archivos de entrevistas.

**Comandos ejecutados:**
```bash
.venv/bin/python -m src.clean
.venv/bin/python -m src.figuras --input data/processed/anuncios_limpios.csv
.venv/bin/python -m py_compile src/*.py
```

**Errores y aprendizajes:**
- `src/figuras.py` falló dos veces con
  `TypeError: Axes.boxplot() got an unexpected keyword argument 'labels'`.
  Matplotlib 3.11 eliminó `labels`; la solución es `tick_labels`.
- No hay binario `jupyter` en `.venv`, así que los notebooks siguen sin
  ejecutarse.

**Pendiente:**
- [ ] Instalar Jupyter en `.venv` y ejecutar los notebooks 02 y 03.
- [ ] Completar las respuestas E01–E10 del cuestionario y generar
  `data/processed/entrevistas.csv` con el esquema de `docs/ENTREVISTAS.md`.
- [ ] Copiar `/home/bri/Recording 9.flac` a `data/raw/entrevistas/` si es una
  entrevista.
- [ ] Redactar `reports/informe.md` con las 10 figuras.
- [ ] Mejorar la cobertura de `anio`, `marca` y `cilindrada_cc`.
- [ ] Cambiar el correo placeholder del `User-Agent` en `src/config.py`.

**Siguiente paso:** instalar Jupyter
(`.venv/bin/pip install jupyter nbformat`) y ejecutar
`notebooks/02_limpieza.ipynb` y `notebooks/03_eda.ipynb`.

**Archivos tocados:** `src/figuras.py`, `data/processed/anuncios_limpios.csv`,
`reports/figures/fig01–fig10.png`, `docs/HANDOFF.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 11:34 — Instalación de Jupyter

**Objetivo:** dejar el entorno listo para ejecutar los notebooks 02 y 03.

**Hecho:**
- Instalado Jupyter dentro de `.venv`:
  `jupyterlab` 4.6.5, `notebook` 7.6.4, `ipykernel` 7.4.0, `nbformat` 5.11.1.
- Kernel `python3` registrado en
  `.venv/share/jupyter/kernels/python3`.
- Verificado con `jupyter --version` y `jupyter kernelspec list`.
- `docs/HANDOFF.md` actualizado: Jupyter ya no figura como bloqueo.

**Decisiones:**
- Instalar Jupyter en el `.venv` del proyecto (no global) para que use
  directamente pandas, numpy, matplotlib y seaborn ya instalados.

**Comandos ejecutados:**
```bash
.venv/bin/pip install jupyter nbformat
.venv/bin/jupyter --version
.venv/bin/jupyter kernelspec list
```

**Errores y aprendizajes:**
- La descarga de `notebook` se interrumpió una vez y pip la reanudó
  automáticamente; la instalación terminó bien.

**Pendiente:**
- [ ] Ejecutar `notebooks/02_limpieza.ipynb` y `notebooks/03_eda.ipynb`.
- [ ] Completar las entrevistas E01–E10.
- [ ] Redactar `reports/informe.md` con las 10 figuras.

**Siguiente paso:** ejecutar el notebook 02 con el kernel del `.venv` y revisar
sus salidas.

**Archivos tocados:** `.venv/` (dependencias), `docs/HANDOFF.md`,
`docs/JOURNAL.md`.

---

## 2026-11-05 11:48 — Ejecución del notebook 02 (limpieza)

**Objetivo:** ejecutar `notebooks/02_limpieza.ipynb` de principio a fin y dejar
sus salidas guardadas.

**Hecho:**
- Revisado el notebook: apuntaba a `data/processed/anuncios.csv` (13 446
  crudos), lo que habría reintroducido vehículos fuera de alcance.
- Se alineó su entrada con el pipeline actual:
  `data/processed/anuncios_relacionados_unicos.csv` (10 804 anuncios).
- Se guardó una copia de seguridad del dataset limpio anterior en
  `/tmp/opencode/anuncios_limpios.backup.csv`.
- Ejecutado con:
  `.venv/bin/jupyter nbconvert --to notebook --execute --inplace
  notebooks/02_limpieza.ipynb`.
- Resultado: **9 celdas de código ejecutadas, 0 errores**. Salidas y figura
  inline guardadas dentro del notebook.
- El notebook generó `data/processed/anuncios_limpios.csv` con **9 841 filas**,
  idéntico en ids al generado por `src.clean`.
- Números confirmados: 963 descartados por precio nulo/señuelo; combustión
  3 349, bicicletas 3 146, eléctricas 2 807, patinetas 539.

**Decisiones:**
- Cambiar la entrada del notebook a `anuncios_relacionados_unicos.csv` para
  mantener el alcance del proyecto (solo motos, bicicletas y patinetas).
- Conservar la copia de seguridad en `/tmp/opencode/` hasta validar el
  resultado.

**Comandos ejecutados:**
```bash
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 notebooks/02_limpieza.ipynb
```

**Errores y aprendizajes:**
- Ningún error de ejecución. Nbformat avisó de celdas sin `id` (aviso de
  compatibilidad futura, no bloqueante).
- Las estadísticas de precio del CSV crudo muestran un máximo absurdo
  (1.1e15) antes de limpiar; por eso la limpieza descarta precios fuera de
  rango.

**Pendiente:**
- [ ] Ejecutar `notebooks/03_eda.ipynb`.
- [ ] Completar las entrevistas E01–E10.
- [ ] Redactar `reports/informe.md` con las 10 figuras.

**Siguiente paso:** ejecutar `notebooks/03_eda.ipynb` y revisar sus resultados.

**Archivos tocados:** `notebooks/02_limpieza.ipynb`,
`data/processed/anuncios_limpios.csv`, `docs/HANDOFF.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 11:51 — Ejecución del notebook 03 (EDA)

**Objetivo:** ejecutar `notebooks/03_eda.ipynb` y producir las figuras y tablas
del análisis exploratorio.

**Hecho:**
- Revisado el notebook: lee `data/processed/anuncios_limpios.csv` (9 841) y
  escribe figuras en `reports/figures/`.
- Ejecutado con:
  `.venv/bin/jupyter nbconvert --to notebook --execute --inplace
  notebooks/03_eda.ipynb`.
- Resultado: **9 celdas de código ejecutadas, 0 errores**; salidas guardadas
  dentro del notebook.
- Generadas 6 figuras nuevas:
  `01_composicion.png`, `02_precios.png`, `03_precio_caracteristicas.png`,
  `04_marcas.png`, `05_provincias.png`, `06_tipo_moto.png`.
- `reports/figures/` pasa a tener **16 PNG** (10 de `src.figuras` + 6 del
  notebook).

**Hallazgos preliminares:**
- Medianas USD: combustión 2 200; eléctricas 1 490; patinetas 720;
  bicicletas 160.
- Eléctricas: menor mediana pero mayor dispersión que combustión
  (desv. típ. 3 115 vs 2 258).
- La Habana: 9 080 de 9 589 anuncios USD; mediana 1 000 USD.
- Medianas provinciales extremas: Pinar del Río 2 000 y Holguín 1 850 frente a
  Cienfuegos 210 y Santiago de Cuba 280 (pocos casos).
- Solo 829 anuncios USD tienen año y 1 343 cilindrada: cruces exploratorios.
- Patinetas: 535 anuncios USD, mediana 720, con ruido de carriolas, scooters
  infantiles y sets de protección.

**Decisiones:**
- Mantener ambos conjuntos de figuras: las de `src.figuras` (fig01–fig10) y las
  del notebook (01–06), porque tienen nombres distintos y se complementan.
- No eliminar outliers: el notebook los describe y el informe debe justificar
  cualquier recorte adicional.

**Comandos ejecutados:**
```bash
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 notebooks/03_eda.ipynb
```

**Errores y aprendizajes:**
- Ningún error de ejecución. Aviso no bloqueante de nbformat por celdas sin
  `id`.
- La categoría `patinetas` mezcla productos infantiles y accesorios; hay que
  declararlo como limitación.

**Pendiente:**
- [ ] Redactar `reports/informe.md` con resultados, discusión y figuras.
- [ ] Completar las entrevistas E01–E10 y triangular con los precios.
- [ ] Revisar la muestra de `anuncios_revisar.csv`.
- [ ] Exportar el informe a PDF.

**Siguiente paso:** redactar `reports/informe.md` usando las tablas del notebook
03 y las 16 figuras disponibles.

**Archivos tocados:** `notebooks/03_eda.ipynb`, `reports/figures/01–06*.png`,
`docs/HANDOFF.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 12:04 — Preparación del trabajo de campo (meta: 30 entrevistas)

**Objetivo:** resolver la brecha entre las 10 personas contactadas y la meta de
30 entrevistas, sin inventar datos y sin publicar información personal.

**Hecho:**
- Se acordó un **diseño mixto**: 10 entrevistas profundas (E01–E10) + 20
  entrevistas cortas (E11–E30) de 5–7 minutos.
- Creado `docs/PROTOCOLO_TRABAJO_CAMPO.md`: cuotas, criterios, lugares de
  captación, plan de 5 días, registro, control de calidad y plan B.
- Creado `docs/CONSENTIMIENTO_INFORMADO.md`: autorizaciones separadas para
  participar, audio, nombre en anexo privado, foto del vehículo y citas
  anónimas.
- Creado `docs/GUION_ENTREVISTA_CORTA.md`: guion imprimible con P56–P63,
  opciones, sondas y espacio para notas.
- Rehecho `data/processed/entrevistas.csv` con una plantilla de **53 columnas**
  (metadatos + encuesta corta + variables clave de la entrevista profunda).
  La fila E01 se migró desde el esquema anterior; copia de seguridad en
  `/tmp/opencode/entrevistas.backup.csv`.
- Creado `src/entrevistas.py`: frecuencias, medianas por moneda y triangulación
  con `anuncios_limpios.csv`. Probado con E01; genera
  `reports/entrevistas_resumen.txt`.
- Actualizado `docs/ENTREVISTAS.md` a la meta de 30 y a los nuevos materiales.
- Actualizado `AGENTS.md` con el comando `python -m src.entrevistas`.

**Decisiones:**
- No fabricar entrevistas, nombres ni respuestas. Si no se llega a 30, se
  documenta y se negocia con el profesor.
- El informe público usa códigos E01–E30; el nombre real solo va en un anexo
  privado con consentimiento escrito.
- Las fotos son solo del vehículo, sin personas ni matrícula, y solo con
  permiso.
- Las 20 cortas se hacen en 5 días (2 piloto + 18 en tres salidas).

**Comandos ejecutados:**
```bash
.venv/bin/python -m py_compile src/*.py
.venv/bin/python -m src.entrevistas
```

**Errores y aprendizajes:**
- El esquema anterior de `entrevistas.csv` solo tenía 5 columnas y no permitía
  cruzar precios, tipo ni canal. Se migró E01 sin perder sus cuatro datos.
- El resumen funciona con muy pocos datos, pero avisa de que n pequeño no
  permite inferencia.

**Pendiente:**
- [ ] Hacer las 20 entrevistas cortas (E11–E30).
- [ ] Pasar al CSV las 10 profundas y las 20 cortas.
- [ ] Firmar y archivar los consentimientos.
- [ ] Transcribir los audios disponibles.
- [ ] Redactar `reports/informe.md` con la triangulación.

**Siguiente paso:** imprimir el guion corto y el consentimiento, y hacer las 2
entrevistas piloto del día 1.

**Archivos tocados:** `docs/PROTOCOLO_TRABAJO_CAMPO.md`,
`docs/CONSENTIMIENTO_INFORMADO.md`, `docs/GUION_ENTREVISTA_CORTA.md`,
`docs/ENTREVISTAS.md`, `data/processed/entrevistas.csv`, `src/entrevistas.py`,
`reports/entrevistas_resumen.txt`, `AGENTS.md`, `docs/HANDOFF.md`,
`docs/JOURNAL.md`.

---

## 2026-11-05 12:13 — Espacio privado de entrevistas y guía de vaciado

**Objetivo:** dejar listo el lugar seguro para nombres, fotos, audios y
consentimientos, y facilitar el paso de las notas al CSV sin filtrar datos
personales.

**Hecho:**
- Creada la carpeta privada `data/raw/entrevistas/` (ignorada por Git) con:
  - `README.md`: reglas, nombres de archivos e índice privado.
  - `indice_privado.csv`: plantilla con código, nombre, contacto y
    autorizaciones.
  - `fotos/` y `transcripciones/`.
  - Permisos `700` en la carpeta y `600` en los archivos con datos.
- Copiado `/home/bri/Recording 9.flac` a
  `data/raw/entrevistas/SIN_ASIGNAR_2026-11-01.flac` (11 MB). El original no se
  movió.
- Creado `docs/VACIADO_ENTREVISTAS.md`: orden de llenado, valores permitidos,
  diccionario de columnas, errores típicos y verificación con el script.
- `src/entrevistas.py` ahora muestra el avance hacia la meta (30, faltantes y
  códigos pendientes) y avisa si un campo de texto libre parece contener un
  correo o un teléfono.
- Actualizados `AGENTS.md`, `data/README.md`, `docs/ENTREVISTAS.md`,
  `docs/PROTOCOLO_TRABAJO_CAMPO.md` y `docs/HANDOFF.md` para que la única
  excepción de datos personales sea la carpeta privada.

**Decisiones:**
- Los nombres y contactos no entran en `docs/`, `reports/` ni
  `data/processed/`; solo en `data/raw/entrevistas/indice_privado.csv`.
- La carpeta privada no se comparte ni se sube a Git.
- No se inventan entrevistas para llegar a 30.

**Comandos ejecutados:**
```bash
.venv/bin/python -m py_compile src/*.py
.venv/bin/python -m src.entrevistas
.venv/bin/python -m src.transcribir --modelo base --idioma es
```

**Errores y aprendizajes:**
- La transcripción no terminó: la descarga del modelo `base` de Whisper avanzó
  solo 2,7 MB en 6 minutos. Se canceló para no bloquear la sesión. Reintentar
  con mejor conexión o con `--modelo tiny`.
- La carpeta privada es una excepción deliberada a la regla de “sin datos
  personales”; queda fuera de Git y solo admite material con consentimiento
  escrito.

**Pendiente:**
- [ ] Hacer las 20 entrevistas cortas (E11–E30).
- [ ] Pasar al CSV las 10 profundas y las 20 cortas con
      `docs/VACIADO_ENTREVISTAS.md`.
- [ ] Transcribir el audio cuando la conexión lo permita.
- [ ] Redactar `reports/informe.md` con la triangulación.

**Siguiente paso:** imprimir `docs/GUION_ENTREVISTA_CORTA.md` y
`docs/CONSENTIMIENTO_INFORMADO.md`, y hacer las 2 entrevistas piloto del día 1.

**Archivos tocados:** `data/raw/entrevistas/README.md`,
`data/raw/entrevistas/indice_privado.csv`,
`data/raw/entrevistas/SIN_ASIGNAR_2026-11-01.flac`, `docs/VACIADO_ENTREVISTAS.md`,
`src/entrevistas.py`, `reports/entrevistas_resumen.txt`, `AGENTS.md`,
`data/README.md`, `docs/ENTREVISTAS.md`, `docs/PROTOCOLO_TRABAJO_CAMPO.md`,
`docs/HANDOFF.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 12:22 — Solo hay nombres y fotos de las 10 personas

**Objetivo:** responder a la restricción real del usuario: de las 10 personas
solo conserva nombres y fotos de los vehículos, sin respuestas registradas.

**Hecho:**
- Creado `docs/GUION_RECONTACTO.md` con:
  - el bloque mínimo de preguntas para recuperar E01–E10 en 5–7 minutos;
  - mensaje para WhatsApp/Telegram y guion de llamada;
  - reglas de consentimiento y qué hacer si la persona no responde;
  - cómo tratar las fotos ya tomadas y cómo quitarles el EXIF;
  - tres escenarios de tiempo (recuperación corta, profunda o 30 nuevas).
- Actualizados `docs/HANDOFF.md`, `docs/ENTREVISTAS.md`,
  `docs/PROTOCOLO_TRABAJO_CAMPO.md` y `AGENTS.md` para reflejar que las 10
  personas no tienen respuestas registradas y que los nombres/fotos no cuentan
  como entrevista.

**Decisiones:**
- Un nombre y una foto no equivalen a una entrevista: sin respuestas y sin
  consentimiento no se usan.
- Si solo se recupera el bloque corto, la fila se marca como `corta` y se anota
  que es un re-contacto; no se llama “profunda” sin registro de entrevista larga.
- Las fotos solo se usan con consentimiento escrito, sin personas ni matrícula.

**Comandos ejecutados:**
```bash
.venv/bin/python -c "import PIL; print(PIL.__version__)"
.venv/bin/python -m py_compile src/*.py
```

**Errores y aprendizajes:**
- Faltaba un documento para el caso “tengo el contacto y la foto, pero no las
  respuestas”. Ahora está cubierto.
- La meta de 30 no se resuelve con material ilustrativo: exige volver a hablar
  con las personas o hacer entrevistas nuevas.

**Pendiente:**
- [ ] Decidir si se re-contacta a las 10 o se hacen 30 nuevas.
- [ ] Recuperar el consentimiento firmado de cada persona que se use.
- [ ] Recuperar al menos el bloque corto de E01–E10.
- [ ] Hacer las 20 entrevistas cortas (E11–E30).
- [ ] Redactar `reports/informe.md` con la triangulación.

**Siguiente paso:** elegir el escenario y ejecutar
`docs/GUION_RECONTACTO.md` o el protocolo de 30 entrevistas nuevas.

**Archivos tocados:** `docs/GUION_RECONTACTO.md`, `docs/HANDOFF.md`,
`docs/ENTREVISTAS.md`, `docs/PROTOCOLO_TRABAJO_CAMPO.md`, `AGENTS.md`,
`docs/JOURNAL.md`.

---

## 2026-11-05 12:39 — Sin contacto ni consentimiento escrito: se reinicia el campo

**Objetivo:** decidir qué hacer con las 10 personas de las que solo hay nombres
y fotos, sin respuestas registradas ni consentimiento firmado.

**Hecho:**
- El usuario confirmó que **no tiene contacto** con las 10 personas y que **no
  tiene consentimiento firmado** de ninguna. Solo hubo permiso verbal para
  conversar y para tomar nombre y foto.
- Se decidió **no usar** a esas 10 personas: sin respuestas no hay datos y sin
  consentimiento escrito no se pueden publicar nombres ni fotos.
- E01 quedó marcada con `consentimiento = no` y una nota; el resto de sus datos
  se conserva solo para auditoría.
- `src/entrevistas.py` ahora **excluye del análisis** las filas cuyo
  `consentimiento` no sea `si`, muestra cuántas filas se excluyeron y avisa.
- El protocolo se reescribió para **30 entrevistas cortas nuevas** (E01–E30),
  6 por día durante 5 días, con cuotas por perfil.
- `docs/ENTREVISTAS.md` y `docs/VACIADO_ENTREVISTAS.md` se ajustaron a ese
  diseño.
- `docs/GUION_RECONTACTO.md` quedó marcado como **no aplicable** mientras no
  haya contacto.

**Decisiones:**
- El permiso verbal sirve para conversar, pero **no sustituye** el
  consentimiento escrito para publicar nombre o foto.
- Los nombres y fotos de las 10 personas no se usan; si no hay consentimiento,
  no se publican.
- La meta de 30 se cumple con 30 entrevistas cortas nuevas, no con material
  ilustrativo.
- Sin `consentimiento = si`, la fila no cuenta en el resumen ni en la
  triangulación.

**Comandos ejecutados:**
```bash
.venv/bin/python -m py_compile src/*.py
.venv/bin/python -m src.entrevistas
```

**Errores y aprendizajes:**
- Un nombre y una foto no son evidencia de una entrevista; sin respuestas no se
  puede analizar el mercado.
- El permiso verbal no alcanza para datos personales publicables. La regla
  escrita evita tener que decidir caso por caso.
- El script ahora protege el análisis de filas sin consentimiento.

**Pendiente:**
- [ ] Hacer las 30 entrevistas cortas nuevas (6 por día).
- [ ] Firmar el consentimiento antes de cada entrevista.
- [ ] Pasar las respuestas al CSV con `docs/VACIADO_ENTREVISTAS.md`.
- [ ] Redactar `reports/informe.md` con la triangulación.

**Siguiente paso:** imprimir el guion corto y el consentimiento, y hacer las 2
entrevistas piloto del día 1.

**Archivos tocados:** `data/processed/entrevistas.csv`, `src/entrevistas.py`,
`reports/entrevistas_resumen.txt`, `docs/PROTOCOLO_TRABAJO_CAMPO.md`,
`docs/ENTREVISTAS.md`, `docs/VACIADO_ENTREVISTAS.md`,
`docs/GUION_RECONTACTO.md`, `docs/HANDOFF.md`, `AGENTS.md`,
`docs/JOURNAL.md`.

---

## 2026-11-05 12:48 — Informe final redactado y exportado

**Objetivo:** cerrar la entrega del 6 de noviembre con lo que existe realmente:
9 841 anuncios limpios y 0 entrevistas válidas.

**Hecho:**
- Reescrito `reports/informe.md`: resumen, introducción, datos y método,
  resultados (composición, precios, eléctricas vs. combustión, marcas,
  geografía, condición/año/cilindrada), discusión, limitaciones,
  conclusiones, recomendaciones, referencias y anexos.
- Insertadas 10 figuras de `reports/figures/`.
- Declarada de forma explícita la ausencia de entrevistas válidas y por qué no
  se usaron los 10 contactos con nombre y foto.
- Exportado `reports/informe.pdf` (19 páginas, A4) desde `reports/informe.html`
  con LibreOffice. También se generó `reports/informe.docx` para editar.
- Creado `docs/NOTA_AL_PROFESOR.md` con el mensaje de entrega y tres
  alternativas (aceptar con limitación, ampliar plazo o ajustar la meta).

**Decisiones:**
- El informe público no incluye nombres, teléfonos ni fotos de personas.
- Las cifras del informe se calcularon sobre `anuncios_limpios.csv` (9 841),
  no sobre los 10 804 relacionados.
- Los precios se comparan solo en USD; CUP y MLC quedan fuera de los cruces.
- La limitación cualitativa va en el cuerpo del informe, no en letra pequeña.

**Comandos ejecutados:**
```bash
.venv/bin/pip install markdown
# generación de reports/informe.html
soffice --headless --convert-to pdf --outdir reports reports/informe.html
soffice --headless --convert-to 'docx:MS Word 2007 XML' --outdir reports reports/informe.html
pdfinfo reports/informe.pdf
pdftotext -f 1 -l 3 reports/informe.pdf -
```

**Errores y aprendizajes:**
- No hay pandoc ni wkhtmltopdf; LibreOffice sí convierte HTML a PDF y DOCX.
- La exportación directa a `docx` falla sin el filtro explícito
  `MS Word 2007 XML`.
- El texto justificado del PDF espacia mucho algunas líneas; es cosmético.

**Pendiente:**
- [ ] Escribir el nombre del autor en `reports/informe.md` (no hay tutor).
- [ ] Revisar el PDF antes de entregarlo.
- [ ] Decidir con el profesor si se amplía el plazo o se ajusta la meta.

**Siguiente paso:** completar los nombres, revisar `reports/informe.pdf` y
entregar junto con `docs/NOTA_AL_PROFESOR.md` si se considera necesario.

**Archivos tocados:** `reports/informe.md`, `reports/informe.html`,
`reports/informe.pdf`, `reports/informe.docx`,
`docs/NOTA_AL_PROFESOR.md`, `docs/HANDOFF.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 12:58 — Nombre de la autora en la portada

**Hecho:**
- Añadido `Brigitte Hernández Romero` como autora en `reports/informe.md`.
- Eliminado el campo “Tutor”: no hay tutor asignado, solo la asignatura.
- Actualizado `docs/NOTA_AL_PROFESOR.md` con el nombre.
- Regenerados `reports/informe.pdf` (19 páginas) y `reports/informe.docx`.

**Decisión:** no se inventa un tutor. La portada queda con autora, asignatura,
institución y fecha.

**Pendiente:** revisar el PDF y entregarlo. Si se quiere tilde en el apellido,
cambiar a “Hernández”.

---

## 2026-11-05 13:06 — Eliminado el Anexo C

**Objetivo:** quitar el anexo sobre datos personales a petición de la autora.

**Hecho:**
- Eliminada la sección “Anexo C. Nota sobre datos personales” de
  `reports/informe.md`.
- Regenerados `reports/informe.pdf` y `reports/informe.docx`.
- Verificado que el PDF no contiene el texto “Anexo C”.

**Decisión:** la ética del manejo de datos sigue explicada en la sección 2.5 y
en la sección 4; solo se quitó el anexo final.

**Pendiente:** revisar el PDF y entregarlo.

---

## 2026-11-05 13:30 — Análisis de títulos y kit para 1–2 entrevistas

**Objetivo:** llenar la sección cualitativa sin inventar datos, dado que la
autora solo puede hacer 1 o 2 entrevistas antes de la entrega.

**Hecho:**
- Creado `src/temas_anuncios.py`: clasifica los 9 841 títulos en 8 temas por
  palabras clave, genera `reports/analisis_temas.txt` y la figura
  `reports/figures/07_temas_anuncios.png`.
- Resultados: 46,0 % de los títulos menciona al menos un tema y 54,0 % ninguno.
  Especificaciones técnicas 22,1 %; estado/novedad 16,4 %; precio 6,8 %;
  uso 5,5 %; garantía/papeles 1,6 %.
- Reescrita la sección 4 de `reports/informe.md`: 4.1 lo que se intentó,
  4.2 análisis de contenido de los anuncios, 4.3 limitación.
- Creados `docs/CONSENTIMIENTO_CORTO.md` (una página),
  `docs/FICHA_ENTREVISTA_RAPIDA.md` y `docs/KIT_1_2_ENTREVISTAS.md`.
- Actualizado `docs/CONSENTIMIENTO_INFORMADO.md` con el nombre de la autora y
  sin “Profesor guía”.
- Regenerado `reports/informe.pdf` (23 páginas) y `reports/informe.docx`.

**Decisiones:**
- No se inventan entrevistas ni se usan los 10 contactos sin consentimiento.
- El análisis de títulos se presenta como análisis de contenido de la oferta,
  no como entrevistas.
- Las 1–2 entrevistas se presentarán como “estudio piloto exploratorio” y se
  declarará que no representan al mercado.

**Comandos ejecutados:**
```bash
.venv/bin/python -m src.temas_anuncios
.venv/bin/python -m py_compile src/temas_anuncios.py
soffice --headless --convert-to pdf --outdir reports reports/informe.html
soffice --headless --convert-to 'docx:MS Word 2007 XML' --outdir reports reports/informe.html
```

**Errores y aprendizajes:**
- El primer script invertía índice y columnas en la tabla por categoría; se
  corrigió.
- Los nombres de tema con coma se rompían al reemplazar separadores de miles;
  se añadió una función `miles()`.
- La clasificación automática puede tener falsos positivos; se declara en el
  informe.

**Pendiente:**
- [ ] Hacer 1 o 2 entrevistas con el kit y el consentimiento corto.
- [ ] Pasar los datos al CSV o entregarlos para integrarlos.
- [ ] Añadir “4.3 Estudio piloto (n = 1–2)” y regenerar el PDF.

**Siguiente paso:** imprimir 4 consentimientos cortos y 2 fichas, hacer las
entrevistas y traer los datos.

---

## 2026-11-05 13:38 — Plantilla de cita textual

**Hecho:**
- Creado `docs/PLANTILLA_CITA_TEXTUAL.md` con las reglas para copiar una cita
  exacta, la diferencia entre textual/paráfrasis/indirecta y un ejemplo
  ficticio marcado como tal.
- Ampliada la sección 6 de `docs/FICHA_ENTREVISTA_RAPIDA.md` con “pregunta que
  la provocó”, “textual o paráfrasis” y “contexto o gesto”.

**Decisión:** una cita solo va entre comillas si se anotó o grabó tal cual; si
se reconstruye de memoria, se marca como paráfrasis.

---

## 2026-11-05 22:07 — Opción B ejecutada e integrada al informe

**Objetivo:** ejecutar la Opción B (análisis de contenido de 200 títulos, sin
entrevistas) e integrarla en el informe y en el PDF de entrega.

**Hecho:**
- Ejecutado `src/analisis_200_titulos.py` sobre `anuncios_limpios.csv`:
  - muestra aleatoria de **200 títulos** (semilla 2026);
  - composición: 68 bicicletas, 65 motos de combustión, 58 eléctricas y
    9 patinetas;
  - **31 títulos (15,5 %)** mencionan al menos uno de los seis temas;
  - **169 (84,5 %)** no mencionan ninguno;
  - 8 ejemplos textuales y figura `08_temas_200_titulos.png`.
- Reescrita la sección 4 de `reports/informe.md`:
  - 4.1 lo que se intentó;
  - 4.2 muestra de 200 títulos con tabla de frecuencias, tabla por categoría,
    figura 08 y 8 ejemplos;
  - 4.3 contraste con los 9 841 títulos y taxonomía de ocho temas (figura 07);
  - 4.4 limitación del componente cualitativo.
- Actualizados resumen, discusión (5.2), limitaciones (6.5), conclusiones,
  recomendaciones (8.6), referencias y anexos.
- Creado `src/generar_informe.py`: convierte Markdown a HTML con la hoja de
  estilo del informe, ajusta el tamaño de las imágenes y permite regenerar el
  PDF de forma reproducible.
- Regenerados `reports/informe.html`, `reports/informe.pdf` (**18 páginas**) y
  `reports/informe.docx`.

**Decisiones:**
- La muestra de 200 títulos es el análisis principal de la Opción B; el
  análisis de los 9 841 títulos queda como contraste de robustez.
- No se inventaron entrevistas ni se usaron los 10 contactos sin
  consentimiento. El informe sigue declarando **0 entrevistas válidas**.
- El análisis se presenta como discurso de la oferta, no como entrevistas.

**Comandos ejecutados:**
```bash
.venv/bin/python -m src.analisis_200_titulos
.venv/bin/python -m src.generar_informe
soffice --headless --convert-to pdf --outdir reports reports/informe.html
soffice --headless --convert-to 'docx:MS Word 2007 XML' --outdir reports reports/informe.html
```

**Errores y aprendizajes:**
- LibreOffice ignoraba `max-width` y `width="100%"` en el CSS: las figuras
  salían recortadas. Se corrigió añadiendo `width` y `height` explícitos en
  píxeles, calculados a partir del tamaño real de cada PNG.
- Con `width="100%"` la figura se veía completa, pero LibreOffice reservaba su
  altura natural y empujaba el texto, dejando páginas casi vacías. El tamaño
  explícito resolvió el flujo.
- La tabla de 200 títulos se partía y dejaba una página en blanco. Se añadió un
  salto de página antes de 4.2 y se movió el párrafo de interpretación antes de
  la figura 07.
- `attr_list` de Python-Markdown permite aplicar el salto de página al título
  sin incrustar HTML en el cuerpo del informe.

**Pendiente:**
- [ ] Revisar el PDF final y entregarlo.
- [ ] Actualizar `docs/NOTA_AL_PROFESOR.md` con el enfoque de 200 títulos.
- [ ] Si el profesor exige entrevistas, completar las 30 en una segunda fase.

**Siguiente paso:** revisar `reports/informe.pdf` (18 páginas) y entregarlo con
`docs/NOTA_AL_PROFESOR.md`.

**Archivos tocados:** `src/analisis_200_titulos.py` (ejecutado),
`src/generar_informe.py`, `reports/informe.md`, `reports/informe.html`,
`reports/informe.pdf`, `reports/informe.docx`, `reports/analisis_200_titulos.txt`,
`reports/muestra_200_titulos.csv`,
`reports/figures/08_temas_200_titulos.png`, `docs/HANDOFF.md`,
`docs/JOURNAL.md`.

---

## 2026-11-05 22:21 — Ajuste final de maquetación del PDF

**Hecho:**
- Retirado el salto de página forzado antes de 4.2: dejaba la página 10 casi
  vacía con un solo elemento de la lista.
- Aclarado que la tabla de los seis temas por categoría corresponde al total
  del dataset (n = 9 841), no a la muestra de 200; se añadieron los tamaños por
  categoría en el texto.
- Regenerados `reports/informe.html`, `reports/informe.pdf` y
  `reports/informe.docx`.
- Anexo de reproducibilidad resumido a una referencia a `README.md` y
  `docs/HANDOFF.md`; se añadió un salto de página antes de los anexos para que
  las figuras finales no dejaran páginas casi vacías.
- PDF final: **18 páginas**; se revisaron visualmente las páginas 2–4, 9–18.
- `docs/HANDOFF.md` y `docs/NOTA_AL_PROFESOR.md` actualizados al estado final
  (18 figuras, 18 páginas, Opción B declarada).

**Decisión:** no se conserva el salto artificial antes de 4.2; con las imágenes
ya dimensionadas en píxeles, el flujo natural no parte las tablas ni recorta
figuras. Los anexos empiezan en página nueva para agrupar las cuatro figuras
finales.

**Pendiente:**
- [ ] Entregar `reports/informe.pdf` (18 páginas) con
  `docs/NOTA_AL_PROFESOR.md`.
- [ ] Completar las 30 entrevistas en una segunda fase, si se requiere.

**Siguiente paso:** revisar una última vez el PDF y entregarlo.

**Archivos tocados:** `reports/informe.md`, `reports/informe.html`,
`reports/informe.pdf`, `reports/informe.docx`, `docs/HANDOFF.md`,
`docs/NOTA_AL_PROFESOR.md`, `entrega/informe.pdf`, `entrega/informe.docx`,
`entrega/NOTA_AL_PROFESOR.md`, `entrega/LEEME.md`, `docs/JOURNAL.md`.

---

## 2026-11-05 22:53 — PDF final integrado al proyecto y carpeta de entrega

**Objetivo:** dejar el PDF final integrado en la estructura del proyecto y
accesible desde la documentación.

**Hecho:**
- Creada la carpeta `entrega/` con `informe.pdf`, `informe.docx`,
  `NOTA_AL_PROFESOR.md` y `LEEME.md`.
- Verificado que `entrega/informe.pdf` y `reports/informe.pdf` tienen el mismo
  SHA-256; la copia es idéntica al PDF canónico.
- Añadida la sección **“Informe final”** al `README.md`, con enlaces al PDF, al
  DOCX y a la copia de entrega.
- Actualizado `docs/HANDOFF.md`: fecha, estado, estructura, cambios recientes,
  próximo paso y referencias.
- Confirmado el PDF final: **18 páginas**, A4, 18 figuras y **0 entrevistas
  válidas**.

**Decisiones:**
- `reports/informe.pdf` sigue siendo la fuente canónica; `entrega/` contiene
  las copias listas para entregar.
- No se duplican los archivos fuente en `entrega/`; `entrega/LEEME.md` indica
  dónde están `reports/`, `docs/` y `src/`.

**Comandos ejecutados:**
```bash
mkdir -p entrega
cp reports/informe.pdf entrega/informe.pdf
cp reports/informe.docx entrega/informe.docx
cp docs/NOTA_AL_PROFESOR.md entrega/NOTA_AL_PROFESOR.md
sha256sum reports/informe.pdf entrega/informe.pdf
pdfinfo entrega/informe.pdf | grep Pages
```

**Errores:** ninguno.

**Pendiente:**
- [ ] Ajustar `entrega/NOTA_AL_PROFESOR.md` con el nombre del profesor.
- [ ] Entregar `entrega/informe.pdf` (18 páginas).
- [ ] Completar las 30 entrevistas en una segunda fase, si se requiere.

**Siguiente paso:** revisar la nota, personalizarla y entregar el PDF.

**Archivos tocados:** `README.md`, `docs/HANDOFF.md`, `docs/JOURNAL.md`,
`entrega/informe.pdf`, `entrega/informe.docx`,
`entrega/NOTA_AL_PROFESOR.md`, `entrega/LEEME.md`.

---

## 2026-11-06 00:06 — Storytelling sin entrevistas y presentación de 8 diapositivas

**Objetivo:** crear el storytelling del proyecto y una presentación PowerPoint
que no mencionara entrevistas, y dejar ambos archivos listos para guardar en el
PC junto con el informe final.

**Hecho:**
- Reescrito `docs/STORYTELLING.md` con el arco problema → apuesta → hallazgos →
  método → límites → cierre. Verificado con `grep` que no contiene
  “entrevista” ni “cualitativ”.
- Creado `src/generar_storytelling_pptx.py`: genera una presentación de **8
  diapositivas**, 16:9, con paleta azul/naranja, gráficos nativos y notas del
  orador.
- Generado `reports/storytelling_proyecto.pptx` y renderizado a PDF/PNG con
  LibreOffice para revisión visual de las 8 diapositivas.
- Corregidos dos problemas de maquetación: etiquetas de barras partidas en dos
  líneas (diapositiva 6) y exceso de proximidad entre etiquetas y texto
  (diapositiva 5). Regenerado y revisado de nuevo.
- Copiado el PPTX a `entrega/storytelling_proyecto.pptx`; verificado que el
  SHA-256 coincide con el de `reports/storytelling_proyecto.pptx`.
- Actualizado `entrega/LEEME.md` con la presentación, el ZIP y los comandos de
  regeneración.
- Creado `entrega/entrega_proyecto_mercado_vehiculos.zip` con el PDF, el DOCX,
  el PPTX, la nota y el LEEME dentro de una carpeta raíz
  `Proyecto-Mercado-Vehiculos/`.
- Copiada la carpeta de entrega a `~/Desktop/Proyecto-Mercado-Vehiculos/`.
- Actualizado `docs/HANDOFF.md` con el PPTX, el generador, el ZIP y la copia del
  Escritorio.

**Decisiones:**
- La presentación y el storytelling **no mencionan entrevistas** ni insinúan que
  se realizaron, por pedido del usuario. El informe conserva la declaración
  explícita de 0 entrevistas válidas.
- `reports/storytelling_proyecto.pptx` es la fuente canónica; `entrega/` y el
  Escritorio tienen copias idénticas.
- El ZIP se generó con `zipfile` de Python porque el comando `zip` no está
  instalado en el sistema.

**Comandos ejecutados:**
```bash
.venv/bin/pip install --only-binary :all: python-pptx
.venv/bin/python -m src.generar_storytelling_pptx
soffice --headless --convert-to pdf --outdir /tmp/opencode reports/storytelling_proyecto.pptx
pdftoppm -png -r 70 /tmp/opencode/storytelling_proyecto.pdf /tmp/opencode/ppt
cp reports/storytelling_proyecto.pptx entrega/storytelling_proyecto.pptx
python - <<'PY'  # creación del ZIP con zipfile
cp -r entrega /home/bri/Desktop/Proyecto-Mercado-Vehiculos
sha256sum reports/storytelling_proyecto.pptx entrega/storytelling_proyecto.pptx
```

**Errores:**
- `zip` no está instalado (`command not found`); se reemplazó por `zipfile`.
- La descarga de `lxml` se interrumpió varias veces; se reanudó con
  `--resume-retries` y terminó bien.
- Las etiquetas de las barras se partían en dos líneas; se corrigió el helper
  `barra_apilada` para usar medias columnas.

**Pendiente:**
- [ ] Ajustar `entrega/NOTA_AL_PROFESOR.md` con el nombre del profesor.
- [ ] Revisar una última vez el PDF y el PPTX antes de entregar.
- [ ] Completar las 30 entrevistas en una segunda fase, si se requiere.

**Siguiente paso:** abrir `~/Desktop/Proyecto-Mercado-Vehiculos/`, personalizar
la nota y entregar el PDF y el PPTX.

**Archivos tocados:** `docs/STORYTELLING.md`,
`src/generar_storytelling_pptx.py`, `reports/storytelling_proyecto.pptx`,
`entrega/storytelling_proyecto.pptx`, `entrega/LEEME.md`,
`entrega/entrega_proyecto_mercado_vehiculos.zip`, `docs/HANDOFF.md`,
`docs/JOURNAL.md`.
