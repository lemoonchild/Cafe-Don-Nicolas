import { Schema, model, Types } from "mongoose";

const menuItemSchema = new Schema({
  name: { type: String, required: true },
  description: String,
  price: { type: Number, required: true },
  ingredients: [{ type: String }],
  category: { type: String, required: true },
  available: { type: Boolean, default: true },
  restaurant_id: { type: Types.ObjectId, ref: "Restaurant", required: true },
  image_id: { type: Types.ObjectId, ref: "fs.files" },
});

menuItemSchema.index({ name: 1, restaurant_id: 1 });
menuItemSchema.index({ ingredients: 1 });

export default model("MenuItem", menuItemSchema);
