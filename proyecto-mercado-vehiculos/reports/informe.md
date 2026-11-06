# Mercado de motos, bicicletas y patinetas en Cuba

## Un análisis exploratorio de anuncios clasificados (Revolico, 2026)

**Autor:** Brigitte Hernández Romero
**Asignatura:** Ciencia de Datos — primer año
**Institución:** Universidad de La Habana
**Fecha:** 6 de noviembre de 2026

---

## Resumen

Este trabajo describe el mercado cubano de motos, bicicletas y patinetas a
partir de **9 841 anuncios clasificados** publicados en Revolico entre el 5 de
septiembre y el 5 de noviembre de 2026. La recolección automatizada partió de
13 446 anuncios únicos; tras filtrar los relacionados con el objeto de estudio,
eliminar duplicados y descartar precios nulos o señuelo, quedó una base de
9 841 registros. El análisis es descriptivo y exploratorio: composición por
categoría, moneda y provincia, distribución de precios pedidos, marcas y
algunas características del vehículo.

Los resultados muestran un mercado dominado por el dólar (97,4 % de los
anuncios con moneda), concentrado en La Habana (94,8 %) y con una brecha
importante entre motos de combustión y eléctricas: la mediana de las primeras
es de **2 200 USD**, frente a **1 485 USD** en las eléctricas. Las bicicletas
son el segmento más barato (mediana de **160 USD**) y las patinetas se ubican
en **720 USD**. La cobertura de marca, año y cilindrada es baja, por lo que los
cruces con esas variables son exploratorios.

El componente cualitativo previsto —30 entrevistas— **no se pudo completar**.
No hay entrevistas válidas registradas ni consentimiento escrito, de modo que
el informe se apoya en los anuncios. Para compensar, se realizó un **análisis
de contenido de una muestra aleatoria de 200 títulos**, contrastado con los
9 841 títulos del dataset, que describe qué destaca el vendedor y qué
información omite. Esta limitación se declara de forma explícita y se discute
su efecto sobre las conclusiones.

**Palabras clave:** mercado, motos eléctricas, bicicletas, patinetas, Cuba,
análisis exploratorio, datos de clasificados.

---

## 1. Introducción

### 1.1 Contexto

La movilidad cotidiana en Cuba depende en gran medida de vehículos ligeros:
motos de combustión, motos eléctricas, bicicletas y patinetas. En los últimos
años la moto eléctrica se consolidó como una alternativa para mensajeros,
trabajadores y estudiantes, mientras que la bicicleta sigue siendo el medio más
barato y la patineta gana espacio en trayectos cortos. Al mismo tiempo, la
compra de un vehículo ligero implica una inversión considerable en un contexto
de ingresos bajos, restricciones de importación y escasez de repuestos.

A pesar de su importancia, no existe un registro público sistemático de precios.
La información circula en clasificados, grupos de mensajería y conversaciones
informales. Esa opacidad dificulta comparar opciones, estimar el costo real de
la movilidad y entender cómo se forma el precio.

### 1.2 Problema

Los anuncios de Revolico ofrecen una ventana a la oferta real, pero no están
estructurados para el análisis: el precio aparece como texto libre, la moneda
varía, la marca y el año suelen estar en el título y muchas publicaciones
mezclan vehículos con accesorios. Convertir ese material en una base analizable
exige un trabajo de limpieza y documentación de supuestos.

### 1.3 Preguntas de investigación

1. ¿Cómo se compone la oferta de motos, bicicletas y patinetas en Revolico?
2. ¿Qué precios se piden y cómo varían por categoría, tipo de propulsión,
   marca y provincia?
3. ¿Qué limitaciones tiene usar anuncios clasificados para describir el
   mercado y qué no se puede concluir con ellos?

### 1.4 Objetivos

**General:** describir la estructura y los precios del mercado de vehículos
ligeros en Cuba a partir de anuncios clasificados.

**Específicos:**

- construir una base limpia y reproducible de anuncios;
- describir la composición por categoría, moneda y territorio;
- comparar los precios pedidos entre segmentos;
- documentar la calidad de los datos y los sesgos del análisis.

