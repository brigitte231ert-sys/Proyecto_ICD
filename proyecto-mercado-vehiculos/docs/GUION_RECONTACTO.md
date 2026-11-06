# Re-contacto y recuperación de E01–E10

> **Nota para este caso:** si no tienes contacto con las personas ni
> consentimiento escrito, esta vía **no aplica**. Esas 10 personas no se usan.
> Pasa al plan de 30 entrevistas nuevas de `docs/PROTOCOLO_TRABAJO_CAMPO.md`.
> Este documento queda como referencia por si más adelante recuperas el
> contacto.

> **Situación:** tienes los nombres y las fotos de los vehículos de 10 personas,
> pero no tienes registradas sus respuestas.
>
> **Clave:** un nombre y una foto **no son una entrevista**. Son material
> ilustrativo. Para que las 10 personas cuenten en el estudio necesitas, como
> mínimo, sus respuestas y su consentimiento escrito. Esto se puede resolver
> re-contactándolas.

---

## 1. Qué hay que recuperar

Con **5–7 minutos** por persona puedes llenar el bloque corto del CSV y salvar
la entrevista:

| Pregunta | Columna del CSV |
|---|---|
| ¿Qué moto tiene? Marca, modelo, año | `P56_marca`, `P56_modelo`, `P56_anio` |
| ¿Es eléctrica o de combustión? | `P13_tipo` |
| ¿Nueva o usada? | `P57_condicion` |
| ¿Dónde y a quién se la compró? | `P58_lugar`, `P58_tipo_vendedor` |
| ¿Cuánto pagó y en qué moneda? | `P59_monto`, `P59_moneda` |
| ¿Cuánto gasta al mes y en qué moneda? | `P60_gasto_mes`, `P60_moneda` |
| ¿Para qué la usa? | `P03_uso` |
| ¿Cuántos km hace al día? | `P21_km_dia` |
| ¿Es su único medio de transporte? | `P22_unico_medio`, `P22_otro_medio` |
| ¿Ha tenido problemas de repuestos, trámites o seguro? | `P62_problemas`, `P62_cual`, `P62_detalle` |
| ¿Qué es lo que más y lo que menos le gusta? | `P61_mas_gusta`, `P61_menos_gusta` |
| ¿Recomendaría comprar una moto en Cuba? ¿Por qué? | `P63_recomienda`, `P63_motivo` |
| ¿Consideraría una moto eléctrica? ¿Por qué? | `P28_considero_electrica` |

Si la conversación original fue profunda y quieres conservar esa categoría,
necesitas recuperar también `P01`, `P02`, `P09`, `P10`, `P12`, `P16`, `P17`,
`P23` y `P27`. Eso ya son **20–25 minutos** por persona.

> **Honestidad metodológica:** si solo recuperas el bloque corto, marca esas
> filas como `modalidad = corta` y anota en `notas` que son un re-contacto. No
> las llames “profundas” si no tienes el registro de una entrevista larga.

## 2. Antes de escribir: el consentimiento

Si no tienes el consentimiento firmado, este es el primer paso. Sin él:

- no puedes usar el nombre en ningún anexo;
- no puedes publicar la foto;
- no puedes grabar audio;
- la persona no debería contar en el estudio.

Puedes enviarle el formulario por WhatsApp, pedirle que lo firme, lo fotografíe
y te lo devuelva. Guarda la foto del formulario en
`data/raw/entrevistas/E__consentimiento.pdf` o `.jpg`.

El formulario está en `docs/CONSENTIMIENTO_INFORMADO.md`.

## 3. Mensaje para WhatsApp o Telegram

Adáptalo con tu nombre y el de la persona:

> Hola ____, soy ____, el estudiante que te hizo unas preguntas sobre las motos
> para un trabajo de la universidad. Estoy cerrando el trabajo y me faltan unos
> datos de nuestra conversación. ¿Me regalas 5 minutos por llamada o por audio?
> No es una venta ni nada político. Si quieres, te mando el consentimiento para
> que veas cómo se usa la información. Gracias.

