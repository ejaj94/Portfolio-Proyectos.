/**
 * Matches: overlay de match, confetes, lista de conversas e separadores da sidebar.
 */
'use strict';

// ═══════════════════════════════════════════════════
// MATCHES & CHAT
// ═══════════════════════════════════════════════════
let MATCHES_DATA = [];

let matchedProfile = null;
function showMatchOverlay(p) {
  matchedProfile = p;
  document.getElementById('match-their-photo').src = p.photo;
  document.getElementById('match-overlay').classList.remove('hidden');
  burstConfetti();

  // Adicionar novo match à lista em tempo real se ainda não existir
  if (!MATCHES_DATA.some(m => m.id === p.id)) {
    MATCHES_DATA.unshift({
      id: p.id,
      name: p.name,
      photo: p.photo,
      lastMsg: 'Novo match! Inicia a conversa 👋',
      time: 'Agora',
      isNew: true
    });
    if (STATE.currentUser) {
      try {
        localStorage.setItem('sigaleve_matches_' + (STATE.currentUser.id || STATE.currentUser.email), JSON.stringify(MATCHES_DATA));
      } catch(e){}
    }
    renderMatches();
  }

  // 🚫 NUNCA MAIS MOSTRAR O PERFIL NO BARALHO SE JÁ HOUVE MATCH
  if (STATE.profiles && STATE.profiles.length > 0) {
    STATE.profiles = STATE.profiles.filter(item => String(item.id) !== String(p.id));
    if (STATE.cursor >= STATE.profiles.length) {
      STATE.cursor = Math.max(0, STATE.profiles.length - 1);
    }
    renderCards();
  }
}
function closeMatch(){ document.getElementById('match-overlay').classList.add('hidden'); }

// 🎉 Confete no match: 18 partículas CSS geradas uma vez por match
function burstConfetti() {
  const c = document.getElementById('confetti-container');
  if (!c) return;
  c.innerHTML = '';
  const cores = ['#fbbf24', '#f472b6', '#a78bfa', '#34d399', '#60a5fa', '#ffffff'];
  for (let i = 0; i < 18; i++) {
    const p = document.createElement('span');
    p.className = 'confetti';
    p.style.left = (Math.random() * 100) + '%';
    p.style.background = cores[i % cores.length];
    p.style.animationDuration = (1.8 + Math.random() * 1.6) + 's';
    p.style.animationDelay = (Math.random() * 0.5) + 's';
    p.style.width = (6 + Math.random() * 6) + 'px';
    p.style.height = (10 + Math.random() * 8) + 'px';
    if (i % 3 === 0) p.style.borderRadius = '50%';
    c.appendChild(p);
  }
}
function goToChat(){
  closeMatch();
  if (matchedProfile) openChat(matchedProfile);
}

// ═══════════════════════════════════════════════════
// TABS E NAVEGAÇÃO DA SIDEBAR DESKTOP
// ═══════════════════════════════════════════════════
function switchSidebarTab(tab) {
  const tabMatches = document.getElementById('sidebar-tab-matches');
  const tabMessages = document.getElementById('sidebar-tab-messages');
  const secNewMatches = document.getElementById('sidebar-new-matches-sec');

  if (tab === 'matches') {
    if (tabMatches) {
      tabMatches.className = 'pb-2.5 text-xs font-black uppercase tracking-wider text-purple-600 border-b-2 border-purple-600 transition-all flex items-center gap-1.5';
    }
    if (tabMessages) {
      tabMessages.className = 'pb-2.5 text-xs font-black uppercase tracking-wider text-gray-400 hover:text-white transition-all flex items-center gap-1.5';
    }
    if (secNewMatches) secNewMatches.style.display = 'block';
  } else {
    if (tabMessages) {
      tabMessages.className = 'pb-2.5 text-xs font-black uppercase tracking-wider text-purple-600 border-b-2 border-purple-600 transition-all flex items-center gap-1.5';
    }
    if (tabMatches) {
      tabMatches.className = 'pb-2.5 text-xs font-black uppercase tracking-wider text-gray-400 hover:text-white transition-all flex items-center gap-1.5';
    }
    if (secNewMatches) secNewMatches.style.display = 'none';
  }
}

