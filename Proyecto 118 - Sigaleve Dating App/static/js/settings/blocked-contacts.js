/**
 * Contactos bloqueados: lista local, adicionar e remover.
 */
// ══════════════════════════════════════════════════════════════════════════════
// GESTIÓN DE CONTACTOS BLOQUEADOS (ESTILO SIGALEVE NATIVO - SIN ALERTAS FEAS)
// ══════════════════════════════════════════════════════════════════════════════
let BLOCKED_CONTACTS_LIST = [];

function getBlockedContactsStorageKey() {
  const uid = (STATE.currentUser && (STATE.currentUser.id || STATE.currentUser.email)) || 'default';
  return 'sigaleve_blocked_contacts_' + uid;
}

function loadBlockedContacts() {
  try {
    const raw = localStorage.getItem(getBlockContactsStorageKey());
    if (raw) {
      BLOCKED_CONTACTS_LIST = JSON.parse(raw);
    } else {
      BLOCKED_CONTACTS_LIST = [
        { id: 'bc_1', contact: '912 345 678', name: 'Contacto importado', date: 'Bloqueado' },
        { id: 'bc_2', contact: 'ex_contacto@gmail.com', name: 'Contacto por email', date: 'Bloqueado' }
      ];
    }
  } catch(e) {
    BLOCKED_CONTACTS_LIST = [];
  }
}

function saveBlockedContacts() {
  try {
    localStorage.setItem(getBlockContactsStorageKey(), JSON.stringify(BLOCKED_CONTACTS_LIST));
  } catch(e){}
}

function openBlockContactsModal() {
  loadBlockedContacts();
  renderBlockedContactsUI();
  const modal = document.getElementById('modal-block-contacts');
  if (modal) modal.classList.remove('hidden');
}

function closeBlockContactsModal() {
  const modal = document.getElementById('modal-block-contacts');
  if (modal) modal.classList.add('hidden');
}

function renderBlockedContactsUI() {
  const container = document.getElementById('blocked-contacts-list-container');
  const countBadge = document.getElementById('blocked-contacts-count');
  if (!container) return;

  const currentLang = (typeof LANG !== 'undefined' && LANG) || localStorage.getItem('sigaleve_lang') || 'pt';
  const isEn = (currentLang === 'en');
  const isEs = (currentLang === 'es');
  
  if (countBadge) {
    const count = BLOCKED_CONTACTS_LIST.length;
    let text = `${count} ${count === 1 ? 'contacto bloqueado' : 'contactos bloqueados'}`;
    if (isEn) {
      text = `${count} ${count === 1 ? 'blocked contact' : 'blocked contacts'}`;
    }
    countBadge.textContent = text;
  }

  const unblockLabel = (typeof T === 'function' ? T('unblockBtn') : null) || (isEn ? 'Unblock' : 'Desbloquear');
  const noContactsText = (typeof T === 'function' ? T('noBlockedContacts') : null) || 
    (isEn ? 'You currently have no blocked contacts.' : (isEs ? 'No tienes ningún contacto bloqueado actualmente.' : 'Não tens nenhum contacto bloqueado atualmente.'));

  if (BLOCKED_CONTACTS_LIST.length === 0) {
    container.innerHTML = `
      <div class="py-8 text-center text-zinc-500 text-xs">
        <i class="fa-solid fa-user-check text-2xl text-zinc-600 mb-2 block"></i>
        <span>${noContactsText}</span>
      </div>
    `;
    return;
  }

  container.innerHTML = '';
  BLOCKED_CONTACTS_LIST.forEach((item, idx) => {
    const row = document.createElement('div');
    row.className = 'p-3 rounded-2xl bg-zinc-900 border border-zinc-800/80 flex items-center justify-between transition-all hover:border-zinc-700';
    row.innerHTML = `
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-full bg-red-500/10 text-red-400 flex items-center justify-center text-xs font-bold flex-shrink-0">
          <i class="fa-solid fa-ban"></i>
        </div>
        <div class="min-w-0">
          <p class="font-bold text-xs text-white truncate">${esc(item.contact)}</p>
          <p class="text-[10px] text-zinc-400">${esc(item.name || (isEn ? 'Blocked contact' : 'Contacto bloqueado'))}</p>
        </div>
      </div>
      <button type="button" onclick="removeBlockedContact(${idx})" class="px-2.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] font-semibold border border-zinc-700 transition-all flex items-center gap-1">
        <i class="fa-solid fa-trash-can text-red-400 text-[10px]"></i> ${unblockLabel}
      </button>
    `;
    container.appendChild(row);
  });
}

function handleAddNewBlockedContact(e) {
  e.preventDefault();
  const input = document.getElementById('block-contact-input');
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;

  const currentLang = (typeof LANG !== 'undefined' && LANG) || localStorage.getItem('sigaleve_lang') || 'pt';
  const duplicateMsg = currentLang === 'en' ? 'This contact is already in your blocked list.' :
    (currentLang === 'es' ? 'Este contacto ya se encuentra en tu lista de bloqueados.' : 'Este contacto já se encontra na tua lista de bloqueados.');

  if (BLOCKED_CONTACTS_LIST.some(c => c.contact.toLowerCase() === val.toLowerCase())) {
    showAppToast(duplicateMsg, 'error');
    return;
  }

  BLOCKED_CONTACTS_LIST.unshift({
    id: 'bc_' + Date.now(),
    contact: val,
    name: currentLang === 'en' ? 'Added manually' : (currentLang === 'es' ? 'Añadido manualmente' : 'Adicionado manualmente'),
    date: 'Hoje'
  });
  saveBlockedContacts();
  renderBlockedContactsUI();
  input.value = '';
}

function removeBlockedContact(idx) {
  if (idx >= 0 && idx < BLOCKED_CONTACTS_LIST.length) {
    BLOCKED_CONTACTS_LIST.splice(idx, 1);
    saveBlockedContacts();
    renderBlockedContactsUI();
  }
}
