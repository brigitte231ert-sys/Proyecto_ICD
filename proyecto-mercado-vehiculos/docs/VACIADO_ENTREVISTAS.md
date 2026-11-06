# Hoja de vaciado: de las notas al CSV

Guía para pasar cada entrevista a `data/processed/entrevistas.csv` sin perder
datos, sin mezclar monedas y sin filtrar información personal.

> **Regla de oro:** una fila por persona. Si un dato no está en tus notas, se
> deja **vacío** y se anota `no_respondio` en `notas`. Nunca se rellena “a
> ojo”.

---

## 1. Antes de abrir el CSV

Ten a mano, por cada persona:

- [ ] El formulario o las notas de la entrevista.
- [ ] El consentimiento firmado (o la marca de que lo firmó).
- [ ] El audio, si lo autorizó.
- [ ] La foto del vehículo, si la autorizó.
- [ ] El código asignado (`E01`…`E30`).

Si falta el consentimiento, **no se pasa la fila**. Primero se resuelve el
consentimiento.

## 2. Orden recomendado de llenado

1. **Identificación:** `id_entrevista`, `fecha`, `provincia`, `municipio`.
2. **Perfil:** `perfil`, `modalidad`, `duracion_min`.
3. **Consentimiento:** `consentimiento`, `usa_nombre`, `usa_foto`.
4. **Bloque corto:** `P56`…`P63` (lo tienen las 30 personas).
5. **Bloque profundo:** `P01`…`P30` (solo si ampliaste la conversación).
6. **Cierre:** `respuesta_abierta`, `notas`.

El bloque corto se llena aunque la entrevista haya sido profunda: son datos
básicos del vehículo y del gasto.

## 3. Valores permitidos

Usa exactamente estos valores (minúsculas, sin tildes) para que el análisis no
se rompa:

| Columna | Valores |
|---|---|
| `modalidad` | `profunda`, `corta` |
| `consentimiento` | `si`, `no` |
| `usa_nombre`, `usa_foto` | `si`, `no` |
| `P56_tiene_moto` | `si`, `no` |
| `P57_condicion` | `nueva`, `usada`, `no_aplica` |
| `P58_lugar` | `revolico`, `telegram`, `redes`, `tienda`, `conocido`, `otro` |
| `P58_tipo_vendedor` | `estatal`, `mipyme`, `importador`, `revendedor`, `particular`, `no_sabe` |
| `P59_moneda`, `P60_moneda`, `P17_moneda`, `P23_moneda` | `USD`, `CUP`, `MLC` |
| `P62_problemas` | `si`, `no` |
| `P62_cual` | `repuestos`, `tramites`, `seguro`, `otro` |
| `P63_recomienda` | `si`, `no`, `depende` |
| `P01_canal` | `revolico`, `telegram`, `conocido`, `otro` |
| `P02_criterio` | `precio`, `motor`, `autonomia`, `marca`, `otro` |
| `P13_tipo` | `electrica`, `combustion`, `no_especifica` |
| `P14_condicion` | `nueva`, `usada`, `no_especifica` |
| `P22_unico_medio` | `si`, `no` |
| `P26_problemas_repuestos` | `si`, `no` |
| `P28_considero_electrica`, `P29_cambiaria` | `si`, `no`, `no_sabe` |
| `P09_relacion_mercado` | `usuario`, `comprador`, `vendedor`, `mecanico`, `importador`, `otro` |

Para campos de respuesta múltiple (`P03_uso`), separa con punto y coma:
`trabajo;transporte_personal`.

## 4. Diccionario rápido de columnas

### Identificación y perfil

| Columna | Qué va |
|---|---|
| `id_entrevista` | `E01`…`E30` |
| `fecha` | `AAAA-MM-DD` |
| `provincia` | Nombre de la provincia |
| `municipio` | Nombre del municipio |
| `perfil` | `particular`, `vendedor`, `mecanico`, `importador`, `otro` |
| `modalidad` | `profunda` o `corta` |
| `duracion_min` | Minutos, solo el número |
| `consentimiento` | `si` si firmó |
| `usa_nombre` | `si` solo si autorizó el nombre en el anexo privado |
| `usa_foto` | `si` solo si autorizó la foto del vehículo |

### Bloque corto (P56–P63)

