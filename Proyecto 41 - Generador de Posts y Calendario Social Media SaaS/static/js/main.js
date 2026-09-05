// SOCIALPOST AI SaaS - Client Interactivity

function showToast(message, isError = false) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    if (isError) {
        toast.style.borderColor = '#EF4444';
    }
    toast.innerHTML = `<span>${isError ? '⚠️' : '✨'}</span> <div>${message}</div>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 4000);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copy copiada para a área de transferência com sucesso!');
    }).catch(err => {
        showToast('Erro ao copiar texto', true);
    });
}

// Generate Post Logic
document.addEventListener('DOMContentLoaded', () => {
    const generatorForm = document.getElementById('generatorForm');
    if (generatorForm) {
        generatorForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const generateBtn = document.getElementById('generateBtn');
            const originalBtnHtml = generateBtn.innerHTML;
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<span>⚡</span> A Gerar Copy com IA...';
            
            const topic = document.getElementById('topicInput').value;
            const platform = document.getElementById('platformSelect').value;
            const tone = document.getElementById('toneSelect').value;
            const ctaType = document.getElementById('ctaSelect').value;
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic, platform, tone, cta_type: ctaType })
                });
                
                const data = await response.json();
                if (data.success) {
                    // Update preview card
                    document.getElementById('previewPlatform').textContent = data.platform;
                    document.getElementById('previewCopy').textContent = data.copy;
                    document.getElementById('previewHashtags').textContent = data.hashtags;
                    document.getElementById('previewCta').textContent = data.cta;
                    document.getElementById('previewMedia').textContent = data.media_suggestion;
                    
                    // Show preview container
                    const previewCard = document.getElementById('previewCard');
                    previewCard.style.display = 'block';
                    previewCard.scrollIntoView({ behavior: 'smooth' });
                    
                    showToast('Post gerado com êxito! Pode pré-visualizar ou agendar.');
                } else {
                    showToast('Erro ao gerar post', true);
                }
            } catch (err) {
                console.error(err);
                showToast('Falha na ligação com o servidor', true);
            } finally {
                generateBtn.disabled = false;
                generateBtn.innerHTML = originalBtnHtml;
            }
        });
    }
    
    // Save Generated Post to Calendar
    const savePostBtn = document.getElementById('savePostBtn');
    if (savePostBtn) {
        savePostBtn.addEventListener('click', async () => {
            const topic = document.getElementById('topicInput') ? document.getElementById('topicInput').value : 'Novo Post';
            const platform = document.getElementById('previewPlatform').textContent;
            const tone = document.getElementById('toneSelect') ? document.getElementById('toneSelect').value : 'Profissional';
            const copyText = document.getElementById('previewCopy').textContent;
            const hashtags = document.getElementById('previewHashtags').textContent;
            const cta = document.getElementById('previewCta').textContent;
            const mediaSuggestion = document.getElementById('previewMedia').textContent;
            
            const scheduleDate = document.getElementById('scheduleDateInput') ? document.getElementById('scheduleDateInput').value : '';
            const scheduleTime = document.getElementById('scheduleTimeInput') ? document.getElementById('scheduleTimeInput').value : '12:00';
            
            try {
                const response = await fetch('/api/posts/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic,
                        platform,
                        tone,
                        copy: copyText,
                        hashtags,
                        cta,
                        media_suggestion: mediaSuggestion,
                        scheduled_date: scheduleDate,
                        scheduled_time: scheduleTime,
                        status: 'Agendado'
                    })
                });
                
                const res = await response.json();
                if (res.success) {
                    showToast('Post adicionado ao Calendário Editorial com sucesso!');
                    setTimeout(() => {
                        window.location.href = '/calendar';
                    }, 1200);
                }
            } catch (err) {
                showToast('Erro ao guardar post no calendário', true);
            }
        });
    }
    
    // Copy Full Post Button
    const copyFullPostBtn = document.getElementById('copyFullPostBtn');
    if (copyFullPostBtn) {
        copyFullPostBtn.addEventListener('click', () => {
            const copyText = document.getElementById('previewCopy').textContent;
            const hashtags = document.getElementById('previewHashtags').textContent;
            const cta = document.getElementById('previewCta').textContent;
            
            const fullPost = `${copyText}\n\n${cta}\n\n${hashtags}`;
            copyToClipboard(fullPost);
        });
    }
});

// Delete Post function
async function deletePost(postId) {
    if (!confirm('Tem a certeza que deseja eliminar esta publicação?')) return;
    
    try {
        const response = await fetch(`/api/posts/delete/${postId}`, {
            method: 'DELETE'
        });
        const res = await response.json();
        if (res.success) {
            showToast('Post eliminado com êxito!');
            const elem = document.getElementById(`post-row-${postId}`) || document.getElementById(`post-card-${postId}`);
            if (elem) elem.remove();
        }
    } catch (err) {
        showToast('Erro ao eliminar publicação', true);
    }
}
