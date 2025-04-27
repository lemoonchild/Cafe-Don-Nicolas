import express from "express";
import {
    getMenuItems,
    getMenuItemById,
    createMenuItem,
    updateMenuItem,
    deleteMenuItem,
    updateManyMenuItems,
    updateManyMenuItemsByIds,   
    deleteManyMenuItems,
    deleteManyMenuItemsByIds,
} from "@controllers/menuItemsController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getMenuItems));
router.get("/:id", validateObjectId(), asyncHandler(getMenuItemById));
router.post("/", asyncHandler(createMenuItem));
router.put("/:id", validateObjectId(), asyncHandler(updateMenuItem));
router.delete("/:id", validateObjectId(), asyncHandler(deleteMenuItem));

router.post("/update-many", asyncHandler(updateManyMenuItems));
router.post("/update-many-by-ids", asyncHandler(updateManyMenuItemsByIds));
router.post("/delete-many", asyncHandler(deleteManyMenuItems));
router.post("/delete-many-by-ids", asyncHandler(deleteManyMenuItemsByIds));

export default router;
