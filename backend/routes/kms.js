const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        totalKeys: 18,
        scheduledForDeletion: 1,
        rotationEnabled: 15,
        keys: [
            { keyId: "arn:aws:kms:us-east-1:123:key/abc", alias: "alias/prod-secret", rotation: true },
            { keyId: "arn:aws:kms:us-east-1:123:key/def", alias: "alias/temp-key", rotation: false }
        ]
    });
});

module.exports = router;