---

## 2. Datos y método

### 2.1 Fuente

Los datos provienen de **Revolico**, sitio de clasificados de uso extendido en
Cuba. La recolección se hizo con un scraper propio en Python, respetando
`robots.txt` y con una pausa de 2–4 segundos entre peticiones. La captura se
realizó el **4 de noviembre de 2026, entre las 22:27 y las 22:36 EST**. La
ventana de publicación observada va del **5 de septiembre al 5 de noviembre de
2026**.

### 2.2 Flujo de construcción de la base

| Etapa | Anuncios |
|---|---:|
| Anuncios únicos recolectados | 13 446 |
| Relacionados con el objeto de estudio | 11 621 |
| Para revisar manualmente | 295 |
| Excluidos por no ser vehículos del alcance | 1 530 |
| Duplicados por título + precio + municipio | 817 |
| **Relacionados únicos** | **10 804** |
| Descartados en limpieza (precio nulo o señuelo) | 963 |
| **Anuncios limpios** | **9 841** |

El filtro de relevancia combinó palabras clave del título y del cuerpo del
anuncio. Se excluyeron accesorios, repuestos, servicios y vehículos fuera del
alcance. La limpieza descartó anuncios sin precio y precios menores a 5 o
mayores a 1 000 000 en la moneda declarada, tratados como señuelos o errores de
captura.

### 2.3 Variables

Cada anuncio incluye: identificador, categoría, título, precio, moneda,
provincia, municipio, fecha de publicación, vistas, número de imágenes,
indicador de anuncio destacado y URL. A partir del título se derivaron
`marca`, `anio`, `cilindrada_cc`, `condicion` y `tipo` (combustión o eléctrica).
`precio_usd` normaliza el precio cuando la moneda es USD.

### 2.4 Análisis

El análisis es **descriptivo y exploratorio**. Se usaron frecuencias,
medianas, cuartiles y correlaciones de Pearson. Se eligió la mediana como
medida central porque la distribución de precios tiene cola larga y valores
extremos. Los cruces con `anio` y `cilindrada_cc` se presentan como
exploratorios debido a su baja cobertura.

No se convirtieron precios de CUP a USD: no hay una tasa única y verificable
para el período. Por eso los cruces de precio se hacen **solo con anuncios en
USD** (9 589 de 9 841).

### 2.5 Consideraciones éticas

El análisis usa únicamente información publicada voluntariamente en un sitio
público de clasificados. No se recolectaron nombres, teléfonos ni direcciones
de los anunciantes, y el informe no identifica a ninguna persona. Las URLs se
conservan solo para trazabilidad interna y no se publican.

---

## 3. Resultados

### 3.1 Composición del mercado

La base limpia contiene **9 841 anuncios**: 3 349 motos de combustión
(34,0 %), 3 146 bicicletas (32,0 %), 2 807 motos eléctricas (28,5 %) y 539
patinetas (5,5 %).

![Composición por categoría, moneda y provincia](figures/01_composicion.png)

La moneda dominante es el **USD**, presente en 9 589 anuncios (97,4 %). Le
siguen 251 anuncios en CUP (2,6 %) y uno en MLC. La concentración en USD es un
hallazgo en sí mismo: indica que el segmento relevante del mercado se cotiza en
divisa, lo que excluye a buena parte de la población y dificulta comparar con
ingresos en pesos.

La distribución territorial es extremadamente desigual: **La Habana reúne
9 326 anuncios (94,8 %)**, seguida de Artemisa (143), Pinar del Río (64) y
Matanzas (54). Las demás provincias tienen menos de 50 anuncios cada una. Esto
no significa que en el resto del país no se vendan vehículos, sino que
Revolico se usa mucho más en la capital; el dato refleja la plataforma, no la
geografía real de la demanda.

### 3.2 Precios pedidos

En los 9 589 anuncios en USD, el precio mediano es de **1 100 USD**, la media
de **1 398,6 USD** y el rango va de 5 a 111 111 USD. La diferencia entre media
y mediana confirma una cola derecha larga: unos pocos anuncios muy caros
elevan el promedio.

