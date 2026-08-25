const express = require("express");

const app = express();

const PORT = 3000;

app.get("/api/security-score", (req, res) => {

    res.json({
        score: 92,
        compliance: 95,
        findings: 8
    });

});

app.listen(PORT, () => {

    console.log(
        "Servidor rodando na porta 3000"
    );

});