/**
 * Chat: Socket.IO em tempo real, fundo do chat, proteção anti-captura, mensagens e quebra-gelos.
 */
'use strict';

let socket = null;

// ═══════════════════════════════════════════════════
// 🔄 TEMPO REAL: ligação Socket.IO persistente
// Conecta ao entrar e mantém salas atualizadas (match, mensagens, notifs)
// ═══════════════════════════════════════════════════
function connectRealtime() {
  try {
    if (!socket) {
      socket = io({ transports: ['websocket', 'polling'] });

      socket.on('connect', () => {
        // Registrar o utilizador para receber eventos globais na sala pessoal
        const u = STATE.currentUser;
        socket.emit('register_user', {
          user_id: u && (u.id || u.email),
          user_email: u && u.email
        });
      });

      // 💜 NOVO MATCH (ou outra pessoa deu like em ti e combinou)
      socket.on('match', (m) => {
        try {
          // Recarregar a lista de matches do servidor em tempo real
          fetch('/api/v1/matches')
            .then(r => r.ok ? r.json() : null)
            .then(data => {
              if (data && Array.isArray(data.matches)) {
                MATCHES_DATA = data.matches;
                try { localStorage.setItem(userMatchesKey, JSON.stringify(MATCHES_DATA)); } catch(e){}
                renderMatches();
              }
            })
            .catch(() => {});
          const who = (m && m.with_user && m.with_user.name) ? m.with_user.name : 'Alguém';
          showAppToast('💜 É um Match com ' + who + '!', 'success');
          // Som/vibração leve (mobile)
          try { if (navigator.vibrate) navigator.vibrate(80); } catch(e){}
        } catch(e){}
      });

      // 💬 MENSAGEM NOVA quando NÃO estás com a conversa aberta
      socket.on('chat_message', (msg) => {
        try {
          if (!STATE.currentUser) return;
          const fromId = String(msg.sender_id || msg.from || '');
          const isMe = fromId === String(STATE.currentUser.id || STATE.currentUser.email);
          if (isMe) return; // eco do próprio remetente
          // Se estás com ESTA conversa aberta, o handler da sala (new_message) trata
          if (STATE.chatPeer && String(STATE.chatPeer.id) === fromId) return;
          const fromName = (msg.peer_name || 'Alguém');
          showAppToast('💬 ' + fromName + ': ' + String(msg.content || '').slice(0, 80), 'info');
          try { if (navigator.vibrate) navigator.vibrate(60); } catch(e){}
          // Badge de não-lidas (persistente entre abas)
          try {
            const key = 'sigaleve_unread_' + (STATE.currentUser.id || STATE.currentUser.email);
            const cur = parseInt(localStorage.getItem(key) || '0', 10) || 0;
            localStorage.setItem(key, String(cur + 1));
          } catch(e){}
        } catch(e){}
      });
    } else if (socket.connected) {
      const u = STATE.currentUser;
      socket.emit('register_user', {
        user_id: u && (u.id || u.email),
        user_email: u && u.email
      });
    }
    // Reconexão: Socket.IO auto-reconnecta; re-registrar ao voltar
    if (socket) {
      socket.on('disconnect', () => {});
      socket.off('reconnect').on('reconnect', () => {
        const u = STATE.currentUser;
        socket.emit('register_user', {
          user_id: u && (u.id || u.email),
          user_email: u && u.email
        });
      });
    }
  } catch(e) { socket = null; }
}
let currentChatMsgIds = new Set();

