// NOVA TRENDS E-Commerce SaaS - Client Side JavaScript Logic & Features

const TRANSLATIONS = {
    'pt': {
        'store': 'Loja',
        'my_orders': 'As Minhas Encomendas',
        'admin_panel': 'Painel Admin',
        'cart': 'Carrinho',
        'search_placeholder': 'Pesquisar produtos inovadores...',
        'hero_badge': 'Nova Coleção 2026',
        'hero_title': 'Tecnologia de Ponta & Produtos Inovadores',
        'hero_desc': 'Descobre os 10 produtos de maior sucesso e mais desejados do momento.',
        'explore': 'Explorar Catálogo',
        'track_order': 'Rastrear Encomenda',
        'buy': 'Comprar',
        'details': 'Ver Ficha',
        'add_to_cart': 'Adicionar ao Carrinho',
        'total': 'Total',
        'checkout': 'Finalizar Compra',
        'cart_empty': 'O teu carrinho está vazio',
        'theme_light': '☀️ Claro',
        'theme_dark': '🌙 Escuro'
    },
    'en': {
        'store': 'Store',
        'my_orders': 'My Orders',
        'admin_panel': 'Admin Dashboard',
        'cart': 'Cart',
        'search_placeholder': 'Search innovative products...',
        'hero_badge': 'New Collection 2026',
        'hero_title': 'Cutting-Edge Tech & Innovative Products',
        'hero_desc': 'Discover the 10 most successful and sought-after products right now.',
        'explore': 'Explore Catalog',
        'track_order': 'Track Order',
        'buy': 'Buy Now',
        'details': 'View Details',
        'add_to_cart': 'Add to Cart',
        'total': 'Total',
        'checkout': 'Proceed to Checkout',
        'cart_empty': 'Your cart is empty',
        'theme_light': '☀️ Light',
        'theme_dark': '🌙 Dark'
    },
    'es': {
        'store': 'Tienda',
        'my_orders': 'Mis Pedidos',
        'admin_panel': 'Panel Admin',
        'cart': 'Carrito',
        'search_placeholder': 'Buscar productos innovadores...',
        'hero_badge': 'Nueva Colección 2026',
        'hero_title': 'Tecnología de Punta y Productos Innovadores',
        'hero_desc': 'Descubre los 10 productos de mayor éxito y más deseados del momento.',
        'explore': 'Explorar Catálogo',
        'track_order': 'Rastrear Pedido',
        'buy': 'Comprar',
        'details': 'Ver Ficha',
        'add_to_cart': 'Añadir al Carrito',
        'total': 'Total',
        'checkout': 'Finalizar Compra',
        'cart_empty': 'Tu carrito está vacío',
        'theme_light': '☀️ Claro',
        'theme_dark': '🌙 Oscuro'
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLanguage();
    initAdminChart();
});

// --- THEME SWITCHER (LIGHT / DARK) ---
function initTheme() {
    const savedTheme = localStorage.getItem('nova_theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    setTheme(currentTheme);
}

function setTheme(theme) {
    if (theme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        localStorage.setItem('nova_theme', 'dark');
    } else {
        document.body.removeAttribute('data-theme');
        localStorage.setItem('nova_theme', 'light');
    }
    updateThemeButtonText();
}

function updateThemeButtonText() {
    const btn = document.getElementById('themeToggleBtn');
    if (!btn) return;
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    const lang = localStorage.getItem('nova_lang') || 'pt';
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['pt'];
    btn.innerHTML = isDark ? dict['theme_light'] : dict['theme_dark'];
}

// --- MULTI-LANGUAGE SYSTEM ---
function initLanguage() {
    const savedLang = localStorage.getItem('nova_lang') || 'pt';
    setLanguage(savedLang, false);
}

function changeLanguage(lang) {
    setLanguage(lang, true);
}

function setLanguage(lang, reload = false) {
    localStorage.setItem('nova_lang', lang);
    const langSelect = document.getElementById('langSelect');
    if (langSelect) langSelect.value = lang;

    updateThemeButtonText();

    // Translate DOM elements marked with data-i18n
    const elements = document.querySelectorAll('[data-i18n]');
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['pt'];

    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            if (el.tagName === 'INPUT' && el.placeholder) {
                el.placeholder = dict[key];
            } else {
                el.innerText = dict[key];
            }
        }
    });

    if (reload) {
        showToast(`Idioma alterado: ${lang.toUpperCase()}`, 'success');
    }
}

// --- CART API OPERATIONS ---
function addToCart(productId, quantity = 1) {
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            updateCartCounter(data.cart_count);
            showToast('🛒 ' + data.message, 'success');
        } else {
            showToast('⚠️ ' + (data.message || 'Erro ao adicionar'), 'error');
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
            'Content-Type': 'application/json'
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
            'Content-Type': 'application/json'
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
                    grid: { color: 'rgba(200, 200, 200, 0.15)' },
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
