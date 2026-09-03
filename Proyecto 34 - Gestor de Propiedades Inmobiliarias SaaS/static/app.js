/* NEXUS REALTY & PROPERTY SaaS — JAVASCRIPT ENGINE WITH PHOTO GALLERY MODAL */

const i18n = {
    pt: {
        titleProperty: "Gestor de Propriedades Imobiliárias",
        subtitleProperty: "Administração de imóveis residenciais, inquilinos, pagamento de rendas e incidências.",
        btnNewProperty: "Registar Nova Propriedade",
        
        kpiTotalProp: "Total Propriedades",
        kpiMonthlyRevenue: "Renda Mensal Total",
        kpiOccupancy: "Taxa de Ocupação",
        kpiIncidents: "Incidências Abertas",
        kpiTenants: "Inquilinos Ativos",
        
        secProperties: "Catálogo de Propriedades & Imóveis",
        secTenants: "Diretório de Inquilinos",
        secPayments: "Histórico de Pagamento de Rendas",
        secIncidents: "Gestão de Incidências & Manutenção",
        
        thTenant: "Inquilino",
        thUnit: "Imóvel Alugado",
        thContact: "Contacto / Email",
        thRent: "Renda Mensal",
        thStartDate: "Contrato Desde",
        thStatus: "Estado Pago",
        
        thProperty: "Propriedade",
        thAmount: "Valor Renda",
        thRefMonth: "Mês Referência",
        thPayDate: "Data de Pagamento",
        thMethod: "Método",
        
        thTicket: "Incidência / Avaria",
        thPriority: "Prioridade",
        thOpenDate: "Data Abertura",
        thCost: "Custo Estimado",
        
        modalTitle: "Registar Nova Propriedade Residencial",
        modalSubtitle: "Introduza os detalhes do imóvel e do proprietário.",
        lblPropTitle: "Título do Imóvel *",
        lblType: "Tipo de Imóvel *",
        lblAddress: "Morada Completa *",
        lblRentVal: "Valor da Renda (€/mês) *",
        lblTypology: "Tipologia (Ex: T2, T3) *",
        lblOwner: "Proprietário *",
        btnSubmitProp: "Guardar Imóvel"
    },
    en: {
        titleProperty: "Real Estate Property Management SaaS",
        subtitleProperty: "Residential properties, tenant tracking, monthly rent collection and maintenance tickets.",
        btnNewProperty: "Register New Property",
        
        kpiTotalProp: "Total Properties",
        kpiMonthlyRevenue: "Total Monthly Rent",
        kpiOccupancy: "Occupancy Rate",
        kpiIncidents: "Open Incidents",
        kpiTenants: "Active Tenants",
        
        secProperties: "Property Directory & Listings",
        secTenants: "Tenant Directory",
        secPayments: "Rent Payments Ledger",
        secIncidents: "Maintenance & Repairs Tickets",
        
        thTenant: "Tenant Name",
        thUnit: "Leased Unit",
        thContact: "Contact / Email",
        thRent: "Monthly Rent",
        thStartDate: "Lease Since",
        thStatus: "Payment Status",
        
        thProperty: "Property",
        thAmount: "Rent Amount",
        thRefMonth: "Reference Month",
        thPayDate: "Payment Date",
        thMethod: "Method",
        
        thTicket: "Issue / Repair Ticket",
        thPriority: "Priority",
        thOpenDate: "Opened Date",
        thCost: "Estimated Cost",
        
        modalTitle: "Register New Residential Property",
        modalSubtitle: "Enter property details and landlord info.",
        lblPropTitle: "Property Title *",
        lblType: "Property Type *",
        lblAddress: "Full Address *",
        lblRentVal: "Monthly Rent (€) *",
        lblTypology: "Layout (e.g., T2, T3) *",
        lblOwner: "Landlord Name *",
        btnSubmitProp: "Save Property"
    },
    es: {
        titleProperty: "Gestor de Propiedades Inmobiliarias",
        subtitleProperty: "Administración de inmuebles residenciales, inquilinos, cobro de alquileres e incidencias.",
        btnNewProperty: "Registrar Nueva Propiedad",
        
        kpiTotalProp: "Total Propiedades",
        kpiMonthlyRevenue: "Renta Mensual Total",
        kpiOccupancy: "Tasa de Ocupación",
        kpiIncidents: "Incidencias Abiertas",
        kpiTenants: "Inquilinos Activos",
        
        secProperties: "Catálogo de Inmuebles Residenciales",
        secTenants: "Directorio de Inquilinos",
        secPayments: "Historial de Pago de Alquileres",
        secIncidents: "Gestión de Mantenimiento e Incidencias",
        
        thTenant: "Inquilino",
        thUnit: "Inmueble Alquilado",
        thContact: "Contacto / Correo",
        thRent: "Alquiler Mensual",
        thStartDate: "Contrato Desde",
        thStatus: "Estado de Pago",
        
        thProperty: "Propiedad",
        thAmount: "Monto Alquiler",
        thRefMonth: "Mes Referencia",
        thPayDate: "Fecha Pago",
        thMethod: "Método",
        
        thTicket: "Incidencia / Avería",
        thPriority: "Prioridad",
        thOpenDate: "Fecha Apertura",
        thCost: "Costo Estimado",
        
        modalTitle: "Registrar Nueva Propiedad Residencial",
        modalSubtitle: "Introduzca los detalles del inmueble y del propietario.",
        lblPropTitle: "Título del Inmueble *",
        lblType: "Tipo de Inmueble *",
        lblAddress: "Dirección Completa *",
        lblRentVal: "Valor Alquiler (€/mes) *",
        lblTypology: "Tipología (Ej: T2, T3) *",
        lblOwner: "Propietario *",
        btnSubmitProp: "Guardar Inmueble"
    },
    fr: {
        titleProperty: "Gestionnaire Immobilière SaaS",
        subtitleProperty: "Gestion des propriétés résidentielles, locataires, loyers et tickets de maintenance.",
        btnNewProperty: "Enregistrer un Bien",
        
        kpiTotalProp: "Total Propriétés",
        kpiMonthlyRevenue: "Loyer Mensuel Total",
        kpiOccupancy: "Taux d'Occupation",
        kpiIncidents: "Incidents Ouverts",
        kpiTenants: "Locataires Actifs",
        
        secProperties: "Catalogue des Biens Immobiliers",
        secTenants: "Répertoire des Locataires",
        secPayments: "Historique de Paiement des Loyers",
        secIncidents: "Maintenance & Réparations",
        
        thTenant: "Locataire",
        thUnit: "Bien Loué",
        thContact: "Contact / Email",
        thRent: "Loyer Mensuel",
        thStartDate: "Bail Depuis",
        thStatus: "Statut Paiement",
        
        thProperty: "Propriété",
        thAmount: "Montant Loyer",
        thRefMonth: "Mois de Référence",
        thPayDate: "Date de Paiement",
        thMethod: "Méthode",
        
        thTicket: "Panne / Incident",
        thPriority: "Priorité",
        thOpenDate: "Date d'Ouverture",
        thCost: "Coût Estimé",
        
        modalTitle: "Enregistrer um Bien Résidentiel",
        modalSubtitle: "Saisissez les informations du bien et du propriétaire.",
        lblPropTitle: "Titre du Bien *",
        lblType: "Type de Bien *",
        lblAddress: "Adresse Complète *",
        lblRentVal: "Loyer (€/mois) *",
        lblTypology: "Typologie (Ex: T2, T3) *",
        lblOwner: "Propriétaire *",
        btnSubmitProp: "Enregistrer le Bien"
    }
};