const CHAT_BG_THEMES = {
  empty: {
    id: 'empty',
    name: 'Vazio (Padrão Limpo)',
    desc: 'Fundo neutro e minimalista sem distrações',
    css: 'transparent',
    preview: 'linear-gradient(135deg,#09090b,#18181b)'
  },
  midnight_velvet: {
    id: 'midnight_velvet',
    name: 'Veludo da Meia-Noite',
    desc: 'Brilho suave violeta e magenta nos cantos',
    css: 'radial-gradient(circle at 15% 15%, rgba(168,85,247,0.16), transparent 55%), radial-gradient(circle at 85% 85%, rgba(236,72,153,0.14), transparent 55%)',
    preview: 'linear-gradient(135deg,#2e1065,#831843)'
  },
  aurora_emerald: {
    id: 'aurora_emerald',
    name: 'Aurora Esmeralda',
    desc: 'Tons serenos de verde esmeralda e azul profundo',
    css: 'radial-gradient(circle at 20% 10%, rgba(16,185,129,0.15), transparent 55%), radial-gradient(circle at 85% 90%, rgba(14,165,233,0.14), transparent 55%)',
    preview: 'linear-gradient(135deg,#064e3b,#0c4a6e)'
  },
  sunset_romance: {
    id: 'sunset_romance',
    name: 'Pôr do Sol Romântico',
    desc: 'Atmosfera quente em tons rosa, coral e âmbar',
    css: 'radial-gradient(circle at 80% 15%, rgba(244,63,94,0.16), transparent 55%), radial-gradient(circle at 15% 85%, rgba(245,158,11,0.12), transparent 55%)',
    preview: 'linear-gradient(135deg,#881337,#78350f)'
  },
  cosmic_stars: {
    id: 'cosmic_stars',
    name: 'Noite Estrelada',
    desc: 'Padrão subtil de constelações sobre fundo escuro',
    css: 'radial-gradient(rgba(192,132,252,0.18) 1px, transparent 1px), radial-gradient(rgba(244,114,182,0.14) 1px, transparent 1px)',
    bgSize: '36px 36px',
    bgPos: '0 0, 18px 18px',
    preview: 'linear-gradient(135deg,#1e1b4b,#3b0764)'
  },
  deep_ocean: {
    id: 'deep_ocean',
    name: 'Oceano Profundo',
    desc: 'Degradê suave azul safira e índigo noturno',
    css: 'linear-gradient(180deg, rgba(30,58,138,0.18) 0%, rgba(15,23,42,0.28) 100%)',
    preview: 'linear-gradient(135deg,#1e3a8a,#0f172a)'
  }
};

function getChatBgStorageKey() {
  const uid = (STATE.currentUser && (STATE.currentUser.id || STATE.currentUser.email)) || 'default';
  return 'sigaleve_chat_bg_' + uid;
}

function applySavedChatBackground() {
  const wmOverlay = document.getElementById('chat-watermark-overlay');
  if (!wmOverlay) return;
  // Limpar qualquer texto ou marca d'água antiga (como ejajtech / SIGALEVE PRIVACY)
  wmOverlay.innerHTML = '';

  let savedData = null;
  try {
    const raw = localStorage.getItem(getChatBgStorageKey());
    if (raw) savedData = JSON.parse(raw);
  } catch (e) {}

  // Se não tiver subscrição ou não houver fundo guardado, manter fundo vazio limpo
  if (!isUserSubscribed() || !savedData || savedData.type === 'empty') {
    wmOverlay.style.background = 'transparent';
    wmOverlay.style.backgroundImage = 'none';
    wmOverlay.style.opacity = '1';
    return;
  }

  if (savedData.type === 'preset' && CHAT_BG_THEMES[savedData.value]) {
    const theme = CHAT_BG_THEMES[savedData.value];
    wmOverlay.style.background = theme.css;
    wmOverlay.style.backgroundSize = theme.bgSize || 'cover';
    wmOverlay.style.backgroundPosition = theme.bgPos || 'center';
    wmOverlay.style.opacity = '1';
  } else if (savedData.type === 'color' && savedData.value) {
    wmOverlay.style.background = savedData.value;
    wmOverlay.style.backgroundImage = 'none';
    wmOverlay.style.opacity = '0.22';
  } else if (savedData.type === 'image' && savedData.value) {
    wmOverlay.style.background = `linear-gradient(rgba(9,9,11,0.68), rgba(9,9,11,0.75)), url("${savedData.value.replace(/"/g, '')}") center/cover no-repeat`;
    wmOverlay.style.opacity = '1';
  }
}

