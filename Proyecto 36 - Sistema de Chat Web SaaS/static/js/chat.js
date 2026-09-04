// CONNECT-CHAT SaaS - Client Side Realtime Logic & Interactive Features (Pt-PT)

let activeConvId = null;
let pollInterval = null;
let callTimerInterval = null;
let callSeconds = 0;

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

// Polling de mensagens em tempo real
function startMessagePolling() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(() => {
        if (activeConvId) {
            fetchMessages(activeConvId, false);
        }
    }, 4000);
}

// Obter mensagens via AJAX
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
        console.error('Erro ao consultar mensagens:', err);
    }
}

// Enviar Nova Mensagem
async function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('messageInput');
    const content = input.value.trim ? input.value.trim() : input.value;

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
            appendSingleMessageDOM(data.message);
            playNotificationSound();
            const container = document.getElementById('chatMessagesContainer');
            if (container) container.scrollTop = container.scrollHeight;
        } else {
            alert('Erro ao enviar mensagem: ' + (data.message || 'Desconhecido'));
        }
    } catch (err) {
        console.error(err);
        alert('Erro de ligação ao servidor de chat.');
    }
}

// Reagir a uma mensagem (👍, ❤️, 😂, 😮, 😢, 🔥) com atualização instantânea no DOM
async function reactToMessage(msgId, emoji) {
    try {
        const res = await fetch(`/api/messages/${msgId}/react`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emoji: emoji })
        });
        const data = await res.json();
        if (data.success) {
            updateMessageReactionsDOM(msgId, data.reactions);
            showToast(`Reação ${emoji} ${data.action === 'added' ? 'adicionada' : 'removida'}`);
        }
    } catch (err) {
        console.error('Erro ao reagir:', err);
    }
}

// Atualizar reações de uma mensagem no DOM
function updateMessageReactionsDOM(msgId, reactions) {
    const msgElem = document.querySelector(`[data-message-id="${msgId}"]`);
    if (!msgElem) return;

    let reactionsContainer = msgElem.querySelector('.reactions-container');
    if (!reactionsContainer) {
        reactionsContainer = document.createElement('div');
        reactionsContainer.className = 'reactions-container flex flex-wrap gap-1 mt-1';
        msgElem.querySelector('.bubble-content-wrapper').appendChild(reactionsContainer);
    }

    if (!reactions || reactions.length === 0) {
        reactionsContainer.innerHTML = '';
        return;
    }

    let html = '';
    reactions.forEach(r => {
        html += `<span class="bg-slate-800 text-slate-200 text-[10px] px-1.5 py-0.5 rounded-full border border-slate-700 font-bold" title="Reagido por ${r.user_name}">${r.emoji}</span>`;
    });
    reactionsContainer.innerHTML = html;
}

// Silenciar Notificações do Chat
async function toggleMuteNotifications() {
    if (!activeConvId) return;

    try {
        const res = await fetch(`/api/conversations/${activeConvId}/toggle-mute`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            const btn = document.getElementById('btnMuteNotifications');
            const icon = document.getElementById('iconMuteNotifications');
            const text = document.getElementById('textMuteNotifications');

            if (data.is_muted) {
                if (icon) icon.className = 'fas fa-bell-slash text-amber-400 mr-2';
                if (text) text.innerText = 'Ativar Notificações';
                showToast('🔕 Notificações silenciadas para esta conversa');
            } else {
                if (icon) icon.className = 'fas fa-bell text-blue-400 mr-2';
                if (text) text.innerText = 'Silenciar Notificações';
                showToast('🔔 Notificações ativadas');
            }
        }
    } catch (err) {
        console.error(err);
    }
}

// Abrir Modal de Ficheiros & Fotos Partilhadas
async function openSharedMediaModal() {
    if (!activeConvId) return;

    const modal = document.getElementById('sharedMediaModal');
    const container = document.getElementById('sharedMediaGrid');
    if (!modal || !container) return;

    modal.classList.remove('hidden');
    container.innerHTML = '<div class="text-center text-xs text-slate-400 py-6">A carregar ficheiros partilhados...</div>';

    try {
        const res = await fetch(`/api/conversations/${activeConvId}/media`);
        const data = await res.json();
        if (data.success && data.media.length > 0) {
            let html = '';
            data.media.forEach(m => {
                html += `
                    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center space-x-3">
                        <div class="w-10 h-10 rounded-lg bg-blue-600/20 border border-blue-500/30 text-blue-400 flex items-center justify-center font-bold text-base shrink-0">
                            <i class="fas fa-file-alt"></i>
                        </div>
                        <div class="flex-grow min-w-0">
                            <div class="text-xs font-bold text-white truncate">${m.content}</div>
                            <div class="text-[10px] text-slate-400">por ${m.sender_name} • ${m.created_at}</div>
                        </div>
                        <a href="${m.media_url}" target="_blank" class="p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold transition-colors">
                            <i class="fas fa-download"></i>
                        </a>
                    </div>
                `;
            });
            container.innerHTML = html;
        } else {
            container.innerHTML = '<div class="text-center text-xs text-slate-500 py-6">Sem ficheiros nem fotos partilhadas ainda.</div>';
        }
    } catch (err) {
        console.error(err);
        container.innerHTML = '<div class="text-center text-xs text-red-400 py-6">Erro ao carregar ficheiros.</div>';
    }
}

