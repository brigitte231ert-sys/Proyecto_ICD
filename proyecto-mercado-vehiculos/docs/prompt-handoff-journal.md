# Prompt de handoff y journaling para OpenCode

Guía para que cualquier sesión de OpenCode cierre con dos artefactos:

- **`docs/HANDOFF.md`** → foto del estado actual, para que la próxima sesión
  (o una persona) continúe sin releer todo el historial.
- **`docs/JOURNAL.md`** → bitácora append-only de lo que se hizo, decidió y
  quedó pendiente.

---

## 1. Cómo usarlo

### Opción A — Al final de cada sesión (recomendado)

Pega el **Prompt principal** (sección 2) en el chat. OpenCode leerá el
repositorio, escribirá/actualizará ambos archivos y te devolverá un resumen.

### Opción B — Instrucción persistente

Añade al `AGENTS.md` de la raíz del proyecto la sección **Instrucción
persistente** (sección 5). Así OpenCode lo hará al cerrar tareas sin que se lo
pidas cada vez.

### Opción C — Comando personalizado

Si prefieres un atajo, crea un comando de OpenCode que ejecute el prompt. La
forma exacta depende de tu versión; si no estás seguro, usa la Opción A.

---

## 2. Prompt principal (copiar y pegar)

```text
Actúa como ingeniero de software y technical writer. Tu tarea es cerrar esta
sesión de trabajo generando dos documentos: un HANDOFF y una entrada de JOURNAL.

CONTEXTO
- Proyecto: <nombre o ruta del proyecto>
- Sesión actual: <resumen breve de lo que se hizo, si no lo puedes inferir>
- Público del handoff: la próxima sesión de OpenCode y, opcionalmente, una
  persona que retoma el proyecto.

PROCESO OBLIGATORIO
1. Recolecta evidencia real antes de escribir. No inventes nada.
   - Lista la estructura relevante del proyecto.
   - Revisa git si existe: `git status`, `git diff --stat`, `git log -5`.
     Si no es un repo git, usa el árbol de archivos y las fechas de modificación.
   - Lee los archivos clave (README, configuración, scripts principales,
     notebooks, tests) y los documentos de estado previos si existen.
   - Ejecuta las verificaciones disponibles y baratas (compilación, tests,
     linters, `--help`, validación de JSON). Si algo no se puede ejecutar,
     dilo explícitamente y explica por qué.
   - Busca TODOs, errores conocidos, dependencias faltantes y trabajo a medias.
2. Actualiza `docs/JOURNAL.md` en modo APPEND-ONLY:
   - No borres ni reescribas entradas anteriores.
   - Añade una entrada nueva al final con la plantilla de la sección 3.
   - Incluye fecha y hora, objetivo, hechos, decisiones, comandos ejecutados,
     errores, pendientes y siguiente paso.
3. Escribe `docs/HANDOFF.md` en modo REEMPLAZO:
   - Sobrescribe el archivo con la foto más reciente.
   - Usa la plantilla de la sección 4.
   - Debe ser autocontenido: alguien sin contexto debe poder continuar.
4. Valida antes de terminar:
   - Que las rutas y comandos citados existan y sean correctos.
   - Que no haya secretos, tokens, contraseñas ni datos personales.
   - Que el estado "funciona / no funciona / sin verificar" sea honesto.
   - Que el próximo paso sea una acción concreta, no una intención vaga.
   - Que JOURNAL y HANDOFF no se contradigan.

REGLAS
- No inventes resultados de pruebas ni estados de archivos.
- Si no hay git, no falles: usa el sistema de archivos y dilo.
- Separa claramente lo verificado de lo supuesto.
- Usa rutas absolutas o relativas a la raíz del proyecto, de forma consistente.
- No incluyas volcados largos de código; enlaza archivos y líneas.
- Si detectas trabajo sin commitear o cambios ajenos, no los revientes:
  documéntalos.
- Escribe en español, claro y conciso.
- Al final, responde en el chat con un resumen de 5–8 bullets y el próximo paso
  exacto.

ENTREGABLES
- `docs/JOURNAL.md` actualizado (entrada nueva al final).
- `docs/HANDOFF.md` reescrito.
- Resumen breve en el chat.
```

---

## 3. Plantilla para `docs/JOURNAL.md`

Cada sesión añade un bloque al final. Nunca se edita lo anterior.

