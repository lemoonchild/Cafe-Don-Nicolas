import express from "express";
import {
    getReviews,
    getReviewById,
    createReview,
    updateReview,
    deleteReview,
} from "@controllers/reviewsItemsController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getReviews));
router.get("/:id", validateObjectId(), asyncHandler(getReviewById));
router.post("/", asyncHandler(createReview));
router.put("/:id", validateObjectId(), asyncHandler(updateReview));
router.delete("/:id", validateObjectId(), asyncHandler(deleteReview));

export default router;
