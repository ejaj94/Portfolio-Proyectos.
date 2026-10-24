/**
 * Motor de i18n: idioma atual, T(), aplicar/traduzir a UI, seletor de idioma.
 */
'use strict';

let LANG = localStorage.getItem('sigaleve_lang') || 'pt';
const T = k => {
  const d = LANGS[LANG] || {};
  return d[k] || (LANGS.en && LANGS.en[k]) || (LANGS.es && LANGS.es[k]) || (LANGS.pt && LANGS.pt[k]) || k;
};

function applyLang() {
  const currentDict = LANGS[LANG] || {};
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.dataset.i18n;
    const val = currentDict[k] || (LANGS.en && LANGS.en[k]) || (LANGS.es && LANGS.es[k]) || (LANGS.pt && LANGS.pt[k]);
    if (val) el.textContent = val;
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const k = el.dataset.i18nPh;
    const val = currentDict[k] || (LANGS.en && LANGS.en[k]) || (LANGS.es && LANGS.es[k]) || (LANGS.pt && LANGS.pt[k]);
    if (val) el.setAttribute('placeholder', val);
  });
  const selApp = document.getElementById('app-lang-select');
  if (selApp) selApp.value = LANG;
  const selAuth = document.getElementById('auth-lang-sel');
  if (selAuth) selAuth.value = LANG;

  // Actualizar botón de idioma en pantalla de login
  const authFlagEl = document.getElementById('auth-current-lang-flag');
  const authLabelEl = document.getElementById('auth-current-lang-label');
  const langNames = { es: 'Español', pt: 'Português', en: 'English', fr: 'Français', de: 'Deutsch', it: 'Italiano', sw: 'Kiswahili', yo: 'Yorùbá', ha: 'Hausa', ar: 'العربية' };
  const currentLangObj = WORLD_107_LANGUAGES.find(x => x.code === LANG);
  if (authFlagEl) authFlagEl.textContent = currentLangObj ? currentLangObj.flag : '🌐';
  if (authLabelEl) authLabelEl.textContent = currentLangObj ? currentLangObj.name : (langNames[LANG] || LANG);

  if (typeof updateOnboardStepUI === 'function') {
    updateOnboardStepUI();
  }
  if (typeof openProductSubscription === 'function' && typeof currentProductTab !== 'undefined') {
    const modalSub = document.getElementById('modal-subscription');
    if (modalSub && !modalSub.classList.contains('hidden')) {
      openProductSubscription(currentProductTab);
    }
  }
  const displayName = currentLangObj ? `${currentLangObj.flag} ${currentLangObj.name}` : (langNames[LANG] || LANG);
  const drawerLangVal = document.getElementById('drawer-lang-val');
  if (drawerLangVal) drawerLangVal.innerHTML = `${displayName} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;

  // Re-traduzir valores exibidos nas linhas de definições e ficha do perfil
  if (typeof getLocalizedOptionLabel === 'function') {
    document.querySelectorAll('[id^="row-val-"]').forEach(el => {
      const orig = el.dataset && el.dataset.originalVal;
      if (orig && !el.classList.contains('red-val')) {
        const trans = getLocalizedOptionLabel(orig, LANG);
        el.innerHTML = `${trans} <i class="fa-solid fa-chevron-right text-xs ml-1 text-zinc-500"></i>`;
      }
    });

    // Perfil: Signo, Educação, O que busco
    const profGoal = document.getElementById('prof-relationship-goal');
    if (profGoal && profGoal.dataset && profGoal.dataset.originalVal) {
      profGoal.textContent = getLocalizedOptionLabel(profGoal.dataset.originalVal, LANG);
    }
    const profSigno = document.querySelector('#sec-profile .fa-moon')?.nextElementSibling?.querySelector('p:last-child');
    if (profSigno && profSigno.dataset && profSigno.dataset.originalVal) {
      profSigno.textContent = getLocalizedOptionLabel(profSigno.dataset.originalVal, LANG);
    }
    const profEdu = document.querySelector('#sec-profile .fa-graduation-cap')?.nextElementSibling?.querySelector('p:last-child');
    if (profEdu && profEdu.dataset && profEdu.dataset.originalVal) {
      profEdu.textContent = getLocalizedOptionLabel(profEdu.dataset.originalVal, LANG);
    }
  }

  // Re-renderizar lista de contactos bloqueados se o modal estiver ativo ou cacheado
  if (typeof renderBlockedContactsUI === 'function') {
    renderBlockedContactsUI();
  }

  // Se o modal de seleção única estiver aberto, atualizar dinamicamente para o novo idioma
  const modalSingle = document.getElementById('modal-single-select');
  if (modalSingle && !modalSingle.classList.contains('hidden') && typeof currentSelectCategory !== 'undefined' && currentSelectCategory) {
    if (typeof openSelectionModal === 'function') {
      openSelectionModal(currentSelectCategory);
    }
  }

  // Re-renderizar matches e conversas para refletir o idioma atual
  if (typeof renderMatches === 'function') {
    renderMatches();
  }

  // Re-renderizar o status do 2FA se já carregado
  if (typeof render2FAStatusUI === 'function') {
    render2FAStatusUI();
  }
}



let TRANSLATIONS_CACHE = {};
try {
  const cached = localStorage.getItem('sigaleve_translations_cache');
  if (cached) TRANSLATIONS_CACHE = JSON.parse(cached);
} catch(e) {}

function openAppLanguageModal() {
  renderAppLanguagesList('');
  const modal = document.getElementById('modal-app-language');
  if (modal) modal.classList.remove('hidden');
  const searchInp = document.getElementById('lang-modal-search');
  if (searchInp) {
    searchInp.value = '';
    setTimeout(() => searchInp.focus(), 200);
  }
}

function closeAppLanguageModal() {
  const modal = document.getElementById('modal-app-language');
  if (modal) modal.classList.add('hidden');
}

function filterAppLanguagesList(query) {
  renderAppLanguagesList(query);
}

function renderAppLanguagesList(filter) {
  const container = document.getElementById('lang-modal-list');
  if (!container) return;
  const q = (filter || '').toLowerCase().trim();
  const list = WORLD_107_LANGUAGES.filter(item => {
    return !q || item.name.toLowerCase().includes(q) || item.native.toLowerCase().includes(q) || item.code.toLowerCase().includes(q);
  });

  const summary = document.getElementById('lang-active-summary');
  const currentObj = WORLD_107_LANGUAGES.find(x => x.code === LANG);
  if (summary) {
    summary.innerHTML = `Activo: <strong>${currentObj ? currentObj.flag + ' ' + currentObj.name : LANG}</strong>`;
  }

  container.innerHTML = '';
  list.forEach(item => {
    const isSelected = item.code === LANG;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.onclick = () => selectAppLanguageAndTranslate(item.code);
    btn.className = 'w-full p-3 rounded-2xl flex items-center justify-between text-left transition-all ' +
      (isSelected ? 'bg-purple-600/20 border-2 border-purple-500 shadow-md text-white' : 'bg-zinc-900 border border-zinc-800/80 hover:bg-zinc-850 hover:border-zinc-700 text-zinc-300');
    
    btn.innerHTML = `
      <div class="flex items-center gap-3">
        <span class="text-xl flex-shrink-0">${item.flag}</span>
        <div>
          <p class="font-bold text-xs ${isSelected ? 'text-white' : 'text-zinc-200'}">${esc(item.name)}</p>
          <p class="text-[10px] text-zinc-400 font-medium">${esc(item.native)} <span class="font-mono text-[9px] uppercase px-1 rounded bg-zinc-800 text-zinc-400 ml-1">${item.code}</span></p>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        ${isSelected ? '<span class="text-[10px] px-2 py-0.5 rounded-full bg-purple-500 text-white font-black uppercase">Activo</span>' : '<i class="fa-solid fa-chevron-right text-xs text-zinc-600"></i>'}
      </div>
    `;
    container.appendChild(btn);
  });
}

async function selectAppLanguageAndTranslate(targetCode) {
  setLang(targetCode);
  closeAppLanguageModal();
}

async function setLang(l) {
  LANG = l;
  window.LANG = l;
  document.documentElement.lang = l;
  localStorage.setItem('sigaleve_lang', l);
  applyLang();

  // Si el idioma está predefinido en LANGS (ej. es, pt, en, fr, de, it, sw, yo, ha, ar), la traducción local es inmediata.
  if (LANGS[l]) {
    return;
  }

  // Si es cualquiera de los 107 idiomas globales adicionales, ejecutar traducción dinámica instantánea
  await translateAppUI(l);
}

async function translateAppUI(targetLang) {
  const transBar = document.getElementById('lang-translating-bar');
  if (transBar) transBar.classList.remove('hidden');

  // Obtener diccionario base en español
  const baseDict = LANGS.es || LANGS.pt;
  if (!TRANSLATIONS_CACHE[targetLang]) {
    TRANSLATIONS_CACHE[targetLang] = {};
  }

  const missingKeys = [];
  const missingTexts = [];
  for (const [k, v] of Object.entries(baseDict)) {
    if (typeof v === 'string') {
      if (!TRANSLATIONS_CACHE[targetLang][k]) {
        missingKeys.push(k);
        missingTexts.push(v);
      }
    }
  }

  if (missingTexts.length > 0) {
    try {
      // Chunk de a 25 textos para velocidad instantánea
      const chunkSize = 25;
      for (let i = 0; i < missingTexts.length; i += chunkSize) {
        const sliceTexts = missingTexts.slice(i, i + chunkSize);
        const sliceKeys = missingKeys.slice(i, i + chunkSize);

        const res = await fetch('/api/v1/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ texts: sliceTexts, target: targetLang, source: 'es' })
        });
        const data = await res.json();
        if (data.success && data.translations) {
          sliceKeys.forEach((key, idx) => {
            const originalText = sliceTexts[idx];
            if (data.translations[originalText]) {
              TRANSLATIONS_CACHE[targetLang][key] = data.translations[originalText];
            }
          });
        }
      }
      try {
        localStorage.setItem('sigaleve_translations_cache', JSON.stringify(TRANSLATIONS_CACHE));
      } catch(e){}
    } catch(err) {
      console.warn('Fallo en traducción remota de interfaz:', err);
    }
  }

  // Aplicar las traducciones al DOM
  const targetDict = TRANSLATIONS_CACHE[targetLang] || {};
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.dataset.i18n;
    if (targetDict[k]) el.textContent = targetDict[k];
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const k = el.dataset.i18nPh;
    if (targetDict[k]) el.setAttribute('placeholder', targetDict[k]);
  });

  if (typeof openProductSubscription === 'function' && typeof currentProductTab !== 'undefined') {
    const modalSub = document.getElementById('modal-subscription');
    if (modalSub && !modalSub.classList.contains('hidden')) {
      openProductSubscription(currentProductTab);
    }
  }

  // Actualizar la barra de reacciones de momentos si ya están cargados
  if (window.CURRENT_MOMENTS_FEED && Array.isArray(window.CURRENT_MOMENTS_FEED)) {
    window.CURRENT_MOMENTS_FEED.forEach(m => {
      const rxBar = document.getElementById(`rx-bar-${m.id}`);
      if (rxBar && typeof renderReactionBar === 'function') {
        rxBar.innerHTML = renderReactionBar(m);
      }
    });
  }

  if (transBar) transBar.classList.add('hidden');
}
