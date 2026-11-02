# Inti Vault, Apu Whisper y Wiracocha Orb

[← Volver al índice](../README.md)

Estos tres retos me permitieron practicar formas distintas de aprovechar un error de memoria. En Inti necesitaba llamar a una función con los argumentos correctos; en Apu, modificar una variable; y en Wiracocha, averiguar dónde estaba libc antes de construir la llamada final.

## Inti Vault: el destino correcto también necesita argumentos

En `offering()` había un buffer de 64 bytes, pero la llamada a `read` aceptaba 200. El desbordamiento permitía alcanzar la dirección de retorno. El desplazamiento era:

```text
64 bytes de buffer + 8 bytes de RBP guardado = 72 bytes hasta RIP
```

La función interesante se llamaba `solar_keys`. No bastaba con saltar a ella: comparaba dos argumentos antes de llamar a `print_flag`.

| Argumento | Registro en x86-64 System V | Valor |
|---|---|---|
| Sol | `rdi` | `0xc0ffee1337` |
| Luna | `rsi` | `0x1337beefcafe` |

Esto corrigió la primera lectura del reto: no era sobrescribir dos variables locales llamadas «llaves», sino preparar los registros de una llamada. Los gadgets encontrados en ese binario fueron `pop rdi; ret` en `0x400a73` y `pop rsi; pop r15; ret` en `0x400a71`.

La cadena quedó así:

```python
payload = b'A' * 72
payload += p64(0x400a73)       # pop rdi; ret
payload += p64(0xc0ffee1337)   # Sol
payload += p64(0x400a71)       # pop rsi; pop r15; ret
payload += p64(0x1337beefcafe) # Luna
payload += p64(0)             # r15 también consume una palabra
payload += p64(0x400923)      # solar_keys
```

`p64` representa aquí el empaquetado de un entero de 64 bits en little-endian. El [script completo](../scripts/inti_vault_exploit.py) usa `struct.pack('<Q', valor)` y espera al prompt antes de enviar los bytes.

La salida guardada en la conversación incluye:

```text
[+] Las llaves encajan. La boveda se abre:
csh{96fdd077a0a2b52d47a08e5bd96beb2dca777ec165164f3f7e81763c38b785cc}}
```

La transcripción tiene una segunda llave y después otro banner. Conservo ese detalle: la cadena con formato de flag es la que termina tras los 64 dígitos hexadecimales, pero no atribuyo el carácter extra a una causa que no comprobé.

La lección fue seguir la convención de llamadas y contar cada palabra que consume un gadget. Un `pop` adicional cambia el resto de la cadena aunque el valor cargado en ese registro no importe.

## Apu Whisper: cuatro escrituras pequeñas

El binario interpretaba la entrada como formato de impresión. Ese comportamiento permite más que mostrar valores de la pila: la familia `%n` escribe en memoria el número de caracteres impresos. Con `%hhn`, la escritura se limita a un byte.

El objetivo del [script recuperado](../scripts/apu_exploit.py) era cambiar `offering_power`, en `0x404010`, a `0x1337babe`. No hacía falta secuestrar el retorno ni modificar la GOT. Bastaba con lograr que la comprobación de la ofrenda tomara el camino que imprimía el secreto.

Primero se envió un marcador `AAAAAAAA` junto con varias posiciones `%N$p`. El valor `0x4141414141414141` permitió identificar que el contenido del buffer empezaba en la posición 6.

En little-endian, los cuatro bytes del valor son `be ba 37 13`. Para no imprimir cantidades innecesarias, el script ordenaba las escrituras por el valor que necesitaba alcanzar:

| Dirección | Byte final | Cuenta de caracteres |
|---|---|---|
| `0x404013` | `0x13` | 19 |
| `0x404012` | `0x37` | 55 |
| `0x404011` | `0xba` | 186 |
| `0x404010` | `0xbe` | 190 |

Así, los incrementos de impresión son 19, 36, 131 y 4. El formato usa esos incrementos antes de cada `%hhn`; las direcciones se añaden al final del buffer, con el relleno necesario para que sus posiciones coincidan con las referencias del formato. En la captura, el payload completo tiene 80 bytes.

![Offset 6, payload y respuesta de Apu Whisper](../assets/apu.jpg)

```text
csh{702768194f8978935e221a6d3fb677bb090083fe037ca1a38a5431a4db49a7cc}
```

Antes de esta ejecución hubo un error al compilar `unicorn`. La versión guardada del exploit usa únicamente la biblioteca estándar de Python. Ese cambio simplificó el entorno, pero la solución seguía dependiendo de entender el offset y las direcciones del binario. El fallo del programa era usar la entrada como cadena de formato; la llamada segura tendría un formato fijo, como `printf("%s", entrada)`.

## Wiracocha Orb: primero una dirección, después la llamada

Wiracocha necesitaba dos etapas. El binario tenía direcciones fijas para los gadgets usados, pero la dirección de libc variaba. El exploit no podía asumir dónde estaban `system` o `/bin/sh`.

El [script de la sesión](../scripts/wiracocha_exploit.py) usa un desplazamiento de **56 bytes** hasta el retorno. La primera cadena aprovecha dos fragmentos de `__libc_csu_init` para preparar una llamada equivalente a:

```c
write(1, &write_got, 8);
```

La entrada GOT ya contenía la dirección de `write` en libc. Al imprimir esos ocho bytes y volver a `main`, el proceso seguía disponible para una segunda entrada. Con los offsets de la libc entregada se calculaban:

```python
libc_base = write_addr - 0x1100f0
system    = libc_base + 0x04f420
binsh     = libc_base + 0x1b3d88
```

La segunda cadena cargaba `binsh` en `rdi`, añadía un `ret` para alinear la pila y saltaba a `system`.

```text
'A' × 56 → pop rdi → dirección de /bin/sh → ret → system
```

Hubo un problema de recepción que merecía documentarse. Si una lectura esperaba un marcador y descartaba los bytes que venían después en el mismo paquete, podía perder parte de la dirección filtrada. La clase `Tube` del script conserva un buffer: `recvuntil` consume hasta el marcador y `recvn(8)` recupera los siguientes ocho bytes sin descartarlos.

La captura muestra direcciones coherentes con los cálculos, el usuario `ctf`, una cadena con formato de flag y el listado del directorio:

![Fuga de libc y ejecución de comandos en Wiracocha](../assets/wiracocha.jpg)

En ese listado, `flag.txt` era un enlace a `/tmp/flag.txt`. Los mensajes de error de `/flag.txt` y `/flag` correspondían a rutas distintas; no significaban que la lectura de `flag.txt` hubiera fallado. Para evitar una transcripción dudosa, la flag queda conservada en la imagen.

Lo que me llevé de este reto fue que el trabajo no termina al construir una cadena ROP. También hay que sincronizar el diálogo con el programa, conservar los bytes del leak y usar la libc correcta. Un error al leer ocho bytes puede parecer un error de explotación y llevar a cambiar una cadena que ya estaba bien.
