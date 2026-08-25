const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        generatedReportsCount: 12,
        lastGenerated: "2026-06-15T10:30:00Z",
        availableFormats: ["PDF", "JSON", "CSV"],
        status: "Ready for Export"
    });
});

module.exports = router;