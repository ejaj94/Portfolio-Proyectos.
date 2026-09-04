// NOVA TRENDS E-Commerce SaaS - Client Side JavaScript Logic

document.addEventListener('DOMContentLoaded', () => {
    initAdminChart();
});

function addToCart(productId, quantity = 1) {
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application.json'
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            updateCartCounter(data.cart_count);
            showToast('🛒 ' + data.message, 'success');
        } else {
            showToast('⚠️ ' + data.message, 'error');
        }
    })
    .catch(err => {
        console.error('Erro ao adicionar ao carrinho:', err);
        showToast('Erro ao adicionar ao carrinho.', 'error');
    });
}

function updateCartQuantity(productId, newQty) {
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application.json'
        },
        body: JSON.stringify({ product_id: productId, quantity: newQty })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(err => console.error(err));
}

function removeFromCart(productId) {
    if (!confirm('Tens a certeza que queres remover este item do carrinho?')) return;

    fetch('/api/cart/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application.json'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(err => console.error(err));
}

function updateCartCounter(count) {
    const badges = document.querySelectorAll('.cart-badge-count');
    badges.forEach(b => {
        b.innerText = count;
        if (count > 0) {
            b.classList.remove('d-none');
        } else {
            b.classList.add('d-none');
        }
    });
}

function showToast(message, type = 'success') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }

    const toastEl = document.createElement('div');
    const bgClass = type === 'success' ? 'bg-white text-dark border-primary' : 'bg-danger text-white';
    
    toastEl.className = `toast align-items-center show shadow-lg border-2 rounded-3 p-2 mb-2 ${bgClass}`;
    toastEl.role = 'alert';
    toastEl.innerHTML = `
        <div class="d-flex align-items-center justify-content-between">
            <div class="toast-body fw-bold">
                ${message}
            </div>
            <button type="button" class="btn-close me-2 ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;

    container.appendChild(toastEl);
    setTimeout(() => {
        if (toastEl) toastEl.remove();
    }, 4000);
}

function initAdminChart() {
    const canvas = document.getElementById('revenueChart');
    if (!canvas) return;

    const categories = JSON.parse(canvas.dataset.categories || '[]');
    const revenues = JSON.parse(canvas.dataset.revenues || '[]');

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Faturação Total (€)',
                data: revenues,
                backgroundColor: [
                    'rgba(37, 99, 235, 0.85)',
                    'rgba(124, 58, 237, 0.85)',
                    'rgba(16, 185, 129, 0.85)',
                    'rgba(245, 158, 11, 0.85)'
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            return ` Faturação: ${ctx.raw.toFixed(2)} €`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f1f5f9' },
                    ticks: {
                        callback: function(val) { return val + ' €'; }
                    }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}
