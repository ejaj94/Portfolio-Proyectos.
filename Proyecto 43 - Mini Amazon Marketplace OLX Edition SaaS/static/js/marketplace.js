// OLX-MARKETPLACE SaaS - Client Interactivity

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
        toast.style.borderColor = '#FF5636';
    }
    toast.innerHTML = `<span style="color: var(--olx-mint);">${isError ? '⚠️' : '🛍️'}</span> <div>${message}</div>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3500);
}

// Add to Cart
async function addToCart(productId, qty = 1) {
    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: qty })
        });
        
        const res = await response.json();
        if (res.success) {
            showToast(res.message);
            // Update cart counter badges
            const badges = document.querySelectorAll('.cart-badge');
            badges.forEach(b => {
                b.textContent = res.cart_count;
                b.style.display = res.cart_count > 0 ? 'inline-flex' : 'none';
            });
        } else {
            showToast('Erro ao adicionar ao carrinho', true);
        }
    } catch (err) {
        showToast('Falha na comunicação com o servidor', true);
    }
}

// Remove Item from Cart
async function removeFromCart(cartId) {
    try {
        const response = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cart_id: cartId })
        });
        
        const res = await response.json();
        if (res.success) {
            showToast(res.message);
            setTimeout(() => window.location.reload(), 800);
        }
    } catch (err) {
        showToast('Erro ao remover produto', true);
    }
}

// Process Checkout
document.addEventListener('DOMContentLoaded', () => {
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const method = document.getElementById('paymentMethodSelect').value;
            const address = document.getElementById('shippingAddressInput').value;
            const phone = document.getElementById('phoneMbwayInput') ? document.getElementById('phoneMbwayInput').value : '';
            
            try {
                const response = await fetch('/api/checkout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        payment_method: method,
                        shipping_address: address,
                        phone_mbway: phone
                    })
                });
                
                const res = await response.json();
                if (res.success) {
                    showToast(res.message);
                    setTimeout(() => {
                        window.location.href = '/orders';
                    }, 1200);
                } else {
                    showToast(res.message || 'Erro ao concluir encomenda', true);
                }
            } catch (err) {
                showToast('Erro ao processar encomenda', true);
            }
        });
    }

    // New Product Creation (Seller)
    const newProductForm = document.getElementById('newProductForm');
    if (newProductForm) {
        newProductForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const title = document.getElementById('titleInput').value;
            const description = document.getElementById('descInput').value;
            const price = document.getElementById('priceInput').value;
            const category = document.getElementById('categorySelect').value;
            const condition = document.getElementById('conditionSelect').value;
            const imageUrl = document.getElementById('imageInput').value;
            const stock = document.getElementById('stockInput').value;
            const location = document.getElementById('locationInput').value;
            
            try {
                const response = await fetch('/api/products/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title, description, price, category, condition, image_url: imageUrl, stock, location
                    })
                });
                
                const res = await response.json();
                if (res.success) {
                    showToast(res.message);
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast(res.message || 'Erro ao publicar anúncio', true);
                }
            } catch (err) {
                showToast('Erro na ligação com o servidor', true);
            }
        });
    }
});
