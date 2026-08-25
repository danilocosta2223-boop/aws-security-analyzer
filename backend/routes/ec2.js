const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        totalInstances: 25,
        openSecurityGroups: 2,
        unpatchedVulnerabilities: 4,
        instances: [
            { id: "i-0123456789abcdef0", name: "prod-web-01", securityGroup: "sg-public-ssh", risk: "High" },
            { id: "i-0abcdef123456789a", name: "db-internal", securityGroup: "sg-internal-db", risk: "Low" }
        ]
    });
});

module.exports = router;