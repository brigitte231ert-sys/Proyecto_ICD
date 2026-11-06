# Entrevistas de mercado (datos primarios)

Documento de trabajo para incorporar las entrevistas de campo al proyecto.
Complementan los anuncios de Revolico: los anuncios muestran **precios
pedidos**; las entrevistas aportan **percepciones, presupuestos y criterios de
compra**.

> **Regla de oro:** aunque sean 30, la muestra no representa al mercado cubano.
> Los resultados se usan para describir patrones y triangular con los anuncios,
> nunca para estimar proporciones poblacionales.

---

## 1. Diseño

| Elemento | Valor |
|---|---|
| Técnica | Encuesta corta semiestructurada, presencial |
| Muestra | 30 personas nuevas (E01–E30) |
| Selección | No probabilística, por conveniencia y cuotas |
| Lugar | Calle, talleres, puntos de venta y espacios públicos |
| Fecha | _(rellenar)_ |
| Duración media | 5–7 minutos por persona |
| Registro | Formulario escrito; audio y foto solo con permiso |
| Consentimiento | Escrito, informado y firmado |

> Las 10 personas anteriores no se incluyen: solo quedan nombres y fotos, sin
> respuestas registradas ni consentimiento escrito. No cuentan como entrevistas.

### Sesgos que hay que declarar

- Muestra de conveniencia: no es aleatoria.
- Posible concentración en una sola provincia o municipio.
- Autoselección: responde quien quiere hablar.
- Respuestas declaradas, no conducta observada.
- n = 30: frecuencias ilustrativas, sin margen de error útil.

---

## 2. Consentimiento y ética

Antes de empezar, se explica y se pide permiso:

> "Estoy haciendo un trabajo de la universidad sobre el mercado de motos,
> bicicletas y patinetas. ¿Me permite hacerle unas preguntas? No voy a publicar
> su nombre ni sus datos de contacto, y las respuestas se usan solo para el
> trabajo. Si quiere, le explico el consentimiento."

Reglas:

- No guardar nombres, teléfonos, direcciones ni audio sin permiso.
- Identificar a cada persona solo como `E01` … `E30`.
- Si la persona pide no ser citada, no se usa su respuesta.
- No publicar fotos de personas.
- **El permiso verbal no basta para el nombre ni la foto:** se necesita el
  consentimiento escrito. Si la persona no firma, se usa solo la respuesta
  anónima y, ante la duda, no se usa.
- Si alguien retira su consentimiento, se borra su material (audio, foto, fila
  del CSV e índice privado).
- Guardar las notas originales en `data/raw/entrevistas/` (ignorado por Git) y
  trabajar con la versión anonimizada.

---

## 3. Cuestionario definitivo

El cuestionario completo, con las **63 preguntas**, sus tipos y sus reglas de
aplicación, vive en **`docs/cuestionario_entrevistas.json`**. Ese archivo es la
fuente de verdad: si cambia una pregunta, se cambia allí y se versiona.

Resumen por bloques:

| Bloque | Preguntas | Contenido |
|---|---|---|
| Compra y canal | P01–P02 | Dónde compró y qué pesó más |
| Uso | P03 | Trabajo, transporte personal, mensajería, ocio |
| Moto eléctrica | P04–P08 | Carga, fallos, autonomía, apagones, preferencia |
| Perfil del entrevistado | P09–P11 | Relación con el mercado y experiencia |
| Transacción | P12–P20 | Moto, tipo, precio, moneda, pago y demora |
| Uso y gastos | P21–P26 | Km/día, único medio, gastos mensuales y repuestos |
| Preferencias | P27–P30 | Ranking, eléctrica sí/no, cambios y demanda |
| Oferta y canales | P31–P35 | Vendedores, marcas, abastecimiento, monedas/canales y barreras |
| Precios y economía | P36–P40 | Formación del precio, reventa, crédito, inflación y mantenimiento |
| Regulación y trámites | P41–P45 | Requisitos, licencias, importación, aranceles y normativa |
| Repuestos y posventa | P46–P50 | Disponibilidad, talleres, garantía y apagones |
| Tendencias | P51–P55 | Eléctricas, turismo/mensajería, oportunidades y futuro |
| Encuesta de usuarios | P56–P63 | Versión corta autoadministrada |

Reglas que el JSON ya codifica:

- `P04`, `P06` y `P07` solo aplican a motos eléctricas (`P13 == 'Eléctrica'`).
- `P12`–`P20` solo aplican a quienes compraron o vendieron (`P10 > 0`).
- `P31`–`P35` solo aplican a perfiles de oferta (vendedor, importador o revendedor).
- `P41`–`P55` se aplican a informantes clave (vendedores, importadores, mecánicos).
- `P56`–`P63` son una encuesta corta de usuarios: no repetir P12–P26 si ya se respondieron.
- `P27` usa orden 1–6 porque lista seis criterios, aunque el enunciado diga 1–5.
- Las preguntas de dinero siempre llevan moneda (`USD`, `CUP`, `MLC`).
- Las respuestas se guardan como `E01`…`E30`, sin datos personales.

---

## 4. Cómo registrar las respuestas

Un archivo `data/processed/entrevistas.csv`, **una fila por persona**. La
plantilla ya creada tiene 53 columnas agrupadas así:

