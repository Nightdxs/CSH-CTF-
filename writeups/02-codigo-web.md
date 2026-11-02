# Cuatro fallos que se entienden siguiendo los datos en el código

[← Volver al índice](../README.md)

Estos cuatro retos tienen código fuente y scripts recuperados de la sesión. Puedo reconstruir el mecanismo, pero en los registros revisados no encontré una salida remota con la flag de cada uno. Por eso los presento como **análisis de las rutas de explotación**, sin inventar resultados.

## Ayni Records: el rol también viaja en el perfil

El formulario de edición permitía cambiar datos personales, pero el servidor pasaba el cuerpo completo de la petición al modelo. El método de actualización copiaba todos sus campos:

```js
update(fields) { Object.assign(this, fields); }
```

La ruta terminaba llamando a `currentUser.update(req.body)`. Aunque el formulario no incluyera un control para editar `role`, una petición manual podía añadirlo:

```bash
curl -s -b cookies.txt -c cookies.txt -X POST "$U/profile/edit" \
  --data-urlencode 'role=funcionario'
```

Había un detalle más: la autorización consultaba `req.session.role`, mientras que la actualización había cambiado `user.role`. El login copiaba el rol del usuario a la sesión. Por eso la secuencia tenía que incluir un nuevo inicio de sesión antes de consultar `/funcionario`.

```text
Registrar cuenta → editar role → iniciar sesión de nuevo → /funcionario
```

El [script recuperado](../scripts/ayni_exploit.sh) reúne esos pasos. Este ejemplo me ayudó a separar el objeto almacenado de la identidad que conserva la sesión: cambiar uno no siempre actualiza el otro. La defensa consiste en permitir explícitamente los campos editables y mantener la asignación de roles fuera de esta operación.

## Kuska Pay: una firma que solo se comprueba si la envías

En `controllers/webhook.js`, la verificación de la firma estaba dentro de esta condición:

```js
if (signature) {
  if (!verifySignature(signature, req.rawBody || Buffer.from(''))) {
    return res.status(400).json({ message: 'firma invalida' });
  }
}
```

Después se comprobaba `status === "PAID"` y se actualizaba el pago. La consecuencia era que una firma inválida se rechazaba, pero la ausencia de firma permitía continuar.

La ruta propuesta fue registrar un proveedor, obtener su `paymentId` y enviar una confirmación sin `X-Signature`:

```bash
curl -s -X POST "$U/webhooks/payment/confirm" \
  -H 'Content-Type: application/json' \
  -d '{"paymentId":"<ID_OBTENIDO>","status":"PAID"}'
```

El código de `/vendor/payment/status` añadía la flag cuando el pago estaba en estado `PAID`. El [script](../scripts/kuska_exploit.sh) automatiza la secuencia.

La presencia de HMAC y de una comparación segura no resolvía el problema de flujo: la comprobación era opcional. La ausencia de firma tiene que ser motivo de rechazo antes de cambiar el estado del pago.

## Void Ledger: una búsqueda que cruza la frontera de autorización

En la búsqueda del archivo se interpolaba la consulta del usuario en un `LIKE`. La tabla `relics` tenía registros privados con información sensible en `coordinates`. La idea fue combinar ambos hechos con un `UNION` de tres columnas:

```sql
x%' UNION SELECT name,coordinates,'relic' FROM relics-- -
```

La petición usaba el token de una cuenta normal en `/api/archive/search`. La inyección cerraba el `LIKE`, añadía las filas de `relics` y comentaba el resto de la consulta. La posición de `coordinates` hacía que su contenido apareciera en una columna que la búsqueda sí devolvía.

El [script de la sesión](../scripts/void_exploit.sh) registra un usuario y envía esa consulta. Lo relevante es que no hacía falta elevar el rol: una consulta vulnerable podía acceder a datos de otra tabla pese a que la interfaz normal los reservara al administrador. La autorización también tiene que sostenerse en la forma en que se consultan los datos.

## Yaku Register: actualizar mi email y resolver otra identidad

`/api/enroll` utilizaba las claves del JSON como nombres de columnas para actualizar la fila del usuario. Una validación de caracteres permitía identificadores como `email`, pero eso no significaba que el usuario debiera tener permiso para modificar cualquier columna válida.

La otra mitad del problema estaba en la identidad: `/home` resolvía al usuario por el email guardado en el token. En los datos de arranque, el administrador tenía `admin@yaku.gov`. La secuencia propuesta era:

```text
Crear cuenta → iniciar sesión → enroll con email del admin
→ iniciar sesión de nuevo → abrir /home
```

```bash
curl -s -b cookies.txt -X POST "$U/api/enroll" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@yaku.gov"}'
```

El [script recuperado](../scripts/yaku_exploit.sh) implementa esos pasos. El análisis de la sesión señalaba que la búsqueda devolvía la fila del administrador sembrada primero; esa dependencia del resultado concreto debe verificarse en una instancia equivalente. El defecto de diseño es más general: permitir duplicar un atributo usado como identidad y luego confiar en él para resolver permisos. Un identificador interno estable y una lista explícita de campos editables evitan encadenar ambas decisiones.
