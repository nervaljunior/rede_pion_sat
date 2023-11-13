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




//curl -X POST -H "Content-Type: application/json" -d '{"id": 1, "data": "2023-10-26", "server": "meu-server", "dados": {"campo1": "valor1", "campo2": "valor2"}}' http://localhost:3000/set_log

app.post('/set_log', (req, res) => {

  const {client, dados} = req.body;
  const dataAtual = new Date();

  connection = connectionRequest();

  // SQL para inserção
  const query = 'INSERT INTO logs (data_c, server, dados) VALUES ( ?, ?, ?)';

  // Parâmetros para substituir os placeholders no SQL
  const parametros = [dataAtual, client, dados];

  connection.query(query, parametros, (err, results) => {
    if (err) {
      connection.destroy();
      res.status(500).json({ erro: err, status: 0 });
    } else {
      connection.destroy();
      res.status(200).json({ status: 1, message: "Inserido com sucesso!" });
    }
  });

});

