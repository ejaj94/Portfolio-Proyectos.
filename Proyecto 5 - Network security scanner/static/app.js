document.addEventListener('DOMContentLoaded', () => {
    const netRangeInput = document.getElementById('netRangeInput');
    const btnRunSimulation = document.getElementById('btnRunSimulation');
    const btnDownloadPDF = document.getElementById('btnDownloadPDF');

    const kpiTotalDevs = document.getElementById('kpiTotalDevs');
    const kpiActiveDevs = document.getElementById('kpiActiveDevs');
    const kpiAvgScore = document.getElementById('kpiAvgScore');
    const lastScanTime = document.getElementById('lastScanTime');
    const devicesTableBody = document.getElementById('devicesTableBody');

    // 1. Analisar Rede
    btnRunSimulation.addEventListener('click', async () => {
        const range = netRangeInput.value.trim() || '192.168.1.0/24';

        btnRunSimulation.disabled = true;
        btnRunSimulation.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A analisar...';

        try {
            const res = await fetch('/api/simulate-scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ range: range })
            });

            const data = await res.json();
            if (data.success) {
                renderSimulation(data);
                showToast('Análise de inventário concluída com sucesso.', 'success');
            } else {
                showToast(data.message || 'Ocorreu um erro durante a análise.', 'error');
            }
        } catch (err) {
            showToast('Não foi possível ligar ao servidor.', 'error');
        } finally {
            btnRunSimulation.disabled = false;
            btnRunSimulation.innerHTML = '<i class="fa-solid fa-bolt"></i> Analisar Rede';
        }
    });

    // 2. Renderizar Resultados na UI (com Badges Individuais para Portas)
    function renderSimulation(data) {
        kpiTotalDevs.textContent = data.summary.total_found;
        kpiActiveDevs.textContent = data.summary.active_found;
        kpiAvgScore.textContent = `${data.summary.avg_security_score} / 100`;
        lastScanTime.textContent = `Atualizado: ${data.timestamp}`;

        devicesTableBody.innerHTML = '';

        if (!data.devices || data.devices.length === 0) {
            devicesTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="empty-state">
                        <i class="fa-solid fa-shield-halved"></i>
                        <p>Não foram encontrados dados de inventário.</p>
                    </td>
                </tr>
            `;
            return;
        }

        data.devices.forEach(dev => {
            const tr = document.createElement('tr');
            const isActive = dev.status === 'Ativo';
            const statusClass = isActive ? 'active' : 'inactive';
            
            let portsHtml = '<span class="no-ports">Nenhum</span>';
            if (dev.simulated_ports && dev.simulated_ports.length > 0) {
                portsHtml = `<div class="ports-flex">` + 
                    dev.simulated_ports.map(p => `<span class="port-pill">${p}</span>`).join('') + 
                    `</div>`;
            }

            tr.innerHTML = `
                <td>
                    <div class="dev-name-container">
                        <i class="fa-solid fa-network-wired dev-icon"></i>
                        <strong>${dev.hostname}</strong>
                    </div>
                </td>
                <td><code class="code-badge ip-badge">${dev.ip}</code></td>
                <td><code class="code-badge mac-badge">${dev.mac}</code></td>
                <td><span class="type-pill">${dev.type}</span></td>
                <td>${portsHtml}</td>
                <td><span class="score-pill">${dev.security_score} pts</span></td>
                <td class="rec-text">${dev.recommendation}</td>
            `;
            devicesTableBody.appendChild(tr);
        });
    }

    // 3. Exportar PDF
    btnDownloadPDF.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/generate-pdf', { method: 'POST' });
            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'Relatorio_Inventario_Rede_PRO.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
                showToast('Relatório PDF transferido com sucesso.', 'success');
            } else {
                showToast('Erro ao gerar relatório PDF.', 'error');
            }
        } catch (err) {
            showToast('Erro ao transferir ficheiro.', 'error');
        }
    });

    function showToast(msg, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = 'fa-circle-info';
        if (type === 'success') icon = 'fa-circle-check';

        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${msg}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }
});
