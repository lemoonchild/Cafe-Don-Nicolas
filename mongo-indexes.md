# 📄 `mongo-indexes.md` – Documentación de Índices en MongoDB

## 📌 Objetivo

Documentar y justificar el uso de **índices simples, compuestos, multikey, geoespaciales y de texto** implementados en las colecciones del sistema, conforme a la rúbrica de evaluación del proyecto.

## 📁 Colecciones y sus índices

### 🧑‍💼 `Users`

> Información de clientes y administradores.

#### Índices implementados:

1. **Índice de texto sobre `name`**

   ```ts
   db.users.createIndex({ name: "text" });
   ```

   - Justificación: permite búsquedas de usuarios por nombre.
   - Ejemplo de uso: `/api/users/search?nombre=juan`

2. **Índice geoespacial sobre `location`**
   ```ts
   db.users.createIndex({ location: "2dsphere" });
   ```
   - Justificación: permite encontrar restaurantes cercanos al usuario.
   - Ejemplo de uso: `$geoNear` en agregación para sugerencias.

### 🍽️ `Restaurants`

> Cada sucursal de Don Nicolás.

#### Índices implementados:

1. **Índice de texto sobre `name`**

   ```ts
   db.restaurants.createIndex({ name: "text" });
   ```

   - Justificación: permite búsqueda por nombre de sucursal.

2. **Índice geoespacial sobre `location`**
   ```ts
   db.restaurants.createIndex({ location: "2dsphere" });
   ```
   - Justificación: consultar restaurantes cercanos al cliente.

### 🍰 `MenuItems`

> Productos del menú asociados a cada restaurante.

#### Índices implementados:

1. **Índice compuesto sobre `name + restaurant_id`**

   ```ts
   db.menuitems.createIndex({ name: 1, restaurant_id: 1 });
   ```

   - Justificación: mejora búsquedas de productos por nombre dentro de una sucursal específica.

2. **Índice multikey sobre `ingredients`**
   ```ts
   db.menuitems.createIndex({ ingredients: 1 });
   ```
   - Justificación: permite consultar productos que contienen o excluyen ciertos ingredientes (útil para filtros alérgenos).

### 📦 `Orders`

> Pedidos realizados por los usuarios.

#### Índices implementados:

1. **Índice compuesto sobre `user_id + date`**

   ```ts
   db.orders.createIndex({ user_id: 1, date: -1 });
   ```

   - Justificación: mostrar historial de pedidos de un usuario en orden cronológico inverso (más recientes primero).

2. **Índice de texto sobre `status`**
   ```ts
   db.orders.createIndex({ status: "text" });
   ```
   - Justificación: búsqueda por estado textual (`pendiente`, `entregado`, etc.)

### ⭐ `Reviews`

> Reseñas que los usuarios dejan sobre restaurantes o pedidos.

#### Índices implementados:

1. **Índice compuesto sobre `restaurant_id + rating`**

   ```ts
   db.reviews.createIndex({ restaurant_id: 1, rating: -1 });
   ```

   - Justificación: útil para calcular promedio de calificaciones por restaurante y ordenar por calificación.

2. **Índice de texto sobre `comment`**
   ```ts
   db.reviews.createIndex({ comment: "text" });
   ```
   - Justificación: permite búsquedas dentro del contenido del comentario.
   - Ejemplo: `"excelente atención"` o `"pésimo servicio"`

## 📊 Resumen de tipos de índices utilizados

| Tipo de índice  | Colección                                   | Campos                       |
| --------------- | ------------------------------------------- | ---------------------------- |
| **Simple**      | `Users`, `Orders`                           | `name`, `status`             |
| **Compuesto**   | `MenuItems`, `Orders`, `Reviews`            | `name + restaurant_id`, etc. |
| **Multikey**    | `MenuItems`                                 | `ingredients`                |
| **Geoespacial** | `Users`, `Restaurants`                      | `location` (tipo GeoJSON)    |
| **Texto**       | `Users`, `Restaurants`, `Reviews`, `Orders` | `name`, `comment`, `status`  |

## ✅ Verificación

Todas las consultas que involucran búsquedas, filtros, proyecciones o agregaciones están diseñadas para **usar los índices definidos**. Antes de cerrar el proyecto se validará que **no existan `COLLSCAN`** innecesarios usando:

```js
db.coleccion.find({ ... }).explain("executionStats")
```
