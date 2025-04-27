import * as fs from "fs";
import * as path from "path";

// Cargar usuarios, restaurantes y menuItems
const userIds = JSON.parse(
  fs.readFileSync(path.join(__dirname, "cdn.users.json"), "utf-8")
);
const restaurantIds = JSON.parse(
  fs.readFileSync(path.join(__dirname, "cdn.restaurants.json"), "utf-8")
);
const menuItems = JSON.parse(
  fs.readFileSync(path.join(__dirname, "cdn.menuItems.json"), "utf-8")
);

// Estados posibles de un pedido
const statuses = ["pendiente", "preparando", "entregado", "cancelado"];

// Función para generar fecha aleatoria en el último año
function randomDate(start: Date, end: Date) {
  return new Date(
    start.getTime() + Math.random() * (end.getTime() - start.getTime())
  );
}

// Generador de órdenes
function generarOrders() {
  const orders = [];
  const totalOrders = 50000;

  for (let i = 0; i < totalOrders; i++) {
    const user = userIds[Math.floor(Math.random() * userIds.length)]._id;
    const restaurant =
      restaurantIds[Math.floor(Math.random() * restaurantIds.length)]._id.$oid;

    // Filtrar productos disponibles para ese restaurante
    const productosRestaurante = menuItems.filter(
      (item: { restaurant_id: string }) => item.restaurant_id === restaurant
    );

    // Seleccionar de 1 a 5 productos aleatorios
    const cantidadProductos = Math.floor(Math.random() * 5) + 1;
    const productosSeleccionados = [];

    let total = 0;

    for (let j = 0; j < cantidadProductos; j++) {
      const producto =
        productosRestaurante[
          Math.floor(Math.random() * productosRestaurante.length)
        ];
      const cantidad = Math.floor(Math.random() * 3) + 1; // de 1 a 3 unidades

      productosSeleccionados.push({
        product_id: producto._id,
        name: producto.name,
        quantity: cantidad,
        unit_price: producto.price,
      });

      total += cantidad * producto.price;
    }

    const order = {
      user_id: user,
      restaurant_id: restaurant,
      date: randomDate(new Date(2023, 0, 1), new Date()), // fechas entre enero 2023 y hoy
      status: statuses[Math.floor(Math.random() * statuses.length)],
      total: total,
      items: productosSeleccionados,
    };

    orders.push(order);
  }

  return orders;
}

// Generar y guardar
const orders = generarOrders();
const outputPath = "./src/utils/orders.json";

fs.writeFileSync(outputPath, JSON.stringify(orders, null, 2));
console.log(
  `✅ Archivo generado en ${outputPath} con ${orders.length} órdenes.`
);
