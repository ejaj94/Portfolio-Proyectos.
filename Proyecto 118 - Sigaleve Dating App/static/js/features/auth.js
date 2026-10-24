/**
 * Autenticação: login, registo, verificação por código, 2FA (e-mail/TOTP), recuperação de palavra-passe, login social.
 */
'use strict';

// ═══════════════════════════════════════════════════
// VALIDAÇÃO VISUAL DA SENHA (REQUISITOS EM TEMPO REAL)
// ═══════════════════════════════════════════════════
function togglePasswordVisibility(inputId, eyeIconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(eyeIconId);
  if (!input || !icon) return;
  if (input.type === 'password') {
    input.type = 'text';
    icon.className = 'fa-solid fa-eye-slash text-purple-600';
  } else {
    input.type = 'password';
    icon.className = 'fa-solid fa-eye text-gray-400';
  }
}

function checkPasswordRules(pwd) {
  const rLen = pwd.length >= 8;
  const rUpper = /[A-Z]/.test(pwd);
  const rNum = /[0-9]/.test(pwd);
  const rSpec = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\/]/.test(pwd);

  updateRuleUI('rule-len', rLen);
  updateRuleUI('rule-upper', rUpper);
  updateRuleUI('rule-num', rNum);
  updateRuleUI('rule-spec', rSpec);
}

function updateRuleUI(id, pass) {
  const el = document.getElementById(id);
  if (!el) return;
  if (pass) {
    el.className = 'flex items-center gap-1.5 text-green-600 font-bold';
    el.querySelector('i').className = 'fa-solid fa-circle-check text-xs';
  } else {
    el.className = 'flex items-center gap-1.5 text-gray-400';
    el.querySelector('i').className = 'fa-solid fa-circle text-[7px]';
  }
}

function showAuthAlert(msg) {
  const alertBox = document.getElementById('auth-alert');
  const alertMsg = document.getElementById('auth-alert-msg');
  if (alertBox && alertMsg) {
    alertMsg.textContent = msg;
    alertBox.classList.remove('hidden');
  }
}
function hideAuthAlert() {
  const alertBox = document.getElementById('auth-alert');
  if (alertBox) alertBox.classList.add('hidden');
}

// ═══════════════════════════════════════════════════
// AUTENTICAÇÃO REAL (BACKEND FLASK + SESSÕES)
// ═══════════════════════════════════════════════════
function switchAuthTab(tab) {
  hideAuthAlert();
  const loginForm = document.getElementById('form-login');
  const regForm = document.getElementById('form-register');
  const loginTab = document.getElementById('tab-login');
  const regTab = document.getElementById('tab-register');

  if (tab === 'login') {
    if (loginForm) {
      loginForm.style.display = 'flex';
      loginForm.classList.remove('hidden');
    }
    if (regForm) {
      regForm.style.display = 'none';
      regForm.classList.add('hidden');
    }
    if (loginTab) {
      loginTab.classList.add('active');
      loginTab.style.removeProperty('color');
      loginTab.style.removeProperty('background');
    }
    if (regTab) {
      regTab.classList.remove('active');
      regTab.style.removeProperty('color');
      regTab.style.removeProperty('background');
    }
  } else {
    if (loginForm) {
      loginForm.style.display = 'none';
      loginForm.classList.add('hidden');
    }
    if (regForm) {
      regForm.style.display = 'flex';
      regForm.classList.remove('hidden');
    }
    if (regTab) {
      regTab.classList.add('active');
      regTab.style.removeProperty('color');
      regTab.style.removeProperty('background');
    }
    if (loginTab) {
      loginTab.classList.remove('active');
      loginTab.style.removeProperty('color');
      loginTab.style.removeProperty('background');
    }
  }
}

function getDeviceId() {
  let devId = localStorage.getItem('sigaleve_device_id');
  if (!devId) {
    devId = 'dev_' + Math.random().toString(36).substring(2, 12);
    localStorage.setItem('sigaleve_device_id', devId);
  }
  return devId;
}

let pendingAuthEmail = '';
let currentVerifyLink = '';
let currentAuthMethod = 'email'; // 'email' | 'totp'

