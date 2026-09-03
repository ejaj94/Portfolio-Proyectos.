/* SISTEMA DE FACTURAÇÃO PROFISSIONAL SAAS — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleBilling: "Sistema de Facturação & Gestão Financeira",
        subtitleBilling: "Plataforma profissional para emissão de faturas certificadas, gestão de IVA e controlo de clientes.",
        btnNewInvoice: "Emitir Nova Fatura",
        
        kpiRevenue: "Total Faturado",
        kpiPending: "Faturas Pendentes",
        kpiVat: "Impostos Liquidados (IVA)",
        kpiInvoices: "Faturas Emitidas",
        
        tableHeaderTitle: "Histórico Geral de Faturas Certificadas",
        tableSearchPlaceholder: "Pesquisar por NIF, Número de Fatura ou Nome do Cliente...",
        
        thNumber: "Nº Fatura",
        thClient: "Cliente & NIF",
        thDate: "Data Emissão",
        thDueDate: "Vencimento",
        thStatus: "Estado",
        thTotal: "Total (€)",
        thActions: "Ações & PDF",
        
        wizardStep1: "1. Cliente",
        wizardStep2: "2. Artigos & IVA",
        wizardStep3: "3. Resumo Totais",
        wizardStep4: "4. Emitir & PDF",
        
        lblSelectClient: "Selecionar Cliente *",
        lblIssueDate: "Data de Emissão *",
        lblDueDate: "Data de Vencimento *",
        btnAddLine: "Adicionar Linha de Serviço",
        btnGeneratePdf: "Emitir Fatura & Gerar PDF",
        
        modalPdfTitle: "Visualizador de Fatura Certificada PDF"
    },
    en: {
        titleBilling: "Billing & Financial Management System",
        subtitleBilling: "Professional platform for certified invoice issuance, VAT calculation and client management.",
        btnNewInvoice: "Issue New Invoice",
        
        kpiRevenue: "Total Invoiced",
        kpiPending: "Pending Invoices",
        kpiVat: "Total VAT Taxes",
        kpiInvoices: "Invoices Issued",
        
        tableHeaderTitle: "Certified Invoices Directory",
        tableSearchPlaceholder: "Search by VAT/NIF, Invoice Number or Client Name...",
        
        thNumber: "Invoice No.",
        thClient: "Client & Tax ID",
        thDate: "Issue Date",
        thDueDate: "Due Date",
        thStatus: "Status",
        thTotal: "Total (€)",
        thActions: "Actions & PDF",
        
        wizardStep1: "1. Client",
        wizardStep2: "2. Items & VAT",
        wizardStep3: "3. Totals Summary",
        wizardStep4: "4. Issue & PDF",
        
        lblSelectClient: "Select Client *",
        lblIssueDate: "Issue Date *",
        lblDueDate: "Due Date *",
        btnAddLine: "Add Item Row",
        btnGeneratePdf: "Issue Invoice & Download PDF",
        
        modalPdfTitle: "Certified PDF Invoice Viewer"
    },
    es: {
        titleBilling: "Sistema de Facturación & Gestión Financiera",
        subtitleBilling: "Plataforma profesional para emisión de facturas certificadas, IVA y control de clientes.",
        btnNewInvoice: "Emitir Nueva Factura",
        
        kpiRevenue: "Total Facturado",
        kpiPending: "Facturas Pendientes",
        kpiVat: "Impuestos Liquidados (IVA)",
        kpiInvoices: "Facturas Emitidas",
        
        tableHeaderTitle: "Directorio General de Facturas Certificadas",
        tableSearchPlaceholder: "Buscar por NIF, Número de Factura o Nombre de Cliente...",
        
        thNumber: "Nº Factura",
        thClient: "Cliente & NIF",
        thDate: "Fecha Emisión",
        thDueDate: "Vencimiento",
        thStatus: "Estado",
        thTotal: "Total (€)",
        thActions: "Acciones & PDF",
        
        wizardStep1: "1. Cliente",
        wizardStep2: "2. Artículos & IVA",
        wizardStep3: "3. Resumen Totales",
        wizardStep4: "4. Emitir & PDF",
        
        lblSelectClient: "Seleccionar Cliente *",
        lblIssueDate: "Fecha de Emisión *",
        lblDueDate: "Fecha de Vencimiento *",
        btnAddLine: "Añadir Línea de Servicio",
        btnGeneratePdf: "Emitir Factura y Generar PDF",
        
        modalPdfTitle: "Visor de Factura Certificada PDF"
    },
    fr: {
        titleBilling: "Système de Facturation & Gestion Financière",
        subtitleBilling: "Plateforme professionnelle pour l'émission de factures certifiées, calcul de la TVA et gestion des clients.",
        btnNewInvoice: "Émettre une Facture",
        
        kpiRevenue: "Total Facturé",
        kpiPending: "Factures En Attente",
        kpiVat: "Montant TVA",
        kpiInvoices: "Factures Émises",
        
        tableHeaderTitle: "Répertoire Général des Factures Certifiées",
        tableSearchPlaceholder: "Rechercher par TVA, Numéro de Facture ou Client...",
        
        thNumber: "Nº Facture",
        thClient: "Client & NIF",
        thDate: "Date d'Émission",
        thDueDate: "Échéance",
        thStatus: "Statut",
        thTotal: "Total (€)",
        thActions: "Actions & PDF",
        
        wizardStep1: "1. Client",
        wizardStep2: "2. Articles & TVA",
        wizardStep3: "3. Résumé Totaux",
        wizardStep4: "4. Émettre & PDF",
        
        lblSelectClient: "Sélectionner Client *",
        lblIssueDate: "Date d'Émission *",
        lblDueDate: "Date d'Échéance *",
        btnAddLine: "Ajouter uma Ligne",
        btnGeneratePdf: "Émettre Facture & PDF",
        
        modalPdfTitle: "Visualiseur de Facture PDF Certifiée"
    }
};

let currentLang = 'pt';
let rawFaturasData = [];
let rawClientesData = [];
let rawProdutosData = [];
let lineItems = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchClientes();
    fetchProdutos();
    fetchFaturas();
    
    // Set default dates
    const today = new Date().toISOString().split('T')[0];
    const dueDate = new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    document.getElementById('invIssueDate').value = today;
    document.getElementById('invDueDate').value = dueDate;
    
    // Initialize wizard with 1 item line
    addInvoiceLineItem();
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
    
    renderFaturasTable();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiRevenueVal').innerText = data.total_faturado;
            document.getElementById('kpiPendingVal').innerText = data.total_pendente;
            document.getElementById('kpiVatVal').innerText = data.total_iva;
            document.getElementById('kpiInvoicesVal').innerText = data.total_faturas;
        });
}

function fetchClientes() {
    fetch('/api/clientes')
        .then(res => res.json())
        .then(data => {
            rawClientesData = data;
            const select = document.getElementById('invClientSelect');
            select.innerHTML = '<option value="">-- Selecione um Cliente --</option>';
            data.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.nome} (${c.nif})</option>`;
            });
        });
}

function fetchProdutos() {
    fetch('/api/produtos')
        .then(res => res.json())
        .then(data => {
            rawProdutosData = data;
        });
}

function fetchFaturas() {
    fetch('/api/faturas')
        .then(res => res.json())
        .then(data => {
            rawFaturasData = data;
            renderFaturasTable();
        });
}

function renderFaturasTable() {
    const tbody = document.getElementById('faturasTableBody');
    const searchVal = document.getElementById('searchBox').value.toLowerCase();
    tbody.innerHTML = '';
    
    const filtered = rawFaturasData.filter(f => {
        return f.id.toLowerCase().includes(searchVal) ||
            f.cliente_nome.toLowerCase().includes(searchVal) ||
            f.cliente_nif.toLowerCase().includes(searchVal);
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 30px; color: var(--text-subtle);">Nenhuma fatura encontrada.</td></tr>`;
        return;
    }

    filtered.forEach(f => {
        let badgeClass = 'pendente';
        if (f.estado === 'Paga') badgeClass = 'paga';
        if (f.estado === 'Anulada') badgeClass = 'anulada';

        const formattedTotal = f.total_fatura.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
        const tr = document.createElement('tr');
        
        tr.innerHTML = `
            <td style="font-weight: 900; color: var(--navy-executive);">${f.id}</td>
            <td>
                <div style="font-weight: 800; font-size: 14px;">${f.cliente_nome}</div>
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700;">NIF: ${f.cliente_nif}</div>
            </td>
            <td>${f.data_emissao}</td>
            <td>${f.data_vencimento}</td>
            <td>
                <span class="badge-payment ${badgeClass}" onclick="toggleStatus('${f.id}', '${f.estado}')" style="cursor: pointer;" title="Clique para alterar estado">
                    ${f.estado}
                </span>
            </td>
            <td style="font-weight: 900; font-size: 15px; color: var(--text-main);">${formattedTotal}</td>
            <td>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-navy-primary" onclick="viewInvoicePdf('${f.id}')" style="padding: 6px 12px; font-size: 11px;">
                        <i class="fa-solid fa-file-pdf"></i> PDF
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function toggleStatus(faturaId, estadoAtual) {
    const novoEstado = estadoAtual === 'Pendente' ? 'Paga' : (estadoAtual === 'Paga' ? 'Anulada' : 'Pendente');
    fetch(`/api/faturas/estado/${faturaId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ estado: novoEstado })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            fetchFaturas();
            fetchStats();
        }
    });
}

// THE HOOK WIZARD: Cliente -> Produtos -> Gerar -> PDF
function addInvoiceLineItem() {
    const itemIndex = lineItems.length;
    lineItems.push({
        descricao: "Consultoria em Arquitetura de Software SaaS",
        qtd: 1,
        preco: 150.00,
        iva_pct: 23
    });
    renderLineItemsTable();
}

function removeInvoiceLineItem(index) {
    if (lineItems.length <= 1) return;
    lineItems.splice(index, 1);
    renderLineItemsTable();
}

function renderLineItemsTable() {
    const tbody = document.getElementById('lineItemsTableBody');
    tbody.innerHTML = '';
    
    let totalBase = 0;
    let totalIva = 0;
    
    lineItems.forEach((item, idx) => {
        const subtotal = item.qtd * item.preco;
        const valorIva = subtotal * (item.iva_pct / 100);
        const itemTotal = subtotal + valorIva;
        
        totalBase += subtotal;
        totalIva += valorIva;
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <input type="text" class="form-control" value="${item.descricao}" onchange="updateLineItem(${idx}, 'descricao', this.value)">
            </td>
            <td style="width: 90px;">
                <input type="number" class="form-control" value="${item.qtd}" min="1" onchange="updateLineItem(${idx}, 'qtd', parseFloat(this.value))">
            </td>
            <td style="width: 130px;">
                <input type="number" step="0.01" class="form-control" value="${item.preco}" onchange="updateLineItem(${idx}, 'preco', parseFloat(this.value))">
            </td>
            <td style="width: 100px;">
                <select class="form-control" onchange="updateLineItem(${idx}, 'iva_pct', parseInt(this.value))">
                    <option value="23" ${item.iva_pct === 23 ? 'selected' : ''}>23%</option>
                    <option value="13" ${item.iva_pct === 13 ? 'selected' : ''}>13%</option>
                    <option value="6" ${item.iva_pct === 6 ? 'selected' : ''}>6%</option>
                    <option value="0" ${item.iva_pct === 0 ? 'selected' : ''}>0%</option>
                </select>
            </td>
            <td style="font-weight: 900; text-align: right; vertical-align: middle; width: 130px;">
                ${itemTotal.toFixed(2)} €
            </td>
            <td style="width: 50px; text-align: center; vertical-align: middle;">
                <button onclick="removeInvoiceLineItem(${idx})" style="background: transparent; border: none; color: var(--accent-coral); font-size: 16px; cursor: pointer;">&times;</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    const grandTotal = totalBase + totalIva;
    document.getElementById('summaryBaseVal').innerText = `${totalBase.toFixed(2)} €`;
    document.getElementById('summaryIvaVal').innerText = `${totalIva.toFixed(2)} €`;
    document.getElementById('summaryTotalVal').innerText = `${grandTotal.toFixed(2)} €`;
}

function updateLineItem(idx, key, val) {
    if (lineItems[idx]) {
        lineItems[idx][key] = val;
        renderLineItemsTable();
    }
}

function submitCreateInvoiceWizard(event) {
    event.preventDefault();
    
    const clientId = document.getElementById('invClientSelect').value;
    const clientObj = rawClientesData.find(c => c.id === clientId) || {
        nome: "Cliente Final Geral",
        nif: "PT999999990",
        morada: "Portugal"
    };
    
    const preparedItens = lineItems.map(item => {
        const sub = item.qtd * item.preco;
        const vIva = sub * (item.iva_pct / 100);
        return {
            descricao: item.descricao,
            qtd: item.qtd,
            preco: item.preco,
            iva_pct: item.iva_pct,
            subtotal: sub,
            valor_iva: vIva,
            total: sub + vIva
        };
    });
    
    const payload = {
        cliente_nome: clientObj.nome,
        cliente_nif: clientObj.nif,
        cliente_morada: clientObj.morada,
        data_vencimento: document.getElementById('invDueDate').value,
        itens: preparedItens
    };
    
    fetch('/api/faturas/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            fetchFaturas();
            fetchStats();
            viewInvoicePdf(data.fatura.id);
        }
    });
}

// PDF Viewer Modal Controller
function viewInvoicePdf(faturaId) {
    const pdfUrl = `/api/faturas/pdf/${faturaId}`;
    document.getElementById('pdfIframe').src = pdfUrl;
    document.getElementById('pdfModal').classList.add('active');
}

function closePdfModal() {
    document.getElementById('pdfModal').classList.remove('active');
    document.getElementById('pdfIframe').src = '';
}
