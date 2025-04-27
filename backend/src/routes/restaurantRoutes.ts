import express from "express";
import {
  getRestaurants,
  getRestaurantById,
  createRestaurant,
  updateRestaurant,
  deleteRestaurant,
  updateManyRestaurants,
  updateManyRestaurantsByIds,
  deleteManyRestaurants,
  deleteManyRestaurantsByIds,
  createManyRestaurants,
} from "@controllers/restaurantController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getRestaurants));
router.get("/:id", validateObjectId(), asyncHandler(getRestaurantById));
router.post("/", asyncHandler(createRestaurant));
router.put("/:id", validateObjectId(), asyncHandler(updateRestaurant));
router.delete("/:id", validateObjectId(), asyncHandler(deleteRestaurant));

router.post("/update-many", asyncHandler(updateManyRestaurants));
router.post("/update-many-by-ids", asyncHandler(updateManyRestaurantsByIds));
router.post("/delete-many", asyncHandler(deleteManyRestaurants));
router.post("/delete-many-by-ids", asyncHandler(deleteManyRestaurantsByIds));
router.post("/create-many", asyncHandler(createManyRestaurants));

export default router;
