#!/usr/bin/env python3
"""Lee las regiones XOR extraídas de inti_glyph, sin ejecutar el ELF."""
from pathlib import Path
import json
p = json.loads((Path(__file__).parent/'datos/inti-glyph.json').read_text())
print('Palabra:', bytes(b ^ 0x4f for b in bytes.fromhex(p['word_xor_4f'])).decode())
print('Flag:', bytes(b ^ 0x5a for b in bytes.fromhex(p['flag_xor_5a'])).decode())
