const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        totalDatabases: 5,
        publiclyAccessible: 0,
        unencryptedDatabases: 1,
        databases: [
            { dbInstance: "prod-mysql-db", engine: "MySQL 8.0", encryption: true, publicAccess: false },
            { dbInstance: "analytics-pg", engine: "PostgreSQL 14", encryption: false, publicAccess: false }
        ]
    });
});

module.exports = router;