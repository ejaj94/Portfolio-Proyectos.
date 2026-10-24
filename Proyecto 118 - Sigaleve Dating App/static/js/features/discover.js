/**
 * Descoberta: baralho de cartões, detalhe de perfil, gestos de swipe e atalhos de teclado.
 */
'use strict';

// ═══════════════════════════════════════════════════
// CARDS & SWIPE (DESCOBERTA HD)
// ═══════════════════════════════════════════════════
async function loadDiscoverProfiles() {
  try {
    // 💀 Skeleton: baralho pulsando enquanto a API responde (em vez de vazio).
    // IMPORTANTE: NÃO usar innerHTML= aqui — o #empty-discover é FILHO do
    // card-stack e seria destruído (bug descoberto em teste).
    const stack = document.getElementById('card-stack');
    if (stack && !stack.querySelector('.s-card') && !stack.querySelector('.skeleton-card')) {
      const sk = document.createElement('div');
      sk.className = 'skeleton-card';
      stack.appendChild(sk);
    }
    const res = await fetch('/api/v1/discover');
    const data = await res.json();
    let rawProfiles = data.profiles || [];
    
    // Obter IDs com quem o utilizador já deu match
    const matchedIds = new Set((MATCHES_DATA || []).map(m => String(m.id)));
    if (STATE.currentUser) {
      try {
        const key = 'sigaleve_matches_' + (STATE.currentUser.id || STATE.currentUser.email);
        const stored = JSON.parse(localStorage.getItem(key) || '[]');
        stored.forEach(m => matchedIds.add(String(m.id)));
      } catch(_) {}
    }

    // Filtrar para que nenhum perfil já com match volte a aparecer no baralho de descoberta
    STATE.profiles = rawProfiles.filter(p => !matchedIds.has(String(p.id)));
    STATE.cursor = 0;
    renderCards();
  } catch (e) {
    console.error('Erro ao carregar perfis:', e);
  }
}

function renderCards() {
  const stack = document.getElementById('card-stack');
  stack.querySelectorAll('.s-card').forEach(c => c.remove());
  // remover o skeleton shimmer se ainda estiver lá
  stack.querySelectorAll('.skeleton-card').forEach(c => c.remove());

  // Garantir que nenhum perfil com match permaneça nos visíveis
  const matchedIds = new Set((MATCHES_DATA || []).map(m => String(m.id)));
  while (STATE.cursor < STATE.profiles.length && matchedIds.has(String(STATE.profiles[STATE.cursor]?.id))) {
    STATE.cursor++;
  }

  const visible = STATE.profiles.slice(STATE.cursor, STATE.cursor + 3).filter(p => !matchedIds.has(String(p.id)));
  if (visible.length === 0) {
    const emptyEl = document.getElementById('empty-discover');
    if (emptyEl) {
      emptyEl.classList.remove('hidden');
      const curDist = localStorage.getItem('sigaleve_pref_distance') || (STATE.currentUser && STATE.currentUser.max_distance) || 50;
      const emptySlider = document.getElementById('empty-distance-slider');
      const emptyDistText = document.getElementById('empty-dist-text');
      if (emptySlider) emptySlider.value = curDist;
      if (emptyDistText) emptyDistText.textContent = `${curDist} Km`;
      const seenEl = document.getElementById('empty-seen-count');
      if (seenEl) {
        const seenN = (typeof STATE !== 'undefined' && STATE.profiles) ? STATE.profiles.length : 0;
        let seenTpl = (typeof T === 'function') ? T('seenProfilesCount') : '';
        if (!seenTpl || String(seenTpl).indexOf('{n}') === -1) seenTpl = 'Viste {n} perfis';
        seenEl.textContent = String(seenTpl).replace('{n}', seenN);
      }
    }
    return;
  }
  document.getElementById('empty-discover').classList.add('hidden');

  for (let i = visible.length - 1; i >= 0; i--) {
    const card = makeCard(visible[i], i);
    stack.appendChild(card);
    if (i === 0) attachGesture(card);
  }
}

