import { Request, Response } from "express";
import Restaurant from "@models/Restaurant";

export const countRestaurants = async (req: Request, res: Response) => {
  const total = await Restaurant.countDocuments();
  res.json({ total });
};

export const countRestaurantsWithImage = async (
  req: Request,
  res: Response
) => {
  const total = await Restaurant.countDocuments({
    image_id: { $exists: true },
  });
  res.json({ total });
};

export const countRestaurantsOpenNow = async (req: Request, res: Response) => {
  const now = new Date();
  const currentTime = now.toTimeString().substring(0, 5); // formato HH:mm

  const total = await Restaurant.countDocuments({
    $expr: {
      $and: [
        { $lte: ["$schedule.open", currentTime] },
        { $gte: ["$schedule.close", currentTime] },
      ],
    },
  });

  res.json({ openNow: total });
};

export const groupRestaurantsByOpenHour = async (
  req: Request,
  res: Response
) => {
  const result = await Restaurant.aggregate([
    {
      $group: {
        _id: "$schedule.open",
        count: { $sum: 1 },
      },
    },
    {
      $project: {
        hour: "$_id",
        count: 1,
        _id: 0,
      },
    },
    { $sort: { hour: 1 } },
  ]);

  res.json(result);
};