| Categoría | n (USD) | Mediana | Media | Desv. típ. |
|---|---:|---:|---:|---:|
| Motos de combustión | 3 322 | **2 200** | 2 402 | 2 257 |
| Motos eléctricas | 2 796 | **1 485** | 1 540 | 3 117 |
| Patinetas | 535 | **720** | 636 | 273 |
| Bicicletas | 2 936 | **160** | 267 | 2 052 |

![Distribución de precios en USD y precio por categoría](figures/02_precios.png)

La jerarquía de precios es clara: combustión > eléctricas > patinetas >
bicicletas. La brecha entre una moto de combustión y una eléctrica es de
**715 USD** en la mediana, aproximadamente un 48 % más cara la de combustión.
Sin embargo, la desviación típica de las eléctricas (3 117) es mayor que la de
las de combustión (2 257), lo que sugiere un segmento más heterogéneo: conviven
modelos económicos con importaciones de gama alta.

Los anuncios en CUP (n = 251) tienen una mediana de **5 000 CUP**, con un rango
de 12 a 250 000. No se comparan directamente con los de USD por la ausencia de
una tasa de referencia documentada.

### 3.3 Motos eléctricas y de combustión

Entre las motos, 3 340 se clasificaron como de combustión y 2 801 como
eléctricas; solo 15 quedaron sin clasificar o con una etiqueta inconsistente.
La mediana confirma la hipótesis de partida: **la moto eléctrica es más barata
que la de combustión** (1 485 vs. 2 200 USD), aunque con mayor dispersión.

![Precio de motos por tipo de propulsión](figures/06_tipo_moto.png)

Este resultado es consistente con el uso urbano: la eléctrica tiene menor
autonomía y depende de la carga, pero su precio de entrada es más bajo y su
costo operativo por kilómetro suele ser menor. El anuncio no permite medir ese
costo operativo; solo muestra el precio pedido.

### 3.4 Marcas

La marca se pudo identificar en **3 081 anuncios (31,3 %)**. El resto no la
declara en el título o usa denominaciones ambiguas. Las marcas más frecuentes
son:

| Marca | Anuncios |
|---|---:|
| Topmaq | 418 |
| JMD | 257 |
| Yoazaky | 186 |
| Xmotors | 154 |
| Halcón | 152 |
| Unison | 146 |
| Katzu | 136 |
| Vivamax | 132 |
| Italy | 125 |
| Tank | 120 |

![Marcas más frecuentes y precio mediano por marca](figures/04_marcas.png)

Entre las marcas con al menos 20 anuncios en USD, las medianas más altas
corresponden a **Yamaha (5 500 USD)** y **Honda (4 500 USD)**, coherentes con
el prestigio y la disponibilidad de repuestos. En el extremo opuesto, las
marcas de bicicletas se ubican por debajo de 200 USD: Huffy (150), Myniao
(170), Vivamax (180) y Silver Bike (185).

En motos de combustión, las medianas se agrupan entre 2 200 y 2 600 USD
(Xmotors 2 400; Unison 2 600; Italy 2 550; Katzu 2 250; Suzuki 2 200). En
eléctricas, Topmaq lidera en volumen (418 anuncios) con mediana de 2 200 USD,
mientras que JMD, la segunda más frecuente, tiene mediana de 1 490 USD.

### 3.5 Geografía

La Habana concentra **9 080 de los 9 589 anuncios en USD** y tiene una mediana
de **1 000 USD**. Entre las provincias con al menos 10 anuncios, las medianas
más altas son Pinar del Río (2 000), Holguín (1 850) e Isla de la Juventud
(1 850); las más bajas, Cienfuegos (210) y Santiago de Cuba (280). Estas cifras
deben leerse con cautela: fuera de La Habana las muestras son pequeñas y
pueden estar dominadas por un tipo de vehículo.

![Precio mediano en USD por provincia](figures/05_provincias.png)

### 3.6 Condición, año y cilindrada

La condición solo se declara en **1 078 anuncios (11,0 %)**: 952 nuevos, 91
usados y 35 seminuevos. En las motos, la mediana de las declaradas como usadas
(1 210 USD) es menor que la de las nuevas (1 890 USD), lo que va en la
dirección esperada, aunque el grupo de usadas es pequeño.