function selectChatBgOption(type, value) {
  if (!isUserSubscribed()) {
    if (typeof showAppToast === 'function') {
      showAppToast('💎 Personalizar o fundo do chat é exclusivo para subscritores Sigaleve!', 'warning');
    }
    closeChatBgCustomizerModal();
    openSubscriptionModal('plus');
    return;
  }
  try {
    localStorage.setItem(getChatBgStorageKey(), JSON.stringify({ type, value }));
  } catch (e) {}
  applySavedChatBackground();
  renderChatBgModalOptions();
  if (typeof showAppToast === 'function') {
    showAppToast(type === 'empty' ? 'Fundo do chat reposto para o padrão vazio.' : '✨ Fundo do chat personalizado com sucesso!', 'success');
  }
}

async function handleCustomChatBgFile(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;

  const btnLbl = document.getElementById('btn-lbl-chat-bg-file');
  const prevLbl = btnLbl ? btnLbl.textContent : '';
  if (btnLbl) btnLbl.textContent = 'A carregar foto...';

  try {
    const serverUrl = await uploadPhotoFile(file);
    if (serverUrl) {
      selectChatBgOption('image', serverUrl);
    }
  } catch (err) {
    console.error('Erro ao enviar imagem de fundo:', err);
    if (typeof showAppToast === 'function') showAppToast('Falha ao processar imagem de fundo.', 'error');
  } finally {
    if (btnLbl) btnLbl.textContent = prevLbl || 'Escolher Imagem do Dispositivo / Galeria';
    e.target.value = '';
  }
}

function renderChatBgModalOptions() {
  const grid = document.getElementById('chat-bg-presets-grid');
  if (!grid) return;
  let current = { type: 'empty', value: 'empty' };
  try {
    const raw = localStorage.getItem(getChatBgStorageKey());
    if (raw) current = JSON.parse(raw);
  } catch (e) {}

  grid.innerHTML = Object.values(CHAT_BG_THEMES).map(t => {
    const isSelected = (current.type === 'empty' && t.id === 'empty') || (current.type === 'preset' && current.value === t.id);
    const borderCls = isSelected ? 'border-purple-500 ring-2 ring-purple-500/40' : 'border-zinc-800 hover:border-zinc-600';
    return `
      <button type="button" onclick="selectChatBgOption('${t.id === 'empty' ? 'empty' : 'preset'}', '${t.id}')" class="p-3 rounded-2xl border text-left transition-all flex items-center gap-3 bg-zinc-900/80 hover:bg-zinc-900 ${borderCls}">
        <div class="w-11 h-11 rounded-xl flex-shrink-0 border border-white/15 shadow-inner" style="background:${t.preview}"></div>
        <div class="min-w-0 flex-1">
          <div class="flex items-center justify-between gap-1">
            <p class="text-xs font-black text-white truncate">${t.name}</p>
            ${isSelected ? '<i class="fa-solid fa-circle-check text-purple-400 text-xs"></i>' : ''}
          </div>
          <p class="text-[10px] text-zinc-400 line-clamp-1 mt-0.5">${t.desc}</p>
        </div>
      </button>
    `;
  }).join('');
}

