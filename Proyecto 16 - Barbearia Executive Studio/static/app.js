document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const bookingForm = document.getElementById('bookingForm');

    const selService = document.getElementById('selService');
    const selBarber = document.getElementById('selBarber');
    const inputDate = document.getElementById('inputDate');
    const selTime = document.getElementById('selTime');
    const inputClientName = document.getElementById('inputClientName');
    const inputClientPhone = document.getElementById('inputClientPhone');
    const inputClientEmail = document.getElementById('inputClientEmail');
    const inputNotes = document.getElementById('inputNotes');
    const btnSubmitBooking = document.getElementById('btnSubmitBooking');

    // Receipt Modal Elements
    const receiptModal = document.getElementById('receiptModal');
    const btnCloseModal = document.getElementById('btnCloseModal');
    const btnFinishModal = document.getElementById('btnFinishModal');
    const rcId = document.getElementById('rcId');
    const rcClient = document.getElementById('rcClient');
    const rcService = document.getElementById('rcService');
    const rcBarber = document.getElementById('rcBarber');
    const rcDateTime = document.getElementById('rcDateTime');
    const btnModalWa = document.getElementById('btnModalWa');

    // Set Minimum Date to Today
    if (inputDate) {
        const today = new Date().toISOString().split('T')[0];
        inputDate.min = today;
        inputDate.value = today;
    }

    // Mobile Drawer Toggle
    if (mobileMenuToggle && mobileDrawer) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileDrawer.classList.toggle('open');
        });

        document.querySelectorAll('.mobile-link').forEach(link => {
            link.addEventListener('click', () => {
                mobileDrawer.classList.remove('open');
            });
        });
    }

    // Helper functions for selecting Service / Barber from card buttons
    window.selectService = (serviceName) => {
        if (selService) {
            for (let i = 0; i < selService.options.length; i++) {
                if (selService.options[i].value.includes(serviceName) || serviceName.includes(selService.options[i].value)) {
                    selService.selectedIndex = i;
                    break;
                }
            }
        }
        const bookingSection = document.getElementById('booking');
        if (bookingSection) {
            bookingSection.scrollIntoView({ behavior: 'smooth' });
        }
    };

    window.selectBarber = (barberName) => {
        if (selBarber) {
            for (let i = 0; i < selBarber.options.length; i++) {
                if (selBarber.options[i].value === barberName) {
                    selBarber.selectedIndex = i;
                    break;
                }
            }
        }
        const bookingSection = document.getElementById('booking');
        if (bookingSection) {
            bookingSection.scrollIntoView({ behavior: 'smooth' });
        }
    };

    // Booking Submission Handler
    if (bookingForm) {
        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const serviceVal = selService.value;
            const dateVal = inputDate.value;
            const timeVal = selTime.value;
            const nameVal = inputClientName.value.trim();
            const phoneVal = inputClientPhone.value.trim();

            if (!serviceVal || !dateVal || !timeVal || !nameVal || !phoneVal) {
                showToast('Por favor, preencha todos os campos obrigatórios.', 'error');
                return;
            }

            btnSubmitBooking.disabled = true;
            btnSubmitBooking.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Registar Marcação...';

            const payload = {
                service: serviceVal,
                barber: selBarber.value,
                booking_date: dateVal,
                booking_time: timeVal,
                client_name: nameVal,
                client_phone: phoneVal,
                client_email: inputClientEmail.value.trim(),
                notes: inputNotes.value.trim()
            };

            try {
                const res = await fetch('/api/booking', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await res.json();

                if (res.ok && data.success) {
                    const b = data.booking;
                    rcId.textContent = b.id;
                    rcClient.textContent = b.client_name;
                    rcService.textContent = b.service;
                    rcBarber.textContent = b.barber;
                    rcDateTime.textContent = `${b.booking_date} às ${b.booking_time}`;

                    // Set WhatsApp Direct Confirmation Link
                    const waText = `Olá Barbearia Império! Gostaria de confirmar a minha marcação:\n\n` +
                                  `📌 Código: ${b.id}\n` +
                                  `👤 Nome: ${b.client_name}\n` +
                                  `💈 Serviço: ${b.service}\n` +
                                  `✂️ Barbeiro: ${b.barber}\n` +
                                  `📅 Data: ${b.booking_date}\n` +
                                  `⏰ Hora: ${b.booking_time}\n` +
                                  `📞 Telemóvel: ${b.client_phone}`;

                    btnModalWa.href = `https://wa.me/351925814730?text=${encodeURIComponent(waText)}`;

                    receiptModal.classList.add('open');
                    showToast('Marcação realizada com sucesso!', 'success');
                    bookingForm.reset();
                } else {
                    showToast(data.message || 'Erro ao efetuar a marcação.', 'error');
                }
            } catch (err) {
                showToast('Falha na ligação com o servidor.', 'error');
            } finally {
                btnSubmitBooking.disabled = false;
                btnSubmitBooking.innerHTML = '<i class="fa-solid fa-circle-check"></i> Confirmar Marcação Instantânea';
            }
        });
    }

    // Modal Close Handlers
    if (btnCloseModal) {
        btnCloseModal.addEventListener('click', () => {
            receiptModal.classList.remove('open');
        });
    }

    if (btnFinishModal) {
        btnFinishModal.addEventListener('click', () => {
            receiptModal.classList.remove('open');
        });
    }

    receiptModal.addEventListener('click', (e) => {
        if (e.target === receiptModal) {
            receiptModal.classList.remove('open');
        }
    });

    // Toast Notification System
    function showToast(msg, type = 'success') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<i class="fa-solid fa-circle-info"></i> <span>${msg}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(-100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
});
