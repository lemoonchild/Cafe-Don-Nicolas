import { Request, Response } from "express";
import Restaurant from "@models/Restaurant";
import mongoose from "mongoose";

export const getRestaurants = async (req: Request, res: Response) => {
  const {
    search,
    near,
    maxDistance,
    hasImage,
    openAt,
    sort,
    order,
    limit,
    skip,
    fields,
    ids,
  } = req.query;

  let query: any = {};

  //Text search
  if (search) query.$text = { $search: search.toString() };

  // Has image
  if (hasImage === "true") query.image_id = { $exists: true };

  // Horario abierto (openAt en formato HH:mm)
  if (openAt) {
    query["$expr"] = {
      $and: [
        { $lte: ["$schedule.open", openAt.toString()] },
        { $gte: ["$schedule.close", openAt.toString()] },
      ],
    };
  }

  // Filtrar por múltiples IDs
  if (ids) {
    const idArray = ids
      .toString()
      .split(",")
      .filter((id) => mongoose.Types.ObjectId.isValid(id));
    query._id = { $in: idArray };
  }

  let cursor: any;

  // GeoNear si se solicita
  if (near && typeof near === "string") {
    const [lat, lng] = near.split(",").map(Number);
    const distance = parseInt(maxDistance?.toString() || "5000");

    const pipeline: any[] = [
      {
        $geoNear: {
          near: { type: "Point", coordinates: [lng, lat] },
          distanceField: "dist.calculated",
          maxDistance: distance,
          spherical: true,
          query,
        },
      },
    ];

    if (fields) {
      const project = Object.fromEntries(
        fields
          .toString()
          .split(",")
          .map((f) => [f, 1])
      );
      pipeline.push({ $project: project });
    }

    if (sort) {
      pipeline.push({
        $sort: { [sort.toString()]: order === "desc" ? -1 : 1 },
      });
    }

    if (skip) {
      pipeline.push({
        $skip: parseInt(skip.toString()),
      });
    }

    if (limit) {
      pipeline.push({
        $limit: parseInt(limit.toString()),
      });
    }

    cursor = Restaurant.aggregate(pipeline);
    const results = await cursor.exec();
    return res.json(results);
  }

  // Si no hay geo, usar .find()
  cursor = Restaurant.find(query);

  if (sort)
    cursor = cursor.sort({ [sort.toString()]: order === "desc" ? -1 : 1 });
  if (limit) cursor = cursor.limit(parseInt(limit.toString()));
  if (skip) cursor = cursor.skip(parseInt(skip.toString()));
  if (fields) {
    const projection = Object.fromEntries(
      fields
        .toString()
        .split(",")
        .map((f) => [f, 1])
    );
    cursor = cursor.select(projection);
  }

  const restaurants = await cursor.exec();
  res.json(restaurants);
};

export const getRestaurantById = async (req: Request, res: Response) => {
  const restaurant = await Restaurant.findById(req.params.id);
  if (!restaurant)
    return res.status(404).json({ message: "Restaurante no encontrado" });
  res.json(restaurant);
};

export const createRestaurant = async (req: Request, res: Response) => {
  const restaurant = new Restaurant(req.body);
  await restaurant.save();
  res.status(201).json(restaurant);
};

export const updateRestaurant = async (req: Request, res: Response) => {
  const restaurant = await Restaurant.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true }
  );
  if (!restaurant)
    return res.status(404).json({ message: "Restaurante no encontrado" });
  res.json(restaurant);
};

export const deleteRestaurant = async (req: Request, res: Response) => {
  const restaurant = await Restaurant.findByIdAndDelete(req.params.id);
  if (!restaurant)
    return res.status(404).json({ message: "Restaurante no encontrado" });
  res.json({ message: "Restaurante eliminado correctamente" });
};
