// src/middlewares/validateObjectId.ts
import { Request, Response, NextFunction } from "express";
import mongoose from "mongoose";

export const validateObjectId = (param: string = "id") => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const value = req.params[param];
    if (!mongoose.Types.ObjectId.isValid(value)) {
      res.status(400).json({
        message: `El valor de '${param}' no es un ObjectId válido.`,
      });
      return; // <- importante para evitar ejecutar `next()` luego del res
    }
    next();
  };
};