function makeCard(p, depth) {
  const card = document.createElement('div');
  card.className = 's-card' + (depth === 0 ? ' top' : '');
  card.dataset.pid = p.id;
  card.dataset.photoIdx = '0';
  if (depth > 0) card.dataset.depth = depth;

  const diagColors = { A:'#9333ea', B:'#3b82f6', C:'#10b981', D:'#f59e0b', E:'#ef4444', F:'#8b5cf6' };
  const diagColor = diagColors[p.code] || '#9333ea';
  const interestsHTML = (p.interests || []).slice(0, 3).map(t => `<span class="tag">${esc(t)}</span>`).join('');
  const photos = (p.photos && p.photos.length) ? p.photos : [p.photo];

  // Render story indicators matching number of photos
  let barsHTML = '';
  photos.forEach((_, idx) => {
    barsHTML += `<div class="story-bar ${idx === 0 ? 'active' : ''}" data-idx="${idx}"></div>`;
  });

  card.innerHTML = `
    <span class="sw-ind ind-like">${T('cardLike')}</span>
    <span class="sw-ind ind-nope">${T('cardNope')}</span>
    <span class="sw-ind ind-super">${T('cardSuper')}</span>
    <div class="heart-stamp"><i class="fa-solid fa-heart"></i></div>
    <div class="relative w-full h-full">
      <!-- Story progress indicators like Tinder -->
      <div class="story-bars pointer-events-none">
        ${barsHTML}
      </div>

      <!-- Tap zones: Click left half for previous photo, right half for next photo -->
      <div class="tap-zone left" onclick="changeCardPhoto('${p.id}', -1, event)"></div>
      <div class="tap-zone right" onclick="changeCardPhoto('${p.id}', 1, event)"></div>

      <img src="${photos[0]}" class="card-img" alt="${esc(p.name)}" ondragstart="return false" oncontextmenu="return false" onerror="if(!this.dataset.fb){this.dataset.fb=1;this.src='/static/img/avatar-fallback.svg';}"/>
      <div class="card-overlay"></div>
      ${p.verified ? '<div class="ver absolute top-6 left-4 z-30"><i class="fa-solid fa-certificate text-xs"></i> ' + T('verified') + '</div>' : ''}
      
      <!-- 📱 UX MOBILE: painel de infos todo clicável abre o perfil (padrão Tinder);
           swipes continuam funcionando porque o gesto ignora cliques em elementos
           filhos (e.target.closest('button')) e o toque curto não arrasta o card -->
      <div class="card-info z-30 pointer-events-auto" onclick="openProfileDetail('${p.id}')">
        <!-- Badge de Actividad Reciente idéntico a Tinder -->
        <div class="flex items-center gap-1.5 mb-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 inline-block shadow-[0_0_6px_#34d399]"></span>
          <span class="text-xs text-white/95 font-semibold tracking-wide">${T('recentActivityTag')}</span>
        </div>

        <div class="flex items-center justify-between gap-2">
          <h2 class="text-3xl font-black text-white leading-tight flex items-center gap-2 truncate tracking-tight">
            <span>${esc(p.name)}</span>
            <span class="font-normal text-2xl text-white/90">${p.age}</span>
            ${p.verified ? '<i class="fa-solid fa-circle-check text-sky-400 text-lg flex-shrink-0"></i>' : ''}
          </h2>

          <!-- Ícone Branco de Abrir Perfil Estilo Tinder (Up Arrowhead) -->
          <button type="button" onclick="event.stopPropagation(); openProfileDetail('${p.id}')" class="w-11 h-11 -mr-2 flex items-center justify-center text-white/90 hover:text-white transition-transform active:scale-90 flex-shrink-0 cursor-pointer" style="touch-action:manipulation" title="Abrir perfil">
            <svg class="w-6 h-6 fill-current" viewBox="0 0 24 24"><path d="M12 4l-8 8h5v8h6v-8h5z"/></svg>
          </button>
        </div>

        <!-- Meta / Ocupação / Trabalho com ícones idênticos a Tinder -->
        <div class="mt-2 space-y-0.5 text-xs text-white/90 font-medium">
          ${p.occupation || p.education ? `
            <p class="flex items-center gap-1.5 truncate">
              <span class="text-sm">💼</span>
              <span>${esc(p.occupation || p.education || T('cardWorkDefault'))}</span>
            </p>
          ` : ''}
          ${p.lifestyle || p.city ? `
            <p class="flex items-center gap-1.5 truncate">
              <span class="text-sm">🧭</span>
              <span>${esc(p.city ? T('cardLivesIn') + ' ' + p.city : T('cardTravelDefault'))}</span>
            </p>
          ` : ''}
        </div>

        <!-- Biografía / Lo que busca -->
        ${p.bio ? `
          <div class="mt-2.5">
            <p class="text-white/90 text-xs line-clamp-2 leading-relaxed font-normal">${esc(p.bio)}</p>
            <p class="text-white/60 text-xs font-bold tracking-widest mt-0.5">...</p>
          </div>
        ` : ''}

        <!-- Prompt de Conversa (gancho estilo Hinge) -->
        ${p.profile_prompt ? `
          <div class="mt-2.5 px-3 py-2 rounded-xl bg-black/35 border border-white/15 backdrop-blur-sm">
            <p class="text-[10px] font-black uppercase tracking-wider text-pink-300/90 flex items-center gap-1">
              <i class="fa-solid fa-comment-dots"></i> ${T('cardAskMe')}
            </p>
            <p class="text-white text-xs font-semibold leading-snug mt-0.5">${esc(p.profile_prompt)}</p>
          </div>
        ` : ''}
      </div>
    </div>`;
  return card;
}

