/**
 * Definições: interruptores, tema claro/escuro/sistema e Saída Rápida (botão de pânico, Esc 2x).
 */
// ═══════════════════════════════════════════════════
// ACCIONES INTERACTIVAS DE AJUSTES (TINDER 1:1)
// ═══════════════════════════════════════════════════
function toggleTinderSwitch(el) {
  if (!el) return;
  el.classList.toggle('on');
}

function selectControlSee(type) {
  const bal = document.getElementById('chk-control-balanced');
  const rec = document.getElementById('chk-control-recent');
  if (type === 'balanced') {
    if (bal) bal.classList.remove('hidden');
    if (rec) rec.classList.add('hidden');
  } else {
    if (bal) bal.classList.add('hidden');
    if (rec) rec.classList.remove('hidden');
  }
}

function selectControlSeen(type) {
  const std = document.getElementById('chk-seen-standard');
  if (type === 'standard') {
    if (std) std.classList.remove('hidden');
  }
}

function applyCurrentTheme() {
  const saved = localStorage.getItem('sigaleve_dark');
  const sysDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (saved === 'dark' || saved === 'true') {
    document.documentElement.classList.add('dark');
  } else if (saved === 'light' || saved === 'false') {
    document.documentElement.classList.remove('dark');
  } else {
    // Modo Sistema (por omisión)
    if (sysDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }
  updateThemeCheckmarks();
  if (typeof updateDarkTog === 'function') updateDarkTog();
}

function toggleThemeQuickly() {
  const isCurrentlyDark = document.documentElement.classList.contains('dark');
  selectThemeMode(isCurrentlyDark ? 'light' : 'dark');
}

function updateThemeCheckmarks() {
  const saved = localStorage.getItem('sigaleve_dark');
  let currentMode = 'system';
  if (saved === 'true' || saved === 'dark') currentMode = 'dark';
  else if (saved === 'false' || saved === 'light') currentMode = 'light';

  ['system', 'light', 'dark'].forEach(m => {
    const chk = document.getElementById('chk-theme-' + m);
    if (!chk) return;
    if (m === currentMode) chk.classList.remove('hidden');
    else chk.classList.add('hidden');
  });

  const isNowDark = document.documentElement.classList.contains('dark');
  const icon = document.getElementById('auth-theme-toggle-icon');
  const lbl = document.getElementById('auth-theme-toggle-label');
  if (icon) {
    icon.className = isNowDark ? 'fa-solid fa-sun text-amber-400 text-xs' : 'fa-solid fa-moon text-purple-400 text-xs';
  }
  if (lbl) {
    lbl.textContent = isNowDark ? 'Modo Claro' : 'Modo Escuro';
  }
}

function selectThemeMode(mode) {
  if (mode === 'dark') {
    document.documentElement.classList.add('dark');
    localStorage.setItem('sigaleve_dark', 'true');
  } else if (mode === 'light') {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('sigaleve_dark', 'false');
  } else {
    localStorage.removeItem('sigaleve_dark');
    const sysDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (sysDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  updateThemeCheckmarks();
  if (typeof updateDarkTog === 'function') updateDarkTog();
}

// ── SAÍDA RÁPIDA (QUICK EXIT) ── Privacidade crítica neste nicho:
// alguém passa ao lado -> um clique (ou Esc 2x) fecha a sessão e substitui
// o histórico do separador por um site neutro. O botão "voltar" não reabre o app.
const QUICK_EXIT_URL = 'https://www.24kitchen.pt/receitas/tipo-de-refeicao/bolos-e-pastelaria/bolachas';
let _escCount = 0;
let _escTimer = null;

async function quickExit() {
  try {
    // 1. Terminar a sessão no servidor (limpa o cookie de sessão)
    await fetch('/api/v1/auth/logout', { method: 'POST' }).catch(() => {});
  } catch (e) { /* segue mesmo offline */ }
  try {
    sessionStorage.clear();
    localStorage.removeItem('sigaleve_user_id');
    localStorage.removeItem('sigaleve_dark');
  } catch (e) {}

  // 2. Substituir a entrada actual do histórico por um site neutro
  //    (window.location substitui o registo actual -> "voltar" não reabre o Sigaleve)
  window.location.replace(QUICK_EXIT_URL);
}

// Esc 2x (clique duplo na tecla) dispara a Saída Rápida em qualquer ecrã
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  // não disparar enquanto o utilizador escreve
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : '';
  if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) return;
  _escCount++;
  if (_escCount === 1) {
    _escTimer = setTimeout(() => { _escCount = 0; }, 800);
  } else if (_escCount >= 2) {
    clearTimeout(_escTimer);
    _escCount = 0;
    quickExit();
  }
});

// Escuchar cambios de tema del sistema en tiempo real
if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    const saved = localStorage.getItem('sigaleve_dark');
    if (!saved || saved === 'system') {
      applyCurrentTheme();
    }
  });
}
