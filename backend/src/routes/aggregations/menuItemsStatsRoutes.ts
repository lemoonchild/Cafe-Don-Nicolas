import {
  countAvailableMenuItems,
  averagePriceMenuItems,
  countMenuItemsByCategory,
  averagePriceByCategory,
  topIngredients,
  priceRangeMenuItems,
  menuItemsByRestaurant,
} from "@controllers/aggregations/menuItemsStatsController";
import { Router } from "express";
import { asyncHandler } from "@middlewares/asyncHandler";

const router = Router();

// Agregaciones
router.get("/count-available", asyncHandler(countAvailableMenuItems));
router.get("/avg-price", asyncHandler(averagePriceMenuItems));
router.get("/count-by-category", asyncHandler(countMenuItemsByCategory));
router.get("/avg-price-by-category", asyncHandler(averagePriceByCategory));
router.get("/top-ingredients", asyncHandler(topIngredients));
router.get("/price-range", asyncHandler(priceRangeMenuItems));
router.get("/by-restaurant", asyncHandler(menuItemsByRestaurant));

export default router;