function openChatBgCustomizerModal() {
  if (!isUserSubscribed()) {
    if (typeof showAppToast === 'function') {
      showAppToast('💎 A personalização do fundo do chat é exclusiva para membros subscritos Sigaleve!', 'warning');
    }
    openSubscriptionModal('plus');
    return;
  }

  let modal = document.getElementById('modal-chat-bg-customizer');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'modal-chat-bg-customizer';
    modal.className = 'fixed inset-0 z-[9990] flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in';
    modal.innerHTML = `
      <div class="w-full max-w-lg rounded-3xl p-5 sm:p-6 border border-purple-500/30 shadow-2xl flex flex-col max-h-[90vh] overflow-y-auto" style="background:var(--card)">
        <div class="flex items-center justify-between pb-3 border-b" style="border-color:var(--bdr)">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-2xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-base">
              <i class="fa-solid fa-palette"></i>
            </div>
            <div>
              <h3 class="text-sm font-black text-white flex items-center gap-2">
                <span>Personalizar Fundo do Chat</span>
                <span class="text-[9px] bg-gradient-to-r from-purple-500 to-pink-500 text-white px-2 py-0.5 rounded-full font-black uppercase">VIP</span>
              </h3>
              <p class="text-[11px] text-zinc-400">Escolhe um ambiente limpo ou personaliza ao teu gosto</p>
            </div>
          </div>
          <button type="button" onclick="closeChatBgCustomizerModal()" class="w-8 h-8 rounded-full bg-white/5 hover:bg-white/15 text-zinc-400 hover:text-white flex items-center justify-center transition-all">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <div class="mt-4 space-y-4">
          <div>
            <p class="text-[11px] font-black uppercase tracking-wider text-zinc-400 mb-2">Temas & Ambientes Sigaleve</p>
            <div id="chat-bg-presets-grid" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5"></div>
          </div>

          <div class="pt-3 border-t border-white/5">
            <p class="text-[11px] font-black uppercase tracking-wider text-zinc-400 mb-2">Cor Sólida Suave</p>
            <div class="flex items-center gap-3">
              <input type="color" id="inp-custom-chat-bg-color" value="#6b21a8" onchange="selectChatBgOption('color', this.value)" class="w-10 h-10 rounded-xl cursor-pointer bg-transparent border border-zinc-700"/>
              <span class="text-xs text-zinc-300">Escolhe qualquer cor para aplicar uma tonalidade suave ao fundo</span>
            </div>
          </div>

          <div class="pt-3 border-t border-white/5">
            <p class="text-[11px] font-black uppercase tracking-wider text-zinc-400 mb-2">Imagem de Fundo Personalizada (Ficheiro do Dispositivo / Galeria)</p>
            <input type="file" id="inp-custom-chat-bg-file" accept="image/*" class="hidden" onchange="handleCustomChatBgFile(event)"/>
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
              <button type="button" onclick="document.getElementById('inp-custom-chat-bg-file').click()" class="flex-1 py-3 px-4 rounded-2xl bg-zinc-900 hover:bg-zinc-800 border border-purple-500/30 hover:border-purple-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-md">
                <i class="fa-solid fa-cloud-arrow-up text-pink-400 text-base"></i>
                <span id="btn-lbl-chat-bg-file">Escolher Imagem do Dispositivo / Galeria</span>
              </button>
            </div>
            <p class="text-[10px] text-zinc-500 mt-1.5">Podes selecionar qualquer foto do teu telemóvel ou computador (PNG, JPG, WebP).</p>
          </div>
        </div>

        <div class="mt-5 pt-3 border-t flex items-center justify-between" style="border-color:var(--bdr)">
          <button type="button" onclick="selectChatBgOption('empty', 'empty')" class="px-3.5 py-2 rounded-xl text-xs font-bold text-zinc-400 hover:text-white bg-zinc-900 border border-zinc-800 transition-all">
            <i class="fa-solid fa-rotate-left mr-1"></i> Repor Fundo Vazio
          </button>
          <button type="button" onclick="closeChatBgCustomizerModal()" class="px-5 py-2 rounded-xl text-xs font-bold text-white bg-purple-600 hover:bg-purple-500 transition-all">
            Concluído
          </button>
        </div>
      </div>
    `;
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeChatBgCustomizerModal();
    });
    document.body.appendChild(modal);
  }

  renderChatBgModalOptions();
  modal.classList.remove('hidden');
}

function closeChatBgCustomizerModal() {
  const modal = document.getElementById('modal-chat-bg-customizer');
  if (modal) modal.classList.add('hidden');
}

let _globalScreenshotExplicitLock = false;

function activateGlobalPrivacyLock(explicitAttempt = false, reasonMsg = '') {
  document.body.classList.add('app-privacy-locked');
  const secChat = document.getElementById('sec-chat');
  if (secChat && (secChat.classList.contains('active') || secChat.style.display === 'flex')) {
    secChat.classList.add('chat-blurred');
  }
  if (explicitAttempt) {
    _globalScreenshotExplicitLock = true;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText('🔒 Conteúdo confidencial protegido pelo Sigaleve. Capturas e cópias não são permitidas.');
      }
    } catch (_) {}
    if (reasonMsg && typeof showAppToast === 'function') {
      showAppToast(reasonMsg, 'error');
    }
  }
}

