# Metodología

Documento de referencia para reproducir y defender el proyecto. Si algo cambia
en el sitio o en las reglas de limpieza, actualízalo aquí primero.

---

## 1. Fuente de datos

| Elemento | Valor |
|---|---|
| Sitio | Revolico (`https://www.revolico.com`) |
| Tipo | Anuncios clasificados públicos |
| Acceso | HTML renderizado en servidor |
| `robots.txt` | Permite `/`; bloquea `/checkout/`, `/cdn-cgi/`, `/account`, `/auth`, `/favorites/` |
| Fecha de verificación | 2026-11-04 |

### Categorías utilizadas

| Categoría del proyecto | Parámetro de búsqueda | Nota |
|---|---|---|
| `motos_combustion` | `category=vehiculos&subcategory=vehiculos-motos-de-combustion` | Categoría limpia |
| `motos_electricas` | `category=vehiculos&subcategory=vehiculos-motos-electricas-y-triciclos` | La subcategoría incluye otros vehículos; se descartan en el filtro |
| `bicicletas` | `category=vehiculos&subcategory=vehiculos-bicicletas` | ~43 páginas de 100 |
| `patinetas` | `q=patineta` | Sin subcategoría propia; requiere filtrado |

Combinaciones de búsqueda probadas para patinetas:

- `?q=patineta` → ~800 anuncios estimados (8 páginas).
- `?q=patineta electrica` → ~600 anuncios.
- `?category=vehiculos&subcategory=vehiculos-otros-vehiculos&q=patineta` → 85 anuncios.

Se usa `q=patineta` para maximizar cobertura y se filtra por palabras clave
durante la limpieza.

---

## 2. Método de extracción

### Por qué no Selenium

El HTML llega completo desde el servidor. Cada página incluye un bloque:

```html
<script id="__NEXT_DATA__" type="application/json">{ ... }</script>
```

Dentro está el estado de Apollo:

```
data["props"]["pageProps"]["__APOLLO_STATE__"]
```

Los anuncios son las claves `AdType:<id>`. Esto es más estable y rápido que
depender de selectores CSS.

### Flujo

1. `fetch(url)` descarga con `requests`, reintentos y espera exponencial.
2. Se guarda el HTML crudo en `data/raw/<categoria>_p<NNN>.html`.
3. `parse_state(html)` extrae el JSON y devuelve `__APOLLO_STATE__`.
4. `extraer_anuncios(state, categoria, fecha_captura)` produce filas.
5. `deduplicar` elimina IDs repetidos entre categorías o páginas.
6. `guardar_csv` escribe `data/processed/anuncios.csv` en UTF-8 con BOM.

### Paginación

Se añade `cu=1&page=N` a la URL de búsqueda. Cada página devuelve 100 anuncios.
La metadata `ROOT_QUERY["adsPerPage(...)"]` contiene `pageInfo.hasNextPage` y
`pageCount`, que se usan para detener el recorrido.

Verificación realizada: páginas 1 y 2 de bicicletas devolvieron 100 anuncios
cada una con **0 solapamiento**.

### Página de detalle (opcional)

`https://www.revolico.com/item/<slug>-<id>` añade:

- `description` y `shortDescription`
- `updatedOnByUser` (fecha absoluta)
- `isSold`, `status`

Se descargan solo para una submuestra aleatoria (`src/details.py`) porque cada
petición extra cuesta tiempo y cortesía con el servidor.

---

## 3. Diccionario de datos

### Nivel listado (`anuncios.csv`)

| Columna | Origen en el JSON | Tipo | Nulos posibles |
|---|---|---|---|
| `id` | `AdType.id` | texto | no |
| `categoria` | asignada por el script | categórica | no |
| `titulo` | `AdType.title` | texto | sí |
| `precio` | `AdType.price` | entero | sí |
| `moneda` | `AdType.currency` | categórica | sí |
| `provincia` | `ProvinceType.name` vía `provinceId` | categórica | sí |
| `municipio` | `MunicipalityType.name` vía `municipalityId` | categórica | sí |
| `fecha_publicacion` | `AdType.updatedOnToOrder` | fecha ISO | sí |
| `vistas` | `AdType.viewCount` | entero | sí |
| `n_imagenes` | `AdType.imagesCount` | entero | sí |
| `destacado` | `AdType.isPromoted` | booleano | no |
| `url` | `BASE_URL + permalink` | texto | no |
| `fecha_captura` | reloj del sistema | fecha ISO | no |

### Nivel detalle (`descripciones.csv`)

| Columna | Origen |
|---|---|
| `id` | `AdType.id` |
| `descripcion` | `description` o `shortDescription` |
| `fecha_actualizacion` | `updatedOnByUser` |
| `vendido` | `isSold` |
| `estado` | `status` |

