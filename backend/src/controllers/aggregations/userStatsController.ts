import { Request, Response } from "express";
import User from "@models/User";

export const countUsers = async (req: Request, res: Response) => {
  try {
    const total = await User.countDocuments();
    res.json({ total });
  } catch (error) {
    res.status(500).json({ message: "Error al contar usuarios.", error });
  }
};

export const countUsersByRole = async (req: Request, res: Response) => {
  try {
    const result = await User.aggregate([
      {
        $group: {
          _id: "$role",
          count: { $sum: 1 },
        },
      },
      {
        $project: {
          role: "$_id",
          count: 1,
          _id: 0,
        },
      },
    ]);
    res.json(result);
  } catch (error) {
    res
      .status(500)
      .json({ message: "Error al contar usuarios por rol.", error });
  }
};
