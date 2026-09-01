// VALE DO LOBO • LUXURY REAL ESTATE — Interactive Engine

const CURRENCY_RATES = {
    EUR: { rate: 1.0, symbol: '€', prefix: false },
    GBP: { rate: 0.85, symbol: '£', prefix: true },
    USD: { rate: 1.08, symbol: '$', prefix: true }
};

let currentCurrency = 'EUR';

const PROPERTY_GALLERIES = {
    villa_ocean_cliff: {
        title: "Villa Ocean Cliff Palace",
        price: 14500000,
        desc: "Esta deslumbrante mansão contemporânea ergue-se no topo das falésias de Vale do Lobo, oferecendo vistas ininterruptas de 180º sobre o Oceano Atlântico. Inclui piscina de bordo infinito aquecida, sauna em pedra natural e acabamentos em mármore de Carrara.",
        images: [
            "/static/images/villa_ocean_cliff.jpg",
            "/static/images/interior_living.jpg",
            "/static/images/interior_suite.jpg",
            "/static/images/pool_sunset.jpg"
        ]
    },
    villa_royal_golf: {
        title: "Mansão Royal Golf Estate",
        price: 8900000,
        desc: "Localizada em primeira linha do prestigiado Royal Golf Course, esta propriedade alia a privacidade absoluta de um bosque de pinheiros com uma arquitetura neoclássica refinada. Dispõe de cave de vinhos climatizada e spa privativo.",
        images: [
            "/static/images/villa_royal_golf.jpg",
            "/static/images/interior_living.jpg",
            "/static/images/pool_sunset.jpg"
        ]
    },
    palacio_atlantico: {
        title: "Palácio Atlântico Vale do Lobo",
        price: 18200000,
        desc: "Uma autêntica obra-prima da arquitetura moderna no Algarve. Situada num lote privativo de 4.500 m² com acesso exclusivo à praia através de um trilho nas falésias. Conta com heliporto certificado e 7 suites master.",
        images: [
            "/static/images/palacio_atlantico.jpg",
            "/static/images/interior_suite.jpg",
            "/static/images/interior_living.jpg",
            "/static/images/pool_sunset.jpg"
        ]
    },
    villa_sunset_haven: {
        title: "Villa Sunset Haven",
        price: 6800000,
        desc: "Desenhada para capturar o pôr do sol inesquecível de Vale do Lobo. Amplos janelões de vidro do chão ao teto, cozinha de chef equipada com Miele e terraço panorâmico com lareira exterior.",
        images: [
            "/static/images/villa_sunset_haven.jpg",
            "/static/images/interior_living.jpg",
            "/static/images/pool_sunset.jpg"
        ]
    },
    mansion_pine_crest: {
        title: "Mansão Pine Crest Golf",
        price: 5400000,
        desc: "Um refúgio de serenidade envolto pela natureza mediterrânica. Possui campo de ténis privativo, jardim tropical irrigado com água nascente e garagem subterrânea para 5 viaturas.",
        images: [
            "/static/images/mansion_pine_crest.jpg",
            "/static/images/interior_suite.jpg",
            "/static/images/pool_sunset.jpg"
        ]
    },
    villa_infinity_cliff: {
        title: "Villa Infinity Cliff Resort",
        price: 11200000,
        desc: "Residência ultra-tecnológica equipada com domótica integral 2026. Duas piscinas de bordo infinito (uma delas interior aquecida), cinema 4K privativo e elevador em vidro.",
        images: [
            "/static/images/villa_infinity_cliff.jpg",
            "/static/images/interior_living.jpg",
            "/static/images/interior_suite.jpg"
        ]
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initVipForm();
});

