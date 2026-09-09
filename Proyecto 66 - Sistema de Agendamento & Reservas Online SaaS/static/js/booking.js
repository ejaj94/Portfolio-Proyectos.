document.addEventListener('DOMContentLoaded', () => {
    const serviceCards = document.querySelectorAll('.service-select-card');
    const dateInput = document.getElementById('booking-date');
    const slotsContainer = document.getElementById('time-slots-container');
    const selectedServiceInput = document.getElementById('selected-service-id');
    const selectedTimeInput = document.getElementById('selected-booking-time');
    const bookingForm = document.getElementById('public-booking-form');

    let currentServiceId = selectedServiceInput ? selectedServiceInput.value : null;

    // Service selection
    serviceCards.forEach(card => {
        card.addEventListener('click', () => {
            serviceCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            currentServiceId = card.getAttribute('data-id');
            if (selectedServiceInput) selectedServiceInput.value = currentServiceId;
            fetchSlots();
        });
    });

    // Date change
    if (dateInput) {
        dateInput.addEventListener('change', fetchSlots);
    }

    // Fetch Slots AJAX
    function fetchSlots() {
        if (!dateInput || !slotsContainer || !currentServiceId) return;
        const selectedDate = dateInput.value;
        if (!selectedDate) return;

        slotsContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem;"><i class="fa-solid fa-spinner fa-spin"></i> A carregar horários disponíveis...</div>';

        fetch(`/api/available-slots?service_id=${currentServiceId}&date=${selectedDate}`)
            .then(res => res.json())
            .then(data => {
                slotsContainer.innerHTML = '';
                const slots = data.slots || [];
                if (slots.length === 0) {
                    slotsContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem;">Nenhum horário disponível para esta data.</div>';
                    return;
                }

                const grid = document.createElement('div');
                grid.className = 'time-slots-grid';

                slots.forEach(s => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = `time-slot-btn ${s.available ? '' : 'disabled'}`;
                    btn.innerText = s.time;

                    if (s.available) {
                        btn.addEventListener('click', () => {
                            grid.querySelectorAll('.time-slot-btn').forEach(b => b.classList.remove('selected'));
                            btn.classList.add('selected');
                            if (selectedTimeInput) selectedTimeInput.value = s.time;
                        });
                    } else {
                        btn.disabled = true;
                    }
                    grid.appendChild(btn);
                });

                slotsContainer.appendChild(grid);
            })
            .catch(err => {
                slotsContainer.innerHTML = '<div style="color: var(--blood-red); font-size: 0.9rem;">Erro ao carregar horários.</div>';
            });
    }

    // Initial fetch if date is prefilled
    if (dateInput && dateInput.value) {
        fetchSlots();
    }

    // Form submit
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();

            if (!selectedTimeInput || !selectedTimeInput.value) {
                alert('⚠️ Por favor selecione um horário disponível para a sua reserva.');
                return;
            }

            const formData = new FormData(bookingForm);
            const slug = window.CURRENT_SERVICE_SLUG || 'reserva';

            fetch(`/book/${slug}/submit`, {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('booking-card-container').style.display = 'none';
                    document.getElementById('success-msg-text').innerText = data.message;
                    document.getElementById('success-card').style.display = 'block';
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro na comunicação com o servidor.'));
        });
    }
});
