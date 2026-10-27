/**
 * Momentos & Sentimentos: feed da comunidade, humor, média (câmara/galeria), reações, edição e eliminação.
 */
'use strict';

// Interceptar showSection para suportar 'moments'
const _originalShowSection = window.showSection;
window.showSection = function(sec) {
  _originalShowSection(sec);
  const topTitle = document.getElementById('top-title');
  if (sec === 'moments') {
    if (topTitle) topTitle.textContent = 'Momentos & Sentimentos';
    loadMomentsFeed();
  }
};

// =========================================================================
// REQUISITO 3: MOMENTOS & SENTIMENTOS (FEED COMUNITÁRIO) 💭
// =========================================================================
let currentSelectedMood = '☕ A relaxar';

function selectMomentMood(elem, moodText, emoji) {
  document.querySelectorAll('#moment-mood-chips .mood-chip').forEach(c => {
    c.classList.remove('active', 'bg-purple-500/20', 'text-purple-300', 'border-purple-500/50');
    c.classList.add('bg-zinc-900', 'border-zinc-800', 'text-zinc-300');
  });
  elem.classList.remove('bg-zinc-900', 'border-zinc-800', 'text-zinc-300');
  elem.classList.add('active', 'bg-purple-500/20', 'text-purple-300', 'border-purple-500/50');
  currentSelectedMood = moodText;
  const moodInp = document.getElementById('new-moment-mood');
  if (moodInp) moodInp.value = moodText;
  const emojiInp = document.getElementById('new-moment-emoji');
  if (emojiInp && emoji) emojiInp.value = emoji;
}

function handleMomentTextInput(el) {
  const countEl = document.getElementById('moment-char-count');
  if (countEl) {
    countEl.textContent = `${el.value.length} / 1000`;
  }
  const alertEl = document.getElementById('moment-security-alert');
  if (alertEl) {
    const check = validateContentPrivacyClient(el.value);
    if (!check.ok) {
      const msg = document.getElementById('moment-security-msg');
      if (msg) msg.textContent = check.reason;
      alertEl.classList.remove('hidden');
    } else {
      alertEl.classList.add('hidden');
    }
  }
}

function openMomentMediaPicker() {
  const modal = document.getElementById('modal-moment-media-picker');
  if (modal) modal.classList.remove('hidden');
}

function closeMomentMediaPicker() {
  const modal = document.getElementById('modal-moment-media-picker');
  if (modal) modal.classList.add('hidden');
}

function triggerMomentCapture(sourceType) {
  closeMomentMediaPicker();
  if (sourceType === 'camera') {
    openMomentLiveCamera();
  } else if (sourceType === 'gallery') {
    const input = document.getElementById('moment-file-gallery');
    if (input) {
      input.value = '';
      input.click();
    }
  } else if (sourceType === 'url') {
    promptMomentPhotoUrl();
  }
}

// ── CÂMARA EM DIRETO PARA MOMENTOS (FOTO & VÍDEO) ──
let momentCameraStream = null;
let momentMediaRecorder = null;
let momentRecordedChunks = [];
let momentRecordingTimerInterval = null;
let momentRecordingStartTime = 0;

async function openMomentLiveCamera() {
  const modal = document.getElementById('modal-moment-live-camera');
  const video = document.getElementById('moment-live-video');
  if (!modal || !video) return;

  try {
    closeMomentLiveCamera(); // limpar stream anterior se existisse
    modal.classList.remove('hidden');

    momentCameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: true
    }).catch(async () => {
      // Se falhar áudio (ex: microfone negado ou sem permissão), tenta apenas vídeo
      return await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false
      });
    });

    video.srcObject = momentCameraStream;
    try { await video.play(); } catch(e) {}
  } catch (err) {
    // Fallback: Se o dispositivo não permitir getUserMedia direto no browser, abre o capturador nativo do sistema
    const nativeCam = document.getElementById('moment-file-camera');
    if (nativeCam) {
      nativeCam.value = '';
      nativeCam.click();
    } else {
      showAppToast('Não foi possível aceder à câmara. Por favor verifica as permissões do teu navegador.', 'error');
    }
    if (modal) modal.classList.add('hidden');
  }
}

function closeMomentLiveCamera() {
  if (momentMediaRecorder && momentMediaRecorder.state !== 'inactive') {
    try { momentMediaRecorder.stop(); } catch(e) {}
  }
  if (momentRecordingTimerInterval) {
    clearInterval(momentRecordingTimerInterval);
    momentRecordingTimerInterval = null;
  }
  if (momentCameraStream) {
    momentCameraStream.getTracks().forEach(t => t.stop());
    momentCameraStream = null;
  }

  const modal = document.getElementById('modal-moment-live-camera');
  if (modal) modal.classList.add('hidden');

  // Resetar estado de gravação
  const recIndicator = document.getElementById('moment-live-camera-recording-indicator');
  const timerBadge = document.getElementById('moment-recording-timer');
  const btnRecText = document.getElementById('btn-moment-record-text');
  const btnRecIcon = document.getElementById('btn-moment-record-icon');
  const btnSnap = document.getElementById('btn-moment-snap-photo');

  if (recIndicator) recIndicator.classList.add('hidden');
  if (timerBadge) timerBadge.classList.add('hidden');
  if (btnRecText) btnRecText.textContent = 'Gravar Vídeo';
  if (btnRecIcon) {
    btnRecIcon.className = 'fa-solid fa-circle text-red-500 text-sm';
  }
  if (btnSnap) btnSnap.classList.remove('hidden');
}