// Iniciar Videochamada HD WebRTC
function startVideoCall() {
    const modal = document.getElementById('videoCallModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    startCallTimer('videoCallTimer');
    playCallRingSound();
}

// Iniciar Chamada de Voz
function startVoiceCall() {
    const modal = document.getElementById('voiceCallModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    startCallTimer('voiceCallTimer');
    playCallRingSound();
}

// Terminar Chamada
function endCall(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('hidden');
    if (callTimerInterval) clearInterval(callTimerInterval);
    callSeconds = 0;
    showToast('Chamada terminada');
}

// Temporizador de Chamada
function startCallTimer(timerElemId) {
    if (callTimerInterval) clearInterval(callTimerInterval);
    callSeconds = 0;
    const elem = document.getElementById(timerElemId);
    callTimerInterval = setInterval(() => {
        callSeconds++;
        const mins = String(Math.floor(callSeconds / 60)).padStart(2, '0');
        const secs = String(callSeconds % 60).padStart(2, '0');
        if (elem) elem.innerText = `${mins}:${secs}`;
    }, 1000);
}

// Alternar Painel Lateral de Informações
function toggleRightDrawer() {
    const drawer = document.getElementById('rightDrawer');
    if (drawer) {
        drawer.classList.toggle('hidden');
        drawer.classList.toggle('flex');
    }
}

// Alterar Estado Em Linha
async function setUserPresenceStatus(status) {
    try {
        const res = await fetch('/api/user/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: status })
        });
        const data = await res.json();
        if (data.success) {
            showToast(`Estado atualizado para: ${status}`);
        }
    } catch (err) {
        console.error(err);
    }
}

// Iniciar Conversa Direta
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

// Emojis Rápidos
function initEmojiPicker() {
    const quickEmojis = ['👍', '❤️', '😂', '🔥', '🚀', '👏', '🎉', '💡'];
    const bar = document.getElementById('quickEmojiBar');
    const input = document.getElementById('messageInput');

    if (bar && input) {
        bar.innerHTML = '';
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

// Inserir mensagem no DOM dinamicamente
function appendSingleMessageDOM(msg) {
    const container = document.getElementById('chatMessagesContainer');
    if (!container) return;

    const div = document.createElement('div');
    div.className = `flex items-end space-x-2 message-item relative group justify-end`;
    div.setAttribute('data-message-id', msg.id);

    div.innerHTML = `
        <div class="reaction-popover">
            <button type="button" onclick="reactToMessage(${msg.id}, '👍')" class="reaction-btn">👍</button>
            <button type="button" onclick="reactToMessage(${msg.id}, '❤️')" class="reaction-btn">❤️</button>
            <button type="button" onclick="reactToMessage(${msg.id}, '😂')" class="reaction-btn">😂</button>
            <button type="button" onclick="reactToMessage(${msg.id}, '😮')" class="reaction-btn">😮</button>
            <button type="button" onclick="reactToMessage(${msg.id}, '🔥')" class="reaction-btn">🔥</button>
        </div>
        <div class="max-w-md bubble-content-wrapper">
            <div class="p-3 text-xs leading-relaxed bubble-sent">
                ${msg.content}
            </div>
            <div class="flex items-center space-x-1 mt-1 text-[10px] text-slate-500 justify-end">
                <span>${msg.created_at.split(' ')[1].substring(0, 5)}</span>
                <span class="text-blue-400 font-black ml-1" title="Visto a azul">✓✓</span>
            </div>
            <div class="reactions-container flex flex-wrap gap-1 mt-1 justify-end"></div>
        </div>
    `;

    container.appendChild(div);
}

// Mostrar Toast Flutuante em Pt-PT
function showToast(text) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-5 right-5 bg-blue-600 text-white font-bold text-xs px-4 py-3 rounded-xl shadow-2xl z-50 animate-bounce flex items-center space-x-2 border border-blue-400';
    toast.innerHTML = `<i class="fab fa-facebook-messenger text-base"></i><span>${text}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Som de Notificação
function playNotificationSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.15);
    } catch (e) {}
}

function playCallRingSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.4);
    } catch (e) {}
}

// Renderizar mensagens
function renderMessages(messagesList) {
    const container = document.getElementById('chatMessagesContainer');
    if (!container) return;

    const currentCount = container.querySelectorAll('.message-item').length;
    if (messagesList.length === currentCount) return;
}
