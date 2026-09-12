document.addEventListener('DOMContentLoaded', () => {
    // Warranty Registration Form Submit
    const warrantyForm = document.getElementById('register-warranty-form');
    if (warrantyForm) {
        warrantyForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                client_id: document.getElementById('warranty-client-id').value,
                product_id: document.getElementById('warranty-product-id').value,
                serial_number: document.getElementById('warranty-serial').value,
                purchase_date: document.getElementById('warranty-date').value,
                warranty_months: document.getElementById('warranty-months').value,
                notes: document.getElementById('warranty-notes').value
            };

            fetch('/api/warranty/register', {
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
            .catch(err => alert('❌ Erro ao registar garantia.'));
        });
    }

    // RMA Incident Claim Form Submit
    const incidentForm = document.getElementById('create-incident-form');
    if (incidentForm) {
        incidentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                warranty_id: document.getElementById('rma-warranty-id').value,
                fault_description: document.getElementById('rma-fault-desc').value,
                severity: document.getElementById('rma-severity').value,
                assigned_technician: document.getElementById('rma-technician').value
            };

            fetch('/api/incident/create', {
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
            .catch(err => alert('❌ Erro ao abrir chamado RMA.'));
        });
    }
});

// Update RMA Incident Status
function updateIncidentStatus(incidentId, newStatus) {
    const technician = prompt(`Alterar estado da incidência para "${newStatus}".\nIntroduza o nome do técnico responsável:`, 'Enmanuel Jimenez');
    if (!technician) return;

    const notes = prompt('Adicionar notas técnicas de intervenção:', `Atualizado para ${newStatus}`);

    fetch(`/api/incident/status/${incidentId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus, technician: technician, notes: notes || '' })
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
    .catch(err => alert('❌ Erro ao atualizar incidência.'));
}
