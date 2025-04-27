import { Request, Response } from "express";
import Order from "@models/Order";
import mongoose from "mongoose";

export const getOrders = async (req: Request, res: Response) => {
  const {
    user_id,
    restaurant_id,
    status,
    dateMin,
    dateMax,
    sort,
    order,
    limit,
    skip,
    fields,
  } = req.query;

  let query: any = {};

  if (user_id && mongoose.Types.ObjectId.isValid(user_id.toString())) {
    query.user_id = user_id;
  }

  if (
    restaurant_id &&
    mongoose.Types.ObjectId.isValid(restaurant_id.toString())
  ) {
    query.restaurant_id = restaurant_id;
  }

  if (status) {
    query.status = status;
  }

  if (dateMin || dateMax) {
    query.date = {};
    if (dateMin) query.date.$gte = new Date(dateMin.toString());
    if (dateMax) query.date.$lte = new Date(dateMax.toString());
  }

  let cursor = Order.find(query);

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

  if (sort)
    cursor = cursor.sort({ [sort.toString()]: order === "desc" ? -1 : 1 });
  if (limit) cursor = cursor.limit(parseInt(limit.toString()));
  if (skip) cursor = cursor.skip(parseInt(skip.toString()));

  const orders = await cursor.exec();
  res.json(orders);
};

export const getOrderById = async (req: Request, res: Response) => {
  const order = await Order.findById(req.params.id);
  if (!order) return res.status(404).json({ message: "Orden no encontrada" });
  res.json(order);
};

export const createOrder = async (req: Request, res: Response) => {
  const order = new Order(req.body);
  await order.save();
  res.status(201).json(order);
};

export const updateOrder = async (req: Request, res: Response) => {
  const order = await Order.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
  });
  if (!order) return res.status(404).json({ message: "Orden no encontrada" });
  res.json(order);
};

export const deleteOrder = async (req: Request, res: Response) => {
  const order = await Order.findByIdAndDelete(req.params.id);
  if (!order) return res.status(404).json({ message: "Orden no encontrada" });
  res.json({ message: "Orden eliminada correctamente" });
};

export const createManyOrders = async (req: Request, res: Response) => {
  const { items } = req.body;

  if (!items || !Array.isArray(items) || items.length === 0) {
    return res.status(400).json({ message: "Debes enviar 'items' como un array no vacío." });
  }

  try {
    const result = await Order.insertMany(items);
    res.status(201).json({ message: `Se crearon ${result.length} ordenes.`, result });
  } catch (error) {
    res.status(500).json({ message: "Error al crear ordenes.", error });
  }
};

export const updateManyOrders = async (req: Request, res: Response) => {
  const { filter, update } = req.body;

  if (!filter || !update) {
    return res.status(400).json({ message: "Debes enviar 'filter' y 'update'." });
  }

  const result = await Order.updateMany(filter, update);
  res.json({ message: `Se actualizaron ${result.modifiedCount} órdenes.`, result });
};

export const updateManyOrdersByIds = async (req: Request, res: Response) => {
  const { ids, update } = req.body;

  if (!ids || !Array.isArray(ids) || !update) {
    return res.status(400).json({ message: "Debes enviar 'ids' (array) y 'update'." });
  }

  const result = await Order.updateMany(
    { _id: { $in: ids } },
    update
  );
  res.json({ message: `Se actualizaron ${result.modifiedCount} órdenes.`, result });
};

export const deleteManyOrders = async (req: Request, res: Response) => {
  const { filter } = req.body;

  if (!filter) {
    return res.status(400).json({ message: "Debes enviar 'filter'." });
  }

  const result = await Order.deleteMany(filter);
  res.json({ message: `Se eliminaron ${result.deletedCount} órdenes.`, result });
};

export const deleteManyOrdersByIds = async (req: Request, res: Response) => {
  const { ids } = req.body;

  if (!ids || !Array.isArray(ids)) {
    return res.status(400).json({ message: "Debes enviar 'ids' (array)." });
  }

  const result = await Order.deleteMany(
    { _id: { $in: ids } }
  );
  res.json({ message: `Se eliminaron ${result.deletedCount} órdenes.`, result });
};
