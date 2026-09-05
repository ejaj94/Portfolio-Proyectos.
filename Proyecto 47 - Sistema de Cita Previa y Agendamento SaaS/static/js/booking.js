/**
 * Generic Appointment Booking System SaaS (Proyecto 47)
 * Client-Side Controller & Availability Engine
 */

window.bookingApp = {
    step: 1,
    bookingData: {
        professional_id: null,
        professional_name: '',
        service_id: null,
        service_title: '',
        service_duration: 0,
        service_price: 0,
        date: '',
        start_time: '',
        client_name: '',
        client_email: '',
        client_phone: '',
        client_notes: ''
    },

    init: function() {
        console.log('[BOOKING SAAS] Sistema de Cita Previa & Agendamento Inicializado.');
        this.bindEvents();
    },

    bindEvents: function() {
        const dateInput = document.getElementById('bookingDatePicker');
        if (dateInput) {
            dateInput.addEventListener('change', (e) => {
                this.bookingData.date = e.target.value;
                this.fetchAvailability();
            });
        }
    },

    selectService: function(id, title, duration, price, profId, profName) {
        this.bookingData.service_id = id;
        this.bookingData.service_title = title;
        this.bookingData.service_duration = duration;
        this.bookingData.service_price = price;

        if (profId) {
            this.bookingData.professional_id = profId;
            this.bookingData.professional_name = profName;
        }

        this.goToStep(2);
    },

    selectProfessional: function(id, name) {
        this.bookingData.professional_id = id;
        this.bookingData.professional_name = name;

        // Set default date to tomorrow if empty
        if (!this.bookingData.date) {
            const tmr = new Date();
            tmr.setDate(tmr.getDate() + 1);
            this.bookingData.date = tmr.toISOString().split('T')[0];
            const dateInput = document.getElementById('bookingDatePicker');
            if (dateInput) dateInput.value = this.bookingData.date;
        }

        this.goToStep(3);
        this.fetchAvailability();
    },

    goToStep: function(nextStep) {
        this.step = nextStep;

        // Update Wizard Bar UI
        for (let i = 1; i <= 4; i++) {
            const stepItem = document.getElementById(`step-item-${i}`);
            const pane = document.getElementById(`wizard-pane-${i}`);

            if (stepItem) {
                stepItem.classList.remove('active', 'completed');
                if (i < nextStep) stepItem.classList.add('completed');
                if (i === nextStep) stepItem.classList.add('active');
            }

            if (pane) {
                pane.style.display = (i === nextStep) ? 'block' : 'none';
            }
        }

        if (nextStep === 4) {
            this.updateSummaryUI();
        }
    },

    fetchAvailability: function() {
        if (!this.bookingData.professional_id || !this.bookingData.date) return;

        const container = document.getElementById('slotsContainer');
        if (container) {
            container.innerHTML = '<div class="text-center text-muted py-4"><span class="spinner-border spinner-border-sm me-2"></span>A calcular horários livres na agenda...</div>';
        }

        const url = `/api/availability?professional_id=${this.bookingData.professional_id}&service_id=${this.bookingData.service_id || ''}&date=${this.bookingData.date}`;
        fetch(url)
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.renderSlots(data.slots, data.available, data.message);
                } else {
                    if (container) container.innerHTML = `<div class="alert alert-warning">${data.message}</div>`;
                }
            })
            .catch(err => {
                console.error('Erro na disponibilidade:', err);
                if (container) container.innerHTML = '<div class="alert alert-danger">Erro ao ligar à agenda.</div>';
            });
    },

    renderSlots: function(slots, isAvailable, message) {
        const container = document.getElementById('slotsContainer');
        if (!container) return;

        if (!isAvailable || slots.length === 0) {
            container.innerHTML = `
                <div class="p-4 bg-dark rounded-3 text-center border border-secondary">
                    <i class="bi bi-calendar-x text-warning fs-2 mb-2 d-block"></i>
                    <h6 class="text-white fw-bold mb-1">${message || 'Sem vagas disponíveis para esta data.'}</h6>
                    <small class="text-muted">Por favor selecione outro dia no calendário acima.</small>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="slot-grid">
                ${slots.map(t => `
                    <div class="slot-pill ${this.bookingData.start_time === t ? 'active' : ''}" onclick="bookingApp.selectSlot('${t}', this)">
                        <i class="bi bi-clock me-1"></i>${t}
                    </div>
                `).join('')}
            </div>
        `;
    },

    selectSlot: function(time, element) {
        this.bookingData.start_time = time;
        document.querySelectorAll('.slot-pill').forEach(p => p.classList.remove('active'));
        if (element) element.classList.add('active');

        const btnStep3Next = document.getElementById('btnStep3Next');
        if (btnStep3Next) btnStep3Next.disabled = false;
    },

    updateSummaryUI: function() {
        if (document.getElementById('sumService')) document.getElementById('sumService').innerText = this.bookingData.service_title;
        if (document.getElementById('sumProf')) document.getElementById('sumProf').innerText = this.bookingData.professional_name;
        if (document.getElementById('sumDate')) document.getElementById('sumDate').innerText = `${this.bookingData.date} às ${this.bookingData.start_time}`;
        if (document.getElementById('sumDuration')) document.getElementById('sumDuration').innerText = `${this.bookingData.service_duration} minutos`;
        if (document.getElementById('sumPrice')) document.getElementById('sumPrice').innerText = `€ ${this.bookingData.service_price.toFixed(2)}`;
    },

    submitBooking: function() {
        this.bookingData.client_name = document.getElementById('clientName').value.trim();
        this.bookingData.client_email = document.getElementById('clientEmail').value.trim();
        this.bookingData.client_phone = document.getElementById('clientPhone').value.trim();
        this.bookingData.client_notes = document.getElementById('clientNotes').value.trim();

        if (!this.bookingData.client_name || !this.bookingData.client_phone) {
            alert('Por favor preencha o seu nome e número de telemóvel.');
            return;
        }

        fetch('/api/appointments/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.bookingData)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('confirmedCodeLbl').innerText = data.code;
                document.getElementById('confirmedMessageLbl').innerText = data.message;
                const modal = new bootstrap.Modal(document.getElementById('confirmationModal'));
                modal.show();
            } else {
                alert(`⚠️ ${data.message}`);
            }
        })
        .catch(err => {
            console.error('Erro ao efetuar agendamento:', err);
            alert('Ocorreu um erro ao submeter o agendamento.');
        });
    },

    cancelAppointment: function(codeOrId) {
        const reason = prompt('Por favor especifique o motivo do cancelamento:', 'Impossibilidade de comparência');
        if (reason === null) return;

        fetch('/api/appointments/cancel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code_or_id: codeOrId, reason: reason })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✅ ${data.message}`);
                window.location.reload();
            }
        });
    },

    sendReminder: function(appointmentId) {
        fetch('/api/reminders/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ appointment_id: appointmentId })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`📲 ${data.message}`);
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    bookingApp.init();
});