| Columna | Qué va |
|---|---|
| `P56_tiene_moto` | Si tiene moto propia o la usa |
| `P56_marca`, `P56_modelo` | Texto tal como lo dijo; si no sabe, vacío |
| `P56_anio` | Año de la moto; vacío si no lo sabe |
| `P57_condicion` | Nueva o usada |
| `P58_lugar` | Dónde la compró |
| `P58_tipo_vendedor` | A quién se la compró |
| `P59_monto`, `P59_moneda` | Precio pagado, separado por moneda |
| `P60_gasto_mes`, `P60_moneda` | Gasto mensual declarado |
| `P61_mas_gusta`, `P61_menos_gusta` | Síntesis corta, no transcripción |
| `P62_problemas`, `P62_cual`, `P62_detalle` | Si tuvo problemas y cuáles |
| `P63_recomienda`, `P63_motivo` | Si recomienda y por qué |

### Bloque profundo (P01–P30)

| Columna | Qué va |
|---|---|
| `P01_canal` | Canal de compra |
| `P02_criterio` | Lo más importante al comprar |
| `P03_uso` | Uso principal |
| `P09_relacion_mercado` | Relación con el mercado |
| `P10_n_operaciones` | Número de operaciones en 5 años |
| `P12_vehiculo` | Marca/modelo comprado o vendido |
| `P13_tipo` | Eléctrica o combustión |
| `P14_condicion` | Nueva o usada |
| `P15_anio_transaccion` | Año de la operación |
| `P16_monto`, `P17_moneda` | Monto y moneda de la operación |
| `P21_km_dia` | Kilómetros al día |
| `P22_unico_medio`, `P22_otro_medio` | Si es su único medio y cuál usa además |
| `P23_gasto_mes`, `P23_moneda` | Gasto mensual |
| `P24_gasto_repuestos` | Gasto en repuestos (indica moneda en `notas` si no es claro) |
| `P25_gasto_seguridad` | Gasto en seguridad |
| `P26_problemas_repuestos` | Si tuvo problemas con repuestos |
| `P27_ranking` | Orden de preferencia, por ejemplo `precio > autonomia > marca` |
| `P28_considero_electrica` | Si consideraría una eléctrica |
| `P29_cambiaria` | Si cambiaría su vehículo |
| `P30_moto_mas_buscada` | Modelo que considera más buscado |

### Cierre

| Columna | Qué va |
|---|---|
| `respuesta_abierta` | Una cita o síntesis de la respuesta más útil, entre comillas |
| `notas` | Incidencias: `no_respondio`, `interrumpida`, `audio_no_autorizado` |

## 5. Formato de una fila

```text
id_entrevista: E__
fecha: AAAA-MM-DD
provincia: ...
municipio: ...
perfil: particular | vendedor | mecanico | importador | otro
modalidad: profunda | corta
consentimiento: si
usa_nombre: si | no
usa_foto: si | no
duracion_min: ...
```

No copies valores de ejemplo: cada fila debe venir de una entrevista real.

## 6. Después de cada tanda

1. Guarda el CSV.
2. Ejecuta:
   ```bash
   cd /home/bri/proyectos/proyecto-mercado-vehiculos
   .venv/bin/python -m src.entrevistas
   ```
3. Revisa al inicio de `reports/entrevistas_resumen.txt`:
   - `Registradas`, `Faltan` y `Códigos pendientes`;
   - que **no** aparezca `AVISO DE PRIVACIDAD`.
4. Si aparece el aviso, borra el teléfono o correo del campo de texto y pásalo
   a `data/raw/entrevistas/indice_privado.csv` (solo si la persona lo autorizó).
5. Comprueba que el número de filas coincide con el número de entrevistas
   hechas.

## 7. Errores típicos

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| Poner `Eléctrica` y `electrica` | Dos categorías distintas | Usar siempre minúsculas |
| Guardar `1500 USD` en `P16_monto` | El monto no se puede sumar | Monto y moneda en columnas separadas |
| Poner el nombre en `notas` | Dato personal en la parte pública | Nombre solo en el índice privado |
| Dejar `consentimiento` vacío | No se puede defender la ética | `si` solo si está firmado |
| Inventar un dato que no está en las notas | Datos falsos | Dejar vacío y anotar `no_respondio` |
