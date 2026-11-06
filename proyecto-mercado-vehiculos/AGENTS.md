# AGENTS.md

Instrucciones para agentes de OpenCode que trabajen en este repositorio.

## Proyecto

Análisis del mercado de motos, bicicletas y patinetas en Cuba usando anuncios
públicos de Revolico. El objetivo es un dataset reproducible + notebooks de
limpieza/EDA + informe. Sin dashboard ni modelo predictivo.

## Convenciones

- Idioma de la documentación y los comentarios: **español**.
- Código Python 3.10+, estilo PEP 8, nombres de funciones en español.
- No guardar datos personales en archivos versionados ni en `docs/`, `reports/`
  o `data/processed/` (teléfonos, nombres, `userId`, imágenes). La única
  excepción es `data/raw/entrevistas/`, que está ignorada por Git y solo admite
  audios, fotos de vehículos y el índice privado **con consentimiento escrito**.
- No reducir la pausa entre peticiones por debajo de 2 s ni paralelizar.
- No mezclar USD y CUP sin una tasa documentada.
- Solo se analizan las entrevistas con `consentimiento = si`; las demás se
  excluyen del resumen y de la triangulación.
- Los datos crudos de `data/raw/` no se borran ni se sobrescriben.
- `data/`, `reports/figures/` y `.venv/` están ignorados por Git.

## Comandos

```bash
python -m src.scraper --max-pages 1 --categorias bicicletas
python -m src.scraper --max-pages 43
python -m src.details --n 300
python -m src.clean
python -m src.entrevistas
python -m src.transcribir --modelo base
python3 -m py_compile src/*.py
```

## Cierre de sesión

Al terminar una tarea o cuando el usuario pida cerrar la sesión:

1. Añade una entrada al final de `docs/JOURNAL.md` (append-only) con fecha,
   objetivo, hechos, decisiones, comandos, errores, pendientes y siguiente paso.
2. Reescribe `docs/HANDOFF.md` con el estado actual usando su plantilla.
3. Verifica que las rutas y comandos citados existan.
4. No incluyas secretos ni datos personales.
5. Responde con un resumen breve y el próximo paso exacto.

Si no hay cambios que registrar, dilo y no inventes actividad.

## Referencias

- `README.md` — reproducción en 5 pasos.
- `docs/HANDOFF.md` — estado actual.
- `docs/JOURNAL.md` — historia de sesiones.
- `docs/metodologia.md` — método, limpieza y ética.
- `docs/VACIADO_ENTREVISTAS.md` — guía de vaciado de entrevistas al CSV.
- `docs/GUION_RECONTACTO.md` — cómo recuperar E01–E10 sin respuestas.
- `docs/prompt-handoff-journal.md` — plantillas de cierre.
