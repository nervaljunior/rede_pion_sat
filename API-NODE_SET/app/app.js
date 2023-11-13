const express = require("express");
let connectionRequest = require('./connectionRequest')


const app = express();
const port = process.env.PORT || 3033;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});

app.get("/", (req, res, next) => {

  const M = {
    status: "success",
    data: {
      id: 1,
      name: "Exemplo API",
      version: "1.0.0",
      description: "API DE REGISTRO DE DADOS"
    }
  }

  res.json(M);
});

