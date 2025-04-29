import {
  totalSales,
  averageOrderValue,
  countOrdersByStatus,
  ordersWithRestaurant,
  unwindOrderItems,
} from "@controllers/aggregations/orderStatsController";

import { Router } from "express";
import { asyncHandler } from "@middlewares/asyncHandler";

const router = Router();

router.get("/total-sales", asyncHandler(totalSales));
router.get("/avg-order-value", asyncHandler(averageOrderValue));
router.get("/count-by-status", asyncHandler(countOrdersByStatus));
router.get("/with-restaurant", asyncHandler(ordersWithRestaurant));
router.get("/unwind-items", asyncHandler(unwindOrderItems));

export default router;