function dismissGlobalPrivacyShield() {
  _globalScreenshotExplicitLock = false;
  document.body.classList.remove('app-privacy-locked');
  const secChat = document.getElementById('sec-chat');
  if (secChat) secChat.classList.remove('chat-blurred');
}

function initChatAntiScreenshot() {
  const secChat = document.getElementById('sec-chat');
  if (secChat) {
    applySavedChatBackground();
  }

  if (window._globalPrivacyShieldBound) return;
  window._globalPrivacyShieldBound = true;

  // 1. Desfocar toda a aplicação imediatamente quando a janela perde foco (ex: Snipping Tool / Win+Shift+S / Alt+Tab)
  window.addEventListener('blur', () => {
    activateGlobalPrivacyLock(false);
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      activateGlobalPrivacyLock(false);
    } else if (!_globalScreenshotExplicitLock) {
      document.body.classList.remove('app-privacy-locked');
    }
  });

  window.addEventListener('focus', () => {
    // Se foi apenas troca de janela normal (sem tecla de captura), restaura automaticamente ao focar
    if (!_globalScreenshotExplicitLock) {
      document.body.classList.remove('app-privacy-locked');
    }
  });

  // 2. Interceptar PrintScreen e atalhos de captura ou cópia em TODA a aplicação
  const handleCaptureOrCopyKey = (e) => {
    const key = (e.key || '').toLowerCase();
    const isPrintScreen = e.key === 'PrintScreen' || e.keyCode === 44;
    const isWinSnip = e.metaKey && e.shiftKey && (key === 's' || key === '3' || key === '4' || key === '5');
    const isCtrlPrint = (e.ctrlKey || e.metaKey) && key === 'p';
    const isCopyOrCut = (e.ctrlKey || e.metaKey) && (key === 'c' || key === 'x' || key === 'v' || key === 's' || key === 'u');

    if (isPrintScreen || isWinSnip || isCtrlPrint) {
      e.preventDefault();
      e.stopPropagation();
      activateGlobalPrivacyLock(true, '🔒 Captura de ecrã bloqueada! A privacidade no Sigaleve é total.');
      return false;
    }

    if (isCopyOrCut) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof showAppToast === 'function') {
        showAppToast('🔒 Copiar, cortar ou colar informações não é permitido no Sigaleve.', 'error');
      }
      return false;
    }
  };

  window.addEventListener('keydown', handleCaptureOrCopyKey, true);
  window.addEventListener('keyup', (e) => {
    if (e.key === 'PrintScreen' || e.keyCode === 44) {
      activateGlobalPrivacyLock(true, '🔒 Captura de ecrã bloqueada! A privacidade no Sigaleve é total.');
    }
  }, true);

  // 3. Bloquear Copy / Cut / Paste em toda a aplicação (proteção de perfis, chats, fotos e dados)
  ['copy', 'cut', 'paste'].forEach(evtName => {
    document.addEventListener(evtName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (typeof showAppToast === 'function') {
        showAppToast('🔒 Copiar ou colar informações de utilizadores está desativado por segurança.', 'error');
      }
      return false;
    }, true);
  });

  // 4. Bloquear clique direito (menu de contexto / guardar imagem) e arrastar fotos em TODA a aplicação
  document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    return false;
  }, true);

  document.addEventListener('dragstart', (e) => {
    e.preventDefault();
    return false;
  }, true);
}

function dismissChatShield() {
  dismissGlobalPrivacyShield();
}

function isUserSubscribed() {
  // 💳 PAYWALL REAL ATIVO (14/10/26): mensagem ilimitada, perfil completo,
  // álbum e cofre exigem subscrição ativa. O estado vem do SERVIDOR
  // (subscription.expires_at validada) — sem bypass local.
  if (!STATE.currentUser) return false;
  // Subscrição ativa (qualquer plano: Plus, Gold, Platinum)
  const isPlus = !!STATE.currentUser.is_plus;
  const sub = STATE.currentUser.subscription;
  const isSubActive = !!(sub && (sub.active === true || sub.status === 'active'));
  return isPlus || isSubActive;
}