function renderMatches() {
  const count = MATCHES_DATA.length;
  
  // Atualizar contadores visuais de matches (Mobile badge e Desktop sidebar badge)
  const deskBadge = document.getElementById('sidebar-match-badge');
  if (deskBadge) deskBadge.textContent = count;
  const mobBadge = document.getElementById('matches-badge');
  if (mobBadge) mobBadge.textContent = count;
  const profMatches = document.getElementById('prof-stat-matches');
  if (profMatches) profMatches.textContent = count;

  // 1. Mobile Horizontal Matches
  const row = document.getElementById('new-matches-row');
  if (row) {
    row.innerHTML = '';
    if (count === 0) {
      row.innerHTML = `
        <div class="w-full py-4 text-center text-xs text-gray-400 font-medium">
          <i class="fa-solid fa-sparkles text-purple-400 mb-1 block text-base"></i>
          ${T('noNewMatchesMobile')}
        </div>`;
    } else {
      MATCHES_DATA.forEach(m => {
        const div = document.createElement('div');
        div.className = 'flex flex-col items-center gap-1.5 cursor-pointer flex-shrink-0 group';
        div.style.width = '70px';
        div.innerHTML = `
          <div class="avatar-ring transition-transform group-hover:scale-105" style="${m.isNew ? '' : 'background:#94a3b8'}" title="Ver perfil de ${esc(m.name)}">
            <img src="${m.photo}" alt="${esc(m.name)}" style="width:100%;height:100%;border-radius:50%;object-fit:cover;border:2px solid var(--bg)"/>
          </div>
          <p class="text-xs font-bold truncate w-full text-center group-hover:text-purple-400 transition-colors">${esc(m.name.split(' ')[0])}</p>`;
        div.onclick = (e) => {
          openProfileDetail(m);
        };
        row.appendChild(div);
      });
    }
  }

  // 2. Mobile Conversations List
  const list = document.getElementById('messages-list');
  const noMatchesEl = document.getElementById('no-matches');
  if (list) {
    list.innerHTML = '';
    if (count === 0) {
      if (noMatchesEl) noMatchesEl.classList.remove('hidden');
    } else {
      if (noMatchesEl) noMatchesEl.classList.add('hidden');
      MATCHES_DATA.forEach(m => {
        const div = document.createElement('div');
        div.className = 'match-item group';
        div.innerHTML = `
          <div class="relative flex-shrink-0 cursor-pointer" onclick="event.stopPropagation(); openProfileDetail('${m.id}')" title="Ver perfil de ${esc(m.name)}">
            <img src="${m.photo}" class="avatar-sm hover:ring-2 hover:ring-purple-500 transition-all" alt=""/>
            ${m.isNew ? '<span class="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-purple-600 border-2" style="border-color:var(--bg)"></span>' : ''}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-baseline justify-between">
              <p class="font-black text-sm">${esc(m.name)}</p>
              <p class="text-[11px] font-semibold flex-shrink-0 ml-2" style="color:var(--sub)">${esc(m.time)}</p>
            </div>
            <p class="text-xs truncate mt-0.5 ${m.isNew ? 'font-bold text-purple-600' : 'text-gray-500'}">${esc(m.lastMsg)}</p>
          </div>
          <button type="button" onclick="event.stopPropagation(); openProfileDetail('${m.id}')" class="p-2 text-zinc-400 hover:text-white rounded-full hover:bg-white/5 transition-all" title="Ver perfil">
            <i class="fa-solid fa-circle-info text-sm"></i>
          </button>`;
        div.onclick = () => openChat(m);
        list.appendChild(div);
      });
    }
  }

  // 3. Desktop Sidebar Matches Grid (Tinder Web Style)
  const deskGrid = document.getElementById('desktop-matches-grid');
  if (deskGrid) {
    deskGrid.innerHTML = '';
    if (count === 0) {
      deskGrid.innerHTML = `
        <div class="col-span-3 py-6 px-3 text-center rounded-2xl border border-dashed border-gray-700/50 bg-white/[0.02]">
          <div class="w-10 h-10 rounded-full mx-auto mb-2 flex items-center justify-center bg-purple-500/10 text-purple-400">
            <i class="fa-solid fa-heart-crack text-sm"></i>
          </div>
          <p class="text-xs font-bold text-gray-300">${T('noMatchesYet')}</p>
          <p class="text-[11px] text-gray-500 mt-1">${T('likeProfilesToChat')}</p>
        </div>`;
    } else {
      MATCHES_DATA.forEach(m => {
        const item = document.createElement('div');
        item.className = 'flex flex-col items-center p-2 rounded-xl hover:bg-white/5 cursor-pointer transition-all group';
        item.innerHTML = `
          <div class="relative w-14 h-14 rounded-full p-0.5 mb-1 group-hover:scale-105 transition-transform" style="background:linear-gradient(135deg,#9333ea,#ec4899)" title="Ver perfil de ${esc(m.name)}">
            <img src="${m.photo}" class="w-full h-full rounded-full object-cover border-2" style="border-color:var(--bg)"/>
            ${m.isNew ? '<span class="absolute 0 top-0 right-0 w-3.5 h-3.5 rounded-full bg-pink-500 border-2" style="border-color:var(--bg)"></span>' : ''}
          </div>
          <p class="text-[11px] font-bold truncate max-w-[65px] text-center group-hover:text-purple-400 transition-colors">${esc(m.name.split(' ')[0])}</p>`;
        item.onclick = () => openProfileDetail(m);
        deskGrid.appendChild(item);
      });
    }
  }

  // 4. Desktop Sidebar Conversations List
  const deskList = document.getElementById('desktop-conversations-list');
  if (deskList) {
    deskList.innerHTML = '';
    if (count === 0) {
      deskList.innerHTML = `
        <div class="p-6 text-center text-xs text-gray-400">
          <i class="fa-regular fa-comments text-2xl text-gray-600 mb-2 block"></i>
          ${T('noConversationsYet')}<br/>${T('messagesAppearHere')}
        </div>`;
    } else {
      MATCHES_DATA.forEach(m => {
        const div = document.createElement('div');
        div.className = 'flex items-center gap-3 p-2.5 rounded-xl cursor-pointer hover:bg-white/5 transition-all group';
        div.innerHTML = `
          <div class="relative flex-shrink-0 w-12 h-12 cursor-pointer" onclick="event.stopPropagation(); openProfileDetail('${m.id}')" title="Ver perfil de ${esc(m.name)}">
            <img src="${m.photo}" class="w-12 h-12 rounded-full object-cover group-hover:ring-2 group-hover:ring-purple-500 transition-all"/>
            ${m.isNew ? '<span class="absolute top-0 right-0 w-3 h-3 rounded-full bg-purple-600 border-2" style="border-color:var(--card)"></span>' : ''}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-xs truncate">${esc(m.name)}</h4>
              <span class="text-[10px] text-gray-400 ml-1 flex-shrink-0">${esc(m.time)}</span>
            </div>
            <p class="text-[11px] truncate mt-0.5 ${m.isNew ? 'font-bold text-purple-400' : 'text-gray-400'}">${esc(m.lastMsg)}</p>
          </div>
          <button type="button" onclick="event.stopPropagation(); openProfileDetail('${m.id}')" class="p-1.5 text-zinc-400 hover:text-white rounded-full hover:bg-white/10 transition-all" title="Ver perfil">
            <i class="fa-solid fa-circle-info text-xs"></i>
          </button>`;
        div.onclick = () => openChat(m);
        deskList.appendChild(div);
      });
    }
  }
}