function snapMomentLivePhoto() {
  const video = document.getElementById('moment-live-video');
  const canvas = document.getElementById('moment-live-canvas');
  if (!video || !canvas) return;

  const w = video.videoWidth || 640;
  const h = video.videoHeight || 480;
  canvas.width = w;
  canvas.height = h;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, w, h);

  const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
  setMomentMedia(dataUrl, 'photo');
  closeMomentLiveCamera();
}

function toggleMomentVideoRecording() {
  if (!momentCameraStream) return;

  const btnRecText = document.getElementById('btn-moment-record-text');
  const btnRecIcon = document.getElementById('btn-moment-record-icon');
  const recIndicator = document.getElementById('moment-live-camera-recording-indicator');
  const timerBadge = document.getElementById('moment-recording-timer');
  const timerSeconds = document.getElementById('moment-recording-seconds');
  const btnSnap = document.getElementById('btn-moment-snap-photo');

  if (momentMediaRecorder && momentMediaRecorder.state === 'recording') {
    // Parar gravação
    momentMediaRecorder.stop();
    if (momentRecordingTimerInterval) {
      clearInterval(momentRecordingTimerInterval);
      momentRecordingTimerInterval = null;
    }
    if (recIndicator) recIndicator.classList.add('hidden');
    if (timerBadge) timerBadge.classList.add('hidden');
    if (btnRecText) btnRecText.textContent = 'A processar...';
    return;
  }

  // Iniciar gravação de vídeo
  momentRecordedChunks = [];
  try {
    let options = { mimeType: 'video/webm;codecs=vp9,opus' };
    if (!MediaRecorder.isTypeSupported(options.mimeType)) {
      options = { mimeType: 'video/webm;codecs=vp8,opus' };
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        options = { mimeType: 'video/webm' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
          options = { mimeType: 'video/mp4' };
          if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            options = {};
          }
        }
      }
    }

    momentMediaRecorder = new MediaRecorder(momentCameraStream, options);

    momentMediaRecorder.ondataavailable = function(e) {
      if (e.data && e.data.size > 0) {
        momentRecordedChunks.push(e.data);
      }
    };

    momentMediaRecorder.onstop = function() {
      // Usar MIME limpo sem codecs complexos na declaração do Blob para compatibilidade com Safari/Chrome video
      let rawMime = momentMediaRecorder.mimeType || 'video/webm';
      let cleanMime = rawMime.split(';')[0] || 'video/webm';
      const blob = new Blob(momentRecordedChunks, { type: cleanMime });
      const reader = new FileReader();
      reader.onload = function(evt) {
        let videoDataUrl = evt.target.result;
        // Garantir prefixo limpo data:video/webm;base64,...
        if (videoDataUrl && videoDataUrl.includes(';codecs=')) {
          const parts = videoDataUrl.split(';base64,');
          if (parts.length === 2) {
            videoDataUrl = `${cleanMime};base64,${parts[1]}`;
          }
        }
        setMomentMedia(videoDataUrl, 'video');
        closeMomentLiveCamera();
      };
      reader.readAsDataURL(blob);
    };

    momentMediaRecorder.start(100);
    momentRecordingStartTime = Date.now();

    if (recIndicator) recIndicator.classList.remove('hidden');
    if (timerBadge) timerBadge.classList.remove('hidden');
    if (btnSnap) btnSnap.classList.add('hidden'); // Ocultar botão de foto enquanto grava vídeo
    if (btnRecText) btnRecText.textContent = 'Parar Gravação';
    if (btnRecIcon) {
      btnRecIcon.className = 'fa-solid fa-square text-red-500 text-sm animate-pulse';
    }

    momentRecordingTimerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - momentRecordingStartTime) / 1000);
      const hrs = Math.floor(elapsed / 3600);
      const mins = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
      const secs = String(elapsed % 60).padStart(2, '0');
      if (timerSeconds) {
        timerSeconds.textContent = hrs > 0 ? `${hrs}:${mins}:${secs}` : `${mins}:${secs}`;
      }
      // O utilizador grava todo o tempo que desejar (15 seg, 5 min, 1 hora, etc.) sem corte forçado
    }, 1000);

  } catch (err) {
    console.error('Erro ao iniciar MediaRecorder:', err);
    showAppToast('Não foi possível gravar vídeo neste dispositivo/navegador.', 'error');
  }
}

function handleMomentFileSelected(inputEl, forceType) {
  const file = inputEl.files && inputEl.files[0];
  if (!file) return;

  const isVideo = file.type.startsWith('video/') || forceType === 'video';
  const reader = new FileReader();

  reader.onload = function(e) {
    const dataUrl = e.target.result;
    setMomentMedia(dataUrl, isVideo ? 'video' : 'photo');
  };

  reader.readAsDataURL(file);
}

