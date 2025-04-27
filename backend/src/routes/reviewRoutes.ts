import express from "express";
import {
    getReviews,
    getReviewById,
    createReview,
    updateReview,
    deleteReview,
    updateManyReviews,
    updateManyReviewsByIds,
    deleteManyReviews,
    deleteManyReviewsByIds,
    createManyReviews,
} from "@controllers/reviewsItemsController";
import { asyncHandler } from "@middlewares/asyncHandler";
import { validateObjectId } from "@middlewares/validateObjectId";

const router = express.Router();

router.get("/", asyncHandler(getReviews));
router.get("/:id", validateObjectId(), asyncHandler(getReviewById));
router.post("/", asyncHandler(createReview));
router.put("/:id", validateObjectId(), asyncHandler(updateReview));
router.delete("/:id", validateObjectId(), asyncHandler(deleteReview));

router.post("/update-many", asyncHandler(updateManyReviews));
router.post("/update-many-by-ids", asyncHandler(updateManyReviewsByIds));
router.post("/delete-many", asyncHandler(deleteManyReviews));
router.post("/delete-many-by-ids", asyncHandler(deleteManyReviewsByIds));
router.post("/create-many", asyncHandler(createManyReviews));

export default router;