// Property Filter Engine
function applyPropertyFilters() {
    const typeVal = document.getElementById('filterType').value;
    const priceVal = document.getElementById('filterPrice').value;
    const bedsVal = document.getElementById('filterBeds').value;
    const locationVal = document.getElementById('filterLocation').value;

    const cards = document.querySelectorAll('.property-card-luxury');

    cards.forEach(card => {
        const type = card.getAttribute('data-type');
        const price = parseFloat(card.getAttribute('data-price'));
        const beds = parseInt(card.getAttribute('data-beds'));
        const location = card.getAttribute('data-location');

        let matchType = (typeVal === 'all' || type === typeVal);
        let matchLocation = (locationVal === 'all' || location === locationVal);

        // Match Price Range
        let matchPrice = true;
        if (priceVal === '5-8') matchPrice = (price >= 5000000 && price <= 8000000);
        else if (priceVal === '8-12') matchPrice = (price > 8000000 && price <= 12000000);
        else if (priceVal === '12+') matchPrice = (price > 12000000);

        // Match Beds
        let matchBeds = true;
        if (bedsVal === '4') matchBeds = (beds === 4);
        else if (bedsVal === '5') matchBeds = (beds === 5);
        else if (bedsVal === '6+') matchBeds = (beds >= 6);

        if (matchType && matchPrice && matchBeds && matchLocation) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// Currency Switcher Engine
function changeCurrency(currencyCode) {
    if (!CURRENCY_RATES[currencyCode]) return;
    currentCurrency = currencyCode;

    const priceTags = document.querySelectorAll('.property-price-tag');
    priceTags.forEach(tag => {
        const eurVal = parseFloat(tag.getAttribute('data-eur'));
        tag.textContent = formatCurrencyValue(eurVal, currencyCode);
    });

    // Update Lightbox price if open
    const lightboxPriceEl = document.getElementById('lightboxPrice');
    if (lightboxPriceEl && lightboxPriceEl.getAttribute('data-eur')) {
        const eurVal = parseFloat(lightboxPriceEl.getAttribute('data-eur'));
        lightboxPriceEl.textContent = formatCurrencyValue(eurVal, currencyCode);
    }
}

function formatCurrencyValue(eurAmount, currencyCode) {
    const config = CURRENCY_RATES[currencyCode];
    const converted = eurAmount * config.rate;
    const formattedNum = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 0 }).format(converted);

    if (config.prefix) {
        return `${config.symbol} ${formattedNum}`;
    } else {
        return `${formattedNum} ${config.symbol}`;
    }
}

// Lightbox Fullscreen Modal Engine
let currentLightboxPropertyKey = null;

function openLightbox(propertyKey) {
    const prop = PROPERTY_GALLERIES[propertyKey];
    if (!prop) return;

    currentLightboxPropertyKey = propertyKey;

    const modal = document.getElementById('lightboxModal');
    const mainImg = document.getElementById('lightboxMainImage');
    const titleEl = document.getElementById('lightboxTitle');
    const priceEl = document.getElementById('lightboxPrice');
    const descEl = document.getElementById('lightboxDesc');
    const thumbsRow = document.querySelector('.lightbox-thumbs-row');

    if (titleEl) titleEl.textContent = prop.title;
    if (descEl) descEl.textContent = prop.desc;
    if (priceEl) {
        priceEl.setAttribute('data-eur', prop.price);
        priceEl.textContent = formatCurrencyValue(prop.price, currentCurrency);
    }

    if (mainImg && prop.images.length > 0) {
        mainImg.src = prop.images[0];
    }

    // Build Thumbnail Strip
    if (thumbsRow) {
        thumbsRow.innerHTML = '';
        prop.images.forEach((imgSrc, idx) => {
            const thumb = document.createElement('img');
            thumb.src = imgSrc;
            thumb.className = `lightbox-thumb ${idx === 0 ? 'active' : ''}`;
            thumb.onclick = () => switchLightboxImage(imgSrc, thumb);
            thumbsRow.appendChild(thumb);
        });
    }

    if (modal) modal.classList.add('active');
}

function switchLightboxImage(srcUrl, clickedThumb = null) {
    const mainImg = document.getElementById('lightboxMainImage');
    if (mainImg) mainImg.src = srcUrl;

    if (clickedThumb) {
        const allThumbs = document.querySelectorAll('.lightbox-thumb');
        allThumbs.forEach(t => t.classList.remove('active'));
        clickedThumb.classList.add('active');
    }
}

function closeLightbox() {
    const modal = document.getElementById('lightboxModal');
    if (modal) modal.classList.remove('active');
}

// VIP Contact Modal Engine
function openVipModal(propertyTitle = "Consulta Geral Vale do Lobo") {
    const modal = document.getElementById('vipContactModal');
    const targetInput = document.getElementById('vipTargetProperty');

    if (targetInput) targetInput.value = propertyTitle;
    if (modal) modal.classList.add('active');
}

function openVipModalFromLightbox() {
    closeLightbox();
    const titleEl = document.getElementById('lightboxTitle');
    const title = titleEl ? titleEl.textContent : "Consulta Geral Vale do Lobo";
    openVipModal(title);
}

function closeVipModal() {
    const modal = document.getElementById('vipContactModal');
    if (modal) modal.classList.remove('active');
}

function initVipForm() {
    const form = document.getElementById('vipInquiryForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const propertyTitle = document.getElementById('vipTargetProperty').value;
        const fullName = document.getElementById('vipFullName').value.trim();
        const phone = document.getElementById('vipPhone').value.trim();
        const email = document.getElementById('vipEmail').value.trim();
        const preferredDate = document.getElementById('vipPreferredDate').value;
        const notes = document.getElementById('vipNotes').value.trim();

        const btn = document.getElementById('btnSubmitVipForm');
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Processar Solicitação VIP...';

        try {
            const resp = await fetch('/api/contact-vip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    property_title: propertyTitle,
                    full_name: fullName,
                    phone: phone,
                    email: email,
                    preferred_date: preferredDate,
                    notes: notes
                })
            });
            const data = await resp.json();

            if (data.success) {
                closeVipModal();
                form.reset();
                setTimeout(() => {
                    window.open(data.whatsapp_url, '_blank');
                }, 500);
            } else {
                alert(data.message || "Erro ao enviar solicitação.");
            }
        } catch (err) {
            console.error(err);
            alert("Erro de ligação ao servidor.");
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Solicitar Dossier via WhatsApp';
        }
    });
}