// ── MULTI-MÍDIA: até 5 fotos/vídeos num só momento ──
const MOMENT_MEDIA_MAX = 5;
let momentMediaList = []; // [{url, type}]

function handleMomentFilesSelected(inputEl, forceType) {
  const files = inputEl.files;
  if (!files || !files.length) return;
  const restantes = MOMENT_MEDIA_MAX - momentMediaList.length;
  if (restantes <= 0) {
    showAppToast(`Máximo de ${MOMENT_MEDIA_MAX} fotos/vídeos por momento.`, 'warning');
    inputEl.value = '';
    return;
  }
  const selecionados = Array.from(files).slice(0, restantes);
  if (files.length > restantes) {
    showAppToast(`Só ${restantes} ${restantes === 1 ? 'mídia cabe' : 'mídias cabem'} — o resto foi ignorado.`, 'warning');
  }
  let pendentes = selecionados.length;
  selecionados.forEach(file => {
    const isVideo = file.type.startsWith('video/') || forceType === 'video';
    const reader = new FileReader();
    reader.onload = function(e) {
      momentMediaList.push({ url: e.target.result, type: isVideo ? 'video' : 'photo' });
      pendentes--;
      if (pendentes === 0) renderMomentMediaPreview();
    };
    reader.readAsDataURL(file);
  });
  inputEl.value = '';
}

function renderMomentMediaPreview() {
  const previewBox = document.getElementById('moment-media-preview-container');
  const photoInp = document.getElementById('new-moment-photo');
  const typeInp = document.getElementById('new-moment-media-type');
  const badge = document.getElementById('moment-photo-badge');
  if (!previewBox) return;
  if (!momentMediaList.length) { clearMomentMedia(); return; }
  const primeira = momentMediaList[0];
  if (photoInp) photoInp.value = primeira.url;
  if (typeInp) typeInp.value = primeira.type;
  previewBox.classList.remove('hidden');
  previewBox.classList.add('flex');
  // re-gerar os thumbs (imagem/vídeo por item + X de remover)
  const cont = document.getElementById('moment-preview-thumbs');
  if (cont) {
    cont.innerHTML = momentMediaList.map((m, i) => `
      <div class="relative w-9 h-9 rounded-xl overflow-hidden border border-purple-500/50 shadow flex-shrink-0">
        ${m.type === 'video' ? `<video src="${m.url}" class="w-full h-full object-cover" muted playsinline></video>` : `<img src="${m.url}" class="w-full h-full object-cover"/>`}
        <button type="button" onclick="removeMomentMediaItem(${i})" class="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-red-600 text-white flex items-center justify-center text-[9px] shadow hover:bg-red-500" title="Remover"><i class="fa-solid fa-xmark"></i></button>
        ${momentMediaList.length > 1 ? `<span class="absolute bottom-0 right-0 bg-purple-600 text-white text-[8px] font-bold px-1 rounded-tl">${i+1}</span>` : ''}
      </div>
    `).join('');
  }
  if (badge) {
    const nV = momentMediaList.filter(m => m.type === 'video').length;
    const nF = momentMediaList.length - nV;
    badge.textContent = momentMediaList.length === 1
      ? (nV ? 'Vídeo pronto ✓' : 'Foto pronta ✓')
      : `${nF ? nF + (nF === 1 ? ' foto' : ' fotos') : ''}${nF && nV ? ' + ' : ''}${nV ? nV + (nV === 1 ? ' vídeo' : ' vídeos') : ''} ✓`;
  }
}

function removeMomentMediaItem(i) {
  momentMediaList.splice(i, 1);
  renderMomentMediaPreview();
}

function setMomentMedia(mediaUrl, mediaType) {
  // Compat: câmara/vídeo ao vivo e URL manual chamam setMomentMedia (1 mídia).
  // Na nova UI multi-mídia, substitui a lista inteira por este item.
  momentMediaList = mediaUrl ? [{ url: mediaUrl, type: mediaType }] : [];
  renderMomentMediaPreview();
}

function clearMomentMedia() {
  const photoInp = document.getElementById('new-moment-photo');
  const typeInp = document.getElementById('new-moment-media-type');
  const previewBox = document.getElementById('moment-media-preview-container');
  const thumbs = document.getElementById('moment-preview-thumbs');

  momentMediaList = [];
  if (photoInp) photoInp.value = '';
  if (typeInp) typeInp.value = 'photo';
  if (thumbs) thumbs.innerHTML = '';
  if (previewBox) {
    previewBox.classList.remove('flex');
    previewBox.classList.add('hidden');
  }
}

function promptMomentPhotoUrl() {
  const current = document.getElementById('new-moment-photo')?.value || '';
  showAppPrompt(
    'Adicionar Link de Foto ou Vídeo',
    'Insere o link / URL direto da imagem ou vídeo:',
    current,
    (url) => {
      const cleanUrl = (url || '').trim();
      if (cleanUrl) {
        const isVideo = cleanUrl.match(/\.(mp4|webm|mov|ogg)($|\?)/i);
        setMomentMedia(cleanUrl, isVideo ? 'video' : 'photo');
      } else {
        clearMomentMedia();
      }
    }
  );
}

