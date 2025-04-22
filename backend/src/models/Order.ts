import { Schema, model, Types } from "mongoose";

const orderSchema = new Schema({
  user_id: { type: Types.ObjectId, ref: "User", required: true },
  restaurant_id: { type: Types.ObjectId, ref: "Restaurant", required: true },
  date: { type: Date, default: Date.now },
  status: {
    type: String,
    enum: ["pendiente", "preparando", "entregado", "cancelado"],
    default: "pendiente",
  },
  total: { type: Number, required: true },
  items: [
    {
      product_id: { type: Types.ObjectId, ref: "MenuItem", required: true },
      name: String,
      quantity: Number,
      unit_price: Number,
    },
  ],
});

orderSchema.index({ user_id: 1, date: -1 });
orderSchema.index({ status: "text" });

export default model("Order", orderSchema, "Orders");
