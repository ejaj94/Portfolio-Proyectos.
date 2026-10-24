/**
 * Onboarding de nova conta: passos, foto/câmara, interesses e finalização.
 */
'use strict';

// ═══════════════════════════════════════════════════
// ONBOARDING WIZARD (PASSO A PASSO PARA NOVA CONTA)
// ═══════════════════════════════════════════════════
let currentOnboardStep = 1;
const totalOnboardSteps = 5;

function openOnboardingModal() {
  currentOnboardStep = 1;
  const modal = document.getElementById('modal-onboarding');
  if (!modal) return;

  const u = STATE.currentUser || {};
  if (u.photo) {
    document.getElementById('onboard-preview-img').src = u.photo;
    document.getElementById('onboard-photo-url').value = u.photo;
  }
  if (u.city) {
    document.getElementById('onboard-city').value = u.city;
  }
  if (u.bio && u.bio !== 'Sem biografia ainda.') {
    document.getElementById('onboard-bio').value = u.bio;
  }
  if (u.zodiac && document.getElementById('onboard-zodiac')) {
    document.getElementById('onboard-zodiac').value = u.zodiac;
  }
  if (u.education && document.getElementById('onboard-education')) {
    document.getElementById('onboard-education').value = u.education;
  }
  if (u.height && document.getElementById('onboard-height')) {
    document.getElementById('onboard-height').value = u.height;
  }
  if (u.lifestyle && document.getElementById('onboard-lifestyle')) {
    document.getElementById('onboard-lifestyle').value = u.lifestyle;
  }

  // Pre-seleccionar intereses del usuario o resetear
  const container = document.getElementById('onboard-interests-chips');
  if (container) {
    const userInterests = (u.interests || []).map(s => s.toLowerCase().trim());
    const chips = container.querySelectorAll('.onboard-chip');
    let selCount = 0;
    chips.forEach(btn => {
      const cleanText = btn.textContent.replace(/^[\uD800-\uDBFF\uDC00-\uDFFF\u2000-\u3300\s]+/, '').trim().toLowerCase();
      if (userInterests.includes(cleanText) && selCount < 5) {
        btn.classList.add('selected');
        btn.style.background = 'linear-gradient(135deg,#9333ea,#ec4899)';
        btn.style.color = '#fff';
        btn.style.borderColor = 'transparent';
        selCount++;
      } else {
        btn.classList.remove('selected');
        btn.style.background = '';
        btn.style.color = '';
        btn.style.borderColor = '';
      }
    });
  }
  updateOnboardInterestsCounter();

  updateOnboardStepUI();
  modal.classList.remove('hidden');
}

function closeOnboardingModal() {
  const modal = document.getElementById('modal-onboarding');
  if (modal) modal.classList.add('hidden');
}

function updateOnboardStepUI() {
  for (let s = 1; s <= totalOnboardSteps; s++) {
    const el = document.getElementById('onboard-step-' + s);
    if (el) {
      if (s === currentOnboardStep) el.classList.remove('hidden');
      else el.classList.add('hidden');
    }
  }

  const indicator = document.getElementById('onboarding-step-indicator');
  if (indicator) indicator.textContent = currentOnboardStep + ' / ' + totalOnboardSteps;

  const progress = document.getElementById('onboarding-progress-bar');
  if (progress) progress.style.width = (currentOnboardStep / totalOnboardSteps * 100) + '%';

  const subtitle = document.getElementById('onboarding-subtitle');
  if (subtitle) {
    const stepTitles = [
      T('onboardStep1Title') || 'Passo 1 de 5: Foto de Apresentação',
      T('onboardStep2Title') || 'Passo 2 de 5: Gostos & Atividades',
      T('onboardStep3Title') || 'Passo 3 de 5: Condição de Saúde & Comunidade ETS',
      T('onboardStep4Title') || 'Passo 4 de 5: Acerca de Mim & Metas',
      T('onboardStep5Title') || 'Passo 5 de 5: Mais Sobre Mim (Signo, Educação, Altura, Estilo de Vida)'
    ];
    subtitle.textContent = stepTitles[currentOnboardStep - 1] || '';
  }

  const prevBtn = document.getElementById('btn-onboard-prev');
  if (prevBtn) {
    prevBtn.innerHTML = '<i class="fa-solid fa-arrow-left mr-1"></i> ' + (T('btnPrevStep') || 'Anterior');
    if (currentOnboardStep > 1) prevBtn.classList.remove('hidden');
    else prevBtn.classList.add('hidden');
  }

  const nextBtn = document.getElementById('btn-onboard-next');
  if (nextBtn) {
    if (currentOnboardStep === totalOnboardSteps) {
      nextBtn.innerHTML = '<i class="fa-solid fa-check mr-1.5"></i> ' + (T('btnFinishProfile') || 'Concluir Perfil');
    } else {
      nextBtn.innerHTML = '<span>' + (T('btnNextStep') || 'Siguiente') + '</span> <i class="fa-solid fa-arrow-right ml-1"></i>';
    }
  }
}

