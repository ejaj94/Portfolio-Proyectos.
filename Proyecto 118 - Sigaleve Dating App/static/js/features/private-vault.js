/**
 * Cofre privado (álbum secreto): fotos, pedidos de acesso e partilha seletiva.
 */
'use strict';

// =========================================================================
// REQUISITO 1: COFRE DE FOTOS PRIVADAS (ÁLBUM PROTEGIDO) 🔒
// =========================================================================
let myVaultPhotos = [];

function openPrivateVaultModal() {
  const modal = document.getElementById('modal-manage-vault');
  if (modal) {
    modal.classList.remove('hidden');
    loadMyPrivateVault();
  }
}

function closePrivateVaultModal() {
  const modal = document.getElementById('modal-manage-vault');
  if (modal) modal.classList.add('hidden');
}

async function loadMyPrivateVault() {
  const myUid = STATE.currentUser ? STATE.currentUser.id : null;
  if (!myUid) return;

  try {
    const res = await fetch(`/api/v1/profile/private-album/${myUid}`);
    const data = await res.json();
    
    // Atualizar UI de resumo no modal e no perfil
    const myPhotos = data.photos || [];
    myVaultPhotos = myPhotos;

    const countModal = document.getElementById('vault-modal-count');
    if (countModal) countModal.textContent = myPhotos.length;

    // Renderizar fotos dentro do modal
    const grid = document.getElementById('vault-modal-photos-grid');
    if (grid) {
      if (myPhotos.length === 0) {
        grid.innerHTML = `<p class="col-span-3 text-center text-xs text-zinc-500 py-6">Ainda não tens fotos no teu cofre privado.</p>`;
      } else {
        grid.innerHTML = myPhotos.map(url => `
          <div class="relative group rounded-2xl overflow-hidden aspect-square border border-zinc-800 bg-zinc-900 shadow">
            <img src="${url}" class="w-full h-full object-cover"/>
            <button onclick="removePhotoFromMyVault('${url}')" class="absolute top-1.5 right-1.5 w-6 h-6 rounded-full bg-red-600/90 text-white flex items-center justify-center text-xs hover:bg-red-500 transition-all shadow-md">
              <i class="fa-solid fa-trash text-[10px]"></i>
            </button>
            <div class="absolute bottom-1 left-1.5 text-[9px] text-amber-300 font-bold flex items-center gap-1 drop-shadow">
              <i class="fa-solid fa-lock text-[8px]"></i> Privada
            </div>
          </div>
        `).join('');
      }
    }

    // Renderizar miniatura no cartão do meu perfil
    const profGrid = document.getElementById('prof-private-vault-grid');
    if (profGrid) {
      if (myPhotos.length === 0) {
        profGrid.innerHTML = `<p class="col-span-3 text-xs text-zinc-500 py-2">Sem fotos confidenciais adicionadas.</p>`;
      } else {
        profGrid.innerHTML = myPhotos.slice(0, 3).map(url => `
          <div class="aspect-square rounded-xl overflow-hidden border border-purple-500/30 relative">
            <img src="${url}" class="w-full h-full object-cover"/>
            <div class="absolute inset-0 bg-black/40 flex items-center justify-center text-amber-300 text-xs">
              <i class="fa-solid fa-lock"></i>
            </div>
          </div>
        `).join('');
      }
    }
  } catch(e) {
    console.error('Erro ao carregar cofre privado:', e);
  }
}

let vaultCameraStream = null;

function handleVaultFileSelect(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;

  // upload em arquivo: o cofre recebe /uploads/<nome> em vez de base64
  uploadPhotoFile(file).then(async serverUrl => {
    if (serverUrl) await savePhotoToVault(serverUrl);
    e.target.value = '';
  });
}

async function startVaultCameraCapture() {
  const container = document.getElementById('vault-camera-container');
  const video = document.getElementById('vault-video');
  if (!container || !video) return;

  try {
    stopVaultCameraCapture();
    vaultCameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 720 }, height: { ideal: 720 } },
      audio: false
    });
    video.srcObject = vaultCameraStream;
    container.classList.remove('hidden');
  } catch (err) {
    showAppToast('Não foi possível aceder à câmara. Por favor verifica as permissões ou usa o botão "Da Galeria".', 'error');
  }
}

function stopVaultCameraCapture() {
  if (vaultCameraStream) {
    vaultCameraStream.getTracks().forEach(t => t.stop());
    vaultCameraStream = null;
  }
  const container = document.getElementById('vault-camera-container');
  if (container) container.classList.add('hidden');
}

async function takeVaultSnapshot() {
  const video = document.getElementById('vault-video');
  const canvas = document.getElementById('vault-canvas');
  if (!video || !canvas) return;

  const w = video.videoWidth || 480;
  const h = video.videoHeight || 480;
  canvas.width = w;
  canvas.height = h;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, w, h);

  const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
  stopVaultCameraCapture();
  // câmera: upload em arquivo e salva a URL no cofre (sem base64 no JSON)
  try {
    const r = await fetch('/api/v1/photo/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ photo_data_url: dataUrl })
    });
    const d = await r.json();
    if (d.success && d.url) {
      await savePhotoToVault(d.url);
    } else if (d.error) {
      showAppToast && showAppToast(d.error, 'error');
    }
  } catch (err) {
    console.error('vault camera upload:', err);
  }
}

