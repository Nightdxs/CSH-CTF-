#!/usr/bin/env python3
"""Decodifica el Hamming (7,4) de Chasqui sin dependencias externas."""
from pathlib import Path
import sys

def encode(n):
    d3, d2, d1, d0 = ((n >> k) & 1 for k in (3, 2, 1, 0))
    return ''.join(map(str, (d3^d2^d0, d3^d1^d0, d3, d2^d1^d0, d2, d1, d0)))

def decode(bits):
    if len(bits) % 14:
        raise ValueError('El flujo no contiene un número entero de bytes codificados')
    codebook = [encode(n) for n in range(16)]
    nibbles, corrected = [], 0
    for pos in range(0, len(bits), 7):
        word = bits[pos:pos+7]
        distances = [sum(a != b for a, b in zip(word, code)) for code in codebook]
        minimum = min(distances)
        if minimum > 1 or distances.count(minimum) != 1:
            raise ValueError(f'Palabra no corregible en {pos}')
        corrected += minimum
        nibbles.append(distances.index(minimum))
    return bytes((a << 4) | b for a, b in zip(nibbles[::2], nibbles[1::2])), corrected

if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'datos/chasqui/dump.txt'
    bits = ''.join(path.read_text().split())
    if set(bits) - {'0','1'}:
        raise ValueError('Se esperaban solo bits')
    message, corrected = decode(bits)
    print(f'Correcciones de distancia 1: {corrected}')
    print(message.decode())
