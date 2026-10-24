/**
 * Terminar sessão, perfil do utilizador e edição de perfil.
 */
'use strict';

async function doLogout() {
  await fetch('/api/v1/auth/logout', { method: 'POST' });
  localStorage.removeItem('sigaleve_remember_me');
  STATE.currentUser = null;
  closeDrawer();
  const appMax = document.querySelector('.app-max');
  if (appMax) appMax.classList.add('is-auth');
  const scrApp = document.getElementById('screen-app');
  if (scrApp) {
    scrApp.style.display = 'none';
    scrApp.classList.add('hidden');
  }
  const scrAuth = document.getElementById('screen-auth');
  if (scrAuth) {
    scrAuth.classList.remove('hidden');
    scrAuth.style.display = 'flex';
  }
}

// ═══════════════════════════════════════════════════
// CARREGAMENTO E ATUALIZAÇÃO DO PERFIL DO USUÁRIO
// ═══════════════════════════════════════════════════
function updateProfileUI(u) {
  if (!u) return;
  const name = u.display_name || 'Utilizador';
  const age = u.age || 25;
  const city = u.city || 'Lisboa, Portugal';
  const bio = u.bio || 'Sem biografia ainda.';
  const phone = u.phone ? formatPhoneNumber(u.phone) : 'Nenhum telemóvel registado.';

  const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  setTxt('prof-display-name', name);
  setTxt('prof-age', age);
  setTxt('prof-city', city);
  setTxt('prof-bio', bio);
  setTxt('prof-phone', phone);
  // Sincronizar con el panel de Ajustes estilo Tinder
  const drawerEmail = document.getElementById('drawer-user-email');
  if (drawerEmail && u.email) {
    const em = u.email;
    const shortEm = em.length > 20 ? em.substring(0, 15) + '...' : em;
    drawerEmail.innerHTML = `${shortEm} <i class="fa-solid fa-check text-xs text-emerald-500 ml-1" title="Verificado y protegido"></i>`;
  }
  const drawerPhone = document.getElementById('drawer-user-phone');
  if (drawerPhone && u.phone) {
    drawerPhone.innerHTML = `${formatPhoneNumber(u.phone)} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;
  }
  const drawerLocation = document.getElementById('drawer-pref-location');
  if (drawerLocation && u.city) {
    drawerLocation.innerHTML = `${u.city} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;
  }
  
  const topPhoto = document.getElementById('top-bar-my-photo');
  if (topPhoto && u.photo) topPhoto.src = u.photo;
  const topName = document.getElementById('top-bar-my-name');
  if (topName) topName.textContent = name.split(' ')[0];

  const mobTopPhoto = document.getElementById('mobile-top-bar-my-photo');
  if (mobTopPhoto && u.photo) mobTopPhoto.src = u.photo;
  const mobTopName = document.getElementById('mobile-top-bar-my-name');
  if (mobTopName) mobTopName.textContent = name.split(' ')[0];

  if (u.photo) {
    const myPhotoEl = document.getElementById('my-photo');
    if (myPhotoEl) myPhotoEl.src = u.photo;
    const myPhotoBgBlur = document.getElementById('my-photo-bg-blur');
    if (myPhotoBgBlur) myPhotoBgBlur.src = u.photo;
    const matchPhotoEl = document.getElementById('match-my-photo');
    if (matchPhotoEl) matchPhotoEl.src = u.photo;
    const editPreview = document.getElementById('edit-preview-img');
    if (editPreview) editPreview.src = u.photo;
    const editPhotoInp = document.getElementById('edit-photo');
    if (editPhotoInp) editPhotoInp.value = u.photo;
    try {
      if (u.email) localStorage.setItem('sigaleve_user_photo_' + u.email, u.photo);
      localStorage.setItem('sigaleve_last_photo', u.photo);
    } catch(e){}
  }

  // Atualizar selo de saúde / condição
  const healthBadge = document.getElementById('prof-health-badge');
  if (healthBadge) {
    const diag = u.diagnosis || 'HPV';
    if (diag === 'OUTRO' && u.custom_diagnosis) {
      healthBadge.textContent = u.custom_diagnosis;
    } else {
      healthBadge.textContent = diag;
    }
  }

  if (u.relationship_goal) {
    const goalEl = document.getElementById('prof-relationship-goal');
    if (goalEl) goalEl.textContent = u.relationship_goal;
  }

    const tagsBox = document.getElementById('prof-interests-tags');
  if (tagsBox) {
    tagsBox.innerHTML = '';
    const interests = u.interests || ['Viagens', 'Música', 'Café'];
    interests.forEach(it => {
      const sp = document.createElement('span');
      sp.className = 'px-3 py-1 rounded-full text-xs font-semibold border';
      sp.style.borderColor = 'var(--bdr)';
      sp.textContent = it;
      tagsBox.appendChild(sp);
    });
  }

  // ── Atualizar Secção 'Mais Sobre Mim' (Apenas se configurada pelo utilizador) ──
  const moreAboutContainer = document.getElementById('prof-more-about-container');
  const itemZodiac = document.getElementById('prof-item-zodiac');
  const itemEdu = document.getElementById('prof-item-education');
  const itemHeight = document.getElementById('prof-item-height');
  const itemLife = document.getElementById('prof-item-lifestyle');

  const valZodiac = document.getElementById('prof-val-zodiac');
  const valEdu = document.getElementById('prof-val-education');
  const valHeight = document.getElementById('prof-val-height');
  const valLife = document.getElementById('prof-val-lifestyle');

  let hasAnyConfigured = false;

  if (u.zodiac && u.zodiac.trim() && valZodiac && itemZodiac) {
    valZodiac.textContent = u.zodiac.trim();
    itemZodiac.classList.remove('hidden');
    hasAnyConfigured = true;
  } else if (itemZodiac) {
    itemZodiac.classList.add('hidden');
  }

  if (u.education && u.education.trim() && valEdu && itemEdu) {
    valEdu.textContent = u.education.trim();
    itemEdu.classList.remove('hidden');
    hasAnyConfigured = true;
  } else if (itemEdu) {
    itemEdu.classList.add('hidden');
  }

  if (u.height && u.height.trim() && valHeight && itemHeight) {
    valHeight.textContent = u.height.trim();
    itemHeight.classList.remove('hidden');
    hasAnyConfigured = true;
  } else if (itemHeight) {
    itemHeight.classList.add('hidden');
  }

  if (u.lifestyle && u.lifestyle.trim() && valLife && itemLife) {
    valLife.textContent = u.lifestyle.trim();
    itemLife.classList.remove('hidden');
    hasAnyConfigured = true;
  } else if (itemLife) {
    itemLife.classList.add('hidden');
  }

  // ── Prompt de Conversa ("Pergunta-me sobre...") ──
  const promptContainer = document.getElementById('prof-prompt-container');
  const promptTextEl = document.getElementById('prof-prompt-text');
  if (promptContainer && promptTextEl) {
    if (u.profile_prompt && u.profile_prompt.trim()) {
      promptTextEl.textContent = u.profile_prompt.trim();
      promptContainer.classList.remove('hidden');
    } else {
      promptContainer.classList.add('hidden');
    }
  }

  if (moreAboutContainer) {
    if (hasAnyConfigured) {
      moreAboutContainer.classList.remove('hidden');
    } else {
      moreAboutContainer.classList.add('hidden');
    }
  }

  // Atualizar estado da subscrição (Perfil limpo em 0 ou ativo)
  renderSubscriptionSettingsUI();

  // Sincronizar álbum privado exclusivo do utilizador
  if (typeof loadMyPrivateVault === 'function') {
    loadMyPrivateVault();
  }
}

