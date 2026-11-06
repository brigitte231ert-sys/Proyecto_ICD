# Protocolo de trabajo de campo — 30 entrevistas cortas

> **Situación de partida:** de las 10 personas solo quedan nombres y fotos de
> los vehículos, **sin respuestas registradas y sin consentimiento firmado**.
> Por eso no se pueden usar: no cuentan como entrevistas.
>
> **Meta:** 30 entrevistas cortas nuevas (E01–E30).
> **Duración:** 5–7 minutos por persona.
> **Regla de oro:** no se inventa ninguna respuesta, nombre ni foto. Sin
> consentimiento firmado, la persona no cuenta. Si no se llega a 30, se
> documenta y se negocia con el profesor.

---

## 1. Diseño de la muestra

| Elemento | Decisión |
|---|---|
| Técnica | Encuesta corta semiestructurada, presencial |
| Muestreo | No probabilístico, por conveniencia y cuotas |
| Muestra | 30 personas nuevas (E01–E30) |
| Unidad | Persona de 18 años o más con relación directa al mercado |
| Lugar | Provincia y municipios donde vives o te desplazas |
| Fecha | _(rellenar al cerrar el campo)_ |
| Registro | Formulario en papel + audio solo con permiso |
| Duración | 5–7 minutos por persona |

### Cuotas sugeridas para las 30

Ajusta las cuotas a lo que encuentres, pero intenta que no sean todos iguales:

| Perfil | Meta | Ejemplos |
|---|---|---|
| Usuarios de moto eléctrica | 10 | Mensajeros, trabajadores, estudiantes |
| Usuarios de moto de combustión | 8 | Trabajadores, particulares |
| Usuarios de bicicleta o patineta | 4 | Trabajadores, estudiantes |
| Vendedores / revendedores | 4 | Puntos de venta, importadores |
| Mecánicos / talleres | 4 | Talleres de motos y bicis |

> Si una cuota no se cumple, se declara. No se rellena con personas inventadas.

## 2. Criterios de inclusión y exclusión

**Incluye a quien:**

- tenga 18 años o más;
- use, haya comprado o haya vendido una moto, bicicleta o patineta;
- viva o trabaje en la zona;
- entienda el objetivo y firme el consentimiento.

**Excluye a quien:**

- sea menor de edad;
- no tenga relación directa con el tema;
- no quiera participar o no firme el consentimiento;
- esté en una situación que impida una conversación tranquila.

No hace falta que la persona sea dueña: puede ser quien decide la compra en la
familia o quien usa el vehículo a diario.

## 3. Dónde captar

Prioriza lugares donde la gente ya está hablando del tema:

1. Talleres y mecánicos de motos y bicicletas.
2. Puntos de venta y parqueos de motos.
3. Paradas y zonas de mensajería / delivery.
4. Ferreterías y tiendas de repuestos.
5. Grupos de Telegram o Facebook (pide permiso al administrador y no publiques
   datos personales).
6. Contactos personales y bola de nieve: pide **1 o 2 contactos** a cada
   persona que entrevistes.

**Mejores horarios:** 8:00–11:00 y 16:00–19:00.

## 4. Plan de 5 días

| Día | Meta | Acción |
|---|---|---|
| 1 | 6 (2 piloto + 4) | Probar el guion, medir tiempo, corregir dudas |
| 2 | 6 | Talleres + puntos de venta |
| 3 | 6 | Mensajería + parques + contactos |
| 4 | 6 | Repuestos + redes + bola de nieve |
| 5 | 6 + cierre | Completar faltantes, revisar formularios, pasar a CSV |

> Meta realista: **2–3 horas de campo al día** y **6 personas por salida**.
> Si una salida falla, no la inventes: anota cuántas personas abordaste y
> cuántas aceptaron.

## 5. Materiales que debes llevar

- [ ] Guion corto impreso (`docs/GUION_ENTREVISTA_CORTA.md`), varias copias.
- [ ] Consentimiento impreso (`docs/CONSENTIMIENTO_INFORMADO.md`), **dos copias
      por persona**.
- [ ] Bolígrafo y tabla de apoyo.
- [ ] Teléfono para audio (solo si la persona autoriza).
- [ ] Esta hoja de protocolo y la lista de códigos E01–E30.
- [ ] Carné de estudiante o carta de la universidad, si la tienes.

## 6. Cómo acercarte

Fórmula breve, sin presión:

