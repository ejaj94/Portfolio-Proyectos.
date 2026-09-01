// FITCLUB GYM — Mobile App Logic & Interactive Engine

document.addEventListener('DOMContentLoaded', () => {
    initLiveClock();
    initThemeEngine();
    initEnrollForm();
    initClassBookingForm();
});

// Live Phone Clock Update
function initLiveClock() {
    const clockEl = document.getElementById('liveAppTime');
    function updateClock() {
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        if (clockEl) clockEl.textContent = `${hrs}:${mins}`;
    }
    updateClock();
    setInterval(updateClock, 10000);
}

// App Tab Switcher Engine
function switchTab(tabId, navBtn = null) {
    const allTabs = document.querySelectorAll('.app-view-tab');
    const navItems = document.querySelectorAll('.nav-tab-item');

    allTabs.forEach(t => t.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) {
        targetTab.classList.add('active');
        // Scroll view to top
        const viewport = document.querySelector('.app-views-viewport');
        if (viewport) viewport.scrollTop = 0;
    }

    // Update bottom nav active state
    navItems.forEach(item => item.classList.remove('active'));
    if (navBtn) {
        navBtn.classList.add('active');
    } else {
        // Find matching nav btn by onClick text or index
        const indexMap = {
            'tab-home': 0,
            'tab-plans': 1,
            'tab-schedule': 2,
            'tab-trainers': 3,
            'tab-enroll': 4
        };
        const idx = indexMap[tabId];
        if (idx !== undefined && navItems[idx]) {
            navItems[idx].classList.add('active');
        }
    }
}

// Select Plan from Plans Tab & Switch to Enrollment Tab
function selectPlanAndEnroll(planName, price) {
    const selectEl = document.getElementById('selectPlanChoice');
    if (selectEl) {
        // Select matching option
        for (let opt of selectEl.options) {
            if (opt.value.startsWith(planName)) {
                opt.selected = true;
                break;
            }
        }
    }
    switchTab('tab-enroll');
    showAppToast(`Plano ${planName} selecionado! Preencha os seus dados.`);
}

// Filter Classes by Day
function filterClasses(day, btnEl) {
    const allChips = document.querySelectorAll('.day-chip');
    const classRows = document.querySelectorAll('.class-card-row');

    allChips.forEach(c => c.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');

    classRows.forEach(row => {
        if (row.getAttribute('data-day') === day) {
            row.style.display = 'flex';
        } else {
            row.style.display = 'none';
        }
    });
}

// Class Booking Modal Logic
let currentBookingClassData = null;

function openClassBookingModal(className, classTime) {
    currentBookingClassData = { name: className, time: classTime };
    
    const modal = document.getElementById('classBookingModal');
    const titleEl = document.getElementById('modalClassName');
    const timeEl = document.getElementById('modalClassTime');

    if (titleEl) titleEl.textContent = className;
    if (timeEl) timeEl.textContent = `Horário: ${classTime}`;

    if (modal) modal.classList.add('active');
}

function closeClassModal() {
    const modal = document.getElementById('classBookingModal');
    if (modal) modal.classList.remove('active');
}

function initClassBookingForm() {
    const form = document.getElementById('classBookingForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('bookingName').value.trim();
        const phone = document.getElementById('bookingPhone').value.trim();

        if (!name || !phone) {
            showAppToast("Preencha o seu nome e telemóvel.", "error");
            return;
        }

        const btn = document.getElementById('btnConfirmBooking');
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Reservar...';

        try {
            const resp = await fetch('/api/class-booking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    class_name: currentBookingClassData ? currentBookingClassData.name : 'Aula FITCLUB',
                    class_time: currentBookingClassData ? currentBookingClassData.time : 'Horário Geral',
                    athlete_name: name,
                    athlete_phone: phone
                })
            });
            const data = await resp.json();

            if (data.success) {
                closeClassModal();
                showAppToast(`Lugar garantido na aula! A abrir WhatsApp...`);
                form.reset();
                setTimeout(() => {
                    window.open(data.whatsapp_url, '_blank');
                }, 1000);
            } else {
                showAppToast(data.message || "Erro ao reservar lugar.", "error");
            }
        } catch (err) {
            console.error(err);
            showAppToast("Erro na ligação ao servidor.", "error");
        } finally {
            btn.disabled = false;
            btn.innerHTML = 'Confirmar Lugar na Aula';
        }
    });
}

