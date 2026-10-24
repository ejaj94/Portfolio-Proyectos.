/**
 * Modais de definições: mensagens, utilizador, estado de atividade, notificações, privacidade, eliminar conta.
 */
// ══════════════════════════════════════════════════════════════════════════════
// CONTROLADORES DE LOS 5 MODALES NATIVOS (DEFAULT ACTIVO EN CUENTA NUEVA)
// ══════════════════════════════════════════════════════════════════════════════

function getSettingsPrefStorageKey(name) {
  const uid = (STATE.currentUser && (STATE.currentUser.id || STATE.currentUser.email)) || 'default';
  return 'sigaleve_pref_' + name + '_' + uid;
}

// 1. Controles de Mensajes
function openMessageControlsModal() {
  const modal = document.getElementById('modal-msg-controls');
  if (!modal) return;

  const photoVerify = localStorage.getItem(getSettingsPrefStorageKey('msg_photo_verify')) !== 'false';
  const filterLang = localStorage.getItem(getSettingsPrefStorageKey('msg_filter_lang')) !== 'false';

  const togPhoto = document.getElementById('tog-msg-photo-verify');
  const togLang = document.getElementById('tog-msg-filter-lang');
  if (togPhoto) togPhoto.className = 't-toggle flex-shrink-0' + (photoVerify ? ' on' : '');
  if (togLang) togLang.className = 't-toggle flex-shrink-0' + (filterLang ? ' on' : '');

  modal.classList.remove('hidden');
}

function closeMsgControlsModal() {
  const modal = document.getElementById('modal-msg-controls');
  if (modal) modal.classList.add('hidden');
}

function toggleMsgControlSwitch(type, el) {
  el.classList.toggle('on');
  const isEnabled = el.classList.contains('on');
  localStorage.setItem(getSettingsPrefStorageKey(type === 'photo_verify' ? 'msg_photo_verify' : 'msg_filter_lang'), isEnabled ? 'true' : 'false');
}

// 2. Nombre de Usuario
function openUsernameModal() {
  const modal = document.getElementById('modal-username-prompt');
  if (!modal) return;

  const inp = document.getElementById('username-dialog-input');
  const err = document.getElementById('username-error-msg');
  if (err) err.classList.add('hidden');

  let curUname = (STATE.currentUser && STATE.currentUser.username) || '';
  if (!curUname) {
    const rawVal = document.getElementById('drawer-username-val')?.textContent || '';
    if (rawVal.includes('@')) curUname = rawVal.replace(/[\s\n]+/g, ' ').trim().split(' ')[0];
  }
  if (!curUname && STATE.currentUser && STATE.currentUser.display_name) {
    curUname = '@' + STATE.currentUser.display_name.toLowerCase().replace(/[^a-z0-9_]/g, '');
  }
  if (inp) {
    inp.value = curUname || '@usuario';
    setTimeout(() => inp.focus(), 200);
  }

  modal.classList.remove('hidden');
}

function closeUsernameModal() {
  const modal = document.getElementById('modal-username-prompt');
  if (modal) modal.classList.add('hidden');
}