function prevOnboardStep() {
  if (currentOnboardStep > 1) {
    currentOnboardStep--;
    updateOnboardStepUI();
  }
}

async function nextOnboardStep() {
  // Validación Paso 2: Intereses
  if (currentOnboardStep === 2) {
    const container = document.getElementById('onboard-interests-chips');
    const selected = container ? container.querySelectorAll('.onboard-chip.selected') : [];
    const alertEl = document.getElementById('interests-limit-alert');
    if (selected.length === 0) {
      if (alertEl) {
        alertEl.classList.remove('hidden');
        alertEl.textContent = T('min1InterestAlert') || 'Por favor seleciona pelo menos 1 interesse (máximo 5).';
      }
      return;
    }
    if (selected.length > 5) {
      if (alertEl) {
        alertEl.classList.remove('hidden');
        alertEl.textContent = T('max5InterestsAlert') || 'Apenas podes selecionar no máximo 5 interesses.';
      }
      return;
    }
  }

  if (currentOnboardStep < totalOnboardSteps) {
    currentOnboardStep++;
    updateOnboardStepUI();
  } else {
    await finishOnboarding();
  }
}

function updateOnboardPhotoPreview(url) {
  const img = document.getElementById('onboard-preview-img');
  if (img && url) {
    img.src = url;
  }
}

function setOnboardPhotoPreset(url) {
  const inp = document.getElementById('onboard-photo-url');
  if (inp) inp.value = url;
  updateOnboardPhotoPreview(url);
}

// ── Upload da Galeria / Ficheiro Local ──
// 🖼️ Fotos agora vão para o servidor como ARQUIVO (multipart), não base64 no JSON.
// helper global usado por onboarding, edição de perfil e cofre privado
async function uploadPhotoFile(file) {
  if (!file) return null;
  const fd = new FormData();
  fd.append('photo', file);
  try {
    const res = await fetch('/api/v1/photo/upload', { method: 'POST', body: fd });
    const data = await res.json();
    if (res.ok && data.success && data.url) return data.url;
    showAppToast && showAppToast(data.error || 'Falha ao enviar foto.', 'error');
    return null;
  } catch (err) {
    console.error('uploadPhotoFile:', err);
    showAppToast && showAppToast('Falha ao enviar foto.', 'error');
    return null;
  }
}

function handleOnboardFileSelect(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  updateOnboardPhotoPreview(url);
  uploadPhotoFile(file).then(serverUrl => {
    if (serverUrl) {
      const inp = document.getElementById('onboard-photo-url');
      if (inp) inp.value = serverUrl;
      updateOnboardPhotoPreview(serverUrl);
    }
    URL.revokeObjectURL(url);
  });
}

// ── Captura da Câmara em Tempo Real ──
let cameraStream = null;

