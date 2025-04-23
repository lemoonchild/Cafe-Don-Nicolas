import express from "express";
import {
  getRestaurants,
  getRestaurantById,
  createRestaurant,
  updateRestaurant,
  deleteRestaurant,
} from "@controllers/restaurantController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getRestaurants));
router.get("/:id", validateObjectId(), asyncHandler(getRestaurantById));
router.post("/", asyncHandler(createRestaurant));
router.put("/:id", validateObjectId(), asyncHandler(updateRestaurant));
router.delete("/:id", validateObjectId(), asyncHandler(deleteRestaurant));

export default router;
