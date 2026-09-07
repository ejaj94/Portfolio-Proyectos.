// EJAJ TECH - Work Orders SaaS Interactive JavaScript Handler

document.addEventListener('DOMContentLoaded', () => {
    initSignatureCanvas();
    initMaterialsTable();
});

// Canvas Signature Pad Logic
function initSignatureCanvas() {
    const canvas = document.getElementById('sigCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let hasSigned = false;

    // Set line styles
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#0f172a';

    function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return {
            x: (clientX - rect.left) * (canvas.width / rect.width),
            y: (clientY - rect.top) * (canvas.height / rect.height)
        };
    }

    function startDrawing(e) {
        isDrawing = true;
        hasSigned = true;
        const pos = getPos(e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
        e.preventDefault();
    }

    function draw(e) {
        if (!isDrawing) return;
        const pos = getPos(e);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        e.preventDefault();
    }

    function stopDrawing() {
        isDrawing = false;
    }

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);

    canvas.addEventListener('touchstart', startDrawing, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);

    // Clear Signature
    const clearBtn = document.getElementById('btnClearSignature');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            hasSigned = false;
        });
    }

    // Submit Signature
    const saveBtn = document.getElementById('btnSaveSignature');
    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            const signerName = document.getElementById('signerNameInput')?.value.trim();
            const woCode = saveBtn.dataset.code;

            if (!signerName) {
                alert('Por favor introduza o nome do responsável antes de assinar.');
                return;
            }

            if (!hasSigned) {
                alert('Por favor assine no quadro digital antes de confirmar.');
                return;
            }

            const dataURL = canvas.toDataURL('image/png');

            try {
                const res = await fetch('/api/workorders/sign', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        code: woCode,
                        signature_data: dataURL,
                        signed_by_name: signerName
                    })
                });

                const data = await res.json();
                if (data.success) {
                    alert('Assinatura registada com sucesso! A Ordem foi concluída.');
                    window.location.reload();
                } else {
                    alert('Erro ao guardar assinatura: ' + data.message);
                }
            } catch (err) {
                alert('Erro de conexão: ' + err.message);
            }
        });
    }
}

// Materials Table Row Builder
function initMaterialsTable() {
    const addRowBtn = document.getElementById('btnAddMaterialRow');
    const tbody = document.getElementById('materialsTableBody');

    if (addRowBtn && tbody) {
        addRowBtn.addEventListener('click', () => {
            const tr = document.createElement('tr');
            tr.className = 'material-row';
            tr.innerHTML = `
                <td><input type="text" class="form-control mat-item" placeholder="Ex: Gás Refrigerante, Válvula..." required></td>
                <td><input type="number" class="form-control mat-qty" value="1" min="1" onchange="calcMaterialsTotal()"></td>
                <td><input type="number" class="form-control mat-price" value="0.00" step="0.01" min="0" onchange="calcMaterialsTotal()"></td>
                <td><strong class="mat-subtotal">€0.00</strong></td>
                <td><button type="button" class="btn btn-danger btn-sm" onclick="removeMaterialRow(this)">✕</button></td>
            `;
            tbody.appendChild(tr);
            calcMaterialsTotal();
        });
    }
}

function removeMaterialRow(btn) {
    const row = btn.closest('tr');
    row.remove();
    calcMaterialsTotal();
}

function calcMaterialsTotal() {
    let subtotal = 0;
    const rows = document.querySelectorAll('.material-row');

    rows.forEach(r => {
        const qty = parseFloat(r.querySelector('.mat-qty')?.value || 1);
        const price = parseFloat(r.querySelector('.mat-price')?.value || 0);
        const lineTotal = qty * price;
        const subtotalEl = r.querySelector('.mat-subtotal');
        if (subtotalEl) {
            subtotalEl.innerText = '€' + lineTotal.toFixed(2);
        }
        subtotal += lineTotal;
    });

    const displaySubtotal = document.getElementById('materialsSubtotalDisplay');
    if (displaySubtotal) {
        displaySubtotal.innerText = '€' + subtotal.toFixed(2);
    }
}

