/* LUXURY VETERINARY EXPENSE MANAGER — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleVet: "Gestão Financeira & Despesas Veterinárias",
        subtitleVet: "Plataforma de controlo financeiro de alta precisão para clínica e boutique de luxo.",
        btnNewTrx: "Nova Transação",
        
        kpiBalance: "Balanço Líquido (Saldo)",
        kpiIncome: "Total de Receitas",
        kpiExpense: "Total de Despesas",
        kpiMargin: "Margem Operacional",
        
        chartLineTitle: "Evolução Financeira: Receitas vs Despesas",
        chartDoughnutTitle: "Distribuição de Gastos por Categoria",
        
        tableHeaderTitle: "Histórico Auditável de Transações Financeiras",
        tableSearchPlaceholder: "Pesquisar por descrição, paciente ou categoria...",
        filterAll: "Todas",
        filterIncome: "Receitas",
        filterExpense: "Despesas",
        
        thType: "Tipo",
        thDesc: "Descrição & Paciente",
        thCategory: "Categoria",
        thDate: "Data",
        thMethod: "Método",
        thAmount: "Montante (€)",
        
        modalTitle: "Registar Transação Financeira",
        modalSubtitle: "Introduza os detalhes do movimento financeiro.",
        lblType: "Tipo de Transação *",
        lblDesc: "Descrição do Serviço ou Despesa *",
        lblCategory: "Categoria *",
        lblAmount: "Montante (€) *",
        lblMethod: "Método de Pagamento *",
        lblNotes: "Notas / Paciente",
        btnSubmitTrx: "Guardar no Sistema Financeiro"
    },
    en: {
        titleVet: "Luxury Vet Financial & Expense Manager",
        subtitleVet: "High-precision financial control suite for luxury veterinary clinics and pet spas.",
        btnNewTrx: "New Transaction",
        
        kpiBalance: "Net Financial Balance",
        kpiIncome: "Total Revenue",
        kpiExpense: "Total Expenses",
        kpiMargin: "Operating Margin",
        
        chartLineTitle: "Financial Trend: Revenue vs Expenses",
        chartDoughnutTitle: "Expenses Breakdown by Category",
        
        tableHeaderTitle: "Audited Financial Transaction Ledger",
        tableSearchPlaceholder: "Search description, patient or category...",
        filterAll: "All",
        filterIncome: "Revenues",
        filterExpense: "Expenses",
        
        thType: "Type",
        thDesc: "Description & Patient",
        thCategory: "Category",
        thDate: "Date",
        thMethod: "Payment Method",
        thAmount: "Amount (€)",
        
        modalTitle: "Register Financial Transaction",
        modalSubtitle: "Enter income or expense details.",
        lblType: "Transaction Type *",
        lblDesc: "Description *",
        lblCategory: "Category *",
        lblAmount: "Amount (€) *",
        lblMethod: "Payment Method *",
        lblNotes: "Notes / Patient",
        btnSubmitTrx: "Save in Financial System"
    },
    es: {
        titleVet: "Gestión Financiera & Gastos Veterinarios",
        subtitleVet: "Plataforma de control financiero de alta precisión para clínica y boutique de lujo.",
        btnNewTrx: "Nueva Transacción",
        
        kpiBalance: "Balance Neto (Saldo)",
        kpiIncome: "Total de Ingresos",
        kpiExpense: "Total de Gastos",
        kpiMargin: "Margen Operativo",
        
        chartLineTitle: "Evolución Financiera: Ingresos vs Gastos",
        chartDoughnutTitle: "Distribución de Gastos por Categoría",
        
        tableHeaderTitle: "Historial Auditado de Transacciones Financieras",
        tableSearchPlaceholder: "Buscar por descripción, paciente o categoría...",
        filterAll: "Todas",
        filterIncome: "Ingresos",
        filterExpense: "Gastos",
        
        thType: "Tipo",
        thDesc: "Descripción & Paciente",
        thCategory: "Categoría",
        thDate: "Fecha",
        thMethod: "Método",
        thAmount: "Monto (€)",
        
        modalTitle: "Registrar Transacción Financiera",
        modalSubtitle: "Rellene los detalles del movimiento financiero.",
        lblType: "Tipo de Transacción *",
        lblDesc: "Descripción *",
        lblCategory: "Categoría *",
        lblAmount: "Monto (€) *",
        lblMethod: "Método de Pago *",
        lblNotes: "Notas / Paciente",
        btnSubmitTrx: "Guardar en Sistema Financiero"
    },
    fr: {
        titleVet: "Gestion Financière & Dépenses Vétérinaires",
        subtitleVet: "Suite de contrôle financier pour clinique et spa vétérinaire de luxe.",
        btnNewTrx: "Nouvelle Transaction",
        
        kpiBalance: "Solde Financier Net",
        kpiIncome: "Revenus Totaux",
        kpiExpense: "Dépenses Totales",
        kpiMargin: "Marge Opérationnelle",
        
        chartLineTitle: "Évolution Financière: Revenus vs Dépenses",
        chartDoughnutTitle: "Répartition des Dépenses par Catégorie",
        
        tableHeaderTitle: "Registre des Transactions Financières",
        tableSearchPlaceholder: "Rechercher par description, patient ou catégorie...",
        filterAll: "Toutes",
        filterIncome: "Revenus",
        filterExpense: "Dépenses",
        
        thType: "Type",
        thDesc: "Description & Patient",
        thCategory: "Catégorie",
        thDate: "Date",
        thMethod: "Méthode",
        thAmount: "Montant (€)",
        
        modalTitle: "Enregistrer une Transaction",
        modalSubtitle: "Saisissez les détails du mouvement financier.",
        lblType: "Type de Transaction *",
        lblDesc: "Description *",
        lblCategory: "Catégorie *",
        lblAmount: "Montant (€) *",
        lblMethod: "Méthode de Paiement *",
        lblNotes: "Notes / Patient",
        btnSubmitTrx: "Enregistrer dans le Système"
    }
};

let currentLang = 'pt';
let rawTransacoesData = [];
let activeFilter = 'all';
let lineChart = null;
let doughnutChart = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchChartsData();
    fetchTransacoes();
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
    
    renderTransacoesTable();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiBalanceVal').innerText = data.balance_liquido;
            document.getElementById('kpiIncomeVal').innerText = data.total_ingresos;
            document.getElementById('kpiExpenseVal').innerText = data.total_gastos;
            document.getElementById('kpiMarginVal').innerText = data.margem_operacional;
        });
}

function fetchChartsData() {
    fetch('/api/graficos')
        .then(res => res.json())
        .then(data => {
            renderLineChart(data);
            renderDoughnutChart(data.categorias_despesas);
        });
}

function renderLineChart(data) {
    const ctx = document.getElementById('financeLineChart').getContext('2d');
    if (lineChart) lineChart.destroy();
    
    lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.meses,
            datasets: [
                {
                    label: 'Receitas (€)',
                    data: data.receitas,
                    borderColor: '#10b981',
                    borderWidth: 3,
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Despesas (€)',
                    data: data.despesas,
                    borderColor: '#dc2626',
                    borderWidth: 3,
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#022c22', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
            },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: 'rgba(6, 78, 59, 0.1)' } }
            }
        }
    });
}

function renderDoughnutChart(categorias) {
    const ctx = document.getElementById('expenseDoughnutChart').getContext('2d');
    if (doughnutChart) doughnutChart.destroy();

    doughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categorias.labels,
            datasets: [{
                data: categorias.valores,
                backgroundColor: ['#064e3b', '#d4af37', '#e0a96d', '#0284c7', '#dc2626'],
                borderColor: '#ffffff',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#022c22', font: { family: 'Plus Jakarta Sans', weight: 'bold' } } }
            }
        }
    });
}

function fetchTransacoes() {
    fetch('/api/transacoes')
        .then(res => res.json())
        .then(data => {
            rawTransacoesData = data;
            renderTransacoesTable();
        });
}

function setFilter(filterType) {
    activeFilter = filterType;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-filter') === filterType);
    });
    renderTransacoesTable();
}

function renderTransacoesTable() {
    const tbody = document.getElementById('transacoesTableBody');
    const searchVal = document.getElementById('searchBox').value.toLowerCase();
    tbody.innerHTML = '';
    
    const filtered = rawTransacoesData.filter(t => {
        const matchesFilter = activeFilter === 'all' || 
            (activeFilter === 'receita' && t.tipo === 'Receita') ||
            (activeFilter === 'despesa' && t.tipo === 'Despesa');
            
        const matchesSearch = t.descricao.toLowerCase().includes(searchVal) ||
            t.categoria.toLowerCase().includes(searchVal) ||
            t.notas.toLowerCase().includes(searchVal);
            
        return matchesFilter && matchesSearch;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 30px; color: var(--text-subtle);">Nenhuma transação encontrada.</td></tr>`;
        return;
    }

    filtered.forEach(t => {
        const isReceita = t.tipo === 'Receita';
        const badgeClass = isReceita ? 'receita' : 'despesa';
        const sign = isReceita ? '+' : '-';
        const formattedAmount = t.montante.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span class="badge-trx ${badgeClass}">${t.tipo}</span></td>
            <td>
                <div style="font-weight: 800; font-size: 14px;">${t.descricao}</div>
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700;">${t.notas}</div>
            </td>
            <td><span style="font-size: 12px; font-weight: 800; color: var(--emerald-dark);">${t.categoria}</span></td>
            <td>${t.data}</td>
            <td><span style="font-size: 12px; font-weight: 700; color: var(--text-muted);">${t.metodo}</span></td>
            <td style="font-weight: 900; font-size: 15px; color: ${isReceita ? 'var(--accent-emerald)' : 'var(--accent-coral)'};">
                ${sign} ${formattedAmount}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Modal Form Controller
function openNewTrxModal() {
    document.getElementById('newTrxModal').classList.add('active');
}

function closeNewTrxModal() {
    document.getElementById('newTrxModal').classList.remove('active');
}

function submitNewTrxForm(event) {
    event.preventDefault();
    
    const newTrxData = {
        tipo: document.getElementById('trxTypeSelect').value,
        descricao: document.getElementById('trxDescInput').value.trim(),
        categoria: document.getElementById('trxCategorySelect').value,
        montante: parseFloat(document.getElementById('trxAmountInput').value) || 0.0,
        metodo: document.getElementById('trxMethodSelect').value,
        notas: document.getElementById('trxNotesInput').value.trim()
    };
    
    fetch('/api/transacoes/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTrxData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewTrxModal();
            fetchTransacoes();
            fetchStats();
        }
    });
}
