# Herramientas y archivos utilizados

[← Volver al índice](../README.md)

Reuní aquí los códigos y las herramientas que aparecen en los artículos para que sea fácil relacionar cada uno con lo que resolvía. Los 13 scripts de las capturas de mi carpeta local están incluidos en GitHub dentro de [scripts/](../scripts/), junto con sus datos de ejemplo y las indicaciones de uso.

## Los 13 códigos

| Archivo | Reto o uso |
|---|---|
| [apu_exploit.py](../scripts/apu_exploit.py) | Escrituras de un byte con format strings en Apu Whisper |
| [ayni_exploit.sh](../scripts/ayni_exploit.sh) | Actualización del rol y nuevo login en Ayni Records |
| [chasqui_decode.py](../scripts/chasqui_decode.py) | Decodificar y corregir las palabras Hamming de Chasqui Relay |
| [chavin_exploit.py](../scripts/chavin_exploit.py) | Carreras UAF, fugas y solapamiento en Chavín |
| [inti_glyph_decode.py](../scripts/inti_glyph_decode.py) | Recuperar palabra y flag a partir de las regiones XOR |
| [inti_vault_exploit.py](../scripts/inti_vault_exploit.py) | Preparar los argumentos de solar_keys con una cadena ROP |
| [kuelap_solve.py](../scripts/kuelap_solve.py) | Meet in the middle y comprobación del sello de Kuélap |
| [kuska_exploit.sh](../scripts/kuska_exploit.sh) | Recorrido del webhook de pago sin firma en Kuska Pay |
| [mallku_sqli.py](../scripts/mallku_sqli.py) | Extracción booleana mediante búsqueda binaria |
| [pachamama_nosqli.py](../scripts/pachamama_nosqli.py) | Extracción por prefijos con el operador regex |
| [void_exploit.sh](../scripts/void_exploit.sh) | Consulta UNION en la búsqueda de Void Ledger |
| [wiracocha_exploit.py](../scripts/wiracocha_exploit.py) | Fuga de libc, recepción con buffer y ret2libc |
| [yaku_exploit.sh](../scripts/yaku_exploit.sh) | Cambio de email y resolución de identidad en Yaku Register |

Los scripts de Ayni, Kuska, Void y Yaku acompañan el análisis del código, mientras que las limitaciones de reproducción y las comprobaciones de los demás están detalladas en [VERIFICACION.md](VERIFICACION.md).

## Herramientas que aparecen en el recorrido

| Herramienta | Para qué se utilizó |
|---|---|
| Python 3 | Automatizar peticiones, construir payloads y decodificar datos |
| Bash y curl | Preparar peticiones HTTP, guardar cookies y comparar respuestas |
| SSH y netcat | Entrar a las instancias y comunicarse con los servicios del laboratorio |
| grep, cat, ls y ps | Localizar fragmentos y configuraciones, leer archivos y revisar procesos |
| netstat | Listar puertos en una instancia donde ss no estaba disponible |
| crontab | Revisar y modificar la tarea programada documentada en Pisac |
| groundctl | Gestionar los servicios del laboratorio de Ollanta |
| base64 | Decodificar los fragmentos concatenados de Kotosh |
| objdump y strings | Apoyar el análisis de los binarios y sus cadenas |
| struct y socket, de Python | Empaquetar direcciones y manejar las conexiones de los exploits |
| urllib, json y re, de Python | Enviar solicitudes, preparar JSON y escapar expresiones regulares |
| hashlib y cryptography | Calcular hashes y verificar el descifrado AES-GCM de Kuélap |
| venv y pip | Preparar el entorno para repetir los decodificadores publicados |

También utilicé ChatGPT/Codex y Claude como apoyo durante el trabajo y la preparación de este material, contrastando las explicaciones con las salidas y los archivos que pude conservar.

## Datos y capturas

En [scripts/datos](../scripts/datos/) están el dump y el codificador de Chasqui, el verificador y el sello de Kuélap, y las dos regiones codificadas de Inti Glyph; en [assets](../assets/) están las capturas publicadas que acompañan las explicaciones. Los archivos y ensayos que todavía no permiten cerrar una solución se describen en [las notas pendientes](NOTAS-PENDIENTES.md).