function openVerifyModal(email, verifyLink, otpCode, subtitle, authMethod = 'email') {
  pendingAuthEmail = email;
  currentVerifyLink = verifyLink || '';
  currentAuthMethod = authMethod;

  const modal = document.getElementById('modal-auth-verify');
  if (!modal) return;

  const titleEl = document.getElementById('verify-modal-title');
  const subEl = document.getElementById('verify-modal-sub');
  const emailBox = document.getElementById('verify-email-details');
  const totpBox = document.getElementById('verify-totp-details');
  const resendBtn = document.getElementById('btn-resend-verify');
  const icon = document.getElementById('verify-icon');
  const inputLabel = document.getElementById('verify-input-label');

  if (authMethod === 'totp') {
    if (titleEl) titleEl.textContent = 'Autenticación en 2 Pasos (TOTP)';
    if (subEl) subEl.textContent = 'Introduce el código dinámico de 6 dígitos que muestra tu app (Google Authenticator o Authy).';
    if (icon) icon.className = 'fa-solid fa-mobile-screen-button text-2xl';
    if (emailBox) emailBox.classList.add('hidden');
    if (totpBox) totpBox.classList.remove('hidden');
    if (resendBtn) resendBtn.classList.add('hidden');
    if (inputLabel) inputLabel.textContent = 'Introduce el código de Google Authenticator:';
  } else {
    if (titleEl) titleEl.textContent = 'Verificación de Seguridad';
    if (subEl) subEl.textContent = subtitle || 'Enviamos un enlace de confirmación y un código a tu correo.';
    if (icon) icon.className = 'fa-solid fa-envelope-circle-check text-2xl';
    if (emailBox) emailBox.classList.remove('hidden');
    if (totpBox) totpBox.classList.add('hidden');
    if (resendBtn) resendBtn.classList.remove('hidden');
    if (inputLabel) inputLabel.textContent = 'Introduce el código de 6 dígitos:';
  }

  const emailEl = document.getElementById('verify-target-email-text');
  if (emailEl) emailEl.textContent = email;

  const linkEl = document.getElementById('verify-direct-link');
  if (linkEl && verifyLink) linkEl.href = verifyLink;

  const codeEl = document.getElementById('verify-preview-code');
  if (codeEl) codeEl.textContent = otpCode || '------';

  const badgeEl = document.getElementById('badge-link-confirmed');
  if (badgeEl) badgeEl.classList.add('hidden');

  const errEl = document.getElementById('verify-error-msg');
  if (errEl) errEl.classList.add('hidden');

  const inp = document.getElementById('verify-otp-input');
  if (inp) {
    inp.value = '';
    setTimeout(() => inp.focus(), 300);
  }

  modal.classList.remove('hidden');
}

// ══════════════════════════════════════════════════════════════════════════════
// GESTIÓN DE 2FA (MODAL DE AJUSTES: TOTP & EMAIL)
// ══════════════════════════════════════════════════════════════════════════════

let current2FAState = { enabled: false, method: 'none', has_totp: false };
let currentTotpSecret = '';

async function fetch2FAStatus() {
  try {
    const res = await fetch('/api/v1/auth/2fa/status');
    const data = await res.json();
    if (res.ok && data.success) {
      current2FAState = data.two_factor;
      render2FAStatusUI();
    }
  } catch (e) {
    console.error('Error fetching 2FA status:', e);
  }
}

