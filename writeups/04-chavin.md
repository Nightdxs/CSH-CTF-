# Chavín: una carrera y dos entornos que no se comportaban igual

[← Volver al índice](../README.md)

Chavín fue el que más trabajo de depuración dejó en los registros, con flags locales de prueba, diferencias entre versiones de libc y procesos que abortaban antes de llegar a la respuesta remota. Al ordenar el writeup tuve que separar esas etapas para explicar qué funcionaba en cada entorno y qué faltaba corregir.

## El problema estaba entre guardar un puntero y usarlo

El servicio mantenía galerías compartidas entre varias conexiones mediante una estructura de tres campos, que pude recuperar en la transcripción:

```c
typedef struct Galeria {
    char *datos;
    size_t largo;
    void (*eco)(const char *, size_t);
} Galeria;
```

Las operaciones `susurrar` y `gritar` tomaban los datos de una galería y esperaban 20 ms antes de usarlos. Este es el fragmento relevante de `gritar`, simplificado a partir del código guardado:

```c
char *donde = g->datos;
size_t cuanto = g->largo > MAX_BYTES ? MAX_BYTES : g->largo;
void (*como)(const char *, size_t) = g->eco;
usleep(20000);
como(donde, cuanto);
```

Mientras una conexión esperaba, otra podía ejecutar `derrumbar`, que retiraba la galería del arreglo y liberaba `g->datos` y `g`. Poner el elemento compartido a `NULL` no invalidaba las copias que ya estaban guardadas en la primera conexión.

Con esa misma ventana, `gritar` podía leer memoria liberada y `susurrar` escribir en ella, así que el siguiente paso consistía en preparar su reutilización para controlar datos que siguieran siendo accesibles.

## De un bloque liberado al control de una galería

El [exploit de Chavín](../scripts/chavin_exploit.py) utiliza dos conexiones, `F` y `C`, repartiendo las operaciones para que una libere y reasigne mientras la otra usa los punteros que había guardado, en esta secuencia:

1. Preparar varias galerías y sus buffers para obtener un patrón de asignaciones conocido.
2. Provocar una lectura después de la liberación para recuperar metadatos del heap.
3. Usar una segunda carrera para modificar el enlace de un bloque libre.
4. Conseguir que una nueva estructura de galería se solape con un buffer que seguía siendo accesible.
5. Modificar los campos `datos`, `largo` y `eco` a través de ese solapamiento.

El script calcula el enlace codificado que quiere escribir con:

```python
mangle = (DY >> 12) ^ D
```

`DY` es la dirección del bloque cuya lista libre se está manipulando y `D` el destino de la siguiente asignación. Son direcciones derivadas del patrón concreto del exploit, no constantes válidas para cualquier heap.

Uno de los detalles que costó intentos fue qué conexión hacía cada operación, porque cambiar el hilo que liberaba y el que reasignaba impedía obtener el solapamiento esperado. Hubo que reproducir el orden de asignaciones del servicio y comprobar dónde terminaba cada bloque para entender por qué no se reutilizaba como esperaba el exploit.

## Dos fugas para preparar la llamada final

Una vez controlada la estructura solapada, el campo `eco` permitía conocer la base del ejecutable:

```python
pie = eco - ECO_OFF
```

Después se apuntaba `datos` a la entrada GOT de `read` y se pedían ocho bytes. Con el offset de `read` de la libc del reto se obtenía la base de esa biblioteca:

```python
libc = read_pointer - LIBC_READ
```

Finalmente se reemplazaba `eco` por `system` y `datos` por una cadena de comandos que leía la flag y enviaba la salida a un descriptor de socket disponible. El exploit conserva los offsets y la secuencia completa; esta descripción resume el recorrido, no sustituye el código.

## El error de una página

Las pruebas locales llegaron a producir `csh{FLAG_LOCAL_DE_PRUEBA}`, aunque todavía faltaba trasladar esa cadena al entorno del reto, donde aparecía este error:

```text
malloc(): unaligned tcache chunk detected
```

El error estaba en el cálculo de la base del arena: el buffer usado para el leak caía en `0x1100`, dentro de la segunda página, por lo que reconstruir su página y tratarla como la base dejaba los cálculos desplazados en `0x1000`.

La corrección registrada en el script fue:

```python
arena = (fd_raw << 12) - (OFF_DL & ~0xfff)
```

Después de relanzar una instancia, el registro remoto mostró:

```text
[i] arena=0x7f82f4000000 PIE=0x55fec43e8000 libc=0x7f82fa600000
[0] csh{776f588779e6f4e96a7299a2c57b98e39e6a520c1785b63a0b4efa8a23adab1c}
```

La fuente de este resultado es la transcripción de la sesión de Claude, no una nueva ejecución remota durante la escritura del artículo.

## Qué aprendí de los intentos fallidos

Lo que más aprendí fue a separar las causas de cada fallo, porque perder la carrera antes de guardar un puntero, liberar desde otro hilo o equivocarse en una página podían romper el exploit de formas distintas y cada una necesitaba su propia comprobación.

Al revisar los archivos apareció otra confusión: el ZIP llamado `chavin.zip` contenía fuentes de **Huaca**, por lo que tuve que apoyarme en el código de galerías conservado en la transcripción y en el exploit correspondiente para reconstruir Chavín.

Esta parte recoge la ejecución y la depuración guardadas durante el trabajo, con offsets que dependen del ejecutable y de la libc de aquella sesión; al preparar el artículo no repetí la cadena contra un servidor.
