document.addEventListener('DOMContentLoaded', () => {
    const netRangeInput = document.getElementById('netRangeInput');
    const btnRunSimulation = document.getElementById('btnRunSimulation');
    const btnDownloadPDF = document.getElementById('btnDownloadPDF');

    const kpiTotalDevs = document.getElementById('kpiTotalDevs');
    const kpiActiveDevs = document.getElementById('kpiActiveDevs');
    const kpiAvgScore = document.getElementById('kpiAvgScore');
    const lastScanTime = document.getElementById('lastScanTime');
    const devicesTableBody = document.getElementById('devicesTableBody');

    // 1. Executar Simulação
    btnRunSimulation.addEventListener('click', async () => {
        const range = netRangeInput.value.trim() || '192.168.1.0/24';

        btnRunSimulation.disabled = true;
        btnRunSimulation.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> A simular...';

        try {
            const res = await fetch('/api/simulate-scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ range: range })
            });

            const data = await res.json();
            if (data.success) {
                renderSimulation(data);
                showToast('Simulação de inventário concluída com sucesso.', 'success');
            } else {
                showToast(data.message || 'Ocorreu um erro na simulação.', 'error');
            }
        } catch (err) {
            showToast('Não foi possível ligar ao servidor.', 'error');
        } finally {
            btnRunSimulation.disabled = false;
            btnRunSimulation.innerHTML = '<i class="fa-solid fa-play"></i> Executar Simulação';
        }
    });

    // 2. Renderizar Resultados Simulados em UI
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
                        <p>Não foram encontrados dados simulados.</p>
                    </td>
                </tr>
            `;
            return;
        }

        data.devices.forEach(dev => {
            const tr = document.createElement('tr');
            const isActive = dev.status === 'Ativo';
            const statusClass = isActive ? 'active' : 'inactive';
            const portsText = dev.simulated_ports.length > 0 ? dev.simulated_ports.join(', ') : 'Nenhum';

            tr.innerHTML = `
                <td><strong>${dev.hostname}</strong></td>
                <td><code>${dev.ip}</code></td>
                <td><code>${dev.mac}</code></td>
                <td>${dev.type}</td>
                <td><span class="badge-status ${statusClass}">${portsText}</span></td>
                <td><strong>${dev.security_score} pts</strong></td>
                <td style="font-size: 12px; color: #94a3b8;">${dev.recommendation}</td>
            `;
            devicesTableBody.appendChild(tr);
        });
    }

    // 3. Transferir PDF Simulado
    btnDownloadPDF.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/generate-pdf', { method: 'POST' });
            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'Relatorio_Inventario_Rede_Simulado.pdf';
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
