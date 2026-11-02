# Evidencias y reproducción

[← Volver al índice](../README.md)

## Qué se volvió a comprobar

| Reto | Material comprobado | Resultado |
|---|---|---|
| Chasqui Relay | `encoder.sv`, `dump.txt` y decodificador | 83 palabras a distancia 1; flag idéntica al registro histórico |
| Inti Glyph | Dos regiones XOR del ELF y decodificador | `inti_raymi` y flag coincidente |
| Kuélap | `muralla.py`, `muralla.txt` y solver | Combinación `0x9486e1b5e6`; condición satisfecha y descifrado AES-GCM autenticado |

Los scripts Python se revisaron sintácticamente y los scripts shell con `bash -n`. También se comprobaron los enlaces locales del Markdown y la presencia de las imágenes referenciadas. No se volvieron a ejecutar los exploits remotos.

## De dónde proceden los resultados históricos

- Pachamama, Mallku, Amaru, Apu, Wiracocha, Kotosh, Pachacámac, Ollanta y Pisac: capturas de terminal aportadas por el participante, con apoyo de los scripts cuando se conservan.
- Inti Vault y Chavín: salida de terminal y explicación recuperadas de las transcripciones de Claude, contrastadas con los scripts guardados.
- Ayni, Kuska, Void y Yaku: código de los paquetes del reto, transcripción y scripts. No se recuperó una salida remota con flag para cada uno.
- Resultado general: captura del marcador final. `44` es la cifra individual; `50/53` corresponde al conjunto de participantes.

La captura de Amaru con datos de sesión se excluye de la publicación; sus valores se sustituyen por marcadores en el texto. Las demás imágenes de `assets/` son copias de las aportadas, con nombres más claros y sin regenerar su contenido. `imagenes.sha256` permite comprobar su integridad. Que una flag aparezca en una terminal no demuestra por sí solo que se enviara y aceptara en la plataforma; el repositorio no hace esa atribución individual.

## Decisiones de edición

Los artículos reconstruyen los pasos con respaldo documental. No se publican conversaciones completas ni archivos ajenos al CTF. Los nombres de los retos de Linux se basan en los hostnames visibles cuando falta la ficha oficial. Los solvers creados para esta publicación se identifican como tales. Las diferencias entre una flag local de prueba y un resultado remoto se conservan, especialmente en Chavín.

Los materiales de ejemplo originales incluidos pertenecen al reto CSH CON CTF 2026 y se usan para explicar su solución. Los textos y scripts de la sesión se comparten como portafolio educativo; no se asigna una licencia nueva a los archivos de terceros.
