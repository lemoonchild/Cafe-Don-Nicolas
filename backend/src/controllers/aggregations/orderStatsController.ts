import Order from "@models/Order";
import mongoose from "mongoose";
import { Request, Response } from "express";

export const totalSales = async (req: Request, res: Response) => {
  const result = await Order.aggregate([
    { $group: { _id: null, totalSales: { $sum: "$total" } } },
  ]);

  res.json({ totalSales: result[0]?.totalSales ?? 0 });
};

export const averageOrderValue = async (req: Request, res: Response) => {
  const result = await Order.aggregate([
    { $group: { _id: null, avgOrderValue: { $avg: "$total" } } },
  ]);

  res.json({ avgOrderValue: result[0]?.avgOrderValue ?? 0 });
};

export const countOrdersByStatus = async (req: Request, res: Response) => {
  const result = await Order.aggregate([
    { $group: { _id: "$status", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
  ]);

  res.json(result);
};

export const ordersWithRestaurant = async (req: Request, res: Response) => {
  const limit = parseInt(req.query.limit as string) || 10; // default 100 documentos

  const result = await Order.aggregate([
    {
      $lookup: {
        from: "Restaurants",
        localField: "restaurant_id",
        foreignField: "_id",
        as: "restaurantInfo",
      },
    },
    { $unwind: "$restaurantInfo" },
    {
      $project: {
        total: 1,
        status: 1,
        date: 1,
        "restaurantInfo.name": 1,
        "restaurantInfo.address": 1,
      },
    },
    { $limit: limit },
  ]);

  res.json(result);
};

export const unwindOrderItems = async (req: Request, res: Response) => {
  const limit = parseInt(req.query.limit as string) || 10;

  const result = await Order.aggregate([
    { $unwind: "$items" },
    {
      $lookup: {
        from: "Users",
        localField: "user_id",
        foreignField: "_id",
        as: "userInfo",
      },
    },
    { $unwind: "$userInfo" },
    {
      $lookup: {
        from: "Restaurants",
        localField: "restaurant_id",
        foreignField: "_id",
        as: "restaurantInfo",
      },
    },
    { $unwind: "$restaurantInfo" },
    {
      $project: {
        user_id: 1,
        "userInfo.name": 1,
        restaurant_id: 1,
        "restaurantInfo.name": 1,
        "restaurantInfo.address": 1,
        "items.name": 1,
        "items.quantity": 1,
        "items.unit_price": 1,
        date: 1,
        status: 1,
      },
    },
    { $limit: limit },
  ]);

  res.json(result);
};
