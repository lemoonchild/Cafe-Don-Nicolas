import { Request, Response } from "express";
import MenuItem from "@models/MenuItem";
import mongoose from "mongoose";

export const getMenuItems = async (req: Request, res: Response) => {
  const {
    search,
    restaurant_id,
    category,
    available,
    priceMin,
    priceMax,
    ingredient,
    sort,
    order,
    limit,
    skip,
    fields,
  } = req.query;

  let query: any = {};

  // Búsqueda textual
  if (search) query.$text = { $search: search.toString() };

  // Filtrar por restaurante
  if (
    restaurant_id &&
    mongoose.Types.ObjectId.isValid(restaurant_id.toString())
  ) {
    query.restaurant_id = restaurant_id;
  }

  // Categoría
  if (category) query.category = category;

  // Disponibilidad
  if (available !== undefined) query.available = available === "true";

  // Rango de precios
  if (priceMin || priceMax) {
    query.price = {};
    if (priceMin) query.price.$gte = parseFloat(priceMin.toString());
    if (priceMax) query.price.$lte = parseFloat(priceMax.toString());
  }

  // Buscar por ingrediente
  if (ingredient) {
    const ingredientsArray = ingredient.toString().split(",");
    query.ingredients = { $in: ingredientsArray };
  }

  let cursor = MenuItem.find(query);

  // Proyección de campos
  if (fields) {
    const projection = Object.fromEntries(
      fields
        .toString()
        .split(",")
        .map((f) => [f, 1])
    );
    cursor = cursor.select(projection);
  }

  // Ordenar
  if (sort)
    cursor = cursor.sort({ [sort.toString()]: order === "desc" ? -1 : 1 });

  // Paginación
  if (limit) cursor = cursor.limit(parseInt(limit.toString()));
  if (skip) cursor = cursor.skip(parseInt(skip.toString()));

  const menuItems = await cursor.exec();
  res.json(menuItems);
};

export const getMenuItemById = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findById(req.params.id);
  if (!menuItem)
    return res.status(404).json({ message: "Producto no encontrado" });
  res.json(menuItem);
};

export const createMenuItem = async (req: Request, res: Response) => {
  const menuItem = new MenuItem(req.body);
  await menuItem.save();
  res.status(201).json(menuItem);
};

export const updateMenuItem = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
  });
  if (!menuItem)
    return res.status(404).json({ message: "Producto no encontrado" });
  res.json(menuItem);
};

export const deleteMenuItem = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findByIdAndDelete(req.params.id);
  if (!menuItem)
    return res.status(404).json({ message: "Producto no encontrado" });
  res.json({ message: "Producto eliminado correctamente" });
};
