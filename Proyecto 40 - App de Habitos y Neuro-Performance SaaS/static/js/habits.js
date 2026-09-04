// MINDHABIT SaaS - Client Side Interactive Logic

document.addEventListener('DOMContentLoaded', () => {
    initAnalyticsCharts();
});

function toggleHabit(habitId) {
    const checkEl = document.getElementById(`check-${habitId}`);
    const cardEl = document.getElementById(`habit-card-${habitId}`);
    const streakEl = document.getElementById(`streak-${habitId}`);

    fetch('/api/habits/toggle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ habit_id: habitId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            if (data.completed_today === 1) {
                checkEl.classList.add('checked');
                checkEl.innerHTML = '<i class="fa-solid fa-check text-white"></i>';
                cardEl.classList.add('border-success');
            } else {
                checkEl.classList.remove('checked');
                checkEl.innerHTML = '';
                cardEl.classList.remove('border-success');
            }

            if (streakEl) {
                streakEl.innerText = `${data.current_streak} dias`;
            }

            const rateEl = document.getElementById('globalRateText');
            const rateBar = document.getElementById('globalRateBar');
            if (rateEl && rateBar) {
                rateEl.innerText = `${data.completion_rate}%`;
                rateBar.style.width = `${data.completion_rate}%`;
            }

            showToast('🔥 ' + data.message, 'success');
        }
    })
    .catch(err => {
        console.error('Erro ao atualizar hábito:', err);
    });
}

function updateGoalProgress(goalId, stepVal = 1) {
    fetch('/api/goals/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ goal_id: goalId, add_value: stepVal })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(err => console.error(err));
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
    toastEl.className = 'toast align-items-center show glass-card border-0 text-white p-2 mb-2 shadow-lg';
    toastEl.role = 'alert';
    toastEl.innerHTML = `
        <div class="d-flex align-items-center justify-content-between">
            <div class="toast-body fw-bold">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;

    container.appendChild(toastEl);
    setTimeout(() => {
        if (toastEl) toastEl.remove();
    }, 4000);
}

function initAnalyticsCharts() {
    // Chart 1: Trend Bar Chart
    const trendCanvas = document.getElementById('weeklyTrendChart');
    if (trendCanvas) {
        const trendData = JSON.parse(trendCanvas.dataset.trend || '[]');
        const labels = trendData.map(t => t.day);
        const values = trendData.map(t => t.count);

        new Chart(trendCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Hábitos Concluídos',
                    data: values,
                    backgroundColor: 'rgba(16, 185, 129, 0.85)',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }

    // Chart 2: Category Doughnut Chart
    const catCanvas = document.getElementById('categoryChart');
    if (catCanvas) {
        const catData = JSON.parse(catCanvas.dataset.categories || '[]');
        const labels = catData.map(c => c.category);
        const values = catData.map(c => c.count);

        new Chart(catCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#10b981',
                        '#8b5cf6',
                        '#3b82f6',
                        '#f59e0b',
                        '#ec4899'
                    ],
                    borderColor: '#0b0f19',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#f8fafc', font: { family: 'Plus Jakarta Sans' } }
                    }
                },
                cutout: '70%'
            }
        });
    }
}
