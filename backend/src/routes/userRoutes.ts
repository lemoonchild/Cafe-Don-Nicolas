import { Router } from "express";
import {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
} from "@controllers/userController.ts";
import { asyncHandler } from "@middlewares/asyncHandler.ts";
import { validateObjectId } from "@middlewares/validateObjectId.ts";

const router = Router();

router.get("/", asyncHandler(getUsers));
router.get("/:id", validateObjectId(), asyncHandler(getUserById));
router.post("/", asyncHandler(createUser));
router.put("/:id", validateObjectId(), asyncHandler(updateUser));
router.delete("/:id", validateObjectId(), asyncHandler(deleteUser));

export default router;
