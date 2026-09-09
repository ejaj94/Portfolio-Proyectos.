document.addEventListener('DOMContentLoaded', () => {
    // Live Clock Update
    const clockDisplay = document.getElementById('live-clock');
    if (clockDisplay) {
        setInterval(() => {
            const now = new Date();
            clockDisplay.innerText = now.toLocaleTimeString('pt-PT', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }, 1000);
    }

    // Quick Punch Handler Form
    const punchForm = document.getElementById('quick-punch-form');
    if (punchForm) {
        punchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const employeeId = document.getElementById('punch-employee-id').value;

            if (!employeeId) {
                alert('⚠️ Selecione ou introduza um código de colaborador.');
                return;
            }

            fetch('/api/punch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ employee_id: employeeId })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const resultContainer = document.getElementById('punch-result');
                    if (resultContainer) {
                        resultContainer.style.display = 'block';
                        resultContainer.innerHTML = `
                            <div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid var(--emerald-green); border-radius: 16px; padding: 1.25rem; color: white; text-align: center;">
                                <div style="font-size: 1.2rem; font-weight: 800; color: var(--emerald-green);">${data.message}</div>
                                <div style="font-size: 0.9rem; color: var(--text-muted); margin-top: 0.3rem;">Operação efetuada às <strong>${data.time}</strong></div>
                            </div>
                        `;
                    }
                    setTimeout(() => window.location.reload(), 1800);
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro de ligação ao terminal.'));
        });
    }
});

// Employee Punch via Kiosk Cards
function punchByEmployeeId(empId, empName) {
    if (!confirm(`Confirmar registo de ponto (Entrada/Saída) para "${empName}"?`)) return;

    fetch('/api/punch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employee_id: empId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            window.location.reload();
        } else {
            alert('⚠️ ' + data.message);
        }
    })
    .catch(err => alert('❌ Erro no terminal de ponto.'));
}
