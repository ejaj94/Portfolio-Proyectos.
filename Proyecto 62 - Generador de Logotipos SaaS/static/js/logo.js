// EJAJ TECH - LogoCraft AI SaaS Interactive Engine
let currentVariations = [];
let currentModalSvg = '';
let currentModalTitle = 'Logótipo EJAJ TECH';

document.addEventListener('DOMContentLoaded', () => {
    initLogoStudio();
});

function initLogoStudio() {
    const form = document.getElementById('logoGeneratorForm');
    
    // Parse URL params for palette integration (?c1=#FFDE59&c2=#FF6B6B)
    const urlParams = new URLSearchParams(window.location.search);
    const paramC1 = urlParams.get('c1');
    const paramC2 = urlParams.get('c2');
    const paramBrand = urlParams.get('brand');

    if (paramC1 && document.getElementById('primaryColorInput')) {
        document.getElementById('primaryColorInput').value = paramC1;
    }
    if (paramC2 && document.getElementById('secondaryColorInput')) {
        document.getElementById('secondaryColorInput').value = paramC2;
    }
    if (paramBrand && document.getElementById('brandNameInput')) {
        document.getElementById('brandNameInput').value = paramBrand;
    }

    if (!form) return;

    form.addEventListener('submit', generateLogos);
    // Generate initial logos on page load
    generateLogos(null);
}

async function generateLogos(e) {
    if (e && typeof e.preventDefault === 'function') {
        e.preventDefault();
    }

    const brandEl = document.getElementById('brandNameInput');
    const sloganEl = document.getElementById('sloganInput');
    const sectorEl = document.getElementById('sectorInput');
    const styleEl = document.getElementById('styleInput');
    const c1El = document.getElementById('primaryColorInput');
    const c2El = document.getElementById('secondaryColorInput');
    const symbolEl = document.getElementById('symbolInput');

    const brandName = (brandEl ? brandEl.value : 'EJAJ TECH').trim() || 'EJAJ TECH';
    const slogan = (sloganEl ? sloganEl.value : 'Software & Studio').trim() || 'Software & Studio';
    const sector = sectorEl ? sectorEl.value : 'Tecnologia';
    const style = styleEl ? styleEl.value : 'Caricatura 3D';
    const primaryColor = c1El ? c1El.value : '#FFDE59';
    const secondaryColor = c2El ? c2El.value : '#FF6B6B';
    const symbol = symbolEl ? symbolEl.value : 'rocket';

    const variationsGrid = document.getElementById('variationsGrid');
    if (variationsGrid) {
        variationsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3.5rem; background: white; border-radius: 16px; border: 3px dashed var(--border-stroke);">
                <i class="fa-solid fa-paintbrush fa-spin" style="font-size: 3rem; color: var(--cartoon-coral); margin-bottom: 1rem;"></i>
                <h3 style="font-weight: 900; font-size: 1.3rem;">A gerar logótipos animados em vetor...</h3>
                <p style="color: var(--text-muted); font-weight: 600;">A processar 4 variações com cores vibrantes e tipografia 3D.</p>
            </div>
        `;
    }

    try {
        const res = await fetch('/api/logo/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                brand_name: brandName,
                slogan: slogan,
                sector: sector,
                style: style,
                primary_color: primaryColor,
                secondary_color: secondaryColor,
                icon_symbol: symbol
            })
        });

        const data = await res.json();
        if (data.success) {
            currentVariations = data.variations;
            renderVariations(currentVariations, brandName, slogan, sector, style, primaryColor, secondaryColor, symbol);
        } else {
            alert('Erro ao gerar: ' + data.message);
        }
    } catch (err) {
        console.error('Erro de geração:', err);
        if (variationsGrid) {
            variationsGrid.innerHTML = `<div style="grid-column: 1 / -1; color: red; font-weight: 800;">Erro ao conectar com o servidor: ${err.message}</div>`;
        }
    }
}

function renderVariations(variations, brandName, slogan, sector, style, c1, c2, symbol) {
    const grid = document.getElementById('variationsGrid');
    if (!grid) return;

    grid.innerHTML = '';
    variations.forEach((varItem, idx) => {
        const div = document.createElement('div');
        div.className = 'variation-card';
        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span class="badge badge-yellow">${varItem.name}</span>
                <span class="badge badge-cyan">${sector}</span>
            </div>
            <div class="svg-preview-box" onclick="openLogoModal(${idx})" title="Clique para abrir em grande HD">
                ${varItem.svg}
            </div>
            <div style="display: flex; gap: 0.4rem; justify-content: center; flex-wrap: wrap;">
                <button type="button" class="btn btn-coral btn-sm" onclick="saveLogoDesign(${idx}, '${brandName.replace(/'/g, "\\'")}', '${slogan.replace(/'/g, "\\'")}', '${sector}', '${style}', '${c1}', '${c2}', '${symbol}', '${varItem.layout}')">
                    <i class="fa-solid fa-bookmark"></i> Guardar
                </button>
                <button type="button" class="btn btn-cyan btn-sm" onclick="openLogoModal(${idx})">
                    <i class="fa-solid fa-magnifying-glass-plus"></i> Ver HD
                </button>
                <button type="button" class="btn btn-yellow btn-sm" onclick="downloadSvgDirect(${idx})">
                    <i class="fa-solid fa-download"></i> SVG
                </button>
                <button type="button" class="btn btn-pink btn-sm" onclick="downloadPngDirect(${idx})">
                    <i class="fa-solid fa-file-image"></i> PNG HD
                </button>
            </div>
        `;
        grid.appendChild(div);
    });
}

