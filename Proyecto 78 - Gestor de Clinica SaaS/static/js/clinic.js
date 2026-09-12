document.addEventListener('DOMContentLoaded', () => {
    // Create Appointment Form
    const apptForm = document.getElementById('create-appointment-form');
    if (apptForm) {
        apptForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                patient_id: document.getElementById('appt-patient-id').value,
                professional_id: document.getElementById('appt-professional-id').value,
                appointment_date: document.getElementById('appt-date').value,
                appointment_time: document.getElementById('appt-time').value,
                reason: document.getElementById('appt-reason').value
            };

            fetch('/api/appointment/create', {
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
            .catch(err => alert('❌ Erro ao agendar cita médica.'));
        });
    }

    // Create Patient Form
    const patientForm = document.getElementById('create-patient-form');
    if (patientForm) {
        patientForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                name: document.getElementById('pat-name').value,
                nif: document.getElementById('pat-nif').value,
                email: document.getElementById('pat-email').value,
                phone: document.getElementById('pat-phone').value,
                birth_date: document.getElementById('pat-birth-date').value,
                insurance: document.getElementById('pat-insurance').value,
                blood_type: document.getElementById('pat-blood-type').value
            };

            fetch('/api/patient/create', {
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
            .catch(err => alert('❌ Erro ao cadastrar paciente.'));
        });
    }

    // Create Professional Form
    const profForm = document.getElementById('create-professional-form');
    if (profForm) {
        profForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                name: document.getElementById('prof-name').value,
                specialty: document.getElementById('prof-specialty').value,
                license_no: document.getElementById('prof-license').value,
                email: document.getElementById('prof-email').value,
                phone: document.getElementById('prof-phone').value,
                consultation_fee: document.getElementById('prof-fee').value
            };

            fetch('/api/professional/create', {
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
            .catch(err => alert('❌ Erro ao cadastrar profissional.'));
        });
    }

    // Create Consultation Form
    const consultForm = document.getElementById('create-consultation-form');
    if (consultForm) {
        consultForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                appointment_id: document.getElementById('cons-appointment-id').value,
                diagnosis: document.getElementById('cons-diagnosis').value,
                symptoms: document.getElementById('cons-symptoms').value,
                prescription: document.getElementById('cons-prescription').value,
                vitals: document.getElementById('cons-vitals').value
            };

            fetch('/api/consultation/create', {
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
            .catch(err => alert('❌ Erro ao registar consulta clínica.'));
        });
    }

    // Create Document Form
    const docForm = document.getElementById('create-document-form');
    if (docForm) {
        docForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                patient_id: document.getElementById('doc-patient-id').value,
                title: document.getElementById('doc-title').value,
                doc_type: document.getElementById('doc-type').value,
                file_name: document.getElementById('doc-file-name').value
            };

            fetch('/api/document/create', {
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
            .catch(err => alert('❌ Erro ao anexar documento.'));
        });
    }

    // Create Payment / Invoice Form
    const payForm = document.getElementById('create-payment-form');
    if (payForm) {
        payForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                appointment_id: document.getElementById('pay-appointment-id').value,
                amount: document.getElementById('pay-amount').value,
                payment_method: document.getElementById('pay-method').value,
                status: document.getElementById('pay-status').value
            };

            fetch('/api/payment/create', {
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
            .catch(err => alert('❌ Erro ao emitir factura.'));
        });
    }
});

// Update Appointment Status
function updateAppointmentStatus(apptId, newStatus) {
    fetch(`/api/appointment/status/${apptId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
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
    .catch(err => alert('❌ Erro ao atualizar cita.'));
}
