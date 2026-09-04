// RESOLV-IT SaaS - Main Interactive Scripts

document.addEventListener('DOMContentLoaded', () => {
    initSLAHighlighting();
    initQuickResponses();
});

// Resaltar y calcular SLAs
function initSLAHighlighting() {
    const slaElements = document.querySelectorAll('[data-due-at]');
    slaElements.forEach(el => {
        const dueAt = new Date(el.getAttribute('data-due-at')).getTime();
        const now = new Date().getTime();
        const diffHours = (dueAt - now) / (1000 * 60 * 60);

        if (diffHours < 0) {
            el.classList.add('text-red-400', 'font-bold');
            el.innerHTML = `<i class="fas fa-exclamation-triangle mr-1"></i> Vencido (${Math.abs(Math.round(diffHours))}h atrás)`;
        } else if (diffHours < 2) {
            el.classList.add('text-amber-400', 'font-bold');
            el.innerHTML = `<i class="fas fa-clock mr-1"></i> ${Math.round(diffHours * 60)} min restantes`;
        }
    });
}

// Respuestas Rápidas (Canned Responses)
function initQuickResponses() {
    const commentBox = document.getElementById('comment_content');
    const quickButtons = document.querySelectorAll('.canned-btn');

    if (commentBox && quickButtons.length > 0) {
        quickButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const templateText = btn.getAttribute('data-template');
                commentBox.value = templateText;
                commentBox.focus();
            });
        });
    }
}

// API: Actualizar Estado del Ticket vía AJAX
async function updateTicketStatus(ticketId, newStatus, redirectReload = true) {
    try {
        const res = await fetch(`/api/tickets/${ticketId}/update-status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus, actor: 'Agente Soporte' })
        });
        const data = await res.json();
        if (data.success) {
            if (redirectReload) window.location.reload();
        } else {
            alert('Error al actualizar estado: ' + (data.message || 'Error desconocido'));
        }
    } catch (err) {
        console.error(err);
        alert('Error de conexión al servidor.');
    }
}

// API: Actualizar Prioridad del Ticket vía AJAX
async function updateTicketPriority(ticketId, newPriority) {
    try {
        const res = await fetch(`/api/tickets/${ticketId}/update-priority`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ priority: newPriority, actor: 'Agente Soporte' })
        });
        const data = await res.json();
        if (data.success) {
            window.location.reload();
        } else {
            alert('Error al actualizar prioridad: ' + (data.message || 'Error desconocido'));
        }
    } catch (err) {
        console.error(err);
        alert('Error de conexión al servidor.');
    }
}

// API: Reasignar Agente
async function reassignTicketAgent(ticketId, agentId) {
    try {
        const res = await fetch(`/api/tickets/${ticketId}/reassign`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ agent_id: agentId, actor: 'Supervisor Soporte' })
        });
        const data = await res.json();
        if (data.success) {
            window.location.reload();
        } else {
            alert('Error al reasignar agente: ' + (data.message || 'Error desconocido'));
        }
    } catch (err) {
        console.error(err);
        alert('Error de conexión al servidor.');
    }
}
