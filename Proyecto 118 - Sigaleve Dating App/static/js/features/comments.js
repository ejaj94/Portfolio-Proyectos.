/**
 * Comentários e gostos em fotos e em momentos.
 */
'use strict';

// =========================================================================
// REQUISITO 2: LIKES E COMENTÁRIOS COM FILTRO ANTI-DOXXING 🛡️
// =========================================================================
let currentPhotoCommentTarget = null;

function quickLikeCardPhoto(profileId) {
  const card = document.querySelector(`.s-card[data-pid="${profileId}"]`);
  let photoIdx = card ? parseInt(card.dataset.photoIdx || '0', 10) : 0;
  const photoId = `photo_${profileId}_${photoIdx}`;

  const heart = document.getElementById(`card-heart-${profileId}`);
  const counter = document.getElementById(`card-likes-count-${profileId}`);

  fetch('/api/v1/photos/like', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ photo_id: photoId })
  }).then(r => r.json()).then(data => {
    if (data.success) {
      if (counter) counter.textContent = data.likes_count;
      if (heart) {
        heart.classList.toggle('text-pink-500', data.liked);
        heart.classList.toggle('text-pink-400', !data.liked);
      }
    }
  }).catch(() => {});
}

function openCardPhotoComments(profileId, fallbackPhotoUrl, authorName) {
  const card = document.querySelector(`.s-card[data-pid="${profileId}"]`);
  let photoIdx = card ? parseInt(card.dataset.photoIdx || '0', 10) : 0;
  const p = STATE.profiles ? STATE.profiles.find(x => x.id === profileId) : null;
  const photos = (p && p.photos && p.photos.length) ? p.photos : [fallbackPhotoUrl];
  const photoUrl = photos[photoIdx] || fallbackPhotoUrl;
  const photoId = `photo_${profileId}_${photoIdx}`;

  currentPhotoCommentTarget = {
    profileId: profileId,
    photoId: photoId,
    photoUrl: photoUrl,
    authorName: authorName
  };

  const modal = document.getElementById('modal-photo-comments');
  if (!modal) return;

  const previewImg = document.getElementById('photo-comments-preview-img');
  if (previewImg) previewImg.src = photoUrl;
  const authorEl = document.getElementById('photo-comments-author');
  if (authorEl) authorEl.textContent = `Foto de ${authorName}`;
  const inputEl = document.getElementById('photo-comment-input');
  if (inputEl) inputEl.value = '';
  const alertEl = document.getElementById('photo-comment-security-alert');
  if (alertEl) alertEl.classList.add('hidden');

  modal.classList.remove('hidden');
  loadPhotoCommentsList(currentPhotoCommentTarget.photoId);
}

function closePhotoCommentsModal() {
  const modal = document.getElementById('modal-photo-comments');
  if (modal) modal.classList.add('hidden');
  currentPhotoCommentTarget = null;
}

async function loadPhotoCommentsList(photoId) {
  const container = document.getElementById('photo-comments-list');
  if (!container) return;

  try {
    const res = await fetch(`/api/v1/photos/comments?photo_id=${encodeURIComponent(photoId)}`);
    const data = await res.json();
    const comments = data.comments || [];

    const likesCountEl = document.getElementById('photo-comments-likes-count');
    if (likesCountEl) likesCountEl.textContent = `${data.likes_count || 0} gostos`;

    if (comments.length === 0) {
      container.innerHTML = `
        <div class="text-center py-6 text-zinc-500 text-xs">
          <i class="fa-regular fa-comment-dots text-2xl mb-1 text-zinc-600 block"></i>
          Ainda não há comentários nesta foto. Deixa o teu elogio respeitoso!
        </div>`;
      return;
    }

    container.innerHTML = comments.map(c => `
      <div class="p-3 rounded-2xl bg-zinc-900 border border-zinc-800 text-xs">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center gap-2">
            <img src="${c.user_photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'}" class="w-6 h-6 rounded-full object-cover"/>
            <span class="font-bold text-white">${esc(c.user_name || 'Utilizador')}</span>
          </div>
          <span class="text-[10px] text-zinc-500">${esc(c.time || 'Agora')}</span>
        </div>
        <p class="text-zinc-200 mt-1 pl-8">${esc(c.text)}</p>
      </div>
    `).join('');
  } catch(e) {
    container.innerHTML = `<p class="text-xs text-red-400">Erro ao carregar comentários.</p>`;
  }
}

