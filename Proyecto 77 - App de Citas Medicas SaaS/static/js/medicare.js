document.addEventListener('DOMContentLoaded', () => {
    // Book Appointment Form Handler
    const bookForm = document.getElementById('book-appointment-form');
    if (bookForm) {
        bookForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                patient_id: document.getElementById('book-patient-id').value,
                doctor_id: document.getElementById('book-doctor-id').value,
                specialty_id: document.getElementById('book-specialty-id') ? document.getElementById('book-specialty-id').value : null,
                appointment_date: document.getElementById('book-date').value,
                appointment_time: document.getElementById('book-time').value,
                reason: document.getElementById('book-reason').value
            };

            fetch('/api/appointment/book', {
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
            .catch(err => alert('❌ Erro ao agendar consulta.'));
        });
    }

    // Patient Registration Form Handler
    const patientForm = document.getElementById('create-patient-form');
    if (patientForm) {
        patientForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                name: document.getElementById('pat-name').value,
                email: document.getElementById('pat-email').value,
                phone: document.getElementById('pat-phone').value,
                birth_date: document.getElementById('pat-birth-date').value,
                blood_type: document.getElementById('pat-blood-type').value,
                nif: document.getElementById('pat-nif').value
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
});

// Update Appointment Status
function updateAppointmentStatus(apptId, newStatus) {
    let diagnosis = '';
    let prescription = '';

    if (newStatus === 'Concluída') {
        diagnosis = prompt('Registar diagnóstico médico:', 'Consulta de acompanhamento concluída com sucesso.');
        if (diagnosis === null) return;
        prescription = prompt('Registar prescrição / tratamento recomendado:', 'Medicação sintomática se necessário.');
    }

    fetch(`/api/appointment/status/${apptId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus, diagnosis: diagnosis || '', prescription: prescription || '' })
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
    .catch(err => alert('❌ Erro ao atualizar cita médica.'));
}

// Mark Notification as Read
function markNotificationRead(notifId) {
    fetch(`/api/notification/read/${notifId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    });
}
