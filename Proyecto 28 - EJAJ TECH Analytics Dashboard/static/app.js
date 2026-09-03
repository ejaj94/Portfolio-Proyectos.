/* EJAJ TECH ANALYTICS DASHBOARD — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleDashboard: "Painel Analítico de Desempenho",
        subtitleDashboard: "Plataforma de inteligência empresarial EJAJ TECH — Software • Web • Apps Development",
        
        kpiRevenue: "Faturação Total (YTD)",
        kpiMrr: "MRR (Receita Recorrente)",
        kpiProfit: "Lucro Líquido Operacional",
        kpiClients: "Clientes Ativos",
        
        chartRevenueTitle: "Evolução Mensal de Faturação vs Custos",
        chartBusinessTitle: "Distribuição por Unidade de Negócio",
        chartLeadsTitle: "Leads Convertidos vs Projetos Concluídos",
        
        tableHeaderTitle: "Projetos Tecnológicos Recentes & Estado",
        thProject: "Projeto & Unidade",
        thClient: "Cliente",
        thValue: "Valor (€)",
        thProgress: "Progresso",
        thStatus: "Estado"
    },
    en: {
        titleDashboard: "Executive Performance Analytics",
        subtitleDashboard: "EJAJ TECH Business Intelligence Platform — Software • Web • Apps Development",
        
        kpiRevenue: "Total Revenue (YTD)",
        kpiMrr: "MRR (Monthly Recurring)",
        kpiProfit: "Net Operating Profit",
        kpiClients: "Active Enterprise Clients",
        
        chartRevenueTitle: "Monthly Revenue vs Operating Costs",
        chartBusinessTitle: "Revenue by Business Unit",
        chartLeadsTitle: "Converted Leads vs Delivered Projects",
        
        tableHeaderTitle: "Recent Software Projects & Delivery Status",
        thProject: "Project & Unit",
        thClient: "Client",
        thValue: "Value (€)",
        thProgress: "Progress",
        thStatus: "Status"
    },
    es: {
        titleDashboard: "Panel Analítico de Rendimiento",
        subtitleDashboard: "Plataforma de inteligencia empresarial EJAJ TECH — Software • Web • Apps Development",
        
        kpiRevenue: "Facturación Total (YTD)",
        kpiMrr: "MRR (Ingreso Recurrente)",
        kpiProfit: "Beneficio Neto Operativo",
        kpiClients: "Clientes Activos",
        
        chartRevenueTitle: "Evolución Mensual de Facturación vs Costes",
        chartBusinessTitle: "Distribución por Unidad de Negocio",
        chartLeadsTitle: "Leads Convertidos vs Proyectos Concluidos",
        
        tableHeaderTitle: "Proyectos Tecnológicos Recientes y Estado",
        thProject: "Proyecto y Unidad",
        thClient: "Cliente",
        thValue: "Valor (€)",
        thProgress: "Progreso",
        thStatus: "Estado"
    },
    fr: {
        titleDashboard: "Tableau de Bord Analytique",
        subtitleDashboard: "Plateforme d'intelligence d'entreprise EJAJ TECH — Software • Web • Apps Development",
        
        kpiRevenue: "Chiffre d'Affaires Total",
        kpiMrr: "MRR (Revenu Récurrent)",
        kpiProfit: "Bénéfice Net Opérationnel",
        kpiClients: "Clients Actifs",
        
        chartRevenueTitle: "Évolution Mensuelle Revenus vs Coûts",
        chartBusinessTitle: "Répartition par Unité d'Affaires",
        chartLeadsTitle: "Leads Convertis vs Projets Livrés",
        
        tableHeaderTitle: "Projets Récents & Statut de Livraison",
        thProject: "Projet & Unité",
        thClient: "Client",
        thValue: "Valeur (€)",
        thProgress: "Progression",
        thStatus: "Statut"
    }
};

let currentLang = 'pt';
let lineChart = null;
let doughnutChart = null;
let barChart = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchAnalytics();
    fetchChartsData();
    fetchProjetos();
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
            elem.innerText = dict[key];
        }
    });
}

function fetchAnalytics() {
    fetch('/api/analytics')
        .then(res => res.json())
        .then(data => {
            const formattedRevenue = data.faturacao_total.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
            const formattedMrr = data.mrr.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
            const formattedProfit = data.lucro_liquido.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
            
            document.getElementById('kpiRevenueVal').innerText = formattedRevenue;
            document.getElementById('kpiMrrVal').innerText = formattedMrr;
            document.getElementById('kpiProfitVal').innerText = formattedProfit;
            document.getElementById('kpiClientsVal').innerText = data.clientes_ativos;
            
            document.getElementById('badgeYoY').innerText = data.comparativa_yoy;
            document.getElementById('badgeMoM').innerText = data.comparativa_mom;
        });
}

function fetchChartsData() {
    fetch('/api/graficos')
        .then(res => res.json())
        .then(data => {
            renderLineChart(data);
            renderDoughnutChart(data.unidades_negocio);
            renderBarChart(data);
        });
}

function renderLineChart(data) {
    const ctx = document.getElementById('revenueLineChart').getContext('2d');
    if (lineChart) lineChart.destroy();
    
    const gradientRev = ctx.createLinearGradient(0, 0, 0, 300);
    gradientRev.addColorStop(0, 'rgba(217, 70, 239, 0.4)');
    gradientRev.addColorStop(1, 'rgba(217, 70, 239, 0.0)');

    const gradientCost = ctx.createLinearGradient(0, 0, 0, 300);
    gradientCost.addColorStop(0, 'rgba(6, 182, 212, 0.4)');
    gradientCost.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

    lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.meses,
            datasets: [
                {
                    label: 'Faturação (€)',
                    data: data.receita,
                    borderColor: '#d946ef',
                    borderWidth: 3,
                    backgroundColor: gradientRev,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: '#d946ef'
                },
                {
                    label: 'Custos (€)',
                    data: data.custos,
                    borderColor: '#06b6d4',
                    borderWidth: 3,
                    backgroundColor: gradientCost,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#06b6d4'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#cbd5e1', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
            },
            scales: {
                x: { grid: { color: 'rgba(217, 70, 239, 0.1)' }, ticks: { color: '#cbd5e1' } },
                y: { grid: { color: 'rgba(217, 70, 239, 0.1)' }, ticks: { color: '#cbd5e1' } }
            }
        }
    });
}

function renderDoughnutChart(unidades) {
    const ctx = document.getElementById('businessDoughnutChart').getContext('2d');
    if (doughnutChart) doughnutChart.destroy();

    doughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: unidades.labels,
            datasets: [{
                data: unidades.valores,
                backgroundColor: ['#d946ef', '#a855f7', '#06b6d4'],
                borderColor: '#0b061a',
                borderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
            }
        }
    });
}

function renderBarChart(data) {
    const ctx = document.getElementById('leadsBarChart').getContext('2d');
    if (barChart) barChart.destroy();

    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.meses,
            datasets: [
                {
                    label: 'Leads Convertidos',
                    data: data.leads_vs_projetos.leads,
                    backgroundColor: '#a855f7',
                    borderRadius: 8
                },
                {
                    label: 'Projetos Entregues',
                    data: data.leads_vs_projetos.projetos,
                    backgroundColor: '#10b981',
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#cbd5e1', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#cbd5e1' } },
                y: { grid: { color: 'rgba(217, 70, 239, 0.1)' }, ticks: { color: '#cbd5e1' } }
            }
        }
    });
}

function fetchProjetos() {
    fetch('/api/projetos')
        .then(res => res.json())
        .then(projetos => {
            renderProjetosTable(projetos);
        });
}

function renderProjetosTable(projetos) {
    const tbody = document.getElementById('projetosTableBody');
    tbody.innerHTML = '';

    projetos.forEach(p => {
        const formattedVal = p.valor.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
        const tr = document.createElement('tr');
        
        tr.innerHTML = `
            <td>
                <div style="font-weight: 900; font-size: 15px; color: var(--text-white);">${p.nome}</div>
                <div style="font-size: 11px; color: var(--neon-magenta); font-weight: 800;">${p.categoria}</div>
            </td>
            <td style="font-weight: 700; color: var(--text-muted);">${p.cliente}</td>
            <td style="font-weight: 900; color: var(--electric-cyan);">${formattedVal}</td>
            <td style="width: 180px;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; font-weight: 800;">
                    <span>Progresso</span>
                    <span>${p.progresso}%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: ${p.progresso}%;"></div>
                </div>
            </td>
            <td>
                <span style="font-size: 11px; font-weight: 900; background: ${p.progresso === 100 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)'}; color: ${p.progresso === 100 ? '#10b981' : '#f59e0b'}; padding: 4px 12px; border-radius: 12px;">
                    ${p.estado}
                </span>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