async function savePhotoToVault(photoData) {
  if (!photoData) return;
  const updated = [...myVaultPhotos, photoData];
  try {
    const res = await fetch('/api/v1/profile/private-album/manage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ photos: updated })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      if (typeof showAppToast === 'function') {
        showAppToast('Foto adicionada ao teu álbum privado!', 'success');
      }
      await loadMyPrivateVault();
    }
  } catch (e) {
    console.error('Erro ao guardar foto no cofre:', e);
  }
}

async function addPhotoToMyVault() {
  const input = document.getElementById('vault-add-url');
  if (!input) return;
  const url = input.value.trim();
  if (!url) return;

  await savePhotoToVault(url);
  input.value = '';
}

async function removePhotoFromMyVault(urlToRemove) {
  const updated = myVaultPhotos.filter(u => u !== urlToRemove);
  try {
    const res = await fetch('/api/v1/profile/private-album/manage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ photos: updated })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      await loadMyPrivateVault();
    }
  } catch(e) {}
}

async function respondVaultRequest(requesterUid, action) {
  try {
    await fetch('/api/v1/profile/private-album/respond', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ requester_id: requesterUid, action: action })
    });
    await loadMyPrivateVault();
  } catch(e) {}
}

// Carregar estado do cofre no Perfil Detalhado de outra pessoa
async function loadDetailProfileVault(targetUid) {
  const statusArea = document.getElementById('detail-vault-status-area');
  if (!statusArea) return;

  statusArea.innerHTML = `
    <div class="flex items-center justify-center py-3 text-xs text-zinc-400 gap-2">
      <i class="fa-solid fa-spinner fa-spin"></i> A verificar autorizações...
    </div>`;

  try {
    const res = await fetch(`/api/v1/profile/private-album/${targetUid}`);
    const data = await res.json();

    if (data.is_owner) {
      statusArea.innerHTML = `
        <div class="flex items-center justify-between text-xs">
          <span class="text-amber-400 font-semibold">Este é o teu cofre pessoal (${data.total_photos || 0} fotos)</span>
          <button onclick="openPrivateVaultModal()" class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500 hover:text-black font-bold transition-all">
            Gerir Cofre
          </button>
        </div>`;
      return;
    }

    if (data.access_granted) {
      // Tem permissão! Exibir fotos privadas
      const photos = data.photos || [];
      if (photos.length === 0) {
        statusArea.innerHTML = `
          <div class="text-xs text-emerald-400 flex items-center gap-1.5 font-medium">
            <i class="fa-solid fa-circle-check"></i> Autorizado! Este perfil não possui fotos confidenciais adicionais.
          </div>`;
      } else {
        statusArea.innerHTML = `
          <div>
            <div class="flex items-center gap-1.5 text-xs text-emerald-400 font-bold mb-2.5">
              <i class="fa-solid fa-lock-open"></i> Acesso Concedido (${photos.length} fotos desbloqueadas)
            </div>
            <div class="grid grid-cols-2 gap-2">
              ${photos.map(p => `
                <div class="aspect-square rounded-xl overflow-hidden border border-emerald-500/30">
                  <img src="${p}" class="w-full h-full object-cover"/>
                </div>
              `).join('')}
            </div>
          </div>`;
      }
    } else if (data.status === 'pending') {
      statusArea.innerHTML = `
        <div class="flex items-center justify-between text-xs">
          <span class="text-amber-400 flex items-center gap-1.5">
            <i class="fa-solid fa-clock"></i> Pedido de autorização enviado... Aguarda resposta.
          </span>
          <button disabled class="opacity-50 px-3 py-1 rounded-full bg-zinc-800 text-zinc-400 text-xs">
            Pendente
          </button>
        </div>`;
    } else {
      // Não tem acesso: mostrar botão de pedir autorização
      statusArea.innerHTML = `
        <div class="flex items-center justify-between gap-3 text-xs">
          <p class="text-zinc-300">As fotos confidenciais estão ocultas para proteção de privacidade.</p>
          <button onclick="requestTargetVaultAccess('${targetUid}')" class="flex-shrink-0 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-black font-extrabold text-xs shadow-md transition-all">
            <i class="fa-solid fa-key mr-1"></i> Pedir Acesso
          </button>
        </div>`;
    }
  } catch(e) {
    statusArea.innerHTML = `<p class="text-xs text-zinc-500">Informação de cofre indisponível.</p>`;
  }
}

async function requestTargetVaultAccess(targetUid) {
  try {
    const res = await fetch('/api/v1/profile/private-album/request', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_id: targetUid })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      loadDetailProfileVault(targetUid);
    }
  } catch(e) {}
}

// Estender openProfileDetail para carregar o cofre privado
const _originalOpenProfileDetail = window.openProfileDetail;
window.openProfileDetail = function(pid) {
  if (typeof isUserSubscribed === 'function' && !isUserSubscribed()) {
    showAppToast('👑 Ver o perfil completo de outros membros é um recurso exclusivo para membros com subscrição ativa.', 'warning');
    openSubscriptionModal('gold');
    return;
  }
  _originalOpenProfileDetail(pid);
  // 🔧 pid pode ser objeto (match) — o cofre espera o UID como string
  loadDetailProfileVault(typeof pid === 'object' && pid !== null ? (pid.id || pid.email) : pid);
};
