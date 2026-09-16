function runAwsAudit() {

    const resultContainer =
        document.getElementById(
            "aws-result"
        );

    resultContainer.innerHTML =
        "🔄 Executando auditoria AWS...";

    fetch("/api/dashboard")

        .then(response => response.json())

        .then(data => {

            resultContainer.innerHTML = `

                <div class="dashboard-grid">

                    <div class="card">
                        <h3>🏢 Account ID</h3>
                        <p>${data.account_id}</p>
                    </div>

                    <div class="card">
                        <h3>🌎 Região</h3>
                        <p>${data.region}</p>
                    </div>

                    <div class="card">
                        <h3>👤 IAM User</h3>
                        <p>${data.iam_user}</p>
                    </div>

                    <div class="card">
                        <h3>🛡️ Security Score</h3>
                        <p>${data.security_score}%</p>
                    </div>

                </div>

            `;

        })

        .catch(error => {

            resultContainer.innerHTML = `

                <div class="card">

                    <h3>❌ Erro</h3>

                    <p>${error.message}</p>

                </div>

            `;

        });

}