function esc(s){ const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

// Navegação de fotos por clique (Tap Story)
function changeCardPhoto(pid, dir, ev) {
  if (ev) ev.stopPropagation();
  const card = document.querySelector(`.s-card[data-pid="${pid}"]`);
  if (!card) return;
  const p = STATE.profiles.find(item => item.id === pid);
  if (!p) return;
  const photos = (p.photos && p.photos.length) ? p.photos : [p.photo];
  let currentIdx = parseInt(card.dataset.photoIdx || '0', 10);
  let nextIdx = currentIdx + dir;
  if (nextIdx < 0) nextIdx = 0;
  if (nextIdx >= photos.length) nextIdx = photos.length - 1;

  if (nextIdx !== currentIdx) {
    card.dataset.photoIdx = nextIdx;
    const img = card.querySelector('.card-img');
    if (img) img.src = photos[nextIdx];

    // Atualizar barras de história
    const bars = card.querySelectorAll('.story-bar');
    bars.forEach((b, idx) => {
      b.classList.toggle('active', idx === nextIdx);
    });
  }
}

// Abertura do Perfil Completo estilo Tinder Web (↑ Abrir perfil)
let currentDetailProfile = null;
let currentDetailPhotoIdx = 0;

function changeDetailModalPhoto(dir, ev) {
  if (ev) ev.stopPropagation();
  if (!currentDetailProfile) return;
  const photos = (currentDetailProfile.photos && currentDetailProfile.photos.length) ? currentDetailProfile.photos : [currentDetailProfile.photo];
  if (!photos || photos.length <= 1) return;
  currentDetailPhotoIdx += dir;
  if (currentDetailPhotoIdx < 0) currentDetailPhotoIdx = 0;
  if (currentDetailPhotoIdx >= photos.length) currentDetailPhotoIdx = photos.length - 1;
  
  const imgEl = document.getElementById('detail-photo');
  if (imgEl) imgEl.src = photos[currentDetailPhotoIdx];

  const bars = document.querySelectorAll('#detail-story-bars .story-bar');
  bars.forEach((b, idx) => {
    b.classList.toggle('active', idx === currentDetailPhotoIdx);
  });
}

async function openProfileDetail(target) {
  // 🔒 BLOQUEIO POR SUBSCRIÇÃO: VER PERFIL COMPLETO É EXCLUSIVO PARA ASSINANTES
  if (!isUserSubscribed()) {
    showAppToast('👑 Ver o perfil completo de outros membros é um recurso exclusivo para membros com subscrição ativa.', 'warning');
    openSubscriptionModal('gold');
    return;
  }

  let p = null;
  if (typeof target === 'object' && target !== null) {
    p = target;
  } else if (typeof target === 'string') {
    p = (STATE.profiles || []).find(item => item.id === target);
    if (!p) {
      p = (MATCHES_DATA || []).find(item => item.id === target);
    }
    if (!p) {
      try {
        const res = await fetch(`/api/v1/user/${encodeURIComponent(target)}`);
        if (res.ok) {
          const data = await res.json();
          p = data.profile;
        }
      } catch(e) {
        console.error('Erro ao buscar perfil remoto:', e);
      }
    }
  }

  if (!p) return;
  currentDetailProfile = p;
  currentDetailPhotoIdx = 0;

  document.getElementById('detail-name').textContent = p.name || 'Utilizador';
  document.getElementById('detail-age').textContent = p.age || '';
  document.getElementById('detail-bio').textContent = p.bio || 'Sem descrição.';

  const promptBox = document.getElementById('detail-prompt-box');
  const promptText = document.getElementById('detail-prompt-text');
  if (promptBox && promptText) {
    if (p.profile_prompt) {
      promptText.textContent = p.profile_prompt;
      promptBox.classList.remove('hidden');
    } else {
      promptBox.classList.add('hidden');
    }
  }
  // 📍 km agora é a cidade (ou "Perto de ti") — evitar "Lisboa • Lisboa"
  const locLabel = (p.km && p.km !== p.city) ? `${p.city || 'Portugal'} • ${p.km}` : (p.km || p.city || 'Portugal');
  document.getElementById('detail-location').textContent = locLabel;
  document.getElementById('detail-activity').textContent = p.presence || p.activity || presenceLabelFromTs(p.last_active) || 'Ativo recentemente';

  const goalEl = document.getElementById('detail-goal');
  if (goalEl) goalEl.textContent = p.relationship_goal || 'Algo sério, mas veremos';
  const goalIconEl = document.getElementById('detail-goal-icon');
  if (goalIconEl) goalIconEl.textContent = p.goal_icon || '🥂';

  document.getElementById('detail-zodiac').textContent = p.zodiac || 'Touro';
  document.getElementById('detail-edu').textContent = p.education || 'Licenciatura';
  document.getElementById('detail-height').textContent = p.height || '175 cm';
  document.getElementById('detail-lifestyle').textContent = p.lifestyle || 'Ativo / Desportivo';

  const diagColors = { A:'#9333ea', B:'#3b82f6', C:'#10b981', D:'#f59e0b', E:'#ef4444', F:'#8b5cf6' };
  const diagCode = p.code || (p.diagnosis ? p.diagnosis.charAt(0).toUpperCase() : 'A');
  const diagColor = diagColors[diagCode] || '#9333ea';
  const badge = document.getElementById('detail-code-badge');
  if (badge) {
    badge.textContent = `Tipo ${diagCode} (ETS)`;
    badge.style.background = diagColor + '33';
    badge.style.borderColor = diagColor;
  }

  const verEl = document.getElementById('detail-verified');
  if (verEl) verEl.style.display = p.verified ? 'inline-block' : 'none';

  const photos = (p.photos && p.photos.length) ? p.photos : [p.photo || ''];
  const photoEl = document.getElementById('detail-photo');
  if (photoEl) photoEl.src = photos[0];

  const barsBox = document.getElementById('detail-story-bars');
  if (barsBox) {
    barsBox.innerHTML = '';
    photos.forEach((_, idx) => {
      const bar = document.createElement('div');
      bar.className = 'story-bar' + (idx === 0 ? ' active' : '');
      barsBox.appendChild(bar);
    });
  }

  const interestsBox = document.getElementById('detail-interests');
  if (interestsBox) {
    interestsBox.innerHTML = '';
    (p.interests || []).forEach(it => {
      const sp = document.createElement('span');
      sp.className = 'px-3 py-1.5 rounded-full text-xs font-semibold border flex items-center gap-1.5';
      sp.style.borderColor = 'var(--bdr)';
      sp.style.background = 'var(--inp)';
      sp.textContent = it;
      interestsBox.appendChild(sp);
    });
  }

  const modal = document.getElementById('profile-detail-modal');
  if (modal) {
    modal.classList.add('open');
    modal.scrollTop = 0;
  }
}

function closeProfileDetail() {
  const modal = document.getElementById('profile-detail-modal');
  if (modal) modal.classList.remove('open');
  currentDetailProfile = null;
  currentDetailPhotoIdx = 0;
}

// Volta do chat para a lista de conversas/matches (sem limpar STATE.chatPeer,
// para que seja possível reabrir o chat e o perfil do peer no mesmo contexto)
// ⏱️ PRESENÇA: converte last_active (epoch seg) em rótulo honesto
function presenceLabelFromTs(ts) {
  if (!ts || isNaN(Number(ts))) return '';
  const elapsed = (Date.now() / 1000) - Number(ts);
  if (elapsed < 120) return 'Online agora';
  if (elapsed < 3600) return 'Ativo há pouco';
  if (elapsed < 86400) return 'Ativo recentemente';
  if (elapsed < 7 * 86400) return 'Ativo esta semana';
  return 'Offline';
}

// 💓 Heartbeat: enquanto o app está aberto, pinge a presença a cada 60s
(function startPresenceHeartbeat() {
  setInterval(async () => {
    try { await fetch('/api/v1/presence/heartbeat', {method: 'POST'}); } catch (e) {}
  }, 60000);
})();

// 🔒 O e-mail é fixo por segurança (anti-sequestro de conta) — explicar ao tocar
function openEmailChangePrompt() {
  showAppToast('🔒 Por segurança, o e-mail não pode ser alterado. Fala com o suporte se precisares.', 'info');
}

function goBackFromChat() {
  showSection('matches');
}

// Abre o perfil completo do peer a partir do chat: STATE.chatPeer é um objeto
// simplificado {id, name, photo}, por isso busca o perfil remoto e faz merge
async function openPeerProfileFromChat() {
  if (!STATE.chatPeer) return;
  let p = STATE.chatPeer;
  try {
    const res = await fetch(`/api/v1/user/${encodeURIComponent(STATE.chatPeer.id)}`);
    if (res.ok) {
      const data = await res.json();
      const remote = data && data.profile;
      if (remote) p = Object.assign({}, STATE.chatPeer, remote);
    }
  } catch (e) {
    console.error('Erro ao buscar perfil do peer do chat:', e);
  }
  openProfileDetail(p);
}

// GESTOS TÁCTEIS E DE RATO
function attachGesture(card) {
  let x0 = 0, y0 = 0, dx = 0, dragging = false, raf = null;
  const THRESH = 90;
  const likeEl = card.querySelector('.ind-like');
  const nopeEl = card.querySelector('.ind-nope');
  const superEl = card.querySelector('.ind-super');

  const px = e => e.touches ? e.touches[0].clientX : e.clientX;
  const py = e => e.touches ? e.touches[0].clientY : e.clientY;

  function start(e) {
    if (!card.classList.contains('top')) return;
    // Don't drag if clicking buttons or expand
    if (e.target.closest('button')) return;
    // 📱 UX MOBILE: o painel de infos (card-info) é tocável p/ abrir o perfil;
    // arrastar a partir dele não move o card (o clique curto já abre o perfil)
    if (e.target.closest('.card-info')) return;
    dragging = true; x0 = px(e); y0 = py(e); dx = 0;
    card.style.transition = 'none';
  }
  function move(e) {
    if (!dragging) return;
    const ddx = px(e) - x0, ddy = py(e) - y0;
    if (Math.abs(ddy) > Math.abs(ddx) * 1.8) { cancel(); return; }
    if (e.cancelable) e.preventDefault();
    dx = ddx;
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => {
      const rot = dx * 0.07;
      card.style.transform = `translateX(${dx}px) rotate(${rot}deg)`;
      const r = Math.min(Math.abs(dx) / THRESH, 1);
      if (dx > 10) { likeEl.style.opacity = r; nopeEl.style.opacity = 0; superEl.style.opacity = 0; }
      else if (dx < -10) { nopeEl.style.opacity = r; likeEl.style.opacity = 0; superEl.style.opacity = 0; }
      else { likeEl.style.opacity = 0; nopeEl.style.opacity = 0; superEl.style.opacity = 0; }
    });
  }
  function end() {
    if (!dragging) return; dragging = false;
    if (raf) cancelAnimationFrame(raf);
    if (dx > THRESH) exitCard(card, 'like');
    else if (dx < -THRESH) exitCard(card, 'nope');
    else snapBack(card);
  }
  function cancel() { dragging = false; if (raf) cancelAnimationFrame(raf); snapBack(card); }

  card.addEventListener('touchstart', start, { passive: true });
  card.addEventListener('touchmove', move, { passive: false });
  card.addEventListener('touchend', end, { passive: true });
  card.addEventListener('touchcancel', cancel, { passive: true });
  card.addEventListener('mousedown', start);
  document.addEventListener('mousemove', move);
  document.addEventListener('mouseup', end);
}

