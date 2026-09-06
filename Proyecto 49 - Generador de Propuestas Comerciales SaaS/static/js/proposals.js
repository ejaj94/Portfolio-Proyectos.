/* 
  EJAJ TECH - Proyecto 49: Generador de Propuestas Comerciales SaaS Engine
  Dynamic Items, Timeline Stepper & Digital Canvas Signature Pad
*/

document.addEventListener('DOMContentLoaded', () => {
  initProposalForm();
  initSignaturePad();
});

// FORM DYNAMIC ITEM & TIMELINE BUILDER
function initProposalForm() {
  const btnAddItem = document.getElementById('btn_add_item');
  if (btnAddItem) {
    btnAddItem.addEventListener('click', addServiceRow);
  }

  const btnAddPhase = document.getElementById('btn_add_phase');
  if (btnAddPhase) {
    btnAddPhase.addEventListener('click', addTimelineRow);
  }

  const vatSelect = document.getElementById('vat_rate');
  if (vatSelect) {
    vatSelect.addEventListener('change', recalculateTotals);
  }
}

function addServiceRow() {
  const tbody = document.getElementById('items_tbody');
  if (!tbody) return;

  const rowCount = tbody.children.length + 1;
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td>
      <input type="text" class="form-control item-title" placeholder="ex: Desenvolvimento Web Frontend" required>
      <input type="text" class="form-control item-desc" placeholder="Descrição detalhada do serviço..." style="margin-top: 4px; font-size: 0.85rem;">
    </td>
    <td style="width: 100px;">
      <input type="number" class="form-control item-qty" value="1" min="1" oninput="recalculateTotals()">
    </td>
    <td style="width: 150px;">
      <input type="number" class="form-control item-price" value="500.00" step="50" min="0" oninput="recalculateTotals()">
    </td>
    <td style="width: 130px; font-weight: 700; text-align: right;" class="item-subtotal">
      € 500,00
    </td>
    <td style="width: 50px; text-align: center;">
      <button type="button" onclick="removeRow(this)" style="background: none; border: none; color: #EF4444; cursor: pointer; font-size: 1rem;">
        <i class="fas fa-trash-alt"></i>
      </button>
    </td>
  `;
  tbody.appendChild(tr);
  recalculateTotals();
}

function addTimelineRow() {
  const container = document.getElementById('timeline_container');
  if (!container) return;

  const count = container.children.length + 1;
  const div = document.createElement('div');
  div.className = 'timeline-step';
  div.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <div style="display: flex; gap: 8px; width: 80%;">
        <input type="text" class="form-control phase-title" value="Fase ${count}: Especificação & Entregáveis" style="font-weight: 700;">
        <input type="text" class="form-control phase-duration" value="Semana ${count}" style="width: 140px; font-weight: 700;">
      </div>
      <button type="button" onclick="this.closest('.timeline-step').remove()" style="background: none; border: none; color: #EF4444; cursor: pointer;">
        <i class="fas fa-trash-alt"></i>
      </button>
    </div>
    <input type="text" class="form-control phase-deliverables" placeholder="Descreva os produtos e objetivos entregues nesta fase..." value="Protótipos aprovados e documentação do projeto.">
  `;
  container.appendChild(div);
}

function removeRow(btn) {
  btn.closest('tr').remove();
  recalculateTotals();
}

function recalculateTotals() {
  let subtotal = 0;
  const rows = document.querySelectorAll('#items_tbody tr');

  rows.forEach(tr => {
    const qty = parseFloat(tr.querySelector('.item-qty')?.value || 1);
    const price = parseFloat(tr.querySelector('.item-price')?.value || 0);
    const tot = qty * price;
    subtotal += tot;

    const subCell = tr.querySelector('.item-subtotal');
    if (subCell) {
      subCell.innerText = formatMoney(tot);
    }
  });

  const vatRate = parseFloat(document.getElementById('vat_rate')?.value || 23);
  const vatAmount = subtotal * (vatRate / 100);
  const total = subtotal + vatAmount;

  setText('out_subtotal', formatMoney(subtotal));
  setText('out_vat', formatMoney(vatAmount));
  setText('out_total', formatMoney(total));
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.innerText = val;
}

