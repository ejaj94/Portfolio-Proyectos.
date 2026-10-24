/**
 * Tema escuro (toggle) e objeto STATE global da aplicação.
 */
'use strict';

// ═══════════════════════════════════════════════════
// DARK MODE
// ═══════════════════════════════════════════════════
function isDark(){ return document.documentElement.classList.contains('dark'); }
function toggleDark(){
  const dark = !isDark();
  document.documentElement.classList.toggle('dark', dark);
  localStorage.setItem('sigaleve_dark', dark);
  updateDarkTog();
}
function updateDarkTog(){
  const t = document.getElementById('dark-tog');
  if(t) t.classList.toggle('on', isDark());
}

// ═══════════════════════════════════════════════════
// ESTADO GLOBAL DA APLICAÇÃO
// ═══════════════════════════════════════════════════
const STATE = {
  section: 'discover',
  cursor: 0,
  currentUser: null,
  chatPeer: null,
  profiles: []
};
