/**
 * Comunidade: Q&A de saúde, ideias de encontros em grupo (com comentários) e histórias de sucesso.
 */
'use strict';

if (typeof window.esc !== 'function') {
  window.esc = function(s) {
    if (s === null || s === undefined) return '';
    const d = document.createElement('div');
    d.textContent = String(s);
    return d.innerHTML;
  };
}
var esc = window.esc;

// ═══════════════════════════════════════════════════
// COMUNIDADE & SAÚDE — Q&A ANÓNIMO
// ═══════════════════════════════════════════════════
let QA_CURRENT_CATEGORY = '';

function selectQaCategory(btn, cat) {
  document.querySelectorAll('.qa-cat-chip').forEach(c => {
    c.classList.remove('active', 'bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/50');
    c.classList.add('bg-zinc-900', 'border-zinc-800', 'text-zinc-300');
  });
  btn.classList.add('active', 'bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/50');
  btn.classList.remove('bg-zinc-900', 'border-zinc-800', 'text-zinc-300');
  QA_CURRENT_CATEGORY = cat;
  loadQaList();
}

async function loadQaList() {
  try {
    const url = QA_CURRENT_CATEGORY ? `/api/v1/qa-health?category=${encodeURIComponent(QA_CURRENT_CATEGORY)}` : '/api/v1/qa-health';
    const res = await fetch(url);
    const data = await res.json();
    renderQaList(data.questions || []);
  } catch (e) {
    console.error('Erro ao carregar Q&A:', e);
  }
}

function qaCatLabel(cat) {
  const map = { diagnostico: '🩺 Diagnóstico', tratamento: '💊 Tratamento' };
  return map[cat] || cat;
}

function qaTimeAgo(ts) {
  const s = Math.max(1, Math.floor(Date.now() / 1000 - ts));
  if (s < 3600) return 'há ' + Math.max(1, Math.floor(s / 60)) + ' min';
  if (s < 86400) return 'há ' + Math.floor(s / 3600) + ' h';
  if (s < 2592000) return 'há ' + Math.floor(s / 86400) + ' dias';
  return 'há ' + Math.floor(s / 2592000) + ' meses';
}

