async function testConnection() {
    const resultDiv = document.getElementById('resultado');
    resultDiv.innerHTML = "Testando conexão com o AWS STS...";

    try {
        const response = await fetch('/api/test-connection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                access_key: document.getElementById('access-key').value.trim(),
                secret_key: document.getElementById('secret-key').value.trim(),
                region: document.getElementById('region').value.trim()
            })
        });

        const data = await response.json();
        resultDiv.innerHTML = JSON.stringify(data, null, 2);
    } catch (error) {
        resultDiv.innerHTML = "Erro de conexão: " + error.message;
    }
}

async function runAudit() {
    const resultDiv = document.getElementById('resultado');
    resultDiv.innerHTML = "Executando varredura real na AWS (isso pode levar alguns segundos)...";

    try {
        const response = await fetch('/api/real-scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                access_key: document.getElementById('access-key').value.trim(),
                secret_key: document.getElementById('secret-key').value.trim(),
                region: document.getElementById('region').value.trim()
            })
        });

        const data = await response.json();
        resultDiv.innerHTML = JSON.stringify(data, null, 2);
    } catch (error) {
        resultDiv.innerHTML = "Erro na auditoria: " + error.message;
    }
}