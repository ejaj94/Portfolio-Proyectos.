document.addEventListener('DOMContentLoaded', () => {
    let systemChart = null;
    let rawProcesses = [];
    const maxDataPoints = 15;
    const chartLabels = [];
    const cpuData = [];
    const ramData = [];

    // DOM Elements
    const lblUptime = document.getElementById('lblUptime');
    const lblCpuPct = document.getElementById('lblCpuPct');
    const barCpu = document.getElementById('barCpu');
    const lblCpuCores = document.getElementById('lblCpuCores');
    const lblCpuFreq = document.getElementById('lblCpuFreq');

    const lblRamPct = document.getElementById('lblRamPct');
    const barRam = document.getElementById('barRam');
    const lblRamUsed = document.getElementById('lblRamUsed');
    const lblRamTotal = document.getElementById('lblRamTotal');

    const lblDiskPct = document.getElementById('lblDiskPct');
    const barDisk = document.getElementById('barDisk');
    const lblDiskUsed = document.getElementById('lblDiskUsed');
    const lblDiskTotal = document.getElementById('lblDiskTotal');

    const lblNetTotal = document.getElementById('lblNetTotal');
    const barNet = document.getElementById('barNet');
    const lblNetSent = document.getElementById('lblNetSent');
    const lblNetRecv = document.getElementById('lblNetRecv');

    const tblProcessesBody = document.getElementById('tblProcessesBody');
    const txtSearchProcess = document.getElementById('txtSearchProcess');
    const selSortBy = document.getElementById('selSortBy');
    const consoleLogFeed = document.getElementById('consoleLogFeed');
    const btnClearLogs = document.getElementById('btnClearLogs');

    const modalInspector = document.getElementById('modalInspector');
    const modalBody = document.getElementById('modalBody');
    const btnCloseModal = document.getElementById('btnCloseModal');

    // 1. Inicializar Gráfico Chart.js
    function initChart() {
        const ctx = document.getElementById('systemChart').getContext('2d');
        systemChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,
                datasets: [
                    {
                        label: 'CPU (%)',
                        data: cpuData,
                        borderColor: '#00f0ff',
                        backgroundColor: 'rgba(0, 240, 255, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'RAM (%)',
                        data: ramData,
                        borderColor: '#ff007f',
                        backgroundColor: 'rgba(255, 0, 127, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8', font: { family: 'Share Tech Mono' } }
                    },
                    y: {
                        min: 0,
                        max: 100,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8', font: { family: 'Share Tech Mono' } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc', font: { family: 'Orbitron', size: 11 } }
                    }
                }
            }
        });
    }

    // 2. Fetch System Stats
    async function fetchStats() {
        try {
            const res = await fetch('/api/system-stats');
            const data = await res.json();

            if (data.success) {
                updateMetricsUI(data.data);
            }
        } catch (err) {
            logConsole(`[ERR] Falha ao consultar telemetria do sistema: ${err.message}`, 'error');
        }
    }

    function updateMetricsUI(stats) {
        lblUptime.textContent = stats.boot_time;

        // CPU
        lblCpuPct.textContent = `${stats.cpu.percent}%`;
        barCpu.style.width = `${stats.cpu.percent}%`;
        lblCpuCores.textContent = stats.cpu.cores;
        lblCpuFreq.textContent = `${stats.cpu.freq_mhz} MHz`;

        // RAM
        lblRamPct.textContent = `${stats.ram.percent}%`;
        barRam.style.width = `${stats.ram.percent}%`;
        lblRamUsed.textContent = `${stats.ram.used_gb} GB`;
        lblRamTotal.textContent = `${stats.ram.total_gb} GB`;

        // DISK
        lblDiskPct.textContent = `${stats.disk.percent}%`;
        barDisk.style.width = `${stats.disk.percent}%`;
        lblDiskUsed.textContent = `${stats.disk.used_gb} GB`;
        lblDiskTotal.textContent = `${stats.disk.total_gb} GB`;

        // NETWORK
        const netTotal = roundVal(stats.network.sent_mb + stats.network.recv_mb, 1);
        lblNetTotal.textContent = `${netTotal} MB`;
        lblNetSent.textContent = `${stats.network.sent_mb} MB`;
        lblNetRecv.textContent = `${stats.network.recv_mb} MB`;

        // Chart Update
        chartLabels.push(stats.timestamp);
        cpuData.push(stats.cpu.percent);
        ramData.push(stats.ram.percent);

        if (chartLabels.length > maxDataPoints) {
            chartLabels.shift();
            cpuData.shift();
            ramData.shift();
        }

        if (systemChart) systemChart.update();
    }

    // 3. Fetch Processes
    async function fetchProcesses() {
        const sortBy = selSortBy.value;
        try {
            const res = await fetch(`/api/processes?limit=40&sort_by=${sortBy}`);
            const data = await res.json();

            if (data.success) {
                rawProcesses = data.processes;
                renderProcessesTable();
            }
        } catch (err) {
            logConsole(`[ERR] Erro ao carregar processos: ${err.message}`, 'error');
        }
    }

    function renderProcessesTable() {
        const query = txtSearchProcess.value.toLowerCase().trim();
        let filtered = rawProcesses;

        if (query) {
            filtered = rawProcesses.filter(p => 
                p.name.toLowerCase().includes(query) || 
                p.pid.toString().includes(query) ||
                p.user.toLowerCase().includes(query)
            );
        }

        tblProcessesBody.innerHTML = '';

        if (filtered.length === 0) {
            tblProcessesBody.innerHTML = `
                <tr>
                    <td colspan="7" class="loading-row">Nenhum processo encontrado.</td>
                </tr>
            `;
            return;
        }

        filtered.forEach(p => {
            const tr = document.createElement('tr');
            const statusClass = p.status === 'running' ? 'running' : 'sleeping';

            tr.innerHTML = `
                <td class="pid-pill">${p.pid}</td>
                <td class="proc-name">${p.name}</td>
                <td><span class="badge-status ${statusClass}">${p.status.toUpperCase()}</span></td>
                <td class="cpu-highlight">${p.cpu_pct}%</td>
                <td class="ram-highlight">${p.memory_mb} MB</td>
                <td style="color: #94a3b8; font-size: 12px;">${p.user}</td>
                <td>
                    <button class="btn-inspect" data-pid="${p.pid}">
                        <i class="fa-solid fa-eye"></i> Ver
                    </button>
                </td>
            `;
            tblProcessesBody.appendChild(tr);
        });

        // Add event listeners to inspect buttons
        document.querySelectorAll('.btn-inspect').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const pid = e.currentTarget.getAttribute('data-pid');
                inspectProcess(pid);
            });
        });
    }

    // 4. Inspect Process Modal
    async function inspectProcess(pid) {
        modalBody.innerHTML = '<p><i class="fa-solid fa-spinner fa-spin"></i> A carregar detalhes do PID ' + pid + '...</p>';
        modalInspector.style.display = 'flex';

        try {
            const res = await fetch(`/api/process/${pid}`);
            const data = await res.json();

            if (data.success) {
                modalBody.innerHTML = `
                    <p><strong>PID:</strong> ${data.pid}</p>
                    <p><strong>Nome:</strong> ${data.name}</p>
                    <p><strong>Estado:</strong> ${data.status}</p>
                    <p><strong>Uso de CPU:</strong> ${data.cpu_pct}%</p>
                    <p><strong>Uso de RAM:</strong> ${data.memory_mb} MB</p>
                    <p><strong>Hora de Início:</strong> ${data.create_time}</p>
                    <p><strong>Caminho Executável:</strong> <code>${data.exe_path}</code></p>
                `;
                logConsole(`[INSPECT] Processo consultado PID ${pid} (${data.name}).`, 'info');
            } else {
                modalBody.innerHTML = `<p class="error">${data.message}</p>`;
            }
        } catch (err) {
            modalBody.innerHTML = `<p class="error">Erro de comunicação.</p>`;
        }
    }

    btnCloseModal.addEventListener('click', () => {
        modalInspector.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modalInspector) modalInspector.style.display = 'none';
    });

    // Event Listeners for Filters
    txtSearchProcess.addEventListener('input', renderProcessesTable);
    selSortBy.addEventListener('change', fetchProcesses);

    btnClearLogs.addEventListener('click', () => {
        consoleLogFeed.innerHTML = '<div class="log-line info">[>] Consola de telemetria limpa.</div>';
    });

    function logConsole(msg, type = 'info') {
        const line = document.createElement('div');
        line.className = `log-line ${type}`;
        line.textContent = `${new Date().toLocaleTimeString()} - ${msg}`;
        consoleLogFeed.appendChild(line);
        consoleLogFeed.scrollTop = consoleLogFeed.scrollHeight;
    }

    function roundVal(num, decimals) {
        return Math.round(num * Math.pow(10, decimals)) / Math.pow(10, decimals);
    }

    function showToast(msg, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<i class="fa-solid fa-circle-info"></i> <span>${msg}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Init & Polling Loops
    initChart();
    fetchStats();
    fetchProcesses();

    setInterval(fetchStats, 2000);
    setInterval(fetchProcesses, 3000);
});
