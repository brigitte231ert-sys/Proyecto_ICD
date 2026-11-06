#!/usr/bin/env python3
"""Extracción de marca, año, condición, cilindrada y tipo desde el título.

Los títulos de Revolico son cortos, informales y con errores. Este módulo
concentra las reglas en un solo lugar para que el análisis, la limpieza y los
notebooks usen exactamente el mismo criterio.

Todas las funciones son de la librería estándar y devuelven ``None`` cuando no
hay señal suficiente: es preferible un nulo honesto a una marca inventada.

Uso como módulo:

    from src.extraccion import enriquecer_fila
    datos = enriquecer_fila({"titulo": "Moto Yamaha 150cc 2019 nueva"})
"""

from __future__ import annotations

import re
import unicodedata

# --- Normalización ---------------------------------------------------------

_ESPACIOS = re.compile(r"\s+")


def normalizar(texto: object) -> str:
    """Minúsculas, sin acentos y con espacios colapsados."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return _ESPACIOS.sub(" ", texto.lower()).strip()


# --- Marcas ----------------------------------------------------------------
# Alias normalizado -> nombre canónico. Se admiten variantes ortográficas y
# separaciones que aparecen en los anuncios ("top maq", "silver bike", etc.).

MARCAS: dict[str, str] = {
    # Motos internacionales
    "harley davidson": "Harley-Davidson",
    "harley": "Harley-Davidson",
    "kawasaki": "Kawasaki",
    "yamaha": "Yamaha",
    "suzuki": "Suzuki",
    "zusuki": "Suzuki",
    "honda": "Honda",
    "bmw": "BMW",
    "ktm": "KTM",
    "ducati": "Ducati",
    "benelli": "Benelli",
    "piaggio": "Piaggio",
    "vespa": "Vespa",
    "aprilia": "Aprilia",
    "gilera": "Gilera",
    "derbi": "Derbi",
    "bultaco": "Bultaco",
    "ossa": "Ossa",
    "montesa": "Montesa",
    "puch": "Puch",
    "jawa": "Jawa",
    "mz": "MZ",
    "izh": "IZH",
    "ural": "Ural",
    "dnepr": "Dnepr",
    "minsk": "Minsk",
    "riga": "Riga",
    "simson": "Simson",
    "sachs": "Sachs",
    "kreidler": "Kreidler",
    "zundapp": "Zundapp",
    "yumbo": "Yumbo",
    "hero": "Hero",
    "bajaj": "Bajaj",
    "tvs": "TVS",
    # Motos de origen chino y marcas ensambladas para Cuba
    "lifan": "Lifan",
    "liffan": "Lifan",
    "loncin": "Loncin",
    "zongshen": "Zongshen",
    "dayun": "Dayun",
    "sanya": "Sanya",
    "jiajue": "Jiajue",
    "jincheng": "Jincheng",
    "haojue": "Haojue",
    "zontes": "Zontes",
    "voge": "Voge",
    "cfmoto": "CFMoto",
    "cf moto": "CFMoto",
    "kove": "Kove",
    "qjmotor": "QJMotor",
    "rusi": "Rusi",
    "motorstar": "MotorStar",
    "euroke": "Euroke",
    "italika": "Italika",
    "vento": "Vento",
    "krathos": "Krathos",
    "trapper": "Trapper",
    "xmotors": "Xmotors",
    "x motors": "Xmotors",
    "xmotor": "Xmotors",
    "flamingo": "Flamingo",
    "lexzuki": "Lexzuki",
    "hongli": "Hongli",
    "unison": "Unison",
    "topman": "Topman",
    "topmaq": "Topmaq",
    "top maq": "Topmaq",
    "katzu": "Katzu",
    "katsu": "Katzu",
    "italy": "Italy",
    "rali": "Rali",
    "muniao": "Muniao",
    "myniao": "Myniao",
    "vivamax": "Vivamax",
    "jinghan": "Jinghan",
    "werhy": "Werhy",
    "yoazaky": "Yoazaky",
    "yoazaki": "Yoazaky",
    "yoazki": "Yoazaky",
    "mishozuki": "Mishozuki",
    "misho zuki": "Mishozuki",
    "motorstreck": "Motorstreck",
    "motor streck": "Motorstreck",
    "bera": "Bera",
    "ava": "AVA",
    "tank": "Tank",
    "jin": "Jin",
    "jmd": "JMD",
    "izuki": "Izuki",
    "isuki": "Izuki",
    "galactica": "Galactica",
    "jupiter": "Jupiter",
    "aquila": "Aquila",
    "halcon": "Halcon",
    "restrepa": "Restrepa",
    "panther": "Panther",
    "rally": "Rally",
    "caribe": "Caribe",
    # Bicicletas
    "specialized": "Specialized",
    "trek": "Trek",
    "giant": "Giant",
    "scott": "Scott",
    "merida": "Merida",
    "cannondale": "Cannondale",
    "bianchi": "Bianchi",
    "orbea": "Orbea",
    "mongoose": "Mongoose",
    "schwinn": "Schwinn",
    "diamondback": "Diamondback",
    "raleigh": "Raleigh",
    "nakamura": "Nakamura",
    "barracuda": "Barracuda",
    "silver bike": "Silver Bike",
    "silverbike": "Silver Bike",
    "bicystar": "Bicystar",
    "bicy star": "Bicystar",
    "huffy": "Huffy",
    # Patinetas y movilidad eléctrica
    "xiaomi": "Xiaomi",
    "segway": "Segway",
    "ninebot": "Ninebot",
    "razor": "Razor",
    "roinside": "Roinside",
}

# Una sola expresión regular, con los alias más largos primero, para que
# "silver bike" gane sobre "silver" y "misho zuki" sobre "mishozuki".
_MARCAS_RE = re.compile(
    r"\b("
    + "|".join(
        re.escape(alias) for alias in sorted(MARCAS, key=len, reverse=True)
    )
    + r")\b"
)

_MARCA_EXPLICITA_RE = re.compile(r"\bmarca\s*[:\-]?\s*([a-z0-9]+)")


def extraer_marca(titulo: object) -> str | None:
    """Devuelve la marca canónica o ``None`` si no se reconoce."""
    texto = normalizar(titulo)
    coincidencia = _MARCAS_RE.search(texto)
    if coincidencia:
        return MARCAS[coincidencia.group(1)]

    explicita = _MARCA_EXPLICITA_RE.search(texto)
    if explicita:
        candidata = explicita.group(1)
        if candidata in MARCAS:
            return MARCAS[candidata]
    return None


# --- Año -------------------------------------------------------------------

# Un año plausible, que no sea en realidad una cilindrada ni una unidad.
_ANIO_RE = re.compile(
    r"(?<!\$)"
    r"\b(19[5-9]\d|20[0-2]\d)\b"
    r"(?!\s*(?:cc|ccm|c\.\s*c|km|kg|kw|ah|mah|usd|cup|watt|w\b|v\b))",
    re.IGNORECASE,
)
ANIO_MINIMO = 1950
ANIO_MAXIMO = 2027


def extraer_anio(titulo: object) -> int | None:
    """Primer año plausible del título (1950–2027)."""
    for coincidencia in _ANIO_RE.finditer(str(titulo)):
        anio = int(coincidencia.group(1))
        if ANIO_MINIMO <= anio <= ANIO_MAXIMO:
            return anio
    return None


# --- Cilindrada -------------------------------------------------------------

_CILINDRADA_RE = re.compile(
    r"\b(\d{2,4})\s*(?:cc|ccm|c\.\s*c\.?)(?![a-z])", re.IGNORECASE
)
_CILINDRADA_SIN_UNIDAD_RE = re.compile(
    r"\bcilindrada\s*(?:de\s*)?(\d{2,4})\b", re.IGNORECASE
)
CILINDRADA_MINIMA = 25
CILINDRADA_MAXIMA = 2500


def extraer_cilindrada(titulo: object) -> int | None:
    """Cilindrada en cc, descartando valores imposibles."""
    for patron in (_CILINDRADA_RE, _CILINDRADA_SIN_UNIDAD_RE):
        coincidencia = patron.search(str(titulo))
        if coincidencia:
            valor = int(coincidencia.group(1))
            if CILINDRADA_MINIMA <= valor <= CILINDRADA_MAXIMA:
                return valor
    return None


# --- Condición -------------------------------------------------------------

_CONDICION_SEMINUEVA_RE = re.compile(
    r"\b(?:semi\s*nuev[ao]|casi\s+nuev[ao]|como\s+nuev[ao]"
    r"|practicamente\s+nuev[ao]|poco\s+usad[ao]|apenas\s+usad[ao])\b"
)
_CONDICION_NUEVA_RE = re.compile(
    r"\b(?:nuev[ao]s?|0\s*km|cero\s*km|sin\s+uso|a\s+estrenar"
    r"|sin\s+estrenar|nunca\s+usad[ao]|de\s+paquete|en\s+caja"
    r"|en\s+su\s+guacal|recien\s+sacad[ao])\b"
)
_CONDICION_USADA_RE = re.compile(
    r"\b(?:usad[ao]s?|de\s+uso|segunda\s+mano|de\s+segunda)\b"
)


def extraer_condicion(titulo: object) -> str:
    """``nueva``, ``seminueva``, ``usada`` o ``no_especificada``."""
    texto = normalizar(titulo)
    if _CONDICION_SEMINUEVA_RE.search(texto):
        return "seminueva"
    if _CONDICION_NUEVA_RE.search(texto):
        return "nueva"
    if _CONDICION_USADA_RE.search(texto):
        return "usada"
    return "no_especificada"


# --- Tipo de propulsión ----------------------------------------------------

_ELECTRICA_RE = re.compile(r"\b(?:electric[ao]s?|e-?bike|ebike|litio)\b")
_COMBUSTION_RE = re.compile(r"\b(?:combustion|gasolina|4t|2t|cc)\b")


def extraer_tipo(titulo: object, categoria: object = "") -> str:
    """``electrica``, ``combustion`` o ``no_especificada``."""
    texto = normalizar(titulo)
    es_electrica = bool(_ELECTRICA_RE.search(texto))
    es_combustion = bool(_COMBUSTION_RE.search(texto))

    # El título manda si contradice la categoría (bicicleta en motos, etc.).
    if es_electrica and not es_combustion:
        return "electrica"
    if es_combustion and not es_electrica:
        return "combustion"

    if categoria == "motos_electricas":
        return "electrica"
    if categoria == "motos_combustion":
        return "combustion"
    return "no_especificada"


# --- Interfaz --------------------------------------------------------------

CAMPOS_DERIVADOS = ("marca", "anio", "condicion", "cilindrada_cc", "tipo")


def enriquecer_fila(fila: dict) -> dict:
    """Devuelve solo los campos derivados de una fila del dataset."""
    titulo = fila.get("titulo", "")
    categoria = fila.get("categoria", "")
    return {
        "marca": extraer_marca(titulo),
        "anio": extraer_anio(titulo),
        "condicion": extraer_condicion(titulo),
        "cilindrada_cc": extraer_cilindrada(titulo),
        "tipo": extraer_tipo(titulo, categoria),
    }
