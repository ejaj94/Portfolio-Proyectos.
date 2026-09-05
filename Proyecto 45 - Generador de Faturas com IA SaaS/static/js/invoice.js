/**
 * AI Invoice Generator SaaS (Proyecto 45)
 * Client Controller
 */

window.aiInvoice = {
    items: [],

    init: function() {
        console.log('[AI INVOICE] Gerador de Faturas com IA Inicializado.');
        this.bindEvents();
    },

    bindEvents: function() {
        const vatSelect = document.getElementById('vatRateSelect');
        if (vatSelect) {
            vatSelect.addEventListener('change', () => this.recalculateTotals());
        }
    },

    processAIPrompt: function() {
        const promptText = document.getElementById('aiPromptInput').value.trim();
        if (!promptText) {
            alert('Por favor introduza a descrição do trabalho para a IA processar.');
            return;
        }

        const btn = document.getElementById('btnProcessAI');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>A Processar com IA...';
        }

        fetch('/api/ai/parse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: promptText })
        })
        .then(res => res.json())
        .then(data => {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-cpu-fill me-2"></i>GERAR FATURA COM IA 🤖';
            }

            if (data.success) {
                const parsed = data.parsed_data;
                // Select Client
                if (parsed.client && parsed.client.id) {
                    const clientSelect = document.getElementById('clientSelect');
                    if (clientSelect) clientSelect.value = parsed.client.id;
                }

                // Select VAT
                const vatSelect = document.getElementById('vatRateSelect');
                if (vatSelect) vatSelect.value = parsed.vat_rate;

                // Load items
                this.items = parsed.items || [];
                this.renderItemsTable();
                this.recalculateTotals();

                // Notes
                const notesInput = document.getElementById('invoiceNotes');
                if (notesInput) notesInput.value = parsed.suggested_notes || '';

                alert('✨ IA: Fatura processada e itemizada com sucesso! Verifique os valores abaixo.');
            } else {
                alert(`⚠️ ${data.message}`);
            }
        })
        .catch(err => {
            console.error('Erro no parser IA:', err);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-cpu-fill me-2"></i>GERAR FATURA COM IA 🤖';
            }
            alert('Erro ao ligar ao motor de Inteligência Artificial.');
        });
    },

    renderItemsTable: function() {
        const tbody = document.getElementById('itemsTableBody');
        if (!tbody) return;

        if (this.items.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted py-4">Nenhum item adicionado à fatura.</td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = this.items.map((item, index) => `
            <tr>
                <td>
                    <input type="text" class="form-control form-control-sm border-secondary-subtle" value="${this.escapeStr(item.description)}" onchange="aiInvoice.updateItem(${index}, 'description', this.value)">
                </td>
                <td style="width: 100px;">
                    <input type="number" step="0.5" class="form-control form-control-sm text-center border-secondary-subtle" value="${item.quantity}" onchange="aiInvoice.updateItem(${index}, 'quantity', this.value)">
                </td>
                <td style="width: 140px;">
                    <div class="input-group input-group-sm">
                        <span class="input-group-text">€</span>
                        <input type="number" step="0.01" class="form-control text-end border-secondary-subtle" value="${item.unit_price}" onchange="aiInvoice.updateItem(${index}, 'unit_price', this.value)">
                    </div>
                </td>
                <td class="text-end fw-bold text-neon-blue" style="width: 130px;">
                    € ${(item.quantity * item.unit_price).toFixed(2)}
                </td>
                <td class="text-center" style="width: 60px;">
                    <button class="btn btn-outline-danger btn-sm rounded-circle" onclick="aiInvoice.removeItem(${index})" title="Remover Line Item">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    },

    addItemRow: function() {
        this.items.push({
            description: 'Novo Serviço / Produto',
            quantity: 1.0,
            unit_price: 100.0,
            total_price: 100.0
        });
        this.renderItemsTable();
        this.recalculateTotals();
    },

    updateItem: function(index, field, val) {
        if (!this.items[index]) return;
        if (field === 'quantity' || field === 'unit_price') {
            this.items[index][field] = parseFloat(val) || 0;
            this.items[index].total_price = this.items[index].quantity * this.items[index].unit_price;
        } else {
            this.items[index][field] = val;
        }
        this.renderItemsTable();
        this.recalculateTotals();
    },

    removeItem: function(index) {
        this.items.splice(index, 1);
        this.renderItemsTable();
        this.recalculateTotals();
    },

    recalculateTotals: function() {
        const subtotal = this.items.reduce((acc, item) => acc + (item.quantity * item.unit_price), 0);
        const vatRate = parseFloat(document.getElementById('vatRateSelect')?.value || 23.0);
        const vatAmount = subtotal * (vatRate / 100.0);
        const total = subtotal + vatAmount;

        if (document.getElementById('lblSubtotal')) document.getElementById('lblSubtotal').innerText = `€ ${subtotal.toFixed(2)}`;
        if (document.getElementById('lblVatAmount')) document.getElementById('lblVatAmount').innerText = `€ ${vatAmount.toFixed(2)}`;
        if (document.getElementById('lblTotal')) document.getElementById('lblTotal').innerText = `€ ${total.toFixed(2)}`;
    },

    submitInvoice: function() {
        const clientId = document.getElementById('clientSelect').value;
        const vatRate = document.getElementById('vatRateSelect').value;
        const notes = document.getElementById('invoiceNotes').value;

        if (!clientId) {
            alert('Por favor selecione o cliente da fatura.');
            return;
        }

        if (this.items.length === 0) {
            alert('A fatura necessita de pelo menos 1 linha de serviço/produto.');
            return;
        }

        fetch('/api/invoice/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_id: clientId,
                items: this.items,
                vat_rate: vatRate,
                notes: notes
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✅ ${data.message}`);
                window.location.href = `/invoice/${data.invoice_id}`;
            } else {
                alert(`⚠️ ${data.message}`);
            }
        })
        .catch(err => {
            console.error('Erro ao emitir fatura:', err);
            alert('Ocorreu um erro ao emitir a fatura.');
        });
    },

    updateStatus: function(invoiceId, status) {
        fetch(`/api/invoice/${invoiceId}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: status })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`👍 ${data.message}`);
                window.location.reload();
            }
        });
    },

    escapeStr: function(str) {
        if (!str) return '';
        return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    aiInvoice.init();
});
