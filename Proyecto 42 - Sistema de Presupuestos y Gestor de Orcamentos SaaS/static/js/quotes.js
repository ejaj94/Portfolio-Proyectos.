// PRESUPUESTO PRO SaaS - Client Side Logic

function showToast(message, isError = false) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    if (isError) {
        toast.style.borderColor = '#EF4444';
    }
    toast.innerHTML = `<span>${isError ? '⚠️' : '📄'}</span> <div>${message}</div>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 4000);
}

// Quote Item Row Calculator
function calculateTotals() {
    const rows = document.querySelectorAll('.item-row');
    let subtotal = 0.0;
    
    rows.forEach(row => {
        const qtyInput = row.querySelector('.item-qty');
        const priceInput = row.querySelector('.item-price');
        const totalSpan = row.querySelector('.item-total');
        
        const qty = parseFloat(qtyInput.value) || 0;
        const price = parseFloat(priceInput.value) || 0;
        const total = qty * price;
        
        totalSpan.textContent = `€ ${total.toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        subtotal += total;
    });
    
    const taxRateInput = document.getElementById('taxRateInput');
    const taxRate = parseFloat(taxRateInput ? taxRateInput.value : 23) || 0;
    const taxAmount = subtotal * (taxRate / 100.0);
    const grandTotal = subtotal + taxAmount;
    
    const subtotalElem = document.getElementById('calcSubtotal');
    const taxElem = document.getElementById('calcTax');
    const totalElem = document.getElementById('calcTotal');
    
    if (subtotalElem) subtotalElem.textContent = `€ ${subtotal.toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (taxElem) taxElem.textContent = `€ ${taxAmount.toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (totalElem) totalElem.textContent = `€ ${grandTotal.toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

document.addEventListener('DOMContentLoaded', () => {
    // Add Item Row
    const addItemBtn = document.getElementById('addItemBtn');
    if (addItemBtn) {
        addItemBtn.addEventListener('click', () => {
            const tableBody = document.getElementById('itemsTableBody');
            const newRow = document.createElement('tr');
            newRow.className = 'item-row';
            newRow.style.borderBottom = '1px solid var(--card-border)';
            newRow.innerHTML = `
                <td style="padding: 0.75rem;">
                    <input type="text" class="form-input item-desc" placeholder="Descrição do serviço ou requisito técnico" required>
                </td>
                <td style="padding: 0.75rem; width: 100px;">
                    <input type="number" class="form-input item-qty" value="1" min="1" step="1" oninput="calculateTotals()" required>
                </td>
                <td style="padding: 0.75rem; width: 160px;">
                    <input type="number" class="form-input item-price" value="0.00" min="0" step="0.01" oninput="calculateTotals()" required>
                </td>
                <td style="padding: 0.75rem; width: 160px; font-weight: 700; text-align: right;" class="item-total">
                    € 0,00
                </td>
                <td style="padding: 0.75rem; width: 50px; text-align: center;">
                    <button type="button" class="btn-slate remove-row-btn" style="padding: 0.4rem 0.6rem; color: #EF4444; border-color: rgba(239,68,68,0.3);">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(newRow);
            
            newRow.querySelector('.remove-row-btn').addEventListener('click', () => {
                if (document.querySelectorAll('.item-row').length > 1) {
                    newRow.remove();
                    calculateTotals();
                } else {
                    showToast('O orçamento deve ter pelo menos 1 item', true);
                }
            });
        });
    }

    // Quote Form Submit
    const quoteForm = document.getElementById('quoteForm');
    if (quoteForm) {
        quoteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const clientId = document.getElementById('clientSelect').value;
            if (!clientId) {
                showToast('Por favor selecione um cliente registrado', true);
                return;
            }
            
            const issueDate = document.getElementById('issueDateInput').value;
            const validUntil = document.getElementById('validUntilInput').value;
            const taxRate = document.getElementById('taxRateInput').value;
            const notes = document.getElementById('notesInput').value;
            
            const items = [];
            document.querySelectorAll('.item-row').forEach(row => {
                const desc = row.querySelector('.item-desc').value.trim();
                const qty = row.querySelector('.item-qty').value;
                const price = row.querySelector('.item-price').value;
                if (desc) {
                    items.push({ description: desc, quantity: qty, unit_price: price });
                }
            });
            
            if (items.length === 0) {
                showToast('Adicione pelo menos 1 serviço válido', true);
                return;
            }
            
            try {
                const response = await fetch('/quotes/new', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        client_id: clientId,
                        issue_date: issueDate,
                        valid_until: validUntil,
                        tax_rate: taxRate,
                        notes: notes,
                        items: items
                    })
                });
                
                const res = await response.json();
                if (res.success) {
                    showToast(`Orçamento ${res.quote_number} gerado com sucesso!`);
                    setTimeout(() => {
                        window.location.href = `/quotes/${res.quote_id}`;
                    }, 1200);
                } else {
                    showToast('Erro ao criar orçamento', true);
                }
            } catch (err) {
                showToast('Falha na comunicação com o servidor', true);
            }
        });
    }
});

// Update Quote Status
async function updateQuoteStatus(quoteId, newStatus) {
    try {
        const response = await fetch('/api/quotes/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: quoteId, status: newStatus })
        });
        const res = await response.json();
        if (res.success) {
            showToast(res.message);
            setTimeout(() => window.location.reload(), 1000);
        }
    } catch (err) {
        showToast('Erro ao atualizar estado do orçamento', true);
    }
}

// Send Quote Email
async function sendQuoteEmail(quoteId, clientEmail) {
    if (!confirm(`Deseja enviar a proposta comercial por e-mail para ${clientEmail}?`)) return;
    
    try {
        const response = await fetch('/api/quotes/send_email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: quoteId, email: clientEmail })
        });
        const res = await response.json();
        if (res.success) {
            showToast(res.message);
        }
    } catch (err) {
        showToast('Erro ao enviar e-mail', true);
    }
}
