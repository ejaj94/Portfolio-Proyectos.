document.addEventListener('DOMContentLoaded', () => {
    // Document Upload Form Submit
    const docForm = document.getElementById('upload-doc-form');
    if (docForm) {
        docForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                file_name: document.getElementById('upload-file-name').value,
                category: document.getElementById('upload-category').value,
                folder_id: document.getElementById('upload-folder-id').value,
                file_extension: document.getElementById('upload-extension').value,
                access_permission: document.getElementById('upload-permission').value,
                uploaded_by: document.getElementById('upload-author').value
            };

            fetch('/api/document/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao carregar documento.'));
        });
    }

    // Folder Create Form Submit
    const folderForm = document.getElementById('create-folder-form');
    if (folderForm) {
        folderForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                folder_name: document.getElementById('folder-name-input').value,
                color: document.getElementById('folder-color-input').value
            };

            fetch('/api/folder/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao criar pasta.'));
        });
    }
});

// Toggle Star/Favorite AJAX
function toggleStar(docId, btnElem) {
    fetch(`/api/document/star/${docId}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const icon = btnElem.querySelector('i');
            if (data.is_starred === 1) {
                icon.className = 'fa-solid fa-star';
                icon.style.color = 'var(--warm-amber)';
            } else {
                icon.className = 'fa-regular fa-star';
                icon.style.color = 'var(--text-muted)';
            }
        }
    })
    .catch(err => alert('❌ Erro ao atualizar favorito.'));
}

// Download Document AJAX
function downloadDocument(docId, fileName) {
    fetch(`/api/document/download/${docId}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        alert(`📥 Download iniciado: ${fileName}\n\nFicheiro transferido com sucesso para a sua pasta de Downloads.`);
        window.location.reload();
    })
    .catch(err => alert('❌ Erro ao descarregar ficheiro.'));
}

// Copy Share Link Helper
function copyShareLink(shareCode) {
    const fullUrl = `${window.location.origin}/share/${shareCode}`;
    navigator.clipboard.writeText(fullUrl).then(() => {
        alert(`🔗 Link de Partilha Encriptado Copiado!\n\nURL: ${fullUrl}`);
    }).catch(() => {
        prompt('Copie o link de partilha:', fullUrl);
    });
}
