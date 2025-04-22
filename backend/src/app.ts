import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { connectDB } from "./config/db.ts";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

connectDB();

//app.get('/', (_, res) => res.send('API funcionando 🚀'));

app.listen(PORT, () => console.log(`Servidor en http://localhost:${PORT}`));