async function startCameraCapture() {
  const container = document.getElementById('onboard-camera-container');
  const video = document.getElementById('onboard-video');
  if (!container || !video) return;

  try {
    stopCameraCapture(); // fechar anterior se houver
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 720 }, height: { ideal: 720 } },
      audio: false
    });
    video.srcObject = cameraStream;
    container.classList.remove('hidden');
  } catch (err) {
    showAppToast('Não foi possível aceder à câmara. Por favor, verifica as permissões do teu navegador ou escolhe uma foto da galeria.', 'error');
  }
}

function stopCameraCapture() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  const container = document.getElementById('onboard-camera-container');
  if (container) container.classList.add('hidden');
}

function takeSnapshot() {
  const video = document.getElementById('onboard-video');
  const canvas = document.getElementById('onboard-canvas');
  if (!video || !canvas) return;

  const w = video.videoWidth || 480;
  const h = video.videoHeight || 480;
  canvas.width = w;
  canvas.height = h;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, w, h);

  const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
  updateOnboardPhotoPreview(dataUrl);
  // câmera: envia como data_url ao servidor e grava a URL do arquivo
  fetch('/api/v1/photo/upload', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ photo_data_url: dataUrl })
  }).then(r => r.json()).then(d => {
    if (d.success && d.url) {
      const inp = document.getElementById('onboard-photo-url');
      if (inp) inp.value = d.url;
      updateOnboardPhotoPreview(d.url);
    } else if (d.error) {
      showAppToast && showAppToast(d.error, 'error');
    }
  }).catch(() => {});

  stopCameraCapture();
}

function updateOnboardInterestsCounter() {
  const container = document.getElementById('onboard-interests-chips');
  const countBadge = document.getElementById('interests-count-badge');
  const alertEl = document.getElementById('interests-limit-alert');
  if (!container || !countBadge) return;

  const selectedCount = container.querySelectorAll('.onboard-chip.selected').length;
  countBadge.textContent = `${selectedCount} / 5`;

  if (selectedCount >= 5) {
    countBadge.classList.remove('text-purple-400');
    countBadge.classList.add('text-pink-500');
  } else {
    countBadge.classList.remove('text-pink-500');
    countBadge.classList.add('text-purple-400');
    if (alertEl) alertEl.classList.add('hidden');
  }
}

function toggleOnboardChip(btn) {
  const container = document.getElementById('onboard-interests-chips');
  const alertEl = document.getElementById('interests-limit-alert');
  const currentlySelected = container ? container.querySelectorAll('.onboard-chip.selected') : [];

  if (btn.classList.contains('selected')) {
    // Deseleccionar
    btn.classList.remove('selected');
    btn.style.background = '';
    btn.style.color = '';
    btn.style.borderColor = '';
    if (alertEl) alertEl.classList.add('hidden');
  } else {
    // Validar límite máximo de 5
    if (currentlySelected.length >= 5) {
      if (alertEl) {
        alertEl.classList.remove('hidden');
        alertEl.textContent = T('max5InterestsAlert') || 'Apenas podes selecionar no máximo 5 interesses.';
      }
      return;
    }
    // Seleccionar
    btn.classList.add('selected');
    btn.style.background = 'linear-gradient(135deg,#9333ea,#ec4899)';
    btn.style.color = '#fff';
    btn.style.borderColor = 'transparent';
    if (alertEl) alertEl.classList.add('hidden');
  }

  updateOnboardInterestsCounter();
}

function handleEtsChange(val) {
  const container = document.getElementById('onboard-other-ets-container');
  if (!container) return;
  if (val === 'OUTRO') {
    container.classList.remove('hidden');
    document.getElementById('onboard-custom-ets').focus();
  } else {
    container.classList.add('hidden');
  }
}

