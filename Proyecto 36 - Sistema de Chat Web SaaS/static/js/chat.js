// CONNECT-CHAT SaaS - Client Side Realtime Logic

let activeConvId = null;
let pollInterval = null;

document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatMessagesContainer');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    const currentConvElem = document.getElementById('activeConvId');
    if (currentConvElem) {
        activeConvId = parseInt(currentConvElem.value);
        startMessagePolling();
    }

    initEmojiPicker();
});

// Polling de mensajes en tiempo real
function startMessagePolling() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(() => {
        if (activeConvId) {
            fetchMessages(activeConvId, false);
        }
    }, 4000);
}

// Obtener mensajes vía AJAX
async function fetchMessages(convId, scrollToBottom = true) {
    try {
        const res = await fetch(`/api/conversations/${convId}/messages`);
        const data = await res.json();
        if (data.success) {
            renderMessages(data.messages);
            if (scrollToBottom) {
                const container = document.getElementById('chatMessagesContainer');
                if (container) container.scrollTop = container.scrollHeight;
            }
        }
    } catch (err) {
        console.error('Error al consultar mensajes:', err);
    }
}

// Enviar Nuevo Mensaje
async function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('messageInput');
    const content = input.value.strip ? input.value.strip() : input.value.trim();

    if (!content || !activeConvId) return;

    input.value = '';

    try {
        const res = await fetch(`/api/conversations/${activeConvId}/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content })
        });
        const data = await res.json();
        if (data.success) {
            fetchMessages(activeConvId, true);
            playNotificationSound();
        } else {
            alert('Error enviando mensaje: ' + (data.message || 'Desconocido'));
        }
    } catch (err) {
        console.error(err);
        alert('Error de conexión al servidor de chat.');
    }
}

// Reaccionar a un mensaje (👍, ❤️, 😂, 😮, 😢, 🔥)
async function reactToMessage(msgId, emoji) {
    try {
        const res = await fetch(`/api/messages/${msgId}/react`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emoji: emoji })
        });
        const data = await res.json();
        if (data.success) {
            fetchMessages(activeConvId, false);
        }
    } catch (err) {
        console.error(err);
    }
}

// Cambiar Estado Online del Usuario
async function setUserPresenceStatus(status) {
    try {
        const res = await fetch('/api/user/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: status })
        });
        const data = await res.json();
        if (data.success) {
            window.location.reload();
        }
    } catch (err) {
        console.error(err);
    }
}

// Iniciar Chat Directo con usuario
async function startDirectChat(userId) {
    try {
        const res = await fetch('/api/conversations/start-direct', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = `/?conv_id=${data.conversation_id}`;
        }
    } catch (err) {
        console.error(err);
    }
}

// Selector Rápido de Emojis
function initEmojiPicker() {
    const quickEmojis = ['👍', '❤️', '😂', '🔥', '🚀', '👏', '🎉', '💡'];
    const bar = document.getElementById('quickEmojiBar');
    const input = document.getElementById('messageInput');

    if (bar && input) {
        quickEmojis.forEach(em => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'hover:scale-125 transition-transform text-lg px-1';
            btn.innerText = em;
            btn.onclick = () => {
                input.value += em + ' ';
                input.focus();
            };
            bar.appendChild(btn);
        });
    }
}

// Simulación de sonido de notificación Messenger
function playNotificationSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.15); // A5
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.15);
    } catch (e) {
        // Ignorar si el navegador bloquea audio sin interacción previa
    }
}

// Renderizar Mensajes vía JS
function renderMessages(messagesList) {
    // Si viene la misma cantidad, no re-renderizar para evitar parpadeo
    const container = document.getElementById('chatMessagesContainer');
    if (!container) return;

    const currentCount = container.querySelectorAll('.message-item').length;
    if (messagesList.length === currentCount) return;

    // Re-render en cambios
    window.location.reload();
}