function toggleLikeCurrentPhoto() {
  if (!currentPhotoCommentTarget) return;
  fetch('/api/v1/photos/like', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ photo_id: currentPhotoCommentTarget.photoId })
  }).then(r => r.json()).then(data => {
    if (data.success) {
      const likesCountEl = document.getElementById('photo-comments-likes-count');
      if (likesCountEl) likesCountEl.textContent = `${data.likes_count} gostos`;
      const btn = document.getElementById('btn-photo-like-toggle');
      if (btn) {
        btn.classList.toggle('bg-pink-600', data.liked);
        btn.classList.toggle('text-white', data.liked);
      }
      // Se estiver visível no cartão, atualizar também
      const cardCounter = document.getElementById(`card-likes-count-${currentPhotoCommentTarget.profileId}`);
      if (cardCounter) cardCounter.textContent = data.likes_count;
    }
  }).catch(() => {});
}

function handlePhotoCommentInput(input) {
  const alertEl = document.getElementById('photo-comment-security-alert');
  const alertText = document.getElementById('photo-comment-security-text');

  if (alertEl) {
    const check = validateContentPrivacyClient(input.value);
    if (!check.ok) {
      if (alertText) alertText.textContent = check.reason;
      alertEl.classList.remove('hidden');
    } else {
      alertEl.classList.add('hidden');
    }
  }
}

async function submitPhotoComment() {
  if (!currentPhotoCommentTarget) return;

  const input = document.getElementById('photo-comment-input');
  const alertEl = document.getElementById('photo-comment-security-alert');
  const alertText = document.getElementById('photo-comment-security-text');
  const text = input ? input.value.trim() : '';

  if (!text) {
    if (alertText) alertText.textContent = 'Escreve um comentário.';
    if (alertEl) alertEl.classList.remove('hidden');
    return;
  }

  // Validação Anti-Doxxing
  const privacyCheck = validateContentPrivacyClient(text);
  if (!privacyCheck.ok) {
    if (alertText) alertText.textContent = privacyCheck.reason;
    if (alertEl) alertEl.classList.remove('hidden');
    return;
  }

  try {
    const res = await fetch('/api/v1/photos/comment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        photo_id: currentPhotoCommentTarget.photoId,
        text: text
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      if (alertText) alertText.textContent = data.error || 'Erro ao publicar comentário.';
      if (alertEl) alertEl.classList.remove('hidden');
      return;
    }

    input.value = '';
    if (alertEl) alertEl.classList.add('hidden');
    await loadPhotoCommentsList(currentPhotoCommentTarget.photoId);
  } catch(e) {
    if (alertText) alertText.textContent = 'Erro de ligação ao servidor.';
    if (alertEl) alertEl.classList.add('hidden');
  }
}

// ══ COMENTÁRIOS DE MOMENTS (HISTÓRIAS 24H) ═════════════════════════════════
let currentMomentCommentId = null;

function openMomentComments(momentId) {
  currentMomentCommentId = momentId;
  const modal = document.getElementById('modal-moment-comments');
  if (!modal) return;
  const inputEl = document.getElementById('moment-comment-input');
  if (inputEl) inputEl.value = '';
  const alertEl = document.getElementById('moment-comment-security-alert');
  if (alertEl) alertEl.classList.add('hidden');
  modal.classList.remove('hidden');
  loadMomentCommentsList(momentId);
}

function closeMomentComments() {
  const modal = document.getElementById('modal-moment-comments');
  if (modal) modal.classList.add('hidden');
  currentMomentCommentId = null;
}