function snapBack(card) {
  card.style.transition = 'transform .3s cubic-bezier(.34,1.56,.64,1)';
  card.style.transform = '';
  card.querySelectorAll('.sw-ind').forEach(el => el.style.opacity = 0);
}

function exitCard(card, action) {
  closeProfileDetail();
  if (action === 'like') {
    const stamp = card.querySelector('.heart-stamp');
    if (stamp) stamp.classList.add('show');
  }
  card.classList.add(action === 'like' ? 'exit-r' : action === 'super' ? 'exit-u' : 'exit-l');
  const pid = card.dataset.pid;
  const profile = STATE.profiles.find(p => p.id === pid);

  if (action === 'like' || action === 'super') {
    fetch('/api/v1/like', { 
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_id: pid })
    }).then(r => r.json()).then(data => {
      // APENAS mostrar Match se o backend confirmar que houve MATCH MÚTUO REAL
      if (data && data.matched && profile) {
        showMatchOverlay(profile);
      }
    }).catch(() => {});
  } else if (action === 'nope') {
    fetch('/api/v1/skip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_id: pid })
    }).catch(() => {});
  }

  // Remover de imediato do baralho local para que nunca mais reapareça nesta sessão
  if (STATE.profiles) {
    STATE.profiles = STATE.profiles.filter(p => String(p.id) !== String(pid));
  }

  setTimeout(() => {
    STATE.cursor++;
    renderCards();
  }, 420);
}