// ═══════════════════════════════════════════════════
// LISTA EXTENSA DE 22+ INTERESSES GLOBAIS
// ═══════════════════════════════════════════════════
const EDIT_PROFILE_INTERESTS_LIST = [
  '✈️ Viagens', '☕ Café', '🎵 Música', '🎬 Cinema', '🎨 Arte', 
  '🏋️ Fitness', '🏖️ Praia', '🍷 Gastronomia', '📚 Leitura', '🐶 Animais', 
  '🧘 Yoga', '🌿 Natureza', '🎮 Jogos', '🚴 Ciclismo', '📸 Fotografia', 
  '🏕️ Campismo', '💃 Dança', '🍕 Cozinhar', '💻 Tecnologia', '🧗 Escalada', 
  '🏄 Surf', '👗 Moda', '🎭 Teatro', '🎤 Concertos'
];

let editCameraStream = null;

function renderEditInterestsChips(selectedInterests = []) {
  const container = document.getElementById('edit-interests-chips-container');
  if (!container) return;
  container.innerHTML = '';

  const cleanSelected = (selectedInterests || []).map(s => s.toLowerCase().trim());

  EDIT_PROFILE_INTERESTS_LIST.forEach(item => {
    // Normalizar texto para checar se está selecionado
    const itemClean = item.replace(/^[^\w\s]+\s*/, '').toLowerCase().trim();
    const isSelected = cleanSelected.some(sel => sel.includes(itemClean) || itemClean.includes(sel));

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer select-none ${isSelected ? 'selected grad text-white border-transparent shadow' : 'border-zinc-800 text-zinc-300 bg-zinc-950/60 hover:bg-zinc-800'}`;
    btn.textContent = item;
    btn.onclick = function() {
      const currentSelected = container.querySelectorAll('.selected');
      const alertBox = document.getElementById('edit-interests-alert');
      
      if (btn.classList.contains('selected')) {
        btn.classList.remove('selected', 'grad', 'text-white', 'border-transparent', 'shadow');
        btn.classList.add('border-zinc-800', 'text-zinc-300', 'bg-zinc-950/60');
        if (alertBox) alertBox.classList.add('hidden');
      } else {
        if (currentSelected.length >= 5) {
          if (alertBox) alertBox.classList.remove('hidden');
          return;
        }
        if (alertBox) alertBox.classList.add('hidden');
        btn.classList.add('selected', 'grad', 'text-white', 'border-transparent', 'shadow');
        btn.classList.remove('border-zinc-800', 'text-zinc-300', 'bg-zinc-950/60');
      }
      updateEditInterestsCount();
    };

    container.appendChild(btn);
  });

  updateEditInterestsCount();
}

function updateEditInterestsCount() {
  const countBadge = document.getElementById('edit-interests-count');
  const container = document.getElementById('edit-interests-chips-container');
  if (!countBadge || !container) return;
  const count = container.querySelectorAll('.selected').length;
  countBadge.textContent = `${count} / 5`;
}

function handleEditFileSelect(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;

  // preview imediato; upload em arquivo e grava a URL do servidor
  const url = URL.createObjectURL(file);
  document.getElementById('edit-preview-img').src = url;
  uploadPhotoFile(file).then(serverUrl => {
    if (serverUrl) {
      document.getElementById('edit-photo').value = serverUrl;
      document.getElementById('edit-preview-img').src = serverUrl;
    }
    URL.revokeObjectURL(url);
  });
}

async function startEditCameraCapture() {
  const container = document.getElementById('edit-camera-container');
  const video = document.getElementById('edit-video');
  if (!container || !video) return;

  try {
    stopEditCameraCapture();
    editCameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 720 }, height: { ideal: 720 } },
      audio: false
    });
    video.srcObject = editCameraStream;
    container.classList.remove('hidden');
  } catch (err) {
    showAppToast('Não foi possível aceder à câmara. Por favor verifica as permissões ou usa o botão "Da Galeria".', 'error');
  }
}

function stopEditCameraCapture() {
  if (editCameraStream) {
    editCameraStream.getTracks().forEach(t => t.stop());
    editCameraStream = null;
  }
  const container = document.getElementById('edit-camera-container');
  if (container) container.classList.add('hidden');
}

function takeEditSnapshot() {
  const video = document.getElementById('edit-video');
  const canvas = document.getElementById('edit-canvas');
  if (!video || !canvas) return;

  const w = video.videoWidth || 480;
  const h = video.videoHeight || 480;
  canvas.width = w;
  canvas.height = h;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, w, h);

  const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
  document.getElementById('edit-preview-img').src = dataUrl;
  // câmera: upload em arquivo e grava a URL do servidor
  fetch('/api/v1/photo/upload', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ photo_data_url: dataUrl })
  }).then(r => r.json()).then(d => {
    if (d.success && d.url) {
      document.getElementById('edit-photo').value = d.url;
      document.getElementById('edit-preview-img').src = d.url;
    } else if (d.error) {
      showAppToast && showAppToast(d.error, 'error');
    }
  }).catch(() => {});

  stopEditCameraCapture();
}

function handleEditEtsChange(val) {
  const otherContainer = document.getElementById('edit-other-ets-container');
  const otherInput = document.getElementById('edit-custom-ets');
  if (!otherContainer) return;

  if (val === 'OUTRO') {
    otherContainer.classList.remove('hidden');
    if (otherInput) {
      otherInput.focus();
      updateCustomEtsCharCount(otherInput);
    }
  } else {
    otherContainer.classList.add('hidden');
  }
}

function updateCustomEtsCharCount(input) {
  const countEl = document.getElementById('edit-custom-ets-charcount');
  if (!countEl || !input) return;
  countEl.textContent = `${input.value.length} / 50`;
}

function toggleProfileEditModal(open) {
  const modal = document.getElementById('modal-edit-profile');
  if (!modal) return;

  if (open) {
    const u = STATE.currentUser || {};
    document.getElementById('edit-name').value = u.display_name || '';
    document.getElementById('edit-city').value = u.city || 'Faro, Portugal';
    let existingPhone = (u.phone || '').trim();
    const prefixEl = document.getElementById('edit-phone-prefix');
    const phoneEl = document.getElementById('edit-phone');
    if (existingPhone.startsWith('+')) {
      const parts = existingPhone.split(' ');
      const possiblePrefix = parts[0];
      if (prefixEl && Array.from(prefixEl.options).some(o => o.value === possiblePrefix)) {
        prefixEl.value = possiblePrefix;
        existingPhone = parts.slice(1).join(' ');
      }
    }
    if (phoneEl) phoneEl.value = existingPhone;
    
    // Foto
    const photoUrl = u.photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=85';
    document.getElementById('edit-photo').value = photoUrl;
    document.getElementById('edit-preview-img').src = photoUrl;
    
    // Biografia: Começa estritamente vazia/em branco caso o usuário ainda não a tenha escrito
    document.getElementById('edit-bio').value = u.bio || '';
    
    if (u.relationship_goal) {
      document.getElementById('edit-goal').value = u.relationship_goal;
    }
    if (document.getElementById('edit-profile-prompt')) {
      document.getElementById('edit-profile-prompt').value = u.profile_prompt || '';
      updatePromptCharCount();
    }
    if (document.getElementById('edit-zodiac')) {
      document.getElementById('edit-zodiac').value = u.zodiac || '';
    }
    if (document.getElementById('edit-education')) {
      document.getElementById('edit-education').value = u.education || '';
    }
    if (document.getElementById('edit-height')) {
      document.getElementById('edit-height').value = u.height || '';
    }
    if (document.getElementById('edit-lifestyle')) {
      document.getElementById('edit-lifestyle').value = u.lifestyle || '';
    }

    // Interesses: Renderizar chips e marcar selecionados
    renderEditInterestsChips(u.interests || []);

    // Condição de Saúde / ETS
    const userDiag = u.diagnosis || 'HPV';
    const radios = document.getElementsByName('edit_ets');
    let matched = false;
    for (const r of radios) {
      if (r.value === userDiag) {
        r.checked = true;
        matched = true;
        break;
      }
    }
    if (!matched) {
      const rOther = Array.from(radios).find(r => r.value === 'OUTRO');
      if (rOther) rOther.checked = true;
      handleEditEtsChange('OUTRO');
      const customInput = document.getElementById('edit-custom-ets');
      if (customInput) {
        customInput.value = (u.custom_diagnosis || userDiag || '').substring(0, 50);
        updateCustomEtsCharCount(customInput);
      }
    } else {
      handleEditEtsChange(userDiag);
    }

    modal.classList.remove('hidden');
  } else {
    stopEditCameraCapture();
    modal.classList.add('hidden');
  }
}

function promptPhotoUrl() {
  toggleProfileEditModal(true);
}

// ── Prompt de conversa ("Pergunta-me sobre...") ──
function handlePromptPresetChange(sel) {
  const ta = document.getElementById('edit-profile-prompt');
  if (!ta || !sel) return;
  if (sel.value && sel.value !== 'OUTRO') {
    ta.value = sel.value;
    updatePromptCharCount();
  } else if (sel.value === 'OUTRO') {
    ta.value = '';
    ta.focus();
  }
}
function updatePromptCharCount() {
  const ta = document.getElementById('edit-profile-prompt');
  const counter = document.getElementById('edit-prompt-char-count');
  if (ta && counter) counter.textContent = `${ta.value.length} / 200`;
}

async function handleProfileSave(e) {
  e.preventDefault();
  const name = document.getElementById('edit-name').value.trim();
  const city = document.getElementById('edit-city').value.trim();
  const phoneRaw = document.getElementById('edit-phone').value.trim();
  const phonePrefix = document.getElementById('edit-phone-prefix') ? document.getElementById('edit-phone-prefix').value : '';
  const phone = phoneRaw ? (phoneRaw.startsWith('+') ? phoneRaw : `${phonePrefix} ${phoneRaw}`) : '';
  const photo = document.getElementById('edit-photo').value.trim();
  const bio = document.getElementById('edit-bio').value.trim();
  const goal = document.getElementById('edit-goal').value;

  // Interesses dos chips (máximo 5)
  const chipsContainer = document.getElementById('edit-interests-chips-container');
  const selectedChips = chipsContainer ? chipsContainer.querySelectorAll('.selected') : [];
  const interests = Array.from(selectedChips).map(btn => btn.textContent.replace(/^[^\w\s]+\s*/, '').trim()).slice(0, 5);

  // ETS única
  const radios = document.getElementsByName('edit_ets');
  let chosenDiag = 'HPV';
  for (const r of radios) {
    if (r.checked) {
      chosenDiag = r.value;
      break;
    }
  }

  let customDiag = '';
  if (chosenDiag === 'OUTRO') {
    const customInp = document.getElementById('edit-custom-ets');
    customDiag = customInp ? customInp.value.trim().substring(0, 50) : '';
  }

  const saveBtn = document.getElementById('btn-save-profile-modal');
  if (saveBtn) {
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin mr-1"></i> A guardar...';
  }

  const zodiac = document.getElementById('edit-zodiac') ? document.getElementById('edit-zodiac').value.trim() : '';
  const education = document.getElementById('edit-education') ? document.getElementById('edit-education').value.trim() : '';
  const height = document.getElementById('edit-height') ? document.getElementById('edit-height').value.trim() : '';
  const lifestyle = document.getElementById('edit-lifestyle') ? document.getElementById('edit-lifestyle').value.trim() : '';
  const profilePrompt = document.getElementById('edit-profile-prompt') ? document.getElementById('edit-profile-prompt').value.trim().substring(0, 200) : '';

  await saveProfileData({
    display_name: name,
    city: city,
    phone: phone,
    photo: photo || (STATE.currentUser && STATE.currentUser.photo),
    bio: bio,
    relationship_goal: goal,
    interests: interests,
    diagnosis: chosenDiag,
    custom_diagnosis: customDiag,
    zodiac: zodiac,
    education: education,
    height: height,
    lifestyle: lifestyle,
    profile_prompt: profilePrompt
  });

  if (saveBtn) {
    saveBtn.disabled = false;
    saveBtn.innerHTML = 'Guardar Alterações';
  }

  const goalEl = document.getElementById('prof-relationship-goal');
  if (goalEl) goalEl.textContent = goal;

  toggleProfileEditModal(false);
}

async function saveProfileData(fields) {
  try {
    const payload = Object.assign({
      email: STATE.currentUser && STATE.currentUser.email,
      user_id: STATE.currentUser && STATE.currentUser.id,
      is_profile_configured: true
    }, fields);
    const res = await fetch('/api/v1/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.success) {
      STATE.currentUser = Object.assign({}, STATE.currentUser, data.user, { is_profile_configured: true });
      updateProfileUI(STATE.currentUser);
      return true;
    }
    return false;
  } catch (err) {
    console.error('Erro ao guardar perfil:', err);
    return false;
  }
}
