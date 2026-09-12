// EventCraft AI SaaS - Frontend Scripting (pt-PT)

document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch if page elements exist
    if (document.getElementById('eventsTableBody') || document.getElementById('eventsGrid')) {
        loadEvents();
    }
    if (document.getElementById('ticketsTableBody')) {
        loadTickets();
    }
    if (document.getElementById('usersTableBody')) {
        loadUsers();
    }
    if (document.getElementById('organizersGrid')) {
        loadOrganizers();
    }
    if (document.getElementById('recentCheckinsBody')) {
        loadCheckins();
    }
    if (document.getElementById('dashStats')) {
        loadDashboardStats();
    }
});

// Toast system
function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Modal helper
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add('active');
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('active');
}

// Load Dashboard Stats
async function loadDashboardStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        if (document.getElementById('statActiveEvents')) {
            document.getElementById('statActiveEvents').innerText = data.active_events;
        }
        if (document.getElementById('statTicketsSold')) {
            document.getElementById('statTicketsSold').innerText = data.total_tickets_sold;
        }
        if (document.getElementById('statCheckins')) {
            document.getElementById('statCheckins').innerText = data.total_checkins;
        }
        if (document.getElementById('statRevenue')) {
            document.getElementById('statRevenue').innerText = '€' + Number(data.total_revenue).toFixed(2);
        }
        if (document.getElementById('statOrganizers')) {
            document.getElementById('statOrganizers').innerText = data.total_organizers;
        }
        if (document.getElementById('statUsers')) {
            document.getElementById('statUsers').innerText = data.total_users;
        }
    } catch (err) {
        console.error('Erro ao carregar estatísticas:', err);
    }
}