async function finishOnboarding() {
  const nextBtn = document.getElementById('btn-onboard-next');
  const prevBtn = document.getElementById('btn-onboard-prev');
  if (nextBtn) {
    nextBtn.disabled = true;
    nextBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A guardar perfil...';
  }
  if (prevBtn) prevBtn.disabled = true;

  // 1. Foto
  const photoInp = document.getElementById('onboard-photo-url');
  const photo = (photoInp ? photoInp.value.trim() : '') ||
    (STATE.currentUser && STATE.currentUser.photo) ||
    'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=85';

  // 2. Interesses
  const selectedChips = Array.from(document.querySelectorAll('#onboard-interests-chips .onboard-chip.selected'))
    .map(el => el.textContent.trim().replace(/^[\p{Extended_Pictographic}\u{FE0F}\u{200D}\u{FE0E}\s]+/u, '').trim())
    .filter(Boolean);
  const customInterestsEl = document.getElementById('onboard-custom-interests');
  const customInterests = customInterestsEl ? customInterestsEl.value.split(',').map(s => s.trim()).filter(Boolean) : [];
  let interests = [...selectedChips, ...customInterests];
  if (interests.length === 0) {
    interests = ['Viagens', 'Música', 'Café'];
  }

  // 3. Condição de Saúde / ETS
  const checkedRadio = document.querySelector('input[name="onboard_ets"]:checked');
  let diagnosis = checkedRadio ? checkedRadio.value : 'HPV';
  let customDiagnosis = '';
  if (diagnosis === 'OUTRO') {
    const customEtsInp = document.getElementById('onboard-custom-ets');
    customDiagnosis = customEtsInp ? customEtsInp.value.trim() : '';
    if (!customDiagnosis) customDiagnosis = 'Outra Condição';
  }

  // 4. Bio & Metas
  const bioInp = document.getElementById('onboard-bio');
  const bio = (bioInp ? bioInp.value.trim() : '') || 'Olá! Estou no Sigaleve para conexões reais, respeitosas e sem preconceito.';
  const goalEl2 = document.getElementById('onboard-goal');
  const goal = goalEl2 ? goalEl2.value : '';
  const cityInp = document.getElementById('onboard-city');
  const city = (cityInp ? cityInp.value.trim() : '') || 'Lisboa, Portugal';

  // 5. Mais Sobre Mim (Signo, Educação, Estatura, Estilo de Vida)
  const zodiac = document.getElementById('onboard-zodiac') ? document.getElementById('onboard-zodiac').value.trim() : '';
  const education = document.getElementById('onboard-education') ? document.getElementById('onboard-education').value.trim() : '';
  const height = document.getElementById('onboard-height') ? document.getElementById('onboard-height').value.trim() : '';
  const lifestyle = document.getElementById('onboard-lifestyle') ? document.getElementById('onboard-lifestyle').value.trim() : '';

  try {
    await saveProfileData({
      photo,
      interests,
      diagnosis,
      custom_diagnosis: customDiagnosis,
      bio,
      relationship_goal: goal,
      city,
      zodiac,
      education,
      height,
      lifestyle
    });

    // Garantizar actualización instantánea del perfil en UI
    if (STATE.currentUser) {
      STATE.currentUser.photo = photo;
      STATE.currentUser.bio = bio;
      STATE.currentUser.city = city;
      STATE.currentUser.interests = interests;
      STATE.currentUser.relationship_goal = goal;
      STATE.currentUser.zodiac = zodiac;
      STATE.currentUser.education = education;
      STATE.currentUser.height = height;
      STATE.currentUser.lifestyle = lifestyle;
      STATE.currentUser.is_profile_configured = true;
      updateProfileUI(STATE.currentUser);
    }

    const goalEl = document.getElementById('prof-relationship-goal');
    if (goalEl) goalEl.textContent = goal;
  } catch (err) {
    console.error('Erro ao concluir onboarding:', err);
  } finally {
    // GARANTIA: o modal fecha e os botões reabilitam mesmo se algo falhar acima
    closeOnboardingModal();
    if (nextBtn) {
      nextBtn.disabled = false;
      nextBtn.innerHTML = '<span>Seguinte</span> <i class="fa-solid fa-arrow-right ml-1"></i>';
    }
    if (prevBtn) prevBtn.disabled = false;
    showSection('discover');
  }
}
