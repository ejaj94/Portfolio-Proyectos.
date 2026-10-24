/**
 * Verificação por selfie e atualização do método de pagamento.
 */
// ══════════════════════════════════════════════════════════════════════════════
// VERIFICAÇÃO POR SELFIE (selo ✔ Verificado)
// ══════════════════════════════════════════════════════════════════════════════
let _selfieStream = null;

function openSelfieVerifyModal() {
  // Já verificado? Mostra sucesso direto
  fetch('/api/v1/verify/status', { credentials: 'include' })
    .then(r => r.json())
    .then(data => {
      if (data.verified) { showSelfieState('success'); }
      else { startSelfieCapture(); }
      document.getElementById('modal-selfie-verify').classList.remove('hidden');
    })
    .catch(() => {
      showAppToast('Erro de rede. Tenta novamente.', 'error');
    });
}

function closeSelfieVerifyModal() {
  document.getElementById('modal-selfie-verify').classList.add('hidden');
  stopSelfieCamera();
}

function showSelfieState(state) {
  ['capture', 'loading', 'error', 'success'].forEach(s => {
    const el = document.getElementById('selfie-verify-state-' + s);
    if (el) el.classList.toggle('hidden', s !== state);
  });
  if (state !== 'capture') stopSelfieCamera();
}

async function startSelfieCapture() {
  showSelfieState('capture');
  try {
    _selfieStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 720 }, height: { ideal: 960 } },
      audio: false
    });
    const video = document.getElementById('selfie-video');
    video.srcObject = _selfieStream;
    await video.play();
  } catch (err) {
    // Sem câmara (permissão negada / desktop sem câmara) — upload de ficheiro
    showSelfieState('error');
    document.getElementById('selfie-verify-error-text').textContent =
      'Não foi possível aceder à câmara. Verifica as permissões do navegador ou usa um dispositivo com câmara.';
  }
}

function stopSelfieCamera() {
  if (_selfieStream) {
    _selfieStream.getTracks().forEach(t => t.stop());
    _selfieStream = null;
  }
}

function captureAndVerifySelfie() {
  const video = document.getElementById('selfie-video');
  if (!video || !video.videoWidth) {
    showSelfieState('error');
    document.getElementById('selfie-verify-error-text').textContent = 'A câmara ainda não está pronta. Aguarda um segundo e tenta de novo.';
    return;
  }
  // Captura em JPEG (qualidade 0.9, resolução da câmara)
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  // Espelhar horizontalmente para parecer um espelho (selfie natural)
  ctx.translate(canvas.width, 0);
  ctx.scale(-1, 1);
  ctx.drawImage(video, 0, 0);
  const dataUrl = canvas.toDataURL('image/jpeg', 0.9);

  showSelfieState('loading');
  document.getElementById('selfie-verify-loading-text').textContent = 'A analisar a tua selfie…';

  fetch('/api/v1/verify/selfie', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ selfie: dataUrl })
  })
    .then(r => r.json().then(j => ({ ok: r.ok, status: r.status, body: j })))
    .then(({ ok, status, body }) => {
      if (ok && body.success) {
        showSelfieState('success');
        const badge = document.getElementById('drawer-selfie-verify-text');
        if (badge) {
          badge.textContent = 'Verificado ✔';
          badge.className = 'text-xs text-emerald-400 font-bold';
        }
      } else if (status === 503) {
        showSelfieState('error');
        document.getElementById('selfie-verify-error-text').textContent = body.error || 'Verificação temporariamente indisponível. Tenta mais tarde.';
      } else {
        showSelfieState('error');
        document.getElementById('selfie-verify-error-text').textContent = body.message || body.error || 'Não foi possível verificar. Tenta novamente.';
      }
    })
    .catch(() => {
      showSelfieState('error');
      document.getElementById('selfie-verify-error-text').textContent = 'Erro de rede ao enviar a selfie. Verifica a tua ligação e tenta de novo.';
    });
}

function promptUpdatePaymentMethod() {
  openProductSubscription('plus');
}
