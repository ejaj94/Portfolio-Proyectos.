// EJAJ TECH - Gourmet POS & Restaurant SaaS JavaScript Logic

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLanguage();
});

// Light / Dark Mode Toggle Logic
function initTheme() {
    const savedTheme = localStorage.getItem('ejaj_restaurant_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeButtonIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('ejaj_restaurant_theme', newTheme);
    updateThemeButtonIcon(newTheme);
}

function updateThemeButtonIcon(theme) {
    const btn = document.getElementById('themeToggleBtn');
    if (btn) {
        btn.innerHTML = theme === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Escuro';
    }
}

// Multi-Language Translation Dictionary (Pt-PT, ES, EN)
const i18n = {
    'pt': {
        'dashboard': 'Dashboard',
        'tables': 'Mesas',
        'reservations': 'Reservas',
        'orders': 'Comandas POS',
        'menu': 'Menú Digital',
        'kitchen': 'Cozinha (KDS)',
        'waiters': 'Empregados',
        'billing': 'Facturação',
        'active_tables': 'Mesas Ocupadas',
        'daily_revenue': 'Facturação do Dia',
        'kitchen_pending': 'Pratos a Cozinhar',
        'reservations_today': 'Reservas Hoje',
        'new_order': 'Nova Comanda POS',
        'new_reservation': 'Nova Reserva'
    },
    'es': {
        'dashboard': 'Panel Principal',
        'tables': 'Mesas',
        'reservations': 'Reservas',
        'orders': 'Comandas POS',
        'menu': 'Menú Digital',
        'kitchen': 'Cocina (KDS)',
        'waiters': 'Camareros',
        'billing': 'Facturación',
        'active_tables': 'Mesas Ocupadas',
        'daily_revenue': 'Facturación del Día',
        'kitchen_pending': 'Platos en Cocina',
        'reservations_today': 'Reservas Hoy',
        'new_order': 'Nueva Comanda',
        'new_reservation': 'Nueva Reserva'
    },
    'en': {
        'dashboard': 'Dashboard',
        'tables': 'Tables',
        'reservations': 'Bookings',
        'orders': 'POS Orders',
        'menu': 'Digital Menu',
        'kitchen': 'Kitchen Display',
        'waiters': 'Waitstaff',
        'billing': 'Billing & Receipts',
        'active_tables': 'Occupied Tables',
        'daily_revenue': 'Daily Revenue',
        'kitchen_pending': 'Cooking Orders',
        'reservations_today': 'Today Bookings',
        'new_order': 'New Order',
        'new_reservation': 'New Booking'
    }
};

function initLanguage() {
    const savedLang = localStorage.getItem('ejaj_restaurant_lang') || 'pt';
    const langSelect = document.getElementById('langSelect');
    if (langSelect) {
        langSelect.value = savedLang;
    }
    applyLanguage(savedLang);
}

function changeLanguage(lang) {
    localStorage.setItem('ejaj_restaurant_lang', lang);
    applyLanguage(lang);
}

function applyLanguage(lang) {
    const dictionary = i18n[lang] || i18n['pt'];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dictionary[key]) {
            el.innerText = dictionary[key];
        }
    });
}

// Update Table Status AJAX
async function updateTableStatus(tableId, status, waiterName = null) {
    try {
        const res = await fetch('/api/tables/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_id: tableId, status: status, waiter_name: waiterName })
        });

        const data = await res.json();
        if (data.success) {
            alert('Estado da mesa atualizado com sucesso!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Update Kitchen Item Status AJAX
async function updateKitchenStatus(itemId, newStatus) {
    try {
        const res = await fetch('/api/kitchen/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId, kitchen_status: newStatus })
        });

        const data = await res.json();
        if (data.success) {
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}

// POS Item Cart Builder Logic
const posCart = [];

function addToPosCart(itemName, price) {
    const existing = posCart.find(i => i.item_name === itemName);
    if (existing) {
        existing.quantity += 1;
    } else {
        posCart.push({ item_name: itemName, unit_price: price, quantity: 1 });
    }
    renderPosCart();
}

function removeFromPosCart(index) {
    posCart.splice(index, 1);
    renderPosCart();
}

function renderPosCart() {
    const tbody = document.getElementById('posCartTableBody');
    const totalEl = document.getElementById('posCartTotalDisplay');
    if (!tbody || !totalEl) return;

    tbody.innerHTML = '';
    let grandTotal = 0;

    posCart.forEach((item, index) => {
        const lineTotal = item.quantity * item.unit_price;
        grandTotal += lineTotal;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${item.item_name}</strong></td>
            <td>${item.quantity}</td>
            <td>€${item.unit_price.toFixed(2)}</td>
            <td><strong>€${lineTotal.toFixed(2)}</strong></td>
            <td><button type="button" class="btn btn-secondary btn-sm" onclick="removeFromPosCart(${index})">✕</button></td>
        `;
        tbody.appendChild(tr);
    });

    totalEl.innerText = '€' + (grandTotal * 1.23).toFixed(2) + ' (C/ IVA)';
}

// Submit POS Order AJAX
async function submitPosOrder(event) {
    event.preventDefault();
    const tableNum = document.getElementById('posTableSelect').value;
    const waiter = document.getElementById('posWaiterSelect').value;

    if (!tableNum || !waiter) {
        alert('Por favor escolha a mesa e o empregado.');
        return;
    }

    if (posCart.length === 0) {
        alert('Por favor adicione pelo menos um item ao pedido.');
        return;
    }

    try {
        const res = await fetch('/api/orders/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_number: parseInt(tableNum), waiter_name: waiter, items: posCart })
        });

        const data = await res.json();
        if (data.success) {
            alert('Comanda criada com sucesso! Código: ' + data.order_code);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Submit Reservation AJAX
async function submitReservation(event) {
    event.preventDefault();
    const name = document.getElementById('resGuestName').value.trim();
    const phone = document.getElementById('resGuestPhone').value.trim();
    const party = document.getElementById('resPartySize').value;
    const time = document.getElementById('resTime').value;
    const tableId = document.getElementById('resTableSelect').value;
    const notes = document.getElementById('resNotes').value.trim();

    try {
        const res = await fetch('/api/reservations/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                guest_name: name,
                guest_phone: phone,
                party_size: parseInt(party),
                reservation_time: time,
                table_id: parseInt(tableId),
                special_requests: notes
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('Reserva confirmada!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}

// Issue Invoice & Free Table AJAX
async function issueInvoice(orderId) {
    const method = prompt('Método de Pagamento (MBWay, Multibanco, Dinheiro, Cartão):', 'MBWay');
    if (!method) return;

    try {
        const res = await fetch('/api/invoices/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_id: parseInt(orderId), payment_method: method })
        });

        const data = await res.json();
        if (data.success) {
            alert('Fatura emitida: ' + data.invoice_code + '. Mesa libertada!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}
