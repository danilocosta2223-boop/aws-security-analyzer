const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        evaluatedRules: 45,
        compliantRules: 42,
        nonCompliantRules: 3,
        evaluations: [
            { rule: "s3-bucket-public-read-prohibited", status: "COMPLIANT" },
            { rule: "root-account-mfa-enabled", status: "COMPLIANT" },
            { rule: "iam-password-policy", status: "NON_COMPLIANT" }
        ]
    });
});

module.exports = router;