async function saveLogoDesign(idx, brandName, slogan, sector, style, c1, c2, symbol, layout) {
    const svgCode = currentVariations[idx] ? currentVariations[idx].svg : '';

    try {
        const res = await fetch('/api/logo/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                brand_name: brandName,
                slogan: slogan,
                sector: sector,
                style: style,
                primary_color: c1,
                secondary_color: c2,
                icon_symbol: symbol,
                layout_type: layout,
                svg_code: svgCode
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('🎉 ' + data.message);
            window.location.href = `/export/${data.logo_id}`;
        } else {
            alert('Erro ao guardar: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

function downloadSvgDirect(idx) {
    const svgCode = currentVariations[idx] ? currentVariations[idx].svg : '';
    if (!svgCode) return;
    triggerSvgDownload(svgCode, `logotipo_ejajtech_${idx + 1}.svg`);
}

function downloadPngDirect(idx) {
    if (!currentVariations[idx]) return;
    downloadModalPng(currentVariations[idx].svg, currentVariations[idx].name);
}

function triggerSvgDownload(svgContent, filename) {
    const blob = new Blob([svgContent], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'logotipo.svg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function applyPalette(c1, c2) {
    const pInput = document.getElementById('primaryColorInput');
    const sInput = document.getElementById('secondaryColorInput');
    
    if (pInput && sInput) {
        pInput.value = c1;
        sInput.value = c2;
        generateLogos(null);
    } else {
        window.location.href = `/?c1=${encodeURIComponent(c1)}&c2=${encodeURIComponent(c2)}`;
    }
}

/* Modal Zoom Engine */
function openLogoModal(idx, rawSvg, title) {
    const modal = document.getElementById('logoZoomModal');
    const container = document.getElementById('modalSvgContainer');
    const modalTitleEl = document.getElementById('modalTitle');
    if (!modal || !container) return;

    if (typeof idx === 'number' && currentVariations[idx]) {
        currentModalSvg = currentVariations[idx].svg;
        currentModalTitle = currentVariations[idx].name || 'Logótipo EJAJ TECH';
    } else if (rawSvg) {
        currentModalSvg = rawSvg;
        currentModalTitle = title || 'Logótipo Guardado EJAJ TECH';
    } else {
        return;
    }

    if (modalTitleEl) modalTitleEl.innerHTML = `🔍 ${currentModalTitle} (Vista HD)`;
    container.innerHTML = currentModalSvg;
    modal.style.display = 'flex';
}

function closeLogoModal() {
    const modal = document.getElementById('logoZoomModal');
    if (modal) modal.style.display = 'none';
}

function downloadModalSvg() {
    if (!currentModalSvg) return;
    triggerSvgDownload(currentModalSvg, `${currentModalTitle.toLowerCase().replace(/\s+/g, '_')}.svg`);
}

function prepareSvgForPng(rawSvg, targetWidth = 1200, targetHeight = 900) {
    let svg = (rawSvg || '').trim();
    if (!svg) return '';

    if (!svg.includes('xmlns=')) {
        svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
    }

    svg = svg.replace(/width="[^"]*"/gi, `width="${targetWidth}"`);
    svg = svg.replace(/height="[^"]*"/gi, `height="${targetHeight}"`);

    return svg;
}

function fallbackServerPngExport(titleSource) {
    const brandName = document.getElementById('brandNameInput')?.value || 'EJAJ TECH';
    const slogan = document.getElementById('sloganInput')?.value || 'Software de Alta Performance';
    const primaryColor = document.getElementById('primaryColorInput')?.value || '#FFDE59';
    const secondaryColor = document.getElementById('secondaryColorInput')?.value || '#FF6B6B';
    const symbol = document.getElementById('symbolInput')?.value || 'rocket';
    const style = document.getElementById('styleInput')?.value || 'Caricatura 3D';

    const url = `/api/logo/export-png?brand_name=${encodeURIComponent(brandName)}&slogan=${encodeURIComponent(slogan)}&primary_color=${encodeURIComponent(primaryColor)}&secondary_color=${encodeURIComponent(secondaryColor)}&icon_symbol=${encodeURIComponent(symbol)}&style=${encodeURIComponent(style)}`;
    window.location.href = url;
}

function downloadModalPng(customSvg, customTitle) {
    const svgSource = customSvg || currentModalSvg;
    const titleSource = customTitle || currentModalTitle || 'logotipo_ejajtech';

    if (!svgSource) {
        fallbackServerPngExport(titleSource);
        return;
    }

    try {
        const sanitizedSvg = prepareSvgForPng(svgSource, 1200, 900);
        const canvas = document.createElement('canvas');
        canvas.width = 1200;
        canvas.height = 900;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#FFFDF0';
        ctx.fillRect(0, 0, 1200, 900);

        const img = new Image();

        img.onload = function() {
            try {
                ctx.drawImage(img, 0, 0, 1200, 900);
                const pngUrl = canvas.toDataURL('image/png');
                const a = document.createElement('a');
                a.href = pngUrl;
                a.download = `${titleSource.toLowerCase().replace(/[^a-z0-9]+/g, '_')}_hd.png`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } catch (err) {
                console.warn('Canvas export error, invoking server fallback PNG download...', err);
                fallbackServerPngExport(titleSource);
            }
        };

        img.onerror = function(err) {
            console.warn('Client SVG render error, invoking server fallback PNG download...', err);
            fallbackServerPngExport(titleSource);
        };

        const svgBase64 = 'data:image/svg+xml;base64,' + window.btoa(unescape(encodeURIComponent(sanitizedSvg)));
        img.src = svgBase64;
    } catch (err) {
        console.warn('JS PNG export exception, invoking server fallback:', err);
        fallbackServerPngExport(titleSource);
    }
}

function copyModalSvgCode() {
    if (!currentModalSvg) return;
    navigator.clipboard.writeText(currentModalSvg).then(() => {
        const btn = document.getElementById('btnModalCopy');
        if (btn) {
            const oldHtml = btn.innerHTML;
            btn.innerHTML = `<i class="fa-solid fa-check"></i> Copiado!`;
            setTimeout(() => { btn.innerHTML = oldHtml; }, 2000);
        }
    }).catch(err => {
        alert('Erro ao copiar: ' + err);
    });
}

async function deleteSavedLogo(logoId) {
    if (!confirm('Tem a certeza que deseja eliminar este logótipo da galeria?')) return;
    try {
        const res = await fetch(`/api/logo/delete/${logoId}`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            alert('🗑️ ' + data.message);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}

function copyPaletteColors(c1, c2, btn) {
    const text = `Cor Primária: ${c1} | Cor Secundária: ${c2}`;
    navigator.clipboard.writeText(text).then(() => {
        if (btn) {
            const orig = btn.innerText;
            btn.innerText = '✅ Cores Copiadas!';
            setTimeout(() => { btn.innerText = orig; }, 2000);
        }
    });
}
