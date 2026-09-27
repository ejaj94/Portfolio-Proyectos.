// EJAJ TECH - BotCorp AI Chatbot Interactive JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initChatWidget();
});

function initChatWidget() {
    const chatForm = document.getElementById('chatForm');
    const inputMsg = document.getElementById('chatInputMessage');
    const messagesBody = document.getElementById('chatMessagesBody');

    if (chatForm && inputMsg && messagesBody) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = inputMsg.value.trim();
            if (!text) return;

            // 1. Append User Message
            appendMessage('user', text);
            inputMsg.value = '';

            // 2. Show Bot Typing Indicator
            const typingEl = appendTypingIndicator();

            try {
                // 3. Fetch Bot Response
                const res = await fetch('/api/chat/message', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, conversation_id: 1 })
                });

                const data = await res.json();
                typingEl.remove();

                if (data.success) {
                    appendMessage('bot', data.reply);
                } else {
                    appendMessage('bot', '❌ Desculpe, ocorreu um erro ao processar a resposta.');
                }
            } catch (err) {
                typingEl.remove();
                appendMessage('bot', '❌ Erro de ligação com o servidor do chatbot.');
            }
        });
    }
}

function appendMessage(sender, text) {
    const messagesBody = document.getElementById('chatMessagesBody');
    if (!messagesBody) return;

    const div = document.createElement('div');
    div.className = `chat-msg ${sender}`;

    // Handle HTML links inside bot response
    if (text.includes('http')) {
        div.innerHTML = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color: #00d8f6; font-weight: bold; text-decoration: underline;">$1</a>');
    } else {
        div.innerText = text;
    }

    messagesBody.appendChild(div);
    messagesBody.scrollTop = messagesBody.scrollHeight;
}

function appendTypingIndicator() {
    const messagesBody = document.getElementById('chatMessagesBody');
    const div = document.createElement('div');
    div.className = 'chat-msg bot';
    div.style.fontStyle = 'italic';
    div.style.color = '#94a3b8';
    div.innerHTML = '<i class="fa-solid fa-robot fa-spin"></i> O BotCorp AI está a processar...';
    messagesBody.appendChild(div);
    messagesBody.scrollTop = messagesBody.scrollHeight;
    return div;
}

function sendQuickFaq(questionText) {
    const inputMsg = document.getElementById('chatInputMessage');
    const chatForm = document.getElementById('chatForm');

    if (inputMsg && chatForm) {
        inputMsg.value = questionText;
        chatForm.dispatchEvent(new Event('submit'));
    }
}

// Admin API Actions

async function submitAddFaq(event) {
    event.preventDefault();
    const q = document.getElementById('faqQuestionInput').value.trim();
    const a = document.getElementById('faqAnswerInput').value.trim();
    const cat = document.getElementById('faqCatInput').value;
    const kw = document.getElementById('faqKwInput').value.trim();

    try {
        const res = await fetch('/api/faq/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: q, answer: a, category: cat, keywords: kw })
        });
        const data = await res.json();
        if (data.success) {
            alert('✅ ' + data.message);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}

async function deleteFaq(faqId) {
    if (!confirm('Eliminar esta FAQ?')) return;
    try {
        const res = await fetch(`/api/faq/delete/${faqId}`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            alert('🗑️ ' + data.message);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}

async function submitAddKb(event) {
    event.preventDefault();
    const title = document.getElementById('kbTitleInput').value.trim();
    const cat = document.getElementById('kbCatInput').value;
    const content = document.getElementById('kbContentInput').value.trim();

    try {
        const res = await fetch('/api/kb/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title, category: cat, content: content })
        });
        const data = await res.json();
        if (data.success) {
            alert('📚 ' + data.message);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}
