import { Schema, model, Types } from "mongoose";

const restaurantSchema = new Schema({
  name: { type: String, required: true },
  address: { type: String, required: true },
  location: {
    type: { type: String, enum: ["Point"], required: true, default: "Point" },
    coordinates: { type: [Number], required: true },
  },
  schedule: {
    open: { type: String, required: true },
    close: { type: String, required: true },
  },
  description: String,
  image_id: { type: Types.ObjectId, ref: "fs.files" },
});

restaurantSchema.index({ name: "text" });
restaurantSchema.index({ location: "2dsphere" });

export default model("Restaurant", restaurantSchema);