async function publishNewMoment() {
  const textEl = document.getElementById('new-moment-text');
  const photoEl = document.getElementById('new-moment-photo');
  const alertEl = document.getElementById('moment-security-alert');
  const alertMsg = document.getElementById('moment-security-msg');
  const submitBtn = document.getElementById('btn-publish-moment');

  if (alertEl) alertEl.classList.add('hidden');

  const text = (textEl ? textEl.value : '').trim();
  const photo = photoEl ? photoEl.value.trim() : '';

  if (!text && !photo) {
    if (alertMsg) alertMsg.textContent = 'Escreve algo sobre o teu momento ou partilha uma foto/vídeo.';
    if (alertEl) alertEl.classList.remove('hidden');
    return;
  }

  // Validação Anti-Doxxing
  if (text) {
    const privacyCheck = validateContentPrivacyClient(text);
    if (!privacyCheck.ok) {
      if (alertMsg) alertMsg.textContent = privacyCheck.reason;
      if (alertEl) alertEl.classList.remove('hidden');
      return;
    }
  }

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A partilhar...';
  }

  try {
    const myUid = STATE.currentUser ? String(STATE.currentUser.id) : (sessionStorage.getItem('sigaleve_user_id') || 'default_owner');
    const myName = STATE.currentUser ? (STATE.currentUser.name || 'Eu') : 'Eu';
    const myPhoto = STATE.currentUser ? (STATE.currentUser.photo || '') : '';

    const res = await fetch('/api/v1/moments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: myUid,
        user_name: myName,
        user_avatar: myPhoto,
        text: text,
        mood: currentSelectedMood,
        photo_url: photo,
        photos: momentMediaList.map(m => m.url)
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      if (alertMsg) alertMsg.textContent = data.error || 'Erro ao publicar momento.';
      if (alertEl) alertEl.classList.remove('hidden');
      return;
    }

    // Sucesso
    textEl.value = '';
    clearMomentMedia();
    const charCount = document.getElementById('moment-char-count');
    if (charCount) charCount.textContent = '0 / 1000';
    if (typeof showAppToast === 'function') {
      showAppToast('História temporária publicada com sucesso (24h para os teus matches)!', 'success');
    }
    
    // Recarregar feed
    await loadMomentsFeed();
  } catch (e) {
    console.error('Erro ao publicar momento:', e);
    if (alertMsg) alertMsg.textContent = 'Erro de ligação ao servidor.';
    if (alertEl) alertEl.classList.remove('hidden');
    if (typeof showAppToast === 'function') {
      showAppToast('Erro ao publicar momento.', 'error');
    }
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane text-[11px]"></i> <span>Publicar</span>';
    }
  }
}

// ── REAÇÕES EXPANDIDAS COM NOMES & MULTI-IDIOMA HD ─────────────────────────────
const MOMENT_REACTIONS = [
  { key: 'heart',  emoji: '❤️', labelKey: 'rx_like',   color: 'pink',   activeBg: 'bg-pink-500/25 text-pink-400 border-pink-500 shadow-sm' }
];

const REACTION_LABELS = {
  es: { rx_like: 'Like', rx_adoro: 'Adoro', rx_relaja: 'Me relaja', rx_divierte: 'Me divierte', rx_triste: 'Me entristece', rx_enoja: 'Me enoja' },
  pt: { rx_like: 'Gosto', rx_adoro: 'Adoro', rx_relaja: 'Relaxa-me', rx_divierte: 'Diverte-me', rx_triste: 'Entristece-me', rx_enoja: 'Irrita-me' },
  en: { rx_like: 'Like', rx_adoro: 'Love', rx_relaja: 'Relaxing', rx_divierte: 'Haha', rx_triste: 'Sad', rx_enoja: 'Angry' },
  fr: { rx_like: "J'aime", rx_adoro: "J'adore", rx_relaja: 'Apaisant', rx_divierte: 'Drôle', rx_triste: 'Triste', rx_enoja: 'En colère' },
  it: { rx_like: 'Mi piace', rx_adoro: 'Adoro', rx_relaja: 'Rilassante', rx_divierte: 'Divertente', rx_triste: 'Triste', rx_enoja: 'Arrabbiato' },
  de: { rx_like: 'Gefällt mir', rx_adoro: 'Liebe', rx_relaja: 'Entspannend', rx_divierte: 'Lustig', rx_triste: 'Traurig', rx_enoja: 'Wütend' }
};

function getReactionLabel(labelKey) {
  const lang = (window.LANG || localStorage.getItem('sigaleve_lang') || 'pt').substring(0, 2).toLowerCase();
  const dict = REACTION_LABELS[lang] || REACTION_LABELS['es'] || REACTION_LABELS['pt'];
  return (dict && dict[labelKey]) || (REACTION_LABELS['es'] && REACTION_LABELS['es'][labelKey]) || labelKey;
}

