document.addEventListener('DOMContentLoaded', () => {
    // Chat Message Form Submit
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = document.getElementById('chat-message-input');
            const content = input.value.trim();

            if (!content) return;

            fetch('/api/message/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: content })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    input.value = '';
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao enviar mensagem.'));
        });
    }

    // Support Ticket Form Submit
    const ticketForm = document.getElementById('ticket-form');
    if (ticketForm) {
        ticketForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                subject: document.getElementById('ticket-subject').value,
                category: document.getElementById('ticket-category').value,
                priority: document.getElementById('ticket-priority').value
            };

            fetch('/api/ticket/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao abrir ticket.'));
        });
    }

    // Document Upload Form Submit
    const docForm = document.getElementById('document-form');
    if (docForm) {
        docForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                title: document.getElementById('doc-title').value,
                doc_type: document.getElementById('doc-type').value,
                project_id: document.getElementById('doc-project-id').value
            };

            fetch('/api/document/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao carregar documento.'));
        });
    }
});
