#!/usr/bin/env python3
"""Meet in the middle: dos espacios de 20 bits para la combinación de Kuélap."""
import importlib.util
from pathlib import Path
p=Path(__file__).parent/'datos/kuelap'
spec=importlib.util.spec_from_file_location('muralla',p/'muralla.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
obj,nonce,ct=m.leer(str(p/'muralla.txt'))
left={m.piedra(b'kuelap/oeste|',v):v for v in range(1<<20)}
for east in range(1<<20):
    west=left.get(obj ^ m.piedra(b'kuelap/este|',east))
    if west is None:
        continue
    combination=sum(((west>>i)&1)<<(2*i) | ((east>>i)&1)<<(2*i+1) for i in range(20))
    assert m.encaja(combination,obj)
    print('Combinación:',hex(combination))
    print(m.abrir(combination,nonce,ct).decode())
    break
else:
    raise SystemExit('No hay combinación')