function renderReactionBar(m) {
  const rx = m.reactions || {};
  const activeRx = m.my_reaction;
  return MOMENT_REACTIONS.map(item => {
    const count = rx[item.key] || (item.key === 'heart' ? (rx['❤️'] || 0) : (item.key === 'hug' ? (rx['✨'] || 0) : 0));
    const isActive = activeRx === item.key;
    const activeClasses = isActive
      ? item.activeBg + ' font-bold scale-105 ring-1 ring-white/20'
      : 'bg-zinc-900/90 hover:bg-zinc-800 text-zinc-300 hover:text-white border-zinc-800 hover:border-zinc-700';
    const label = getReactionLabel(item.labelKey);

    return `
      <button type="button" id="btn-react-${item.key}-${m.id}" onclick="reactMoment('${m.id}', '${item.key}')" class="px-3 py-2 rounded-full border text-xs transition-all flex items-center gap-1.5 cursor-pointer select-none active:scale-95 ${activeClasses}">
        <span class="text-sm leading-none drop-shadow filter contrast-125">${item.emoji}</span>
        <span class="font-semibold">${label}</span>
        <span id="react-${item.key}-${m.id}" class="text-[10px] font-bold px-1 rounded-full ${count > 0 ? 'bg-white/10 text-zinc-200' : 'text-zinc-500'}">${count}</span>
      </button>
    `;
  }).join('');
}

