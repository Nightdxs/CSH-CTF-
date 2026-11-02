# Inti Glyph y Chasqui Relay: recuperar el dato, no adivinarlo

[← Volver al índice](../README.md)

De estos dos retos conservaba los archivos necesarios para repetir la extracción, y los scripts incluidos devuelven los mismos valores que aparecían en el historial sin depender de un servicio remoto.

## Inti Glyph: dos XOR antes y después de la comparación

Al seguir el flujo de `inti_glyph` apareció una comparación con `strcmp`, precedida por un XOR con `0x4f` sobre diez bytes; si la palabra coincidía, el programa aplicaba XOR `0x5a` a otra región de 69 bytes y mostraba la flag.

Las regiones estaban en `0x20a0:0x20aa` y `0x20c0:0x2105`, posiciones dentro del archivo original que había que distinguir de las direcciones virtuales del proceso.

La extracción podía hacerse sin ejecutar el ELF:

```python
from pathlib import Path
b = Path('inti_glyph').read_bytes()
word = bytes(x ^ 0x4f for x in b[0x20a0:0x20aa])
flag = bytes(x ^ 0x5a for x in b[0x20c0:0x2105])
print(word.decode())
print(flag.decode())
```

El resultado fue:

```text
inti_raymi
csh{ca2e96797a399eed614d52fbee389dfc595976b8f502e47161968745457d5c7d}
```

Guardé esas dos regiones codificadas en [un JSON](../scripts/datos/inti-glyph.json) y preparé un [decodificador](../scripts/inti_glyph_decode.py) para poder repetir la operación con los bytes extraídos, sin tener que ejecutar el ELF.

Seguir los dos bucles XOR me permitió entender de dónde salían la palabra y la flag, y ver que una cadena que no aparece legible con `strings` puede seguir guardada en una forma fácil de recuperar.

## Chasqui Relay: usar el codificador como especificación

Con Chasqui venían `encoder.sv` y `dump.txt`, y el primero daba la especificación del Hamming (7,4) usado para convertir cuatro bits de datos en siete con tres bits de paridad.

El orden de salida era:

```text
p0 p1 d3 p2 d2 d1 d0
```

Y las paridades estaban definidas así:

```text
p0 = d3 XOR d2 XOR d0
p1 = d3 XOR d1 XOR d0
p2 = d2 XOR d1 XOR d0
```

En vez de asumir el orden de otra implementación de Hamming, usé esas ecuaciones para construir las 16 palabras válidas. Para cada grupo de siete bits del dump, el decodificador calcula la distancia de Hamming a esas palabras: cuántas posiciones son distintas.

```python
distance = sum(a != b for a, b in zip(received, valid_word))
```

El decodificador elige la palabra válida más cercana con distancia máxima de uno, recupera su nibble de datos y lo une al siguiente para formar cada byte.

Hamming (7,4) permite corregir un error por palabra bajo ese modelo. El procedimiento no demuestra que nunca existan errores múltiples: sin redundancia adicional, algunos pueden parecer una palabra cercana a otra distinta. En este archivo, el texto obtenido y la coincidencia con la extracción histórica apoyan el resultado.

```bash
python3 scripts/chasqui_decode.py
```

La verificación local produjo:

```text
Correcciones de distancia 1: 83
csh{f4a10c95fa25f3c1de8e033dcaa86ee8cbb6f037f0a7b09df05a9f7b3487b75b}
```

Al repetir la extracción también pude atribuir esta flag a **Chasqui Relay**, porque en el primer resumen la había conservado sin un reto asignado.

Los [datos](../scripts/datos/chasqui/) y el [decodificador completo](../scripts/chasqui_decode.py) están incluidos para reproducir la comprobación.
