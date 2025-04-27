import * as fs from "fs";

const restaurantesBase = [
  {
    name: "Don Nicolás Zona 1",
    address: "5ta Avenida 10-55, Zona 1, Ciudad de Guatemala",
    coordinates: [-90.5133, 14.6349],
  },
  {
    name: "Don Nicolás Zona 10",
    address: "14 Calle 5-33, Zona 10, Ciudad de Guatemala",
    coordinates: [-90.5124, 14.5831],
  },
  {
    name: "Don Nicolás Zona 11",
    address: "Calzada Roosevelt 7-22, Zona 11, Ciudad de Guatemala",
    coordinates: [-90.5614, 14.6095],
  },
  {
    name: "Don Nicolás Zona 13",
    address: "Avenida La Reforma 8-66, Zona 13, Ciudad de Guatemala",
    coordinates: [-90.5067, 14.5985],
  },
  {
    name: "Don Nicolás Zona 14",
    address: "7a Avenida 15-20, Zona 14, Ciudad de Guatemala",
    coordinates: [-90.5002, 14.5825],
  },
  {
    name: "Don Nicolás Antigua",
    address: "5a Avenida Norte 29, Antigua Guatemala",
    coordinates: [-90.7343, 14.5586],
  },
  {
    name: "Don Nicolás Xela",
    address: "12 Avenida 3-45, Quetzaltenango",
    coordinates: [-91.5189, 14.8348],
  },
  {
    name: "Don Nicolás Chimaltenango",
    address: "2a Calle 4-56, Chimaltenango",
    coordinates: [-90.82, 14.6594],
  },
  {
    name: "Don Nicolás Escuintla",
    address: "Avenida Centroamérica 2-18, Escuintla",
    coordinates: [-90.7903, 14.305],
  },
  {
    name: "Don Nicolás Puerto Barrios",
    address: "10a Avenida 5-11, Puerto Barrios",
    coordinates: [-88.5976, 15.717],
  },
  {
    name: "Don Nicolás Cobán",
    address: "3a Avenida 6-77, Cobán",
    coordinates: [-90.3693, 15.4714],
  },
  {
    name: "Don Nicolás Mazatenango",
    address: "5a Calle 2-44, Mazatenango",
    coordinates: [-91.5076, 14.5312],
  },
  {
    name: "Don Nicolás Totonicapán",
    address: "1a Calle 5-20, Totonicapán",
    coordinates: [-91.3652, 14.9119],
  },
  {
    name: "Don Nicolás Jalapa",
    address: "2a Avenida 3-55, Jalapa",
    coordinates: [-89.9906, 14.6325],
  },
  {
    name: "Don Nicolás Zacapa",
    address: "4a Calle 7-23, Zacapa",
    coordinates: [-89.5354, 14.9728],
  },
  {
    name: "Don Nicolás Jutiapa",
    address: "5a Avenida 1-13, Jutiapa",
    coordinates: [-89.8957, 14.2905],
  },
  {
    name: "Don Nicolás Santa Rosa",
    address: "3a Calle 6-33, Cuilapa",
    coordinates: [-90.3025, 14.2722],
  },
  {
    name: "Don Nicolás Huehuetenango",
    address: "2a Avenida 4-17, Huehuetenango",
    coordinates: [-91.4767, 15.319],
  },
  {
    name: "Don Nicolás San Marcos",
    address: "6a Avenida 8-90, San Marcos",
    coordinates: [-91.7993, 14.9664],
  },
  {
    name: "Don Nicolás Sololá",
    address: "7a Calle 3-11, Sololá",
    coordinates: [-91.1832, 14.7744],
  },
  {
    name: "Don Nicolás Retalhuleu",
    address: "1a Avenida 2-66, Retalhuleu",
    coordinates: [-91.6857, 14.5347],
  },
  {
    name: "Don Nicolás Chiquimula",
    address: "4a Avenida 5-19, Chiquimula",
    coordinates: [-89.5423, 14.8009],
  },
  {
    name: "Don Nicolás Alta Verapaz",
    address: "6a Calle 8-24, Cobán",
    coordinates: [-90.3693, 15.4714],
  },
  {
    name: "Don Nicolás Petén",
    address: "3a Avenida 2-45, Flores",
    coordinates: [-89.8865, 16.9256],
  },
  {
    name: "Don Nicolás Sacatepéquez",
    address: "2a Calle 4-10, Antigua Guatemala",
    coordinates: [-90.7343, 14.5586],
  },
];

function randomHora(min: number, max: number) {
  const hora = Math.floor(Math.random() * (max - min + 1)) + min;
  return hora.toString().padStart(2, "0") + ":00";
}

function generarRestaurants() {
  return restaurantesBase.map((r) => ({
    name: r.name,
    address: r.address,
    location: {
      type: "Point",
      coordinates: r.coordinates,
    },
    schedule: {
      open: randomHora(5, 10), // entre 5:00 y 10:00
      close: randomHora(17, 22), // entre 17:00 y 22:00
    },
  }));
}

const restaurants = generarRestaurants();
const outputPath = "./src/utils/restaurants.json";
fs.writeFileSync(outputPath, JSON.stringify(restaurants, null, 2));
console.log(`Archivo JSON generado en ${outputPath}`);