async function loadMomentsFeed() {
  const container = document.getElementById('moments-feed-container');
  if (!container) return;

  try {
    const myUid = STATE.currentUser ? String(STATE.currentUser.id) : (sessionStorage.getItem('sigaleve_user_id') || 'default_owner');
    const matchIds = (typeof MATCHES_DATA !== 'undefined' && Array.isArray(MATCHES_DATA))
      ? MATCHES_DATA.map(m => encodeURIComponent(m.id || '')).filter(Boolean).join(',')
      : '';
    const res = await fetch(`/api/v1/moments?user_id=${encodeURIComponent(myUid)}&matches=${matchIds}`);
    const data = await res.json();
    const moments = data.moments || [];
    window.CURRENT_MOMENTS_FEED = moments;

    if (moments.length === 0) {
      container.innerHTML = `
        <div class="text-center py-12 px-4 rounded-3xl bg-zinc-900/50 border border-zinc-800/80">
          <i class="fa-regular fa-clock text-4xl text-purple-400/50 mb-3"></i>
          <h4 class="text-white font-bold text-sm">Sem histórias temporárias ativas</h4>
          <p class="text-xs text-zinc-400 mt-1">As histórias são efémeras (24h) e visíveis apenas entre pessoas que deram match mútuo!</p>
        </div>`;
      return;
    }

    let html = '';
    moments.forEach(m => {
      const isOwner = STATE.currentUser && String(STATE.currentUser.id) === String(m.user_id);
      const mediaSrc = m.photo_url || m.photo || '';
      const isVideo = mediaSrc.startsWith('data:video/') || mediaSrc.match(/\.(mp4|webm|mov|ogg)($|\?)/i);
      const remainingTime = m.remaining_time || '24h';

      html += `
        <div class="p-4 sm:p-5 rounded-3xl bg-zinc-900/90 border border-zinc-800 shadow-md">
          <div class="flex items-start justify-between gap-2 mb-3">
            <div class="flex items-center gap-3 min-w-0">
              <img src="${m.user_photo || m.author_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'}" class="w-10 h-10 rounded-full object-cover ring-2 ring-purple-500/40 flex-shrink-0"/>
              <div class="min-w-0">
                <h4 class="text-[15px] font-bold text-white flex items-center gap-1.5 flex-wrap">
                  ${esc(m.user_name || m.author_name || 'Utilizador')}
                  <span class="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded-full border border-purple-500/30">${esc(m.mood || '✨')}</span>
                </h4>
                <p class="text-[11px] text-zinc-400 flex items-center gap-1.5 mt-0.5">
                  <span id="moment-elapsed-${m.id}" data-created="${m.created_at || ''}">${esc(m.time || m.timestamp || 'Agora mesmo')}</span>
                  <span class="text-zinc-600">·</span>
                  <span class="text-zinc-400" title="História efémera visível apenas por 24h para matches">
                    <i class="fa-regular fa-clock text-[10px]"></i> <span id="moment-countdown-${m.id}" data-expires="${m.created_at ? Math.floor(Number(m.created_at)*1000 + 86400000) : 0}">${esc(remainingTime)}</span>
                  </span>
                </p>
              </div>
            </div>
            ${isOwner ? `
              <div class="flex items-center gap-1.5 flex-shrink-0">
                <button type="button" onclick="openEditMomentModal('${m.id}')" class="px-2.5 py-1.5 rounded-xl bg-zinc-800 hover:bg-purple-900/40 text-zinc-200 hover:text-purple-300 border border-zinc-700/80 hover:border-purple-500/50 transition-all text-xs font-semibold flex items-center gap-1 cursor-pointer">
                  <i class="fa-solid fa-pen text-[10px]"></i> <span class="hidden sm:inline">Editar</span><span class="sm:hidden"><i class="fa-solid fa-pen text-[10px]"></i></span>
                </button>
                <button type="button" onclick="confirmDeleteMoment('${m.id}')" class="px-2.5 py-1.5 rounded-xl bg-zinc-800 hover:bg-red-900/40 text-zinc-200 hover:text-red-400 border border-zinc-700/80 hover:border-red-500/50 transition-all text-xs font-semibold flex items-center gap-1 cursor-pointer">
                  <i class="fa-solid fa-trash-can text-[10px]"></i> <span class="hidden sm:inline">Eliminar</span><span class="sm:hidden"><i class="fa-solid fa-trash-can text-[10px]"></i></span>
                </button>
              </div>
            ` : ''}
          </div>

          ${m.text ? `<p class="text-[15px] sm:text-base text-zinc-50 leading-relaxed font-normal mb-1">${esc(m.text)}</p>` : ''}

          ${(mediaSrc && mediaSrc !== 'null' && mediaSrc !== 'undefined') || (m.photos && m.photos.length > 0) ? (() => {
            const listaFotos = (m.photos && m.photos.length ? m.photos : [mediaSrc]).filter(f => f && f !== 'null' && f !== 'undefined');
            if (listaFotos.length === 0) return '';
            const ehCarrossel = listaFotos.length > 1;
            const ehVideo = mediaSrc && (mediaSrc.startsWith('data:video/') || mediaSrc.match(/\.(mp4|webm|mov|ogg)($|\?)/i));
            return `
            <div class="relative mt-3 rounded-2xl overflow-hidden border border-zinc-800 bg-zinc-950 flex items-center justify-center p-1 sm:p-2 moment-media-box" style="max-height:85vh;width:100%;">
              ${ehCarrossel ? `
                <div class="w-full flex overflow-x-auto snap-x snap-mandatory gap-1 moment-carousel" data-moment="${m.id}" style="scrollbar-width:none;">
                  ${listaFotos.map((f, idx) => {
                    const fv = f.startsWith('data:video/') || f.match(/\.(mp4|webm|mov|ogg)($|\?)/i);
                    return fv ? `
                      <div class="snap-center flex-shrink-0 w-full flex items-center justify-center">
                        <video controls playsinline preload="metadata" class="w-auto h-auto rounded-xl bg-black" style="max-width:100%;max-height:75vh;object-fit:contain;" onerror="this.parentElement.style.display='none'">
                          <source src="${f}" type="${f.startsWith('data:video/mp4') ? 'video/mp4' : 'video/webm'}">
                          O teu navegador não suporta a reprodução deste vídeo.
                        </video>
                      </div>
                    ` : `
                      <div class="snap-center flex-shrink-0 w-full flex items-center justify-center">
                        <img src="${f}" class="w-auto h-auto rounded-xl block mx-auto" style="max-width:100%;max-height:75vh;width:auto;height:auto;object-fit:contain;" alt="História de ${esc(m.user_name || 'Utilizador')} (${idx+1}/${listaFotos.length})" onerror="this.closest('.moment-media-box') ? this.closest('.moment-media-box').style.display='none' : (this.style.display='none')"/>
                      </div>
                    `;
                  }).join('')}
                </div>
              ` : ehVideo ? `
                <video controls playsinline preload="metadata" class="w-auto h-auto rounded-xl bg-black" style="max-width:100%;max-height:75vh;object-fit:contain;" onerror="this.closest('.moment-media-box') ? this.closest('.moment-media-box').style.display='none' : (this.style.display='none')">
                  <source src="${mediaSrc}" type="${mediaSrc.startsWith('data:video/mp4') ? 'video/mp4' : 'video/webm'}">
                  O teu navegador não suporta a reprodução deste vídeo.
                </video>
              ` : `
                <img src="${mediaSrc}" class="w-auto h-auto rounded-xl block mx-auto" style="max-width:100%;max-height:75vh;width:auto;height:auto;object-fit:contain;" alt="História de ${esc(m.user_name || 'Utilizador')}" onerror="this.closest('.moment-media-box') ? this.closest('.moment-media-box').style.display='none' : (this.style.display='none')"/>
              `}
              ${ehCarrossel ? `<div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5" id="moment-dots-${m.id}">
                  ${listaFotos.map((_, i) => `<span class="w-1.5 h-1.5 rounded-full ${i === 0 ? 'bg-white' : 'bg-white/40'} transition-colors"></span>`).join('')}
                </div>
              ` : ''}
            </div>
          `;})() : ''}

          <!-- Ações: só like + comentários (pedido de simplificação) -->
          <div class="mt-3 pt-3 border-t border-zinc-800/80 flex items-center justify-between gap-2 text-xs">
            <div class="flex flex-wrap items-center gap-1.5" id="rx-bar-${m.id}">
              ${renderReactionBar(m)}
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <button type="button" onclick="openMomentComments('${m.id}')" class="px-3 py-2 rounded-full bg-zinc-800 text-zinc-200 hover:text-white hover:bg-purple-600 transition-all text-xs font-bold flex items-center gap-1.5 active:scale-95" title="Comentários">
                <i class="fa-regular fa-comment-dots text-xs"></i>
                <span id="moment-comments-count-${m.id}">${(m.comments || []).length}</span>
              </button>
            </div>
          </div>
        </div>
      `;
    });
    container.innerHTML = html;
    wireMomentCarousels();
    updateMomentCountdowns();
  } catch (e) {
    container.innerHTML = `<p class="text-xs text-red-400 text-center py-6">Erro ao carregar histórias temporárias.</p>`;
  }
}

