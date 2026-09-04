// VELOCE-LINK SaaS - Client Side Interactive Scripts

// Copiar URL encurtado para a área de transferência
function copyToClipboard(urlText) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(urlText).then(() => {
            showToast('📋 Hiperlink copiado com sucesso!');
        });
    } else {
        const dummy = document.createElement('input');
        document.body.appendChild(dummy);
        dummy.value = urlText;
        dummy.select();
        document.execCommand('copy');
        document.body.removeChild(dummy);
        showToast('📋 Hiperlink copiado com sucesso!');
    }
}

// Abrir Modal de QR Code
function openQRModal(title, qrUrl, shortUrl) {
    const modal = document.getElementById('qrModal');
    const titleElem = document.getElementById('qrModalTitle');
    const imgElem = document.getElementById('qrModalImage');
    const linkElem = document.getElementById('qrModalLink');
    const downloadBtn = document.getElementById('qrModalDownload');

    if (modal && titleElem && imgElem && linkElem) {
        titleElem.innerText = title;
        imgElem.src = qrUrl;
        linkElem.innerText = shortUrl;
        linkElem.href = shortUrl;
        if (downloadBtn) downloadBtn.href = qrUrl;

        modal.classList.remove('hidden');
    }
}

// Mostrar Toast Flutuante
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-5 right-5 bg-cyan-600 text-white font-bold text-xs px-4 py-3 rounded-xl shadow-2xl z-50 animate-bounce flex items-center space-x-2 border border-cyan-400';
    toast.innerHTML = `<i class="fas fa-link text-base"></i><span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