> “Buenos días, soy estudiante de primer año de Ciencia de Datos de la
> Universidad de La Habana. Estoy haciendo un trabajo sobre el mercado de motos,
> bicicletas y patinetas. ¿Me regala 5 minutos para unas preguntas? No pido
> datos de contacto y puede decir que no.”

Si la persona duda, añade:

> “No es una venta ni una encuesta política. Son 8 preguntas sobre su moto y
> cómo la usa. Si quiere, le muestro el consentimiento.”

Si dice que no:

> “Gracias igual. Que tenga buen día.”

No insistas más de una vez.

## 7. Consentimiento y privacidad

Antes de la primera pregunta:

1. Explica el objetivo, la duración y que es voluntario.
2. Entrega el consentimiento y responde dudas.
3. Pide permiso para **audio** y **foto del vehículo** por separado.
4. Firma las dos copias: una para la persona y otra para el proyecto.
5. Si no autoriza audio, toma notas a mano.
6. Si no autoriza foto, no la tomes.
7. Si no firma, no se toma foto ni se usa su nombre. Sus respuestas anónimas
   solo se usan si el profesor lo autoriza; ante la duda, no se usan.

> **Permiso verbal no es consentimiento escrito.** Que la persona acepte hablar
> y permita una foto no autoriza a publicar su nombre ni la imagen. Para eso
> hace falta el formulario firmado.

Reglas del proyecto:

- En el informe público se usa **E01…E30**, nunca el nombre.
- El nombre solo va en un **anexo privado** si la persona lo autoriza por
  escrito.
- Las fotos son **solo del vehículo**: sin personas, sin matrícula y sin
  reflejos que identifiquen.
- Los audios y fotos se guardan en `data/raw/entrevistas/` (ignorado por Git).
  Las instrucciones completas están en `data/raw/entrevistas/README.md`.
- Los nombres y contactos, si se autorizan, van solo en
  `data/raw/entrevistas/indice_privado.csv`, nunca en `docs/` ni en
  `data/processed/`.
- No se publican en redes ni se comparten con terceros.
- La persona puede retirar su consentimiento y pedir que se elimine su
  aportación.

## 8. Registro de cada entrevista

1. Asigna el código correlativo: **E01, E02, … E30**.
2. Guarda el consentimiento escaneado como `E01_consentimiento.pdf`.
3. Guarda el audio como `E01.m4a`, `E02.opus`, etc.
4. Guarda la foto como `fotos/E01_vehiculo.jpg` (solo si la autorizó).
5. Anota el código en `data/raw/entrevistas/indice_privado.csv` con las
   autorizaciones; el nombre y el contacto solo si los dio.
6. Transcribe con:
   ```bash
   .venv/bin/python -m src.transcribir --modelo base
   ```
7. Pasa las respuestas a `data/processed/entrevistas.csv` **el mismo día**,
   siguiendo `docs/VACIADO_ENTREVISTAS.md`.
8. Separa la cita textual de tu interpretación.
9. Si no respondió, deja el campo vacío y anota `no_respondio` en `notas`.
10. No mezcles monedas: guarda monto y moneda en columnas separadas.

## 9. Control de calidad

- [ ] Cada formulario tiene código, fecha, provincia y municipio.
- [ ] Cada formulario tiene consentimiento firmado.
- [ ] No hay nombres ni teléfonos en el CSV.
- [ ] Las respuestas cerradas están normalizadas.
- [ ] Las monedas están separadas.
- [ ] Las fotos no muestran personas ni matrículas.
- [ ] Se anotaron las negativas y las cuotas no cumplidas.
- [ ] Otra persona puede entender el formulario sin preguntarte.

## 10. Plan B si no llegas a 30

No rellenes con datos falsos. Haz esto:

1. Anota cuántas personas abordaste, cuántas aceptaron y por qué fallaron las
   demás.
2. Entrega lo que tengas (por ejemplo, 20 cortas).
3. Declara la limitación en el informe.
4. Pide al profesor una ampliación de plazo o que acepte un diseño con menos
   casos y más peso de los anuncios.
5. Si acepta, completa las que falten y actualiza el CSV.

## 11. Checklist final

- [ ] 30 cortas (E01–E30) hechas y pasadas al CSV.
- [ ] Consentimientos firmados y archivados en `data/raw/entrevistas/`.
- [ ] `indice_privado.csv` actualizado y fuera de Git.
- [ ] Audios transcritos (si hubo permiso).
- [ ] Fotos de vehículos sin datos identificativos.
- [ ] `reports/entrevistas_resumen.txt` generado.
- [ ] Limitaciones escritas en `reports/informe.md`.
