import { Router } from "express";
import {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  updateManyUsers,
  updateManyUsersByIds,
  deleteManyUsers,
  deleteManyUsersByIds,
  createManyUsers,
} from "@controllers/userController.ts";
import { asyncHandler } from "@middlewares/asyncHandler.ts";
import { validateObjectId } from "@middlewares/validateObjectId.ts";

const router = Router();

router.get("/", asyncHandler(getUsers));
router.get("/:id", validateObjectId(), asyncHandler(getUserById));
router.post("/", asyncHandler(createUser));
router.put("/:id", validateObjectId(), asyncHandler(updateUser));
router.delete("/:id", validateObjectId(), asyncHandler(deleteUser));

router.post("/update-many", asyncHandler(updateManyUsers));
router.post("/update-many-by-ids", asyncHandler(updateManyUsersByIds));
router.post("/delete-many", asyncHandler(deleteManyUsers));
router.post("/delete-many-by-ids", asyncHandler(deleteManyUsersByIds));
router.post("/create-many", asyncHandler(createManyUsers));

export default router;