// Load Events
async function loadEvents() {
    try {
        const res = await fetch('/api/events');
        const events = await res.json();
        
        const grid = document.getElementById('eventsGrid');
        if (grid) {
            grid.innerHTML = events.map(e => `
                <div class="event-card">
                    <div class="event-card-header">
                        <div>
                            <span class="badge badge-purple">${e.category}</span>
                            <h3 style="margin-top:0.5rem; font-size:1.15rem;">${e.title}</h3>
                        </div>
                        <span class="badge badge-${e.status === 'Ativo' ? 'active' : 'pending'}">${e.status}</span>
                    </div>
                    <div class="event-card-body">
                        <div class="event-detail-item"><i class="fa-solid fa-building text-secondary"></i> ${e.organizer_company}</div>
                        <div class="event-detail-item"><i class="fa-solid fa-location-dot text-secondary"></i> ${e.venue_name}, ${e.city}</div>
                        <div class="event-detail-item"><i class="fa-solid fa-calendar-days text-secondary"></i> ${e.event_date} às ${e.event_time}</div>
                        <div class="event-detail-item"><i class="fa-solid fa-ticket text-secondary"></i> ${e.available_tickets} bilhetes disponíveis (Lotação: ${e.total_capacity})</div>
                    </div>
                    <div class="event-card-footer">
                        <span style="font-weight:700; font-size:1.1rem; color:#a855f7;">€${Number(e.ticket_price).toFixed(2)}</span>
                        <button class="btn btn-primary btn-sm" onclick="prepareBuyTicket(${e.id}, '${e.title.replace(/'/g, "\\'")}', ${e.ticket_price})">
                            <i class="fa-solid fa-cart-shopping"></i> Comprar Bilhete
                        </button>
                    </div>
                </div>
            `).join('');
        }

        const tbody = document.getElementById('eventsTableBody');
        if (tbody) {
            tbody.innerHTML = events.map(e => `
                <tr>
                    <td><strong>${e.title}</strong><br><small class="text-muted">${e.category}</small></td>
                    <td>${e.organizer_company}</td>
                    <td>${e.venue_name}, ${e.city}</td>
                    <td>${e.event_date} ${e.event_time}</td>
                    <td>€${Number(e.ticket_price).toFixed(2)}</td>
                    <td>${e.available_tickets} / ${e.total_capacity}</td>
                    <td><span class="badge badge-${e.status === 'Ativo' ? 'active' : 'pending'}">${e.status}</span></td>
                    <td>
                        <button class="btn btn-secondary btn-sm" onclick="prepareBuyTicket(${e.id}, '${e.title.replace(/'/g, "\\'")}', ${e.ticket_price})">
                            <i class="fa-solid fa-ticket"></i> Emitir
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Erro ao carregar eventos:', err);
    }
}

// Prepare Ticket Buy Modal
function prepareBuyTicket(eventId, eventTitle, price) {
    document.getElementById('buyEventId').value = eventId;
    document.getElementById('buyEventTitle').innerText = eventTitle;
    document.getElementById('buyEventPrice').innerText = '€' + Number(price).toFixed(2);
    openModal('buyTicketModal');
}

// Buy Ticket Form Submit
async function submitBuyTicket(e) {
    e.preventDefault();
    const eventId = document.getElementById('buyEventId').value;
    const userId = document.getElementById('buyUserId').value;
    const seatNumber = document.getElementById('buySeatNumber').value;
    
    try {
        const res = await fetch('/api/tickets/purchase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_id: parseInt(eventId),
                user_id: parseInt(userId),
                seat_number: seatNumber || 'Livre'
            })
        });
        const data = await res.json();
        if (data.success) {
            showToast('Bilhete emitido com sucesso! Código: ' + data.ticket_code, 'success');
            closeModal('buyTicketModal');
            loadEvents();
            if (document.getElementById('ticketsTableBody')) loadTickets();
            if (document.getElementById('dashStats')) loadDashboardStats();
        } else {
            showToast('Erro: ' + (data.error || 'Não foi possível emitir o bilhete'), 'error');
        }
    } catch (err) {
        showToast('Erro na ligação ao servidor', 'error');
    }
}

// Load Tickets
async function loadTickets() {
    try {
        const res = await fetch('/api/tickets');
        const tickets = await res.json();
        
        const tbody = document.getElementById('ticketsTableBody');
        if (tbody) {
            tbody.innerHTML = tickets.map(t => `
                <tr>
                    <td><code>${t.ticket_code}</code></td>
                    <td><strong>${t.event_title}</strong><br><small class="text-muted">${t.event_date}</small></td>
                    <td>${t.user_name}<br><small class="text-muted">${t.user_email}</small></td>
                    <td>${t.seat_number || 'Geral'}</td>
                    <td>€${Number(t.price_paid).toFixed(2)}</td>
                    <td><span class="badge badge-${t.checkin_status === 'Validado' ? 'active' : 'pending'}">${t.checkin_status}</span></td>
                    <td>
                        <button class="btn btn-secondary btn-sm" onclick="showQRModal('${t.ticket_code}', '${t.event_title.replace(/'/g, "\\'")}', '${t.user_name.replace(/'/g, "\\'")}')">
                            <i class="fa-solid fa-qrcode"></i> Ver QR
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Erro ao carregar bilhetes:', err);
    }
}

// Show QR Code Modal
function showQRModal(ticketCode, eventTitle, userName) {
    document.getElementById('modalQRTitle').innerText = eventTitle;
    document.getElementById('modalQRUser').innerText = 'Participante: ' + userName;
    document.getElementById('modalQRCode').innerText = ticketCode;
    
    // Generate QR visual placeholder using QuickChart or simple svg
    const qrContainer = document.getElementById('qrImageContainer');
    qrContainer.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(ticketCode)}" alt="QR Code Bilhete" style="border-radius:12px; border:4px solid #7c3aed;">`;
    
    openModal('qrModal');
}

// Checkin Process
async function validateCheckin(e) {
    if (e) e.preventDefault();
    const input = document.getElementById('scanCodeInput');
    const code = input.value.trim();
    if (!code) {
        showToast('Introduza um código de bilhete válido', 'error');
        return;
    }
    
    try {
        const res = await fetch('/api/checkin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket_code: code, scanned_by: 'Controlo de Acesso Portal' })
        });
        const data = await res.json();
        if (data.success) {
            showToast(data.message, 'success');
            input.value = '';
            loadCheckins();
            if (document.getElementById('dashStats')) loadDashboardStats();
        } else {
            showToast('Atenção: ' + data.error, 'error');
        }
    } catch (err) {
        showToast('Erro ao validar check-in', 'error');
    }
}

