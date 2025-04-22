import { Schema, model } from "mongoose";

const userSchema = new Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  role: { type: String, enum: ["cliente", "admin"], required: true },
  location: {
    type: { type: String, enum: ["Point"], required: true, default: "Point" },
    coordinates: { type: [Number], required: true }, // [longitude, latitude]
  },
});

userSchema.index({ name: "text" });
userSchema.index({ location: "2dsphere" });

export default model("User", userSchema);
