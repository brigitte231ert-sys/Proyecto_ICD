"""Configuración central del proyecto.

Todo lo que puede cambiar (URLs, categorías, rutas, cabeceras) vive aquí.
Así, si el sitio cambia, solo tocas un archivo.
"""

from pathlib import Path

# --- Rutas -----------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DOCS = PROJECT_ROOT / "docs"
REPORTS = PROJECT_ROOT / "reports"
FIGURES = REPORTS / "figures"

# --- Fuente ----------------------------------------------------------------
BASE_URL = "https://www.revolico.com"

# Identifícate: es una buena práctica de scraping ético.
# Cambia el correo por uno real antes de recolectar.
HEADERS = {
    "User-Agent": (
        "TFG-mercado-vehiculos/1.0 "
        "(estudiante de Ciencia de Datos, Universidad de La Habana)"
    ),
    "Accept-Language": "es-CU,es;q=0.9,en;q=0.5",
}

# --- Categorías del proyecto ----------------------------------------------
# Los slugs se verificaron el 2026-11-04 contra el sitio.
CATEGORIAS = {
    "motos_combustion": {
        "category": "vehiculos",
        "subcategory": "vehiculos-motos-de-combustion",
    },
    "motos_electricas": {
        "category": "vehiculos",
        "subcategory": "vehiculos-motos-electricas-y-triciclos",
    },
    "bicicletas": {
        "category": "vehiculos",
        "subcategory": "vehiculos-bicicletas",
    },
    # Las patinetas no tienen subcategoría propia: se buscan por texto.
    "patinetas": {
        "q": "patineta",
    },
}

# --- Parámetros de recolección --------------------------------------------
# Pausa entre peticiones (segundos). No bajar de 2 s.
DELAY_RANGE = (2.0, 4.0)

# Bicicletas ronda las 43 páginas de 100 anuncios.
# Para una primera prueba usa 1.
DEFAULT_MAX_PAGES = 43

# Columnas del CSV de salida (nivel listado).
COLUMNAS = [
    "id",
    "categoria",
    "titulo",
    "precio",
    "moneda",
    "provincia",
    "municipio",
    "fecha_publicacion",
    "vistas",
    "n_imagenes",
    "destacado",
    "url",
    "fecha_captura",
]

# Tasa de cambio usada SOLO si decides convertir CUP a USD.
# CUP por 1 USD. Déjalo en None para no convertir y analizar por separado.
TASA_CUP_USD_DEFECTO = None
