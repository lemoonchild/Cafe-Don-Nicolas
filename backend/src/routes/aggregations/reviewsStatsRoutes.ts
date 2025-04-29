import {
  averageRatingByRestaurant,
  countReviewsByRestaurant,
  reviewsWithUserInfo,
} from "@controllers/aggregations/reviewsStatsController";

import { Router } from "express";
import { asyncHandler } from "@middlewares/asyncHandler";

const router = Router();

router.get(
  "/average-rating/:restaurantId",
  asyncHandler(averageRatingByRestaurant)
);
router.get("/count-by-restaurant", asyncHandler(countReviewsByRestaurant));
router.get("/with-user", asyncHandler(reviewsWithUserInfo));

export default router;