let currentLang = 'pt';
let rawPropiedadesData = [];
let rawInquilinosData = [];
let rawPagosData = [];
let rawIncidenciasData = [];

// Gallery Modal Active State
let currentGalleryProperty = null;
let currentGalleryIndex = 0;

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchPropiedades();
    fetchInquilinos();
    fetchPagos();
    fetchIncidencias();
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
    
    renderPropiedades();
    renderInquilinos();
    renderPagos();
    renderIncidencias();
}

function fetchStats() {
    fetch('/api/stats?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiTotalPropVal').innerText = data.total_propriedades;
            document.getElementById('kpiMonthlyRevVal').innerText = data.renda_total;
            document.getElementById('kpiOccupancyVal').innerText = data.taxa_ocupacao;
            document.getElementById('kpiIncidentsVal').innerText = data.incidencias_abertas;
            document.getElementById('kpiTenantsVal').innerText = data.total_inquilinos;
        });
}

function fetchPropiedades() {
    fetch('/api/propiedades?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawPropiedadesData = data;
            renderPropiedades();
        });
}

function fetchInquilinos() {
    fetch('/api/inquilinos?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawInquilinosData = data;
            renderInquilinos();
        });
}

function fetchPagos() {
    fetch('/api/pagos?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawPagosData = data;
            renderPagos();
        });
}