function swipe(act){
  const top = document.querySelector('.s-card.top');
  if (top) exitCard(top, act);
}
function undoSwipe(){
  if (STATE.cursor > 0) { STATE.cursor--; renderCards(); }
}
function expandDistanceAndReload() {
  const slider = document.getElementById('pref-distance-slider');
  const distText = document.getElementById('pref-dist-text');
  if (slider) {
    let current = parseInt(slider.value, 10) || 50;
    let nextVal = Math.min(160, current + 50);
    slider.value = nextVal;
    if (distText) distText.textContent = nextVal + ' Km';
    localStorage.setItem('sigaleve_pref_distance', String(nextVal));
    saveDistancePref(nextVal);
  }
  resetDiscover();
}

function handleEmptyDistanceChange(val) {
  const num = parseInt(val, 10);
  const textEl = document.getElementById('empty-dist-text');
  if (textEl) textEl.textContent = `${num} Km`;
  const drawerSlider = document.getElementById('pref-distance-slider');
  const drawerText = document.getElementById('pref-dist-text');
  if (drawerSlider) drawerSlider.value = num;
  if (drawerText) drawerText.textContent = `${num} Km`;
}

function applyNewDistanceAndReload() {
  const slider = document.getElementById('empty-distance-slider');
  const val = slider ? parseInt(slider.value, 10) : 50;
  localStorage.setItem('sigaleve_pref_distance', String(val));
  saveDistancePref(val);
  resetDiscover();
}

