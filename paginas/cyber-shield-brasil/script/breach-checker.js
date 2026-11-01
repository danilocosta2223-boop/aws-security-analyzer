const checkBtn = document.getElementById('checkBtn');
const emailInput = document.getElementById('emailInput');

const resultContainer =
    document.getElementById('resultContainer');

const statusBox =
    document.getElementById('statusBox');

const statusIcon =
    document.getElementById('statusIcon');

const statusText =
    document.getElementById('statusText');

const riskScore =
    document.getElementById('riskScore');

const analysisDate =
    document.getElementById('analysisDate');

checkBtn.addEventListener('click', async () => {

    const email = emailInput.value.trim();

    if (!email || !email.includes('@')) {

        alert(
            'Por favor, insira um endereço de e-mail válido.'
        );

        return;
    }

    checkBtn.disabled = true;
    checkBtn.textContent = 'Consultando API...';

    try {

        const response = await fetch(
            'http://127.0.0.1:5000/api/breach/check',
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({
                    email: email
                })
            }
        );

        const data = await response.json();

        resultContainer.style.display = 'block';

        analysisDate.textContent =
            new Date().toLocaleString('pt-BR');

        if (data.exposed) {

            statusBox.className =
                'status-box status-warning';

            statusIcon.textContent =
                '⚠️';

            statusText.textContent =
                'Possível exposição encontrada';

            riskScore.textContent =
                data.risk + '%';

            riskScore.style.color =
                '#f1c40f';

        } else {

            statusBox.className =
                'status-box status-safe';

            statusIcon.textContent =
                '✅';

            statusText.textContent =
                'Nenhum vazamento encontrado';

            riskScore.textContent =
                '0%';

            riskScore.style.color =
                '#22c55e';
        }

    } catch (error) {

        console.error(error);

        alert(
            'Erro ao conectar com a API Flask.'
        );

    } finally {

        checkBtn.disabled = false;

        checkBtn.textContent =
            'Verificar Vazamentos';
    }

});