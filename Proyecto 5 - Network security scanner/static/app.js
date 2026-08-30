document.addEventListener('DOMContentLoaded', () => {
    const netRangeInput = document.getElementById('netRangeInput');
    const btnRunSimulation = document.getElementById('btnRunSimulation');
    const btnDownloadPDF = document.getElementById('btnDownloadPDF');

    const kpiTotalDevs = document.getElementById('kpiTotalDevs');
    const kpiActiveDevs = document.getElementById('kpiActiveDevs');
    const kpiAvgScore = document.getElementById('kpiAvgScore');
    const lastScanTime = document.getElementById('lastScanTime');
    const devicesTableBody = document.getElementById('devicesTableBody');

    // 1. Ejecutar Simulación
    btnRunSimulation.addEventListener('click', async () => {
        const range = netRangeInput.value.trim() || '192.168.1.0/24';

        btnRunSimulation.disabled = true;
        btnRunSimulation.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Simulando...';

        try {
            const res = await fetch('/api/simulate-scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ range: range })
            });

            const data = await res.json();
            if (data.success) {
                renderSimulation(data);
                showToast('Simulación de inventario completada.', 'success');
            } else {
                showToast(data.message || 'Error en la simulación.', 'error');
            }
        } catch (err) {
            showToast('No se pudo conectar con el servidor.', 'error');
        } finally {
            btnRunSimulation.disabled = false;
            btnRunSimulation.innerHTML = '<i class="fa-solid fa-play"></i> Ejecutar Simulación';
        }
    });

    // 2. Renderizar Resultados Simulados en UI
    function renderSimulation(data) {
        kpiTotalDevs.textContent = data.summary.total_found;
        kpiActiveDevs.textContent = data.summary.active_found;
        kpiAvgScore.textContent = `${data.summary.avg_security_score} / 100`;
        lastScanTime.textContent = `Actualizado: ${data.timestamp}`;

        devicesTableBody.innerHTML = '';

        if (!data.devices || data.devices.length === 0) {
            devicesTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="empty-state">
                        <i class="fa-solid fa-shield-halved"></i>
                        <p>No se encontraron datos simulados.</p>
                    </td>
                </tr>
            `;
            return;
        }

        data.devices.forEach(dev => {
            const tr = document.createElement('tr');
            const isActive = dev.status === 'Activo';
            const statusClass = isActive ? 'active' : 'inactive';
            const portsText = dev.simulated_ports.length > 0 ? dev.simulated_ports.join(', ') : 'Ninguno';

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

    // 3. Descargar PDF Simulado
    btnDownloadPDF.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/generate-pdf', { method: 'POST' });
            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'Reporte_Inventario_Red_Simulado.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
                showToast('Reporte PDF descargado.', 'success');
            } else {
                showToast('Error al generar PDF.', 'error');
            }
        } catch (err) {
            showToast('Error en la descarga.', 'error');
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
