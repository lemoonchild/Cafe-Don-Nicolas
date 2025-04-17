import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

mongoose.connect(process.env.MONGO_URI || '')
  .then(() => console.log('MongoDB conectado'))
  .catch(err => console.error(err));

//app.get('/', (_, res) => res.send('API funcionando 🚀'));

app.listen(PORT, () => console.log(`Servidor en http://localhost:${PORT}`));
