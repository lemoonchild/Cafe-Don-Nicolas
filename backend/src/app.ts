import express, { Request, Response } from "express";
import cors from "cors";
import dotenv from "dotenv";
import { connectDB } from "@config/db.ts";
import userRoutes from "@routes/userRoutes.ts";
import restaurantRoutes from "@routes/restaurantRoutes.ts";
import menuItemsRoutes from "@routes/menuItemsRoutes.ts";
import reviewRoutes from "@routes/reviewRoutes.ts";
import orderRoutes from "@routes/orderRoutes.ts";
import userStatsRoutes from "@routes/aggregations/userStatsRoutes.ts";
import restaurantStatsRoutes from "@routes/aggregations/restaurantStatsRoutes.ts";
import menuItemsStatsRoutes from "@routes/aggregations/menuItemsStatsRoutes.ts";
import reviewStatsRoutes from "@routes/aggregations/reviewsStatsRoutes.ts";
import orderStatsRoutes from "@routes/aggregations/orderStatsRoutes.ts";
import imageRoutes from "@routes/imageRoutes.ts";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

connectDB();

app.get("/", (_: Request, res: Response) => {
  res.status(200).send("API funcionando correctamente");
});

app.use("/api/users", userRoutes);
app.use("/api/restaurants", restaurantRoutes);
app.use("/api/menu-items", menuItemsRoutes);
app.use("/api/reviews", reviewRoutes);
app.use("/api/orders", orderRoutes);

app.use("/api/users/stats", userStatsRoutes);
app.use("/api/restaurants/stats", restaurantStatsRoutes);
app.use("/api/menu-items/stats", menuItemsStatsRoutes);

app.use("/api/reviews/stats", reviewStatsRoutes);
app.use("/api/orders/stats", orderStatsRoutes);

app.use("/api/images", imageRoutes);

app.listen(PORT, () => console.log(`Servidor en http://localhost:${PORT}`));
