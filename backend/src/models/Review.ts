import { Schema, model, Types } from "mongoose";

const reviewSchema = new Schema({
  user_id: { type: Types.ObjectId, ref: "User", required: true },
  restaurant_id: { type: Types.ObjectId, ref: "Restaurant", required: true },
  order_id: { type: Types.ObjectId, ref: "Order" }, // opcional
  rating: { type: Number, min: 1, max: 5, required: true },
  comment: String,
  date: { type: Date, default: Date.now },
});

reviewSchema.index({ restaurant_id: 1, rating: -1 });
reviewSchema.index({ comment: "text" });

export default model("Review", reviewSchema, "Reviews");