function openChat(peer) {
  // 🔒 BLOQUEIO POR SUBSCRIÇÃO: O CHAT É EXCLUSIVO PARA ASSINANTES
  if (!isUserSubscribed()) {
    showAppToast('💎 O Chat Privado é exclusivo para membros subscritos. Escolhe um plano para conversar!', 'warning');
    openSubscriptionModal('plus');
    return;
  }

  STATE.chatPeer = peer;
  document.getElementById('chat-peer-name').textContent = peer.name;

  // ⏱️ PRESENÇA REAL do peer no header do chat
  try {
    const pd = document.getElementById('chat-peer-presence');
    const dot = document.getElementById('chat-peer-presence-dot');
    let label = peer.presence || '';
    if (!label && peer.last_active) label = presenceLabelFromTs(Number(peer.last_active));
    // sem dados locais → buscar presença real do servidor (async, não bloqueia o chat)
    if (!label || label === 'Offline') {
      fetch(`/api/v1/user/${encodeURIComponent(peer.id)}`).then(r => r.json()).then(j => {
        const prof = (j && j.profile) || {};
        const l2 = prof.presence || presenceLabelFromTs(prof.last_active);
        if (l2 && pd && STATE.chatPeer && String(STATE.chatPeer.id) === String(peer.id)) {
          pd.textContent = l2;
          if (dot) dot.className = 'w-2 h-2 rounded-full inline-block mr-1 transition-colors ' + (l2 === 'Online agora' ? 'bg-green-500 animate-pulse' : 'bg-gray-500');
        }
      }).catch(() => {});
    }
    if (label && pd) pd.textContent = label;
    if (label && dot) dot.className = 'w-2 h-2 rounded-full inline-block mr-1 transition-colors ' + (label === 'Online agora' ? 'bg-green-500 animate-pulse' : 'bg-gray-500');
  } catch (e) {}
  document.getElementById('chat-peer-photo').src = peer.photo;
  document.getElementById('chat-messages').innerHTML = '';
  currentChatMsgIds.clear();
  dismissChatShield();
  showSection('chat');
  initChatAntiScreenshot();

  const myUid = (STATE.currentUser && (STATE.currentUser.id || STATE.currentUser.email)) || 'local_user';

  // Garantir socket ativo (connectRealtime liga ao entrar; fallback aqui)
  connectRealtime();

  if (socket) {
    // Handler da sala: mensagens da conversa aberta (idempotente)
    if (!socket._chatHandlersInstalled) {
      socket.on('new_message', (msgData) => {
        const { sender_id, content, ts, msg_id } = msgData;
        if (msg_id && currentChatMsgIds.has(msg_id)) {
          // Já renderizado otimisticamente pelo próprio remetente
          return;
        }
        if (msg_id) currentChatMsgIds.add(msg_id);
        const isMe = STATE.currentUser ? (String(sender_id) === String(STATE.currentUser.id) || String(sender_id) === String(STATE.currentUser.email)) : false;
        appendBubble(content, isMe, ts);
      });
      socket._chatHandlersInstalled = true;
    }
    const joinChat = () => socket.emit('join_room', { 
      other_user_id: peer.id,
      sender_id: myUid
    });
    if (socket.connected) joinChat();
    else socket.on('connect', joinChat);
  }

  // 💾 HISTÓRICO REAL: carregar mensagens persistidas da conversa (efêmeras 24h)
  (async () => {
    try {
      const res = await fetch(`/api/v1/chat/messages?peer_id=${encodeURIComponent(peer.id)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.success && Array.isArray(data.messages)) {
          for (const m of data.messages) {
            if (m.id && currentChatMsgIds.has(m.id)) continue;
            if (m.id) currentChatMsgIds.add(m.id);
            const isMe = STATE.currentUser ? (String(m.sender_id) === String(STATE.currentUser.id) || String(m.sender_id) === String(STATE.currentUser.email)) : false;
            appendBubble(m.content, isMe, m.ts);
          }
        }
      }
    } catch (e) { /* offline: segue só com tempo real */ }
    // Mostrar quebra-gelos só se a conversa ainda não tem mensagens
    const chatArea2 = document.getElementById('chat-messages');
    if (chatArea2 && chatArea2.children.length === 0) {
      showIcebreakers();
    }
  })();

}

// ═══ QUEBRA-GELO: SUGESTÕES DE PRIMEIRA MENSAGEM ═══
function showIcebreakers() {
  const bar = document.getElementById('icebreaker-bar');
  const chipsBox = document.getElementById('icebreaker-chips');
  if (!bar || !chipsBox) return;
  const d = LANGS[LANG] || {};
  const phrases = d.icebreakers || (LANGS.en && LANGS.en.icebreakers) || [];
  if (!phrases.length) return;
  chipsBox.innerHTML = '';
  // Embaralhar e mostrar 4 sugestões
  const picks = [...phrases].sort(() => Math.random() - 0.5).slice(0, 4);
  picks.forEach(txt => {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.textContent = txt;
    chip.style.background = 'var(--card, #18181b)';
    chip.style.borderColor = 'var(--bdr, #3f3f46)';
    chip.style.color = 'var(--txt, #fff)';
    chip.onclick = () => {
      const inp = document.getElementById('chat-input');
      if (inp) {
        inp.value = txt;
        inp.focus();
        inp.dispatchEvent(new Event('input', {bubbles:true}));
        autoResize(inp);
      }
    };
    chipsBox.appendChild(chip);
  });
  bar.classList.remove('hidden');
}

function hideIcebreakers() {
  const bar = document.getElementById('icebreaker-bar');
  if (bar) bar.classList.add('hidden');
}

function appendBubble(text, isMe, ts) {
  const area = document.getElementById('chat-messages');
  if (!area) return;
  hideIcebreakers();
  const time = ts ? new Date(ts).toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' }) : '';
  const wrap = document.createElement('div');
  wrap.className = 'bubble flex ' + (isMe ? 'justify-end' : 'justify-start');
  const bub = document.createElement('div');
  bub.className = 'max-w-[78%] px-4 py-2.5 rounded-2xl text-xs leading-relaxed shadow-sm ' + (isMe ? 'text-white rounded-br-sm' : 'rounded-bl-sm');
  bub.style.background = isMe ? 'linear-gradient(135deg,#9333ea,#ec4899)' : 'var(--inp)';
  bub.style.color = isMe ? '#fff' : 'var(--txt)';
  
  const p = document.createElement('p'); 
  p.textContent = text; 
  p.className = 'break-words select-none';
  bub.appendChild(p);
  if (time) {
    const t = document.createElement('p');
    t.className = 'text-[10px] mt-1 text-right opacity-70 select-none';
    t.textContent = time;
    bub.appendChild(t);
  }
  wrap.appendChild(bub);
  area.appendChild(wrap);
  area.scrollTop = area.scrollHeight;
}

function sendChat() {
  const inp = document.getElementById('chat-input');
  const text = inp.value.trim();
  if (!text || !STATE.chatPeer) return;

  if (!isUserSubscribed()) {
    showAppToast('💎 É necessária uma subscrição ativa para enviar mensagens no chat.', 'warning');
    openSubscriptionModal('plus');
    return;
  }

  const nowIso = new Date().toISOString();
  const clientMsgId = 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
  currentChatMsgIds.add(clientMsgId);

  // 1. RENDERIZAÇÃO IMEDIATA OTIMISTA (Visível para o próprio remetente sem atraso)
  appendBubble(text, true, nowIso);

  const myUid = (STATE.currentUser && (STATE.currentUser.id || STATE.currentUser.email)) || 'local_user';

  // 2. ENVIO REAL VIA SOCKET.IO (Sem respostas automáticas ou simuladas)
  if (socket && socket.connected) {
    socket.emit('send_message', { 
      other_user_id: STATE.chatPeer.id, 
      sender_id: myUid,
      content: text,
      msg_id: clientMsgId
    });
  }
  inp.value = '';
  autoResize(inp);
}

function handleChatKey(e){ if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); } }
function autoResize(el){ el.style.height = 'auto'; el.style.height = Math.min(el.scrollHeight, 120) + 'px'; }
