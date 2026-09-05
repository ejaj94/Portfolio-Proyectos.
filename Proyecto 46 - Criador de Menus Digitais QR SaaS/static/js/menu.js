/**
 * QR Digital Menu Builder SaaS (Proyecto 46)
 * Client Controller & Cart System
 */

window.qrMenu = {
    cart: [],
    whatsappPhone: '',

    init: function() {
        console.log('[QR MENU] Plataforma de Menus Digitais Inicializada.');
        this.bindEvents();
    },

    bindEvents: function() {
        const searchInput = document.getElementById('menuSearchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.filterProducts(e.target.value));
        }
    },

    selectCategory: function(catId, btn) {
        document.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');

        if (catId === 'all') {
            document.querySelectorAll('.category-section').forEach(s => s.style.display = 'block');
        } else {
            document.querySelectorAll('.category-section').forEach(s => {
                if (s.id === `cat-section-${catId}`) {
                    s.style.display = 'block';
                    s.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    s.style.display = 'none';
                }
            });
        }
    },

    filterProducts: function(query) {
        const q = query.toLowerCase().strip ? query.toLowerCase().strip() : query.toLowerCase();
        document.querySelectorAll('.product-item-card').forEach(card => {
            const name = card.getAttribute('data-name') || '';
            const desc = card.getAttribute('data-desc') || '';
            if (name.toLowerCase().includes(q) || desc.toLowerCase().includes(q)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    },

    addToCart: function(id, name, price) {
        const existing = this.cart.find(item => item.id === id);
        if (existing) {
            existing.qty += 1;
        } else {
            this.cart.push({ id, name, price, qty: 1 });
        }
        this.updateCartUI();
    },

    updateCartUI: function() {
        const bar = document.getElementById('floatingCartBar');
        const countLbl = document.getElementById('cartCountLbl');
        const totalLbl = document.getElementById('cartTotalLbl');

        const totalItems = this.cart.reduce((sum, item) => sum + item.qty, 0);
        const totalPrice = this.cart.reduce((sum, item) => sum + (item.qty * item.price), 0);

        if (countLbl) countLbl.innerText = totalItems;
        if (totalLbl) totalLbl.innerText = `€ ${totalPrice.toFixed(2)}`;

        if (bar) {
            if (totalItems > 0) {
                bar.style.display = 'flex';
            } else {
                bar.style.display = 'none';
            }
        }
    },

    sendWhatsAppOrder: function(phone) {
        if (this.cart.length === 0) return;

        let msg = "🛒 *NOVO PEDIDO DE MESA - MENU DIGITAL QR*\n\n";
        let total = 0;

        this.cart.forEach(item => {
            const sub = item.qty * item.price;
            total += sub;
            msg += `• ${item.qty}x *${item.name}* (€ ${sub.toFixed(2)})\n`;
        });

        msg += `\n💰 *TOTAL DO PEDIDO:* € ${total.toFixed(2)}\n`;
        msg += "📌 *Mesa N.º:* [Mesa 04]";

        const targetPhone = phone ? phone.replace(/[^0-9]/g, '') : '351911151993';
        const url = `https://wa.me/${targetPhone}?text=${encodeURIComponent(msg)}`;
        window.open(url, '_blank');
    },

    // ADMIN ACTIONS
    createProduct: function(restId) {
        const name = document.getElementById('prodName').value.trim();
        const catId = document.getElementById('prodCatId').value;
        const price = document.getElementById('prodPrice').value;
        const origPrice = document.getElementById('prodOrigPrice').value;
        const desc = document.getElementById('prodDesc').value.trim();
        const allergens = document.getElementById('prodAllergens').value.trim();
        const img = document.getElementById('prodImage').value.trim();
        const featured = document.getElementById('prodFeatured').checked;

        if (!name || !catId || !price) {
            alert('Por favor preencha nome, categoria e preço.');
            return;
        }

        fetch('/api/products/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                restaurant_id: restId,
                category_id: catId,
                name: name,
                description: desc,
                price: price,
                original_price: origPrice,
                image_url: img,
                allergens: allergens,
                is_featured: featured
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✅ ${data.message}`);
                window.location.reload();
            } else {
                alert(`⚠️ ${data.message}`);
            }
        });
    },

    createCategory: function(restId) {
        const name = document.getElementById('catName').value.trim();
        const icon = document.getElementById('catIcon').value;

        if (!name) return;

        fetch('/api/categories/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ restaurant_id: restId, name: name, icon: icon })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✅ ${data.message}`);
                window.location.reload();
            }
        });
    },

    createOffer: function(restId) {
        const title = document.getElementById('offerTitle').value.trim();
        const desc = document.getElementById('offerDesc').value.trim();
        const badge = document.getElementById('offerBadge').value.trim();
        const discount = document.getElementById('offerDiscount').value;

        if (!title) return;

        fetch('/api/offers/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                restaurant_id: restId,
                title: title,
                description: desc,
                badge_text: badge,
                discount_percent: discount
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✅ ${data.message}`);
                window.location.reload();
            }
        });
    },

    updateTheme: function(restId) {
        const color = document.getElementById('themeColor').value;
        const bg = document.getElementById('themeBg').value;
        const tagline = document.getElementById('themeTagline').value;
        const phone = document.getElementById('themePhone').value;

        fetch('/api/theme/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                restaurant_id: restId,
                primary_color: color,
                bg_theme: bg,
                tagline: tagline,
                phone_whatsapp: phone
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`🎨 ${data.message}`);
                window.location.reload();
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    qrMenu.init();
});
