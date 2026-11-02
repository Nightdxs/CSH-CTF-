# Scripts del writeup

[← Volver al índice](../README.md)

## Comprobaciones locales

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
python3 scripts/chasqui_decode.py
python3 scripts/inti_glyph_decode.py
python3 scripts/kuelap_solve.py
```

Chasqui e Inti Glyph usan solo la biblioteca estándar. Kuélap necesita `cryptography`. Los archivos de `datos/chasqui` y `datos/kuelap` proceden de los paquetes del reto; `inti-glyph.json` contiene las regiones codificadas extraídas del ELF original. Los decodificadores se prepararon al escribir el artículo y se comprobaron contra los resultados históricos.

## Exploits recuperados

| Archivo | Función | Configuración |
|---|---|---|
| `pachamama_nosqli.py` | Extraer mediante `$regex` | URL como primer argumento |
| `mallku_sqli.py` | Extraer mediante condiciones SQL booleanas | URL como primer argumento |
| `inti_vault_exploit.py` | Ret2win con dos argumentos | Ajustar `HOST, PORT` |
| `apu_exploit.py` | Cuatro escrituras `%hhn` | Ajustar `HOST, PORT`; offset opcional como argumento |
| `wiracocha_exploit.py` | Leak de libc y ret2libc | Ajustar `HOST, PORT` |
| `chavin_exploit.py` | Carrera UAF y solapamiento | Host y puerto como argumentos; offsets originales del reto |
| `ayni_exploit.sh` | Actualización de rol y nuevo login | URL como primer argumento |
| `kuska_exploit.sh` | Confirmación de pago sin firma | URL como primer argumento |
| `void_exploit.sh` | UNION en búsqueda del archivo | URL como primer argumento |
| `yaku_exploit.sh` | Cambio de email y resolución de identidad | URL como primer argumento |

Los destinos predeterminados de los scripts apuntan a localhost. Son scripts históricos de laboratorio: los offsets, prompts y estructura de las respuestas dependen de las instancias originales. No se ejecutaron de nuevo contra servicios remotos durante la preparación del repositorio. Las cuatro rutas web de Ayni, Kuska, Void y Yaku tienen análisis de fuente, pero no una flag remota recuperada en esta revisión.
