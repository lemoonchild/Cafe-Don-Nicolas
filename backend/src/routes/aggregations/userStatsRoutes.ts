import { Router } from "express";
import {
  countUsers,
  countUsersByRole,
} from "@controllers/aggregations/userStatsController";

const router = Router();

// Estadísticas de usuarios
router.get("/count", countUsers);
router.get("/count-by-role", countUsersByRole);

export default router;
