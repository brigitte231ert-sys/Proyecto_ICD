#!/usr/bin/env python3
"""Transcribe las entrevistas de audio a texto con Whisper local.

Lee los audios de ``data/raw/entrevistas/`` y guarda un ``.txt`` por archivo en
``data/raw/entrevistas/transcripciones/``. El audio nunca sale de la máquina.

La primera ejecución descarga el modelo (unos 150 MB para ``base`` y unos
500 MB para ``small``). Después funciona sin conexión.

Uso:

    python -m src.transcribir
    python -m src.transcribir --modelo small
    python -m src.transcribir --idioma es --modelo base

Formatos admitidos: m4a, mp3, opus, ogg, wav, flac, aac, mp4, webm.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from faster_whisper import WhisperModel

from src.config import DATA_RAW

EXTENSIONES = {
    ".m4a",
    ".mp3",
    ".opus",
    ".ogg",
    ".wav",
    ".flac",
    ".aac",
    ".mp4",
    ".webm",
}


def buscar_audios(carpeta: Path) -> list[Path]:
    return sorted(
        archivo
        for archivo in carpeta.iterdir()
        if archivo.is_file() and archivo.suffix.lower() in EXTENSIONES
    )


def transcribir(modelo: WhisperModel, archivo: Path, idioma: str) -> str:
    segmentos, informacion = modelo.transcribe(
        str(archivo),
        language=idioma,
        vad_filter=True,
        beam_size=5,
    )
    lineas = [
        f"# {archivo.name}",
        f"# Duración: {informacion.duration:.1f} s | Idioma: {informacion.language}",
        "",
    ]
    for segmento in segmentos:
        texto = segmento.text.strip()
        if texto:
            lineas.append(f"[{segmento.start:7.1f}s → {segmento.end:7.1f}s] {texto}")
    return "\n".join(lineas)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--entrada",
        type=Path,
        default=DATA_RAW / "entrevistas",
        help="Carpeta con los audios.",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=None,
        help="Carpeta de transcripciones (por defecto, entrada/transcripciones).",
    )
    parser.add_argument(
        "--modelo",
        default="base",
        choices=("tiny", "base", "small", "medium"),
        help="Tamaño del modelo Whisper. Más grande = más preciso y más lento.",
    )
    parser.add_argument(
        "--idioma",
        default="es",
        help="Idioma del audio (por defecto, es).",
    )
    args = parser.parse_args()

    if not args.entrada.exists():
        raise SystemExit(f"No existe la carpeta {args.entrada}.")

    audios = buscar_audios(args.entrada)
    if not audios:
        raise SystemExit(
            f"No hay audios en {args.entrada}.\n"
            "Copia los archivos como E01.m4a, E02.opus, …"
        )

    salida = args.salida or (args.entrada / "transcripciones")
    salida.mkdir(parents=True, exist_ok=True)

    print(f"Modelo: {args.modelo} | Idioma: {args.idioma}")
    print(f"Audios: {len(audios)}")
    modelo = WhisperModel(args.modelo, device="cpu", compute_type="int8")

    for archivo in audios:
        destino = salida / f"{archivo.stem}.txt"
        print(f"Transcribiendo {archivo.name} …")
        try:
            texto = transcribir(modelo, archivo, args.idioma)
        except Exception as error:  # noqa: BLE001 - se informa y se continúa
            print(f"  Error con {archivo.name}: {type(error).__name__}: {error}")
            continue
        destino.write_text(texto, encoding="utf-8")
        print(f"  Guardado en {destino}")

    print("\nListo. Revisa las transcripciones antes de pasarlas al CSV.")
    print("No se borra ningún audio: quedan en data/raw/entrevistas/.")


if __name__ == "__main__":
    main()
