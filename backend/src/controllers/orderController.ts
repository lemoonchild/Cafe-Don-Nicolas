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
