/**
 * Componentes de feedback: toasts, confirmação e prompt personalizados (substituem alert/confirm/prompt).
 */
'use strict';

// ══════════════════════════════════════════════════════════════════════════════
// SISTEMA NATIVO DE NOTIFICAÇÕES (TOAST) E DIÁLOGOS DE CONFIRMAÇÃO NATIVOS
// ══════════════════════════════════════════════════════════════════════════════
function showAppToast(msg, type = 'success', duration = 4000) {
  const container = document.getElementById('app-toast-container');
  if (!container) {
    console.log(msg);
    return;
  }
  const toast = document.createElement('div');
  const bgStyles = type === 'success'
    ? 'bg-zinc-950/95 border-emerald-500/50 text-white shadow-[0_10px_30px_rgba(16,185,129,0.25)]'
    : (type === 'error'
      ? 'bg-zinc-950/95 border-rose-500/50 text-white shadow-[0_10px_30px_rgba(244,63,94,0.25)]'
      : 'bg-zinc-950/95 border-purple-500/50 text-white shadow-[0_10px_30px_rgba(168,85,247,0.25)]');

  const iconHtml = type === 'success'
    ? '<div class="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0 text-sm"><i class="fa-solid fa-circle-check"></i></div>'
    : (type === 'error'
      ? '<div class="w-8 h-8 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center flex-shrink-0 text-sm"><i class="fa-solid fa-circle-xmark"></i></div>'
      : '<div class="w-8 h-8 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center flex-shrink-0 text-sm"><i class="fa-solid fa-bell"></i></div>');

  toast.className = `pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-2xl border text-xs font-semibold backdrop-blur-xl transition-all duration-300 transform translate-y-[-10px] opacity-0 ${bgStyles}`;
  toast.innerHTML = `
    ${iconHtml}
    <div class="flex-1 leading-snug">${msg}</div>
    <button onclick="this.parentElement.remove()" class="text-zinc-500 hover:text-white text-xs ml-2"><i class="fa-solid fa-xmark"></i></button>
  `;
  container.appendChild(toast);

  // Trigger smooth enter animation
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-[-10px]', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');
  });

  setTimeout(() => {
    toast.classList.remove('translate-y-0', 'opacity-100');
    toast.classList.add('translate-y-[-10px]', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

function showAppConfirm(title, message, onConfirm, options = {}) {
  const modal = document.getElementById('app-confirm-modal');
  if (!modal) return;

  document.getElementById('app-confirm-title').textContent = title || 'Confirmação';
  document.getElementById('app-confirm-message').textContent = message || '';

  const iconBox = document.getElementById('app-confirm-icon-box');
  const iconEl = document.getElementById('app-confirm-icon');
  const okBtn = document.getElementById('app-confirm-ok-btn');
  const cancelBtn = document.getElementById('app-confirm-cancel-btn');

  if (options.danger) {
    if (iconBox) iconBox.className = 'w-14 h-14 rounded-2xl flex items-center justify-center mx-auto text-2xl bg-rose-500/20 text-rose-400 border border-rose-500/30 shadow-inner';
    if (iconEl) iconEl.className = options.icon || 'fa-solid fa-trash-can';
    if (okBtn) okBtn.className = 'flex-1 py-3 rounded-xl bg-gradient-to-r from-rose-600 to-red-600 text-white font-black text-xs shadow-lg hover:opacity-90 active:scale-95 transition-all';
  } else {
    if (iconBox) iconBox.className = 'w-14 h-14 rounded-2xl flex items-center justify-center mx-auto text-2xl bg-purple-500/20 text-purple-400 border border-purple-500/30 shadow-inner';
    if (iconEl) iconEl.className = options.icon || 'fa-solid fa-shield-halved';
    if (okBtn) okBtn.className = 'flex-1 py-3 rounded-xl grad text-white font-black text-xs shadow-lg hover:opacity-90 active:scale-95 transition-all';
  }

  if (okBtn) okBtn.textContent = options.confirmText || 'Confirmar';
  if (cancelBtn) cancelBtn.textContent = options.cancelText || 'Cancelar';

  const closeFn = () => modal.classList.add('hidden');
  cancelBtn.onclick = closeFn;

  okBtn.onclick = () => {
    closeFn();
    if (typeof onConfirm === 'function') onConfirm();
  };

  modal.classList.remove('hidden');
}

function showAppPrompt(title, message, defaultValue, onSubmit) {
  const modal = document.getElementById('app-prompt-modal');
  if (!modal) return;

  document.getElementById('app-prompt-title').textContent = title || 'Inserir Valor';
  document.getElementById('app-prompt-message').textContent = message || '';
  const inp = document.getElementById('app-prompt-input');
  if (inp) {
    inp.value = defaultValue || '';
    setTimeout(() => inp.focus(), 100);
  }

  const okBtn = document.getElementById('app-prompt-ok-btn');
  const cancelBtn = document.getElementById('app-prompt-cancel-btn');

  const closeFn = () => modal.classList.add('hidden');
  cancelBtn.onclick = closeFn;

  okBtn.onclick = () => {
    const val = inp ? inp.value : '';
    closeFn();
    if (typeof onSubmit === 'function') onSubmit(val);
  };

  modal.classList.remove('hidden');
}
