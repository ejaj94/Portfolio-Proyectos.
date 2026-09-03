/* ENTERPRISE AUTO PARTS INVENTORY — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleInventory: "Gestão de Inventário de Peças Auto",
        subtitleInventory: "Catálogo industrial multi-atributo, controlo de stock em tempo real e registo auditável de entradas/saídas.",
        btnNewProduct: "Registar Nova Peça",
        btnJournal: "Registo de Movimentos",
        
        kpiValuation: "Valor Total em Stock",
        kpiParts: "Peças Catalogadas",
        kpiAlerts: "Alertas Críticos",
        kpiMovements: "Movimentos Hoje",
        
        tableHeaderTitle: "Catálogo Geral de Peças Automóveis",
        tableSearchPlaceholder: "Pesquisar por Referência OEM, SKU, Nome ou Modelo de Veículo...",
        
        filterAll: "Todas as Peças",
        filterMotor: "Filtros & Motor",
        filterBrakes: "Sistema de Travões",
        filterSuspension: "Suspensão & Direção",
        filterElectric: "Sistema Elétrico",
        filterLighting: "Iluminação",
        
        thSku: "SKU / OEM",
        thPartName: "Nome da Peça & Compatibilidade",
        thCategory: "Categoria",
        thLocation: "Localização",
        thStock: "Stock",
        thPrice: "Preço Venda",
        thStatus: "Estado",
        thActions: "Ações",
        
        modalTitle: "Registar Nova Peça no Inventário",
        modalSubtitle: "Preencha os atributos técnicos da peça automóvel.",
        lblOem: "Referência OEM *",
        lblPartName: "Nome da Peça *",
        lblCategory: "Categoria *",
        lblBrand: "Marca *",
        lblCompatibility: "Veículos Compatíveis *",
        lblStockInit: "Stock Inicial *",
        lblStockMin: "Stock Mínimo Alerta *",
        lblCostPrice: "Preço de Custo (€) *",
        lblSalePrice: "Preço de Venda (€) *",
        lblLocation: "Localização no Armazém *",
        btnSubmitPart: "Guardar no Inventário",
        
        movModalTitle: "Registar Movimento de Stock",
        movModalSubtitle: "Entrada de Fornecedor ou Saída para Expedição",
        lblMovType: "Tipo de Movimento *",
        lblMovQty: "Quantidade *",
        lblMovReason: "Motivo / Ref. Documento *",
        btnSubmitMov: "Confirmar Movimento"
    },
    en: {
        titleInventory: "Auto Parts Enterprise Inventory",
        subtitleInventory: "Industrial multi-attribute catalog, real-time stock control and audit movement ledger.",
        btnNewProduct: "Register New Part",
        btnJournal: "Movement Journal",
        
        kpiValuation: "Total Stock Valuation",
        kpiParts: "Cataloged Parts",
        kpiAlerts: "Critical Stock Alerts",
        kpiMovements: "Movements Today",
        
        tableHeaderTitle: "General Auto Parts Directory",
        tableSearchPlaceholder: "Search OEM Reference, SKU, Part Name or Vehicle Compatibility...",
        
        filterAll: "All Parts",
        filterMotor: "Filters & Engine",
        filterBrakes: "Brake System",
        filterSuspension: "Suspension & Steering",
        filterElectric: "Electrical System",
        filterLighting: "Lighting",
        
        thSku: "SKU / OEM",
        thPartName: "Part Name & Fitment",
        thCategory: "Category",
        thLocation: "Warehouse Bin",
        thStock: "Stock",
        thPrice: "Sale Price",
        thStatus: "Status",
        thActions: "Actions",
        
        modalTitle: "Register New Auto Part",
        modalSubtitle: "Enter technical attributes for warehouse catalog.",
        lblOem: "OEM Reference *",
        lblPartName: "Part Name *",
        lblCategory: "Category *",
        lblBrand: "Brand *",
        lblCompatibility: "Compatible Vehicles *",
        lblStockInit: "Initial Stock *",
        lblStockMin: "Min Alert Threshold *",
        lblCostPrice: "Cost Price (€) *",
        lblSalePrice: "Sale Price (€) *",
        lblLocation: "Bin Location *",
        btnSubmitPart: "Save in Inventory",
        
        movModalTitle: "Register Stock Movement",
        movModalSubtitle: "Supplier Check-In or Shipment Check-Out",
        lblMovType: "Movement Type *",
        lblMovQty: "Quantity *",
        lblMovReason: "Reason / Doc Ref *",
        btnSubmitMov: "Confirm Movement"
    },
    es: {
        titleInventory: "Gestión de Inventario de Piezas Auto",
        subtitleInventory: "Catálogo industrial multi-atributo, control de stock en tiempo real y libro de movimientos.",
        btnNewProduct: "Registrar Nueva Pieza",
        btnJournal: "Historial Movimientos",
        
        kpiValuation: "Valor Total de Stock",
        kpiParts: "Piezas Catalogadas",
        kpiAlerts: "Alertas Críticas",
        kpiMovements: "Movimientos Hoy",
        
        tableHeaderTitle: "Catálogo General de Piezas de Automóvil",
        tableSearchPlaceholder: "Buscar por Referencia OEM, SKU, Nombre o Modelo de Vehículo...",
        
        filterAll: "Todas las Piezas",
        filterMotor: "Filtros y Motor",
        filterBrakes: "Sistema de Frenos",
        filterSuspension: "Suspensión y Dirección",
        filterElectric: "Sistema Eléctrico",
        filterLighting: "Iluminación",
        
        thSku: "SKU / OEM",
        thPartName: "Nombre de Pieza y Compatibilidad",
        thCategory: "Categoría",
        thLocation: "Ubicación Almacén",
        thStock: "Stock",
        thPrice: "Precio Venta",
        thStatus: "Estado",
        thActions: "Acciones",
        
        modalTitle: "Registrar Nueva Pieza en Inventario",
        modalSubtitle: "Rellene los atributos técnicos de la pieza.",
        lblOem: "Referencia OEM *",
        lblPartName: "Nombre de Pieza *",
        lblCategory: "Categoría *",
        lblBrand: "Marca *",
        lblCompatibility: "Vehículos Compatibles *",
        lblStockInit: "Stock Inicial *",
        lblStockMin: "Stock Mínimo Alerta *",
        lblCostPrice: "Precio Coste (€) *",
        lblSalePrice: "Precio Venta (€) *",
        lblLocation: "Ubicación Almacén *",
        btnSubmitPart: "Guardar en Inventario",
        
        movModalTitle: "Registrar Movimiento de Stock",
        movModalSubtitle: "Entrada de Proveedor o Salida de Expedición",
        lblMovType: "Tipo de Movimiento *",
        lblMovQty: "Cantidad *",
        lblMovReason: "Motivo / Ref. Documento *",
        btnSubmitMov: "Confirmar Movimiento"
    },
    fr: {
        titleInventory: "Gestion d'Inventaire Pièces Auto",
        subtitleInventory: "Catalogue industriel multi-attributs, contrôle de stock en temps réel et journal de mouvements.",
        btnNewProduct: "Enregistrer Pièce",
        btnJournal: "Journal Mouvements",
        
        kpiValuation: "Valeur Totale du Stock",
        kpiParts: "Pièces Cataloguées",
        kpiAlerts: "Alertes Critiques",
        kpiMovements: "Mouvements Aujourd'hui",
        
        tableHeaderTitle: "Répertoire Général de Pièces Automobile",
        tableSearchPlaceholder: "Rechercher par Référence OEM, SKU, Nom ou Véhicule...",
        
        filterAll: "Toutes les Pièces",
        filterMotor: "Filtres & Moteur",
        filterBrakes: "Système de Freinage",
        filterSuspension: "Suspension & Direction",
        filterElectric: "Système Électrique",
        filterLighting: "Éclairage",
        
        thSku: "SKU / OEM",
        thPartName: "Nom de Pièce & Compatibilité",
        thCategory: "Catégorie",
        thLocation: "Emplacement Almacén",
        thStock: "Stock",
        thPrice: "Prix Vente",
        thStatus: "Statut",
        thActions: "Actions",
        
        modalTitle: "Enregistrer une Nouvelle Pièce",
        modalSubtitle: "Saisissez les attributs techniques de la pièce.",
        lblOem: "Référence OEM *",
        lblPartName: "Nom de Pièce *",
        lblCategory: "Catégorie *",
        lblBrand: "Marque *",
        lblCompatibility: "Véhicules Compatibles *",
        lblStockInit: "Stock Initial *",
        lblStockMin: "Seuil Alerte Min *",
        lblCostPrice: "Prix d'Achat (€) *",
        lblSalePrice: "Prix de Vente (€) *",
        lblLocation: "Emplacement *",
        btnSubmitPart: "Enregistrer dans l'Inventaire",
        
        movModalTitle: "Enregistrer Mouvement de Stock",
        movModalSubtitle: "Réception Fournisseur ou Expédition Commande",
        lblMovType: "Type de Mouvement *",
        lblMovQty: "Quantité *",
        lblMovReason: "Motif / Réf Doc *",
        btnSubmitMov: "Confirmer Mouvement"
    }
};

let currentLang = 'pt';
let rawProdutosData = [];
let activeCategory = 'all';
let selectedSkuForMov = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchProdutos();
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
    
    renderProdutosTable();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiValuationVal').innerText = data.valor_stock;
            document.getElementById('kpiPartsVal').innerText = data.total_pecas;
            document.getElementById('kpiAlertsVal').innerText = data.alertas_criticos;
            document.getElementById('kpiMovementsVal').innerText = data.movimentos_hoje;
        });
}

function fetchProdutos() {
    fetch('/api/produtos')
        .then(res => res.json())
        .then(data => {
            rawProdutosData = data;
            renderProdutosTable();
        });
}

function setCategoryFilter(cat) {
    activeCategory = cat;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-category') === cat);
    });
    renderProdutosTable();
}

function renderProdutosTable() {
    const tbody = document.getElementById('produtosTableBody');
    const searchVal = document.getElementById('searchBox').value.toLowerCase();
    tbody.innerHTML = '';
    
    const filtered = rawProdutosData.filter(p => {
        const matchesCategory = activeCategory === 'all' || p.categoria === activeCategory;
        const matchesSearch = p.nome.toLowerCase().includes(searchVal) ||
            p.oem.toLowerCase().includes(searchVal) ||
            p.sku.toLowerCase().includes(searchVal) ||
            p.compatibilidade.toLowerCase().includes(searchVal) ||
            p.marca.toLowerCase().includes(searchVal);
            
        return matchesCategory && matchesSearch;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 30px; color: var(--text-subtle);">Nenhuma peça encontrada no catálogo.</td></tr>`;
        return;
    }

    filtered.forEach(p => {
        let badgeClass = 'ok';
        if (p.estado === 'Alerta Crítico') badgeClass = 'alerta';
        if (p.estado === 'Fora de Stock') badgeClass = 'fora';

        const formattedPrice = p.preco_venda.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
        const tr = document.createElement('tr');
        
        tr.innerHTML = `
            <td>
                <div style="font-weight: 900; color: var(--autodoc-orange);">${p.sku}</div>
                <div class="oem-code-tag">${p.oem}</div>
            </td>
            <td>
                <div style="font-weight: 800; font-size: 15px;">${p.nome}</div>
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700;"><i class="fa-solid fa-car-side"></i> ${p.compatibilidade} (${p.marca})</div>
            </td>
            <td><span style="font-size: 12px; font-weight: 800; color: var(--electric-blue);">${p.categoria}</span></td>
            <td><span class="location-tag"><i class="fa-solid fa-boxes-packing"></i> ${p.localizacao}</span></td>
            <td>
                <div style="font-weight: 900; font-size: 16px;">${p.stock} un.</div>
                <div style="font-size: 10px; color: var(--text-subtle);">Min: ${p.stock_min} un.</div>
            </td>
            <td style="font-weight: 900; color: var(--text-main);">${formattedPrice}</td>
            <td><span class="badge-stock ${badgeClass}">${p.estado}</span></td>
            <td>
                <div style="display: flex; gap: 6px;">
                    <button class="btn-stock-in" onclick="openMovementModal('${p.sku}', 'Entrada')" title="Entrada de Stock">+</button>
                    <button class="btn-stock-out" onclick="openMovementModal('${p.sku}', 'Saída')" title="Saída de Stock">-</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Movement Modal Controller
function openMovementModal(sku, defaultType = 'Entrada') {
    selectedSkuForMov = sku;
    const prod = rawProdutosData.find(p => p.sku === sku);
    if (!prod) return;
    
    document.getElementById('movTargetName').innerText = `${prod.nome} (${prod.oem})`;
    document.getElementById('movTypeSelect').value = defaultType;
    document.getElementById('movQtyInput').value = 1;
    document.getElementById('movReasonInput').value = defaultType === 'Entrada' ? 'Recebimento de Fornecedor' : 'Expedição de Encomenda';
    
    document.getElementById('movementModal').classList.add('active');
}

function closeMovementModal() {
    document.getElementById('movementModal').classList.remove('active');
    selectedSkuForMov = null;
}

function submitMovementForm(event) {
    event.preventDefault();
    if (!selectedSkuForMov) return;
    
    const movData = {
        sku: selectedSkuForMov,
        tipo: document.getElementById('movTypeSelect').value,
        quantidade: parseInt(document.getElementById('movQtyInput').value) || 1,
        motivo: document.getElementById('movReasonInput').value.trim()
    };
    
    fetch('/api/produtos/movimento', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(movData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeMovementModal();
            fetchProdutos();
            fetchStats();
        } else {
            alert(data.message || "Erro ao processar movimento.");
        }
    });
}

// Journal Drawer Controller
function openJournalDrawer() {
    fetch('/api/movimentos')
        .then(res => res.json())
        .then(movimentos => {
            renderJournalList(movimentos);
            document.getElementById('journalDrawerBackdrop').classList.add('active');
        });
}

function closeJournalDrawer() {
    document.getElementById('journalDrawerBackdrop').classList.remove('active');
}

function renderJournalList(movimentos) {
    const list = document.getElementById('journalListContainer');
    list.innerHTML = '';
    
    movimentos.forEach(m => {
        const item = document.createElement('div');
        item.style.cssText = "background: var(--bg-main); border: 1px solid var(--border-light); border-radius: 14px; padding: 14px; margin-bottom: 12px;";
        const isEntrada = m.tipo === 'Entrada';
        const icon = isEntrada ? '<i class="fa-solid fa-arrow-down" style="color: var(--accent-emerald);"></i>' : '<i class="fa-solid fa-arrow-up" style="color: var(--accent-coral);"></i>';
        
        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-weight: 900; font-size: 13px;">${icon} ${m.tipo}: <b>${m.quantidade} un.</b></span>
                <span style="font-size: 11px; color: var(--text-subtle);">${m.data}</span>
            </div>
            <div style="font-size: 13px; font-weight: 800; color: var(--text-main);">${m.nome}</div>
            <div style="font-size: 11px; color: var(--text-subtle); margin-top: 4px;">${m.motivo} • (${m.operador})</div>
        `;
        list.appendChild(item);
    });
}

// Modal Form Controller for New Product
function openNewProductModal() {
    document.getElementById('newProductModal').classList.add('active');
}

function closeNewProductModal() {
    document.getElementById('newProductModal').classList.remove('active');
}

function submitNewProductForm(event) {
    event.preventDefault();
    
    const newProdData = {
        oem: document.getElementById('partOem').value.trim(),
        nome: document.getElementById('partName').value.trim(),
        categoria: document.getElementById('partCategory').value,
        marca: document.getElementById('partBrand').value.trim(),
        compatibilidade: document.getElementById('partCompatibility').value.trim(),
        stock: parseInt(document.getElementById('partStock').value) || 10,
        stock_min: parseInt(document.getElementById('partStockMin').value) || 5,
        preco_custo: floatParse(document.getElementById('partCostPrice').value),
        preco_venda: floatParse(document.getElementById('partSalePrice').value),
        localizacao: document.getElementById('partLocation').value.trim()
    };
    
    fetch('/api/produtos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProdData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewProductModal();
            fetchProdutos();
            fetchStats();
        }
    });
}

function floatParse(val) {
    return parseFloat(val) || 0.0;
}
