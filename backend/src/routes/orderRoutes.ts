import express from "express";
import {
  getOrders,
  getOrderById,
  createOrder,
  updateOrder,
  deleteOrder,
} from "@controllers/orderController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getOrders));
router.get("/:id", validateObjectId(), asyncHandler(getOrderById));
router.post("/", asyncHandler(createOrder));
router.put("/:id", validateObjectId(), asyncHandler(updateOrder));
router.delete("/:id", validateObjectId(), asyncHandler(deleteOrder));

export default router;
