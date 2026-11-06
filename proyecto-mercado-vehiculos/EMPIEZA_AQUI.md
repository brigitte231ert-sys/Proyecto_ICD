# EMPIEZA AQUÍ

Estás en la carpeta correcta:

```
/home/bri/proyectos/proyecto-mercado-vehiculos
```

## Lo único que tienes que hacer

1. **Lee el plan:** `docs/PLAN_DE_TRABAJO.md`
2. **Pídeme en el chat:** “ejecuta el scraper de una página”
3. **Revisa el resultado:** `data/processed/anuncios.csv`

No necesitas abrir una terminal aparte: yo ejecuto los comandos desde el chat.

## Primer comando (si lo quieres escribir tú)

```bash
python3 -m src.scraper --max-pages 1 --categorias bicicletas
```

## Atajo

Si no sabes qué sigue, pregúntame:

- “¿Qué hago ahora?”
- “Muéstrame el estado del proyecto”
- “Ejecuta el siguiente paso”

## Documentos útiles

| Archivo | Para qué |
|---|---|
| `docs/PLAN_DE_TRABAJO.md` | Ruta paso a paso y plan de 2 semanas |
| `docs/HANDOFF.md` | Estado actual del proyecto |
| `docs/JOURNAL.md` | Bitácora de lo que ya se hizo |
| `README.md` | Instalación y reproducción completa |
| `docs/metodologia.md` | Fuente, limpieza y ética |

## Dependencias

Hoy, para el scraper, solo hace falta `requests` (ya está instalado).
Para la limpieza y los notebooks necesitarás `pandas`, `matplotlib`,
`seaborn` y `jupyter`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Si `pip` o `venv` fallan, pídeme ayuda desde el chat.
