// legal_i18n.js — Auto-traductor universal y selector de idiomas para páginas legales de Sigaleve
(function () {
  const WORLD_LANGS = [
    { code: 'pt', name: 'Português', flag: '🇵🇹' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'it', name: 'Italiano', flag: '🇮🇹' },
    { code: 'ru', name: 'Русский', flag: '🇷🇺' },
    { code: 'zh', name: '中文 (Chinese)', flag: '🇨🇳' },
    { code: 'ja', name: '日本語 (Japanese)', flag: '🇯🇵' },
    { code: 'ko', name: '한국어 (Korean)', flag: '🇰🇷' },
    { code: 'ar', name: 'العربية (Arabic)', flag: '🇸🇦' },
    { code: 'hi', name: 'हिन्दी (Hindi)', flag: '🇮🇳' },
    { code: 'nl', name: 'Nederlands', flag: '🇳🇱' },
    { code: 'pl', name: 'Polski', flag: '🇵🇱' },
    { code: 'sv', name: 'Svenska', flag: '🇸🇪' },
    { code: 'tr', name: 'Türkçe', flag: '🇹🇷' },
    { code: 'uk', name: 'Українська', flag: '🇺🇦' },
    { code: 'el', name: 'Ελληνικά', flag: '🇬🇷' },
    { code: 'he', name: 'עברית', flag: '🇮🇱' },
    { code: 'id', name: 'Bahasa Indonesia', flag: '🇮🇩' },
    { code: 'ms', name: 'Bahasa Melayu', flag: '🇲🇾' },
    { code: 'th', name: 'ไทย', flag: '🇹🇭' },
    { code: 'vi', name: 'Tiếng Việt', flag: '🇻🇳' },
    { code: 'ro', name: 'Română', flag: '🇷🇴' },
    { code: 'cs', name: 'Čeština', flag: '🇨🇿' },
    { code: 'hu', name: 'Magyar', flag: '🇭🇺' },
    { code: 'da', name: 'Dansk', flag: '🇩🇰' },
    { code: 'fi', name: 'Suomi', flag: '🇫🇮' },
    { code: 'no', name: 'Norsk', flag: '🇳🇴' },
    { code: 'sw', name: 'Kiswahili', flag: '🇰🇪' },
    { code: 'af', name: 'Afrikaans', flag: '🇿🇦' },
    { code: 'bg', name: 'Български', flag: '🇧🇬' },
    { code: 'hr', name: 'Hrvatski', flag: '🇭🇷' },
    { code: 'sk', name: 'Slovenčina', flag: '🇸🇰' },
    { code: 'ca', name: 'Català', flag: '🇪🇸' },
    { code: 'gl', name: 'Galego', flag: '🇪🇸' },
    { code: 'eu', name: 'Euskara', flag: '🇪🇸' },
    { code: 'tl', name: 'Tagalog', flag: '🇵🇭' }
  ];

  let currentLang = localStorage.getItem('sigaleve_lang') || 'pt';

  // Obter ou inicializar cache local de traduções
  function getTranslationsCache() {
    try {
      return JSON.parse(localStorage.getItem('sigaleve_legal_cache') || '{}');
    } catch (e) {
      return {};
    }
  }

  function saveTranslationsCache(cache) {
    try {
      localStorage.setItem('sigaleve_legal_cache', JSON.stringify(cache));
    } catch (e) {}
  }

  // Cria a barra superior de idioma se não existir
  function injectLanguageBar() {
    const nav = document.querySelector('nav');
    if (!nav) return;
    const actionsContainer = nav.querySelector('div.flex.items-center.gap-2') || nav.querySelector('.max-w-5xl > div:last-child') || nav.querySelector('.max-w-4xl > div:last-child');
    if (!actionsContainer) return;

    if (document.getElementById('sigaleve-legal-lang-wrap')) return;

    const wrap = document.createElement('div');
    wrap.id = 'sigaleve-legal-lang-wrap';
    wrap.className = 'relative flex items-center';

    const select = document.createElement('select');
    select.id = 'sigaleve-legal-lang-select';
    select.className = 'text-xs font-semibold px-2.5 py-1.5 rounded-xl border cursor-pointer outline-none transition-all shadow-sm';
    select.style.background = 'var(--card)';
    select.style.borderColor = 'var(--bdr)';
    select.style.color = 'var(--txt)';

    WORLD_LANGS.forEach(l => {
      const opt = document.createElement('option');
      opt.value = l.code;
      opt.textContent = `${l.flag} ${l.name}`;
      if (l.code === currentLang) opt.selected = true;
      select.appendChild(opt);
    });

    select.addEventListener('change', (e) => {
      const newLang = e.target.value;
      localStorage.setItem('sigaleve_lang', newLang);
      currentLang = newLang;
      applyTranslation(newLang);
    });

    wrap.appendChild(select);
    actionsContainer.insertBefore(wrap, actionsContainer.firstChild);

    // Indicador discreto de tradução flutuante
    if (!document.getElementById('sigaleve-legal-loading-banner')) {
      const banner = document.createElement('div');
      banner.id = 'sigaleve-legal-loading-banner';
      banner.className = 'fixed bottom-4 right-4 z-50 px-4 py-2 rounded-2xl bg-purple-600/90 text-white text-xs font-bold shadow-2xl backdrop-blur-md flex items-center gap-2 transition-all opacity-0 pointer-events-none transform translate-y-3';
      banner.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin text-sm"></i> <span>A traduzir documento para o teu idioma...</span>';
      document.body.appendChild(banner);
    }
  }

  function showLoading(show, text) {
    const banner = document.getElementById('sigaleve-legal-loading-banner');
    if (!banner) return;
    if (show) {
      if (text) banner.querySelector('span').textContent = text;
      banner.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-3');
    } else {
      banner.classList.add('opacity-0', 'pointer-events-none', 'translate-y-3');
    }
  }

  // Coleta nós textuais significativos
  function collectTranslatableElements() {
    const elements = [];
    const main = document.querySelector('main') || document.querySelector('article') || document.body;
    const targets = main.querySelectorAll('h1, h2, h3, h4, p, li, td, th, span.badge-essential, span.badge-functional, span.badge-analytics, span.badge-none, .toc a, #toc-t, nav.toc a');
    
    targets.forEach(el => {
      // Ignorar nós que são puramente ícones
      if (el.children.length === 1 && el.querySelector('i')) return;
      // Salva texto original caso ainda não tenha salvo
      if (!el.hasAttribute('data-orig-text')) {
        el.setAttribute('data-orig-text', el.innerText.trim());
      }
      elements.push(el);
    });
    return elements;
  }

  async function applyTranslation(targetLang) {
    if (!targetLang) targetLang = 'pt';
    const sel = document.getElementById('sigaleve-legal-lang-select');
    if (sel) sel.value = targetLang;

    const elements = collectTranslatableElements();
    if (elements.length === 0) return;

    // Se o idioma for o base de redação inicial (espanhol), restauramos o original se foi traduzido
    if (targetLang === 'es') {
      elements.forEach(el => {
        const orig = el.getAttribute('data-orig-text');
        if (orig && el.innerText.trim() !== orig) {
          el.innerText = orig;
        }
      });
      return;
    }

    const cache = getTranslationsCache();
    if (!cache[targetLang]) cache[targetLang] = {};

    const toTranslate = [];
    const textToEl = [];

    elements.forEach(el => {
      const orig = el.getAttribute('data-orig-text') || el.innerText.trim();
      if (!orig || orig.length < 2) return;
      if (cache[targetLang][orig]) {
        // Já está em cache
        el.innerText = cache[targetLang][orig];
      } else {
        toTranslate.push(orig);
        textToEl.push({ el, orig });
      }
    });

    if (toTranslate.length === 0) return;

    // Tradução remota em lote via /api/v1/translate
    showLoading(true, `A carregar tradução oficial (${targetLang.toUpperCase()})...`);
    
    // Agrupa em chunks de 20 para resposta ultra rápida
    const chunkSize = 25;
    const uniqueTexts = Array.from(new Set(toTranslate));

    for (let i = 0; i < uniqueTexts.length; i += chunkSize) {
      const chunk = uniqueTexts.slice(i, i + chunkSize);
      try {
        const res = await fetch('/api/v1/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ texts: chunk, target: targetLang, source: 'es' })
        });
        const data = await res.json();
        if (data.success && data.translations) {
          Object.assign(cache[targetLang], data.translations);
          // Atualiza nós correspondentes
          textToEl.forEach(item => {
            if (data.translations[item.orig]) {
              item.el.innerText = data.translations[item.orig];
            }
          });
        }
      } catch (err) {
        console.warn('Erro ao traduzir trecho:', err);
      }
    }

    saveTranslationsCache(cache);
    showLoading(false);
  }

  // Inicialização
  window.addEventListener('DOMContentLoaded', () => {
    injectLanguageBar();
    // Executa tradução com o idioma ativo
    const lang = localStorage.getItem('sigaleve_lang') || 'pt';
    applyTranslation(lang);
  });
})();
