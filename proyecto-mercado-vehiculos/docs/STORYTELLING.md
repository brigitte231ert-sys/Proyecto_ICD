# Storytelling del proyecto

## El mapa de un mercado que no tenía mapa

### 1. El problema: un precio que se pregunta, no se consulta

En Cuba, si alguien quiere saber cuánto cuesta una moto, no abre un registro
oficial: pregunta. Pregunta en el barrio, en el grupo de WhatsApp, al mecánico,
al vecino que acaba de vender. El precio de una moto, una bicicleta o una
patineta no vive en una base de datos; vive en la conversación.

Eso no significa que no haya mercado. Significa que el mercado existe sin
memoria. Cada anuncio de Revolico es una pequeña ventana a esa memoria: alguien
escribe un título, pone un precio y espera. Si se pudieran leer miles de esas
ventanas al mismo tiempo, quizá aparecería un patrón.

La pregunta del proyecto fue sencilla: **¿cómo se comporta ese mercado cuando
se mira con datos en vez de con impresiones?**

### 2. La apuesta: convertir anuncios en evidencia

La respuesta exigía construir algo que no existía: una base reproducible de
anuncios de motos, bicicletas y patinetas. No una encuesta, no una opinión, no
una foto suelta. Una base que otra persona pudiera auditar y repetir.

El camino empezó con **13 446 anuncios únicos** recolectados de Revolico. Pero
un anuncio no es un dato limpio: hay duplicados, precios señuelo, vehículos
fuera de alcance, títulos incompletos y monedas distintas. Después de filtrar,
deduplicar y descartar precios nulos o imposibles, quedaron **9 841 anuncios
limpios**.

Ese número no es el final del proyecto. Es el comienzo de la historia.

### 3. Los hallazgos: tres certezas y una grieta

La primera certeza es que **el mercado habla en dólares**. El 97,4 % de los
anuncios con moneda están en USD. No es un detalle: significa que el precio de
una moto está atado a una divisa que la mayoría de los cubanos no recibe como
salario. El mercado existe, pero no en la moneda de la vida cotidiana.

La segunda es que **el mercado vive en La Habana**. El 94,8 % de los anuncios
se concentran allí. La capital no solo tiene más oferta: tiene más visibilidad,
más anunciantes y más competencia. Fuera de La Habana el mercado existe, pero
aparece en pequeñas muestras, casi como un eco.

La tercera es que **el mercado está segmentado**. La mediana de una moto de
combustión es de **2 200 USD**; la de una eléctrica, **1 485 USD**; la de una
patineta, **720 USD**; la de una bicicleta, **160 USD**. La bicicleta es la
puerta de entrada más barata. La moto de combustión es el segmento más caro.
La eléctrica queda en medio: más accesible que la de combustión, pero con una
dispersión enorme, porque conviven modelos económicos con importaciones de gama
alta.

Y entonces aparece la grieta: **el anuncio describe el vehículo, pero casi no
explica la operación**. En una muestra aleatoria de **200 títulos**, el **84,5 %
no menciona ninguno de los seis temas** analizados: estado, batería, papeles,
motivo de venta, urgencia o negociación. En el total de 9 841 títulos, con una
taxonomía más amplia de ocho temas, el **54,0 % tampoco menciona ninguno**.

El silencio también es un dato. El vendedor escribe “Moto” o “Bicicleta”, pone
un precio y espera. La información que falta —por qué vende, si tiene papeles,
si acepta negociar— se resuelve en la conversación privada, fuera del anuncio.
El título no es el mercado: es la puerta de entrada al mercado.

### 4. Lo que el proyecto sí puede decir

Con los datos en la mano, el proyecto puede afirmar tres cosas con solidez
descriptiva:

1. **El mercado relevante se cotiza en USD.** El precio está dolarizado y eso
   segmenta la demanda.
2. **La moto de combustión es el segmento más caro y la bicicleta el más
   barato.** La diferencia de medianas es de más de diez veces.
3. **La eléctrica ocupa un espacio intermedio.** Es la puerta de entrada
   motorizada más accesible, pero su costo total depende de batería, carga y
   repuestos, variables que los anuncios no capturan.

También puede decir lo que **no** puede afirmar: no son precios de transacción,
no es una muestra representativa, la categorización tiene ruido y la cobertura
de marca, año y cilindrada es baja. Esas no son debilidades escondidas: son
parte del mapa.

### 5. El cierre: un mapa honesto

Este proyecto no es un retrato completo del mercado. Es un **mapa honesto**:
muestra dónde está el terreno firme y dónde todavía falta profundidad.

La base de 9 841 anuncios queda como línea base. El análisis de contenido de
200 títulos queda como primera lectura del discurso de la oferta. La siguiente
fase es ampliar la muestra, leer el cuerpo completo de los anuncios y cruzar
los precios con otras fuentes.

Porque el mercado ya habló en los títulos. Ahora falta leerlo con más
precisión, desde más ángulos y con más datos.

---

## Versión corta para exponer (2–3 minutos)

1. **Hook:** “En Cuba, el precio de una moto no se consulta: se pregunta.”
2. **Problema:** no hay registro público; Revolico es el mercado real, pero está
   desordenado.
3. **Qué hicimos:** recolectamos 13 446 anuncios, limpiamos 9 841 y construimos
   una base reproducible.
4. **Tres hallazgos:** mercado dolarizado (97,4 % USD), capitalino (94,8 % La
   Habana) y segmentado (2 200 / 1 485 / 720 / 160 USD de mediana).
5. **La grieta:** el 84,5 % de 200 títulos no menciona ningún tema; el anuncio
   describe el vehículo, no la operación.
6. **Cierre:** “No es un retrato completo; es un mapa honesto. La siguiente fase
   es leer más y mejor el discurso de la oferta.”

## Estructura sugerida para 6 diapositivas

1. **El problema:** un mercado sin registro público.
2. **La apuesta:** 13 446 anuncios → 9 841 datos limpios.
3. **Los hallazgos:** dólar, La Habana y segmentación por categoría.
4. **La grieta:** el silencio de los títulos (84,5 % sin tema).
5. **El método:** muestra de 200 títulos + contraste con 9 841.
6. **El mapa:** lo que sabemos, lo que no y la siguiente fase.

## Frases ancla

- “El mercado existe sin memoria; este proyecto le construyó una.”
- “El título no es el mercado: es la puerta de entrada.”
- “El silencio también es un dato.”
- “No es un retrato completo; es un mapa honesto.”
- “Primero los datos; después, las preguntas.”
