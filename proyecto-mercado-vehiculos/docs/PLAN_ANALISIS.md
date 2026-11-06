# Plan de análisis

> Documento de trabajo. Define qué datos necesitamos, qué preguntas responden y
> qué análisis produce el informe. Se actualiza a medida que avanza el proyecto.

---

## 1. Datos que necesitamos

### Nivel listado (obligatorio)

Ya lo extrae `src/scraper.py`:

| Variable | Para qué sirve |
|---|---|
| `id` | Identificar y deduplicar anuncios |
| `categoria` | Comparar motos, bicicletas y patinetas |
| `titulo` | Extraer marca, año, cilindrada, condición y detectar ruido |
| `precio` | Variable central del análisis |
| `moneda` | Separar USD y CUP; nunca mezclarlas sin tasa |
| `provincia`, `municipio` | Análisis geográfico |
| `fecha_publicacion` | Ventana temporal y antigüedad del anuncio |
| `vistas` | Señal de interés o exposición |
| `n_imagenes` | Calidad/esfuerzo del anuncio |
| `destacado` | Anuncios promocionados (posible sesgo) |
| `url` | Trazabilidad y verificación |
| `fecha_captura` | Reproducibilidad |

### Nivel detalle (opcional)

`src/details.py` puede añadir, para una submuestra de 300–500 anuncios:

- `descripcion`: texto para análisis de palabras o NLP básico.
- `fecha_actualizacion`: fecha absoluta.
- `vendido`: si el anuncio fue marcado como vendido.
- `estado`: estado del anuncio.

No es obligatorio para el alcance actual. Si se usa, debe documentarse el
muestreo y no incluir datos personales.

### Datos deliberadamente excluidos

- Teléfonos, nombres de vendedores e identificadores de usuario.
- Imágenes.
- Datos de contacto.
- Anuncios de vehículos fuera del alcance (no motos, bicicletas ni patinetas).

---

## 2. Preguntas y análisis

| Pregunta | Variables | Análisis | Figura |
|---|---|---|---|
| ¿Cómo se compone la oferta? | `categoria`, `provincia`, `moneda`, `marca` | Conteos y porcentajes | Barras |
| ¿Cómo se distribuyen los precios? | `precio`, `moneda`, `categoria` | Histograma, boxplot, mediana, IQR | Histograma y boxplot |
| ¿Qué marcas dominan? | `marca`, `precio` | Top 10 por anuncios; precio mediano por marca | Barras |
| ¿Cómo influye el año? | `anio`, `precio` | Dispersión + tendencia; mediana por década | Scatter |
| ¿Cómo influye la cilindrada? | `cilindrada_cc`, `precio` | Dispersión solo motos | Scatter |
| ¿Nueva vs. usada? | `condicion`, `precio` | Boxplot y medianas | Boxplot |
| ¿Eléctrica vs. combustión? | `tipo`, `precio` | Boxplot y dispersión | Boxplot |
| ¿Hay diferencias geográficas? | `provincia`, `precio` | Mediana por provincia con n ≥ 10 | Barras |
| ¿Cuánto ruido hay? | `titulo`, `precio` | Precios < 5, duplicados, contaminación | Tabla |
| ¿Cómo cambia en el tiempo? | `fecha_publicacion` | Anuncios por día/semana | Línea |

### Umbrales

- No calcular medianas por grupo con **menos de 10 anuncios**.
- No comparar precios entre monedas sin tasa documentada.
- Reportar siempre `n` junto a cada estadístico.

---

## 3. Orden de ejecución

1. **Recolectar** todas las páginas de las cuatro categorías.
2. **Auditar** el CSV: nulos, duplicados, precios señuelo, monedas.
3. **Limpiar** con `src/clean.py`.
4. **Analizar** con `src/analisis_basico.py` (sin pandas) o con los notebooks.
5. **Visualizar** y guardar figuras en `reports/figures/`.
6. **Redactar** resultados y discusión en `reports/informe.md`.

---

## 4. Entregables

- `data/processed/anuncios.csv`: dataset crudo tabular.
- `data/processed/anuncios_limpios.csv`: dataset limpio.
- `reports/analisis_basico.txt`: resumen descriptivo automático.
- `reports/figures/*.png`: figuras del informe.
- `notebooks/03_eda.ipynb`: análisis reproducible.
- `reports/informe.md`: informe final.

---

## 5. Limitaciones que el análisis debe declarar

- Son **precios pedidos**, no precios de transacción.
- La muestra es **no probabilística**: solo quienes publican en Revolico.
- La primera página está ordenada por fecha y concentra La Habana; el dataset
  completo reduce, pero no elimina, ese sesgo.
- Conviven **USD y CUP**.
- Hay **precios señuelo** y **contaminación de categoría**.
- Hay **duplicados** por republicación.
- La ventana de captura es corta.
- No se observa si el anuncio se vendió ni a qué precio.

---

## 6. Criterio de “análisis suficiente” para primer año

- [ ] Dataset con al menos 500 anuncios limpios.
- [ ] Al menos 3 categorías con n ≥ 30.
- [ ] Tabla de composición de la muestra.
- [ ] Distribución de precios por categoría y moneda.
- [ ] Top 10 de marcas.
- [ ] Precio vs. al menos dos variables (año, condición, tipo o provincia).
- [ ] 5–6 figuras con título, ejes y fuente.
- [ ] Limitaciones declaradas.
