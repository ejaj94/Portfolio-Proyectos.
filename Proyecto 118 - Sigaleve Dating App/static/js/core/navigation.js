/**
 * Navegação entre secções (showSection).
 */
'use strict';

// ═══════════════════════════════════════════════════
// NAVEGAÇÃO ENTRE ABAS
// ═══════════════════════════════════════════════════
function showSection(sec) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));

  const sTarget = document.getElementById('sec-' + sec);
  if (sTarget) {
    sTarget.classList.add('active');
    if (sTarget.scrollTop !== undefined) sTarget.scrollTop = 0;
  }

  const tab = document.getElementById('nav-' + sec);
  if (tab) tab.classList.add('active');

  const topTitle = document.getElementById('top-title');
  if (topTitle) {
    if (sec === 'discover') topTitle.textContent = 'Sigaleve';
    else if (sec === 'matches') topTitle.textContent = T('matches');
    else if (sec === 'profile') topTitle.textContent = T('profile');
    else if (sec === 'moments') topTitle.textContent = 'Momentos & Sentimentos';
    else if (sec === 'qa-health') topTitle.textContent = 'Comunidade & Saúde';
    else if (sec === 'date-ideas') topTitle.textContent = 'Encontros Grupais com Amigos';
  }

  // Carregar dados da secção aberta
  if (sec === 'qa-health') {
    loadQaList();
  } else if (sec === 'moments') {
    loadMomentsFeed();
  } else if (sec === 'date-ideas') {
    loadDateIdeas();
  } else if (sec === 'discover') {
    if (!(STATE.profiles && STATE.profiles.length) || !document.querySelector('#card-stack .s-card')) {
      loadDiscoverProfiles();
    }
  }

  // Guardar a aba ativa para persistir ao refrescar a página
  if (sec && sec !== 'chat') {
    localStorage.setItem('sigaleve_active_section', sec);
  }
}