function render2FAStatusUI() {
  const badgeText = document.getElementById('drawer-2fa-status-text');
  const dot = document.getElementById('modal-2fa-status-dot');
  const statusTitle = document.getElementById('modal-2fa-status-title');
  const statusSub = document.getElementById('modal-2fa-status-sub');
  const btnDisable = document.getElementById('btn-2fa-disable');

  const checkTotp = document.querySelector('#check-method-totp i');
  const checkEmail = document.querySelector('#check-method-email i');
  const cardTotp = document.getElementById('card-method-totp');
  const cardEmail = document.getElementById('card-method-email');

  if (checkTotp) checkTotp.classList.add('hidden');
  if (checkEmail) checkEmail.classList.add('hidden');
  if (cardTotp) cardTotp.classList.remove('border-purple-500', 'bg-purple-950/20');
  if (cardEmail) cardEmail.classList.remove('border-pink-500', 'bg-pink-950/20');

  if (current2FAState.enabled) {
    const methodLabel = current2FAState.method === 'totp' ? T('authenticatorAppLabel') : T('codeByEmailLabel');
    if (badgeText) badgeText.innerHTML = `<span class="text-emerald-400 font-bold">${T('activeStatusLabel')} (${methodLabel})</span>`;
    if (dot) { dot.className = 'w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]'; }
    if (statusTitle) statusTitle.textContent = `${T('twoFactorActiveTitle')} (${methodLabel})`;
    if (statusSub) statusSub.textContent = T('twoFactorActiveDesc');
    if (btnDisable) btnDisable.classList.remove('hidden');

    if (current2FAState.method === 'totp') {
      if (checkTotp) checkTotp.classList.remove('hidden');
      if (cardTotp) cardTotp.classList.add('border-purple-500', 'bg-purple-950/20');
    } else if (current2FAState.method === 'email') {
      if (checkEmail) checkEmail.classList.remove('hidden');
      if (cardEmail) cardEmail.classList.add('border-pink-500', 'bg-pink-950/20');
    }
  } else {
    if (badgeText) badgeText.innerHTML = T('disabledStatusLabel');
    if (dot) { dot.className = 'w-2.5 h-2.5 rounded-full bg-zinc-500'; }
    if (statusTitle) statusTitle.textContent = T('twoFactorDisabledTitle');
    if (statusSub) statusSub.textContent = T('twoFactorDisabledDesc');
    if (btnDisable) btnDisable.classList.add('hidden');
  }
}

async function open2FAModal() {
  const modal = document.getElementById('modal-2fa-settings');
  if (!modal) return;
  modal.classList.remove('hidden');

  // Reset panels
  document.getElementById('panel-setup-totp')?.classList.add('hidden');
  document.getElementById('panel-setup-email')?.classList.add('hidden');

  await fetch2FAStatus();
}

function close2FAModal() {
  const modal = document.getElementById('modal-2fa-settings');
  if (modal) modal.classList.add('hidden');
}

async function select2FAMethod(method) {
  const panelTotp = document.getElementById('panel-setup-totp');
  const panelEmail = document.getElementById('panel-setup-email');

  if (method === 'totp') {
    if (panelEmail) panelEmail.classList.add('hidden');
    if (panelTotp) panelTotp.classList.remove('hidden');
    await startTotpSetup();
  } else if (method === 'email') {
    if (panelTotp) panelTotp.classList.add('hidden');
    if (panelEmail) panelEmail.classList.remove('hidden');
  }
}

