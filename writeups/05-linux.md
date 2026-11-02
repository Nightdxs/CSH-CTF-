# Linux: leer el entorno antes de cambiarlo

[← Volver al índice](../README.md)

En estos retos pude avanzar revisando el propio sistema, entre logs, archivos de configuración, puertos y tareas programadas. Los organicé con los nombres de los hosts que aparecen en las capturas, porque no conservé todas las fichas originales.

## Kotosh: tres fragmentos entre mucho ruido

Entre los mensajes de retransmisiones, señal y buffers aparecía la marca `SIGNAL_FRAGMENT`, así que filtré esa etiqueta en los archivos del relay para ver solo los fragmentos que interesaban:

```bash
grep 'SIGNAL_FRAGMENT' /var/log/relay/*.log
```

Los resultados estaban repartidos entre `noise.log`, `telemetry.log` y `uplink.log`, pero las marcas `1/3`, `2/3` y `3/3` daban el orden en que había que unirlos.

```bash
printf '%s' '<fragmento-1><fragmento-2><fragmento-3>' | base64 -d
```

La salida guardada fue:

```text
csh{c65f381972cfc20192753a866b79a543f28d02dc8226b3bb6d706b9c993e719c}
```

![Localización y decodificación de los fragmentos de Kotosh](../assets/kotosh.jpg)

Al unir los fragmentos antes de decodificarlos no hacía falta suponer que cada uno fuera un bloque Base64 independiente, y toda aquella salida terminó reducida a tres líneas ordenadas.

## Pachacámac: el servicio también estaba dentro

La captura que guardé comienza con una sesión SSH como `operator`, así que explico el recorrido desde ese acceso, sin atribuirle una obtención de contraseña que no aparece en el registro.

Una búsqueda en archivos de configuración encontró el `callsign` en `/etc/groundwork/relay.conf`:

```bash
grep -Rin --include='*.conf' 'callsign' /etc /opt /home 2>/dev/null
```

Para listar los puertos intenté usar `ss` y, como no estaba instalado, pasé a la alternativa disponible:

```bash
netstat -lnt
```

En el puerto 4444 encontré `BUREAU COMMS RELAY`, que al conectarme desde la propia instancia pidió el callsign:

```bash
nc 127.0.0.1 4444
```

Introducir el valor del archivo de configuración devolvió:

```text
csh{15fc392c3260a16c62a079073302e10122d0976655c7812553bebc0b13b8d90e}
```

![Configuración, puertos y autenticación del relay](../assets/pachacamac.jpg)

Este reto me hizo revisar qué más había dentro del contenedor después de entrar por SSH, porque la configuración guardaba el callsign que pedía otro servicio de la misma instancia.

## Ollanta: el sufijo que cambiaba el resultado

La instancia traía una utilidad propia llamada `groundctl`, cuya ayuda permitía listar, iniciar, detener, habilitar y desenmascarar servicios; al revisar el estado aparecían `corruptor.service` habilitado y `generator.service` enmascarado.

En el primer intento añadí `.service` a los nombres, pero la herramienta respondió con `.service.service` y `~/recovery.txt` seguía corrupto, lo que apuntaba a que la interfaz ya añadía el sufijo por su cuenta.

La segunda secuencia fue:

```bash
sudo groundctl disable corruptor
sudo groundctl stop corruptor
sudo groundctl unmask generator
sudo groundctl start generator
sudo groundctl list
cat ~/recovery.txt
```

Después de corregir los nombres, el listado mostraba `corruptor.service disabled` y `generator.service enabled`, mientras que el archivo ya contenía:

```text
csh{1b28f75940ecba0ec0af687e8e64ac710e2b5b7603a5a982d38fa44a65fe1ff3}
```

![Primer intento con sufijo y secuencia corregida en Ollanta](../assets/ollanta.jpg)

Lo que me ayudó fue volver a mirar el archivo y el listado de servicios después de los comandos, porque el mensaje de «iniciado» del primer intento no bastaba para saber si había cambiado lo que necesitaba.

## Pisac: una tarea que volvía cada minuto

Antes de intentar recuperar el archivo, revisé qué se ejecutaba periódicamente:

```bash
crontab -l
ls -la /etc/cron.d
cat /etc/crontab
ps aux
```

En la crontab del usuario había esta línea:

```cron
* * * * * /opt/groundwork/wiper.sh
```

También aparecía un proceso `generator.sh`, mientras que `wiper.sh` se ejecutaba cada minuto y podía interferir con la recuperación, así que la secuencia guardada retiró esa entrada y eliminó el script de la instancia:

```bash
crontab -l | grep -Fv '/opt/groundwork/wiper.sh' | crontab -
sudo rm /opt/groundwork/wiper.sh
cat ~/flag.txt
```

![Tarea cron, procesos y lectura de la flag en Pisac](../assets/pisac.jpg)

La cadena transcrita de la captura es:

```text
csh{aef35d5055652f8795785886b9bf6be657abc24665a104d438b273c629de5a7a}
```

No conservé el contenido de `wiper.sh`, pero sí la tarea programada y la lectura de la flag después de retirarla. Me sirvió para recordar que, cuando un archivo vuelve a cambiar, conviene revisar qué proceso o automatización puede estar actuando sobre él.
