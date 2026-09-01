// VELOCE • LUXURY & HYPERCARS STAND — Interactive Engine

const CURRENCY_RATES = {
    EUR: { rate: 1.0, symbol: '€', prefix: false },
    GBP: { rate: 0.85, symbol: '£', prefix: true },
    USD: { rate: 1.08, symbol: '$', prefix: true }
};

let currentCurrency = 'EUR';

const CAR_SPECS = {
    bugatti_chiron: {
        title: "Bugatti Chiron Super Sport 300+",
        price: 3900000,
        desc: "Hipercarro de coleção com motor 8.0 Quad-Turbo W16, desenvolvendo 1.600 CV de potência bruta. Velocidade máxima de 440 km/h com monocoque em fibra de carbono, jantes em magnésio e escape em titânio impresso em 3D.",
        motor: "8.0L W16 Quad-Turbo (1.600 CV / 1.600 Nm)",
        gear: "7-Velocidades DSG Dupla Embraiagem",
        accel: "2,4 Segundos (0-100 km/h)",
        accel200: "5,8 Segundos (0-200 km/h)",
        images: [
            "/static/images/bugatti_chiron.jpg",
            "/static/images/interior_cockpit.jpg",
            "/static/images/engine_v12.jpg"
        ]
    },
    ferrari_sf90: {
        title: "Ferrari SF90 XX Stradale Hybrid",
        price: 980000,
        desc: "O primeiro modelo XX homologado para estrada na história da Ferrari. Motor V8 Twin-Turbo associado a 3 motores elétricos, totalizando 1.030 CV com aerodinâmica ativa derivada da Fórmula 1.",
        motor: "4.0L V8 Twin-Turbo + 3 Motores Elétricos (1.030 CV)",
        gear: "8-Velocidades F1 Dual-Clutch",
        accel: "2,3 Segundos (0-100 km/h)",
        accel200: "6,5 Segundos (0-200 km/h)",
        images: [
            "/static/images/ferrari_sf90.jpg",
            "/static/images/interior_cockpit.jpg",
            "/static/images/engine_v12.jpg"
        ]
    },
    lambo_revuelto: {
        title: "Lamborghini Revuelto V12 Hybrid",
        price: 740000,
        desc: "O novo barco insígnia de Sant'Agata Bolognese. Motor V12 atmosférico de 6.5 litros combinado com sistema HPEV híbrido de 3 motores elétricos e chassi Monofusione em fibra de carbono.",
        motor: "6.5L V12 Atmosférico + 3 Motores Elétricos (1.015 CV)",
        gear: "8-Velocidades Dupla Embraiagem Transversal",
        accel: "2,5 Segundos (0-100 km/h)",
        accel200: "7,0 Segundos (0-200 km/h)",
        images: [
            "/static/images/lambo_revuelto.jpg",
            "/static/images/interior_cockpit.jpg",
            "/static/images/engine_v12.jpg"
        ]
    },
    rolls_cullinan: {
        title: "Rolls-Royce Cullinan Black Badge",
        price: 580000,
        desc: "O pináculo do luxo em formato SUV. Edição Black Badge com detalhes em crómio negro, motor V12 Twin-Turbo otimizado para 600 CV, teto Starlight com estrelas cadentes em fibra ótica e suspensão a ar Magic Carpet Ride.",
        motor: "6.75L V12 Twin-Turbo (600 CV / 900 Nm)",
        gear: "8-Velocidades ZF Automática com Navegação Satélite",
        accel: "4,9 Segundos (0-100 km/h)",
        accel200: "Velocidade Máx. 250 km/h (Limitada)",
        images: [
            "/static/images/rolls_cullinan.jpg",
            "/static/images/interior_cockpit.jpg"
        ]
    },
    aston_dbs: {
        title: "Aston Martin DBS 770 Ultimate",
        price: 490000,
        desc: "A edição de despedida mais potente de sempre do lendário DBS. Produção limitada a apenas 499 unidades no mundo com motor V12 Twin-Turbo de 770 CV e elementos aerodinâmicos em carbono visível.",
        motor: "5.2L V12 Twin-Turbo (770 CV / 900 Nm)",
        gear: "8-Velocidades ZF Automática Calibrada",
        accel: "3,2 Segundos (0-100 km/h)",
        accel200: "Velocidade Máx. 340 km/h",
        images: [
            "/static/images/aston_dbs.jpg",
            "/static/images/interior_cockpit.jpg"
        ]
    },
    amg_gt_black: {
        title: "Mercedes-AMG GT Black Series",
        price: 450000,
        desc: "Campeão de Nürburgring com motor V8 Flat-Plane Crank de 730 CV. Asa traseira de fibra de carbono com flap ajustável eletronicamente e suspensão coilover ajustável para pista.",
        motor: "4.0L V8 Biturbo Flat-Plane (730 CV / 800 Nm)",
        gear: "7-Velocidades AMG SPEEDSHIFT DCT",
        accel: "3,2 Segundos (0-100 km/h)",
        accel200: "9,0 Segundos (0-200 km/h)",
        images: [
            "/static/images/amg_gt_black.jpg",
            "/static/images/interior_cockpit.jpg",
            "/static/images/engine_v12.jpg"
        ]
    },
    maserati_mc20: {
        title: "Maserati MC20 Cielo Spyder",
        price: 340000,
        desc: "Superdesportivo descapotável italiano equipado com o revolucionário motor V6 Nettuno com tecnologia de pré-câmara derivada da Fórmula 1 e teto de vidro eletrocromático inteligente.",
        motor: "3.0L V6 Nettuno Twin-Turbo F1 Tech (630 CV)",
        gear: "8-Velocidades Dual-Clutch",
        accel: "2,9 Segundos (0-100 km/h)",
        accel200: "Velocidade Máx. 320 km/h",
        images: [
            "/static/images/maserati_mc20.jpg",
            "/static/images/interior_cockpit.jpg"
        ]
    },
    bmw_m8: {
        title: "BMW M8 Competition Gran Coupé",
        price: 195000,
        desc: "O topo de gama da divisão M da BMW. Motor 4.4 V8 TwinPower Turbo de 625 CV com tração integral M xDrive inteligente e travões carbo-cerâmicos de alto rendimento.",
        motor: "4.4L V8 TwinPower Turbo (625 CV / 750 Nm)",
        gear: "8-Velocidades M Steptronic com Drivelogic",
        accel: "3,2 Segundos (0-100 km/h)",
        accel200: "Velocidade Máx. 305 km/h (M Driver's Package)",
        images: [
            "/static/images/bmw_m8.jpg",
            "/static/images/interior_cockpit.jpg"
        ]
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initVipForm();
});