async function startTotpSetup() {
  const qrImg = document.getElementById('totp-qr-img');
  const secretKey = document.getElementById('totp-secret-key');
  const errEl = document.getElementById('totp-setup-error');
  if (errEl) errEl.classList.add('hidden');

  try {
    const res = await fetch('/api/v1/auth/2fa/setup-totp', { method: 'POST' });
    const data = await res.json();
    if (res.ok && data.success) {
      currentTotpSecret = data.secret;
      if (qrImg) qrImg.src = data.qr_code;
      if (secretKey) secretKey.textContent = data.secret;
    } else {
      if (errEl) {
        errEl.textContent = data.error || 'Error al generar la configuración TOTP.';
        errEl.classList.remove('hidden');
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.textContent = 'Error de conexión con el servidor.';
      errEl.classList.remove('hidden');
    }
  }
}

function copyTotpSecret() {
  if (!currentTotpSecret) return;
  navigator.clipboard.writeText(currentTotpSecret).then(() => {
    showAppToast('Chave secreta copiada para a área de transferência.', 'info');
  }).catch(() => {
    showAppToast('Chave: ' + currentTotpSecret, 'info');
  });
}

async function confirmTotpSetup() {
  const codeInp = document.getElementById('totp-setup-code-inp');
  const errEl = document.getElementById('totp-setup-error');
  const btn = document.getElementById('btn-confirm-totp');
  const code = codeInp ? codeInp.value.trim().replace(/\s/g, '') : '';

  if (!code || code.length < 6) {
    if (errEl) {
      errEl.textContent = 'Introduza o código de 6 dígitos completo gerado pela aplicação.';
      errEl.classList.remove('hidden');
    }
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A validar código...';

  try {
    const res = await fetch('/api/v1/auth/2fa/verify-setup-totp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      current2FAState = data.two_factor;
      render2FAStatusUI();
      document.getElementById('panel-setup-totp')?.classList.add('hidden');
      showAppToast('Google Authenticator ativado com sucesso para a tua conta!', 'success');
    } else {
      if (errEl) {
        errEl.textContent = data.error || 'Código incorreto. Verifica a hora do teu telemóvel e tenta novamente.';
        errEl.classList.remove('hidden');
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.textContent = 'Erro de ligação com o servidor.';
      errEl.classList.remove('hidden');
    }
  } finally {
    btn.disabled = false;
    btn.textContent = T('totpVerifyActivate');
  }
}

async function requestEmail2FACode() {
  const btn = document.getElementById('btn-request-email-code');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A enviar código para o teu e-mail...';
  }

  const errEl = document.getElementById('email-2fa-error-msg');
  if (errEl) errEl.classList.add('hidden');

  try {
    const res = await fetch('/api/v1/auth/2fa/send-email-code', { method: 'POST' });
    const data = await res.json();
    if (res.ok && data.success) {
      document.getElementById('panel-email-step-request')?.classList.add('hidden');
      document.getElementById('panel-email-step-verify')?.classList.remove('hidden');
      
      const desc = document.getElementById('panel-email-desc');
      if (desc) {
        desc.innerHTML = `Código enviado para <strong class="text-white">${data.email}</strong>. Consulta a tua caixa de entrada.`;
      }

      showAppToast(`Código de confirmação enviado para ${data.email}`, 'info');
      
      const otpInput = document.getElementById('email-2fa-otp-input');
      if (otpInput) {
        otpInput.value = '';
        setTimeout(() => otpInput.focus(), 300);
      }
    } else {
      showAppToast(data.error || 'Erro ao enviar código por e-mail.', 'error');
    }
  } catch (err) {
    showAppToast('Erro de comunicação com o servidor.', 'error');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> <span>Enviar Código para o Meu E-mail</span>';
    }
  }
}

async function verifyEmail2FACode() {
  const input = document.getElementById('email-2fa-otp-input');
  const code = input ? input.value.trim().replace(/\s/g, '') : '';
  const errEl = document.getElementById('email-2fa-error-msg');
  const btn = document.getElementById('btn-verify-email-code');

  if (!code || code.length < 6) {
    if (errEl) {
      errEl.textContent = 'Introduza o código de 6 dígitos que recebeu no e-mail.';
      errEl.classList.remove('hidden');
    }
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A validar código...';
  if (errEl) errEl.classList.add('hidden');

  try {
    const res = await fetch('/api/v1/auth/2fa/verify-email-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      current2FAState = data.two_factor;
      render2FAStatusUI();
      document.getElementById('panel-setup-email')?.classList.add('hidden');
      showAppToast('Verificação por Código de E-mail ativada com sucesso!', 'success');
    } else {
      if (errEl) {
        errEl.textContent = data.error || 'Código incorreto. Verifica o e-mail recebido e tenta novamente.';
        errEl.classList.remove('hidden');
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.textContent = 'Erro de ligação com o servidor.';
      errEl.classList.remove('hidden');
    }
  } finally {
    btn.disabled = false;
    btn.textContent = T('verifyEmailCode');
  }
}

async function disable2FA() {
  showAppConfirm(
    'Desativar Verificação em Duas Etapas',
    'Tens a certeza de que desejas desativar o 2FA? A tua conta ficará mais vulnerável.',
    async () => {
      try {
        const res = await fetch('/api/v1/auth/2fa/disable', { method: 'POST' });
        const data = await res.json();
        if (res.ok && data.success) {
          current2FAState = data.two_factor;
          render2FAStatusUI();
          document.getElementById('panel-setup-totp')?.classList.add('hidden');
          document.getElementById('panel-setup-email')?.classList.add('hidden');
          showAppToast('Verificação em duas etapas desativada.', 'info');
        } else {
          showAppToast(data.error || 'Erro ao desativar 2FA.', 'error');
        }
      } catch (err) {
        showAppToast('Erro ao contactar o servidor.', 'error');
      }
    }
  );
}

function closeVerifyModal() {
  const modal = document.getElementById('modal-auth-verify');
  if (modal) modal.classList.add('hidden');
}

async function markEmailVerified() {
  // Confirmar imediatamente no servidor em segundo plano e atualizar a UI
  try {
    if (currentVerifyLink) {
      await fetch(currentVerifyLink, { method: 'GET', mode: 'no-cors' });
    }
  } catch (err) {}

  const badgeEl = document.getElementById('badge-link-confirmed');
  if (badgeEl) badgeEl.classList.remove('hidden');

  const codeEl = document.getElementById('verify-preview-code');
  if (codeEl && codeEl.textContent !== '------') {
    const inp = document.getElementById('verify-otp-input');
    if (inp && !inp.value) inp.value = codeEl.textContent.trim();
  }
}

function copyOtpCode() {
  const codeEl = document.getElementById('verify-preview-code');
  if (codeEl) {
    const code = codeEl.textContent.trim();
    if (!code || code === '------') return;
    navigator.clipboard.writeText(code).then(() => {
      const inp = document.getElementById('verify-otp-input');
      if (inp) inp.value = code;
    }).catch(() => {
      const inp = document.getElementById('verify-otp-input');
      if (inp) inp.value = code;
    });
  }
}

async function handleVerifyOtpSubmit(e) {
  e.preventDefault();
  const inp = document.getElementById('verify-otp-input');
  const errEl = document.getElementById('verify-error-msg');
  const btn = document.getElementById('btn-verify-submit');
  const code = inp.value.trim();

  if (!code || code.length < 6) {
    if (errEl) {
      errEl.textContent = 'Introduza o código de 6 dígitos completo.';
      errEl.classList.remove('hidden');
    }
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> ' + T('verifyingDots');

  try {
    const res = await fetch('/api/v1/auth/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: pendingAuthEmail,
        code: code,
        device_id: getDeviceId()
      })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      closeVerifyModal();
      const remember = document.getElementById('login-remember') ? document.getElementById('login-remember').checked : false;
      if (remember) {
        localStorage.setItem('sigaleve_remember_me', 'true');
        if (data.user && data.user.email) {
          localStorage.setItem('sigaleve_saved_email', data.user.email);
        }
      } else {
        localStorage.removeItem('sigaleve_remember_me');
        localStorage.removeItem('sigaleve_saved_email');
      }
      onUserAuthenticated(data.user);
    } else {
      if (errEl) {
        errEl.textContent = data.error || 'Código incorreto. Verifique o seu e-mail.';
        errEl.classList.remove('hidden');
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.textContent = 'Erro de ligação com o servidor.';
      errEl.classList.remove('hidden');
    }
  } finally {
    btn.disabled = false;
    btn.textContent = T('verifyConfirmEnter');
  }
}

async function resendVerificationCode() {
  if (!pendingAuthEmail) return;
  try {
    const res = await fetch('/api/v1/auth/resend-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: pendingAuthEmail })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      if (data.otp_code) {
        document.getElementById('verify-preview-code').textContent = data.otp_code;
      }
      if (data.verify_link) {
        document.getElementById('verify-direct-link').href = data.verify_link;
      }
      showAppToast('Novo código de acesso e ligação enviados com sucesso para ' + pendingAuthEmail, 'info');
    }
  } catch (e) {
    showAppToast('Erro ao reenviar código.', 'error');
  }
}

// ── Gestão de Recuperação de Palavra-passe ────────────────────────────────
let lastGeneratedPassword = '';

function openForgotPasswordModal() {
  const m = document.getElementById('modal-forgot-password');
  const loginEmail = document.getElementById('login-email')?.value.trim();
  const forgotInput = document.getElementById('forgot-email');
  if (forgotInput && loginEmail) {
    forgotInput.value = loginEmail;
  }
  
  // Limpar alertas anteriores
  const errEl = document.getElementById('forgot-alert-error');
  const succEl = document.getElementById('forgot-alert-success');
  if (errEl) errEl.classList.add('hidden');
  if (succEl) succEl.classList.add('hidden');
  
  const form = document.getElementById('form-forgot-password');
  if (form) form.classList.remove('hidden');

  if (m) m.classList.remove('hidden');
}

function closeForgotPasswordModal() {
  const m = document.getElementById('modal-forgot-password');
  if (m) m.classList.add('hidden');
}

async function handleForgotPasswordSubmit(e) {
  e.preventDefault();
  const emailInput = document.getElementById('forgot-email');
  const email = emailInput ? emailInput.value.trim() : '';
  const btn = document.getElementById('btn-forgot-submit');
  const errEl = document.getElementById('forgot-alert-error');
  const errMsgEl = document.getElementById('forgot-alert-error-msg');
  const succEl = document.getElementById('forgot-alert-success');
  const succMsgEl = document.getElementById('forgot-alert-success-msg');
  const form = document.getElementById('form-forgot-password');

  if (!email) return;

  if (errEl) errEl.classList.add('hidden');
  if (succEl) succEl.classList.add('hidden');

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A gerar e a enviar...';

  try {
    const res = await fetch('/api/v1/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await res.json();

    if (res.ok && data.success) {
      lastGeneratedPassword = '';
      if (succMsgEl) succMsgEl.textContent = data.message || 'Se a conta existir, enviámos um link de recuperação para o teu e-mail.';
      if (succEl) succEl.classList.remove('hidden');
      if (form) form.classList.add('hidden');
    } else {
      if (errMsgEl) errMsgEl.textContent = data.error || 'Não foi possível recuperar a palavra-passe.';
      if (errEl) errEl.classList.remove('hidden');
    }
  } catch (err) {
    if (errMsgEl) errMsgEl.textContent = 'Erro ao contactar o servidor. Tente novamente.';
    if (errEl) errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-paper-plane text-xs"></i> <span>Gerar e Enviar Nova Palavra-passe</span>';
  }
}

// 🔒 Fluxo reset por link: deteta ?reset_token= na URL e abre o form de nova senha
function handleResetTokenFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('reset_token');
  if (!token) return;
  window.__resetToken = token;
  // limpar o token da URL (nao fica no historico)
  try { window.history.replaceState({}, document.title, window.location.pathname + '?lang=' + (new URLSearchParams(window.location.search).get('lang') || '')); } catch (e) {}
  // abrir modal do forgot com o form de reset visivel
  setTimeout(() => {
    const form = document.getElementById('form-reset-password');
    const forgotForm = document.getElementById('form-forgot-password');
    const modal = document.getElementById('modal-forgot-password');
    if (forgotForm) forgotForm.classList.add('hidden');
    if (form) form.classList.remove('hidden');
    if (modal) modal.classList.remove('hidden');
  }, 800);
}

async function handleResetPasswordSubmit(e) {
  e.preventDefault();
  const token = window.__resetToken;
  const pass = document.getElementById('reset-new-password')?.value || '';
  const confirm = document.getElementById('reset-confirm-password')?.value || '';
  const errEl = document.getElementById('reset-alert-error');
  const btn = document.getElementById('btn-reset-submit');

  if (!token) { if (errEl) { errEl.textContent = 'Link de recuperação inválido. Pede um novo.'; errEl.classList.remove('hidden'); } return; }
  if (pass !== confirm) { if (errEl) { errEl.textContent = 'As palavras-passe não coincidem.'; errEl.classList.remove('hidden'); } return; }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A guardar...';
  try {
    const res = await fetch('/api/v1/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, new_password: pass })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      if (errEl) errEl.classList.add('hidden');
      btn.innerHTML = '<i class="fa-solid fa-check"></i> ' + (data.message || 'Palavra-passe redefinida!');
      setTimeout(() => { window.location.href = '/app?lang=br'; }, 1800);
    } else {
      if (errEl) { errEl.textContent = data.error || 'Não foi possível redefinir a palavra-passe.'; errEl.classList.remove('hidden'); }
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-key text-xs"></i> <span>Guardar Nova Palavra-passe</span>';
    }
  } catch (err) {
    if (errEl) { errEl.textContent = 'Erro ao contactar o servidor. Tente novamente.'; errEl.classList.remove('hidden'); }
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-key text-xs"></i> <span>Guardar Nova Palavra-passe</span>';
  }
}

function useNewPasswordAndLogin() {
  const emailVal = document.getElementById('forgot-email')?.value.trim();
  const loginEmail = document.getElementById('login-email');
  const loginPass = document.getElementById('login-password');

  if (loginEmail && emailVal) loginEmail.value = emailVal;
  if (loginPass && lastGeneratedPassword) loginPass.value = lastGeneratedPassword;

  closeForgotPasswordModal();
  switchAuthTab('login');

  // Destacar o formulário de login pronto para entrar
  const submitBtn = document.getElementById('btn-login-submit');
  if (submitBtn) {
    submitBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    submitBtn.classList.add('ring-4', 'ring-pink-500');
    setTimeout(() => submitBtn.classList.remove('ring-4', 'ring-pink-500'), 2500);
  }
}

async function handleSocialAuth(provider) {
  hideAuthAlert();
  startGoogleAuth();
}

function openSocialPickerModal() {
  const m = document.getElementById('modal-social-picker');
  if (m) m.classList.remove('hidden');
  initGoogleOneTap();
}

function closeSocialPickerModal() {
  const m = document.getElementById('modal-social-picker');
  if (m) m.classList.add('hidden');
}

const GOOGLE_CLIENT_ID = "86970408130-8ugh10poqvbespttgfqr5553hkgvkn4d.apps.googleusercontent.com";

function startGoogleAuth() {
  hideAuthAlert();
  // Redirecionamento direto e limpo ao endpoint OAuth 2.0 do servidor
  window.location.href = '/auth/google/login';
}

function initGoogleOneTap() {
  // O fluxo de login do Google agora utiliza o padrão OAuth 2.0 seguro via redirecionamento de servidor
}

window.addEventListener('DOMContentLoaded', () => {
  // DOM pronto
  // 🔒 Reset por link: deteta ?reset_token= e abre o form de nova senha
  handleResetTokenFromUrl();
  const resetForm = document.getElementById('form-reset-password');
  if (resetForm) resetForm.addEventListener('submit', handleResetPasswordSubmit);
});

// ── PWA: DESATIVADO por decisão de produto (2026-10-13) ──────────────────────
// O service worker deixava o app lento/defasado para os nossos utilizadores.
// Este bloco GARANTE que qualquer SW antigo (de versões anteriores) é removido
// do navegador de quem já visitou o site, e não volta a ser registado.
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const regs = await navigator.serviceWorker.getRegistrations();
      await Promise.all(regs.map(r => r.unregister()));
      const keys = await caches.keys();
      await Promise.all(keys.filter(k => k.startsWith('sigaleve')).map(k => caches.delete(k)));
      console.log('[sigaleve] Service worker antigo removido (PWA desativado).');
    } catch (e) { /* silencioso: sem SW registrado é o comportamento desejado */ }
  });
}

