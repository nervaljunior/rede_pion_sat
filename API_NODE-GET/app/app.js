const express = require("express");
let connectionRequest = require('./connectionRequest')


const app = express();
const port = process.env.PORT || 3034;

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
      description: "API DE CONSULTA DE DADOS"
    }
  }

  res.json(M);
});



// Rota para obter a lista de produtos
app.get('/logs', (req, res) => {

  const dataParametro = req.query.data;

  connection = connectionRequest();

  let  query = 'SELECT * FROM logs where 1';

    // Adicionar condição baseada no parâmetro, se estiver presente
    if (dataParametro) {
      // Adicionar condição para a coluna de data
      query += ' AND data_c >= ?';
    }
  

  connection.query(query,[dataParametro], (err, results) => {
    if (err) {
      connection.destroy();
      res.status(500).send('Erro: ' + err);
    } else {
      connection.destroy();
      res.status(200).json(results);
    }
  });

});