async function handleSaveUsernameSubmit(e) {
  e.preventDefault();
  const inp = document.getElementById('username-dialog-input');
  const err = document.getElementById('username-error-msg');
  if (!inp) return;
  let val = inp.value.trim();
  if (!val.startsWith('@')) val = '@' + val;

  if (val.length < 3) {
    if (err) {
      err.textContent = 'El nombre de usuario debe tener al menos 3 caracteres.';
      err.classList.remove('hidden');
    }
    return;
  }

  const drawerVal = document.getElementById('drawer-username-val');
  if (drawerVal) drawerVal.innerHTML = `${val} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;

  if (STATE.currentUser) STATE.currentUser.username = val;
  localStorage.setItem(getSettingsPrefStorageKey('username'), val);

  try {
    await fetch('/api/v1/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: STATE.currentUser && STATE.currentUser.email,
        username: val
      })
    });
  } catch(e){}

  closeUsernameModal();
}

// 3. Estatus de Actividad
function openActivityStatusModal() {
  const modal = document.getElementById('modal-activity-status');
  if (!modal) return;

  const isActivityActive = localStorage.getItem(getSettingsPrefStorageKey('activity_status')) !== 'false';
  const tog = document.getElementById('tog-activity-status');
  if (tog) tog.className = 't-toggle flex-shrink-0' + (isActivityActive ? ' on' : '');

  modal.classList.remove('hidden');
}

function closeActivityStatusModal() {
  const modal = document.getElementById('modal-activity-status');
  if (modal) modal.classList.add('hidden');
}

function toggleActivityStatusSwitch(el) {
  el.classList.toggle('on');
  const isEnabled = el.classList.contains('on');
  localStorage.setItem(getSettingsPrefStorageKey('activity_status'), isEnabled ? 'true' : 'false');
}

// 4. Notificaciones por Correo Electrónico
function openEmailNotifModal() {
  const modal = document.getElementById('modal-email-notif');
  if (!modal) return;

  const notifMatches = localStorage.getItem(getSettingsPrefStorageKey('email_notif_matches')) !== 'false';
  const notifMessages = localStorage.getItem(getSettingsPrefStorageKey('email_notif_messages')) !== 'false';
  const notifPromos = localStorage.getItem(getSettingsPrefStorageKey('email_notif_promos')) !== 'false';

  const togMatches = document.getElementById('tog-email-notif-matches');
  const togMessages = document.getElementById('tog-email-notif-messages');
  const togPromos = document.getElementById('tog-email-notif-promos');

  if (togMatches) togMatches.className = 't-toggle flex-shrink-0' + (notifMatches ? ' on' : '');
  if (togMessages) togMessages.className = 't-toggle flex-shrink-0' + (notifMessages ? ' on' : '');
  if (togPromos) togPromos.className = 't-toggle flex-shrink-0' + (notifPromos ? ' on' : '');

  modal.classList.remove('hidden');
}

function closeEmailNotifModal() {
  const modal = document.getElementById('modal-email-notif');
  if (modal) modal.classList.add('hidden');
}

function toggleEmailNotifSwitch(type, el) {
  el.classList.toggle('on');
  const isEnabled = el.classList.contains('on');
  localStorage.setItem(getSettingsPrefStorageKey('email_notif_' + type), isEnabled ? 'true' : 'false');
}

// 5. Notificaciones Push
function openPushNotifModal() {
  const modal = document.getElementById('modal-push-notif');
  if (!modal) return;

  const pushMatches = localStorage.getItem(getSettingsPrefStorageKey('push_notif_matches')) !== 'false';
  const pushMessages = localStorage.getItem(getSettingsPrefStorageKey('push_notif_messages')) !== 'false';
  const pushSuper = localStorage.getItem(getSettingsPrefStorageKey('push_notif_superlikes')) !== 'false';

  const togMatches = document.getElementById('tog-push-matches');
  const togMessages = document.getElementById('tog-push-messages');
  const togSuper = document.getElementById('tog-push-superlikes');

  if (togMatches) togMatches.className = 't-toggle flex-shrink-0' + (pushMatches ? ' on' : '');
  if (togMessages) togMessages.className = 't-toggle flex-shrink-0' + (pushMessages ? ' on' : '');
  if (togSuper) togSuper.className = 't-toggle flex-shrink-0' + (pushSuper ? ' on' : '');

  modal.classList.remove('hidden');
}

function closePushNotifModal() {
  const modal = document.getElementById('modal-push-notif');
  if (modal) modal.classList.add('hidden');
}

function togglePushNotifSwitch(type, el) {
  el.classList.toggle('on');
  const isEnabled = el.classList.contains('on');
  localStorage.setItem(getSettingsPrefStorageKey('push_notif_' + type), isEnabled ? 'true' : 'false');
}


function openConsentDataModal() {
  openPrivacySettingsModal();
}

function openPrivacySettingsModal() {
  const modal = document.getElementById('modal-privacy-settings');
  if (modal) modal.classList.remove('hidden');
}

function closePrivacySettingsModal() {
  const modal = document.getElementById('modal-privacy-settings');
  if (modal) modal.classList.add('hidden');
}

function togglePrivacyPref(key, el) {
  if (el) el.classList.toggle('on');
  const isEnabled = el ? el.classList.contains('on') : true;
  localStorage.setItem(getSettingsPrefStorageKey('privacy_' + key), isEnabled ? 'true' : 'false');
}

function openAppLanguageSelector() {
  openAppLanguageModal();
}

function toggleDistUnits() {
  const el = document.getElementById('drawer-dist-unit-val');
  if (!el) return;
  const isKm = el.textContent.includes('Km');
  el.innerHTML = `${isKm ? 'Mi' : 'Km'} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;
}

function shareAppPrompt() {
  if (navigator.share) {
    navigator.share({ title: 'Sigaleve Dating', text: 'Liga-te sem julgamentos no Sigaleve', url: window.location.origin });
  } else {
    navigator.clipboard.writeText(window.location.origin);
    showAppToast('🔗 Link do Sigaleve copiado para a área de transferência!', 'success');
  }
}

function promptDeleteAccount() {
  showAppConfirm(
    'Eliminar Conta Permanentemente',
    'Tens a certeza absoluta de que queres eliminar a tua conta? Esta ação não pode ser desfeita e apagará todos os teus matches, conversações e momentos.',
    () => {
      fetch('/api/v1/auth/delete-account', { method: 'POST', credentials: 'include' })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            showAppToast('✅ A tua conta foi eliminada permanentemente.', 'info');
            doLogout();
          } else {
            showAppToast(data.error || 'Não foi possível eliminar a conta. Tenta novamente.', 'error');
          }
        })
        .catch(() => showAppToast('Erro de rede ao eliminar a conta. Tenta novamente.', 'error'));
    },
    { danger: true, confirmText: 'Eliminar Conta', icon: 'fa-solid fa-triangle-exclamation' }
  );
}
