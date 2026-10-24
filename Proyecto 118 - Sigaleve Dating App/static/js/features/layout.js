/**
 * Layout: largura da sidebar (redimensionável), modo de foto de perfil e lightbox.
 */
'use strict';

// ═══════════════════════════════════════════════════════════════════
// REDIMENSIONAMENTO DA SIDEBAR LATERAL + VISUALIZAÇÃO COMPLETA DA FOTO
// ═══════════════════════════════════════════════════════════════════
const SIDEBAR_MIN_W = 280;
const SIDEBAR_MAX_W = 620;
const SIDEBAR_DEFAULT_W = 380;
const SIDEBAR_PRESETS = [300, 380, 480, 560];

function applySidebarWidth(widthPx, save = true) {
  const sidebar = document.getElementById('desktop-sidebar') || document.querySelector('.desktop-sidebar');
  if (!sidebar) return;
  const clamped = Math.max(SIDEBAR_MIN_W, Math.min(SIDEBAR_MAX_W, Math.round(Number(widthPx) || SIDEBAR_DEFAULT_W)));
  sidebar.style.setProperty('--sidebar-w', clamped + 'px');
  sidebar.style.width = clamped + 'px';

  // Ajustar grelha de matches conforme largura da barra (2, 3 ou 4 colunas)
  const grid = document.getElementById('desktop-matches-grid');
  if (grid) {
    grid.classList.remove('grid-cols-2', 'grid-cols-3', 'grid-cols-4');
    if (clamped < 325) grid.classList.add('grid-cols-2');
    else if (clamped >= 470) grid.classList.add('grid-cols-4');
    else grid.classList.add('grid-cols-3');
  }

  if (save) {
    try { localStorage.setItem('sigaleve_sidebar_width', String(clamped)); } catch (e) {}
  }
}

function getCurrentSidebarWidth() {
  const sidebar = document.getElementById('desktop-sidebar') || document.querySelector('.desktop-sidebar');
  if (!sidebar) return SIDEBAR_DEFAULT_W;
  const saved = parseInt(localStorage.getItem('sigaleve_sidebar_width') || '', 10);
  if (!isNaN(saved)) return saved;
  return sidebar.getBoundingClientRect().width || SIDEBAR_DEFAULT_W;
}

function adjustSidebarWidth(deltaPx) {
  const next = getCurrentSidebarWidth() + deltaPx;
  applySidebarWidth(next, true);
}

function cycleSidebarWidthPreset() {
  const current = getCurrentSidebarWidth();
  const nextPreset = SIDEBAR_PRESETS.find(w => w > current + 15) || SIDEBAR_PRESETS[0];
  applySidebarWidth(nextPreset, true);
  if (typeof showAppToast === 'function') {
    showAppToast(`Largura da barra: ${nextPreset}px`, 'info');
  }
}

function toggleMyPhotoFitMode(forceMode) {
  const img = document.getElementById('my-photo');
  const lbl = document.getElementById('lbl-photo-fit-mode');
  if (!img) return;
  const isCurrentlyContain = img.classList.contains('object-contain');
  const nextMode = forceMode || (isCurrentlyContain ? 'cover' : 'contain');

  if (nextMode === 'cover') {
    img.classList.remove('object-contain');
    img.classList.add('object-cover');
    if (lbl) lbl.textContent = 'Preencher';
  } else {
    img.classList.remove('object-cover');
    img.classList.add('object-contain');
    if (lbl) lbl.textContent = 'Foto Completa';
  }
  try { localStorage.setItem('sigaleve_photo_fit_mode', nextMode); } catch (e) {}
}

function openMyPhotoLightbox(customSrc) {
  const topPhoto = document.getElementById('top-bar-my-photo');
  const myPhoto = document.getElementById('my-photo');
  const src = customSrc || (myPhoto && myPhoto.src) || (topPhoto && topPhoto.src) || '';
  if (!src) return;

  let modal = document.getElementById('modal-my-photo-lightbox');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'modal-my-photo-lightbox';
    modal.className = 'fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in';
    modal.innerHTML = `
      <div class="relative max-w-2xl w-full rounded-3xl overflow-hidden border border-purple-500/30 shadow-2xl flex flex-col" style="background:var(--card);max-height:90vh">
        <div class="flex items-center justify-between px-5 py-3.5 border-b" style="border-color:var(--bdr)">
          <div class="flex items-center gap-2.5">
            <i class="fa-solid fa-image text-purple-400"></i>
            <span class="text-sm font-black text-white">A Minha Foto de Perfil (Vista Completa)</span>
          </div>
          <div class="flex items-center gap-2">
            <button type="button" onclick="closeMyPhotoLightbox(); promptPhotoUrl();" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-purple-600/20 text-purple-300 border border-purple-500/40 hover:bg-purple-600/30 transition-all flex items-center gap-1.5">
              <i class="fa-solid fa-camera"></i> Alterar Foto
            </button>
            <button type="button" onclick="closeMyPhotoLightbox()" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-all">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>
        </div>
        <div class="p-4 flex-1 flex items-center justify-center bg-zinc-950 overflow-auto">
          <img id="lightbox-my-photo-img" src="" alt="Foto de Perfil" class="max-h-[72vh] w-auto max-w-full object-contain rounded-2xl shadow-xl"/>
        </div>
      </div>
    `;
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeMyPhotoLightbox();
    });
    document.body.appendChild(modal);
  }
  const imgEl = document.getElementById('lightbox-my-photo-img');
  if (imgEl) imgEl.src = src;
  modal.classList.remove('hidden');
}

function closeMyPhotoLightbox() {
  const modal = document.getElementById('modal-my-photo-lightbox');
  if (modal) modal.classList.add('hidden');
}

(function initSidebarResizerAndPhotoPrefs() {
  const setup = () => {
    // 1. Restaurar largura guardada da sidebar
    try {
      const savedW = parseInt(localStorage.getItem('sigaleve_sidebar_width') || '', 10);
      if (!isNaN(savedW)) applySidebarWidth(savedW, false);
      const savedFit = localStorage.getItem('sigaleve_photo_fit_mode');
      if (savedFit === 'cover' || savedFit === 'contain') toggleMyPhotoFitMode(savedFit);
    } catch (e) {}

    // 2. Ativar arrasto (drag) no divisor lateral
    const resizer = document.getElementById('sidebar-resizer');
    const sidebar = document.getElementById('desktop-sidebar');
    if (!resizer || !sidebar) return;

    let dragging = false;

    resizer.addEventListener('mousedown', (e) => {
      e.preventDefault();
      dragging = true;
      sidebar.classList.add('is-resizing');
      document.body.style.cursor = 'col-resize';
    });

    window.addEventListener('mousemove', (e) => {
      if (!dragging) return;
      const rect = sidebar.getBoundingClientRect();
      const newWidth = e.clientX - rect.left;
      applySidebarWidth(newWidth, false);
    });

    window.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      sidebar.classList.remove('is-resizing');
      document.body.style.cursor = '';
      const finalW = sidebar.getBoundingClientRect().width;
      applySidebarWidth(finalW, true);
    });

    // Duplo clique no divisor restaura largura padrão (380px)
    resizer.addEventListener('dblclick', () => {
      applySidebarWidth(SIDEBAR_DEFAULT_W, true);
      if (typeof showAppToast === 'function') {
        showAppToast('Largura da barra restaurada (380px)', 'info');
      }
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
})();
