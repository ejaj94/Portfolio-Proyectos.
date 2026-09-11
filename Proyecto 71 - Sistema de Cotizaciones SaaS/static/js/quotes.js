document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Quote Line Items Manager
    const addItemBtn = document.getElementById('add-line-item-btn');
    const itemsContainer = document.getElementById('quote-line-items-container');

    if (addItemBtn && itemsContainer) {
        addItemBtn.addEventListener('click', () => {
            const row = document.createElement('div');
            row.className = 'line-item-row';
            row.style.display = 'grid';
            row.style.gridTemplateColumns = '2fr 1fr 1fr 40px';
            row.style.gap = '0.75rem';
            row.style.marginBottom = '0.75rem';

            row.innerHTML = `
                <input type="text" class="form-input item-name-input" placeholder="Nome do Serviço / Produto" required>
                <input type="number" class="form-input item-qty-input" value="1" min="1" required>
                <input type="number" step="0.01" class="form-input item-price-input" placeholder="Preço (€)" required>
                <button type="button" onclick="this.parentElement.remove()" class="btn-sm btn-secondary" style="color: var(--vibrant-crimson); padding: 0.5rem; justify-content: center;">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            `;
            itemsContainer.appendChild(row);
        });
    }

    // Quote Form Submit
    const quoteForm = document.getElementById('quote-form');
    if (quoteForm) {
        quoteForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const rows = document.querySelectorAll('.line-item-row');
            const items = [];
            rows.forEach(r => {
                const name = r.querySelector('.item-name-input').value.trim();
                const qty = parseInt(r.querySelector('.item-qty-input').value || 1);
                const price = parseFloat(r.querySelector('.item-price-input').value || 0);
                if (name && price > 0) {
                    items.push({ item_name: name, quantity: qty, unit_price: price });
                }
            });

            if (items.length === 0) {
                alert('⚠️ Adicione pelo menos um item válido ao orçamento.');
                return;
            }

            const payload = {
                client_id: document.getElementById('quote-client-id').value,
                discount_percent: parseFloat(document.getElementById('quote-discount').value || 0),
                vat_rate: parseFloat(document.getElementById('quote-vat').value || 23),
                notes: document.getElementById('quote-notes').value,
                items: items
            };

            fetch('/api/quote/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.href = `/quote/${data.quote_id}`;
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao gerar orçamento.'));
        });
    }

    // Client Form Submit
    const clientForm = document.getElementById('client-form');
    if (clientForm) {
        clientForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                company_name: document.getElementById('client-company').value,
                full_name: document.getElementById('client-name').value,
                email: document.getElementById('client-email').value,
                phone: document.getElementById('client-phone').value,
                vat_nif: document.getElementById('client-nif').value,
                address: document.getElementById('client-address').value
            };

            fetch('/api/client/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao guardar cliente.'));
        });
    }

    // Item Form Submit
    const itemForm = document.getElementById('item-form');
    if (itemForm) {
        itemForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                item_name: document.getElementById('item-name').value,
                category: document.getElementById('item-category').value,
                unit_price: parseFloat(document.getElementById('item-price').value || 0),
                description: document.getElementById('item-desc').value
            };

            fetch('/api/item/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao guardar item.'));
        });
    }
});

// Update Quote Status AJAX
function updateQuoteStatus(quoteId, newStatus) {
    if (!confirm(`Deseja alterar o estado do orçamento #${quoteId} para "${newStatus}"?`)) return;

    fetch(`/api/quote/status/${quoteId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('⚠️ ' + data.message);
        }
    })
    .catch(err => alert('❌ Erro ao atualizar orçamento.'));
}
