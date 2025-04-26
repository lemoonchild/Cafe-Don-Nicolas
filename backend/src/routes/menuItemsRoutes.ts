import express from "express";
import {
    getMenuItems,
    getMenuItemById,
    createMenuItem,
    updateMenuItem,
    deleteMenuItem,
} from "@controllers/menuItemsController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getMenuItems));
router.get("/:id", validateObjectId(), asyncHandler(getMenuItemById));
router.post("/", asyncHandler(createMenuItem));
router.put("/:id", validateObjectId(), asyncHandler(updateMenuItem));
router.delete("/:id", validateObjectId(), asyncHandler(deleteMenuItem));

export default router;
