# CSH CON CTF 2026 · Lo que aprendí resolviendo retos

**Jhon Paul Mejia Quispe · NIGHTMAR3 · Universidad Nacional de Ingeniería**

El 30 de octubre participé en el CTF de CSH CON, organizado por Cyber Security Hub de UTEC, donde terminé en **tercer lugar con 44 retos y 11 438 puntos**, usando el alias NIGHTMAR3 y representando a la UNI.

Después de la competencia me puse a ordenar los comandos, las capturas y los scripts que había guardado para explicar cómo fui avanzando en los retos, desde las primeras pruebas hasta los detalles que hicieron funcionar cada solución. Dejé también los intentos que quedaron a medias, porque volver sobre los errores me ayudó a entender cosas que durante el CTF había pasado por alto.

![Marcador final de CSH CON CTF 2026: tercer puesto de NIGHTMAR3](assets/resultados.jpg)

## Por dónde empezar

| Si te interesa… | Lectura recomendada | Lo que se trabaja |
|---|---|---|
| Seguridad web | [Pachamama, Mallku y Amaru](writeups/01-web.md) | Inyección NoSQL, SQLi booleana y exposición de tokens |
| Análisis de código web | [Ayni, Kuska, Void y Yaku](writeups/02-codigo-web.md) | Asignación masiva, firmas opcionales y autorización |
| Explotación de binarios | [Inti Vault, Apu y Wiracocha](writeups/03-pwn.md) | Convención de llamadas, format strings, GOT y ret2libc |
| Depuración de un exploit | [Chavín](writeups/04-chavin.md) | Carreras, use-after-free, safe-linking y diferencias entre entornos |
| Administración de Linux | [Kotosh, Pachacámac, Ollanta y Pisac](writeups/05-linux.md) | Logs, servicios, configuración y tareas programadas |
| Reversing y codificación | [Inti Glyph y Chasqui Relay](writeups/06-reversing-y-codificacion.md) | XOR, lectura de un ELF y corrección Hamming (7,4) |
| Criptografía | [Kuélap](writeups/07-kuelap.md) | Meet in the middle y verificación AES-GCM |

Por ahora reuní **14 soluciones reconstruidas y 4 análisis adicionales de código web**, una parte de los 44 retos del marcador para la que pude recuperar suficiente material. Los agrupé por los temas que trabajé en cada uno para que sea más fácil elegir por dónde empezar.

## Lo que más trabajé

- **Razonamiento a partir de respuestas:** convertir errores SQL, diferencias de autenticación o una lista vacía en pruebas concretas.
- **Lectura de código y ensamblador:** seguir cómo llega una entrada a una consulta, una variable de rol o una dirección de retorno.
- **Automatización:** escribir oráculos de extracción y decodificadores que evitan repetir tareas a mano.
- **Depuración:** distinguir un problema de parseo, de sincronización, de alineación o de offsets antes de cambiar todo el exploit.
- **Documentación técnica:** explicar tanto el resultado como la evidencia que lo sostiene.

## Scripts y reproducción

En [scripts](scripts/README.md) están los **13 archivos de código**, los datos de ejemplo y las indicaciones de uso; para esta publicación volví a comprobar Chasqui, Inti Glyph y Kuélap, así que esas tres soluciones se pueden reproducir sin conectarse a ninguna instancia.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/chasqui_decode.py
python3 scripts/inti_glyph_decode.py
python3 scripts/kuelap_solve.py
```

Para los exploits remotos hace falta el binario y el entorno correspondientes, por eso dejé explicado qué pude volver a comprobar en [reproducción y evidencias](docs/VERIFICACION.md), además de un [índice de herramientas y archivos](docs/HERRAMIENTAS.md).

## Sobre esta reconstrucción

Preparé el writeup después de la competencia a partir de mis notas, archivos, capturas y conversaciones con ChatGPT/Codex y Claude, que también me ayudaron a organizar la explicación y las comprobaciones. Las salidas que incluyo vienen de esos registros o de las verificaciones locales indicadas; aunque las capturas muestran las flags obtenidas, no guardé la pantalla de aceptación de cada envío.

Las capturas conservan su resolución original para poder abrirlas y leer los comandos con calma, mientras que los materiales usados como datos de ejemplo mantienen su atribución a CSH CON CTF 2026.

También dejé [notas de los retos pendientes](docs/NOTAS-PENDIENTES.md) y un [texto para compartir el proyecto en LinkedIn](docs/LINKEDIN.md).

**Evento:** [CSH CON CTF 2026](https://conf.csh.org.pe/ctf) · **Perfil:** [Nightdxs](https://github.com/Nightdxs)
