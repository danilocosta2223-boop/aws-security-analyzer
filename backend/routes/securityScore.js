const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        score: 92,
        compliance: 95,
        findings: 8,
        status: "Optimal"
    });
});

module.exports = router;