// ── PUSH: DESATIVADO junto com o PWA (push web precisa do service worker) ────
async function ensurePushSubscription() {
  // PWA desativado por decisão de produto — push web indisponível sem service worker.
  return;
}






async function handleLoginSubmit(e) {
  e.preventDefault();
  hideAuthAlert();
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  const btn = document.getElementById('btn-login-submit');

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A validar...';

  let loginSuccess = false;
  let authUser = null;

  try {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        password,
        device_id: getDeviceId()
      })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      if (data.requires_verification) {
        openVerifyModal(
          data.email || email,
          data.verify_link,
          data.otp_code,
          data.message || 'Verificación de seguridad en 2 pasos.',
          data.auth_method || 'email'
        );
      } else {
        loginSuccess = true;
        authUser = data.user;
        const remember = document.getElementById('login-remember') ? document.getElementById('login-remember').checked : false;
        if (remember) {
          localStorage.setItem('sigaleve_remember_me', 'true');
          if (email) localStorage.setItem('sigaleve_saved_email', email);
        } else {
          localStorage.removeItem('sigaleve_remember_me');
          localStorage.removeItem('sigaleve_saved_email');
        }
      }
    } else {
      showAuthAlert(data.error || 'Falha ao iniciar sessão.');
    }
  } catch (err) {
    console.error('Fetch login error:', err);
    showAuthAlert('Erro de ligação ao servidor.');
  } finally {
    btn.disabled = false;
    btn.textContent = T('login');
  }

  if (loginSuccess && authUser) {
    try {
      onUserAuthenticated(authUser);
    } catch (err) {
      console.error('Error in onUserAuthenticated post-login:', err);
    }
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  hideAuthAlert();

  const name = document.getElementById('reg-name').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const phoneRaw = document.getElementById('reg-phone').value.trim();
  const phonePrefix = document.getElementById('reg-phone-prefix') ? document.getElementById('reg-phone-prefix').value : '';
  const phone = phoneRaw ? (phoneRaw.startsWith('+') ? phoneRaw : `${phonePrefix} ${phoneRaw}`) : '';
  const password = document.getElementById('reg-password').value;
  const confirm = document.getElementById('reg-confirm').value;
  const dob = document.getElementById('reg-dob').value;
  const btn = document.getElementById('btn-reg-submit');

  if (password !== confirm) {
    showAuthAlert('As palavras-passe não coincidem.');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A criar conta segura...';

  try {
    const res = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        phone,
        password,
        confirm_password: confirm,
        date_of_birth: dob,
        device_id: getDeviceId()
      })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      if (data.requires_verification) {
        openVerifyModal(
          data.email || email,
          data.verify_link,
          data.otp_code,
          'A tua conta foi registada! Confirma primeiro a ligação enviada e em seguida digita o teu código de 6 dígitos.'
        );
      } else {
        localStorage.setItem('sigaleve_remember_me', 'true');
        onUserAuthenticated(data.user);
        openOnboardingModal();
      }
    } else {
      showAuthAlert(data.error || 'Erro ao criar conta.');
    }
  } catch (err) {
    showAuthAlert('Erro de comunicação com o servidor.');
  } finally {
    btn.disabled = false;
    btn.textContent = T('createAccount');
  }
}

