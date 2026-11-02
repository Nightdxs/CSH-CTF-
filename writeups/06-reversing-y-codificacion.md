# Inti Glyph y Chasqui Relay: recuperar el dato, no adivinarlo

[← Volver al índice](../README.md)

Para estos dos retos conservaba archivos suficientes como para volver a comprobar la extracción. Los scripts incluidos no necesitan un servicio remoto y producen los mismos valores que aparecían en el historial.

## Inti Glyph: dos XOR antes y después de la comparación

El análisis de `inti_glyph` llevó a una comparación con `strcmp`. Antes se transformaban diez bytes mediante XOR con `0x4f`. Si la palabra coincidía, otra región de 69 bytes se transformaba con XOR `0x5a` para imprimir la flag.

En el archivo original, las regiones estaban en los offsets de archivo `0x20a0:0x20aa` y `0x20c0:0x2105`. No deben confundirse esos offsets con direcciones virtuales de un proceso.

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

El repositorio conserva únicamente esas regiones codificadas en [un JSON](../scripts/datos/inti-glyph.json), junto con un [decodificador](../scripts/inti_glyph_decode.py). Así se puede comprobar la operación sin distribuir un ejecutable ni introducir en el script la respuesta ya descifrada.

El aprendizaje fue seguir la transformación que hace el programa. Una cadena que no aparece legible con `strings` puede seguir estando almacenada de forma recuperable. En este reto, la comparación y los dos bucles XOR explicaban tanto la palabra de entrada como la salida.

## Chasqui Relay: usar el codificador como especificación

El paquete de Chasqui incluía `encoder.sv` y `dump.txt`. El primero describía un codificador Hamming (7,4): cuatro bits de datos se convertían en siete bits mediante tres bits de paridad.

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

Se elige la palabra válida más cercana, con distancia máxima de uno. Después se recupera su nibble de datos y se unen dos nibbles para formar cada byte.

Hamming (7,4) permite corregir un error por palabra bajo ese modelo. El procedimiento no demuestra que nunca existan errores múltiples: sin redundancia adicional, algunos pueden parecer una palabra cercana a otra distinta. En este archivo, el texto obtenido y la coincidencia con la extracción histórica apoyan el resultado.

```bash
python3 scripts/chasqui_decode.py
```

La verificación local produjo:

```text
Correcciones de distancia 1: 83
csh{f4a10c95fa25f3c1de8e033dcaa86ee8cbb6f037f0a7b09df05a9f7b3487b75b}
```

Esto también resolvió un dato suelto de mis notas: esa flag sí podía atribuirse a **Chasqui Relay**. El resumen inicial la conservaba sin reto asignado; volver al archivo y al codificador permitió cerrar la relación.

Los [datos](../scripts/datos/chasqui/) y el [decodificador completo](../scripts/chasqui_decode.py) están incluidos para reproducir la comprobación.