```markdown
## 2026-11-04 20:30 — <título corto de la sesión>

**Objetivo:** <qué se quería lograr>

**Hecho:**
- <cambio o resultado verificable>
- <cambio o resultado verificable>

**Decisiones:**
- <decisión> — <motivo>
- <decisión> — <motivo>

**Comandos ejecutados:**
```bash
<comando>   # resultado breve
```

**Errores / bloqueos:**
- <error> — <causa> — <estado>

**Pendiente:**
- [ ] <tarea>
- [ ] <tarea>

**Siguiente paso:** <acción concreta, con comando si aplica>

**Archivos tocados:** `<ruta>`, `<ruta>`
```

---

## 4. Plantilla para `docs/HANDOFF.md`

Se reescribe completo en cada cierre.

```markdown
# Handoff — <nombre del proyecto>

> **Última actualización:** 2026-11-04 20:30
> **Sesión:** <id o título>
> **Estado:** en progreso | bloqueado | listo para revisión

## 1. TL;DR

<3–5 líneas: qué es el proyecto, en qué estado está y qué sigue.>

## 2. Objetivo y alcance

- **Objetivo:** <...>
- **Alcance actual:** <...>
- **Fuera de alcance:** <...>

## 3. Estado actual

### Funciona
- <...>

### No funciona / bloqueado
- <...> — <causa> — <qué falta>

### Sin verificar
- <...> — <por qué no se pudo verificar>

## 4. Cómo ejecutar

```bash
# Requisitos
<comandos de instalación>

# Prueba rápida
<comando>

# Flujo completo
<comando>
```

## 5. Estructura relevante

```text
<árbol resumido con una línea por archivo/carpeta importante>
```

## 6. Decisiones tomadas

| Fecha | Decisión | Motivo | Consecuencia |
|---|---|---|---|
|  |  |  |  |

## 7. Cambios recientes

- `<ruta>` — <qué cambió>
- `<ruta>` — <qué cambió>

## 8. Próximo paso exacto

1. <acción>
2. <acción>
3. <verificación>

Comando sugerido:

```bash
<comando>
```

## 9. Contexto que no debe perderse

- <restricción, convención, dato externo, credencial NO incluida, etc.>

## 10. Riesgos y advertencias

- <riesgo> — <mitigación>

## 11. Referencias

- `<ruta>` — <para qué sirve>
- <enlace externo> — <qué contiene>
```

---

## 5. Instrucción persistente para `AGENTS.md`

Añade esto al final del `AGENTS.md` del proyecto si quieres que OpenCode lo
aplique de forma automática:

```markdown
## Cierre de sesión

Al terminar una tarea o cuando el usuario pida cerrar la sesión:

1. Añade una entrada al final de `docs/JOURNAL.md` (append-only) con fecha,
   objetivo, hechos, decisiones, comandos, errores, pendientes y siguiente paso.
2. Reescribe `docs/HANDOFF.md` con el estado actual usando su plantilla.
3. Verifica que las rutas y comandos citados existan.
4. No incluyas secretos ni datos personales.
5. Responde con un resumen breve y el próximo paso exacto.

Si no hay cambios que registrar, dilo y no inventes actividad.
```

---

## 6. Prompt de arranque para la próxima sesión

Úsalo al empezar, antes de tocar código:

```text
Antes de hacer cualquier cambio:

1. Lee `docs/HANDOFF.md` y las últimas 3 entradas de `docs/JOURNAL.md`.
2. Revisa el estado real del repositorio (git status si existe).
3. Resúmeme en 5 bullets: objetivo, estado, bloqueos, próximo paso y riesgos.
4. Contrasta el handoff con la realidad y señala cualquier discrepancia.
5. Espera mi confirmación antes de modificar archivos.
```

---

## 7. Reglas de oro

- **JOURNAL = append-only.** Es historia; no se reescribe.
- **HANDOFF = reemplazo.** Es la foto de ahora; lo viejo queda en el journal.
- **Verificado ≠ supuesto.** Etiqueta cada estado con honestidad.
- **Próximo paso accionable.** Debe poder ejecutarse sin interpretar.
- **Sin secretos.** Nunca tokens, contraseñas, teléfonos ni datos personales.
- **Corto.** Si el handoff supera 2–3 pantallas, está contando historia en vez de
  estado.
