document.addEventListener('DOMContentLoaded', () => {
    // Quick Clock-In / Out Handler
    const clockInForm = document.getElementById('clock-in-form');
    if (clockInForm) {
        clockInForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const employeeId = document.getElementById('clock-employee-id').value;
            const status = document.getElementById('clock-status').value;

            fetch('/api/clock-in', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ employee_id: employeeId, status: status })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro na ligação ao servidor.'));
        });
    }

    // Save Vacation Handler
    const vacationForm = document.getElementById('vacation-form');
    if (vacationForm) {
        vacationForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                employee_id: document.getElementById('vac-employee-id').value,
                start_date: document.getElementById('vac-start-date').value,
                end_date: document.getElementById('vac-end-date').value,
                reason: document.getElementById('vac-reason').value
            };

            fetch('/api/vacation/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao guardar pedido de férias.'));
        });
    }

    // Save Document Handler
    const documentForm = document.getElementById('document-form');
    if (documentForm) {
        documentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                employee_id: document.getElementById('doc-employee-id').value,
                title: document.getElementById('doc-title').value,
                category: document.getElementById('doc-category').value,
                file_url: document.getElementById('doc-file-url').value || '/docs/exemplo.pdf'
            };

            fetch('/api/document/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao guardar documento.'));
        });
    }
});

// Update Vacation Status (Aprovado / Rejeitado)
function updateVacationStatus(vacationId, newStatus) {
    if (!confirm(`Deseja alterar o pedido de férias #${vacationId} para "${newStatus}"?`)) return;

    fetch(`/api/vacation/status/${vacationId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('⚠️ ' + data.message);
        }
    })
    .catch(err => alert('❌ Erro ao atualizar férias.'));
}

// Delete Employee
function deleteEmployee(id, name) {
    if (!confirm(`Tem a certeza que deseja eliminar o colaborador "${name}"? Esta ação removerá também o seu histórico.`)) return;

    fetch(`/api/employee/delete/${id}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('⚠️ ' + data.message);
        }
    })
    .catch(err => alert('❌ Erro ao eliminar colaborador.'));
}
