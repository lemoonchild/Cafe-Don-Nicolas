import { Request, Response } from "express";
import MenuItem from "@models/MenuItem";
import mongoose from "mongoose";

// Contar productos disponibles
export const countAvailableMenuItems = async (req: Request, res: Response) => {
  const count = await MenuItem.countDocuments({ available: true });
  res.json({ count });
};

// Promedio de precio de todos los productos
export const averagePriceMenuItems = async (req: Request, res: Response) => {
  const result = await MenuItem.aggregate([
    { $group: { _id: null, avgPrice: { $avg: "$price" } } },
  ]);
  res.json({ avgPrice: result[0]?.avgPrice ?? 0 });
};

// Contar productos por categoría
export const countMenuItemsByCategory = async (req: Request, res: Response) => {
  const result = await MenuItem.aggregate([
    { $group: { _id: "$category", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
  ]);
  res.json(result);
};

// Promedio de precio por categoría
export const averagePriceByCategory = async (req: Request, res: Response) => {
  const result = await MenuItem.aggregate([
    { $group: { _id: "$category", avgPrice: { $avg: "$price" } } },
    { $sort: { avgPrice: -1 } },
  ]);
  res.json(result);
};

// Ingredientes más comunes
export const topIngredients = async (req: Request, res: Response) => {
  const result = await MenuItem.aggregate([
    { $unwind: "$ingredients" },
    { $group: { _id: "$ingredients", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
    { $limit: 10 }, // Top 10 ingredientes
  ]);
  res.json(result);
};

// Productos agrupados por rango de precio
export const priceRangeMenuItems = async (req: Request, res: Response) => {
  const result = await MenuItem.aggregate([
    {
      $bucket: {
        groupBy: "$price",
        boundaries: [0, 20, 40, 60, 80, 100],
        default: "Más de 100",
        output: { count: { $sum: 1 } },
      },
    },
  ]);
  res.json(result);
};

// Productos agrupados por restaurante
export const menuItemsByRestaurant = async (req: Request, res: Response) => {
  const result = await MenuItem.aggregate([
    {
      $lookup: {
        from: "Restaurants", // nombre de la colección de restaurantes
        localField: "restaurant_id",
        foreignField: "_id",
        as: "restaurant",
      },
    },
    { $unwind: "$restaurant" },
    {
      $group: {
        _id: "$restaurant_id",
        count: { $sum: 1 },
        name: { $first: "$restaurant.name" },
      },
    },
    { $sort: { count: -1 } },
  ]);
  res.json(result);
};