| Grupo | Columnas principales | Ejemplo |
|---|---|---|
| Identificación | `id_entrevista`, `fecha`, `provincia`, `municipio` | `E11`, `2026-11-06`, `La Habana`, `Playa` |
| Perfil | `perfil`, `modalidad`, `duracion_min` | `particular`, `corta`, `6` |
| Consentimiento | `consentimiento`, `usa_nombre`, `usa_foto` | `si`, `no`, `si` |
| Encuesta corta | `P56_tiene_moto` … `P63_motivo` | `si`, `Topmaq`, `electrica` |
| Entrevista profunda | `P01_canal` … `P30_moto_mas_buscada` | `Revolico`, `precio`, `trabajo` |
| Cierre | `respuesta_abierta`, `notas` | síntesis, incidencias |

La plantilla está en `data/processed/entrevistas.csv`. No cambies los nombres de
las columnas: el script `src/entrevistas.py` los usa.

Buenas prácticas:

- Normalizar las respuestas cerradas **antes** de analizar (`Eléctrica`,
  `eléctrica`, `electrica` → `electrica`).
- No inventar valores: si no respondió, dejar vacío y anotar `no_respondio` en
  `notas`.
- Separar la respuesta textual de la codificación.
- No mezclar monedas: guardar el monto y la moneda en columnas separadas.
- Usar solo el código `E__` en el CSV; el nombre real va en el anexo privado.
- Pasar cada entrevista al CSV **el mismo día** para no perder detalle.

---

## 5. Análisis previsto

| Análisis | Método | Salida |
|---|---|---|
| Perfil de la muestra | Frecuencias absolutas y relativas | Tabla |
| Precio pagado / presupuesto | Mediana y rango por moneda (n = 30) | Tabla |
| Preferencia eléctrico/combustión | Conteo | Tabla |
| Canales de búsqueda | Conteo | Tabla |
| Gasto mensual | Mediana por moneda | Tabla |
| Problemas y posventa | Conteo de menciones | Tabla |
| Respuestas abiertas | Codificación temática (3–5 temas) | Tabla de temas y citas anónimas |
| Triangulación | Comparar precios declarados con medianas de anuncios | Párrafo |

El script `src/entrevistas.py` genera `reports/entrevistas_resumen.txt` con las
frecuencias y la triangulación:

```bash
.venv/bin/python -m src.entrevistas
```

La triangulación es la parte más valiosa: por ejemplo, si la mediana de las
motos de combustión en Revolico es 2.200 USD y los entrevistados dicen estar
dispuestos a pagar 1.500 USD, aparece una brecha entre **precio pedido** y
**presupuesto de compra**.

---

## 6. Dónde va en el informe

- **Metodología:** nuevo apartado "Estudio cualitativo complementario".
- **Resultados:** apartado "Percepción y intención de compra (entrevistas)".
- **Discusión:** triangulación con los precios de los anuncios.
- **Limitaciones:** muestra de conveniencia, n = 30, autoinforme.
- **Anexo:** guion completo y tabla de respuestas anonimizadas.

---

## 7. Lista de verificación

- [ ] Guion definitivo con códigos.
- [ ] 30 entrevistas cortas (E01–E30) realizadas y pasadas al CSV.
- [ ] Consentimiento escrito y firmado por cada persona.
- [ ] Sin nombres, teléfonos ni direcciones en el CSV.
- [ ] Respuestas cerradas normalizadas.
- [ ] `data/processed/entrevistas.csv` completo.
- [ ] `reports/entrevistas_resumen.txt` generado.
- [ ] Triangulación escrita en el informe.

---

## 8. Nombres, fotos y consentimiento

El informe público usa **solo códigos** (`E01`…`E30`). Los nombres y las fotos
son datos personales y necesitan permiso explícito:

| Dato | Regla |
|---|---|
| Nombre | Solo en `data/raw/entrevistas/indice_privado.csv` o en un **anexo privado**, si la persona lo autoriza por escrito |
| Foto | Solo del vehículo, **sin personas y sin matrícula**, en `data/raw/entrevistas/fotos/` |
| Audio | Solo con permiso; se guarda en `data/raw/entrevistas/` (ignorado por Git) |
| Citas | Anónimas: “E____ dice que…” |
| Retiro | La persona puede pedir que se elimine su aportación |

Materiales:

- `data/raw/entrevistas/README.md` — reglas de la carpeta privada, nombres de
  archivos e índice privado.
- `docs/VACIADO_ENTREVISTAS.md` — de las notas al CSV, columna por columna.
- `docs/GUION_RECONTACTO.md` — guion para recuperar E01–E10.
- `docs/GUION_RECONTACTO.md` — cómo recuperar las 10 entrevistas con nombres y
  fotos, pero sin respuestas registradas.
- `docs/CONSENTIMIENTO_INFORMADO.md` — formulario para firmar (dos copias).
- `docs/GUION_ENTREVISTA_CORTA.md` — guion imprimible de 8 preguntas.
- `docs/PROTOCOLO_TRABAJO_CAMPO.md` — plan de captación y control de calidad.

> Sin consentimiento firmado no se toma foto, no se graba audio y no se publica
> el nombre. No hay excepciones.
