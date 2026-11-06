# Plan de trabajo — por dónde empezar

> Para primer año: no empieces por el informe ni por el modelo. Empieza por
> cerrar el ciclo más pequeño posible: **una página → un CSV → tres
> observaciones**. Cuando eso funcione, repites a escala.

---

## Meta de la primera sesión (2–3 horas)

Conseguir **100 anuncios reales en un CSV** y escribir **3 observaciones** sobre
ellos. Nada más. Si logras eso, ya tienes proyecto.

### Checklist

- [ ] Leer `README.md` y `docs/HANDOFF.md` (15 min).
- [ ] Verificar Python e instalar dependencias.
- [ ] Cambiar el correo placeholder del `User-Agent` en `src/config.py`.
- [ ] Ejecutar el scraper con **una sola página**.
- [ ] Abrir `data/processed/anuncios.csv` y revisar 5 filas.
- [ ] Contar anuncios, monedas y provincias.
- [ ] Anotar 3 observaciones en `docs/JOURNAL.md`.

---

## Paso 0 — Verifica tu entorno

En la terminal, desde la raíz del proyecto:

```bash
cd /home/bri/proyectos/proyecto-mercado-vehiculos

python3 --version
python3 -m pip --version
```

Si `pip` no aparece, instálalo o usa otro entorno. Si `python3 -m venv` falla
con *“ensurepip is not available”*:

```bash
sudo apt install python3-venv
```

Luego:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Si trabajas en un entorno donde no puedes instalar nada, avísame y buscamos
> alternativa. Para el scraper solo necesitas `requests`.

---

## Paso 1 — Identifícate antes de recolectar

Abre `src/config.py` y cambia:

```python
"contacto: cambia-esto@example.com"
```

por un correo real (o uno de la universidad). Es parte del scraping ético.

---

## Paso 2 — Ejecuta una sola página

```bash
python -m src.scraper --max-pages 1 --categorias bicicletas
```

Deberías ver algo así:

```
[bicicletas] página 1 → https://www.revolico.com/search?...
[bicicletas] 100 anuncios recolectados
Listo: 100 anuncios únicos en .../data/processed/anuncios.csv
```

Si falla, copia el error completo y pídeme ayuda. No lo resuelvas a ciegas.

---

## Paso 3 — Mira los datos con tus propios ojos

```bash
python3 - <<'PY'
import csv

with open('data/processed/anuncios.csv', encoding='utf-8-sig') as f:
    filas = list(csv.DictReader(f))

print('Anuncios:', len(filas))
print('Columnas:', list(filas[0]))
print('\nPrimeras 5 filas:')
for fila in filas[:5]:
    print(fila['titulo'][:60], '|', fila['precio'], fila['moneda'], '|', fila['provincia'])
PY
```

Pregúntate:

- ¿Los precios tienen sentido?
- ¿Hay anuncios en USD y en CUP?
- ¿Qué provincias aparecen más?
- ¿Hay títulos que no parecen bicicletas?
- ¿Cuántos anuncios tienen precio muy bajo?

Escribe esas respuestas en `docs/JOURNAL.md` (sección *Observaciones*).

---

## Paso 4 — Recolecta el dataset completo

Cuando la prueba de una página funcione:

```bash
python -m src.scraper --max-pages 43
```

Tarda decenas de minutos por la pausa de 2–4 s. Déjalo corriendo y no lo
interrumpas. Al terminar, anota en `docs/metodologia.md` (Registro de captura):

- fecha y hora,
- comando usado,
- número de anuncios únicos.

---

## Paso 5 — Limpia

```bash
python -m src.clean
```

Revisa el resumen que imprime: cuántos se descartaron, cuántos quedan por
categoría, cuántos nulos hay y cómo se distribuye el precio en USD.

Abre `notebooks/02_limpieza.ipynb` y ejecútalo celda por celda. Ahí puedes
cambiar reglas y ver el efecto.

---

## Paso 6 — Analiza

Abre `notebooks/03_eda.ipynb` y responde, una por una, tus preguntas de
investigación. Guarda las figuras en `reports/figures/`.

---

## Orden recomendado (2 semanas)

| Día | Tarea | Entregable |
|---|---|---|
| 1 | Entorno + 1 página + 3 observaciones | CSV de 100 filas |
| 2 | Recolección completa | CSV completo + registro de captura |
| 3 | Limpieza y revisión de reglas | `anuncios_limpios.csv` |
| 4–5 | EDA: composición y precios | Figuras 1–4 |
| 6–7 | EDA: marcas, geografía, tipo | Figuras 5–8 |
| 8–9 | Redactar resultados y discusión | Borrador del informe |
| 10 | Revisar, exportar y ensayar | Informe PDF + defensa |

---

## Qué NO hacer al principio

- No empieces por el dashboard ni por un modelo predictivo.
- No ejecutes las 43 páginas antes de probar una.
- No borres `data/raw/`: es tu evidencia.
- No promedies USD y CUP juntos.
- No escribas el informe antes de ver los datos.
- No cambies diez cosas a la vez: cambia una, ejecuta, observa.

---

## Tu primera pregunta de investigación

Si no sabes por dónde empezar el análisis, usa esta:

> **¿Cómo varía el precio pedido de las bicicletas según la marca y la
> provincia en los anuncios de Revolico?**

Es acotada, tiene dos variables y se responde con un boxplot y una tabla. Luego
amplías a motos y patinetas.

---

## Definición de “voy bien”

- [ ] Tengo un CSV con más de 100 anuncios reales.
- [ ] Sé cuántos anuncios hay por categoría y moneda.
- [ ] Puedo explicar de dónde sale cada columna.
- [ ] Tengo al menos 3 figuras con título y ejes rotulados.
- [ ] Puedo responder mis preguntas con datos, no con opiniones.
- [ ] Mi README permite que otra persona reproduzca el proyecto.