El **año** aparece en 8,4 % de los anuncios; entre las motos en USD, en 798 de
6 118 (13,0 %). La mediana es 2026 y el rango va de 1950 a 2026. La correlación
entre año y precio es débil y negativa (r = −0,167, n = 798): a mayor año
declarado, menor precio pedido, un resultado contraintuitivo que probablemente
refleja que los anuncios más caros no declaran año o que "2026" se usa como
sinónimo de "nuevo".

La **cilindrada** aparece en 13,6 % de los anuncios y en 21,9 % de las motos en
USD (1 342 casos). La correlación con el precio es moderada y positiva
(r = +0,619, n = 1 342): a mayor cilindrada, mayor precio pedido. Este es el
cruce más consistente de los dos, aunque sigue siendo exploratorio por la
cobertura.

![Precio y características del vehículo](figures/03_precio_caracteristicas.png)

### 3.7 Interés y exposición

La mediana de vistas por anuncio es de **12**, con un máximo de 15 821. La
mediana de imágenes es 1 y solo 8 anuncios (0,1 %) están destacados. Estas
variables describen la exposición dentro de la plataforma, no la demanda real:
un anuncio con muchas vistas puede ser simplemente antiguo o estar mal
preciado.

---

## 4. Componente cualitativo: discurso de la oferta y ausencia de entrevistas

### 4.1 Lo que se intentó

El diseño original preveía **30 entrevistas** a personas con relación directa
al mercado (usuarios, vendedores y mecánicos), con consentimiento informado por
escrito. Ese componente **no se completó**.

Al cierre de este informe:

- **0 entrevistas válidas** están registradas en la base de datos del proyecto.
- Existe **1 fila (E01)** en el CSV, pero está **excluida** porque no tiene
  consentimiento firmado.
- Hubo **10 contactos exploratorios** de los que solo se conservan nombres y
  fotos de los vehículos, sin respuestas registradas y sin autorización escrita
  para publicar datos personales.

Por decisión metodológica y ética, esas 10 personas **no se usan**: un nombre y
una foto no constituyen una entrevista, y el permiso verbal para conversar no
autoriza a publicar nombre ni imagen. Incluirlas sería presentar como evidencia
algo que no existe.

Para no dejar el componente vacío, se optó por un **análisis de contenido de
los anuncios**. No sustituye a las entrevistas ni mide la demanda: describe el
discurso público de la oferta. Se hizo en dos pasos:

1. una muestra aleatoria de **200 títulos**, clasificada con seis temas;
2. un contraste con los **9 841 títulos** del dataset, con una taxonomía más
   amplia de ocho temas.

### 4.2 Análisis de una muestra de 200 títulos

Se tomó una muestra aleatoria simple de **200 títulos** de
`anuncios_limpios.csv` (semilla 2026). La muestra quedó compuesta por
**68 bicicletas, 65 motos de combustión, 58 motos eléctricas y 9 patinetas**,
una proporción cercana a la del dataset. Cada título se clasificó con seis
temas: nueva o usada, batería o autonomía, papeles o garantía, motivo de venta,
urgente y negociable. Un título puede recibir más de un tema.

| Tema | Muestra (n = 200) | % muestra | % total (n = 9 841) |
|---|---:|---:|---:|
| Nueva o usada | 17 | 8,5 | 8,6 |
| Batería o autonomía | 11 | 5,5 | 6,5 |
| Papeles o garantía | 3 | 1,5 | 3,2 |
| Motivo de venta | 0 | 0,0 | 0,1 |
| Urgente | 1 | 0,5 | 0,1 |
| Negociable | 1 | 0,5 | 0,4 |

![Temas destacados en una muestra de 200 títulos](figures/08_temas_200_titulos.png)

**El 84,5 % de los títulos (169 de 200) no menciona ninguno de los seis temas.**
Solo el 15,5 % (31) aporta al menos una señal de estado, batería, papeles,
urgencia, negociación o motivo de venta. La proporción es muy cercana a la del
total del dataset (17,3 % con al menos un tema), lo que sugiere que la muestra
reproduce razonablemente el patrón general.

