import express from "express";
import {
  getOrders,
  getOrderById,
  createOrder,
  updateOrder,
  deleteOrder,
  updateManyOrders,
  updateManyOrdersByIds,
  deleteManyOrders,
  deleteManyOrdersByIds,
  createManyOrders,

} from "@controllers/orderController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getOrders));
router.get("/:id", validateObjectId(), asyncHandler(getOrderById));
router.post("/", asyncHandler(createOrder));
router.put("/:id", validateObjectId(), asyncHandler(updateOrder));
router.delete("/:id", validateObjectId(), asyncHandler(deleteOrder));

router.post("/update-many", asyncHandler(updateManyOrders));
router.post("/update-many-by-ids", asyncHandler(updateManyOrdersByIds));
router.post("/delete-many", asyncHandler(deleteManyOrders));
router.post("/delete-many-by-ids", asyncHandler(deleteManyOrdersByIds));
router.post("/create-many", asyncHandler(createManyOrders));

export default router;
