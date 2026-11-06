# Criterios de relevancia

El scraper recorre categorías que pueden contener anuncios ajenos al tema:
repuestos, accesorios, gasolina, otros vehículos o electrodomésticos. Antes de
analizar, separamos los anuncios relacionados.

## Alcance del proyecto

El mercado analizado son **solo motos, bicicletas y patinetas**. Cualquier otro
vehículo que aparezca en las mismas categorías se descarta como *fuera de
alcance* y no forma parte del dataset ni del análisis.

## Clasificación

Cada anuncio recibe uno de tres valores en la columna `relevante`:

| Valor | Significado | Acción |
|---|---|---|
| `si` | Relacionado con motos, bicicletas o patinetas | Pasa al dataset de análisis |
| `revisar` | Ambiguo: producto con posible ruido o título poco claro | Revisión manual |
| `no` | Fuera de alcance o claramente ajeno | Se excluye |

## Palabras de producto

- **Moto:** moto, motocicleta, motoneta, motico, bimoto, bicimoto, velomotor,
  ciclomotor, scooter, marcas conocidas.
- **Bicicleta:** bici, bicicleta, rodada, MTB, BMX, montaña, ruta, fixie,
  urbana, paseo, infantil, marcas conocidas.
- **Patineta:** patineta, patinete, scooter, skate, longboard, monopatin.

El filtro acepta plurales simples (`moto`/`motos`, `rin`/`rines`) y algunas
variantes ortográficas frecuentes (`trisiclo`, `motico`, `bicimoto`).

## Ruido fuerte

Describe otro producto y basta para excluir: repuesto, lavadora, nevera, aire
acondicionado, planta, generador, inversor, extractor, adorno, juguete, camión,
tráiler, carreta.

## Ruido contextual

Puede ser una característica del vehículo o el nombre de una pieza. Solo cuenta
como ruido cuando el título **no nombra** el vehículo o cuando abre el título:

gasolina, batería, motor, aceite, lubricante, bujía, carburador, escape, espejo,
cubierta, llanta, rin, aro, rayo, cadena, freno, sillín, manubrio, horquilla,
amortiguador, casco, accesorio, pieza, carro, auto, pila, cargador, luz, bocina,
mppt, controlador, cable, goma, cámara, pedal, timbre, asiento, forro, guantilla,
candado, triplato, biela, pedalier, piñón, cassette, desviador.

Ejemplo: `Moto de gasolina` es una moto; `Gasolina B87` es combustible.

## Reglas, en orden

1. Si el título menciona un vehículo fuera de alcance → `no`.
2. Si dice `para moto`, `para bicicleta`, etc. y además menciona una pieza →
   `revisar` (probable accesorio).
3. Si el título **empieza** por una pieza y no nombra un vehículo
   (`Batería 12V`, `Motor 150cc`) → `no`.
4. Si hay ruido fuerte → `no`, salvo que el título nombre un vehículo, en cuyo
   caso → `revisar`.
5. Si el título nombra un vehículo → `si`. Si la categoría no coincide con el
   producto, se conserva y se anota la contaminación en `motivo`.
6. Si no hay producto explícito pero sí ruido contextual → `revisar`.
7. En `patinetas`, sin palabra clave → `revisar`.
8. En el resto, la categoría específica manda → `si`.

### Caso especial: `motor`

En Cuba `motor` también significa moto. Si la categoría es de motos y el título
empieza por `motor` con cilindrada (`Motor 150cc`) o marca (`Motor Krathos`),
se trata como moto. Si solo dice `Motor`, va a `revisar`.

## Salidas

- `data/processed/anuncios_relacionados.csv`: todos los `si`.
- `data/processed/anuncios_relacionados_unicos.csv`: `si` sin duplicados por
  `id` ni por título+precio+municipio.
- `data/processed/anuncios_revisar.csv`: los ambiguos.
- `data/processed/anuncios_excluidos.csv`: los `no`, con el motivo.
- `reports/relevancia_resumen.txt`: conteos y ejemplos.

## Ajuste

Los diccionarios viven en `src/relevancia.py`. Si al revisar los ejemplos ves
falsos positivos o falsos negativos, añade o quita palabras y vuelve a ejecutar:

```bash
python -m src.relevancia
```

## Advertencia

Es un filtro heurístico, no un clasificador perfecto. Por eso existe la categoría
`revisar`: sirve para auditar el filtro y documentar sus límites en el informe.
Un vehículo fuera de alcance que no se nombre en el título puede colarse; se
documenta como limitación.