// Submit Create Form AJAX
async function submitWorkOrderForm(event) {
    event.preventDefault();

    const clientName = document.getElementById('client_name').value.trim();
    const clientCompany = document.getElementById('client_company').value.trim();
    const clientAddress = document.getElementById('client_address').value.trim();
    const clientPhone = document.getElementById('client_phone').value.trim();
    const technicianName = document.getElementById('technician_name').value;
    const priority = document.getElementById('priority').value;
    const title = document.getElementById('title').value.trim();
    const problemDesc = document.getElementById('problem_description').value.trim();
    const laborHours = parseFloat(document.getElementById('labor_hours').value || 0);
    const laborRate = parseFloat(document.getElementById('labor_rate').value || 35.0);

    const photosText = document.getElementById('photo_urls_text').value.strip ? document.getElementById('photo_urls_text').value.trim() : '';
    let photoUrls = [];
    if (photosText) {
        photoUrls = photosText.split('\n').map(u => u.trim()).filter(u => u.length > 0);
    }

    const materials = [];
    const rows = document.querySelectorAll('.material-row');
    rows.forEach(r => {
        const item = r.querySelector('.mat-item').value.trim();
        const qty = parseInt(r.querySelector('.mat-qty').value || 1);
        const price = parseFloat(r.querySelector('.mat-price').value || 0);
        if (item) {
            materials.push({ item_name: item, quantity: qty, unit_price: price });
        }
    });

    try {
        const res = await fetch('/api/workorders/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_name: clientName,
                client_company: clientCompany,
                client_address: clientAddress,
                client_phone: clientPhone,
                technician_name: technicianName,
                priority: priority,
                title: title,
                problem_description: problemDesc,
                labor_hours: laborHours,
                labor_rate: laborRate,
                materials: materials,
                photo_urls: photoUrls
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('Folha de Serviço criada com sucesso! Código: ' + data.code);
            window.location.href = '/workorder/' + data.code;
        } else {
            alert('Erro ao criar Ordem: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Update Status in Detail View
async function updateOrderStatus(code) {
    const status = document.getElementById('statusSelect').value;
    const notes = document.getElementById('resolutionNotesInput').value.trim();
    const hours = parseFloat(document.getElementById('laborHoursInput').value || 0);
    const rate = parseFloat(document.getElementById('laborRateInput').value || 35.0);
    const tech = document.getElementById('techSelect')?.value;

    try {
        const res = await fetch('/api/workorders/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                status: status,
                resolution_notes: notes,
                labor_hours: hours,
                labor_rate: rate,
                technician_name: tech
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('Ordem atualizada com sucesso!');
            window.location.reload();
        } else {
            alert('Erro ao atualizar: ' + data.message);
        }
    } catch (err) {
        alert('Erro de conexão: ' + err.message);
    }
}

// Quick Add Single Material in Detail View
async function quickAddMaterial(code) {
    const name = prompt('Nome do Material / Peça:');
    if (!name) return;

    const qtyStr = prompt('Quantidade:', '1');
    if (!qtyStr) return;

    const priceStr = prompt('Preço Unitário (€):', '0.00');
    if (!priceStr) return;

    try {
        const res = await fetch('/api/workorders/add_material', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                item_name: name,
                quantity: parseInt(qtyStr),
                unit_price: parseFloat(priceStr)
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('Material adicionado!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}

// Delete Work Order
async function deleteWorkOrder(code) {
    if (!confirm(`Tem a certeza que pretende eliminar a Folha de Serviço ${code}?`)) return;

    try {
        const res = await fetch('/api/workorders/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const data = await res.json();
        if (data.success) {
            alert('Folha de Serviço eliminada.');
            window.location.href = '/workorders';
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}
