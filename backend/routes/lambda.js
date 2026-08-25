const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        totalFunctions: 34,
        outdatedRuntimes: 3,
        excessivePermissions: 2,
        functions: [
            { functionName: "auth-processor", runtime: "nodejs18.x", status: "Compliant" },
            { functionName: "legacy-report-generator", runtime: "nodejs12.x", status: "Outdated" }
        ]
    });
});

module.exports = router;