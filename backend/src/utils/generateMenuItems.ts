import * as fs from "fs";

// === Cargar IDs de restaurantes desde el archivo ===
const path = require("path");
const rawData = fs.readFileSync(
  path.join(__dirname, "restaurant_ids.txt"),
  "utf-8"
);
const lines = rawData.trim().split("\n");

const restaurantIds = lines
  .filter((line) => line.trim() !== "")
  .map((line) => {
    const parsed = JSON.parse(line);
    return parsed._id.$oid; // extrae solo el ObjectId en string
  });

const productosBase = [
  // ☕ Bebidas calientes
  {
    name: "Café Americano",
    category: "bebida caliente",
    ingredients: ["agua", "café"],
  },
  {
    name: "Espresso Simple",
    category: "bebida caliente",
    ingredients: ["espresso"],
  },
  {
    name: "Espresso Doble",
    category: "bebida caliente",
    ingredients: ["espresso"],
  },
  {
    name: "Capuccino",
    category: "bebida caliente",
    ingredients: ["espresso", "leche", "espuma"],
  },
  {
    name: "Latte Clásico",
    category: "bebida caliente",
    ingredients: ["espresso", "leche vaporizada"],
  },
  {
    name: "Mocha Chocolate",
    category: "bebida caliente",
    ingredients: ["espresso", "chocolate", "leche"],
  },
  {
    name: "Chocolate Caliente",
    category: "bebida caliente",
    ingredients: ["chocolate", "leche"],
  },
  {
    name: "Té Chai Latte",
    category: "bebida caliente",
    ingredients: ["té chai", "leche"],
  },

  // 🥶 Bebidas frías
  {
    name: "Café Helado",
    category: "bebida fría",
    ingredients: ["café frío", "hielo"],
  },
  {
    name: "Smoothie de Fresa",
    category: "bebida fría",
    ingredients: ["fresas", "yogurt", "hielo"],
  },
  {
    name: "Smoothie de Mango",
    category: "bebida fría",
    ingredients: ["mango", "yogurt", "hielo"],
  },
  {
    name: "Té Helado de Limón",
    category: "bebida fría",
    ingredients: ["té negro", "limón", "hielo"],
  },
  {
    name: "Frappuccino de Vainilla",
    category: "bebida fría",
    ingredients: ["café", "hielo", "vainilla"],
  },
  {
    name: "Cold Brew Clásico",
    category: "bebida fría",
    ingredients: ["café frío concentrado", "agua"],
  },

  // 🍰 Postres
  {
    name: "Cheesecake de Fresa",
    category: "postre",
    ingredients: ["queso crema", "fresa", "galleta"],
  },
  {
    name: "Brownie de Chocolate",
    category: "postre",
    ingredients: ["chocolate", "harina", "azúcar"],
  },
  {
    name: "Pastel de Zanahoria",
    category: "postre",
    ingredients: ["zanahoria", "harina", "nuez"],
  },
  {
    name: "Muffin de Arándano",
    category: "postre",
    ingredients: ["arándanos", "harina", "azúcar"],
  },
  {
    name: "Muffin de Chocolate",
    category: "postre",
    ingredients: ["chocolate", "harina", "azúcar"],
  },
  {
    name: "Galleta de Avena",
    category: "postre",
    ingredients: ["avena", "harina", "miel"],
  },

  // 🥐 Snacks
  {
    name: "Croissant de Mantequilla",
    category: "snack",
    ingredients: ["harina", "mantequilla"],
  },
  {
    name: "Croissant de Jamón y Queso",
    category: "snack",
    ingredients: ["jamón", "queso", "masa hojaldre"],
  },
  {
    name: "Sandwich de Pollo",
    category: "snack",
    ingredients: ["pollo", "lechuga", "pan"],
  },
  {
    name: "Sandwich Vegetariano",
    category: "snack",
    ingredients: ["vegetales", "pan integral", "queso"],
  },
  {
    name: "Empanada de Pollo",
    category: "snack",
    ingredients: ["pollo", "masa de empanada"],
  },
  {
    name: "Empanada de Espinaca",
    category: "snack",
    ingredients: ["espinaca", "queso", "masa"],
  },

  // 🍳 Desayunos
  {
    name: "Omelette de Jamón",
    category: "desayuno",
    ingredients: ["huevo", "jamón", "queso"],
  },
  {
    name: "Omelette Vegetariano",
    category: "desayuno",
    ingredients: ["huevo", "espinacas", "tomate"],
  },
  {
    name: "Waffles con Miel",
    category: "desayuno",
    ingredients: ["harina", "miel", "huevo"],
  },
  {
    name: "Tostadas Francesas",
    category: "desayuno",
    ingredients: ["pan", "huevo", "canela"],
  },
  {
    name: "Bagel con Queso Crema",
    category: "desayuno",
    ingredients: ["bagel", "queso crema"],
  },
  {
    name: "Burrito de Desayuno",
    category: "desayuno",
    ingredients: ["huevo", "frijol", "tortilla"],
  },
];

const adjetivosPorCategoria = {
  "bebida caliente": [
    "Grande",
    "Clásico",
    "Con leche de almendra",
    "Sin azúcar",
    "Especial",
    "Extra shot de espresso",
  ],
  "bebida fría": [
    "Grande",
    "Clásico",
    "Con leche de almendra",
    "Sin azúcar",
    "Especial",
  ],
  postre: [
    "Con extra de chocolate",
    "Clásico",
    "Sin azúcar",
    "Receta especial",
    "Con topping de frutas",
  ],
  snack: ["Clásico", "Especial", "Integral", "Artesanal"],
  desayuno: ["Clásico", "Especial", "Integral", "Relleno de queso"],
};

function generarMenuItems() {
  const items = [];

  for (const restaurantId of restaurantIds) {
    for (let i = 0; i < 20; i++) {
      // 20 productos por restaurante
      const base =
        productosBase[Math.floor(Math.random() * productosBase.length)];
      const adjetivosDisponibles =
        adjetivosPorCategoria[
          base.category as keyof typeof adjetivosPorCategoria
        ];
      const adjetivo =
        adjetivosDisponibles[
          Math.floor(Math.random() * adjetivosDisponibles.length)
        ];
      const precio = Math.floor(Math.random() * 30) + 20; // precio 20 a 50

      items.push({
        name: `${base.name} ${adjetivo}`,
        description: `Delicioso ${base.name.toLowerCase()} ${adjetivo.toLowerCase()}.`,
        price: precio,
        ingredients: base.ingredients,
        category: base.category,
        available: Math.random() > 0.05, // 95% chance de estar disponible
        restaurant_id: restaurantId,
      });
    }
  }

  return items;
}

// === Ejecutarlo y guardarlo ===
const menuItems = generarMenuItems();
const outputPath = "./src/utils/menuItems.json";

fs.writeFileSync(outputPath, JSON.stringify(menuItems, null, 2));
console.log(
  `✅ Archivo generado en ${outputPath} con ${menuItems.length} productos.`
);
