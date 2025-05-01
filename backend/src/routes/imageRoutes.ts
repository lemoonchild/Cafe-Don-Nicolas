import express from "express";
import { upload } from "../config/upload";
import { getGFS } from "../config/db";
import { Readable } from "stream";
import mongoose from "mongoose";

import { asyncHandler } from "@middlewares/asyncHandler";

const router = express.Router();

// Subir imagen genéricamente
router.post("/upload", upload.single("file"), asyncHandler(async (req, res) => {
  if (!req.file) return res.status(400).json({ message: "No se subió archivo." });

  const gfs = getGFS();
  const stream = Readable.from(req.file.buffer);

  const uploadStream = gfs.openUploadStream(req.file.originalname, {
    contentType: req.file.mimetype,
  });

  stream.pipe(uploadStream);

  uploadStream.on("finish", () => {
    res.status(201).json({ fileId: uploadStream.id });
  });

  uploadStream.on("error", () => {
    res.status(500).json({ message: "Error al subir archivo." });
  });
})
);

// Obtener imagen por ID
router.get(
    
    "/:id",
    asyncHandler(async (req, res) => {
      const gfs = getGFS();
      const fileId = new mongoose.Types.ObjectId(req.params.id);
  
      const cursor = gfs.find({ _id: fileId });
      const file = await cursor.next();
  
      if (!file) return res.status(404).json({ message: "Imagen no encontrada" });
  
      res.set("Content-Type", file.contentType || "application/octet-stream");
      gfs.openDownloadStream(fileId).pipe(res);
    })
);

export default router;