### Campos deliberadamente excluidos

- `phoneInfo` (teléfonos)
- `name` (nombre del vendedor)
- `userId`
- imágenes (solo se guarda `imagesCount`)

No aportan al análisis y sí constituyen datos personales.

---

## 4. Reglas de limpieza (`src/clean.py`)

| # | Regla | Justificación |
|---|---|---|
| 1 | `precio` numérico; descartar nulos y `< 5` | El `1 USD` suele ser señuelo o precio en el texto |
| 2 | Deduplicar por `id` | Mismo anuncio repetido entre páginas/categorías |
| 3 | Deduplicar por `titulo + precio + municipio` | Republicaciones del mismo producto |
| 4 | `fecha_publicacion` a datetime UTC | Permite análisis temporal |
| 5 | Extraer `anio` con regex `19[5-9]\d|20[0-2]\d` | Variable clave para precios |
| 6 | Extraer `cilindrada_cc` con regex `\d{2,4}\s*(cc|ccm)` | Solo aplica a motos |
| 7 | Clasificar `condicion` por palabras clave | Nueva / usada / no especificada |
| 8 | Clasificar `tipo` (eléctrica / combustión) | Comparación central del estudio |
| 9 | Normalizar `marca` con diccionario | Evita “Yamaha”, “yamaha”, “YAMAHA” |
| 10 | `precio_usd` solo si moneda = USD | No mezclar monedas sin tasa documentada |

### Manejo de monedas

- **Opción por defecto:** analizar USD y CUP por separado. La mayoría de los
  anuncios de mayor valor están en USD.
- **Opción alternativa:** convertir CUP a USD con `--tasa-cup`. Si lo haces,
  documenta la tasa, la fecha y la fuente, y presenta un análisis de sensibilidad
  con al menos dos tasas distintas.

Nunca promedies `precio` sin separar por moneda: el resultado es inválido.

### Outliers

No se eliminan automáticamente. Se revisan con boxplots y reglas de dominio
(p. ej. una bicicleta a 20 000 USD es un error o un anuncio atípico). Cualquier
eliminación debe quedar registrada en el notebook y en este documento.

---

## 5. Sesgos y limitaciones

1. **Precios pedidos ≠ precios de transacción.** El precio publicado es una
   aspiración del vendedor.
2. **Muestra no probabilística.** Solo aparecen quienes publican en Revolico.
3. **Cobertura desigual.** La Habana suele estar sobrerrepresentada.
4. **Anuncios señuelo.** Precios simbólicos para atraer contactos.
5. **Contaminación de categoría.** Repuestos, gasolina, electrodomésticos y
   otros vehículos aparecen mezclados.
6. **Duplicados.** Un mismo producto puede republicarse varias veces.
7. **Ventana corta.** Los precios cambian; la captura es una foto temporal.
8. **Sin transacciones.** No se observa si el anuncio se vendió ni a qué precio.

Estas limitaciones no invalidan el trabajo: lo acotan. Declararlas es parte del
rigor metodológico.

---

## 6. Ética y cumplimiento

- `robots.txt` revisado antes de recolectar.
- Condiciones de uso revisadas (enlace en el sitemap del sitio).
- `User-Agent` identificable con contacto.
- Pausa aleatoria de 2–4 s; sin paralelismo.
- Volumen acotado (~200–250 peticiones para el dataset completo).
- Sin datos personales ni imágenes de terceros.
- Datos usados solo con fines académicos.
- Fuente y fecha de captura citadas en el informe.

---

## 7. Registro de captura

Rellena esta tabla cada vez que ejecutes una recolección. Es la evidencia de
reproducibilidad que te pedirá el tribunal.

| Fecha y hora | Categorías | `max-pages` | Anuncios únicos | Observaciones |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |

Comando usado:

```bash
python -m src.scraper --max-pages <N> --categorias <...>
```

---

## 8. Plan de contingencia

Si el sitio cambia, en orden de preferencia:

1. **Revisar `__NEXT_DATA__`.** Abre una página, busca el script y comprueba la
   ruta `props.pageProps.__APOLLO_STATE__`. Ajusta `parse_state` si cambió.
2. **Parsear el HTML visible.** Los anuncios están en `li[data-cy="adGrid"]`;
   dentro hay `a[href^="/item/"]`, un `<p>` con precio y otro con título.
3. **Usar el HTML crudo ya guardado.** `data/raw/` permite reprocesar sin
   volver a descargar.
4. **Reducir el alcance.** Una muestra más pequeña pero documentada sigue siendo
   válida para el proyecto.
