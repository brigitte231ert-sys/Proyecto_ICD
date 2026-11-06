# Datos

Esta carpeta contiene los datos del proyecto. **Nada de aquí se versiona** en Git
(ver `.gitignore`): los archivos se regeneran ejecutando los scripts.

## Estructura

```
data/
├── raw/                     # HTML crudo tal como llega del sitio
│   ├── bicicletas_p001.html
│   ├── motos_combustion_p001.html
│   └── entrevistas/         # carpeta privada: audios, fotos y consentimientos
└── processed/               # Datos tabulares derivados
    ├── anuncios.csv             # salida del scraper
    ├── descripciones.csv        # salida de src/details.py (opcional)
    └── anuncios_limpios.csv     # salida de src/clean.py
```

## Reglas

1. **El crudo no se toca.** `data/raw/` es la evidencia original: si cambia el
   sitio o el parser, puedes reprocesar sin volver a descargar.
2. **El procesado se reconstruye.** Cualquier `anuncios_limpios.csv` debe poder
   regenerarse con `python -m src.scraper` + `python -m src.clean`.
3. **No se guardan datos personales.** Ni teléfonos, ni nombres de vendedores,
   ni identificadores de usuario. El scraper los descarta por diseño. La única
   excepción es `data/raw/entrevistas/`, privada e ignorada por Git, para
   audios, fotos de vehículos y el índice de nombres **con consentimiento
   escrito** (ver el README de esa carpeta).
4. **Fecha de captura siempre presente.** La columna `fecha_captura` permite
   citar el momento exacto de la recolección en el informe.

## Diccionario de datos

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | texto | Identificador del anuncio en Revolico |
| `categoria` | categórica | `motos_combustion`, `motos_electricas`, `bicicletas`, `patinetas` |
| `titulo` | texto | Título publicado por el vendedor |
| `precio` | numérico | Precio pedido, tal como aparece en el anuncio |
| `moneda` | categórica | `USD` o `CUP` |
| `provincia` | categórica | Provincia resuelta desde el ID |
| `municipio` | categórica | Municipio resuelto desde el ID |
| `fecha_publicacion` | fecha (ISO) | Última actualización del anuncio |
| `vistas` | entero | Contador de visitas al momento de la captura |
| `n_imagenes` | entero | Número de imágenes del anuncio |
| `destacado` | booleano | Si el anuncio es promocionado |
| `url` | texto | Enlace permanente al anuncio |
| `fecha_captura` | fecha (ISO) | Momento de la recolección |

Columnas derivadas por `src/clean.py`:

| Columna | Descripción |
|---|---|
| `anio` | Año extraído del título (1950–2029) |
| `cilindrada_cc` | Cilindrada en cc extraída del título |
| `condicion` | `nueva`, `usada` o `no_especificada` |
| `tipo` | `electrica`, `combustion` o `no_especificada` |
| `marca` | Marca normalizada desde un diccionario |
| `precio_usd` | Precio en USD (solo si la moneda es USD o si se indica tasa) |
| `descripcion` | Texto del anuncio (solo en `descripciones.csv`) |

## Advertencia

Los datos son **precios pedidos**, no precios de transacción. No representan
todo el mercado: solo los anuncios publicados en Revolico durante la ventana de
captura. Léelo antes de sacar conclusiones en el informe.
