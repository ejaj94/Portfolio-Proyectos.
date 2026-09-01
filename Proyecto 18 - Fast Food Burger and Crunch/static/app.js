// BURGER & CRUNCH — Fast Food Interactive Application Engine

let CART = [];
const DELIVERY_FEE = 1.50;

document.addEventListener('DOMContentLoaded', () => {
    initCategoryFilters();
    initMobileDrawer();
    initCartEvents();
    initCheckoutForm();
    initImageLightbox();
});

// Category Filter Tabs
function initCategoryFilters() {
    const filterBtns = document.querySelectorAll('.menu-tab-btn');
    const menuCards = document.querySelectorAll('.fastfood-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const category = btn.getAttribute('data-category');

            menuCards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Mobile Nav Toggle
function initMobileDrawer() {
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const drawer = document.getElementById('mobileDrawer');

    if (toggleBtn && drawer) {
        toggleBtn.addEventListener('click', () => {
            drawer.classList.toggle('active');
        });

        document.querySelectorAll('.mobile-link').forEach(link => {
            link.addEventListener('click', () => {
                drawer.classList.remove('active');
            });
        });
    }
}

// Cart Drawer Backdrop Controls
function initCartEvents() {
    const btnOpenCart = document.getElementById('btnOpenCart');
    const btnCloseCart = document.getElementById('btnCloseCart');
    const backdrop = document.getElementById('cartDrawerBackdrop');

    if (btnOpenCart && backdrop) {
        btnOpenCart.addEventListener('click', openCartDrawer);
    }
    if (btnCloseCart && backdrop) {
        btnCloseCart.addEventListener('click', closeCartDrawer);
    }
}

function openCartDrawer() {
    const backdrop = document.getElementById('cartDrawerBackdrop');
    if (backdrop) backdrop.classList.add('active');
    renderCart();
}

function closeCartDrawer() {
    const backdrop = document.getElementById('cartDrawerBackdrop');
    if (backdrop) backdrop.classList.remove('active');
}

// Add Item to Cart
function addToCart(name, price, img) {
    const existing = CART.find(item => item.name === name);
    if (existing) {
        existing.quantity += 1;
    } else {
        CART.push({
            name: name,
            price: parseFloat(price),
            img: img,
            quantity: 1
        });
    }

    renderCart();
    showToast(`Adicionado: ${name}`);
}

// Change Item Quantity
function changeQty(name, delta) {
    const item = CART.find(i => i.name === name);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
            CART = CART.filter(i => i.name !== name);
        }
    }
    renderCart();
}

// Render Cart Engine & Update Totals
function renderCart() {
    const cartItemsList = document.getElementById('cartItemsList');
    const cartCountBadge = document.getElementById('cartCountBadge');
    const floatingCartBadge = document.getElementById('floatingCartBadge');
    const heroCartTotal = document.getElementById('heroCartTotal');
    const cartSubtotalText = document.getElementById('cartSubtotalText');
    const cartDeliveryFeeText = document.getElementById('cartDeliveryFeeText');
    const cartTotalText = document.getElementById('cartTotalText');
    const orderType = document.getElementById('selOrderType') ? document.getElementById('selOrderType').value : 'Delivery';

    if (!cartItemsList) return;

    let subtotal = 0;
    let totalItemsCount = 0;

    if (CART.length === 0) {
        cartItemsList.innerHTML = `
            <div class="empty-cart-msg">
                <i class="fa-solid fa-burger text-muted"></i>
                <p>O seu carrinho está vazio. Adicione hambúrgueres e snacks do menu!</p>
            </div>
        `;
    } else {
        let html = '';
        CART.forEach(item => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;
            totalItemsCount += item.quantity;

            html += `
                <div class="cart-item-row">
                    <img src="${item.img}" alt="${item.name}" class="cart-item-img">
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <span class="cart-item-price">${item.price.toFixed(2)} €</span>
                    </div>
                    <div class="cart-qty-ctrl">
                        <button onclick="changeQty('${item.name}', -1)" class="btn-qty">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="changeQty('${item.name}', 1)" class="btn-qty">+</button>
                    </div>
                </div>
            `;
        });
        cartItemsList.innerHTML = html;
    }

    const currentFee = (orderType === 'Delivery' && CART.length > 0) ? DELIVERY_FEE : 0.00;
    const finalTotal = subtotal + currentFee;

    // Badges update
    if (cartCountBadge) cartCountBadge.textContent = totalItemsCount;
    if (floatingCartBadge) floatingCartBadge.textContent = totalItemsCount;
    if (heroCartTotal) heroCartTotal.textContent = `${finalTotal.toFixed(2)}€`;

    // Totals text
    if (cartSubtotalText) cartSubtotalText.textContent = `${subtotal.toFixed(2)} €`;
    if (cartDeliveryFeeText) cartDeliveryFeeText.textContent = `${currentFee.toFixed(2)} €`;
    if (cartTotalText) cartTotalText.textContent = `${finalTotal.toFixed(2)} €`;
}