Para interpretar la muestra, conviene mirar cómo se distribuyen esos mismos seis
temas en todo el dataset (n = 9 841; por categoría: 3 146 bicicletas, 3 349 de
combustión, 2 807 eléctricas y 539 patinetas), donde las categorías sí tienen
tamaño suficiente para comparar:

| Tema | Bicicletas | Combustión | Eléctricas | Patinetas |
|---|---:|---:|---:|---:|
| Nueva o usada | 10,3 | 8,4 | 7,7 | 5,4 |
| Batería o autonomía | 0,8 | 1,7 | 16,5 | 17,1 |
| Papeles o garantía | 1,3 | 7,0 | 1,1 | 0,7 |
| Motivo de venta | 0,1 | 0,2 | 0,0 | 0,2 |
| Urgente | 0,1 | 0,0 | 0,1 | 0,0 |
| Negociable | 0,3 | 0,2 | 0,7 | 0,4 |

En el total, los datos muestran tres patrones:

- **La batería y la autonomía son el argumento de las eléctricas y las
  patinetas** (16,5 % y 17,1 %), no de las de combustión (1,7 %) ni de las
  bicicletas (0,8 %).
- **Los papeles y la garantía son el argumento de las motos de combustión**
  (7,0 %), muy por encima de las eléctricas (1,1 %) y las bicicletas (1,3 %).
  Tiene sentido: la documentación y la chapa son más relevantes en un vehículo
  que se registra y se traspasa.
- **El estado o la novedad aparece en todas las categorías**, con más peso en
  bicicletas (10,3 %) y combustión (8,4 %). La urgencia, la negociación y el
  motivo de venta son casi inexistentes en el título: no porque no ocurran,
  sino porque se resuelven en la conversación privada.

Ejemplos textuales reales (8 títulos, limpiados; se conservan erratas):

- **Nueva o usada:** “Bicicletas medida 20 Rali Roky naranja para varón sin
  ruedas de apoyo nuevas en su caja”.
- **Nueva o usada:** “Bicicletas Nuevas de montaña de 24”.
- **Batería o autonomía:** “Vendo moto Aguila sin batería en 450 USD”.
- **Batería o autonomía:** “MOTO AUTOMÁTICA TOPMAQ RAPTOR (kms) 200 CC,
  4 Tiempos, Capacidad 6 L, Autonomia 35 KM/L, alarma [...] CON CHAPA Y
  CERTIFICO”.
- **Papeles o garantía:** “Moto isuki 250cc con chapa y circulacion”.
- **Papeles o garantía:** “El Mejor Onebot Directo a Chapa”.
- **Urgente:** “Súper oferta. Muévete rápido y sin complicaciones con nuestras
  bicicletas. Medidas 20, 24 y 26” (se omitieron emojis).
- **Negociable:** “Bicicleta 26 REBAJA ESPECIAL”.

El segundo ejemplo de batería es un **falso positivo**: es una moto de
combustión que declara consumo (“Autonomía 35 KM/L”), no una batería. El
ejemplo se conserva porque muestra justamente el límite del método: la
clasificación automática por palabras clave no distingue el contexto. Lo mismo
puede ocurrir con “nueva”, que a veces califica a la batería y no al vehículo.

### 4.3 Contraste con los 9 841 títulos

Para comprobar que el patrón no es un artefacto de la muestra, se clasificaron
los **9 841 títulos** con una taxonomía más amplia de ocho temas: estado o
novedad, especificaciones técnicas, garantía o papeles, precio u oferta, uso o
destinatario, urgencia o motivo de venta, contacto o ubicación, y accesorios.

| Tema | Anuncios | % |
|---|---:|---:|
| Especificaciones técnicas | 2 171 | 22,1 |
| Estado o novedad | 1 614 | 16,4 |
| Precio, oferta o negociación | 665 | 6,8 |
| Uso, trabajo o destinatario | 540 | 5,5 |
| Urgencia o motivo de venta | 458 | 4,7 |
| Garantía, papeles o trámites | 160 | 1,6 |
| Accesorios o extras | 132 | 1,3 |
| Contacto o ubicación | 122 | 1,2 |

