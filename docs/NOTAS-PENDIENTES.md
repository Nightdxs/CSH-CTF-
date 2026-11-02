# Lo recuperado que todavía no permite cerrar un artículo

[← Volver al índice](../README.md)

Estas notas conservan información útil del trabajo sin convertirla en una solución demostrada. La tabla no es una lista de retos aceptados por la plataforma.

| Reto o referencia | Qué se conserva | Qué falta |
|---|---|---|
| Caral | Resumen de sync `1ACFFC1D` en el bit 3925, trama `CARAL/1`, desentrelazado y Viterbi; dos copias de telemetría con la misma sincronización | Recuperar parámetros y decodificador para verificar toda la cadena |
| Marcahuasi | Resumen de subset sum, LLL y AES-GCM con una flag reportada | Datos de entrada, construcción de la red y comprobación del descifrado |
| Wamani Flight | Firmware y un resultado histórico atribuido al descifrado de telemetría | Documentar y verificar el formato completo del contenedor |
| Kuntur Skywatch | Paquete de IQ, criterios del reto y resultado histórico sobre la advertencia ZNY | Reproducir demodulación, CRC, identificación y descifrado |
| Miau | Resultado histórico que atribuye una flag al payload ICMP de una captura | Asociar la captura exacta y preparar extracción reproducible |
| Quipu Parser | Binario, notas de protocolo y exploit; análisis de overflow y ret2win | Recuperar la salida final o verificar en un laboratorio equivalente |
| GEMS | Captura del asistente con referencia a un detalle de entrega y flag cortada | Nombre oficial, diálogo completo y alcance de las herramientas |
| Moche | Fuentes y scripts de etapas; resultados de fugas de heap y libc | Evidencia del paso final y flag remota |
| Wari | Módulo del kernel y entorno QEMU de pruebas | Cadena completa con resultado final; la flag local no equivale a resolver remoto |
| Huaca | Fuentes con escritura nula fuera de límites y filtro seccomp | Solución completa y resultado |
| Illapa Forge | Binario, scripts y diagnósticos de desbordamiento | Explicar con pruebas el fallo de la etapa final y recuperar resultado |
| Just follow the clues | Imagen y pruebas de contraseñas con steghide | Resolución confirmada |
| Tipón, Sechín y Machu Picchu | Menciones en resúmenes previos | Enunciados, datos y secuencia de solución |
| Moray | Intérprete y programa con bucles grandes | Reconstrucción documentada del método aplicado y resultado |

## Flags referidas en la recopilación previa

Se conservan aquí como pistas históricas, sin elevarlas a comprobaciones de esta publicación:

- Caral: `csh{9693daf4da3f5bb518f7bc9eabbfcc529797a3ca490f15f11f95fad482402284}`.
- Marcahuasi: `csh{1ed6f888cb3df1c28e08256612068feddff6317df8a83d001621785100b89416}`.
- Wamani Flight: `csh{58faf9b19d03da367ee6aa1d9a416a529dde35b76d830854e3aa210388fab096}`.
- Kuntur Skywatch: `csh{969add222f7a3d90050150841219ec06bf884598d8bbbb888f2b5d6f1bb83146}`.
- Miau: `csh{1f04db20bde0b02ce74a652d4ae775205d0010a1312ea5e227d3b03a82910a35}`.

La flag que aparecía sin asignación en el primer resumen, `csh{f4a10c95fa25f3c1de8e033dcaa86ee8cbb6f037f0a7b09df05a9f7b3487b75b}`, ya se pudo atribuir y volver a comprobar en Chasqui Relay.

![Captura parcial de GEMS Assistant](../assets/gems.jpg)
