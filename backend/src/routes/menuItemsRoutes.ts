import express from "express";
import {
  getMenuItems,
  getMenuItemById,
  createMenuItem,
  updateMenuItem,
  deleteMenuItem,
  createManyMenuItems,
  updateManyMenuItems,
  updateManyMenuItemsByIds,
  deleteManyMenuItems,
  deleteManyMenuItemsByIds,
  addIngredient,
  removeIngredient,
  addIngredientUnique,
} from "@controllers/menuItemsController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getMenuItems));
router.get("/:id", validateObjectId(), asyncHandler(getMenuItemById));
router.post("/", asyncHandler(createMenuItem));
router.put("/:id", validateObjectId(), asyncHandler(updateMenuItem));
router.delete("/:id", validateObjectId(), asyncHandler(deleteMenuItem));
router.patch("/add-ingredient/:id", asyncHandler(addIngredient));
router.patch("/remove-ingredient/:id", asyncHandler(removeIngredient));
router.patch("/add-ingredient-unique/:id", asyncHandler(addIngredientUnique));

router.post("/update-many", asyncHandler(updateManyMenuItems));
router.post("/update-many-by-ids", asyncHandler(updateManyMenuItemsByIds));
router.post("/delete-many", asyncHandler(deleteManyMenuItems));
router.post("/delete-many-by-ids", asyncHandler(deleteManyMenuItemsByIds));
router.post("/create-many", asyncHandler(createManyMenuItems));

export default router;
