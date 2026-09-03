/* HIGH PERFORMANCE SUPERCAR WORKSHOP — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleWorkshop: "Gestão de Oficina de Alta Performance",
        subtitleWorkshop: "Controlo telemétrico, ordens de serviço e diagnóstico em tempo real para supercarros e exóticos.",
        btnNewOrder: "Nova Ordem de Serviço",
        
        kpiRevenue: "Faturação Total Oficina",
        kpiInRepair: "Supercarros em Oficina",
        kpiCompleted: "Veículos Entregues",
        kpiPower: "Potência Preparada (cv)",
        
        colDiagnostic: "1. Diagnóstico & Telemetria",
        colMaintenance: "2. Manutenção / Tuning",
        colDyno: "3. Ensaio Dyno & Pista",
        colReady: "4. Detalhamento & Pronto",
        
        btnAdvance: "Avançar Fase",
        
        modalTitle: "Registar Nova Ordem de Serviço VIP",
        modalSubtitle: "Preencha a ficha técnica da viatura e orçamento estimado.",
        lblPlate: "Matrícula *",
        lblVin: "Número de Chassi (VIN) *",
        lblVehicleModel: "Marca & Modelo do Supercarro *",
        lblClientName: "Proprietário VIP *",
        lblMechanic: "Mestre Mecânico Responsável *",
        lblService: "Serviços & Modificações *",
        lblBudget: "Orçamento Estimado (€) *",
        lblEstDelivery: "Previsão de Entrega *",
        lblNotes: "Notas de Diagnóstico *",
        btnSubmitOrder: "Guardar Ordem no Sistema"
    },
    en: {
        titleWorkshop: "High-Performance Supercar Workshop",
        subtitleWorkshop: "Telemetry diagnostics, work orders and real-time status tracking for exotic supercars.",
        btnNewOrder: "New Work Order",
        
        kpiRevenue: "Total Workshop Revenue",
        kpiInRepair: "Supercars in Garage",
        kpiCompleted: "Vehicles Delivered",
        kpiPower: "Prepared Power (hp)",
        
        colDiagnostic: "1. Diagnostic & Telemetry",
        colMaintenance: "2. Maintenance / Tuning",
        colDyno: "3. Dyno Test & Track",
        colReady: "4. Detailing & Ready",
        
        btnAdvance: "Advance Stage",
        
        modalTitle: "Register New VIP Work Order",
        modalSubtitle: "Enter technical vehicle spec sheet and estimated budget.",
        lblPlate: "License Plate *",
        lblVin: "Chassis Number (VIN) *",
        lblVehicleModel: "Supercar Make & Model *",
        lblClientName: "VIP Owner *",
        lblMechanic: "Lead Master Technician *",
        lblService: "Services & Tuning *",
        lblBudget: "Estimated Budget (€) *",
        lblEstDelivery: "Estimated Delivery *",
        lblNotes: "Diagnostic Notes *",
        btnSubmitOrder: "Save Order in System"
    },
    es: {
        titleWorkshop: "Gestión de Taller de Alta Performance",
        subtitleWorkshop: "Control telemétrico, órdenes de servicio y diagnóstico en tiempo real para superdeportivos.",
        btnNewOrder: "Nueva Orden de Servicio",
        
        kpiRevenue: "Facturación Total Taller",
        kpiInRepair: "Superdeportivos en Taller",
        kpiCompleted: "Vehículos Entregados",
        kpiPower: "Potencia Preparada (cv)",
        
        colDiagnostic: "1. Diagnóstico y Telemetría",
        colMaintenance: "2. Mantenimiento / Tuning",
        colDyno: "3. Prueba Dyno y Pista",
        colReady: "4. Detallado y Listo",
        
        btnAdvance: "Avanzar Fase",
        
        modalTitle: "Registrar Nueva Orden de Servicio VIP",
        modalSubtitle: "Rellene la ficha técnica del vehículo y presupuesto estimado.",
        lblPlate: "Matrícula *",
        lblVin: "Número de Bastidor (VIN) *",
        lblVehicleModel: "Marca y Modelo del Superdeportivo *",
        lblClientName: "Propietario VIP *",
        lblMechanic: "Maestro Mecánico Responsable *",
        lblService: "Servicios y Modificaciones *",
        lblBudget: "Presupuesto Estimado (€) *",
        lblEstDelivery: "Previsión de Entrega *",
        lblNotes: "Notas de Diagnóstico *",
        btnSubmitOrder: "Guardar Orden en Sistema"
    },
    fr: {
        titleWorkshop: "Atelier Haute Performance Supercars",
        subtitleWorkshop: "Diagnostic télémétrique, ordres de réparation et suivi en temps réel pour supercars.",
        btnNewOrder: "Nouvel Ordre de Service",
        
        kpiRevenue: "Chiffre d'Affaires Atelier",
        kpiInRepair: "Supercars en Atelier",
        kpiCompleted: "Véhicules Livrés",
        kpiPower: "Puissance Préparée (ch)",
        
        colDiagnostic: "1. Diagnostic & Télémétrie",
        colMaintenance: "2. Entretien / Tuning",
        colDyno: "3. Test Dyno & Piste",
        colReady: "4. Detailing & Prêt",
        
        btnAdvance: "Avancer Étape",
        
        modalTitle: "Enregistrer un Ordre de Service VIP",
        modalSubtitle: "Saisissez la fiche technique du véhicule et le devis estimé.",
        lblPlate: "Plaque d'Immatriculation *",
        lblVin: "Numéro de Châssis (VIN) *",
        lblVehicleModel: "Marque & Modèle Supercar *",
        lblClientName: "Propriétaire VIP *",
        lblMechanic: "Maître Technicien *",
        lblService: "Prestations & Tuning *",
        lblBudget: "Devis Estimé (€) *",
        lblEstDelivery: "Date de Livraison *",
        lblNotes: "Notes de Diagnostic *",
        btnSubmitOrder: "Enregistrer l'Ordre"
    }
};

let currentLang = 'pt';
let rawOrdensData = [];
let rawVeiculosData = [];
let dynoBarChart = null;
let servicesDoughnutChart = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchOrdens();
    fetchVeiculos();
    fetchDynoAnalytics();
    
    // Set default delivery date
    const estDelivery = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    document.getElementById('osDeliveryInput').value = estDelivery;
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
    
    renderPipelineBoard();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiRevenueVal').innerText = data.total_faturacao;
            document.getElementById('kpiInRepairVal').innerText = data.em_reparacao;
            document.getElementById('kpiCompletedVal').innerText = data.concluidos;
            document.getElementById('kpiPowerVal').innerText = data.potencia_preparada;
        });
}

function fetchOrdens() {
    fetch('/api/ordens')
        .then(res => res.json())
        .then(data => {
            rawOrdensData = data;
            renderPipelineBoard();
        });
}

function fetchVeiculos() {
    fetch('/api/veiculos')
        .then(res => res.json())
        .then(data => {
            rawVeiculosData = data;
            renderGarageTable();
        });
}

function fetchDynoAnalytics() {
    fetch('/api/dyno')
        .then(res => res.json())
        .then(data => {
            renderDynoBarChart(data);
            renderServicesDoughnutChart(data.servicos_distribuicao);
        });
}

function renderGarageTable() {
    const tbody = document.getElementById('garageTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawVeiculosData.forEach(v => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span style="font-size: 12px; font-weight: 900; background: var(--bg-hover); padding: 4px 8px; border-radius: 6px;">${v.matricula}</span></td>
            <td style="font-weight: 900; font-size: 14px;">${v.marca_modelo}</td>
            <td><span class="vin-tag" style="margin: 0;"><i class="fa-solid fa-barcode"></i> ${v.vin}</span></td>
            <td><span style="font-weight: 900; color: var(--dyno-yellow);">${v.potencia}</span></td>
            <td><span style="font-weight: 800;">${v.proprietario}</span></td>
            <td><span style="font-size: 12px; color: var(--metallic-silver);">${v.contacto}</span></td>
            <td><span style="font-size: 11px; font-weight: 900; color: var(--racing-red); background: var(--racing-red-light); padding: 4px 10px; border-radius: 12px;">${v.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderDynoBarChart(data) {
    const ctx = document.getElementById('dynoPowerChart');
    if (!ctx) return;
    if (dynoBarChart) dynoBarChart.destroy();
    
    dynoBarChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: data.modelos,
            datasets: [
                {
                    label: 'Potência Stock (cv)',
                    data: data.potencia_stock,
                    backgroundColor: 'rgba(148, 163, 184, 0.4)',
                    borderColor: '#94a3b8',
                    borderWidth: 1,
                    borderRadius: 6
                },
                {
                    label: 'Potência Dyno Stage 2 (cv)',
                    data: data.potencia_dyno,
                    backgroundColor: 'rgba(220, 38, 38, 0.85)',
                    borderColor: '#dc2626',
                    borderWidth: 1,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#ffffff', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#cbd5e1' } },
                y: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#cbd5e1' } }
            }
        }
    });
}

function renderServicesDoughnutChart(servicos) {
    const ctx = document.getElementById('servicesDoughnutChart');
    if (!ctx) return;
    if (servicesDoughnutChart) servicesDoughnutChart.destroy();

    servicesDoughnutChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: servicos.labels,
            datasets: [{
                data: servicos.valores,
                backgroundColor: ['#dc2626', '#eab308', '#6366f1', '#10b981', '#ec4899'],
                borderColor: '#1f2937',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#ffffff', font: { family: 'Plus Jakarta Sans', weight: 'bold', size: 10 } } }
            }
        }
    });
}

function renderPipelineBoard() {
    const colDiag = document.getElementById('colDiagnosticContainer');
    const colMaint = document.getElementById('colMaintenanceContainer');
    const colDyno = document.getElementById('colDynoContainer');
    const colReady = document.getElementById('colReadyContainer');
    
    if (!colDiag) return;
    colDiag.innerHTML = '';
    colMaint.innerHTML = '';
    colDyno.innerHTML = '';
    colReady.innerHTML = '';
    
    let cDiag = 0, cMaint = 0, cDyno = 0, cReady = 0;
    const searchVal = document.getElementById('searchBox').value.toLowerCase();
    
    rawOrdensData.forEach(os => {
        const matchesSearch = os.veiculo.toLowerCase().includes(searchVal) ||
            os.vin.toLowerCase().includes(searchVal) ||
            os.matricula.toLowerCase().includes(searchVal) ||
            os.cliente.toLowerCase().includes(searchVal);
            
        if (!matchesSearch) return;
        
        const card = document.createElement('div');
        card.className = 'supercar-card';
        
        const formattedBudget = os.orcamento.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
        const dict = i18n[currentLang];
        
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 11px; font-weight: 900; color: var(--racing-red);">${os.id}</span>
                <span style="font-size: 11px; font-weight: 900; color: var(--text-white); background: var(--bg-hover); padding: 2px 8px; border-radius: 6px;">
                    ${os.matricula}
                </span>
            </div>
            
            <div class="supercar-model">${os.veiculo}</div>
            <div class="vin-tag"><i class="fa-solid fa-barcode"></i> ${os.vin}</div>
            
            <div class="supercar-service">${os.servico}</div>
            <div style="font-size: 11px; color: var(--metallic-silver); font-weight: 700; margin-bottom: 8px;">
                <i class="fa-solid fa-user-gear"></i> ${os.mecanico_chefe}
            </div>
            
            <div class="supercar-budget">${formattedBudget}</div>
            
            <div class="supercar-footer">
                <span style="font-size: 11px; color: var(--text-subtle); font-weight: 700;">
                    <i class="fa-regular fa-clock"></i> ${os.previsao_entrega}
                </span>
                
                ${os.estagio !== 'pronto' ? `
                    <button class="btn-advance-stage" onclick="advanceWorkOrderStage('${os.id}')">
                        <span>${dict.btnAdvance || 'Avançar'}</span> <i class="fa-solid fa-chevron-right"></i>
                    </button>
                ` : `<span style="font-size: 11px; font-weight: 900; color: var(--accent-emerald);"><i class="fa-solid fa-flag-checkered"></i> Entregue</span>`}
            </div>
        `;
        
        if (os.estagio === 'diagnostico') { colDiag.appendChild(card); cDiag++; }
        else if (os.estagio === 'manutencao') { colMaint.appendChild(card); cMaint++; }
        else if (os.estagio === 'dyno') { colDyno.appendChild(card); cDyno++; }
        else if (os.estagio === 'pronto') { colReady.appendChild(card); cReady++; }
    });
    
    document.getElementById('countDiagnostic').innerText = cDiag;
    document.getElementById('countMaintenance').innerText = cMaint;
    document.getElementById('countDyno').innerText = cDyno;
    document.getElementById('countReady').innerText = cReady;
}

function advanceWorkOrderStage(ordemId) {
    fetch(`/api/ordens/avancar/${ordemId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                fetchOrdens();
                fetchVeiculos();
                fetchStats();
            }
        });
}

// Modal Form Controller
function openNewOrderModal() {
    document.getElementById('newOrderModal').classList.add('active');
}

function closeNewOrderModal() {
    document.getElementById('newOrderModal').classList.remove('active');
}

function submitNewOrderForm(event) {
    event.preventDefault();
    
    const newOrderData = {
        matricula: document.getElementById('osPlateInput').value.trim(),
        vin: document.getElementById('osVinInput').value.trim(),
        veiculo: document.getElementById('osVehicleInput').value.trim(),
        cliente: document.getElementById('osClientInput').value.trim(),
        mecanico_chefe: document.getElementById('osMechanicSelect').value,
        servico: document.getElementById('osServiceInput').value.trim(),
        orcamento: parseFloat(document.getElementById('osBudgetInput').value) || 5000.0,
        previsao_entrega: document.getElementById('osDeliveryInput').value,
        diagnostico_notas: document.getElementById('osNotesInput').value.trim()
    };
    
    fetch('/api/ordens/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newOrderData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewOrderModal();
            fetchOrdens();
            fetchVeiculos();
            fetchStats();
        }
    });
}
