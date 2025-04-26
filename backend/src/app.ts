import express, { Request, Response } from "express";
import cors from "cors";
import dotenv from "dotenv";
import { connectDB } from "@config/db.ts";
import userRoutes from "@routes/userRoutes.ts";
import restaurantRoutes from "@routes/restaurantRoutes.ts";
import menuItemsRoutes from "@routes/menuItemsRoutes.ts";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

connectDB();

app.get("/", (_: Request, res: Response) => {
  res.status(200).send("API funcionando 🚀");
});

app.use("/api/users", userRoutes);
app.use("/api/restaurants", restaurantRoutes); 
app.use("/api/menu-items", menuItemsRoutes);

app.listen(PORT, () => console.log(`Servidor en http://localhost:${PORT}`));