// Load Checkins list
async function loadCheckins() {
    try {
        const res = await fetch('/api/checkin/logs');
        const logs = await res.json();
        const tbody = document.getElementById('recentCheckinsBody');
        if (tbody) {
            tbody.innerHTML = logs.map(l => `
                <tr>
                    <td><code>${l.ticket_code}</code></td>
                    <td><strong>${l.event_title}</strong></td>
                    <td>${l.user_name}</td>
                    <td>${l.checkin_time}</td>
                    <td><span class="badge badge-active"><i class="fa-solid fa-circle-check"></i> Validado</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Erro ao carregar registos de checkin:', err);
    }
}

// Load Users
async function loadUsers() {
    try {
        const res = await fetch('/api/users');
        const users = await res.json();
        const tbody = document.getElementById('usersTableBody');
        if (tbody) {
            tbody.innerHTML = users.map(u => `
                <tr>
                    <td>#${u.id}</td>
                    <td><strong>${u.name}</strong></td>
                    <td>${u.email}</td>
                    <td>${u.phone || '-'}</td>
                    <td><span class="badge badge-purple">${u.tickets_bought} bilhetes</span></td>
                    <td>${u.created_at}</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Erro ao carregar utilizadores:', err);
    }
}

// Load Organizers
async function loadOrganizers() {
    try {
        const res = await fetch('/api/organizers');
        const orgs = await res.json();
        const grid = document.getElementById('organizersGrid');
        if (grid) {
            grid.innerHTML = orgs.map(o => `
                <div class="event-card">
                    <div class="event-card-header">
                        <div>
                            <span class="badge badge-cyan">${o.category || 'Organizador'}</span>
                            <h3 style="margin-top:0.5rem;">${o.company_name}</h3>
                        </div>
                    </div>
                    <div class="event-card-body">
                        <div class="event-detail-item"><i class="fa-solid fa-user text-secondary"></i> ${o.name}</div>
                        <div class="event-detail-item"><i class="fa-solid fa-envelope text-secondary"></i> ${o.email}</div>
                        <div class="event-detail-item"><i class="fa-solid fa-phone text-secondary"></i> ${o.phone}</div>
                        <div class="event-detail-item"><i class="fa-solid fa-calendar text-secondary"></i> ${o.total_events} eventos criados</div>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error('Erro ao carregar organizadores:', err);
    }
}

// Create Event Submit
async function submitCreateEvent(e) {
    e.preventDefault();
    const title = document.getElementById('evtTitle').value;
    const category = document.getElementById('evtCategory').value;
    const organizer_id = document.getElementById('evtOrganizer').value;
    const venue_name = document.getElementById('evtVenue').value;
    const city = document.getElementById('evtCity').value;
    const event_date = document.getElementById('evtDate').value;
    const event_time = document.getElementById('evtTime').value;
    const total_capacity = document.getElementById('evtCapacity').value;
    const ticket_price = document.getElementById('evtPrice').value;

    try {
        const res = await fetch('/api/events/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title, category, organizer_id: parseInt(organizer_id), venue_name, city,
                event_date, event_time, total_capacity: parseInt(total_capacity),
                ticket_price: parseFloat(ticket_price)
            })
        });
        const data = await res.json();
        if (data.success) {
            showToast('Evento criado com sucesso!', 'success');
            closeModal('createEventModal');
            loadEvents();
            if (document.getElementById('dashStats')) loadDashboardStats();
        } else {
            showToast('Erro ao criar evento', 'error');
        }
    } catch (err) {
        showToast('Erro no servidor', 'error');
    }
}

// Table Search Filter
function filterTable(inputId, tableBodyId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const tbody = document.getElementById(tableBodyId);
    if (!tbody) return;
    const rows = tbody.getElementsByTagName('tr');

    for (let row of rows) {
        const text = row.textContent || row.innerText;
        row.style.display = text.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
    }
}
