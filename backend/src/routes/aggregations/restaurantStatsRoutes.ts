import { Router } from "express";
import {
  countRestaurants,
  countRestaurantsWithImage,
  countRestaurantsOpenNow,
  groupRestaurantsByOpenHour,
} from "@controllers/aggregations/restaurantStatsController";

const router = Router();

router.get("/count", countRestaurants);
router.get("/count-with-image", countRestaurantsWithImage);
router.get("/count-open-now", countRestaurantsOpenNow);
router.get("/group-by-hour", groupRestaurantsByOpenHour);

export default router;
