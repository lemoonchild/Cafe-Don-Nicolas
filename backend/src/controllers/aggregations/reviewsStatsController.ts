import Review from "@models/Review";
import mongoose from "mongoose";
import { Request, Response } from "express";

// Promedio de rating por restaurante
export const averageRatingByRestaurant = async (
  req: Request,
  res: Response
) => {
  const { restaurantId } = req.params;

  if (!mongoose.Types.ObjectId.isValid(restaurantId)) {
    return res.status(400).json({ message: "ID de restaurante inválido." });
  }

  const result = await Review.aggregate([
    { $match: { restaurant_id: new mongoose.Types.ObjectId(restaurantId) } },
    { $group: { _id: "$restaurant_id", avgRating: { $avg: "$rating" } } },
  ]);

  if (result.length === 0) {
    return res
      .status(404)
      .json({ message: "No hay reseñas para este restaurante." });
  }

  res.json({ restaurantId, avgRating: result[0].avgRating });
};

// Número de reseñas por restaurante
export const countReviewsByRestaurant = async (req: Request, res: Response) => {
  const result = await Review.aggregate([
    { $group: { _id: "$restaurant_id", count: { $sum: 1 } } },
    {
      $lookup: {
        from: "Restaurants", // collection name for restaurants
        localField: "_id",
        foreignField: "_id",
        as: "restaurant",
      },
    },
    { $unwind: "$restaurant" },
    {
      $project: {
        count: 1,
        restaurantName: "$restaurant.name",
      },
    },
    { $sort: { count: -1 } },
  ]);

  res.json(result);
};

// Reseñas con datos de usuario
export const reviewsWithUserInfo = async (req: Request, res: Response) => {
  const result = await Review.aggregate([
    {
      $lookup: {
        from: "Users", // nombre de la colección en MongoDB
        localField: "user_id",
        foreignField: "_id",
        as: "userInfo",
      },
    },
    { $unwind: "$userInfo" },
    {
      $project: {
        rating: 1,
        comment: 1,
        createdAt: 1,
        "userInfo.name": 1,
        "userInfo.email": 1,
      },
    },
    { $sort: { createdAt: -1 } },
  ]);

  res.json(result);
};
