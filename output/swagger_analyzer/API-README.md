# Gestión de Prioridades API

**Versión**: 1.0.0
**OpenAPI**: 3.0.1

## 📋 Descripción

API RESTful para la gestión completa de prioridades mediante operaciones CRUD. Incluye validación de encabezados personalizados, manejo estructurado de errores y enlaces HATEOAS.

## 📑 Tabla de Contenidos

- [Servidores](#servidores)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
  - [GET /priorities/{id}](#get-prioritiesid)
  - [PUT /priorities/{id}](#put-prioritiesid)
  - [DELETE /priorities/{id}](#delete-prioritiesid)
  - [GET /priorities](#get-priorities)
  - [POST /priorities](#post-priorities)
- [Schemas](#schemas)
- [Códigos de Estado](#códigos-de-estado)

## 📊 Resumen

- **Total de Endpoints**: 5
- **Total de Schemas**: 2
- **Autenticación**: ❌ No

### Métodos HTTP

- `DELETE`: 1 endpoint(s)
- `GET`: 2 endpoint(s)
- `POST`: 1 endpoint(s)
- `PUT`: 1 endpoint(s)

## 🌐 Servidores

### http://localhost:8080
> Generated server url

## 🔗 Endpoints

### `GET` /priorities/{id}

**Obtener prioridad por ID**

Recupera una prioridad específica mediante su identificador. Requiere encabezados de validación y que el ID exista en la base de datos.

**Tags**: `Prioridades`

**Operation ID**: `findById`

#### Parámetros

| Nombre | Ubicación | Tipo | Requerido | Descripción |
|--------|-----------|------|-----------|-------------|
| `id` | path | `integer (int32)` | ✅ | ID de la prioridad |
| `x-correlation-id` | header | `string (uuid)` | ✅ | Identificador único para correlación entre servicios. UUID v4 válido con 36 caracteres. |
| `x-request-id` | header | `string (uuid)` | ✅ | Identificador único de la solicitud. UUID v4 válido con 36 caracteres. |
| `x-transaction-id` | header | `string (uuid)` | ✅ | Identificador único de la transacción de negocio. UUID v4 válido con 36 caracteres. |

#### Respuestas

##### 400
Encabezados requeridos faltantes o inválidos
**Códigos de Error Posibles:**

**TYP-001** - header_error (HTTP 400)
  - `HDR-001`: Encabezado requerido faltante en la solicitud
  - `HDR-002`: Valor del encabezado demasiado corto
  - `HDR-003`: Valor del encabezado excede la longitud máxima
  - `HDR-004`: Formato del encabezado inválido


**Content-Type**: `application/json`

**Schema**: [`Response400`](#response400)

##### 404
Prioridad no encontrada - El ID especificado no existe en la base de datos
**Códigos de Error Posibles:**

**TYP-002** - resource_not_found (HTTP 404)
  - `RNF-001`: Recurso no encontrado por ID especificado
  - `RNF-002`: Recurso no encontrado después de una operación
  - `RNF-003`: Endpoint o ruta no existe en la API


**Content-Type**: `application/json`

**Schema**: [`Response404`](#response404)

##### 200
Prioridad encontrada exitosamente

**Content-Type**: `*/*`

**Schema**: [`Response200`](#response200)

---

### `PUT` /priorities/{id}

**Actualizar prioridad**

Actualiza una prioridad existente. El ID debe existir y el nombre debe permanecer único.

**Tags**: `Prioridades`

**Operation ID**: `update`

#### Parámetros

| Nombre | Ubicación | Tipo | Requerido | Descripción |
|--------|-----------|------|-----------|-------------|
| `id` | path | `integer (int32)` | ✅ | ID de la prioridad |
| `x-correlation-id` | header | `string (uuid)` | ✅ | Identificador único para correlación entre servicios. UUID v4 válido con 36 caracteres. |
| `x-request-id` | header | `string (uuid)` | ✅ | Identificador único de la solicitud. UUID v4 válido con 36 caracteres. |
| `x-transaction-id` | header | `string (uuid)` | ✅ | Identificador único de la transacción de negocio. UUID v4 válido con 36 caracteres. |

#### Request Body

**✅ Obligatorio**

**Content-Type**: `application/json`

**Schema**: [`RequestBody`](#requestbody)

#### Respuestas

##### 409
Conflicto - Nombre duplicado. Ya existe una prioridad con ese nombre
**Códigos de Error Posibles:**

**TYP-003** - request_body_validation_error (HTTP 400/409)
  - `RBV-001`: Campo requerido faltante en el cuerpo de la solicitud
  - `RBV-002`: Campo enviado con valor vacío
  - `RBV-003`: Longitud del campo por debajo del mínimo requerido
  - `RBV-004`: Longitud del campo excede el máximo permitido
  - `RBV-005`: Valor duplicado detectado (violación de restricción única)


**Content-Type**: `application/json`

**Schema**: [`Response409`](#response409)

##### 200
Prioridad actualizada exitosamente

**Content-Type**: `*/*`

**Schema**: [`Response200`](#response200)

##### 404
Prioridad no encontrada - El ID especificado no existe en la base de datos
**Códigos de Error Posibles:**

**TYP-002** - resource_not_found (HTTP 404)
  - `RNF-001`: Recurso no encontrado por ID especificado
  - `RNF-002`: Recurso no encontrado después de una operación
  - `RNF-003`: Endpoint o ruta no existe en la API


**Content-Type**: `application/json`

**Schema**: [`Response404`](#response404)

##### 400
Encabezados faltantes o datos de validación incorrectos
**Códigos de Error Posibles:**

**TYP-001** - header_error (HTTP 400)
  - `HDR-001`: Encabezado requerido faltante en la solicitud
  - `HDR-002`: Valor del encabezado demasiado corto
  - `HDR-003`: Valor del encabezado excede la longitud máxima
  - `HDR-004`: Formato del encabezado inválido

**Códigos de Error Posibles:**

**TYP-003** - request_body_validation_error (HTTP 400/409)
  - `RBV-001`: Campo requerido faltante en el cuerpo de la solicitud
  - `RBV-002`: Campo enviado con valor vacío
  - `RBV-003`: Longitud del campo por debajo del mínimo requerido
  - `RBV-004`: Longitud del campo excede el máximo permitido
  - `RBV-005`: Valor duplicado detectado (violación de restricción única)


**Content-Type**: `application/json`

**Schema**: [`Response400`](#response400)

---

### `DELETE` /priorities/{id}

**Eliminar prioridad**

Elimina una prioridad por su ID. Requiere que el ID exista en la base de datos.

**Tags**: `Prioridades`

**Operation ID**: `delete`

#### Parámetros

| Nombre | Ubicación | Tipo | Requerido | Descripción |
|--------|-----------|------|-----------|-------------|
| `id` | path | `integer (int32)` | ✅ | ID de la prioridad |
| `x-correlation-id` | header | `string (uuid)` | ✅ | Identificador único para correlación entre servicios. UUID v4 válido con 36 caracteres. |
| `x-request-id` | header | `string (uuid)` | ✅ | Identificador único de la solicitud. UUID v4 válido con 36 caracteres. |
| `x-transaction-id` | header | `string (uuid)` | ✅ | Identificador único de la transacción de negocio. UUID v4 válido con 36 caracteres. |

#### Respuestas

##### 400
Encabezados requeridos faltantes o inválidos
**Códigos de Error Posibles:**

**TYP-001** - header_error (HTTP 400)
  - `HDR-001`: Encabezado requerido faltante en la solicitud
  - `HDR-002`: Valor del encabezado demasiado corto
  - `HDR-003`: Valor del encabezado excede la longitud máxima
  - `HDR-004`: Formato del encabezado inválido


**Content-Type**: `application/json`

**Schema**: [`Response400`](#response400)

##### 204
Prioridad eliminada exitosamente

##### 404
Prioridad no encontrada - El ID especificado no existe en la base de datos
**Códigos de Error Posibles:**

**TYP-002** - resource_not_found (HTTP 404)
  - `RNF-001`: Recurso no encontrado por ID especificado
  - `RNF-002`: Recurso no encontrado después de una operación
  - `RNF-003`: Endpoint o ruta no existe en la API


**Content-Type**: `application/json`

**Schema**: [`Response404`](#response404)

---

### `GET` /priorities

**Listar todas las prioridades**

Obtiene la lista completa de prioridades disponibles. Requiere encabezados de validación (x-correlation-id, x-client-id, x-user-id).

**Tags**: `Prioridades`

**Operation ID**: `findAll`

#### Parámetros

| Nombre | Ubicación | Tipo | Requerido | Descripción |
|--------|-----------|------|-----------|-------------|
| `x-correlation-id` | header | `string (uuid)` | ✅ | Identificador único para correlación entre servicios. UUID v4 válido con 36 caracteres. |
| `x-request-id` | header | `string (uuid)` | ✅ | Identificador único de la solicitud. UUID v4 válido con 36 caracteres. |
| `x-transaction-id` | header | `string (uuid)` | ✅ | Identificador único de la transacción de negocio. UUID v4 válido con 36 caracteres. |

#### Respuestas

##### 400
Encabezados requeridos faltantes o inválidos
**Códigos de Error Posibles:**

**TYP-001** - header_error (HTTP 400)
  - `HDR-001`: Encabezado requerido faltante en la solicitud
  - `HDR-002`: Valor del encabezado demasiado corto
  - `HDR-003`: Valor del encabezado excede la longitud máxima
  - `HDR-004`: Formato del encabezado inválido


**Content-Type**: `application/json`

**Schema**: [`Response400`](#response400)

##### 200
Lista obtenida exitosamente

**Content-Type**: `*/*`

**Schema**: [`Response200`](#response200)

---

### `POST` /priorities

**Crear nueva prioridad**

Crea una nueva prioridad. El nombre debe ser único y cumplir validaciones (3-70 caracteres).

**Tags**: `Prioridades`

**Operation ID**: `save`

#### Parámetros

| Nombre | Ubicación | Tipo | Requerido | Descripción |
|--------|-----------|------|-----------|-------------|
| `x-correlation-id` | header | `string (uuid)` | ✅ | Identificador único para correlación entre servicios. UUID v4 válido con 36 caracteres. |
| `x-request-id` | header | `string (uuid)` | ✅ | Identificador único de la solicitud. UUID v4 válido con 36 caracteres. |
| `x-transaction-id` | header | `string (uuid)` | ✅ | Identificador único de la transacción de negocio. UUID v4 válido con 36 caracteres. |

#### Request Body

**✅ Obligatorio**

**Content-Type**: `application/json`

**Schema**: [`RequestBody`](#requestbody)

#### Respuestas

##### 201
Prioridad creada exitosamente. Header Location contiene la URI del nuevo recurso.

##### 409
Conflicto - Nombre duplicado. Ya existe una prioridad con ese nombre
**Códigos de Error Posibles:**

**TYP-003** - request_body_validation_error (HTTP 400/409)
  - `RBV-001`: Campo requerido faltante en el cuerpo de la solicitud
  - `RBV-002`: Campo enviado con valor vacío
  - `RBV-003`: Longitud del campo por debajo del mínimo requerido
  - `RBV-004`: Longitud del campo excede el máximo permitido
  - `RBV-005`: Valor duplicado detectado (violación de restricción única)


**Content-Type**: `application/json`

**Schema**: [`Response409`](#response409)

##### 400
Encabezados faltantes o datos de validación incorrectos
**Códigos de Error Posibles:**

**TYP-001** - header_error (HTTP 400)
  - `HDR-001`: Encabezado requerido faltante en la solicitud
  - `HDR-002`: Valor del encabezado demasiado corto
  - `HDR-003`: Valor del encabezado excede la longitud máxima
  - `HDR-004`: Formato del encabezado inválido

**Códigos de Error Posibles:**

**TYP-003** - request_body_validation_error (HTTP 400/409)
  - `RBV-001`: Campo requerido faltante en el cuerpo de la solicitud
  - `RBV-002`: Campo enviado con valor vacío
  - `RBV-003`: Longitud del campo por debajo del mínimo requerido
  - `RBV-004`: Longitud del campo excede el máximo permitido
  - `RBV-005`: Valor duplicado detectado (violación de restricción única)


**Content-Type**: `application/json`

**Schema**: [`Response400`](#response400)

---

## 📦 Schemas

### ErrorResponse

**Tipo**: `object`

#### Propiedades

| Nombre | Tipo | Requerido | Descripción | Validaciones |
|--------|------|-----------|-------------|--------------|
| `errors` | `object` | ❌ |  | - |


### PriorityDTO

DTO de Prioridad

**Tipo**: `object`

#### Propiedades

| Nombre | Tipo | Requerido | Descripción | Validaciones |
|--------|------|-----------|-------------|--------------|
| `idPriority` | `integer (int32)` | ❌ | Identificador único | - |
| `name` | `string` | ✅ | Nombre de la prioridad (único) | min: 3, max: 70 |
| `description` | `string` | ✅ | Descripción de la prioridad | min: 3, max: 70 |


## 📈 Códigos de Estado

| Código | Descripción | Endpoints |
|--------|-------------|-----------|
| `200` | OK - Solicitud exitosa | 3 |
| `201` | Created - Recurso creado exitosamente | 1 |
| `204` | No Content - Operación exitosa sin contenido | 1 |
| `400` | Bad Request - Solicitud inválida | 5 |
| `404` | Not Found - Recurso no encontrado | 3 |
| `409` | Conflict - Conflicto con el estado actual | 2 |

## 📄 Content Types Soportados

- `*/*`
- `application/json`

## 🏷️ Tags

### Prioridades
Operaciones CRUD para la gestión de prioridades

---

*Documentación generada automáticamente por MCP-QA*