Con esta taxonomía, **5 316 títulos (54,0 %)** no mencionan ninguno de los ocho
temas; el 46,0 % restante aporta algún elemento. La diferencia con el 84,5 % de
la muestra no es una contradicción: la taxonomía amplia incluye
especificaciones técnicas, uso, precio, contacto y accesorios, que son más
frecuentes que los motivos de venta o la negociación. Las dos lecturas apuntan
en la misma dirección: **el título se usa para describir el vehículo, no para
explicar la operación**.

![Temas mencionados en los títulos de los anuncios](figures/07_temas_anuncios.png)

El contraste también revela diferencias por categoría:

- En motos de combustión, el **44,1 %** de los títulos menciona
  especificaciones técnicas (cilindrada, potencia, voltaje), frente al
  **19,5 %** en eléctricas y apenas el **1,4 %** en bicicletas.
- En bicicletas domina el **uso o destinatario** (**15,2 %**): “para niños”,
  “de montaña”, “de mujer”.
- En eléctricas y de combustión el acento está en el **estado o novedad**
  (**19,9 %** y **19,8 %**), con el año 2026 como señal de estreno.
- La **garantía y los papeles** aparecen solo en el **1,6 %** de los títulos,
  aunque en motos de combustión suben al **2,7 %**.

### 4.4 Limitación del componente cualitativo

**Consecuencia:** este informe describe la **oferta** (precios pedidos y
discurso de los anuncios), no la **demanda** ni la experiencia de los
compradores. No responde cuánto se pagó realmente, qué problemas enfrentan los
dueños, por qué eligen una eléctrica o cómo afectan los repuestos y los
trámites. Esas preguntas quedan abiertas para una segunda fase. El análisis de
contenido de 200 títulos y el contraste con los 9 841 permiten describir el
discurso de la oferta, pero no reemplazan la voz de los actores.

---

## 5. Discusión

### 5.1 Lo que sí dicen los datos

Los anuncios permiten afirmar tres cosas con razonable solidez descriptiva:

1. **El mercado relevante se cotiza en USD.** El 97,4 % de los anuncios con
   moneda usa dólares. Esto segmenta la demanda y hace que el precio sea
   sensible al tipo de cambio y a la disponibilidad de divisas.
2. **La moto de combustión es el segmento más caro y la bicicleta el más
   barato.** La diferencia de medianas (2 200 vs. 160 USD) es de más de diez
   veces.
3. **La eléctrica ocupa un espacio intermedio**, con mediana de 1 485 USD y
   alta dispersión. Es la puerta de entrada motorizada más accesible, pero su
   costo total depende de batería, carga y repuestos, variables que los
   anuncios no capturan.

### 5.2 Lo que no se puede concluir

- **No son precios de transacción.** Son precios pedidos; el precio final
  puede ser menor tras la negociación.
- **No es una muestra representativa.** Revolico concentra La Habana y a
  quienes tienen acceso a internet y a divisas.
- **La categorización tiene ruido.** Las patinetas incluyen carriolas,
  scooters infantiles y sets de protección; las bicicletas mezclan infantiles y
  de adulto. El filtro redujo el ruido, no lo eliminó.
- **La cobertura de marca, año y cilindrada es baja.** Los cruces con esas
  variables son indicativos, no concluyentes.
- **No hay entrevistas.** El análisis de contenido de los títulos (200 títulos
  y el contraste con los 9 841) describe el discurso de la oferta, pero no
  permite triangular con la experiencia de los actores.

### 5.3 Comparación con la hipótesis de partida

La hipótesis era que la moto eléctrica sería más barata que la de combustión y
que tendría mayor dispersión. Ambas cosas se cumplen en los datos: 1 485 vs.
2 200 USD de mediana y desviación típica de 3 117 vs. 2 257. La dirección es
correcta, pero el anuncio no permite explicar el mecanismo (autonomía, batería,
procedencia, repuestos). Esa explicación exigía las entrevistas que no se
pudieron hacer.

