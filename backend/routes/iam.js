const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
    res.json({
        totalUsers: 14,
        mfaDisabled: 2,
        accessKeysOver90Days: 3,
        rootAccountMfa: true,
        findings: [
            { user: "dev-pipeline", issue: "Chave de acesso com mais de 90 dias", severity: "Medium" },
            { user: "joao.silva", issue: "MFA desativado", severity: "High" },
            { user: "temp-contractor", issue: "Políticas excessivamente permissivas (*)", severity: "Critical" },
            { user: "maria.souza", issue: "MFA desativado", severity: "High" }
        ]
    });
});

module.exports = router;