function formatMoney(val) {
  return '€ ' + val.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

// SAVE PROPOSAL AJAX
async function submitProposal() {
  const client_name = document.getElementById('client_name')?.value.trim();
  const client_company = document.getElementById('client_company')?.value.trim();
  const client_email = document.getElementById('client_email')?.value.trim();
  const client_phone = document.getElementById('client_phone')?.value.trim();
  const title = document.getElementById('title')?.value.trim();
  const description = document.getElementById('description')?.value.trim();
  const validity_days = parseInt(document.getElementById('validity_days')?.value || 30);
  const vat_rate = parseFloat(document.getElementById('vat_rate')?.value || 23);
  const payment_terms = document.getElementById('payment_terms')?.value.trim();

  if (!client_name || !client_company || !title) {
    alert('Por favor preencha os dados do cliente e o título da proposta.');
    return;
  }

  // Collect items
  const items = [];
  document.querySelectorAll('#items_tbody tr').forEach(tr => {
    const s_title = tr.querySelector('.item-title')?.value.trim();
    const s_desc = tr.querySelector('.item-desc')?.value.trim();
    const qty = parseInt(tr.querySelector('.item-qty')?.value || 1);
    const price = parseFloat(tr.querySelector('.item-price')?.value || 0);
    if (s_title) {
      items.push({ service_title: s_title, description: s_desc, quantity: qty, unit_price: price });
    }
  });

  if (items.length === 0) {
    alert('Por favor adicione pelo menos um item/serviço à proposta.');
    return;
  }

  // Collect timeline
  const timeline = [];
  document.querySelectorAll('#timeline_container .timeline-step').forEach(step => {
    const p_name = step.querySelector('.phase-title')?.value.trim();
    const p_dur = step.querySelector('.phase-duration')?.value.trim();
    const p_del = step.querySelector('.phase-deliverables')?.value.trim();
    if (p_name) {
      timeline.push({ phase_name: p_name, duration_text: p_dur, deliverables: p_del });
    }
  });

  const payload = {
    client_name, client_company, client_email, client_phone,
    title, description, validity_days, vat_rate, payment_terms,
    items, timeline
  };

  try {
    const res = await fetch('/api/proposals/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert('✅ ' + result.message);
      window.location.href = result.url;
    } else {
      alert('❌ Erro: ' + result.message);
    }
  } catch (e) {
    alert('❌ Erro de ligação com o servidor.');
  }
}

// DIGITAL CANVAS SIGNATURE ENGINE
let canvas, ctx, isSigning = false;

function initSignaturePad() {
  canvas = document.getElementById('signatureCanvas');
  if (!canvas) return;

  ctx = canvas.getContext('2d');
  ctx.strokeStyle = '#0F172A';
  ctx.lineWidth = 2.5;
  ctx.lineCap = 'round';

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: clientX - rect.left,
      y: clientY - rect.top
    };
  }

  function startSign(e) {
    isSigning = true;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
  }

  function drawSign(e) {
    if (!isSigning) return;
    e.preventDefault();
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  }

  function stopSign() {
    isSigning = false;
  }

  canvas.addEventListener('mousedown', startSign);
  canvas.addEventListener('mousemove', drawSign);
  canvas.addEventListener('mouseup', stopSign);
  canvas.addEventListener('mouseleave', stopSign);

  canvas.addEventListener('touchstart', startSign);
  canvas.addEventListener('touchmove', drawSign);
  canvas.addEventListener('touchend', stopSign);
}

function clearSignature() {
  if (ctx && canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
}

async function submitSignature(propCode) {
  const signerName = document.getElementById('signed_by_name')?.value.trim();
  if (!signerName) {
    alert('Por favor digite o seu nome para validar a assinatura.');
    return;
  }

  if (!canvas) return;
  const signatureData = canvas.toDataURL('image/png');

  try {
    const res = await fetch('/api/proposals/sign', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: propCode,
        signed_by_name: signerName,
        signature_data: signatureData
      })
    });

    const result = await res.json();
    if (result.success) {
      alert('🎉 ' + result.message);
      location.reload();
    } else {
      alert('❌ Erro: ' + result.message);
    }
  } catch (e) {
    alert('❌ Erro ao enviar a assinatura digital.');
  }
}
