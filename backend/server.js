const express = require("express");
const securityScoreRoute = require("./routes/securityScore");

const app = express();
const PORT = 3000;

app.get("/", (req, res) => {
  res.send("AWS Security Analyzer API Online");
});

// Registra a rota modularizada
app.use("/api/security-score", securityScoreRoute);

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});