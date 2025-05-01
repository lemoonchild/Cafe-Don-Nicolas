import mongoose from "mongoose";
import { GridFSBucket } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

let gfs: GridFSBucket;

export const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI || "");
    console.log("✅ MongoDB conectado");

    const db = conn.connection.db!;
    gfs = new mongoose.mongo.GridFSBucket(db, { bucketName: "fs" });
    console.log("📦 GridFS inicializado");

  } catch (err) {
    console.error("❌ Error al conectar a MongoDB", err);
    process.exit(1);
  }
};

export const getGFS = () => {
  if (!gfs) throw new Error("GridFS no ha sido inicializado aún.");
  return gfs;
};