---

## 6. Limitaciones

1. **Muestra no probabilística y concentrada.** 94,8 % de los anuncios son de
   La Habana. No se pueden estimar proporciones poblacionales.
2. **Precios pedidos, no pagados.** El sesgo de negociación no se puede
   cuantificar con esta fuente.
3. **Cobertura incompleta de variables derivadas.** Marca 31,3 %, año 8,4 %,
   cilindrada 13,6 %.
4. **Ruido de categorización.** Especialmente en patinetas y bicicletas.
5. **Sin entrevistas válidas.** El diseño mixto no se completó. Se compensó
   con un análisis de contenido de una muestra de 200 títulos y un contraste
   con los 9 841, que describe la oferta pero no recoge la experiencia de
   compradores ni vendedores.
6. **Una sola captura temporal.** No hay serie temporal; no se puede hablar de
   tendencia.
7. **Monedas no convertidas.** Los 251 anuncios en CUP y el de MLC quedan
   fuera de los cruces de precio.

---

## 7. Conclusiones

El mercado de vehículos ligeros que se anuncia en Revolico es un mercado
**dolarizado, capitalino y segmentado por categoría**. Las motos de combustión
se cotizan alrededor de **2 200 USD**, las eléctricas alrededor de **1 485
USD**, las patinetas en **720 USD** y las bicicletas en **160 USD**. La
eléctrica es la opción motorizada más barata, pero también la más heterogénea.

La base construida —9 841 anuncios limpios y reproducibles— es un insumo útil
para describir la oferta y para diseñar una segunda fase. No sustituye el
trabajo de campo: sin entrevistas válidas no se puede explicar por qué los
precios son esos, cómo se negocian ni qué problemas enfrentan los usuarios.

La limitación principal de esta entrega es explícita: **no se completaron las
30 entrevistas**. Se prefirió declararlo antes que rellenar el informe con
datos no verificados. El análisis de contenido de los anuncios (200 títulos y
el contraste con los 9 841) permite describir el discurso de la oferta, pero no
sustituye la experiencia de los actores. La recomendación es completar el
componente cualitativo en una segunda fase y, mientras tanto, usar este
documento como línea base cuantitativa.

---

## 8. Recomendaciones

1. **Completar el campo** con 30 entrevistas cortas (5–7 minutos), con
   consentimiento escrito y cuotas por perfil.
2. **Repetir la captura** en 3–6 meses para construir una serie temporal.
3. **Mejorar la extracción de marca y año** con reglas más finas o revisión
   manual de una submuestra.
4. **Documentar una tasa CUP/USD** para incorporar los anuncios en pesos.
5. **Separar patinetas y bicicletas infantiles** en la categorización.
6. **Ampliar el análisis de contenido** a los cuerpos de los anuncios y a una
   segunda muestra, para reducir los falsos positivos de la clasificación
   automática.

---

## 9. Referencias

- Revolico. Anuncios de motos, bicicletas y patinetas. Captura del 4 de
  noviembre de 2026. https://www.revolico.com
- Documentación interna del proyecto: `docs/HANDOFF.md`,
  `docs/ENTREVISTAS.md`, `docs/PROTOCOLO_TRABAJO_CAMPO.md`.
- Código de recolección, limpieza y análisis: `src/`.
- Análisis de contenido de los anuncios: `reports/analisis_200_titulos.txt`,
  `reports/analisis_temas.txt` y `reports/figures/08_temas_200_titulos.png`.
- Cuadernos de análisis: `notebooks/02_limpieza.ipynb`,
  `notebooks/03_eda.ipynb`.

---

## Anexos {: style="page-break-before: always;" }

### Anexo A. Figuras adicionales

Los comandos para reproducir la base, las figuras y el informe están en
`README.md` y en `docs/HANDOFF.md`.

![Anuncios por categoría](figures/fig01_anuncios_categoria.png)

![Anuncios por provincia](figures/fig02_provincia.png)

![Precio por categoría](figures/fig03_precio_categoria.png)

![Histograma de precios](figures/fig04_precio_histograma.png)
