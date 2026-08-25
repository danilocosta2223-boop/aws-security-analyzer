const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        activeFindings: 3,
        severityBreakdown: { High: 1, Medium: 2, Low: 0 },
        recentThreats: [
            { id: "g-001", type: "UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration", severity: "High", region: "us-east-1" },
            { id: "g-002", type: "Recon:EC2/PortProbeUnusualPort", severity: "Medium", region: "us-east-1" }
        ]
    });
});

module.exports = router;