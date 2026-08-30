document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const cryptoGrid = document.getElementById('cryptoGrid');
    const forexGrid = document.getElementById('forexGrid');
    const customSymbolInput = document.getElementById('customSymbolInput');
    const btnAddCustomSymbol = document.getElementById('btnAddCustomSymbol');

    // Converter Elements
    const calcAmount = document.getElementById('calcAmount');
    const calcSymbol = document.getElementById('calcSymbol');
    const calcResultDisplay = document.getElementById('calcResultDisplay');

    // Alerts Elements
    const alertSymbol = document.getElementById('alertSymbol');
    const alertCondition = document.getElementById('alertCondition');
    const alertTargetPrice = document.getElementById('alertTargetPrice');
    const btnCreateAlert = document.getElementById('btnCreateAlert');
    const alertsList = document.getElementById('alertsList');
    const alertCountBadge = document.getElementById('alertCountBadge');

    // Modal Elements
    const chartModal = document.getElementById('chartModal');
    const btnCloseModal = document.getElementById('btnCloseModal');
    const modalChartTitle = document.getElementById('modalChartTitle');
    const priceChartCanvas = document.getElementById('priceChartCanvas');

    let activeAlerts = [];
    let currentChartInstance = null;
    let currentModalSymbol = 'BTC-USD';
    let currentModalPeriod = '1d';
    let previousPricesMap = {};
    let latestPricesMap = {};

    // 1. Manejo de Pestañas
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            const target = btn.getAttribute('data-tab');
            document.getElementById(target).classList.add('active');
        });
    });

    // 2. Fetch de Precios en Tiempo Real
    async function fetchLivePrices() {
        try {
            const res = await fetch('/api/prices');
            const data = await res.json();
            if (data.success) {
                renderGrid(cryptoGrid, data.cryptos);
                renderGrid(forexGrid, data.forex);

                // Guardar mapa de precios anteriores y actuales
                data.cryptos.concat(data.forex).forEach(item => {
                    if (item.price > 0) {
                        previousPricesMap[item.symbol] = latestPricesMap[item.symbol] || item.price;
                        latestPricesMap[item.symbol] = item.price;
                    }
                });

                evaluateAlerts();
                updateConverter();
            }
        } catch (err) {
            console.error('Error al actualizar cotizaciones:', err);
        }
    }

    function renderGrid(container, items) {
        if (!items || items.length === 0) return;

        items.forEach(item => {
            if (!item.price || item.price <= 0) return;

            const existingCard = container.querySelector(`[data-card-symbol="${item.symbol}"]`);
            const prevPrice = previousPricesMap[item.symbol] || item.price;
            let flashClass = '';

            if (item.price > prevPrice) flashClass = 'flash-up';
            else if (item.price < prevPrice) flashClass = 'flash-down';

            const isUp = item.change >= 0;
            const changeClass = isUp ? 'up' : 'down';
            const changeIcon = isUp ? 'fa-caret-up' : 'fa-caret-down';
            const sign = isUp ? '+' : '';

            const isForex = item.symbol.includes('=X');
            const formattedPrice = isForex ? `$${item.price.toFixed(4)}` : `$${item.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

            const cardHTML = `
                <div class="ticker-card-top">
                    <div class="symbol-name-box">
                        <span class="symbol-tag">${item.symbol}</span>
                        <span class="friendly-name">${item.name}</span>
                    </div>
                    <span class="badge-change ${changeClass}">
                        <i class="fa-solid ${changeIcon}"></i> ${sign}${item.change_pct}%
                    </span>
                </div>
                <div class="ticker-price-box">
                    <span class="price-value">${formattedPrice}</span>
                </div>
                <div class="ticker-details-row">
                    <span>Máx: $${item.high || 0}</span>
                    <span>Mín: $${item.low || 0}</span>
                    <span>${item.timestamp}</span>
                </div>
                <div class="ticker-card-actions">
                    <button class="btn btn-sm btn-outline btn-view-chart" data-symbol="${item.symbol}">
                        <i class="fa-solid fa-chart-line"></i> Ver Gráfico
                    </button>
                </div>
            `;

            if (existingCard) {
                existingCard.className = `ticker-card ${flashClass}`;
                existingCard.innerHTML = cardHTML;
                setTimeout(() => existingCard.classList.remove('flash-up', 'flash-down'), 800);
            } else {
                const card = document.createElement('div');
                card.className = `ticker-card ${flashClass}`;
                card.setAttribute('data-card-symbol', item.symbol);
                card.innerHTML = cardHTML;
                container.appendChild(card);
            }
        });

        // Limpiar skeleton loader si existe
        const skeleton = container.querySelector('.skeleton-card');
        if (skeleton) skeleton.remove();

        // Event listeners para botones de gráfico
        container.querySelectorAll('.btn-view-chart').forEach(btn => {
            btn.onclick = () => {
                const sym = btn.getAttribute('data-symbol');
                openChartModal(sym);
            };
        });
    }

    // 3. Agregar Ticker Personalizado
    btnAddCustomSymbol.addEventListener('click', async () => {
        const symbol = customSymbolInput.value.trim().toUpperCase();
        if (!symbol) return showToast('Escribe un símbolo válido.', 'error');

        try {
            const res = await fetch('/api/custom-price', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol: symbol })
            });

            const json = await res.json();
            if (json.success) {
                showToast(`Activo ${symbol} agregado!`, 'success');
                customSymbolInput.value = '';
                fetchLivePrices();
            } else {
                showToast(json.message || 'Símbolo no encontrado.', 'error');
            }
        } catch (err) {
            showToast('Error al consultar símbolo.', 'error');
        }
    });

    // 4. Modal de Gráficos Interactivos
    async function openChartModal(symbol, period = '1d') {
        currentModalSymbol = symbol;
        currentModalPeriod = period;
        modalChartTitle.innerHTML = `<i class="fa-solid fa-chart-area"></i> Gráfico de Tendencia: ${symbol}`;
        chartModal.classList.remove('hidden');

        try {
            const res = await fetch(`/api/history/${encodeURIComponent(symbol)}?period=${period}`);
            const json = await res.json();

            if (json.success) {
                renderChart(json.labels, json.prices, symbol);
            } else {
                showToast('No se pudieron obtener datos del gráfico.', 'error');
            }
        } catch (err) {
            console.error('Error al cargar historial:', err);
        }
    }

    function renderChart(labels, dataPrices, symbol) {
        const ctx = priceChartCanvas.getContext('2d');
        if (currentChartInstance) {
            currentChartInstance.destroy();
        }

        const isPositive = dataPrices.length > 1 && dataPrices[dataPrices.length - 1] >= dataPrices[0];
        const lineColor = isPositive ? '#00ff66' : '#ff007f';
        const bgGradient = ctx.createLinearGradient(0, 0, 0, 320);
        bgGradient.addColorStop(0, isPositive ? 'rgba(0, 255, 102, 0.35)' : 'rgba(255, 0, 127, 0.35)');
        bgGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

        currentChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `Precio (${symbol})`,
                    data: dataPrices,
                    borderColor: lineColor,
                    borderWidth: 2.5,
                    fill: true,
                    backgroundColor: bgGradient,
                    tension: 0.25,
                    pointRadius: 0,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#a0a5c0', font: { size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#a0a5c0', font: { size: 10 } }
                    }
                }
            }
        });
    }

    btnCloseModal.addEventListener('click', () => {
        chartModal.classList.add('hidden');
    });

    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const period = btn.getAttribute('data-period');
            openChartModal(currentModalSymbol, period);
        });
    });

    // 5. Calculadora de Conversión
    function updateConverter() {
        const amt = parseFloat(calcAmount.value) || 0;
        const sym = calcSymbol.value;
        const currentPrice = latestPricesMap[sym] || 0;

        const total = amt * currentPrice;
        calcResultDisplay.textContent = `$${total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    calcAmount.addEventListener('input', updateConverter);
    calcSymbol.addEventListener('change', updateConverter);

    // 6. Alertas de Precio
    btnCreateAlert.addEventListener('click', () => {
        const sym = alertSymbol.value;
        const cond = alertCondition.value;
        const target = parseFloat(alertTargetPrice.value);

        if (!target || target <= 0) {
            return showToast('Ingresa un precio objetivo válido.', 'error');
        }

        const alertItem = {
            id: Date.now(),
            symbol: sym,
            condition: cond,
            targetPrice: target
        };

        activeAlerts.push(alertItem);
        renderAlertsList();
        showToast(`Alerta configurada para ${sym} (${cond === 'above' ? '>' : '<'} $${target})`, 'success');
        alertTargetPrice.value = '';
    });

    function renderAlertsList() {
        alertCountBadge.textContent = activeAlerts.length;
        if (activeAlerts.length === 0) {
            alertsList.innerHTML = '<li class="empty-list">No hay alertas configuradas.</li>';
            return;
        }

        alertsList.innerHTML = '';
        activeAlerts.forEach(al => {
            const li = document.createElement('li');
            li.style.display = 'flex';
            li.style.justifyContent = 'space-between';
            li.style.padding = '10px 14px';
            li.style.borderBottom = '1px solid rgba(255, 255, 255, 0.06)';
            li.innerHTML = `
                <span><strong>${al.symbol}</strong> ${al.condition === 'above' ? '>' : '<'} $${al.targetPrice}</span>
                <button class="btn btn-sm btn-outline btn-delete-alert" data-id="${al.id}" style="color: #ff007f; border-color: #ff007f;">
                    <i class="fa-solid fa-trash"></i>
                </button>
            `;
            alertsList.appendChild(li);
        });

        alertsList.querySelectorAll('.btn-delete-alert').forEach(b => {
            b.onclick = () => {
                const id = parseInt(b.getAttribute('data-id'));
                activeAlerts = activeAlerts.filter(a => a.id !== id);
                renderAlertsList();
            };
        });
    }

    function evaluateAlerts() {
        activeAlerts.forEach((al, index) => {
            const livePrice = latestPricesMap[al.symbol];
            if (!livePrice || livePrice <= 0) return;

            let triggered = false;
            if (al.condition === 'above' && livePrice >= al.targetPrice) triggered = true;
            if (al.condition === 'below' && livePrice <= al.targetPrice) triggered = true;

            if (triggered) {
                showToast(`🚨 ¡ALERTA DISPARADA! ${al.symbol} está a $${livePrice} (Objetivo: $${al.targetPrice})`, 'error');
                activeAlerts.splice(index, 1);
                renderAlertsList();
            }
        });
    }

    // Helper Toast
    function showToast(msg, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = 'fa-circle-info';
        if (type === 'success') icon = 'fa-circle-check';
        if (type === 'error') icon = 'fa-triangle-exclamation';

        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${msg}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // Loop de Actualización Automática (3 segundos)
    fetchLivePrices();
    setInterval(fetchLivePrices, 3000);
});
