/**
 * Inicialização precoce (corre no <head>): tema escuro e idioma antes da primeira pintura, evitando "flash".
 */
(function(){
  // Limpeza de cache/estado anterior se o sistema do usuário estiver em modo escuro
  var vKey = 'sigaleve_theme_v4';
  var sysDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (!localStorage.getItem(vKey)) {
    // Primeira execução da versão atualizada: se o sistema é escuro, limpa 'sigaleve_dark' legado para respeitar o SO imediatamente
    if (sysDark) {
      localStorage.removeItem('sigaleve_dark');
    }
    localStorage.setItem(vKey, '1');
  }

  var d = localStorage.getItem('sigaleve_dark');
  var shouldBeDark = (d === 'dark' || d === 'true') || ((d === null || d === undefined || d === 'system') && sysDark);

  if (shouldBeDark) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }

  
  // 1. Extrair idioma: query param ?lang= -> cookie -> localStorage -> default 'pt'
  var urlParams = new URLSearchParams(window.location.search);
  var qLang = urlParams.get('lang');
  if (!qLang) {
    var match = document.cookie.match(/sigaleve_lang=([^;]+)/);
    if (match) qLang = match[1];
  }
  if (qLang) {
    localStorage.setItem('sigaleve_lang', qLang);
    document.cookie = "sigaleve_lang=" + qLang + "; path=/; max-age=31536000";
  }
  var l = qLang || localStorage.getItem('sigaleve_lang') || 'pt';
  window.LANG = l;
  document.documentElement.lang = l;
})();
