# Kuélap: dos búsquedas de 20 bits

[← Volver al índice](../README.md)

De Kuélap tenía anotadas una combinación y una flag, pero al recuperar `muralla.py` y `muralla.txt` pude reconstruir cómo obtenerlas y repetir la comprobación del descifrado.

## La separación ya estaba en el verificador

El programa separa los 40 bits de la combinación entre `oeste` y `este`, poniendo las posiciones pares en un lado y las impares en el otro, de modo que cada mitad queda con 20 bits.

Para decidir si la combinación encaja, calcula:

```python
piedra(b'kuelap/oeste|', oeste) ^ piedra(b'kuelap/este|', este) == objetivo
```

`piedra` aplica SHA-256 al prefijo del lado y al valor representado en tres bytes big-endian, y conserva los primeros ocho bytes del hash. El archivo de datos fija el objetivo:

```text
a43013fbb0c57bc0
```

Recorrer las combinaciones una a una llevaría hasta `2^40` candidatos, pero la forma de la comprobación permitía reorganizarla así:

```text
piedra(oeste) = objetivo XOR piedra(este)
```

## Guardar una mitad y buscar la otra

La solución usa meet in the middle:

1. Calcular las `2^20` posibilidades del oeste y guardarlas en una tabla por el valor de `piedra`.
2. Recorrer las `2^20` posibilidades del este.
3. Para cada una, buscar `objetivo XOR piedra(este)` en la tabla.
4. Si hay coincidencia, volver a intercalar los bits de ambos lados.

Al guardar una mitad en una tabla, el trabajo se reduce a dos recorridos de `2^20`, aprovechando que la condición se puede separar y que cada lado es pequeño, a cambio de usar memoria para las entradas.

El núcleo del [solver](../scripts/kuelap_solve.py) es:

```python
left = {piedra(b'kuelap/oeste|', x): x for x in range(1 << 20)}
for east in range(1 << 20):
    west = left.get(objetivo ^ piedra(b'kuelap/este|', east))
    if west is not None:
        # Intercalar bits pares e impares y comprobar el sello.
        ...
```

Para cada posición `i`, el bit `i` del oeste vuelve a `2*i` y el del este a `2*i+1`. El programa recuperó:

```text
0x9486e1b5e6
```

## Comprobar la combinación con el sello

El verificador deriva la clave así:

```python
sha256(b'kuelap/clave|' + combinacion.to_bytes(5, 'big')).digest()
```

La clave abre un sello AES-GCM con el nonce y el ciphertext de `muralla.txt`, usando `b'kuelap'` como datos autenticados adicionales. El resultado de la nueva comprobación fue:

```text
csh{20fd986e8befbf2e55e838946dbf5ea70f32fd450b050bc5533c4cc932b24c21}
```

La comprobación de GCM ayudó a confirmar el resultado, porque un error en la clave, el nonce, el ciphertext o el AAD haría fallar la autenticación en vez de devolver un mensaje válido.

Dejé los [archivos necesarios](../scripts/datos/kuelap/) junto con el solver para repetir este recorrido, que reconstruí y comprobé al preparar el writeup a partir de los datos originales.