function onUserAuthenticated(user) {
  STATE.currentUser = user;

  // 🔄 TEMPO REAL: ligar o socket ao entrar (não só ao abrir um chat)
  connectRealtime();

  // 🔔 PUSH: subscrever notificações depois do login (silencioso, opcional)
  ensurePushSubscription();

  // Transição de ecrã imediata e garantida
  const appMax = document.querySelector('.app-max');
  if (appMax) appMax.classList.remove('is-auth');
  const scrAuth = document.getElementById('screen-auth');
  if (scrAuth) {
    scrAuth.style.display = 'none';
    scrAuth.classList.add('hidden');
  }
  const scrApp = document.getElementById('screen-app');
  if (scrApp) {
    scrApp.classList.remove('hidden');
    scrApp.style.display = 'flex';
  }

  try {
    updateProfileUI(user);
  } catch(e) {
    console.error('Error in updateProfileUI:', e);
  }

  try {
    initUserPreferencesUI();
  } catch(e) {
    console.error('Error in initUserPreferencesUI:', e);
  }

  try {
    fetch2FAStatus();
  } catch(e) {
    console.error('Error in fetch2FAStatus:', e);
  }

  // Sanitização rigorosa: Eliminar quaisquer perfis de teste ou mock legados do cache
  const userMatchesKey = 'sigaleve_matches_' + (user.id || user.email);
  try {
    const saved = localStorage.getItem(userMatchesKey);
    if (saved) {
      const parsed = JSON.parse(saved);
      // Filtrar estritamente perfis que não sejam do sistema de teste (p1..p7, mock_)
      const mockNames = ['kofi', 'lucas', 'joão', 'mariana', 'beatriz', 'inês', 'camila', 'linda'];
      MATCHES_DATA = (Array.isArray(parsed) ? parsed : []).filter(m => {
        if (!m || !m.id) return false;
        const idStr = String(m.id).toLowerCase();
        const nameStr = String(m.name || '').toLowerCase();
        if (idStr.startsWith('p') || idStr.startsWith('mock_')) return false;
        if (mockNames.some(mn => nameStr.includes(mn))) return false;
        return true;
      });
      localStorage.setItem(userMatchesKey, JSON.stringify(MATCHES_DATA));
    } else {
      MATCHES_DATA = [];
    }
  } catch(e) {
    MATCHES_DATA = [];
  }
  try { renderMatches(); } catch(e){}

  // Sincronizar matches reais a partir do servidor (PostgreSQL / store)
  fetch('/api/v1/matches')
    .then(r => r.json())
    .then(data => {
      if (data && Array.isArray(data.matches)) {
        MATCHES_DATA = data.matches;
        try {
          localStorage.setItem(userMatchesKey, JSON.stringify(MATCHES_DATA));
        } catch(e){}
        renderMatches();
      }
    })
    .catch(() => {});
  
  if (user && user.is_profile_configured === false) {
    showSection('profile');
    openOnboardingModal();
  } else {
    const lastSec = localStorage.getItem('sigaleve_active_section') || 'discover';
    showSection(lastSec);
    if (lastSec === 'discover') {
      loadDiscoverProfiles();
    } else if (lastSec === 'moments') {
      loadMomentsFeed();
    } else if (lastSec === 'qa-health') {
      loadQaList();
    }
    renderMatches();
  }
}
