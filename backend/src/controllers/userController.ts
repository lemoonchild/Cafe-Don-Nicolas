import { Request, Response } from "express";
import User from "@models/User.ts";
import mongoose from "mongoose";

//GET /api/users
export const getUsers = async (req: Request, res: Response) => {
  try {
    const {
      search,
      role,
      near,
      maxDistance,
      sort,
      order,
      limit,
      skip,
      email,
      hasLocation,
      fields,
    } = req.query;

    const query: any = {};

    if (search) query.$text = { $search: search.toString() };
    if (role) query.role = role;
    if (email) query.email = email;
    if (hasLocation) query.location = { $exists: true };

    let cursor = User.find(query);

    //GeoNear
    if (near && typeof near === "string") {
      const [latitude, longitude] = near.split(",").map(Number);
      const distance = parseInt(maxDistance?.toString() || "5000"); // Distancia predeterminada: 5km

      const pipeline: any[] = [
        {
          $geoNear: {
            near: { type: "Point", coordinates: [longitude, latitude] },
            distanceField: "dist.calculated",
            maxDistance: distance,
            spherical: true,
            query: query,
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
        pipeline.push({ $skip: parseInt(skip.toString()) });
      }

      if (limit) {
        pipeline.push({ $limit: parseInt(limit.toString()) });
      }

      const aggQuery = User.aggregate(pipeline);
      const result = await aggQuery.exec();
      return res
        .status(200)
        .json({ msg: "Usuarios cercanos obtenidos correctamente.", result });
    }

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

    //Sort
    if (sort)
      cursor = cursor.sort({ [sort.toString()]: order === "desc" ? -1 : 1 });
    if (limit) cursor = cursor.limit(parseInt(limit.toString()));
    if (skip) cursor = cursor.skip(parseInt(skip.toString()));

    const users = await cursor.exec();
    res
      .status(200)
      .json({ msg: "Lista de usuarios obtenida correctamente.", users });
  } catch (error) {
    res
      .status(500)
      .json({ msg: "❌ Error al obtener los usuarios.", error: error });
  }
};

//GET /api/users/:id
export const getUserById = async (req: Request, res: Response) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ msg: "Usuario no encontrado." });
    }
    res.status(200).json({ msg: "Usuario encontrado.", user });
  } catch (error) {
    res.status(500).json({ msg: "❌ Error al obtener el usuario.", error });
  }
};

//POST /api/users
export const createUser = async (req: Request, res: Response) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.status(201).json({ msg: "Usuario creado correctamente.", user });
  } catch (error) {
    res.status(400).json({ msg: "❌ Error al crear el usuario.", error });
  }
};

//PUT /api/users/:id
export const updateUser = async (req: Request, res: Response) => {
  try {
    const user = await User.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
    });
    if (!user) {
      return res.status(404).json({ msg: "Usuario no encontrado." });
    }
    res.status(200).json({ msg: "Usuario actualizado correctamente.", user });
  } catch (error) {
    res.status(400).json({ msg: "❌ Error al actualizar el usuario.", error });
  }
};

//DELETE /api/users/:id
export const deleteUser = async (req: Request, res: Response) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);
    if (!user) {
      return res.status(404).json({ msg: "Usuario no encontrado." });
    }
    res.status(200).json({ msg: "Usuario eliminado correctamente." });
  } catch (error) {
    res.status(400).json({ msg: "❌ Error al eliminar el usuario.", error });
  }
};