// Supercar Filter Engine
function applyCarFilters() {
    const brandVal = document.getElementById('filterBrand').value;
    const priceVal = document.getElementById('filterPrice').value;
    const catVal = document.getElementById('filterCategory').value;
    const kmVal = document.getElementById('filterKm').value;

    const cards = document.querySelectorAll('.car-card-luxury');

    cards.forEach(card => {
        const brand = card.getAttribute('data-brand');
        const price = parseFloat(card.getAttribute('data-price'));
        const cat = card.getAttribute('data-cat');
        const km = parseInt(card.getAttribute('data-km'));

        let matchBrand = (brandVal === 'all' || brand === brandVal);
        let matchCat = (catVal === 'all' || cat === catVal);

        // Price Filter
        let matchPrice = true;
        if (priceVal === '150-400') matchPrice = (price >= 150000 && price <= 400000);
        else if (priceVal === '400-800') matchPrice = (price > 400000 && price <= 800000);
        else if (priceVal === '800+') matchPrice = (price > 800000);

        // Mileage Filter
        let matchKm = true;
        if (kmVal === '0') matchKm = (km === 0);
        else if (kmVal === 'under5k') matchKm = (km <= 5000);
        else if (kmVal === 'collection') matchKm = (km > 0);

        if (matchBrand && matchPrice && matchCat && matchKm) {
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

    const priceTags = document.querySelectorAll('.car-price-tag');
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

// Lightbox Spec Sheet Engine
function openLightbox(carKey) {
    const spec = CAR_SPECS[carKey];
    if (!spec) return;

    const modal = document.getElementById('lightboxModal');
    const mainImg = document.getElementById('lightboxMainImage');
    const titleEl = document.getElementById('lightboxTitle');
    const priceEl = document.getElementById('lightboxPrice');
    const descEl = document.getElementById('lightboxDesc');
    const motorEl = document.getElementById('specMotor');
    const gearEl = document.getElementById('specGear');
    const accelEl = document.getElementById('specAccel');
    const accel200El = document.getElementById('spec0200');
    const thumbsStrip = document.querySelector('.lightbox-thumbs-strip');

    if (titleEl) titleEl.textContent = spec.title;
    if (descEl) descEl.textContent = spec.desc;
    if (motorEl) motorEl.textContent = spec.motor;
    if (gearEl) gearEl.textContent = spec.gear;
    if (accelEl) accelEl.textContent = spec.accel;
    if (accel200El) accel200El.textContent = spec.accel200;

    if (priceEl) {
        priceEl.setAttribute('data-eur', spec.price);
        priceEl.textContent = formatCurrencyValue(spec.price, currentCurrency);
    }

    if (mainImg && spec.images.length > 0) {
        mainImg.src = spec.images[0];
    }

    // Build Thumbnail Strip
    if (thumbsStrip) {
        thumbsStrip.innerHTML = '';
        spec.images.forEach((imgSrc, idx) => {
            const thumb = document.createElement('img');
            thumb.src = imgSrc;
            thumb.className = `lightbox-thumb ${idx === 0 ? 'active' : ''}`;
            thumb.onclick = () => switchLightboxImage(imgSrc, thumb);
            thumbsStrip.appendChild(thumb);
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

// VIP Booking & Form Modal Engine
function openVipModal(carModel = "Consulta Geral Veloce Motors") {
    const modal = document.getElementById('vipModal');
    const targetInput = document.getElementById('vipTargetCar');

    if (targetInput) targetInput.value = carModel;
    if (modal) modal.classList.add('active');
}

function openVipModalFromLightbox() {
    closeLightbox();
    const titleEl = document.getElementById('lightboxTitle');
    const title = titleEl ? titleEl.textContent : "Consulta Geral Veloce Motors";
    openVipModal(title);
}

function closeVipModal() {
    const modal = document.getElementById('vipModal');
    if (modal) modal.classList.remove('active');
}

function initVipForm() {
    const form = document.getElementById('vipInquiryForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const carModel = document.getElementById('vipTargetCar').value;
        const fullName = document.getElementById('vipFullName').value.trim();
        const phone = document.getElementById('vipPhone').value.trim();
        const email = document.getElementById('vipEmail').value.trim();
        const inquiryType = document.getElementById('vipInquiryType').value;
        const hasTradeIn = document.getElementById('vipHasTradeIn').value;

        const btn = document.getElementById('btnSubmitVipForm');
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A Processar Solicitação VIP...';

        try {
            const resp = await fetch('/api/inquiry-car', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    car_model: carModel,
                    full_name: fullName,
                    phone: phone,
                    email: email,
                    inquiry_type: inquiryType,
                    has_trade_in: hasTradeIn
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
            btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Enviar Solicitação no WhatsApp';
        }
    });
}
