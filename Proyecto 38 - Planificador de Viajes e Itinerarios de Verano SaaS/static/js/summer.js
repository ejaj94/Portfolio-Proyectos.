// SUNSET TRAVEL SaaS - Client-Side Interactive Logic

document.addEventListener('DOMContentLoaded', () => {
    initBudgetChart();
});

function initBudgetChart() {
    const chartCanvas = document.getElementById('budgetChart');
    if (!chartCanvas) return;

    const tripId = chartCanvas.dataset.tripId;
    if (!tripId) return;

    fetch(`/api/trips/${tripId}/budget`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.categories.length > 0) {
                renderChart(chartCanvas, data.categories);
            } else {
                renderEmptyChartMessage(chartCanvas);
            }
        })
        .catch(err => {
            console.error('Erro ao carregar gráfico de orçamento:', err);
        });
}

function renderChart(canvas, categories) {
    const labels = categories.map(c => c.category);
    const dataValues = categories.map(c => c.total);

    const colorsMap = {
        'Voo': '#3b82f6',
        'Hotel': '#a855f7',
        'Restaurante': '#f59e0b',
        'Atividade': '#ff5722',
        'Transporte': '#10b981',
        'Outro': '#6b7280'
    };

    const bgColors = labels.map(l => colorsMap[l] || '#ff7a59');

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dataValues,
                backgroundColor: bgColors,
                borderColor: '#120914',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#fff3e0',
                        font: {
                            family: 'Plus Jakarta Sans',
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.label}: ${context.raw.toFixed(2)} €`;
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });
}

function renderEmptyChartMessage(canvas) {
    const ctx = canvas.getContext('2d');
    ctx.font = '14px Plus Jakarta Sans';
    ctx.fillStyle = '#ff7a59';
    ctx.textAlign = 'center';
    ctx.fillText('Sem despesas registadas no itinerário', canvas.width / 2, canvas.height / 2);
}

function copyTripSummary() {
    const tripTitle = document.getElementById('tripTitleText')?.innerText || 'A minha viagem de Verão';
    const currentUrl = window.location.href;
    const textToCopy = `✈️ Descobre a minha viagem de Verão "${tripTitle}" planeada no SUNSET TRAVEL:\n${currentUrl}\n\nDesenvolvido pela EJAJ TECH - Contacta-nos com a palavra "AJUDA" no WhatsApp +351 911 151 993!`;

    navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Copiaste o resumo da viagem para a área de transferência! 🚀');
    }).catch(err => {
        console.error('Erro ao copiar:', err);
    });
}
