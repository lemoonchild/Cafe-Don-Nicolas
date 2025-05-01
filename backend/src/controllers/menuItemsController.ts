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
  
  res.json(menuItems.map(item => ({
    ...item.toObject(),
    image_url: item.image_id ? `/api/images/${item.image_id}` : null
  })));
};

export const getMenuItemById = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findById(req.params.id);
  if (!menuItem)
    return res.status(404).json({ message: "Producto no encontrado" });
  
  res.json({
    ...menuItem.toObject(),
    image_url: menuItem.image_id ? `/api/images/${menuItem.image_id}` : null
  });
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

export const createManyMenuItems = async (req: Request, res: Response) => {
  const { items } = req.body;

  if (!items || !Array.isArray(items) || items.length === 0) {
    return res
      .status(400)
      .json({ message: "Debes enviar 'items' como un array no vacío." });
  }

  try {
    const result = await MenuItem.insertMany(items);
    res
      .status(201)
      .json({ message: `Se crearon ${result.length} productos.`, result });
  } catch (error) {
    res.status(500).json({ message: "Error al crear productos.", error });
  }
};

export const updateManyMenuItems = async (req: Request, res: Response) => {
  const { filter, update } = req.body;

  if (!filter || !update) {
    return res
      .status(400)
      .json({ message: "Debes enviar 'filter' y 'update'." });
  }

  const result = await MenuItem.updateMany(filter, update);
  res.json({
    message: `Se actualizaron ${result.modifiedCount} productos.`,
    result,
  });
};

export const updateManyMenuItemsByIds = async (req: Request, res: Response) => {
  const { ids, update } = req.body;

  if (!ids || !Array.isArray(ids) || !update) {
    return res
      .status(400)
      .json({ message: "Debes enviar 'ids' (array) y 'update'." });
  }

  const result = await MenuItem.updateMany({ _id: { $in: ids } }, update);
  res.json({
    message: `Se actualizaron ${result.modifiedCount} productos.`,
    result,
  });
};

export const deleteManyMenuItems = async (req: Request, res: Response) => {
  const { filter } = req.body;

  if (!filter) {
    return res.status(400).json({ message: "Debes enviar 'filter'." });
  }

  const result = await MenuItem.deleteMany(filter);
  res.json({
    message: `Se eliminaron ${result.deletedCount} productos.`,
    result,
  });
};

export const deleteManyMenuItemsByIds = async (req: Request, res: Response) => {
  const { ids } = req.body;

  if (!ids || !Array.isArray(ids)) {
    return res.status(400).json({ message: "Debes enviar 'ids' (array)." });
  }

  const result = await MenuItem.deleteMany({ _id: { $in: ids } });
  res.json({
    message: `Se eliminaron ${result.deletedCount} productos.`,
    result,
  });
};

// PATCH /api/menu-items/add-ingredient/:id
export const addIngredient = async (req: Request, res: Response) => {
  const { ingredient } = req.body;

  if (!ingredient) {
    return res.status(400).json({ message: "Debes enviar el 'ingredient'." });
  }

  const result = await MenuItem.findByIdAndUpdate(
    req.params.id,
    { $push: { ingredients: ingredient } },
    { new: true }
  );

  if (!result) {
    return res.status(404).json({ message: "MenuItem no encontrado." });
  }

  res.json({ message: "Ingrediente agregado correctamente.", result });
};

// PATCH /api/menu-items/remove-ingredient/:id
export const removeIngredient = async (req: Request, res: Response) => {
  const { ingredient } = req.body;

  if (!ingredient) {
    return res.status(400).json({ message: "Debes enviar el 'ingredient'." });
  }

  const result = await MenuItem.findByIdAndUpdate(
    req.params.id,
    { $pull: { ingredients: ingredient } },
    { new: true }
  );

  if (!result) {
    return res.status(404).json({ message: "MenuItem no encontrado." });
  }

  res.json({ message: "Ingrediente eliminado correctamente.", result });
};

// PATCH /api/menu-items/add-ingredient-unique/:id
export const addIngredientUnique = async (req: Request, res: Response) => {
  const { ingredient } = req.body;

  if (!ingredient) {
    return res.status(400).json({ message: "Debes enviar el 'ingredient'." });
  }

  const result = await MenuItem.findByIdAndUpdate(
    req.params.id,
    { $addToSet: { ingredients: ingredient } },
    { new: true }
  );

  if (!result) {
    return res.status(404).json({ message: "MenuItem no encontrado." });
  }

  res.json({
    message: "Ingrediente agregado (únicamente si no existía).",
    result,
  });
};