// ── CARROSSEL: bolinhas sincronizadas com o scroll (wiring pós-render) ──
function wireMomentCarousels() {
  document.querySelectorAll('.moment-carousel').forEach(car => {
    if (car.dataset.wired) return;
    car.dataset.wired = '1';
    const dots = document.querySelectorAll('#moment-dots-' + car.dataset.moment + ' span');
    if (!dots.length) return;
    car.addEventListener('scroll', () => {
      const i = Math.max(0, Math.round(car.scrollLeft / car.clientWidth));
      dots.forEach((d, k) => {
        d.className = 'w-1.5 h-1.5 rounded-full transition-colors ' + (k === i ? 'bg-white' : 'bg-white/40');
      });
    }, { passive: true });
  });
}

// ══ FORMATADOR DE TEMPO DECORRIDO EM TEMPO REAL ═════════════════════════════
function formatMomentElapsedTime(createdAtSeconds) {
  if (!createdAtSeconds) return 'Agora mesmo';
  const nowSec = Math.floor(Date.now() / 1000);
  const elapsedSec = Math.max(0, nowSec - Number(createdAtSeconds));
  if (elapsedSec < 60) return 'Agora mesmo';
  const minutes = Math.floor(elapsedSec / 60);
  if (minutes < 60) return `Há ${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  if (hours >= 24) return 'Expirado';
  if (remainingMinutes === 0) return `Há ${hours}h`;
  return `Há ${hours}h ${remainingMinutes}m`;
}

// ══ CONTADOR 24H E TEMPO DECORRIDO AO VIVO NOS CARDS DE MOMENTS ══════════════
let _momentsCountdownTimer = null;

function updateMomentCountdowns() {
  const apply = () => {
    // 1. Atualizar contagem regressiva para expirar (24h)
    document.querySelectorAll('[id^="moment-countdown-"]').forEach(el => {
      const expires = Number(el.dataset.expires || 0);
      const msLeft = expires - Date.now();
      if (!expires || msLeft <= 0) {
        el.textContent = 'Expira já!';
        return;
      }
      const totalMin = Math.floor(msLeft / 60000);
      const h = Math.floor(totalMin / 60);
      const mnt = totalMin % 60;
      el.textContent = h > 0 ? `${h}h ${mnt}m` : `${mnt}m`;
    });

    // 2. Atualizar tempo decorrido desde a publicação em tempo real ("Há Xh Ym")
    document.querySelectorAll('[id^="moment-elapsed-"]').forEach(el => {
      const createdAt = el.dataset.created;
      if (createdAt) {
        el.textContent = formatMomentElapsedTime(createdAt);
      }
    });
  };
  apply();
  if (_momentsCountdownTimer) clearInterval(_momentsCountdownTimer);
  _momentsCountdownTimer = setInterval(apply, 60000);
}

async function reactMoment(momentId, reactionType) {
  try {
    const myUid = STATE.currentUser ? String(STATE.currentUser.id) : (sessionStorage.getItem('sigaleve_user_id') || 'default_owner');
    const res = await fetch('/api/v1/moments/react', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ moment_id: momentId, reaction: reactionType, user_id: myUid })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      const rx = data.reactions || {};
      const activeRx = data.user_reaction;

      // Atualiza os contadores e botões das 6 reações
      MOMENT_REACTIONS.forEach(item => {
        const count = rx[item.key] || 0;
        const countEl = document.getElementById(`react-${item.key}-${momentId}`);
        if (countEl) {
          countEl.textContent = count;
          countEl.className = `text-[10px] font-bold px-1 rounded-full ${count > 0 ? 'bg-white/10 text-zinc-200' : 'text-zinc-500'}`;
        }

        const btnEl = document.getElementById(`btn-react-${item.key}-${momentId}`);
        if (btnEl) {
          const isActive = activeRx === item.key;
          const activeClasses = isActive
            ? item.activeBg + ' font-bold scale-105 ring-1 ring-white/20'
            : 'bg-zinc-900/90 hover:bg-zinc-800 text-zinc-300 hover:text-white border-zinc-800 hover:border-zinc-700';
          btnEl.className = `px-2.5 py-1.5 rounded-full border text-[11px] transition-all flex items-center gap-1.5 cursor-pointer select-none active:scale-95 ${activeClasses}`;
        }
      });

      // Atualiza o momento em cache local para preservar o estado
      if (window.CURRENT_MOMENTS_FEED && Array.isArray(window.CURRENT_MOMENTS_FEED)) {
        const cached = window.CURRENT_MOMENTS_FEED.find(m => String(m.id) === String(momentId));
        if (cached) {
          cached.reactions = rx;
          cached.my_reaction = activeRx;
        }
      }
    }
  } catch(e) {
    console.error('reactMoment error:', e);
  }
}

function replyMomentInChat(targetUid, name, photo) {
  openChat({
    id: targetUid,
    name: name,
    photo: photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'
  });
  setTimeout(() => {
    const input = document.getElementById('chat-input');
    if (input) {
      input.value = `Vi o teu momento partilhado ("${name}")... Achei muito fixe! `;
      input.focus();
    }
  }, 300);
}

// Funções de Edição e Eliminação de Momentos
function openEditMomentModal(id, explicitText, explicitMood) {
  const modal = document.getElementById('modal-edit-moment');
  const idEl = document.getElementById('edit-moment-id');
  const textEl = document.getElementById('edit-moment-text');
  const moodEl = document.getElementById('edit-moment-mood');
  const alertEl = document.getElementById('edit-moment-alert');

  // Localiza o momento no feed carregado
  let targetMoment = null;
  if (window.CURRENT_MOMENTS_FEED && Array.isArray(window.CURRENT_MOMENTS_FEED)) {
    targetMoment = window.CURRENT_MOMENTS_FEED.find(m => String(m.id) === String(id));
  }

  const textToSet = explicitText !== undefined ? explicitText : (targetMoment ? (targetMoment.text || '') : '');
  const moodToSet = explicitMood !== undefined ? explicitMood : (targetMoment ? (targetMoment.mood || '✨') : '☕ A relaxar');

  if (idEl) idEl.value = id;
  if (textEl) {
    textEl.value = textToSet;
    handleEditMomentTextInput(textEl);
  }
  if (moodEl) moodEl.value = moodToSet;
  if (alertEl) alertEl.classList.add('hidden');
  if (modal) modal.classList.remove('hidden');
}

function closeEditMomentModal() {
  const modal = document.getElementById('modal-edit-moment');
  if (modal) modal.classList.add('hidden');
}

function handleEditMomentTextInput(el) {
  const counter = document.getElementById('edit-moment-char-count');
  if (counter) {
    const len = (el.value || '').length;
    counter.textContent = `${len} / 1000`;
    if (len > 950) {
      counter.className = 'text-[11px] font-medium text-amber-400';
    } else {
      counter.className = 'text-[11px] font-medium text-zinc-400';
    }
  }
}

async function submitEditMoment() {
  const id = document.getElementById('edit-moment-id').value;
  const text = (document.getElementById('edit-moment-text').value || '').trim();
  const mood = document.getElementById('edit-moment-mood').value || '✨';
  const alertEl = document.getElementById('edit-moment-alert');
  const alertMsg = document.getElementById('edit-moment-alert-msg');
  const btn = document.getElementById('btn-save-edit-moment');

  if (alertEl) alertEl.classList.add('hidden');

  if (text) {
    const privacyCheck = validateContentPrivacyClient(text);
    if (!privacyCheck.ok) {
      if (alertMsg) alertMsg.textContent = privacyCheck.reason;
      if (alertEl) alertEl.classList.remove('hidden');
      return;
    }
  }

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A guardar...';
  }

  try {
    const myUid = STATE.currentUser ? String(STATE.currentUser.id) : (sessionStorage.getItem('sigaleve_user_id') || 'default_owner');
    const res = await fetch(`/api/v1/moments/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: myUid, text, mood })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      if (alertMsg) alertMsg.textContent = data.error || 'Erro ao editar momento.';
      if (alertEl) alertEl.classList.remove('hidden');
      return;
    }
    closeEditMomentModal();
    await loadMomentsFeed();
  } catch (err) {
    if (alertMsg) alertMsg.textContent = 'Erro de ligação ao servidor.';
    if (alertEl) alertEl.classList.remove('hidden');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-check text-xs"></i> <span>Guardar Alterações</span>';
    }
  }
}

