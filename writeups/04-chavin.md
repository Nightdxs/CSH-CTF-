# Chavín: una carrera y dos entornos que no se comportaban igual

[← Volver al índice](../README.md)

Chavín es el caso del que recuperé una secuencia de depuración más completa. Hubo pruebas con flags locales, diferencias entre la libc de pruebas y la del reto, procesos que abortaban y, al final, una respuesta remota con la flag. Separar esas etapas fue necesario para entender qué estaba demostrado en cada momento.

## El problema estaba entre guardar un puntero y usarlo

El servicio mantenía galerías compartidas entre varias conexiones. La estructura recuperada en la transcripción tenía tres campos:

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

La misma ventana daba dos primitivas: `gritar` podía leer memoria liberada y `susurrar` podía escribir en ella. El reto consistió en hacer que esa memoria se reutilizara de una forma útil.

## De un bloque liberado al control de una galería

El [exploit recuperado](../scripts/chavin_exploit.py) utiliza dos conexiones, `F` y `C`. Una mantiene las operaciones que liberan y reasignan; la otra provoca el uso de los punteros guardados. La secuencia fue:

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

Un detalle que costó intentos fue mantener la relación entre el hilo que liberaba y el que reasignaba. Los registros de depuración mostraron que cambiar esas operaciones de conexión impedía obtener el solapamiento esperado. En lugar de asumir que «liberar y volver a pedir» bastaba, hubo que reproducir el orden de asignaciones del servicio y comprobar dónde terminaba cada bloque.

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

Las pruebas locales llegaron a producir `csh{FLAG_LOCAL_DE_PRUEBA}`. Eso validaba una cadena en el entorno de pruebas, pero todavía no era la flag de la competencia. Contra el entorno correspondiente al reto aparecía:

```text
malloc(): unaligned tcache chunk detected
```

El punto que se corrigió fue el cálculo de la base del arena. El buffer usado para el leak estaba en el offset `0x1100`, ya dentro de la segunda página. Reconstruir la página a partir del enlace y tratarla como si fuera la base desplazaba los cálculos en `0x1000`.

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

La parte más valiosa fue comparar hipótesis con resultados: una carrera podía perderse antes de guardar el puntero; un bloque podía liberarse en el hilo equivocado; una diferencia de página podía invalidar todo el cálculo. Cada caso requería una comprobación distinta.

También apareció un problema de organización de archivos. El ZIP local llamado `chavin.zip` contiene fuentes de **Huaca**, cuyo código es diferente. Para esta reconstrucción usé el código de galerías conservado en la transcripción y el exploit correspondiente. El nombre del archivo, por sí solo, no era suficiente para atribuirle el contenido al reto.

No volví a ejecutar esta cadena contra un servidor. Queda como documentación del laboratorio y de su depuración histórica. Los offsets del script dependen del ejecutable y de la libc usados en aquella sesión.
