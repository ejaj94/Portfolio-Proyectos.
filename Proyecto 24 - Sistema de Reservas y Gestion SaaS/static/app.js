/* SISTEMA DE RESERVAS & GESTÃO SAAS — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleDashboard: "Painel de Gestão de Reservas",
        subtitleDashboard: "Plataforma SaaS empresarial para controlo de agendamentos e clientes em tempo real.",
        btnNewBooking: "Nova Reserva",
        
        kpiTotal: "Total de Reservas",
        kpiOccupancy: "Taxa de Ocupação",
        kpiClients: "Clientes Ativos",
        kpiRevenue: "Receita Estimada",
        
        tableHeaderTitle: "Lista de Agendamentos & Reservas",
        tableSearchPlaceholder: "Pesquisar por cliente, e-mail ou serviço...",
        filterAll: "Todas",
        filterConfirmed: "Confirmadas",
        filterPending: "Pendentes",
        filterCanceled: "Canceladas",
        
        thId: "ID",
        thClient: "Cliente",
        thService: "Serviço",
        thDateTime: "Data & Hora",
        thStatus: "Estado",
        thPrice: "Preço",
        thActions: "Ações",
        
        modalTitle: "Criar Nova Reserva de Software",
        modalSubtitle: "Preencha os dados do agendamento para atualizar o sistema.",
        lblClientName: "Nome do Cliente *",
        lblClientEmail: "E-mail *",
        lblClientPhone: "Telemóvel / WhatsApp *",
        lblService: "Serviço / Procedimento *",
        lblDate: "Data do Agendamento *",
        lblTime: "Horário *",
        lblPrice: "Preço (€) *",
        btnSubmit: "Guardar Reserva no Sistema"
    },
    en: {
        titleDashboard: "Booking Management Dashboard",
        subtitleDashboard: "Enterprise SaaS platform for real-time scheduling and client control.",
        btnNewBooking: "New Booking",
        
        kpiTotal: "Total Bookings",
        kpiOccupancy: "Occupancy Rate",
        kpiClients: "Active Clients",
        kpiRevenue: "Estimated Revenue",
        
        tableHeaderTitle: "Appointments & Bookings Directory",
        tableSearchPlaceholder: "Search client, email or service...",
        filterAll: "All",
        filterConfirmed: "Confirmed",
        filterPending: "Pending",
        filterCanceled: "Canceled",
        
        thId: "ID",
        thClient: "Client",
        thService: "Service",
        thDateTime: "Date & Time",
        thStatus: "Status",
        thPrice: "Price",
        thActions: "Actions",
        
        modalTitle: "Create New SaaS Booking",
        modalSubtitle: "Enter appointment details to update real-time software schedule.",
        lblClientName: "Client Name *",
        lblClientEmail: "Email *",
        lblClientPhone: "Phone / WhatsApp *",
        lblService: "Service / Treatment *",
        lblDate: "Booking Date *",
        lblTime: "Time Slot *",
        lblPrice: "Price (€) *",
        btnSubmit: "Save Booking in System"
    },
    es: {
        titleDashboard: "Panel de Gestión de Reservas",
        subtitleDashboard: "Plataforma SaaS empresarial para control de citas y clientes en tiempo real.",
        btnNewBooking: "Nueva Reserva",
        
        kpiTotal: "Total de Reservas",
        kpiOccupancy: "Tasa de Ocupación",
        kpiClients: "Clientes Activos",
        kpiRevenue: "Ingresos Estimados",
        
        tableHeaderTitle: "Directorio de Citas y Reservas",
        tableSearchPlaceholder: "Buscar por cliente, email o servicio...",
        filterAll: "Todas",
        filterConfirmed: "Confirmadas",
        filterPending: "Pendientes",
        filterCanceled: "Canceladas",
        
        thId: "ID",
        thClient: "Cliente",
        thService: "Servicio",
        thDateTime: "Fecha y Hora",
        thStatus: "Estado",
        thPrice: "Precio",
        thActions: "Acciones",
        
        modalTitle: "Crear Nueva Reserva de Software",
        modalSubtitle: "Rellene los datos de la cita para actualizar el sistema.",
        lblClientName: "Nombre del Cliente *",
        lblClientEmail: "Correo Electrónico *",
        lblClientPhone: "Teléfono / WhatsApp *",
        lblService: "Servicio / Tratamiento *",
        lblDate: "Fecha de Reserva *",
        lblTime: "Horario *",
        lblPrice: "Precio (€) *",
        btnSubmit: "Guardar Reserva en Sistema"
    },
    fr: {
        titleDashboard: "Tableau de Bord de Gestion des Réservations",
        subtitleDashboard: "Plateforme SaaS d'entreprise pour la gestion des rendez-vous en temps réel.",
        btnNewBooking: "Nouvelle Réservation",
        
        kpiTotal: "Réservations Totales",
        kpiOccupancy: "Taux d'Occupation",
        kpiClients: "Clients Actifs",
        kpiRevenue: "Revenu Estimé",
        
        tableHeaderTitle: "Répertoire des Rendez-vous & Réservations",
        tableSearchPlaceholder: "Rechercher par client, e-mail ou service...",
        filterAll: "Toutes",
        filterConfirmed: "Confirmées",
        filterPending: "En Attente",
        filterCanceled: "Annulées",
        
        thId: "ID",
        thClient: "Client",
        thService: "Service",
        thDateTime: "Date & Heure",
        thStatus: "Statut",
        thPrice: "Prix",
        thActions: "Actions",
        
        modalTitle: "Créer une Nouvelle Réservation SaaS",
        modalSubtitle: "Saisissez les détails du rendez-vous pour mettre à jour le système.",
        lblClientName: "Nom du Client *",
        lblClientEmail: "E-mail *",
        lblClientPhone: "Téléphone / WhatsApp *",
        lblService: "Service / Prestation *",
        lblDate: "Date de Réservation *",
        lblTime: "Heure *",
        lblPrice: "Prix (€) *",
        btnSubmit: "Enregistrer dans le Système"
    }
};

let currentLang = 'pt';
let rawReservasData = [];
let activeFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchReservas();
    fetchClientes();
    
    // Set default date in modal
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('bookingDate').value = today;
});

function setLanguage(lang) {
    if (!i18n[lang]) return;
    currentLang = lang;
    
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    
    const dict = i18n[lang];
    document.querySelectorAll('[data-i18n]').forEach(elem => {
        const key = elem.getAttribute('data-i18n');
        if (dict[key]) {
            if (elem.tagName === 'INPUT') {
                elem.placeholder = dict[key];
            } else {
                elem.innerText = dict[key];
            }
        }
    });
    
    renderReservasTable();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiTotalVal').innerText = data.total_reservas;
            document.getElementById('kpiOccupancyVal').innerText = data.taxa_ocupacao;
            document.getElementById('kpiClientsVal').innerText = data.clientes_ativos;
            document.getElementById('kpiRevenueVal').innerText = data.receita_estimada;
        });
}

function fetchReservas() {
    fetch('/api/reservas')
        .then(res => res.json())
        .then(data => {
            rawReservasData = data;
            renderReservasTable();
        });
}

function fetchClientes() {
    fetch('/api/clientes')
        .then(res => res.json())
        .then(data => {
            renderClientesList(data);
        });
}

function setFilter(filterType) {
    activeFilter = filterType;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-filter') === filterType);
    });
    renderReservasTable();
}

function renderReservasTable() {
    const tbody = document.getElementById('reservasTableBody');
    const searchVal = document.getElementById('searchBox').value.toLowerCase();
    tbody.innerHTML = '';
    
    const filtered = rawReservasData.filter(r => {
        const matchesFilter = activeFilter === 'all' || 
            (activeFilter === 'confirmada' && r.estado === 'Confirmada') ||
            (activeFilter === 'pendente' && r.estado === 'Pendente') ||
            (activeFilter === 'cancelada' && r.estado === 'Cancelada');
            
        const matchesSearch = r.cliente.toLowerCase().includes(searchVal) ||
            r.email.toLowerCase().includes(searchVal) ||
            r.servico.toLowerCase().includes(searchVal) ||
            r.id.toLowerCase().includes(searchVal);
            
        return matchesFilter && matchesSearch;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 30px; color: var(--text-subtle);">Nenhum agendamento encontrado.</td></tr>`;
        return;
    }

    filtered.forEach(r => {
        const badgeClass = r.estado.toLowerCase();
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 900; color: var(--primary-indigo);">${r.id}</td>
            <td>
                <div>${r.cliente}</div>
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 600;">${r.telefone}</div>
            </td>
            <td>${r.servico}</td>
            <td>
                <div><i class="fa-solid fa-calendar-day" style="color: var(--primary-indigo);"></i> ${r.data}</div>
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 600;">${r.hora} (${r.duracao})</div>
            </td>
            <td><span class="badge-status ${badgeClass}">${r.estado}</span></td>
            <td style="font-weight: 900; color: var(--text-main);">${r.preco}</td>
            <td>
                ${r.estado !== 'Cancelada' ? `
                    <button class="btn-action-icon" title="Cancelar Reserva" onclick="cancelarReserva('${r.id}')">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                ` : `<span style="font-size: 11px; color: var(--text-subtle);">Cancelada</span>`}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderClientesList(clientes) {
    const list = document.getElementById('clientesList');
    if (!list) return;
    list.innerHTML = '';
    
    clientes.forEach(c => {
        const item = document.createElement('div');
        item.style.cssText = "display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--border-light);";
        item.innerHTML = `
            <div>
                <div style="font-weight: 800; font-size: 14px;">${c.nome}</div>
                <div style="font-size: 11px; color: var(--text-subtle);">${c.email}</div>
            </div>
            <span style="font-size: 11px; font-weight: 900; background: var(--primary-indigo-light); color: var(--primary-indigo); padding: 4px 10px; border-radius: 12px;">${c.tipo}</span>
        `;
        list.appendChild(item);
    });
}

function cancelarReserva(reservaId) {
    if (!confirm(`Tem a certeza que deseja cancelar a reserva ${reservaId}?`)) return;
    
    fetch(`/api/cancelar/${reservaId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                fetchReservas();
                fetchStats();
            }
        });
}

function openNewBookingModal() {
    document.getElementById('newBookingModal').classList.add('active');
}

function closeNewBookingModal() {
    document.getElementById('newBookingModal').classList.remove('active');
}

function submitNewBookingForm(event) {
    event.preventDefault();
    
    const newBookingData = {
        cliente: document.getElementById('bookingClient').value.trim(),
        email: document.getElementById('bookingEmail').value.trim(),
        telefone: document.getElementById('bookingPhone').value.trim(),
        servico: document.getElementById('bookingService').value,
        data: document.getElementById('bookingDate').value,
        hora: document.getElementById('bookingTime').value,
        preco: document.getElementById('bookingPrice').value.trim() + " €"
    };
    
    fetch('/api/reservas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newBookingData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewBookingModal();
            fetchReservas();
            fetchStats();
            fetchClientes();
        }
    });
}