function confirmDeleteMoment(momentId) {
  const modal = document.getElementById('modal-confirm-delete-moment');
  const targetInp = document.getElementById('delete-moment-target-id');
  if (targetInp) targetInp.value = momentId;
  if (modal) modal.classList.remove('hidden');
}

function closeDeleteMomentModal() {
  const modal = document.getElementById('modal-confirm-delete-moment');
  if (modal) modal.classList.add('hidden');
}

async function executeDeleteMoment() {
  const targetInp = document.getElementById('delete-moment-target-id');
  const momentId = targetInp ? targetInp.value : null;
  if (!momentId) return;

  const btn = document.getElementById('btn-confirm-delete-moment-action');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A eliminar...';
  }

  try {
    const myUid = STATE.currentUser ? String(STATE.currentUser.id) : (sessionStorage.getItem('sigaleve_user_id') || 'default_owner');
    const res = await fetch(`/api/v1/moments/${momentId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: myUid })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      closeDeleteMomentModal();
      await loadMomentsFeed();
      showAppToast('Momento eliminado com sucesso.', 'info');
    } else {
      showAppToast(data.error || 'Erro ao eliminar momento.', 'error');
    }
  } catch (err) {
    showAppToast('Erro de rede ao tentar eliminar momento.', 'error');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = 'Eliminar';
    }
  }
}
