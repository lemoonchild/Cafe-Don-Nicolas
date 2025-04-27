import * as fs from "fs";

// Lista de 30 nombres
const nombres = [
  "Alex",
  "Taylor",
  "Jordan",
  "Casey",
  "Morgan",
  "Sam",
  "Cameron",
  "Drew",
  "Riley",
  "Charlie",
  "Jamie",
  "Skyler",
  "Devin",
  "Kendall",
  "Avery",
  "Elliot",
  "Logan",
  "Dakota",
  "Rowan",
  "Quinn",
  "Harper",
  "Peyton",
  "Sage",
  "Emerson",
  "Finley",
  "Reese",
  "Tatum",
  "Blake",
  "Hayden",
  "Parker",
];

// Lista de 30 apellidos
const apellidos = [
  "Smith",
  "Johnson",
  "Williams",
  "Brown",
  "Jones",
  "Garcia",
  "Miller",
  "Davis",
  "Rodriguez",
  "Martinez",
  "Hernandez",
  "Lopez",
  "Gonzalez",
  "Wilson",
  "Anderson",
  "Thomas",
  "Taylor",
  "Moore",
  "Jackson",
  "Martin",
  "Lee",
  "Perez",
  "Thompson",
  "White",
  "Harris",
  "Sanchez",
  "Clark",
  "Ramirez",
  "Lewis",
  "Robinson",
];

// Función para generar coordenadas aleatorias en Guatemala
function generarCoordenadasGuatemala() {
  const lng = -92 + Math.random() * 4; // Entre -92 y -88
  const lat = 13.5 + Math.random() * 4; // Entre 13.5 y 17.5
  return [lng, lat];
}

// Generar los usuarios
function generarUsuarios() {
  const usuarios = [];

  for (let i = 0; i < 500; i++) {
    const nombre = nombres[Math.floor(Math.random() * nombres.length)];
    const apellido = apellidos[Math.floor(Math.random() * apellidos.length)];
    const email = `${nombre.toLowerCase()}.${apellido.toLowerCase()}${i}@example.com`;

    const rol = i < 5 ? "admin" : "cliente"; // 5 primeros admins

    usuarios.push({
      name: `${nombre} ${apellido}`,
      email,
      role: rol,
      location: {
        type: "Point",
        coordinates: generarCoordenadasGuatemala(),
      },
    });
  }

  return usuarios;
}

// Crear los usuarios
const usuarios = generarUsuarios();

// Guardar en JSON
const outputPath = "./src/utils/users.json";
fs.writeFileSync(outputPath, JSON.stringify(usuarios, null, 2));
console.log(`Archivo JSON generado en ${outputPath}`);
