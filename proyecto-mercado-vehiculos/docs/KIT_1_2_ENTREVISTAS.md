# Kit para 1 o 2 entrevistas hoy

> **Meta realista:** 2 personas, 20 minutos de conversación, 40 minutos en total
> contando traslados. No son 30: se presentan como **estudio piloto**.

## 1. A quién buscar

| Prioridad | Dónde | Ejemplo |
|---|---|---|
| 1 | Tu edificio o cuadra | Un vecino con moto eléctrica |
| 2 | Taller o punto de venta | El mecánico o el vendedor |
| 3 | Familia o amigos | Alguien que use bici, patineta o moto |
| 4 | Mensajero o repartidor | En una parada o cafetería |

Regla: **mayor de 18 años**, que tenga o use el vehículo, y que acepte firmar.
Si dice que no, agradece y busca otra persona. No insistas.

## 2. Qué llevar impreso

- [ ] **4 copias** de `docs/CONSENTIMIENTO_CORTO.md` (2 por persona).
- [ ] **2 copias** de `docs/FICHA_ENTREVISTA_RAPIDA.md`.
- [ ] Bolígrafo.
- [ ] Teléfono para audio (solo si autoriza).
- [ ] Tu carné de estudiante, si lo tienes.

## 3. Qué decir al empezar

> “Buenas. Soy Brigitte, estudiante de primer año de Ciencia de Datos de la
> Universidad de La Habana. Estoy haciendo un trabajo sobre el mercado de motos,
> bicicletas y patinetas. ¿Me regala 5 minutos para unas preguntas? No pido
> teléfono ni datos personales y puede decir que no.”

Después:

> “Le explico el consentimiento: es voluntario, sus respuestas van con un código,
> y el audio y la foto son opcionales. ¿Le parece?”

Entrega el consentimiento. **Sin firma no hay entrevista.**

## 4. Orden de las preguntas

1. Qué vehículo tiene (marca, modelo, año).
2. Eléctrica o de combustión; nueva o usada.
3. Dónde y a quién se la compró.
4. Cuánto pagó y en qué moneda.
5. Cuánto gasta al mes y en qué moneda.
6. Para qué la usa y cuántos km al día.
7. Problemas de repuestos, trámites o seguro.
8. Qué es lo que más y lo que menos le gusta.
9. Si recomendaría comprar una moto en Cuba y por qué.

No leas la ficha como un interrogatorio: úsala para no olvidar ningún dato.
Deja que la persona hable; las mejores citas salen de ahí.

## 5. Qué anotar como cita textual

Copia **palabras exactas**, no tu resumen. Ejemplo:

> “La batería me dura un día si no hago mandados largos, pero si llueve no
> trabajo.” (E01)

Si no puedes escribir mientras habla, pide permiso para grabar o anota la idea
al terminar y marca que es una paráfrasis.

## 6. Qué hacer al terminar

1. Revisa que el consentimiento esté firmado y con fecha.
2. Guarda el consentimiento: `data/raw/entrevistas/E01_consentimiento.jpg`.
3. Si autorizó audio: `data/raw/entrevistas/E01.m4a`.
4. Si autorizó foto: `data/raw/entrevistas/fotos/E01_vehiculo.jpg`
   (solo el vehículo, sin personas ni matrícula).
5. Pasa los datos a `data/processed/entrevistas.csv` con
   `docs/VACIADO_ENTREVISTAS.md` o pásame las fichas y yo lo hago.
6. No pongas el nombre en la ficha, en el CSV ni en el informe.

## 7. Cómo lo usamos en el informe

Con 1 o 2 casos se escribe una sección así:

- **4.2 Estudio piloto exploratorio (n = 2)**: tabla con perfil, vehículo,
  precio pagado, uso y problema principal.
- **Tres hallazgos**: lo que coincide entre los casos y con los anuncios.
- **Una o dos citas textuales** por caso.
- **Advertencia**: n = 2 no representa el mercado; sirve para ilustrar
  mecanismos, no para estimar proporciones.

Eso ocupa espacio real, con datos reales, y no exige fingir que son 30.

## 8. Tiempo estimado

| Tarea | Tiempo |
|---|---|
| Imprimir y salir | 15 min |
| Dos entrevistas | 20–30 min |
| Volver y guardar archivos | 15 min |
| Pasar datos al CSV | 20 min |
| **Total** | **~1 hora 20 min** |

Si solo consigues una persona, también sirve: se presenta como **n = 1** y se
declara. Mejor un caso real que una sección vacía.
