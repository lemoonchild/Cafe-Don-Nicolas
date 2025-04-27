import { Request, Response } from "express";
import Review from "@models/Review";
import mongoose from "mongoose";

export const getReviews = async (req: Request, res: Response) => {
  const {
    restaurant_id,
    user_id,
    order_id,
    rating,
    ratingMin,
    ratingMax,
    search,
    sort,
    order,
    limit,
    skip,
    fields,
  } = req.query;

  let query: any = {};

  if (
    restaurant_id &&
    mongoose.Types.ObjectId.isValid(restaurant_id.toString())
  ) {
    query.restaurant_id = restaurant_id;
  }

  if (user_id && mongoose.Types.ObjectId.isValid(user_id.toString())) {
    query.user_id = user_id;
  }

  if (order_id && mongoose.Types.ObjectId.isValid(order_id.toString())) {
    query.order_id = order_id;
  }

  if (rating) {
    query.rating = parseInt(rating.toString());
  } else if (ratingMin || ratingMax) {
    query.rating = {};
    if (ratingMin) query.rating.$gte = parseInt(ratingMin.toString());
    if (ratingMax) query.rating.$lte = parseInt(ratingMax.toString());
  }

  if (search) {
    query.$text = { $search: search.toString() };
  }

  let cursor = Review.find(query);

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

  const reviews = await cursor.exec();
  res.json(reviews);
};

export const getReviewById = async (req: Request, res: Response) => {
  const review = await Review.findById(req.params.id);
  if (!review) return res.status(404).json({ message: "Reseña no encontrada" });
  res.json(review);
};

export const createReview = async (req: Request, res: Response) => {
  const review = new Review(req.body);
  await review.save();
  res.status(201).json(review);
};

export const updateReview = async (req: Request, res: Response) => {
  const review = await Review.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
  });
  if (!review) return res.status(404).json({ message: "Reseña no encontrada" });
  res.json(review);
};

export const deleteReview = async (req: Request, res: Response) => {
  const review = await Review.findByIdAndDelete(req.params.id);
  if (!review) return res.status(404).json({ message: "Reseña no encontrada" });
  res.json({ message: "Reseña eliminada correctamente" });
};

export const updateManyReviews = async (req: Request, res: Response) => {
  const { filter, update } = req.body;

  if (!filter || !update) {
    return res.status(400).json({ message: "Debes enviar 'filter' y 'update'." });
  }

  const result = await Review.updateMany(filter, update);
  res.json({ message: `Se actualizaron ${result.modifiedCount} reseñas.`, result });
};

export const updateManyReviewsByIds = async (req: Request, res: Response) => {
  const { ids, update } = req.body;

  if (!ids || !Array.isArray(ids) || !update) {
    return res.status(400).json({ message: "Debes enviar 'ids' (array) y 'update'." });
  }

  const result = await Review.updateMany(
    { _id: { $in: ids } },
    update
  );
  res.json({ message: `Se actualizaron ${result.modifiedCount} reseñas.`, result });
};

export const deleteManyReviews = async (req: Request, res: Response) => {
  const { filter } = req.body;

  if (!filter) {
    return res.status(400).json({ message: "Debes enviar 'filter'." });
  }

  const result = await Review.deleteMany(filter);
  res.json({ message: `Se eliminaron ${result.deletedCount} reseñas.`, result });
};

export const deleteManyReviewsByIds = async (req: Request, res: Response) => {
  const { ids } = req.body;

  if (!ids || !Array.isArray(ids)) {
    return res.status(400).json({ message: "Debes enviar 'ids' (array)." });
  }

  const result = await Review.deleteMany(
    { _id: { $in: ids } }
  );
  res.json({ message: `Se eliminaron ${result.deletedCount} reseñas.`, result });
};