function renderQaList(questions) {
  const list = document.getElementById('qa-list');
  const empty = document.getElementById('qa-empty');
  if (!list) return;
  if (!questions.length) {
    list.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');
  list.innerHTML = questions.map(q => {
    const answersHtml = (q.answers || []).map(a => `
      <div class="ml-2 sm:ml-4 pl-3 border-l-2 border-emerald-500/30 py-2">
        <div class="flex items-center justify-between mb-1">
          <p class="text-[10px] font-bold text-emerald-300/80">${esc(a.author || 'Membro')} <span class="text-zinc-600">· ${qaTimeAgo(a.created_at || 0)}</span></p>
          <button type="button" onclick="likeQaAnswer('${q.id}', '${a.id}', this)" class="text-[10px] font-bold text-zinc-400 hover:text-emerald-300 transition-colors flex items-center gap-1">
            <i class="fa-solid fa-heart"></i> <span class="qa-likes-count">${a.likes || 0}</span>
          </button>
        </div>
        <p class="text-[11px] leading-relaxed" style="color:var(--txt)">${esc(a.text || '')}</p>
      </div>
    `).join('');

    return `
      <div class="rounded-3xl p-3.5 sm:p-4 border shadow-xl qa-card" style="background:var(--card);border-color:var(--bdr)">
        <div class="flex items-center gap-2 flex-wrap mb-1.5">
          <span class="text-[10px] bg-zinc-800 text-zinc-300 px-2 py-0.5 rounded-full font-bold">${qaCatLabel(q.category)}</span>
          <span class="text-[10px] text-zinc-500">${qaTimeAgo(q.created_at || 0)}</span>
        </div>
        <h4 class="text-sm font-black text-white leading-snug mb-1">${esc(q.question || '')}</h4>
        ${q.question_detail ? `<p class="text-[11px] text-zinc-400 leading-relaxed mb-2">${esc(q.question_detail)}</p>` : ''}

        <div class="flex items-center justify-between mb-2 gap-2">
          <p class="text-[11px] font-bold text-emerald-300"><i class="fa-solid fa-comments text-[10px]"></i> ${q.answers_count || 0} ${q.answers_count === 1 ? 'resposta' : 'respostas'}</p>
          ${(q.answers_count || 0) > 0 ? `<button type="button" onclick="toggleQaAnswers('${q.id}')" class="text-[11px] font-bold text-emerald-300 hover:text-white bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-full transition-colors active:scale-95" id="qa-toggle-${q.id}">
            Ver respostas ▾
          </button>` : ''}
        </div>

        <div id="qa-answers-${q.id}" class="hidden space-y-1.5">
          ${answersHtml}
          <div class="mt-2 flex gap-1.5">
            <input type="text" id="qa-answer-input-${q.id}" maxlength="2000" placeholder="Responder anonimamente com empatia..." class="inp flex-1 px-3 py-2 text-[11px] bg-zinc-900 border-zinc-800 text-white rounded-xl placeholder-zinc-600 focus:border-emerald-500"/>
            <button type="button" onclick="submitQaAnswer('${q.id}')" class="px-3 py-2 rounded-xl text-[11px] font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/30 transition-all">Enviar</button>
          </div>
        </div>
        ${(q.answers_count || 0) === 0 ? `
        <div class="mt-1 flex gap-1.5">
          <input type="text" id="qa-answer-input-${q.id}" maxlength="2000" placeholder="Sê a primeira pessoa a responder anonimamente..." class="inp flex-1 px-3 py-2 text-[11px] bg-zinc-900 border-zinc-800 text-white rounded-xl placeholder-zinc-600 focus:border-emerald-500"/>
          <button type="button" onclick="submitQaAnswer('${q.id}')" class="px-3 py-2 rounded-xl text-[11px] font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/30 transition-all">Enviar</button>
        </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

// ═══════════════════════════════════════════════════
// 💡 ENCONTROS GRUPAIS COM AMIGOS (Limitado por País, Cidade Oficial e Data/Hora Exata)
// ═══════════════════════════════════════════════════
let DATE_IDEAS_STATE = { ideas: [], category: 'todas', country: '', cats: null, initializedSelectors: false };

const DI_CAT_META = {
  cafe:    { label: 'Café & Conversa', emoji: '☕' },
  passeio: { label: 'Passeio', emoji: '🚶' },
  cultura: { label: 'Cultura', emoji: '🎭' },
  natureza:{ label: 'Natureza', emoji: '🌿' },
  comida:  { label: 'Comida', emoji: '🍽️' },
  noite:   { label: 'Fim de Noite', emoji: '🌙' }
};

function detectUserDefaultCountryAndCity() {
  let defaultCountry = 'Portugal';
  let defaultCity = 'Lisboa';
  const rawCity = (STATE.currentUser && STATE.currentUser.city) || localStorage.getItem('sigaleve_pref_location') || '';
  if (rawCity && typeof GLOBAL_LOCATIONS_DATABASE === 'object') {
    for (const [country, cities] of Object.entries(GLOBAL_LOCATIONS_DATABASE)) {
      if (rawCity.toLowerCase().includes(country.toLowerCase())) {
        defaultCountry = country;
        defaultCity = cities[0] || 'Centro';
      }
      for (const c of cities) {
        if (rawCity.toLowerCase().includes(c.toLowerCase())) {
          defaultCountry = country;
          defaultCity = c;
          break;
        }
      }
    }
  }
  return { country: defaultCountry, city: defaultCity };
}

function initDateIdeaSelectors() {
  const countrySelect = document.getElementById('date-idea-country');
  const filterSelect = document.getElementById('date-ideas-country-filter');
  const dateInput = document.getElementById('date-idea-date');
  const timeInput = document.getElementById('date-idea-time');
  const countries = typeof GLOBAL_LOCATIONS_DATABASE === 'object' ? Object.keys(GLOBAL_LOCATIONS_DATABASE) : ['Portugal'];
  const { country: userCountry, city: userCity } = detectUserDefaultCountryAndCity();

  if (!DATE_IDEAS_STATE.country) {
    DATE_IDEAS_STATE.country = userCountry;
  }

  if (countrySelect && !countrySelect.options.length) {
    countrySelect.innerHTML = countries.map(c => `<option value="${esc(c)}" class="bg-zinc-900 text-white">${esc(c)}</option>`).join('');
    countrySelect.value = DATE_IDEAS_STATE.country || userCountry;
    handleDateIdeaCountryChange(countrySelect.value, userCity);
  }

  if (filterSelect && filterSelect.options.length <= 1) {
    filterSelect.innerHTML = countries.map(c => `<option value="${esc(c)}" class="bg-zinc-900 text-white">${esc(c)}</option>`).join('');
    filterSelect.value = DATE_IDEAS_STATE.country || userCountry;
  }

  // Configurar limites estritos de Data (hoje até +365 dias) e Hora padrão
  if (dateInput) {
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    const todayIso = `${yyyy}-${mm}-${dd}`;
    const maxDate = new Date(now.getTime() + 365 * 86400000);
    const maxIso = `${maxDate.getFullYear()}-${String(maxDate.getMonth() + 1).padStart(2, '0')}-${String(maxDate.getDate()).padStart(2, '0')}`;
    dateInput.min = todayIso;
    dateInput.max = maxIso;
    if (!dateInput.value || dateInput.value < todayIso) {
      dateInput.value = todayIso;
    }
  }
  if (timeInput && !timeInput.value) {
    timeInput.value = '18:30';
  }
  DATE_IDEAS_STATE.initializedSelectors = true;
}

function handleDateIdeaCountryChange(selectedCountry, preferredCity = '') {
  const citySelect = document.getElementById('date-idea-city');
  if (!citySelect) return;
  const cities = (typeof GLOBAL_LOCATIONS_DATABASE === 'object' && GLOBAL_LOCATIONS_DATABASE[selectedCountry]) || ['Lisboa'];
  citySelect.innerHTML = cities.map(ct => `<option value="${esc(ct)}" class="bg-zinc-900 text-white">${esc(ct)}</option>`).join('');
  if (preferredCity && cities.includes(preferredCity)) {
    citySelect.value = preferredCity;
  } else {
    citySelect.value = cities[0];
  }
}

function filterDateIdeasByCountry(countryVal) {
  DATE_IDEAS_STATE.country = countryVal;
  // Sincronizar o país do formulário de criação com o país selecionado
  const formCountry = document.getElementById('date-idea-country');
  if (formCountry && countryVal) {
    formCountry.value = countryVal;
    handleDateIdeaCountryChange(countryVal);
  }
  loadDateIdeas();
}

async function loadDateIdeas() {
  try {
    const paywallEl = document.getElementById('date-ideas-plus-paywall');
    const subContentEl = document.getElementById('date-ideas-subscriber-content');
    const btnNewIdea = document.getElementById('btn-new-date-idea');

    // Desbloqueado temporariamente para testes a pedido do utilizador
    // if (typeof isUserSubscribed === 'function' && !isUserSubscribed()) { ... }

    if (paywallEl) paywallEl.classList.add('hidden');
    if (subContentEl) subContentEl.classList.remove('hidden');
    if (btnNewIdea) {
      btnNewIdea.innerHTML = '<i class="fa-solid fa-plus"></i> <span>Propor Encontro</span>';
    }

    if (!DATE_IDEAS_STATE.initializedSelectors) {
      initDateIdeaSelectors();
    }
    const cat = DATE_IDEAS_STATE.category;
    const country = DATE_IDEAS_STATE.country || 'Portugal';
    const params = new URLSearchParams();
    if (cat && cat !== 'todas') params.set('category', cat);
    if (country) params.set('country', country);
    const qs = params.toString() ? '?' + params.toString() : '';
    const res = await fetch(`/api/v1/date-ideas${qs}`);
    const data = await res.json();
    if (res.status === 403 && data && data.subscription_required) {
      if (paywallEl) paywallEl.classList.remove('hidden');
      if (subContentEl) subContentEl.classList.add('hidden');
      return;
    }
    if (!res.ok) throw new Error('falhou');
    DATE_IDEAS_STATE.ideas = data.ideas || [];
    renderDateIdeaCats();
    renderDateIdeas();
  } catch (e) {
    console.warn('[date-ideas] load falhou:', e);
  }
}

function renderDateIdeaCats() {
  const wrap = document.getElementById('date-ideas-cats');
  if (!wrap) return;
  const cats = [['todas', '✨ Todas']].concat(Object.entries(DI_CAT_META).map(([k, v]) => [k, v.emoji + ' ' + v.label]));
  wrap.innerHTML = cats.map(([key, label]) => {
    const active = DATE_IDEAS_STATE.category === key;
    return `<button type="button" onclick="filterDateIdeas('${key}')" class="di-cat whitespace-nowrap px-3 py-2 rounded-full text-xs font-bold border transition-all active:scale-95 ${active ? 'bg-pink-500/20 text-pink-300 border-pink-500/50' : 'text-zinc-400 hover:text-white border-zinc-800 hover:border-zinc-600'}" style="background:${active ? '' : 'var(--card)'}">${label}</button>`;
  }).join('');
}

function filterDateIdeas(cat) {
  DATE_IDEAS_STATE.category = cat;
  loadDateIdeas();
}

function renderDateIdeas() {
  const list = document.getElementById('date-ideas-list');
  const empty = document.getElementById('date-ideas-empty');
  if (!list) return;
  if (!DATE_IDEAS_STATE.ideas.length) {
    list.innerHTML = '';
    if (empty) {
      empty.textContent = `Ainda não há encontros grupais criados para ${DATE_IDEAS_STATE.country || 'este país'}. Sê a primeira pessoa com Sigaleve Plus a propor um encontro! 💜`;
      empty.classList.remove('hidden');
    }
    return;
  }
  if (empty) empty.classList.add('hidden');
  list.innerHTML = DATE_IDEAS_STATE.ideas.map(i => {
    const catMeta = DI_CAT_META[i.category] || { label: i.category_label || 'Encontro', emoji: '💡' };
    const likedCls = i.my_like ? 'bg-pink-500/20 text-pink-300 border-pink-500/50' : 'text-zinc-400 border-zinc-800 hover:border-pink-500/40 hover:text-pink-300';
    const attending = Boolean(i.my_attending);
    const attendeesCount = Number(i.attendees_count || 0);
    const attendCls = attending
      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 shadow-sm shadow-emerald-500/10'
      : 'bg-purple-500/15 text-purple-200 border-purple-500/35 hover:bg-purple-500/25 hover:border-purple-400';

    // Gerar bolinhas misteriosas de "Encontro às Cegas" (sem nomes nem fotos reais)
    const mysteryDotsCount = Math.min(attendeesCount, 4);
    let mysteryAvatarsHtml = '';
    for (let d = 0; d < mysteryDotsCount; d++) {
      mysteryAvatarsHtml += `<span class="w-6 h-6 rounded-full bg-zinc-900 border border-purple-500/40 flex items-center justify-center text-[10px] text-purple-300 -ml-1.5 first:ml-0 shadow" title="Identidade secreta (Encontro às Cegas)"><i class="fa-solid fa-user-secret"></i></span>`;
    }

    let locationLabel = '';
    if (i.city && i.country) {
      locationLabel = `${i.city}, ${i.country}`;
    } else if (i.city) {
      locationLabel = i.city;
    } else if (i.country) {
      locationLabel = i.country;
    }

    const commentsList = i.comments || [];
    const commentsCount = Number(i.comments_count || commentsList.length || 0);
    const authorPhoto = i.author_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80';
    const authorName = i.author_name || (i.mine ? 'Tu (Organizador)' : 'Membro Sigaleve');

    const commentsHtml = commentsList.map(c => `
      <div class="p-2 sm:p-2.5 rounded-2xl bg-zinc-900/80 border border-white/5 flex items-start gap-2 text-xs">
        <img src="${c.user_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'}" class="w-6 h-6 rounded-full object-cover flex-shrink-0 border border-purple-500/30 mt-0.5" alt="Avatar"/>
        <div class="min-w-0 flex-1">
          <div class="flex items-center justify-between gap-1 mb-0.5">
            <span class="font-extrabold text-[11px] text-purple-200 truncate">${esc(c.user_name || 'Membro')}</span>
            <div class="flex items-center gap-1.5 flex-shrink-0">
              <span class="text-[9px] text-zinc-500">${qaTimeAgo(c.created_at || 0)}</span>
              ${(c.mine || i.mine) ? `<button type="button" onclick="deleteDateIdeaComment('${i.id}', '${c.id}')" class="text-zinc-500 hover:text-red-400 text-[10px] transition-colors p-0.5" title="Eliminar comentário"><i class="fa-regular fa-trash-can"></i></button>` : ''}
            </div>
          </div>
          <p class="text-[12px] text-zinc-300 leading-snug break-words">${esc(c.text || '')}</p>
        </div>
      </div>
    `).join('');

    return `
      <div class="date-idea-card p-4 rounded-3xl border shadow-xl flex flex-col justify-between transition-all hover:border-purple-500/35" style="background:var(--card);border-color:var(--bdr)" id="date-idea-card-${i.id}">
        <div>
          <!-- Cabeçalho do Card: Categoria, Localização, Data e Organizador Visível -->
          <div class="flex items-center justify-between gap-2 flex-wrap mb-2.5">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="text-[10px] bg-pink-500/15 text-pink-300 px-2.5 py-0.5 rounded-full font-bold border border-pink-500/25">${catMeta.emoji} ${catMeta.label}</span>
              ${locationLabel ? `<span class="text-[10px] text-zinc-300 bg-white/5 border border-white/10 px-2 py-0.5 rounded-full font-semibold"><i class="fa-solid fa-location-dot text-pink-400 text-[9px]"></i> ${esc(locationLabel)}</span>` : ''}
              ${i.event_date ? `<span class="text-[10px] text-amber-300 bg-amber-500/10 border border-amber-500/25 px-2 py-0.5 rounded-full font-semibold"><i class="fa-regular fa-calendar-check text-[9px]"></i> ${esc(i.event_date)}</span>` : ''}
            </div>
            <span class="text-[9px] text-purple-300 bg-purple-500/15 border border-purple-500/30 px-2 py-0.5 rounded-full font-bold flex items-center gap-1" title="Assistência anónima para participantes">
              <i class="fa-solid fa-user-secret text-[8px]"></i> Assistência Discreta
            </span>
          </div>

          <!-- Perfil do Organizador Visível -->
          <div class="flex items-center gap-2.5 p-2 mb-2.5 rounded-2xl bg-white/[0.03] border border-white/5">
            <img src="${authorPhoto}" class="w-8 h-8 rounded-full object-cover border-2 border-pink-500/40 shadow-sm flex-shrink-0" alt="${esc(authorName)}"/>
            <div class="min-w-0 flex-1 leading-tight">
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="text-xs font-black text-white truncate">${esc(authorName)}</span>
                <span class="text-[9px] bg-pink-500/20 text-pink-300 border border-pink-500/40 px-1.5 py-0.2 rounded-full font-black tracking-wide flex items-center gap-0.5">
                  <i class="fa-solid fa-bullhorn text-[8px]"></i> Organizador
                </span>
                ${i.mine ? '<span class="text-[9px] text-emerald-400 font-bold">(És tu)</span>' : ''}
              </div>
              <p class="text-[10px] text-zinc-400 truncate">Criador oficial deste encontro no Sigaleve Plus</p>
            </div>
          </div>

          <h4 class="text-[15px] font-black text-white leading-snug mb-1">${esc(i.title)}</h4>
          <p class="text-[13px] text-zinc-300 leading-relaxed mb-3">${esc(i.description)}</p>
        </div>

        <!-- Barra de Presença Secreta (Assistência Discreta) -->
        <div class="mt-1 pt-3 border-t border-white/5 flex flex-col gap-2.5">
          <div class="flex items-center justify-between gap-2 bg-black/25 px-3 py-2 rounded-2xl border border-white/5">
            <div class="flex items-center gap-2 min-w-0">
              <div class="flex items-center flex-shrink-0" id="di-mystery-avatars-${i.id}">
                ${mysteryAvatarsHtml || '<span class="w-6 h-6 rounded-full bg-zinc-900 border border-zinc-700 flex items-center justify-center text-[10px] text-zinc-500"><i class="fa-solid fa-user-secret"></i></span>'}
              </div>
              <div class="leading-tight min-w-0">
                <p class="text-xs font-extrabold text-white truncate">
                  <span class="di-attend-count text-purple-300" id="di-attend-count-${i.id}">${attendeesCount}</span>
                  <span id="di-attend-label-${i.id}">${attendeesCount === 1 ? ' pessoa confirmou' : ' pessoas confirmaram'}</span>
                </p>
                <p class="text-[10px] text-zinc-400 truncate flex items-center gap-1">
                  <i class="fa-solid fa-lock text-[8px] text-emerald-400"></i> Participantes 100% discretos
                </p>
              </div>
            </div>

            <button type="button" onclick="attendDateIdea('${i.id}', this)" class="di-attend px-3.5 py-2 rounded-xl border text-xs font-black transition-all flex items-center gap-1.5 active:scale-95 flex-shrink-0 ${attendCls}" title="A tua confirmação é discreta: só o número total aumenta, o teu nome nunca aparece na lista">
              <i class="fa-solid ${attending ? 'fa-circle-check text-emerald-400' : 'fa-user-secret'} text-xs"></i>
              <span class="di-attend-btn-text">${attending ? 'Confirmado' : 'Vou Assistir'}</span>
            </button>
          </div>

          <!-- Ações Inferiores: Comentários, Like e Eliminar -->
          <div class="flex items-center justify-between gap-2 px-1 pt-1">
            <button type="button" onclick="toggleDateIdeaComments('${i.id}')" class="text-xs font-bold text-zinc-300 hover:text-pink-300 flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-white/5 hover:bg-white/10 transition-colors border border-white/5" id="di-comments-toggle-btn-${i.id}">
              <i class="fa-regular fa-comment-dots text-pink-400"></i>
              <span id="di-comments-count-lbl-${i.id}">${commentsCount}</span>
              <span>${commentsCount === 1 ? 'comentário' : 'comentários'}</span>
              <i class="fa-solid fa-chevron-down text-[9px] text-zinc-400 ml-0.5 transition-transform" id="di-comments-chevron-${i.id}"></i>
            </button>

            <div class="flex items-center gap-1.5 flex-shrink-0">
              ${i.mine ? `<button type="button" onclick="deleteDateIdea('${i.id}')" class="px-2.5 py-1.5 rounded-full border border-zinc-800 text-zinc-500 hover:text-red-400 hover:border-red-500/40 transition-all" title="Eliminar encontro"><i class="fa-regular fa-trash-can text-[11px]"></i></button>` : ''}
              <button type="button" onclick="likeDateIdea('${i.id}', this)" class="di-like px-3 py-1.5 rounded-full border text-xs font-bold transition-all flex items-center gap-1.5 active:scale-95 ${likedCls}" title="Apoiar este encontro">
                <i class="${i.my_like ? 'fa-solid' : 'fa-regular'} fa-heart text-[11px]"></i>
                <span class="di-like-count">${i.likes_count || 0}</span>
              </button>
            </div>
          </div>

          <!-- Espaço de Comentários Aberto (Desdobrável) -->
          <div id="di-comments-box-${i.id}" class="hidden mt-2 pt-2 border-t border-white/10 space-y-2">
            <p class="text-[11px] font-black uppercase tracking-wider text-zinc-400 px-1 flex items-center justify-between">
              <span class="flex items-center gap-1.5"><i class="fa-solid fa-comments text-pink-400 text-xs"></i> Conversa do Encontro:</span>
              <span class="text-[9px] text-zinc-500 font-semibold">Tira dúvidas ou combina com o grupo</span>
            </p>

            <!-- Lista de Comentários -->
            <div id="di-comments-feed-${i.id}" class="space-y-1.5 max-h-48 overflow-y-auto pr-1">
              ${commentsHtml || `<p class="text-zinc-500 text-xs italic py-2 text-center" id="di-no-comments-${i.id}">Ainda não há comentários. Sê a primeira pessoa a comentar ou perguntar algo ao organizador! 💬</p>`}
            </div>

            <!-- Caixa para Inserir Novo Comentário -->
            <div class="flex items-center gap-1.5 pt-1">
              <input type="text" id="di-comment-input-${i.id}" maxlength="400" onkeydown="if(event.key==='Enter'){event.preventDefault();submitDateIdeaComment('${i.id}');}" placeholder="Deixa um comentário ou pergunta para o grupo..." class="inp flex-1 py-2 px-3 text-xs bg-zinc-900 border-zinc-800 text-white rounded-xl placeholder-zinc-500 focus:border-pink-500"/>
              <button type="button" onclick="submitDateIdeaComment('${i.id}')" class="px-3.5 py-2 rounded-xl text-xs font-black text-white active:scale-95 transition-all flex items-center gap-1 flex-shrink-0" style="background:linear-gradient(135deg,#a855f7,#ec4899)" title="Publicar comentário">
                <i class="fa-solid fa-paper-plane text-[10px]"></i>
                <span class="hidden sm:inline">Comentar</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

async function attendDateIdea(ideaId, btn) {
  // Desbloqueado temporariamente para testes
  try {
    const res = await fetch(`/api/v1/date-ideas/${encodeURIComponent(ideaId)}/attend`, { method: 'POST' });
    const data = await res.json();
    if (!res.ok || !data.success) throw new Error(data.error || 'falhou');
    const idea = DATE_IDEAS_STATE.ideas.find(i => i.id === ideaId);
    if (idea) {
      idea.my_attending = data.attending;
      idea.attendees_count = data.attendees_count;
    }
    renderDateIdeas();
    if (typeof showAppToast === 'function') {
      if (data.attending) {
        showAppToast('Presença secreta confirmada! 🎭 Só o contador subiu, ninguém sabe que és tu.', 'success');
      } else {
        showAppToast('Retiraste a tua confirmação secreta deste encontro.', 'info');
      }
    }
  } catch (e) {
    console.warn('[date-ideas] attend falhou:', e);
    if (typeof showAppToast === 'function') {
      showAppToast('Não foi possível atualizar a tua presença.', 'error');
    }
  }
}

async function likeDateIdea(ideaId, btn) {
  // Desbloqueado temporariamente para testes
  try {
    const res = await fetch(`/api/v1/date-ideas/${encodeURIComponent(ideaId)}/like`, { method: 'POST' });
    const data = await res.json();
    if (!res.ok || !data.success) throw new Error(data.error || 'falhou');
    const idea = DATE_IDEAS_STATE.ideas.find(i => i.id === ideaId);
    if (idea) { idea.my_like = data.liked; idea.likes_count = data.likes_count; }
    const countEl = btn.querySelector('.di-like-count');
    if (countEl) countEl.textContent = data.likes_count;
    const icon = btn.querySelector('i');
    if (icon) icon.className = (data.liked ? 'fa-solid' : 'fa-regular') + ' fa-heart text-[11px]';
    btn.classList.toggle('bg-pink-500/20', data.liked);
    btn.classList.toggle('text-pink-300', data.liked);
    btn.classList.toggle('border-pink-500/50', data.liked);
    btn.classList.toggle('text-zinc-400', !data.liked);
  } catch (e) {
    console.warn('[date-ideas] like falhou:', e);
  }
}

function deleteDateIdea(ideaId) {
  showAppConfirm(
    'Eliminar Encontro Grupal',
    'Tens a certeza de que desejas eliminar este encontro grupal da comunidade?',
    async () => {
      try {
        const res = await fetch(`/api/v1/date-ideas/${encodeURIComponent(ideaId)}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok || !data.success) throw new Error(data.error || 'falhou');
        DATE_IDEAS_STATE.ideas = DATE_IDEAS_STATE.ideas.filter(i => i.id !== ideaId);
        renderDateIdeas();
        showAppToast('Encontro eliminado com sucesso.', 'info');
      } catch (e) {
        console.warn('[date-ideas] delete falhou:', e);
        showAppToast('Erro ao eliminar encontro.', 'error');
      }
    },
    { danger: true, confirmText: 'Eliminar' }
  );
}

function toggleDateIdeaComments(ideaId) {
  const box = document.getElementById(`di-comments-box-${ideaId}`);
  const chevron = document.getElementById(`di-comments-chevron-${ideaId}`);
  if (!box) return;
  const isHidden = box.classList.contains('hidden');
  if (isHidden) {
    box.classList.remove('hidden');
    if (chevron) chevron.classList.add('rotate-180');
    const input = document.getElementById(`di-comment-input-${ideaId}`);
    if (input) setTimeout(() => input.focus(), 100);
  } else {
    box.classList.add('hidden');
    if (chevron) chevron.classList.remove('rotate-180');
  }
}

async function submitDateIdeaComment(ideaId) {
  const input = document.getElementById(`di-comment-input-${ideaId}`);
  if (!input) return;
  const text = input.value.trim();
  if (!text) {
    if (typeof showAppToast === 'function') showAppToast('Escreve algo no comentário.', 'warning');
    return;
  }
  try {
    input.disabled = true;
    const res = await fetch(`/api/v1/date-ideas/${encodeURIComponent(ideaId)}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      if (typeof showAppToast === 'function') {
        showAppToast(data.error || 'Erro ao publicar comentário.', 'error');
      }
      return;
    }
    input.value = '';
    const idea = DATE_IDEAS_STATE.ideas.find(i => i.id === ideaId);
    if (idea) {
      idea.comments = idea.comments || [];
      idea.comments.push(data.comment);
      idea.comments_count = data.comments_count;
    }
    renderDateIdeas();
    // Reabrir a caixa de comentários
    const newBox = document.getElementById(`di-comments-box-${ideaId}`);
    const newChevron = document.getElementById(`di-comments-chevron-${ideaId}`);
    if (newBox) newBox.classList.remove('hidden');
    if (newChevron) newChevron.classList.add('rotate-180');
    if (typeof showAppToast === 'function') {
      showAppToast('Comentário publicado! 💬', 'success');
    }
  } catch (e) {
    console.warn('[date-ideas] comment falhou:', e);
    if (typeof showAppToast === 'function') showAppToast('Erro de rede ao comentar.', 'error');
  } finally {
    if (input) input.disabled = false;
  }
}

async function deleteDateIdeaComment(ideaId, commentId) {
  showAppConfirm(
    'Eliminar Comentário',
    'Tens a certeza de que desejas apagar este comentário?',
    async () => {
      try {
        const res = await fetch(`/api/v1/date-ideas/${encodeURIComponent(ideaId)}/comments/${encodeURIComponent(commentId)}`, {
          method: 'DELETE'
        });
        const data = await res.json();
        if (!res.ok || !data.success) throw new Error(data.error || 'falhou');
        const idea = DATE_IDEAS_STATE.ideas.find(i => i.id === ideaId);
        if (idea) {
          idea.comments = (idea.comments || []).filter(c => c.id !== commentId);
          idea.comments_count = data.comments_count;
        }
        renderDateIdeas();
        const newBox = document.getElementById(`di-comments-box-${ideaId}`);
        const newChevron = document.getElementById(`di-comments-chevron-${ideaId}`);
        if (newBox) newBox.classList.remove('hidden');
        if (newChevron) newChevron.classList.add('rotate-180');
        if (typeof showAppToast === 'function') showAppToast('Comentário removido.', 'info');
      } catch (e) {
        console.warn('[date-ideas] delete comment falhou:', e);
        if (typeof showAppToast === 'function') showAppToast('Erro ao apagar comentário.', 'error');
      }
    },
    { danger: true, confirmText: 'Eliminar' }
  );
}

function openDateIdeaForm() {
  // Desbloqueado temporariamente para testes
  initDateIdeaSelectors();
  const f = document.getElementById('date-idea-form');
  if (!f) return;
  f.classList.remove('hidden');
  const t = document.getElementById('date-idea-title');
  if (t) t.focus();
}

function closeDateIdeaForm() {
  const f = document.getElementById('date-idea-form');
  if (f) f.classList.add('hidden');
}

function showDateIdeaAlert(msg, ok) {
  const a = document.getElementById('date-idea-alert');
  if (!a) return;
  a.textContent = msg;
  a.style.background = ok ? 'rgba(16,185,129,.12)' : 'rgba(239,68,68,.12)';
  a.style.color = ok ? '#34d399' : '#f87171';
  a.classList.remove('hidden');
  if (!ok) setTimeout(() => a.classList.add('hidden'), 6000);
}

async function submitDateIdea() {
  const titleEl = document.getElementById('date-idea-title');
  const descEl = document.getElementById('date-idea-desc');
  const countryEl = document.getElementById('date-idea-country');
  const cityEl = document.getElementById('date-idea-city');
  const dateEl = document.getElementById('date-idea-date');
  const timeEl = document.getElementById('date-idea-time');
  const catEl = document.getElementById('date-idea-cat');
  const btn = document.getElementById('btn-submit-date-idea');
  if (!titleEl || !descEl) return;

  const title = titleEl.value.trim();
  const description = descEl.value.trim();
  const country = countryEl ? countryEl.value.trim() : '';
  const city = cityEl ? cityEl.value.trim() : '';
  const event_date_iso = dateEl ? dateEl.value.trim() : '';
  const event_time_iso = timeEl ? timeEl.value.trim() : '';

  if (!title || !description) {
    showDateIdeaAlert('Preenche o título e a descrição do encontro grupal.', false);
    return;
  }
  if (!country || !city) {
    showDateIdeaAlert('Seleciona o País e a Cidade na lista oficial.', false);
    return;
  }
  if (!event_date_iso || !event_time_iso) {
    showDateIdeaAlert('Seleciona uma Data e uma Hora exatas para o encontro.', false);
    return;
  }

  // Validar no cliente que a data/hora escolhida é futura
  const chosenDt = new Date(`${event_date_iso}T${event_time_iso}:00`);
  if (isNaN(chosenDt.getTime()) || chosenDt.getTime() < Date.now()) {
    showDateIdeaAlert('A data e hora do encontro devem ser no futuro.', false);
    return;
  }

  try {
    btn.disabled = true;
    btn.textContent = 'A publicar...';
    const res = await fetch('/api/v1/date-ideas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        description,
        country,
        city,
        event_date_iso,
        event_time_iso,
        category: catEl ? catEl.value : 'cafe'
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      showDateIdeaAlert(data.error || 'Não foi possível publicar o encontro.', false);
      return;
    }
    titleEl.value = '';
    descEl.value = '';
    closeDateIdeaForm();
    DATE_IDEAS_STATE.category = 'todas';
    DATE_IDEAS_STATE.country = country;
    const filterSelect = document.getElementById('date-ideas-country-filter');
    if (filterSelect) filterSelect.value = country;
    await loadDateIdeas();
    if (typeof showAppToast === 'function') {
      showAppToast('Encontro grupal publicado! A tua presença secreta já foi incluída. 💜', 'success');
    }
  } catch (e) {
    showDateIdeaAlert('Erro de rede — tenta outra vez.', false);
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Publicar Encontro 💜';
  }
}

// ═══════════════════════════════════════════════════
// 💜 HISTÓRIA DE SUCESSO (submissão — curadoria do dono na landing)
// ═══════════════════════════════════════════════════
function openStorySubmitModal() {
  closeDrawer();
  const m = document.getElementById('modal-story-submit');
  if (!m) return;
  m.classList.remove('hidden');
  const cb = document.getElementById('story-anonymous');
  if (cb) cb.checked = true;
  syncStoryAnonymous();
}

function closeStorySubmitModal() {
  const m = document.getElementById('modal-story-submit');
  if (m) m.classList.add('hidden');
}

function syncStoryAnonymous() {
  const cb = document.getElementById('story-anonymous');
  const names = document.getElementById('story-names');
  if (!cb || !names) return;
  names.disabled = cb.checked;
  names.classList.toggle('opacity-50', cb.checked);
}

async function submitMyStory() {
  const textEl = document.getElementById('story-text');
  const anonEl = document.getElementById('story-anonymous');
  const namesEl = document.getElementById('story-names');
  const cityEl = document.getElementById('story-city');
  const btn = document.getElementById('btn-story-submit');
  const alertEl = document.getElementById('story-submit-alert');
  if (!textEl || !btn) return;
  const show = (msg, ok) => {
    if (!alertEl) return;
    alertEl.textContent = msg;
    alertEl.style.background = ok ? 'rgba(16,185,129,.12)' : 'rgba(239,68,68,.12)';
    alertEl.style.color = ok ? '#34d399' : '#f87171';
    alertEl.classList.remove('hidden');
  };
  const text = textEl.value.trim();
  if (text.length < 80) { show('Conta um pouco mais — mínimo de 80 caracteres.', false); return; }
  try {
    btn.disabled = true;
    btn.textContent = 'A enviar...';
    const res = await fetch('/api/v1/stories/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        anonymous: anonEl ? anonEl.checked : true,
        names: namesEl ? namesEl.value.trim() : '',
        city: cityEl ? cityEl.value.trim() : ''
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success) { show(data.error || 'Não foi possível enviar.', false); return; }
    textEl.value = '';
    if (cityEl) cityEl.value = '';
    if (namesEl) namesEl.value = '';
    show(data.message || 'História enviada! 💜', true);
    setTimeout(closeStorySubmitModal, 2500);
  } catch (e) {
    show('Erro de rede — tenta outra vez.', false);
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Enviar história 💜';
  }
}

function toggleQaAnswers(qid) {
  const box = document.getElementById('qa-answers-' + qid);
  const toggle = document.getElementById('qa-toggle-' + qid);
  if (!box) return;
  if (box.classList.contains('hidden')) {
    box.classList.remove('hidden');
    if (toggle) toggle.textContent = 'Esconder respostas ▴';
    fetch(`/api/v1/qa-health/${qid}/view`, { method: 'POST' }).catch(() => {});
  } else {
    box.classList.add('hidden');
    if (toggle) toggle.textContent = 'Ver respostas ▾';
  }
}

async function submitQaQuestion() {
  const q = document.getElementById('qa-new-question');
  const d = document.getElementById('qa-new-detail');
  if (!q.value.trim()) { showAppToast('Escreve primeiro a tua pergunta.', 'warning'); return; }
  const cat = QA_CURRENT_CATEGORY || 'diagnostico';
  try {
    const res = await fetch('/api/v1/qa-health', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q.value.trim(), detail: d ? d.value.trim() : '', category: cat })
    });
    const data = await res.json();
    if (!data.success) { showAppToast(data.message || 'Não foi possível publicar.', 'error'); return; }
    q.value = '';
    if (d) d.value = '';
    showAppToast('Pergunta publicada anonimamente! 💚', 'success');
    loadQaList();
  } catch (e) {
    showAppToast('Erro de conexão. Tenta novamente.', 'error');
  }
}

async function submitQaAnswer(qid) {
  const input = document.getElementById('qa-answer-input-' + qid);
  if (!input || !input.value.trim()) { showAppToast('Escreve primeiro a resposta.', 'warning'); return; }
  try {
    const res = await fetch(`/api/v1/qa-health/${qid}/answers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input.value.trim() })
    });
    const data = await res.json();
    if (!data.success) { showAppToast(data.message || 'Não foi possível responder.', 'error'); return; }
    input.value = '';
    showAppToast('Resposta enviada anonimamente! 💚', 'success');
    loadQaList();
  } catch (e) {
    showAppToast('Erro de conexão. Tenta novamente.', 'error');
  }
}

async function likeQaAnswer(qid, aid, btn) {
  try {
    const res = await fetch(`/api/v1/qa-health/${qid}/like`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer_id: aid })
    });
    const data = await res.json();
    if (!data.success) return;
    const counter = btn.querySelector('.qa-likes-count');
    if (counter) counter.textContent = data.likes;
    if (data.liked) { btn.classList.add('text-emerald-300'); } else { btn.classList.remove('text-emerald-300'); }
  } catch (e) { /* silencioso */ }
}
