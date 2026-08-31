document.addEventListener('DOMContentLoaded', () => {
    // ─── 1. GOLD DUST CANVAS PARTICLES ENGINE ───
    const canvas = document.getElementById('goldDustCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const particles = [];
        const particleCount = 45;

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 2 + 0.5,
                color: Math.random() > 0.5 ? '#f59e0b' : '#fef08a',
                alpha: Math.random() * 0.6 + 0.2,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.4 - 0.2
            });
        }

        function animateGoldDust() {
            ctx.clearRect(0, 0, width, height);

            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;

                if (p.y < 0) p.y = height;
                if (p.x < 0) p.x = width;
                if (p.x > width) p.x = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha;
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#d97706';
                ctx.fill();
            });

            ctx.globalAlpha = 1;
            requestAnimationFrame(animateGoldDust);
        }

        animateGoldDust();
    }

    // ─── 2. DOM ELEMENTS ───
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const restaurantBookingForm = document.getElementById('restaurantBookingForm');

    const selGuests = document.getElementById('selGuests');
    const selSeating = document.getElementById('selSeating');
    const inputResDate = document.getElementById('inputResDate');
    const selResTime = document.getElementById('selResTime');
    const inputClientName = document.getElementById('inputClientName');
    const inputClientPhone = document.getElementById('inputClientPhone');
    const inputClientEmail = document.getElementById('inputClientEmail');
    const inputNotes = document.getElementById('inputNotes');
    const btnSubmitReservation = document.getElementById('btnSubmitReservation');

    // Modal Elements
    const receiptModal = document.getElementById('receiptModal');
    const btnCloseModal = document.getElementById('btnCloseModal');
    const btnFinishModal = document.getElementById('btnFinishModal');
    const rcId = document.getElementById('rcId');
    const rcClient = document.getElementById('rcClient');
    const rcGuests = document.getElementById('rcGuests');
    const rcSeating = document.getElementById('rcSeating');
    const rcDateTime = document.getElementById('rcDateTime');
    const btnModalWa = document.getElementById('btnModalWa');

    // Minimum Date = Today
    if (inputResDate) {
        const today = new Date().toISOString().split('T')[0];
        inputResDate.min = today;
        inputResDate.value = today;
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

    // ─── 3. CATEGORY FILTER SYSTEM ───
    const filterTabs = document.querySelectorAll('.menu-tab-btn');
    const menuCards = document.querySelectorAll('.gourmet-card');

    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const category = tab.getAttribute('data-category');

            menuCards.forEach(card => {
                const cardCat = card.getAttribute('data-category');
                if (category === 'all' || cardCat === category) {
                    card.style.display = 'flex';
                    card.style.animation = 'modalSlideUp 0.3s ease';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Select Dish for Booking Helper
    window.selectDish = (dishName) => {
        if (inputNotes) {
            if (inputNotes.value) {
                inputNotes.value += `, Prato pretendido: ${dishName}`;
            } else {
                inputNotes.value = `Prato pretendido: ${dishName}`;
            }
        }
        const bookingSection = document.getElementById('booking');
        if (bookingSection) {
            bookingSection.scrollIntoView({ behavior: 'smooth' });
        }
    };

    // ─── 4. BOOKING SUBMISSION HANDLER ───
    if (restaurantBookingForm) {
        restaurantBookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const guestsVal = selGuests.value;
            const dateVal = inputResDate.value;
            const timeVal = selResTime.value;
            const nameVal = inputClientName.value.trim();
            const phoneVal = inputClientPhone.value.trim();

            if (!guestsVal || !dateVal || !timeVal || !nameVal || !phoneVal) {
                showToast('Por favor, preencha todos os campos obrigatórios da reserva.', 'error');
                return;
            }

            btnSubmitReservation.disabled = true;
            btnSubmitReservation.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Confirmar Mesa...';

            const payload = {
                guests: guestsVal,
                seating_area: selSeating.value,
                res_date: dateVal,
                res_time: timeVal,
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
                    const r = data.reservation;
                    rcId.textContent = r.id;
                    rcClient.textContent = r.client_name;
                    rcGuests.textContent = r.guests;
                    rcSeating.textContent = r.seating_area;
                    rcDateTime.textContent = `${r.res_date} às ${r.res_time}`;

                    const waText = `Olá L'Étoile Gourmet! Gostaria de confirmar a minha reserva de mesa:\n\n` +
                                  `📌 Código: ${r.id}\n` +
                                  `👤 Nome: ${r.client_name}\n` +
                                  `👥 Pessoas: ${r.guests}\n` +
                                  `🍷 Área: ${r.seating_area}\n` +
                                  `📅 Data: ${r.res_date}\n` +
                                  `⏰ Hora: ${r.res_time}\n` +
                                  `📞 Telemóvel: ${r.client_phone}`;

                    btnModalWa.href = `https://wa.me/351911151993?text=${encodeURIComponent(waText)}`;

                    receiptModal.classList.add('open');
                    showToast('Reserva de mesa efetuada com sucesso!', 'success');
                    restaurantBookingForm.reset();
                } else {
                    showToast(data.message || 'Erro ao efetuar a reserva.', 'error');
                }
            } catch (err) {
                showToast('Falha na ligação com o servidor.', 'error');
            } finally {
                btnSubmitReservation.disabled = false;
                btnSubmitReservation.innerHTML = '<i class="fa-solid fa-circle-check"></i> Confirmar Reserva de Mesa Instantânea';
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

    if (receiptModal) {
        receiptModal.addEventListener('click', (e) => {
            if (e.target === receiptModal) {
                receiptModal.classList.remove('open');
            }
        });
    }

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