function resetDiscover(){
  const emptyEl = document.getElementById('empty-discover');
  if (emptyEl) emptyEl.classList.add('hidden');
  STATE.cursor = 0;
  loadDiscoverProfiles();
}

async function revertSkippedProfiles(){
  try {
    await fetch('/api/v1/profile/reset-skipped', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (e) {
    console.error('Erro ao reverter perfis passados:', e);
  }
  resetDiscover();
}
function _oldResetDiscover(){
  STATE.cursor = 0; renderCards();
}

// ── ATALHOS DE TECLADO TINDER (← No, → Like, ↑ Abrir perfil, ↓ Cerrar perfil, Espaço Super Like, Enter Próxima Foto) ──
function toggleKeyboardHintBar() {
  const bar = document.getElementById('keyboard-hint-bar');
  if (bar) {
    bar.classList.toggle('hidden');
    const isHidden = bar.classList.contains('hidden');
    localStorage.setItem('sigaleve_hide_keyboard_hints', isHidden ? 'true' : 'false');
  }
}

window.addEventListener('keydown', (e) => {
  // Ignorar se o usuário estiver digitando em campos de texto ou modais de entrada
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : '';
  if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) return;

  const currentSection = STATE.currentSection || 'discover';
  if (currentSection !== 'discover') return;

  // Verificar se os atalhos estão ativos
  const tog = document.getElementById('tog-keyboard-shortcuts');
  if (tog && !tog.classList.contains('on')) return;

  const topCard = document.querySelector('.s-card.top');
  const detailModal = document.getElementById('profile-detail-modal');
  const isDetailOpen = detailModal && detailModal.classList.contains('open');

  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    if (isDetailOpen) closeProfileDetail();
    swipe('nope');
  } else if (e.key === 'ArrowRight') {
    e.preventDefault();
    if (isDetailOpen) closeProfileDetail();
    swipe('like');
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    if (topCard && !isDetailOpen) {
      const pid = topCard.dataset.pid;
      if (pid) openProfileDetail(pid);
    }
  } else if (e.key === 'ArrowDown') {
    e.preventDefault();
    if (isDetailOpen) {
      closeProfileDetail();
    }
  } else if (e.code === 'Space' || e.key === ' ') {
    e.preventDefault();
    if (isDetailOpen) closeProfileDetail();
    swipe('super');
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (topCard) {
      const pid = topCard.dataset.pid;
      if (pid) changeCardPhoto(pid, 1);
    }
  }
});