// Enrollment Form Engine
function initEnrollForm() {
    const form = document.getElementById('fitclubEnrollForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const planValue = document.getElementById('selectPlanChoice').value;
        const [planName, priceStr] = planValue.split('|');
        const price = parseFloat(priceStr || '39.90');

        const fullName = document.getElementById('enrollFullName').value.trim();
        const phone = document.getElementById('enrollPhone').value.trim();
        const email = document.getElementById('enrollEmail').value.trim();
        const startDate = document.getElementById('enrollStartDate').value;
        const notes = document.getElementById('enrollNotes').value.trim();

        // Get Addons
        const addonBoxes = document.querySelectorAll('input[name="addons"]:checked');
        const addonsList = Array.from(addonBoxes).map(b => b.value);

        const btn = document.getElementById('btnSubmitEnroll');
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Processar Matrícula...';

        try {
            const resp = await fetch('/api/enroll', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    full_name: fullName,
                    phone: phone,
                    email: email,
                    plan_name: planName,
                    monthly_price: price,
                    start_date: startDate,
                    addons: addonsList,
                    notes: notes
                })
            });
            const data = await resp.json();

            if (data.success) {
                showEnrollReceiptModal(data.enrollment, data.whatsapp_url);
                form.reset();
            } else {
                showAppToast(data.message || "Erro na matrícula.", "error");
            }
        } catch (err) {
            console.error(err);
            showAppToast("Erro de ligação ao servidor.", "error");
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-bolt"></i> Finalizar Inscrição via WhatsApp';
        }
    });
}

// Show Enrollment Digital Receipt Modal
function showEnrollReceiptModal(enrollment, waUrl) {
    const modal = document.getElementById('enrollReceiptModal');
    const rcId = document.getElementById('rcEnrollId');
    const rcAthlete = document.getElementById('rcAthlete');
    const rcPlan = document.getElementById('rcPlan');
    const rcStart = document.getElementById('rcStart');
    const btnWa = document.getElementById('btnWaReceiptLink');

    if (rcId) rcId.textContent = enrollment.id;
    if (rcAthlete) rcAthlete.textContent = enrollment.full_name;
    if (rcPlan) rcPlan.textContent = `${enrollment.plan_name} (${enrollment.monthly_price.toFixed(2)}€/mês)`;
    if (rcStart) rcStart.textContent = enrollment.start_date || 'Imediato';
    if (btnWa) btnWa.href = waUrl;

    if (modal) modal.classList.add('active');
}

function closeEnrollModal() {
    const modal = document.getElementById('enrollReceiptModal');
    if (modal) modal.classList.remove('active');
}

// Trainer Personal Booking Shortcut
function bookTrainerSession(trainerName) {
    switchTab('tab-enroll');
    showAppToast(`Sessão com ${trainerName} pré-selecionada!`);
}

// Direct WhatsApp Contact
function openWhatsAppContact() {
    const text = encodeURIComponent("Olá FITCLUB Gym Vilamoura! Gostaria de obter mais informações sobre as membresias e horários.");
    window.open(`https://wa.me/351911151993?text=${text}`, '_blank');
}

// App Toast Notifications
function showAppToast(message, type = 'success') {
    const container = document.getElementById('toastAppContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast-app ${type}`;
    toast.innerHTML = `
        <i class="fa-solid ${type === 'success' ? 'fa-circle-check text-neon' : 'fa-circle-exclamation text-yellow'}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Theme Toggle Engine (Dark / Light Mode)
function initThemeEngine() {
    const savedTheme = localStorage.getItem('fitclub_theme') || 'dark';
    setAppTheme(savedTheme);
}

function toggleAppTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setAppTheme(nextTheme);
    showAppToast(`Tema ${nextTheme === 'dark' ? 'Escuro' : 'Claro'} ativado!`);
}

function setAppTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('fitclub_theme', theme);

    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        if (theme === 'light') {
            themeIcon.className = 'fa-solid fa-moon text-purple';
        } else {
            themeIcon.className = 'fa-solid fa-sun text-yellow';
        }
    }
}
