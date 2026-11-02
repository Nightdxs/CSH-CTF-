# Cuatro fallos que se entienden siguiendo los datos en el código

[← Volver al índice](../README.md)

De estos cuatro retos pude recuperar el código y los scripts de la sesión, así que aquí explico cómo seguí las entradas hasta encontrar cada fallo. Como no conservé una salida remota con la flag de todos ellos, los dejé como **análisis de las rutas de explotación**.

## Ayni Records: el rol también viaja en el perfil

Al revisar cómo se guardaba el perfil encontré que el servidor pasaba el cuerpo completo de la petición al modelo, donde este método copiaba todos los campos recibidos:

```js
update(fields) { Object.assign(this, fields); }
```

La ruta terminaba llamando a `currentUser.update(req.body)`. Aunque el formulario no incluyera un control para editar `role`, una petición manual podía añadirlo:

```bash
curl -s -b cookies.txt -c cookies.txt -X POST "$U/profile/edit" \
  --data-urlencode 'role=funcionario'
```

El detalle estaba en que modificar `user.role` no cambiaba inmediatamente `req.session.role`, que era lo que consultaba la autorización; hacía falta iniciar sesión de nuevo para copiar el rol actualizado antes de entrar a `/funcionario`.

```text
Registrar cuenta → editar role → iniciar sesión de nuevo → /funcionario
```

Dejé la secuencia en el [script de Ayni](../scripts/ayni_exploit.sh), incluyendo el nuevo login porque era fácil pasarlo por alto. Me ayudó a entender mejor la diferencia entre el usuario almacenado y la identidad de la sesión, además del riesgo de copiar campos del cliente sin decidir antes cuáles se pueden editar.

## Kuska Pay: una firma que solo se comprueba si la envías

En `controllers/webhook.js`, la verificación de la firma estaba dentro de esta condición:

```js
if (signature) {
  if (!verifySignature(signature, req.rawBody || Buffer.from(''))) {
    return res.status(400).json({ message: 'firma invalida' });
  }
}
```

Después de ese bloque se comprobaba `status === "PAID"` y se actualizaba el pago, lo que dejaba un caso curioso: enviar una firma incorrecta fallaba, pero omitirla permitía continuar.

La ruta propuesta fue registrar un proveedor, obtener su `paymentId` y enviar una confirmación sin `X-Signature`:

```bash
curl -s -X POST "$U/webhooks/payment/confirm" \
  -H 'Content-Type: application/json' \
  -d '{"paymentId":"<ID_OBTENIDO>","status":"PAID"}'
```

Una vez marcado el pago como `PAID`, el código de `/vendor/payment/status` incluía la flag en su respuesta, y esa es la secuencia que reúne el [script de Kuska](../scripts/kuska_exploit.sh).

Me llamó la atención que la verificación HMAC estaba implementada, pero el `if (signature)` permitía saltársela por completo; para que protegiera el webhook, la falta de firma tenía que rechazarse antes de cambiar el pago.

## Void Ledger: una búsqueda que cruza la frontera de autorización

En la búsqueda se interpolaba la entrada del usuario dentro de un `LIKE`, mientras que en la tabla `relics` había registros privados con información en `coordinates`, así que el análisis llevó a probar un `UNION` de tres columnas:

```sql
x%' UNION SELECT name,coordinates,'relic' FROM relics-- -
```

La petición se enviaba a `/api/archive/search` con el token de una cuenta normal, cerrando el `LIKE` para añadir las filas de `relics` y comentar el resto de la consulta. Al colocar `coordinates` en una columna que la búsqueda devolvía, su contenido podía salir por esa misma respuesta.

El [script de Void](../scripts/void_exploit.sh) registra una cuenta y envía la consulta, siguiendo una ruta que podía llegar a la tabla privada sin cambiar el rol. Este análisis me sirvió para ver cómo una inyección puede saltarse las restricciones de la interfaz a través de la propia consulta.

## Yaku Register: actualizar mi email y resolver otra identidad

`/api/enroll` utilizaba las claves del JSON como nombres de columnas para actualizar la fila del usuario. Una validación de caracteres permitía identificadores como `email`, pero eso no significaba que el usuario debiera tener permiso para modificar cualquier columna válida.

La otra mitad del problema aparecía en `/home`, que resolvía al usuario por el email del token; como los datos de arranque usaban `admin@yaku.gov` para el administrador, la secuencia propuesta era:

```text
Crear cuenta → iniciar sesión → enroll con email del admin
→ iniciar sesión de nuevo → abrir /home
```

```bash
curl -s -b cookies.txt -X POST "$U/api/enroll" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@yaku.gov"}'
```

El [script de Yaku](../scripts/yaku_exploit.sh) sigue esos pasos y el análisis de la sesión esperaba recuperar la fila del administrador, insertada primero, algo que queda por verificar en una instancia equivalente. Lo que sí se ve en el diseño es el riesgo de dejar duplicar un email que luego se usa para resolver la identidad, en vez de apoyarse en un identificador interno estable y limitar los campos editables.
