const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        totalBuckets: 12,
        publicBuckets: 1,
        unencryptedBuckets: 2,
        buckets: [
            { name: "corp-backup-vault", publicAccess: false, encryption: "AES-256", status: "Secure" },
            { name: "legacy-data-temp", publicAccess: true, encryption: "None", status: "Critical" },
            { name: "app-logs-prod", publicAccess: false, encryption: "AWS-KMS", status: "Secure" }
        ]
    });
});

module.exports = router;