function fetchIncidencias() {
    fetch('/api/incidencias?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawIncidenciasData = data;
            renderIncidencias();
        });
}

function renderPropiedades() {
    const grid = document.getElementById('propertiesGridContainer');
    if (!grid) return;
    grid.innerHTML = '';
    
    rawPropiedadesData.forEach(p => {
        let badgeClass = 'status-alugado';
        if (p.estado === 'Disponível') badgeClass = 'status-disponivel';
        if (p.estado === 'Em Manutenção') badgeClass = 'status-manutencao';
        
        const card = document.createElement('div');
        card.className = 'property-card';
        card.onclick = () => openGalleryModal(p.id);
        
        card.innerHTML = `
            <div class="property-img-container">
                <img src="${p.foto}" alt="${p.titulo}" class="property-img">
                <span class="property-badge ${badgeClass}">${p.estado}</span>
                <button class="btn-open-gallery"><i class="fa-solid fa-images"></i> Ver Galeria</button>
            </div>
            <div class="property-body">
                <h3 class="property-title">${p.titulo}</h3>
                <p class="property-address"><i class="fa-solid fa-location-dot" style="color: var(--purple-primary);"></i> ${p.morada}</p>
                
                <div class="property-features">
                    <i class="fa-solid fa-house"></i> ${p.tipologia}
                </div>
                
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700; margin-bottom: 12px;">
                    Proprietário: <strong>${p.proprietario}</strong>
                </div>
                
                <div class="property-footer">
                    <div style="font-size: 11px; color: var(--text-subtle); text-transform: uppercase;">Renda Mensal</div>
                    <div class="property-price">${p.renda} € <span style="font-size: 11px; color: var(--text-subtle);">/mês</span></div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderInquilinos() {
    const grid = document.getElementById('tenantGridContainer');
    if (!grid) return;
    grid.innerHTML = '';
    
    rawInquilinosData.forEach(inq => {
        const card = document.createElement('div');
        card.className = 'tenant-card';
        
        card.innerHTML = `
            <div class="tenant-avatar-container">
                <img src="${inq.foto}" alt="${inq.nome}" class="tenant-avatar">
            </div>
            <div style="flex-grow: 1;">
                <h4 style="font-family: var(--font-heading); font-size: 17px; font-weight: 900; color: var(--slate-black);">${inq.nome}</h4>
                <div style="font-size: 12px; font-weight: 800; color: var(--purple-primary); margin-top: 2px;">${inq.unidade}</div>
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700; margin-top: 4px;">
                    <i class="fa-solid fa-phone"></i> ${inq.contacto}
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderPagos() {
    const tbody = document.getElementById('pagosTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawPagosData.forEach(pag => {
        let badgeStyle = 'background: var(--accent-green-light); color: var(--accent-green);';
        if (pag.estado === 'Pendente') badgeStyle = 'background: var(--accent-amber-light); color: var(--accent-amber);';
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span style="font-size: 12px; font-weight: 900; color: var(--purple-primary);">${pag.id}</span></td>
            <td style="font-weight: 900;">${pag.inquilino}</td>
            <td><span style="font-size: 13px; font-weight: 800; color: var(--text-muted);">${pag.propriedade}</span></td>
            <td><span style="font-weight: 900; font-size: 15px; color: var(--purple-dark);">${pag.valor}</span></td>
            <td>${pag.mes_referencia}</td>
            <td>${pag.data_pago}</td>
            <td><span style="font-size: 12px; font-weight: 800;">${pag.metodo}</span></td>
            <td><span style="padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: 900; ${badgeStyle}">${pag.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderIncidencias() {
    const tbody = document.getElementById('incidenciasTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawIncidenciasData.forEach(inc => {
        let badgePrio = 'background: var(--accent-red-light); color: var(--accent-red);';
        if (inc.prioridade === 'Média') badgePrio = 'background: var(--accent-amber-light); color: var(--accent-amber);';
        if (inc.prioridade === 'Baixa') badgePrio = 'background: var(--purple-light); color: var(--purple-dark);';
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span style="font-size: 12px; font-weight: 900; color: var(--text-subtle);">${inc.id}</span></td>
            <td style="font-weight: 900;">${inc.propriedade}</td>
            <td>
                <div style="font-weight: 800; font-size: 13px;">${inc.descricao}</div>
                <div style="font-size: 11px; color: var(--text-subtle);">${inc.inquilino}</div>
            </td>
            <td><span style="padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 900; ${badgePrio}">${inc.prioridade}</span></td>
            <td>${inc.data_abertura}</td>
            <td><span style="font-weight: 900;">${inc.custo_estimado}</span></td>
            <td><span style="padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: 900; background: var(--purple-primary); color: #ffffff;">${inc.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// PHOTO GALLERY MODAL ENGINE
function openGalleryModal(propId) {
    const prop = rawPropiedadesData.find(p => p.id === propId);
    if (!prop) return;
    
    currentGalleryProperty = prop;
    currentGalleryIndex = 0;
    
    document.getElementById('galleryTitle').innerText = prop.titulo;
    document.getElementById('galleryAddress').innerText = prop.morada + ' • ' + prop.tipologia;
    
    updateGalleryViewer();
    document.getElementById('galleryModal').classList.add('active');
}

function closeGalleryModal() {
    document.getElementById('galleryModal').classList.remove('active');
}

function updateGalleryViewer() {
    if (!currentGalleryProperty || !currentGalleryProperty.galeria) return;
    
    const item = currentGalleryProperty.galeria[currentGalleryIndex];
    const mainImg = document.getElementById('galleryMainImg');
    const caption = document.getElementById('galleryCaption');
    const thumbsContainer = document.getElementById('galleryThumbsContainer');
    
    mainImg.src = item.url;
    caption.innerText = item.legenda || `Foto ${currentGalleryIndex + 1}`;
    
    thumbsContainer.innerHTML = '';
    currentGalleryProperty.galeria.forEach((g, idx) => {
        const thumb = document.createElement('div');
        thumb.className = `gallery-thumb ${idx === currentGalleryIndex ? 'active' : ''}`;
        thumb.onclick = () => {
            currentGalleryIndex = idx;
            updateGalleryViewer();
        };
        thumb.innerHTML = `<img src="${g.url}" alt="${g.legenda}">`;
        thumbsContainer.appendChild(thumb);
    });
}

function prevGalleryImage() {
    if (!currentGalleryProperty) return;
    const total = currentGalleryProperty.galeria.length;
    currentGalleryIndex = (currentGalleryIndex - 1 + total) % total;
    updateGalleryViewer();
}

function nextGalleryImage() {
    if (!currentGalleryProperty) return;
    const total = currentGalleryProperty.galeria.length;
    currentGalleryIndex = (currentGalleryIndex + 1) % total;
    updateGalleryViewer();
}

// Modal Form Controller
function openNewPropertyModal() {
    document.getElementById('newPropertyModal').classList.add('active');
}

function closeNewPropertyModal() {
    document.getElementById('newPropertyModal').classList.remove('active');
}

function submitNewPropertyForm(event) {
    event.preventDefault();
    
    const newPropData = {
        titulo: document.getElementById('propTitleInput').value.trim(),
        tipo: document.getElementById('propTypeSelect').value,
        morada: document.getElementById('propAddressInput').value.trim(),
        renda: document.getElementById('propRentInput').value.trim(),
        tipologia: document.getElementById('propTypologyInput').value.trim(),
        proprietario: document.getElementById('propOwnerInput').value.trim()
    };
    
    fetch('/api/propiedades/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPropData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewPropertyModal();
            fetchPropiedades();
            fetchStats();
        }
    });
}
