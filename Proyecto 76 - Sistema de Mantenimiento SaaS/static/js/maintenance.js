document.addEventListener('DOMContentLoaded', () => {
    // Work Order Creation Form
    const mForm = document.getElementById('create-maintenance-form');
    if (mForm) {
        mForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                equipment_id: document.getElementById('m-equipment-id').value,
                technician_id: document.getElementById('m-technician-id').value,
                type: document.getElementById('m-type').value,
                priority: document.getElementById('m-priority').value,
                scheduled_date: document.getElementById('m-scheduled-date').value,
                estimated_hours: document.getElementById('m-estimated-hours').value,
                labor_cost: document.getElementById('m-labor-cost').value,
                parts_cost: document.getElementById('m-parts-cost').value,
                description: document.getElementById('m-description').value
            };

            fetch('/api/maintenance/create', {
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
            .catch(err => alert('❌ Erro ao agendar manutenção.'));
        });
    }

    // Incident Creation Form
    const incForm = document.getElementById('create-incident-form');
    if (incForm) {
        incForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                equipment_id: document.getElementById('inc-equipment-id').value,
                reported_by: document.getElementById('inc-reported-by').value,
                severity: document.getElementById('inc-severity').value,
                description: document.getElementById('inc-description').value
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
            .catch(err => alert('❌ Erro ao reportar anomalia.'));
        });
    }

    // Equipment Creation Form
    const eqpForm = document.getElementById('create-equipment-form');
    if (eqpForm) {
        eqpForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                name: document.getElementById('eqp-name').value,
                category: document.getElementById('eqp-category').value,
                serial_number: document.getElementById('eqp-serial').value,
                location: document.getElementById('eqp-location').value
            };

            fetch('/api/equipment/create', {
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
            .catch(err => alert('❌ Erro ao cadastrar equipamento.'));
        });
    }

    // Technician Creation Form
    const techForm = document.getElementById('create-technician-form');
    if (techForm) {
        techForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                name: document.getElementById('tech-name').value,
                specialty: document.getElementById('tech-specialty').value,
                email: document.getElementById('tech-email').value,
                phone: document.getElementById('tech-phone').value
            };

            fetch('/api/technician/create', {
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
            .catch(err => alert('❌ Erro ao cadastrar técnico.'));
        });
    }
});

// Update Maintenance Work Order Status
function updateMaintenanceStatus(orderId, newStatus) {
    const technician = prompt(`Alterar estado da Ordem de Trabalho para "${newStatus}".\nIntroduza o nome do técnico responsável:`, 'Eng. Enmanuel Jimenez');
    if (!technician) return;

    const partsUsed = prompt('Registar peças de reposição e consumíveis utilizados:', 'Peças padrão de reposição OEM');
    const notes = prompt('Notas técnicas de execução:', `Intervenção concluída sob estado ${newStatus}`);

    fetch(`/api/maintenance/status/${orderId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus, technician: technician, parts_used: partsUsed || '', notes: notes || '' })
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
    .catch(err => alert('❌ Erro ao atualizar estado da ordem de trabalho.'));
}

// Update Incident Status
function updateIncidentStatus(incidentId, newStatus) {
    const technician = prompt(`Alterar estado da incidência para "${newStatus}".\nTécnico responsável:`, 'Eng. Enmanuel Jimenez');
    if (!technician) return;

    const notes = prompt('Notas técnicas de resolução:', `Incidência tratada e sanada`);

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