// Toggle Morada
function toggleDeliveryAddress(type) {
    const groupAddress = document.getElementById('groupDeliveryAddress');
    const inputAddress = document.getElementById('inputDeliveryAddress');

    if (type === 'Takeaway') {
        if (groupAddress) groupAddress.style.display = 'none';
        if (inputAddress) inputAddress.required = false;
    } else {
        if (groupAddress) groupAddress.style.display = 'flex';
        if (inputAddress) inputAddress.required = true;
    }

    renderCart();
}

// Checkout Form Submission
function initCheckoutForm() {
    const form = document.getElementById('fastfoodCheckoutForm');
    const btnSubmit = document.getElementById('btnSubmitOrder');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (CART.length === 0) {
                showToast("Por favor, adicione produtos ao seu carrinho primeiro!", "error");
                return;
            }

            const clientName = document.getElementById('inputClientName').value.trim();
            const clientPhone = document.getElementById('inputClientPhone').value.trim();
            const orderType = document.getElementById('selOrderType').value;
            const deliveryAddress = document.getElementById('inputDeliveryAddress').value.trim();
            const paymentMethod = document.getElementById('selPaymentMethod').value;
            const notes = document.getElementById('inputNotes').value.trim();

            if (orderType === 'Delivery' && !deliveryAddress) {
                showToast("Por favor, indique a morada para entrega!", "error");
                return;
            }

            let subtotal = CART.reduce((acc, item) => acc + (item.price * item.quantity), 0);
            let fee = (orderType === 'Delivery') ? DELIVERY_FEE : 0.00;
            let totalAmount = subtotal + fee;

            btnSubmit.disabled = true;
            btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Enviar Pedido...';

            try {
                const resp = await fetch('/api/order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        client_name: clientName,
                        client_phone: clientPhone,
                        order_type: orderType,
                        delivery_address: deliveryAddress,
                        payment_method: paymentMethod,
                        items: CART,
                        total_amount: totalAmount,
                        notes: notes
                    })
                });

                const data = await resp.json();

                if (data.success) {
                    closeCartDrawer();
                    showReceiptModal(data.order, data.whatsapp_url);

                    // Reset cart
                    CART = [];
                    renderCart();
                    form.reset();
                } else {
                    showToast(data.message || "Erro ao processar pedido.", "error");
                }
            } catch (err) {
                console.error(err);
                showToast("Erro na ligação ao servidor.", "error");
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Finalizar Pedido via WhatsApp';
            }
        });
    }

    // Receipt Modal Closes
    const btnCloseReceipt = document.getElementById('btnCloseReceipt');
    const btnFinishReceipt = document.getElementById('btnFinishReceipt');
    const receiptModal = document.getElementById('receiptModal');

    if (btnCloseReceipt) btnCloseReceipt.onclick = () => receiptModal.classList.remove('active');
    if (btnFinishReceipt) btnFinishReceipt.onclick = () => receiptModal.classList.remove('active');
}

// Receipt Display
function showReceiptModal(order, waUrl) {
    const receiptModal = document.getElementById('receiptModal');
    const rcId = document.getElementById('rcId');
    const rcClient = document.getElementById('rcClient');
    const rcType = document.getElementById('rcType');
    const rcTotal = document.getElementById('rcTotal');
    const btnReceiptWa = document.getElementById('btnReceiptWa');

    if (rcId) rcId.textContent = order.id;
    if (rcClient) rcClient.textContent = order.client_name;
    if (rcType) rcType.textContent = `${order.order_type} (${order.delivery_address})`;
    if (rcTotal) rcTotal.textContent = `${order.total_amount.toFixed(2)} €`;
    if (btnReceiptWa) btnReceiptWa.href = waUrl;

    if (receiptModal) receiptModal.classList.add('active');
}

