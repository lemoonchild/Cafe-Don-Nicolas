import { Request, Response } from "express";
import { Readable } from "stream";
import { getGFS } from "@config/db";
import MenuItem from "@models/MenuItem";

export const uploadMenuItemImage = async (req: Request, res: Response) => {
  const { id } = req.params;

  if (!req.file) {
    return res.status(400).json({ message: "No se subió ningún archivo." });
  }

  const gfs = getGFS();
  const stream = Readable.from(req.file.buffer);

  const uploadStream = gfs.openUploadStream(req.file.originalname, {
    contentType: req.file.mimetype,
  });

  stream.pipe(uploadStream);

  uploadStream.on("finish", async () => {
    const updated = await MenuItem.findByIdAndUpdate(
      id,
      { image_id: uploadStream.id },
      { new: true }
    );

    if (!updated) {
      return res.status(404).json({ message: "MenuItem no encontrado." });
    }

    res.status(200).json({ message: "Imagen subida y asociada", item: updated });
  });

  uploadStream.on("error", () => {
    res.status(500).json({ message: "Error al subir la imagen." });
  });
};
