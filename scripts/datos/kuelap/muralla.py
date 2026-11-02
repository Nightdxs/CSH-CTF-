#!/usr/bin/env python3
"""La muralla de Kuelap: comprueba si una combinacion la abre.

    python3 muralla.py <combinacion>        ; en decimal o 0x...

La combinacion son 40 bits. Esto dice si encaja, y si encaja abre el sello.

--- como esta tallada la piedra -------------------------------------------

Kuelap tiene DOS murallas, la del oeste y la del este, y la entrada es un
pasadizo que las atraviesa las dos. Cada bit de la combinacion talla una
piedra en UNA de las dos murallas: los bits en posicion par van al oeste y los
impares al este.

Las dos piedras resultantes tienen que encajar entre si, que es lo que
comprueba `encaja`.
"""

import hashlib
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BITS = 40
MITAD = BITS // 2


def partir(combinacion: int) -> tuple[int, int]:
    """Los bits pares tallan la muralla oeste; los impares, la este."""
    oeste = este = 0
    for i in range(BITS):
        b = (combinacion >> i) & 1
        if i % 2 == 0:
            oeste |= b << (i // 2)
        else:
            este |= b << (i // 2)
    return oeste, este


def piedra(muralla: bytes, v: int) -> int:
    """La piedra que talla un lado de la combinacion en su muralla."""
    return int.from_bytes(
        hashlib.sha256(muralla + v.to_bytes(MITAD // 8 + 1, "big")).digest()[:8], "big"
    )


def encaja(combinacion: int, objetivo: int) -> bool:
    oeste, este = partir(combinacion)
    return piedra(b"kuelap/oeste|", oeste) ^ piedra(b"kuelap/este|", este) == objetivo


def clave(combinacion: int) -> bytes:
    return hashlib.sha256(b"kuelap/clave|" + combinacion.to_bytes(5, "big")).digest()


def abrir(combinacion: int, nonce: bytes, ct: bytes) -> bytes:
    return AESGCM(clave(combinacion)).decrypt(nonce, ct, b"kuelap")


def leer(ruta: str):
    """(objetivo, nonce, ct) de muralla.txt."""
    objetivo = nonce = ct = None
    for cruda in Path(ruta).read_text().splitlines():
        linea = cruda.split(";", 1)[0].strip()
        if not linea:
            continue
        cab, valor = linea.split(None, 1)
        if cab.upper() == "ENCAJE":
            objetivo = int(valor, 16)
        elif cab.upper() == "SELLO":
            a, b = valor.split()
            nonce, ct = bytes.fromhex(a), bytes.fromhex(b)
    if objetivo is None or nonce is None:
        raise SystemExit(f"{ruta}: faltan ENCAJE o SELLO")
    return objetivo, nonce, ct


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("uso: muralla.py <combinacion> [muralla.txt]")
    combinacion = int(sys.argv[1], 0)
    ruta = sys.argv[2] if len(sys.argv) > 2 else "muralla.txt"
    objetivo, nonce, ct = leer(ruta)
    if not encaja(combinacion, objetivo):
        print("no encaja")
        raise SystemExit(1)
    print(abrir(combinacion, nonce, ct).decode())


if __name__ == "__main__":
    main()
