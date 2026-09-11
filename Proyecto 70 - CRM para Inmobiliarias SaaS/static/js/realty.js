document.addEventListener('DOMContentLoaded', () => {
    // Property Form Submit
    const propForm = document.getElementById('property-form');
    if (propForm) {
        propForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                id: document.getElementById('prop-id').value || null,
                title: document.getElementById('prop-title').value,
                property_type: document.getElementById('prop-type').value,
                address: document.getElementById('prop-address').value,
                city: document.getElementById('prop-city').value,
                price: parseFloat(document.getElementById('prop-price').value || 0),
                bedrooms: parseInt(document.getElementById('prop-bedrooms').value || 0),
                bathrooms: parseInt(document.getElementById('prop-bathrooms').value || 0),
                area_sqm: parseFloat(document.getElementById('prop-area').value || 0),
                status: document.getElementById('prop-status').value,
                agent_name: document.getElementById('prop-agent').value
            };

            fetch('/api/property/save', {
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
            .catch(err => alert('❌ Erro de comunicação com o servidor.'));
        });
    }

    // Client Form Submit
    const clientForm = document.getElementById('client-form');
    if (clientForm) {
        clientForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                full_name: document.getElementById('client-name').value,
                email: document.getElementById('client-email').value,
                phone: document.getElementById('client-phone').value,
                client_type: document.getElementById('client-type').value,
                budget_max: parseFloat(document.getElementById('client-budget').value || 0),
                preferred_type: document.getElementById('client-pref-type').value
            };

            fetch('/api/client/save', {
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
            .catch(err => alert('❌ Erro ao guardar cliente.'));
        });
    }

    // Visit Form Submit
    const visitForm = document.getElementById('visit-form');
    if (visitForm) {
        visitForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                property_id: document.getElementById('visit-property-id').value,
                client_id: document.getElementById('visit-client-id').value,
                visit_date: document.getElementById('visit-date').value,
                visit_time: document.getElementById('visit-time').value,
                notes: document.getElementById('visit-notes').value
            };

            fetch('/api/visit/save', {
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
            .catch(err => alert('❌ Erro ao agendar visita.'));
        });
    }

    // Offer Form Submit
    const offerForm = document.getElementById('offer-form');
    if (offerForm) {
        offerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                property_id: document.getElementById('offer-property-id').value,
                client_id: document.getElementById('offer-client-id').value,
                offer_amount: parseFloat(document.getElementById('offer-amount').value || 0),
                notes: document.getElementById('offer-notes').value
            };

            fetch('/api/offer/save', {
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
            .catch(err => alert('❌ Erro ao registar proposta.'));
        });
    }
});

// Update Lead Status Stage
function updateLeadStatus(leadId, newStatus) {
    fetch(`/api/lead/status/${leadId}`, {
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
    .catch(err => alert('❌ Erro ao atualizar etapa do lead.'));
}

// Update Offer Status (Aceita / Rejeitada)
function updateOfferStatus(offerId, newStatus) {
    if (!confirm(`Deseja alterar a proposta #${offerId} para "${newStatus}"?`)) return;

    fetch(`/api/offer/status/${offerId}`, {
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
    .catch(err => alert('❌ Erro ao atualizar proposta.'));
}