Si no responde, espera **al menos un día** y envía un segundo mensaje corto. No
insistas más de dos veces.

## 4. Guion para llamada o audio

1. **Preséntate y recuerda la conversación:** “Hola, soy ____. Nos vimos el ____
   y hablamos de tu moto para un trabajo de la universidad.”
2. **Pide permiso:** “¿Es buen momento? Son 5 minutos y puedes no responder lo
   que no quieras.”
3. **Explica el uso:** “Todo va con un código, no con tu nombre. El nombre y la
   foto solo van en un anexo privado si tú lo autorizas.”
4. **Consentimiento:** “Te mando el formulario. ¿Me lo puedes firmar y devolver
   por foto? Si no puedes, me dices.”
5. **Preguntas:** usa la lista de la sección 1, en orden. No leas la tabla: haz
   las preguntas como conversación.
6. **Cierre:** “Eso es todo. Muchas gracias. Te mando tu copia del
   consentimiento.”

## 5. Qué hacer si no puedes re-contactar a alguien

- Dos intentos como máximo.
- Anota el intento en una hoja de campo: fecha, medio y resultado, **sin
  teléfonos ni nombres** en la parte pública.
- Esa persona **no cuenta** para la meta.
- No uses su nombre ni su foto.
- Si faltan varias, tendrás que hacer más entrevistas nuevas o negociar con el
  profesor.

## 6. Qué hacer con las fotos que ya tienes

| Situación | Acción |
|---|---|
| La persona autorizó la foto por escrito | Úsala en el anexo privado; solo el vehículo, sin matrícula |
| No autorizó o no firmó | No la publiques; pídele permiso o bórrala |
| La foto muestra personas o matrícula | Recórtala o no la uses |
| Vas a compartir la foto | Quita los metadatos EXIF (pueden incluir GPS) |

Para quitar los metadatos con Python:

```bash
cd /home/bri/proyectos/proyecto-mercado-vehiculos
.venv/bin/python - <<'PY'
from PIL import Image
from pathlib import Path

for ruta in Path("data/raw/entrevistas/fotos").glob("*.jpg"):
    imagen = Image.open(ruta)
    limpia = imagen.convert("RGB")
    limpia.save(ruta, "JPEG", quality=90)  # sin EXIF
    print("limpia:", ruta.name)
PY
```

## 7. Dónde registrar cada cosa

| Dato | Archivo |
|---|---|
| Respuestas | `data/processed/entrevistas.csv` |
| Nombre y contacto | `data/raw/entrevistas/indice_privado.csv` |
| Consentimiento firmado | `data/raw/entrevistas/E__consentimiento.jpg` |
| Foto del vehículo | `data/raw/entrevistas/fotos/E__vehiculo.jpg` |
| Audio | `data/raw/entrevistas/E__.m4a` |

## 8. Meta realista

| Escenario | Qué haces | Tiempo |
|---|---|---|
| Recuperación corta | 10 re-contactos de 5–7 min + 20 nuevas cortas | 2–3 días |
| Recuperación profunda | 10 re-contactos de 20–25 min + 20 nuevas cortas | 4–5 días |
| Sin re-contacto | 30 entrevistas cortas nuevas | 5–6 días |

No hay atajo que no implique hablar con personas. La otra vía es declarar la
limitación y negociar con el profesor.

## 9. Checklist

- [ ] Tengo el consentimiento firmado de cada persona que voy a usar.
- [ ] Recuperé al menos el bloque corto de cada una.
- [ ] Anoté si la fila es `profunda` o `corta`.
- [ ] No puse nombres ni teléfonos en el CSV.
- [ ] Las fotos no muestran personas ni matrículas.
- [ ] Actualicé `indice_privado.csv`.
- [ ] Ejecuté `.venv/bin/python -m src.entrevistas` y revisé el avance.
