// EJAJ TECH - Client Portal Interactive JavaScript

// Open / Close Support Ticket Modal
function openTicketModal() {
    const modal = document.getElementById('ticketModal');
    if (modal) modal.style.display = 'flex';
}

function closeTicketModal() {
    const modal = document.getElementById('ticketModal');
    if (modal) modal.style.display = 'none';
}

// Send Chat Message AJAX
async function sendMessage(event, projectId = null) {
    event.preventDefault();
    const input = document.getElementById('chatInput');
    const content = input ? input.value.trim() : '';

    if (!content) return;

    try {
        const res = await fetch('/api/messages/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content, project_id: projectId })
        });

        const data = await res.json();
        if (data.success) {
            input.value = '';
            window.location.reload();
        } else {
            alert('Erro ao enviar mensagem: ' + data.message);
        }
    } catch (err) {
        alert('Erro de conexão: ' + err.message);
    }
}

// Submit New Support Ticket AJAX
async function submitSupportTicket(event) {
    event.preventDefault();
    const subject = document.getElementById('ticketSubject').value.trim();
    const priority = document.getElementById('ticketPriority').value;
    const description = document.getElementById('ticketDescription').value.trim();

    try {
        const res = await fetch('/api/tickets/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject: subject, priority: priority, description: description })
        });

        const data = await res.json();
        if (data.success) {
            alert('Ticket criado com sucesso! Código: ' + data.ticket_code);
            closeTicketModal();
            window.location.reload();
        } else {
            alert('Erro ao criar ticket: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Approve Budget AJAX
async function approveBudget(budgetId) {
    if (!confirm('Tem a certeza que pretende aprovar este orçamento?')) return;

    try {
        const res = await fetch('/api/budgets/approve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ budget_id: budgetId })
        });

        const data = await res.json();
        if (data.success) {
            alert('Orçamento aprovado com sucesso!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Update Profile AJAX
async function updateProfile(event) {
    event.preventDefault();
    const fullName = document.getElementById('fullNameInput').value.trim();
    const companyName = document.getElementById('companyNameInput').value.trim();
    const phone = document.getElementById('phoneInput').value.trim();

    try {
        const res = await fetch('/api/profile/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: fullName, company_name: companyName, phone: phone })
        });

        const data = await res.json();
        if (data.success) {
            alert('Perfil atualizado com sucesso!');
            window.location.reload();
        } else {
            alert('Erro ao atualizar: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}
