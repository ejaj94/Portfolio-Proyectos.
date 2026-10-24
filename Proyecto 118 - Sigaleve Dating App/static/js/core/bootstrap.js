/**
 * Arranque da aplicação (DOMContentLoaded): idioma, sessão, sidebar e atalhos de teclado. Mantém a posição original para preservar a ordem dos listeners.
 */
'use strict';

// ═══════════════════════════════════════════════════
// INICIALIZAÇÃO AUTOMÁTICA DE SESSÃO & SHORTCUTS PC
// ═══════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', async () => {
  try { initChatAntiScreenshot(); } catch (_) {}
  const urlParams = new URLSearchParams(window.location.search);
  const qLang = urlParams.get('lang');
  if (qLang) {
    localStorage.setItem('sigaleve_lang', qLang);
  }
  LANG = qLang || localStorage.getItem('sigaleve_lang') || 'pt';
  window.LANG = LANG;
  await setLang(LANG);
  if (typeof applyCurrentTheme === 'function') applyCurrentTheme();
  else updateDarkTog();

  // Se retornou com sucesso do fluxo OAuth Google
  const isSocialSuccess = (urlParams.get('google_auth_success') === 'true' || !!urlParams.get('social_auth_success'));
  if (isSocialSuccess) {
    localStorage.setItem('sigaleve_remember_me', 'true');
    window.history.replaceState({}, document.title, window.location.pathname);
  } else if (urlParams.get('error') === 'google_cancelled') {
    showAuthAlert('Autenticação com a conta Google cancelada.');
  } else if (urlParams.get('error')) {
    showAuthAlert('Falha na autenticação.');
  }

  // Pré-preencher o e-mail caso exista guardado em local ou sessão anterior
  const savedEmail = localStorage.getItem('sigaleve_saved_email');
  if (savedEmail) {
    const emailInput = document.getElementById('login-email');
    if (emailInput && !emailInput.value) emailInput.value = savedEmail;
  }

  // ══ ANTI-FLASH DO LOGIN ══
  // O #screen-auth começa escondido (display:none) e o #boot-splash fica visível
  // até /auth/me responder. hideBootSplash() garante que o splash nunca fica eterno.
  const hideBootSplash = () => {
    const splash = document.getElementById('boot-splash');
    if (splash) splash.style.display = 'none';
  };
  let bootResolved = false;
  const showLoginScreen = () => {
    hideBootSplash();
    document.getElementById('screen-auth').style.display = 'flex';
    document.getElementById('screen-app').style.display = 'none';
    switchAuthTab('login');
  };
  // Timeout de segurança (8s): se /auth/me demorar ou nunca responder,
  // cai para o login em vez de deixar o splash preso no ecrã.
  const bootTimeout = setTimeout(() => {
    if (!bootResolved) showLoginScreen();
  }, 8000);

  try {
    const res = await fetch('/api/v1/auth/me');
    if (res.ok) {
      const data = await res.json();
      if (data.authenticated && data.user) {
        // Sessão válida: entra automaticamente na aplicação (fix UX mobile —
        // antes o front fingia deslog e mostrava login mesmo com sessão ativa)
        bootResolved = true;
        clearTimeout(bootTimeout);
        if (data.user.email) localStorage.setItem('sigaleve_saved_email', data.user.email);
        // 🔧 FIX TELA BRANCA: o splash só sai DEPOIS de a UI estar pronta.
        // Antes: hideBootSplash() aqui deixava um gap de segundos com o fundo
        // nu (claro = branco) enquanto connectRealtime/matches/render ainda
        // rodavam — o "tela branca que só resolve com F5" reportado no mobile.
        try { onUserAuthenticated(data.user); } catch (e) { console.error('boot onUserAuthenticated:', e); }
        hideBootSplash();
      } else {
        bootResolved = true;
        clearTimeout(bootTimeout);
        showLoginScreen();
      }
    } else {
      bootResolved = true;
      clearTimeout(bootTimeout);
      showLoginScreen();
    }
  } catch (e) {
    // Erro de rede no /auth/me: mostra o login (nunca deixar splash eterno)
    bootResolved = true;
    clearTimeout(bootTimeout);
    showLoginScreen();
  }

  if (!localStorage.getItem('sigaleve_cookie_consent')) {
    setTimeout(() => {
      document.getElementById('cookie-banner').style.display = 'block';
    }, 1500);
  }

  // Atalhos de Teclado fiéis ao Tinder Web no PC (Frame 954)
  window.addEventListener('keydown', (e) => {
    // Ignorar se o utilizador estiver a escrever num campo de texto
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
    if (document.getElementById('screen-app').style.display !== 'flex') return;
    const sChat = document.getElementById('sec-chat');
    if (sChat && sChat.style.display === 'flex') return;

    const modal = document.getElementById('profile-detail-modal');
    const isModalOpen = modal && modal.classList.contains('open');

    // Seta Cima: Abrir perfil completo estilo Tinder
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (!isModalOpen && STATE.profiles.length > 0 && STATE.cursor < STATE.profiles.length) {
        openProfileDetail(STATE.profiles[STATE.cursor].id);
      }
      return;
    }

    // Seta Baixo ou ESC: Fechar perfil completo
    if (e.key === 'ArrowDown' || e.key === 'Escape') {
      if (isModalOpen) {
        e.preventDefault();
        closeProfileDetail();
        return;
      }
    }

    // Enter ou Barra de Espaço (quando modal fechado): Próxima foto do perfil
    if (e.key === 'Enter') {
      e.preventDefault();
      const topCard = document.querySelector('.s-card.top');
      if (topCard && topCard.dataset.pid) {
        changeCardPhoto(topCard.dataset.pid, 1);
      }
      return;
    }

    // Seta Esquerda: Não / Pass
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      if (isModalOpen) closeProfileDetail();
      swipe('nope');
    }
    // Seta Direita: Gosto / Like
    else if (e.key === 'ArrowRight') {
      e.preventDefault();
      if (isModalOpen) closeProfileDetail();
      swipe('like');
    }
    // Barra de Espaço: Super Like
    else if (e.key === ' ') {
      e.preventDefault();
      if (isModalOpen) closeProfileDetail();
      swipe('super');
    }
    // Z ou Voltar Atrás: Undo
    else if (e.key === 'z' || e.key === 'Z') {
      e.preventDefault();
      undoSwipe();
    }
  });
});