// Toast System
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fa-solid ${type === 'success' ? 'fa-circle-check text-green' : 'fa-circle-exclamation text-orange'}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Lightbox Modal for Full Product Image & Details
let currentProductModalData = null;
let currentModalQty = 1;

function initImageLightbox() {
    const productCards = document.querySelectorAll('.fastfood-card');
    const comboCards = document.querySelectorAll('.combo-card');
    const productModal = document.getElementById('productDetailModal');
    const btnClose = document.getElementById('btnCloseProductModal');

    if (!productModal) return;

    // Fast food menu cards
    productCards.forEach(card => {
        const imgContainer = card.querySelector('.fastfood-card-img');
        const img = card.querySelector('.fastfood-card-img img');
        const title = card.querySelector('.ff-header h3');
        const price = card.querySelector('.ff-price');
        const desc = card.querySelector('.ff-desc');
        const tag = card.querySelector('.ff-tag');
        const badge = card.querySelector('.ff-badge-top');

        if (imgContainer && title && price && desc) {
            imgContainer.addEventListener('click', () => {
                openProductLightbox({
                    title: title.textContent.trim(),
                    price: price.textContent.trim(),
                    rawPrice: parseFloat(price.textContent.replace('€', '').replace(',', '.').trim()),
                    desc: desc.textContent.trim(),
                    img: img ? img.src : '',
                    tag: tag ? tag.innerHTML : '<i class="fa-solid fa-star"></i> Produto Especial',
                    badge: badge ? badge.textContent.trim() : ''
                });
            });
        }
    });

    // Combo cards
    comboCards.forEach(card => {
        const img = card.querySelector('img');
        const title = card.querySelector('.combo-body h3');
        const price = card.querySelector('.combo-price');
        const desc = card.querySelector('.combo-body p');
        const badge = card.querySelector('.combo-badge');

        if (img && title && price && desc) {
            img.style.cursor = 'pointer';
            img.addEventListener('click', () => {
                openProductLightbox({
                    title: title.textContent.trim(),
                    price: price.textContent.trim(),
                    rawPrice: parseFloat(price.textContent.replace('€', '').replace(',', '.').trim()),
                    desc: desc.textContent.trim(),
                    img: img.src,
                    tag: '<i class="fa-solid fa-fire"></i> Combo Promocional',
                    badge: badge ? badge.textContent.trim() : 'COMBO'
                });
            });
        }
    });

    // Close handlers
    if (btnClose) btnClose.onclick = closeProductLightbox;
    productModal.addEventListener('click', (e) => {
        if (e.target === productModal) closeProductLightbox();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeProductLightbox();
            closeCartDrawer();
        }
    });
}

function openProductLightbox(data) {
    currentProductModalData = data;
    currentModalQty = 1;

    const modal = document.getElementById('productDetailModal');
    const pmImage = document.getElementById('pmImage');
    const pmBadge = document.getElementById('pmBadge');
    const pmTag = document.getElementById('pmTag');
    const pmTitle = document.getElementById('pmTitle');
    const pmPrice = document.getElementById('pmPrice');
    const pmDesc = document.getElementById('pmDesc');
    const pmQty = document.getElementById('pmQty');
    const pmAddBtn = document.getElementById('pmAddBtn');

    if (!modal) return;

    if (pmImage) pmImage.src = data.img;
    if (pmBadge) {
        if (data.badge) {
            pmBadge.textContent = data.badge;
            pmBadge.style.display = 'block';
        } else {
            pmBadge.style.display = 'none';
        }
    }
    if (pmTag) pmTag.innerHTML = data.tag;
    if (pmTitle) pmTitle.textContent = data.title;
    if (pmPrice) pmPrice.textContent = data.price;
    if (pmDesc) pmDesc.textContent = data.desc;
    if (pmQty) pmQty.textContent = currentModalQty;

    if (pmAddBtn) {
        pmAddBtn.onclick = () => {
            for (let i = 0; i < currentModalQty; i++) {
                addToCart(data.title, data.rawPrice, data.img);
            }
            closeProductLightbox();
        };
    }

    modal.classList.add('active');
}

function changeModalQty(delta) {
    currentModalQty += delta;
    if (currentModalQty < 1) currentModalQty = 1;
    const pmQty = document.getElementById('pmQty');
    if (pmQty) pmQty.textContent = currentModalQty;
}

function closeProductLightbox() {
    const modal = document.getElementById('productDetailModal');
    if (modal) modal.classList.remove('active');
}