async function loadMomentCommentsList(momentId) {
  const container = document.getElementById('moment-comments-list');
  if (!container) return;
  try {
    const res = await fetch(`/api/v1/moments/comments?moment_id=${encodeURIComponent(momentId)}`);
    const data = await res.json();
    if (!res.ok || !data.success) {
      container.innerHTML = `<p class="text-xs text-red-400 text-center py-4">${esc(data.error || 'Erro ao carregar comentários.')}</p>`;
      return;
    }
    const comments = data.comments || [];
    if (comments.length === 0) {
      container.innerHTML = `
        <div class="text-center py-6 text-zinc-500 text-xs">
          <i class="fa-regular fa-comment-dots text-2xl mb-1 text-zinc-600 block"></i>
          Ainda não há comentários nesta história. Sê o primeiro!
        </div>`;
      return;
    }
    container.innerHTML = comments.map(c => `
      <div class="p-3 rounded-2xl bg-zinc-900 border border-zinc-800 text-xs">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center gap-2">
            <img src="${c.user_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'}" class="w-6 h-6 rounded-full object-cover ring-2 ring-purple-500/30"/>
            <span class="font-bold text-white">${esc(c.user_name || 'Utilizador')}</span>
            <span class="text-[9px] bg-purple-500/15 text-purple-300 rounded-full px-1.5 border border-purple-500/30">Match</span>
          </div>
          <span class="text-[10px] text-zinc-500">${esc(c.timestamp || 'Agora')}</span>
        </div>
        <p class="text-zinc-200 mt-1 pl-8">${esc(c.text)}</p>
      </div>
    `).join('');
  } catch(e) {
    container.innerHTML = `<p class="text-xs text-red-400 text-center py-4">Erro ao carregar comentários.</p>`;
  }
}

function handleMomentCommentInput(input) {
  const alertEl = document.getElementById('moment-comment-security-alert');
  const alertText = document.getElementById('moment-comment-security-text');
  if (!alertEl) return;
  const check = validateContentPrivacyClient(input.value);
  if (!check.ok) {
    if (alertText) alertText.textContent = check.reason;
    alertEl.classList.remove('hidden');
  } else {
    alertEl.classList.add('hidden');
  }
}

async function submitMomentComment() {
  if (!currentMomentCommentId) return;
  const input = document.getElementById('moment-comment-input');
  const alertEl = document.getElementById('moment-comment-security-alert');
  const alertText = document.getElementById('moment-comment-security-text');
  const text = input ? input.value.trim() : '';

  if (!text) {
    if (alertText) alertText.textContent = 'Escreve um comentário.';
    if (alertEl) alertEl.classList.remove('hidden');
    return;
  }

  // Validação Anti-Doxxing (igual ao texto do Moment)
  const privacyCheck = validateContentPrivacyClient(text);
  if (!privacyCheck.ok) {
    if (alertText) alertText.textContent = privacyCheck.reason;
    if (alertEl) alertEl.classList.remove('hidden');
    return;
  }

  try {
    const res = await fetch('/api/v1/moments/comment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ moment_id: currentMomentCommentId, text: text })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      if (alertText) alertText.textContent = data.error || 'Erro ao publicar comentário.';
      if (alertEl) alertEl.classList.remove('hidden');
      return;
    }

    input.value = '';
    if (alertEl) alertEl.classList.add('hidden');
    await loadMomentCommentsList(currentMomentCommentId);

    // atualizar o contador no card do Moment
    const countEl = document.getElementById(`moment-comments-count-${currentMomentCommentId}`);
    if (countEl && data.total_comments !== undefined) {
      const prevCount = countEl.textContent;
      countEl.textContent = data.total_comments;
      // Comentário novo: acende o botão durante 2s para sinalizar atividade
      if (String(prevCount) !== String(data.total_comments)) {
        const btn = countEl.closest('button');
        if (btn) {
          btn.classList.add('animate-pulse');
          setTimeout(() => btn.classList.remove('animate-pulse'), 2000);
        }
      }
    }
  } catch(e) {
    if (alertText) alertText.textContent = 'Erro de ligação ao servidor.';
    if (alertEl) alertEl.classList.remove('hidden');
  }
}
