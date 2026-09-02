/* CRM DE VENTAS & GESTÃO DE LEADS SAAS — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleCRM: "Funil de Vendas & CRM de Leads",
        subtitleCRM: "Gestão completa do ciclo comercial: Lead → Contacto → Negociação → Cliente Ganho.",
        btnNewLead: "Nova Oportunidade",
        
        kpiPipeline: "Valor em Pipeline",
        kpiWon: "Receita Fechada (Ganhos)",
        kpiDeals: "Leads Totais",
        kpiConversion: "Taxa de Conversão",
        
        colLead: "Leads (Oportunidades)",
        colContact: "Contactados",
        colNegotiation: "Em Negociação",
        colWon: "Clientes Fechados",
        
        btnAdvance: "Avançar",
        btnNotes: "Notas",
        
        modalTitle: "Criar Nova Oportunidade / Lead",
        modalSubtitle: "Registe os dados da empresa e valor estimado do negócio.",
        lblCompany: "Nome da Empresa *",
        lblContactPerson: "Pessoa de Contacto *",
        lblEmail: "E-mail de Contacto *",
        lblPhone: "Telemóvel / WhatsApp *",
        lblValue: "Valor Estimado (€) *",
        lblSource: "Origem do Lead",
        btnSubmitLead: "Guardar no CRM",
        
        drawerTitle: "Histórico & Notas de Acompanhamento",
        btnAddNote: "Adicionar Nota",
        notePlaceholder: "Escreva uma nota de reunião ou telefonema..."
    },
    en: {
        titleCRM: "Sales Funnel & Lead CRM",
        subtitleCRM: "Complete sales cycle management: Lead → Contact → Negotiation → Won Client.",
        btnNewLead: "New Lead",
        
        kpiPipeline: "Pipeline Value",
        kpiWon: "Won Revenue",
        kpiDeals: "Total Leads",
        kpiConversion: "Conversion Rate",
        
        colLead: "Leads (Inquiries)",
        colContact: "Contacted",
        colNegotiation: "Negotiation",
        colWon: "Won Clients",
        
        btnAdvance: "Advance",
        btnNotes: "Notes",
        
        modalTitle: "Create New Lead / Deal",
        modalSubtitle: "Enter company details and estimated deal value.",
        lblCompany: "Company Name *",
        lblContactPerson: "Contact Person *",
        lblEmail: "Contact Email *",
        lblPhone: "Phone / WhatsApp *",
        lblValue: "Estimated Value (€) *",
        lblSource: "Lead Source",
        btnSubmitLead: "Save in CRM",
        
        drawerTitle: "Activity Log & Follow-up Notes",
        btnAddNote: "Add Note",
        notePlaceholder: "Type a meeting or call note..."
    },
    es: {
        titleCRM: "Embudos de Ventas & CRM de Leads",
        subtitleCRM: "Gestión completa del ciclo comercial: Lead → Contacto → Negociación → Cliente Ganado.",
        btnNewLead: "Nueva Oportunidad",
        
        kpiPipeline: "Valor de Pipeline",
        kpiWon: "Ingresos Ganados",
        kpiDeals: "Leads Totales",
        kpiConversion: "Tasa de Conversión",
        
        colLead: "Leads (Nuevos)",
        colContact: "Contactados",
        colNegotiation: "En Negociación",
        colWon: "Clientes Ganados",
        
        btnAdvance: "Avanzar",
        btnNotes: "Notas",
        
        modalTitle: "Crear Nueva Oportunidad / Lead",
        modalSubtitle: "Rellene los datos de la empresa y valor estimado del negocio.",
        lblCompany: "Nombre de la Empresa *",
        lblContactPerson: "Persona de Contacto *",
        lblEmail: "Correo Electrónico *",
        lblPhone: "Teléfono / WhatsApp *",
        lblValue: "Valor Estimado (€) *",
        lblSource: "Origen del Lead",
        btnSubmitLead: "Guardar en CRM",
        
        drawerTitle: "Historial y Notas de Seguimiento",
        btnAddNote: "Añadir Nota",
        notePlaceholder: "Escriba una nota de reunión o llamada..."
    },
    fr: {
        titleCRM: "Pipeline de Ventes & CRM Leads",
        subtitleCRM: "Gestion complète du cycle commercial: Lead → Contact → Négociation → Client Gagné.",
        btnNewLead: "Nouveau Lead",
        
        kpiPipeline: "Valeur du Pipeline",
        kpiWon: "Revenus Gagnés",
        kpiDeals: "Leads Totaux",
        kpiConversion: "Taux de Conversion",
        
        colLead: "Leads (Opportunités)",
        colContact: "Contactés",
        colNegotiation: "En Négociation",
        colWon: "Clients Gagnés",
        
        btnAdvance: "Avancer",
        btnNotes: "Notes",
        
        modalTitle: "Créer un Nouveau Lead / Opportunité",
        modalSubtitle: "Saisissez les détails de l'entreprise et la valeur estimée.",
        lblCompany: "Nom de l'Entreprise *",
        lblContactPerson: "Personne de Contact *",
        lblEmail: "E-mail de Contact *",
        lblPhone: "Téléphone / WhatsApp *",
        lblValue: "Valeur Estimée (€) *",
        lblSource: "Source du Lead",
        btnSubmitLead: "Enregistrer dans le CRM",
        
        drawerTitle: "Historique & Notes de Suivi",
        btnAddNote: "Ajouter une Note",
        notePlaceholder: "Rédigez une note de réunion ou d'appel..."
    }
};

let currentLang = 'pt';
let rawLeadsData = [];
let activeDrawerLeadId = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchLeads();
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
            if (elem.tagName === 'INPUT' || elem.tagName === 'TEXTAREA') {
                elem.placeholder = dict[key];
            } else {
                elem.innerText = dict[key];
            }
        }
    });
    
    renderKanbanBoard();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiPipelineVal').innerText = data.pipeline_val;
            document.getElementById('kpiWonVal').innerText = data.ganhos_val;
            document.getElementById('kpiDealsVal').innerText = data.total_leads;
            document.getElementById('kpiConversionVal').innerText = data.taxa_conversao;
        });
}

function fetchLeads() {
    fetch('/api/leads')
        .then(res => res.json())
        .then(data => {
            rawLeadsData = data;
            renderKanbanBoard();
        });
}

function renderKanbanBoard() {
    const colLead = document.getElementById('colLeadContainer');
    const colContact = document.getElementById('colContactContainer');
    const colNegotiation = document.getElementById('colNegotiationContainer');
    const colWon = document.getElementById('colWonContainer');
    
    colLead.innerHTML = '';
    colContact.innerHTML = '';
    colNegotiation.innerHTML = '';
    colWon.innerHTML = '';
    
    let countLead = 0, countContact = 0, countNeg = 0, countWon = 0;
    
    rawLeadsData.forEach(lead => {
        const card = document.createElement('div');
        card.className = 'deal-card';
        
        const formattedVal = lead.valor.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
        const dict = i18n[currentLang];
        
        card.innerHTML = `
            <div class="deal-company">${lead.empresa}</div>
            <div class="deal-contact"><i class="fa-solid fa-user-tie"></i> ${lead.contacto}</div>
            <div style="font-size: 11px; color: var(--text-subtle); margin-bottom: 8px;"><i class="fa-solid fa-phone"></i> ${lead.telefone}</div>
            <div class="deal-value">${formattedVal}</div>
            
            <div class="deal-footer">
                <button class="btn-notes-icon" onclick="openNotesDrawer('${lead.id}')" title="Ver Notas">
                    <i class="fa-solid fa-comment-dots"></i> ${lead.notas.length}
                </button>
                
                ${lead.estagio !== 'cliente' ? `
                    <button class="btn-advance-stage" onclick="advanceLeadStage('${lead.id}')">
                        <span>${dict.btnAdvance || 'Avançar'}</span> <i class="fa-solid fa-arrow-right"></i>
                    </button>
                ` : `<span style="font-size: 11px; font-weight: 900; color: var(--stage-cliente);"><i class="fa-solid fa-circle-check"></i> Cliente Ganho</span>`}
            </div>
        `;
        
        if (lead.estagio === 'lead') {
            colLead.appendChild(card);
            countLead++;
        } else if (lead.estagio === 'contacto') {
            colContact.appendChild(card);
            countContact++;
        } else if (lead.estagio === 'negociacao') {
            colNegotiation.appendChild(card);
            countNeg++;
        } else if (lead.estagio === 'cliente') {
            colWon.appendChild(card);
            countWon++;
        }
    });
    
    document.getElementById('countLead').innerText = countLead;
    document.getElementById('countContact').innerText = countContact;
    document.getElementById('countNegotiation').innerText = countNeg;
    document.getElementById('countWon').innerText = countWon;
}

// THE HOOK: Advance Lead through the sales funnel stages
function advanceLeadStage(leadId) {
    fetch(`/api/leads/advance/${leadId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                fetchLeads();
                fetchStats();
            }
        });
}

// Notes Drawer Controller
function openNotesDrawer(leadId) {
    activeDrawerLeadId = leadId;
    const lead = rawLeadsData.find(l => l.id === leadId);
    if (!lead) return;
    
    document.getElementById('drawerLeadTitle').innerText = lead.empresa;
    document.getElementById('drawerLeadContact').innerText = `${lead.contacto} (${lead.email})`;
    
    renderNotesList(lead.notas);
    document.getElementById('notesDrawerBackdrop').classList.add('active');
}

function closeNotesDrawer() {
    document.getElementById('notesDrawerBackdrop').classList.remove('active');
    activeDrawerLeadId = null;
}

function renderNotesList(notas) {
    const wrapper = document.getElementById('drawerNotesList');
    wrapper.innerHTML = '';
    
    if (!notas || notas.length === 0) {
        wrapper.innerHTML = `<div style="font-size: 12px; color: var(--text-subtle); text-align: center; padding: 20px;">Nenhuma nota registada.</div>`;
        return;
    }
    
    notas.slice().reverse().forEach(n => {
        const item = document.createElement('div');
        item.className = 'note-item-box';
        item.innerHTML = `
            <div class="note-date"><i class="fa-regular fa-clock"></i> ${n.data}</div>
            <div class="note-text">${n.texto}</div>
        `;
        wrapper.appendChild(item);
    });
}

function submitNewNote(event) {
    event.preventDefault();
    if (!activeDrawerLeadId) return;
    
    const input = document.getElementById('newNoteInput');
    const texto = input.value.trim();
    if (!texto) return;
    
    fetch(`/api/leads/notes/${activeDrawerLeadId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: texto })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            input.value = '';
            fetchLeads();
            renderNotesList(data.lead.notas);
        }
    });
}

// Modal Controller
function openNewLeadModal() {
    document.getElementById('newLeadModal').classList.add('active');
}

function closeNewLeadModal() {
    document.getElementById('newLeadModal').classList.remove('active');
}

function submitNewLeadForm(event) {
    event.preventDefault();
    
    const newLeadData = {
        empresa: document.getElementById('leadCompany').value.trim(),
        contacto: document.getElementById('leadContact').value.trim(),
        email: document.getElementById('leadEmail').value.trim(),
        telefone: document.getElementById('leadPhone').value.trim(),
        valor: parseFloat(document.getElementById('leadValue').value) || 10000,
        origem: document.getElementById('leadSource').value
    };
    
    fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newLeadData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewLeadModal();
            fetchLeads();
            fetchStats();
        }
    });
}
