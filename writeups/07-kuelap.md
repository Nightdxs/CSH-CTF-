# Kuélap: dos búsquedas de 20 bits

[← Volver al índice](../README.md)

En las notas anteriores tenía una combinación y una flag atribuidas a Kuélap, pero faltaba la deducción. Recuperar `muralla.py` y `muralla.txt` permitió reconstruir el método y volver a comprobar el descifrado.

## La separación ya estaba en el verificador

El programa recibe una combinación de 40 bits y la divide en dos valores: los bits de posición par forman `oeste` y los impares forman `este`. Cada mitad tiene 20 bits.

Para decidir si la combinación encaja, calcula:

```python
piedra(b'kuelap/oeste|', oeste) ^ piedra(b'kuelap/este|', este) == objetivo
```

`piedra` aplica SHA-256 al prefijo del lado y al valor representado en tres bytes big-endian, y conserva los primeros ocho bytes del hash. El archivo de datos fija el objetivo:

```text
a43013fbb0c57bc0
```

Probar directamente todas las combinaciones significa recorrer hasta `2^40` candidatos. Pero la comprobación se puede reorganizar:

```text
piedra(oeste) = objetivo XOR piedra(este)
```

## Guardar una mitad y buscar la otra

La solución usa meet in the middle:

1. Calcular las `2^20` posibilidades del oeste y guardarlas en una tabla por el valor de `piedra`.
2. Recorrer las `2^20` posibilidades del este.
3. Para cada una, buscar `objetivo XOR piedra(este)` en la tabla.
4. Si hay coincidencia, volver a intercalar los bits de ambos lados.

El trabajo pasa de una búsqueda de `2^40` a dos recorridos de `2^20`, a cambio de memoria para la tabla. SHA-256 no se invierte: la debilidad aprovechada es la estructura separable de la condición y el tamaño de cada mitad.

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

Aquí la autenticación de GCM es una comprobación adicional: con una clave, nonce, ciphertext o AAD equivocados, la operación no debe devolver un mensaje válido. Eso da más confianza que limitarse a encontrar una cadena que «parezca» una flag.

Los [archivos del reto necesarios](../scripts/datos/kuelap/) y el solver están incluidos. Esta reconstrucción del método y su ejecución se hicieron al preparar el writeup; no afirmo que el script de publicación sea el mismo que se usó durante la competencia.
