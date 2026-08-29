document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const folderPathInput = document.getElementById('folderPath');
    const btnScan = document.getElementById('btnScan');
    const btnDryRun = document.getElementById('btnDryRun');
    const btnOrganize = document.getElementById('btnOrganize');
    const btnUndo = document.getElementById('btnUndo');
    const btnDuplicates = document.getElementById('btnDuplicates');
    const shortcutsContainer = document.getElementById('shortcutsContainer');
    const filesTableBody = document.getElementById('filesTableBody');
    const tableSearch = document.getElementById('tableSearch');
    const tableTitle = document.getElementById('tableTitle');

    // KPI Elements
    const kpiTotalFiles = document.getElementById('kpiTotalFiles');
    const kpiTotalSize = document.getElementById('kpiTotalSize');
    const kpiTotalCategories = document.getElementById('kpiTotalCategories');
    const breakdownSection = document.getElementById('breakdownSection');
    const breakdownBars = document.getElementById('breakdownBars');

    let currentScanData = null;

    // 1. Cargar Accesos Directos
    fetchSystemFolders();

    async function fetchSystemFolders() {
        try {
            const res = await fetch('/api/system-folders');
            const data = await res.json();
            if (data.success) {
                shortcutsContainer.innerHTML = '';
                for (const [name, path] of Object.entries(data.folders)) {
                    const chip = document.createElement('div');
                    chip.className = 'chip';
                    chip.innerHTML = `<i class="fa-solid fa-folder"></i> ${name}`;
                    chip.addEventListener('click', () => {
                        folderPathInput.value = path;
                        scanFolder();
                    });
                    shortcutsContainer.appendChild(chip);
                }
                // Si la caja de texto está vacía, colocar Descargas por defecto
                if (!folderPathInput.value && data.folders['Descargas']) {
                    folderPathInput.value = data.folders['Descargas'];
                    scanFolder();
                }
            }
        } catch (err) {
            console.error('Error al cargar carpetas del sistema:', err);
        }
    }

    // Obtener Modo Seleccionado
    function getSelectedMode() {
        const selected = document.querySelector('input[name="orgMode"]:checked');
        return selected ? selected.value : 'category';
    }

    // 2. Escanear Carpeta
    async function scanFolder() {
        const path = folderPathInput.value.trim();
        if (!path) {
            showToast('Ingresa una ruta de carpeta válida.', 'error');
            return;
        }

        const mode = getSelectedMode();

        try {
            const res = await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder_path: path, mode: mode })
            });

            const json = await res.json();
            if (json.success) {
                currentScanData = json.data;
                renderDashboard(json.data);
                showToast(`Escanéo completado: ${json.data.total_files} archivos encontrados.`, 'info');
            } else {
                showToast(json.message || 'Error al escanear carpeta.', 'error');
            }
        } catch (err) {
            showToast('No se pudo conectar con el servidor.', 'error');
        }
    }

    // Renderizar Resultados en UI
    function renderDashboard(data) {
        // Actualizar KPIs
        kpiTotalFiles.textContent = data.total_files;
        kpiTotalSize.textContent = data.total_size_human;
        const categoriesCount = Object.keys(data.breakdown || {}).length;
        kpiTotalCategories.textContent = categoriesCount;

        // Renderizar Barras de Desglose
        if (categoriesCount > 0) {
            breakdownSection.classList.remove('hidden');
            breakdownBars.innerHTML = '';

            const totalBytes = data.total_size_bytes || 1;

            for (const [cat, info] of Object.entries(data.breakdown)) {
                const pct = Math.round((info.size_bytes / totalBytes) * 100) || 1;
                const barItem = document.createElement('div');
                barItem.className = 'bar-item';
                barItem.innerHTML = `
                    <div class="bar-header">
                        <span><strong>${cat}</strong> (${info.count} archivos)</span>
                        <span>${info.size_human} (${pct}%)</span>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${pct}%;"></div>
                    </div>
                `;
                breakdownBars.appendChild(barItem);
            }
        } else {
            breakdownSection.classList.add('hidden');
        }

        // Renderizar Tabla de Archivos
        renderFilesTable(data.files || []);
    }

    function renderFilesTable(files) {
        if (!files || files.length === 0) {
            filesTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-state">
                        <i class="fa-solid fa-folder-open"></i>
                        <p>No hay archivos pendientes por organizar en este nivel de la carpeta.</p>
                    </td>
                </tr>
            `;
            return;
        }

        const filterText = tableSearch.value.toLowerCase().trim();
        const filtered = files.filter(f => 
            f.filename.toLowerCase().includes(filterText) || 
            f.target_folder.toLowerCase().includes(filterText) ||
            f.extension.toLowerCase().includes(filterText)
        );

        filesTableBody.innerHTML = '';

        filtered.forEach(file => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><i class="fa-regular fa-file" style="margin-right: 8px; color: #9ca3af;"></i> ${file.filename}</td>
                <td><code>${file.extension}</code></td>
                <td>${file.size_human}</td>
                <td style="color: #9ca3af; font-size: 12px;">${file.mtime}</td>
                <td><span class="badge-target"><i class="fa-solid fa-folder"></i> ${file.target_folder}</span></td>
            `;
            filesTableBody.appendChild(tr);
        });
    }

    // 3. Simulación (Dry Run)
    btnDryRun.addEventListener('click', async () => {
        const path = folderPathInput.value.trim();
        if (!path) return showToast('Especifica una ruta.', 'error');
        const mode = getSelectedMode();

        try {
            const res = await fetch('/api/organize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder_path: path, mode: mode, dry_run: true })
            });

            const json = await res.json();
            if (json.success) {
                renderDashboard(json.data.scan);
                showToast(`[Simulación]: Se organizarán ${json.data.scan.total_files} archivos sin cambios reales.`, 'info');
            } else {
                showToast(json.message, 'error');
            }
        } catch (err) {
            showToast('Error durante la simulación.', 'error');
        }
    });

    // 4. Organizar Real
    btnOrganize.addEventListener('click', async () => {
        const path = folderPathInput.value.trim();
        if (!path) return showToast('Especifica una ruta.', 'error');
        const mode = getSelectedMode();

        try {
            const res = await fetch('/api/organize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder_path: path, mode: mode, dry_run: false })
            });

            const json = await res.json();
            if (json.success) {
                showToast(`¡Éxito! Se movieron ${json.data.moved_count} archivos correctamente.`, 'success');
                renderDashboard(json.data.scan_after);
            } else {
                showToast(json.message || 'Ocurrió un error al organizar.', 'error');
            }
        } catch (err) {
            showToast('Error al ejecutar la organización.', 'error');
        }
    });

    // 5. Deshacer
    btnUndo.addEventListener('click', async () => {
        const path = folderPathInput.value.trim();
        if (!path) return showToast('Especifica una ruta.', 'error');

        try {
            const res = await fetch('/api/undo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder_path: path })
            });

            const json = await res.json();
            if (json.success) {
                showToast(`Deshecho con éxito: ${json.reverted_count} archivos restaurados.`, 'success');
                scanFolder();
            } else {
                showToast(json.message, 'error');
            }
        } catch (err) {
            showToast('Error al revertir cambios.', 'error');
        }
    });

    // 6. Buscar Duplicados
    btnDuplicates.addEventListener('click', async () => {
        const path = folderPathInput.value.trim();
        if (!path) return showToast('Especifica una ruta.', 'error');

        try {
            const res = await fetch('/api/duplicates', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder_path: path })
            });

            const json = await res.json();
            if (json.success) {
                const dupData = json.data;
                showToast(`Duplicados: ${dupData.group_count} grupos encontrados (${dupData.total_wasted_human} desperdiciados).`, 'info');
                
                // Mostrar en la tabla los duplicados
                filesTableBody.innerHTML = '';
                tableTitle.innerHTML = `<i class="fa-solid fa-copy"></i> Archivos Duplicados Encontrados (${dupData.group_count} Grupos)`;
                
                if (dupData.groups.length === 0) {
                    filesTableBody.innerHTML = `
                        <tr>
                            <td colspan="5" class="empty-state">
                                <i class="fa-solid fa-circle-check" style="color: #10b981;"></i>
                                <p>¡Felicidades! No se encontraron archivos duplicados en esta carpeta.</p>
                            </td>
                        </tr>
                    `;
                    return;
                }

                dupData.groups.forEach((group, idx) => {
                    group.files.forEach((filepath, fIdx) => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td><i class="fa-solid fa-copy" style="margin-right: 8px; color: #f59e0b;"></i> ${filepath}</td>
                            <td><code>HASH: ${group.hash.substring(0, 8)}</code></td>
                            <td>${group.size_human}</td>
                            <td style="color: #9ca3af;">Grupo #${idx + 1}</td>
                            <td><span class="badge-target" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b;">Duplicado ${fIdx > 0 ? '(Copia)' : '(Original)'}</span></td>
                        `;
                        filesTableBody.appendChild(tr);
                    });
                });
            } else {
                showToast(json.message, 'error');
            }
        } catch (err) {
            showToast('Error al buscar duplicados.', 'error');
        }
    });

    // Eventos Adicionales
    btnScan.addEventListener('click', scanFolder);
    tableSearch.addEventListener('input', () => {
        if (currentScanData) renderFilesTable(currentScanData.files);
    });

    document.querySelectorAll('input[name="orgMode"]').forEach(radio => {
        radio.addEventListener('change', () => {
            document.querySelectorAll('.mode-option').forEach(opt => opt.classList.remove('active'));
            radio.closest('.mode-option').classList.add('active');
            if (folderPathInput.value) scanFolder();
        });
    });

    // Función Toast
    function showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = 'fa-circle-info';
        if (type === 'success') icon = 'fa-circle-check';
        if (type === 'error') icon = 'fa-circle-exclamation';

        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
});
