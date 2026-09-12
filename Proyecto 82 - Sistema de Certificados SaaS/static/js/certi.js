// CertiCraft AI SaaS - Shared Frontend JavaScript Logic in pt-PT

// Toast Notification
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
  toast.innerHTML = `<span>${icon}</span> <div>${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Modal Toggle
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
  }
}

// Global Table Search Filter
function filterTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  const filter = input.value.toLowerCase();
  const table = document.getElementById(tableId);
  if (!table) return;

  const trs = table.getElementsByTagName('tr');
  for (let i = 1; i < trs.length; i++) {
    let rowText = trs[i].textContent.toLowerCase();
    if (rowText.includes(filter)) {
      trs[i].style.display = '';
    } else {
      trs[i].style.display = 'none';
    }
  }
}

// Populate Select Dropdowns
async function loadRecipientsSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/recipients');
    const recipients = await res.json();
    select.innerHTML = '<option value="">Selecione o Formando / Destinatário...</option>';
    recipients.forEach(r => {
      select.innerHTML += `<option value="${r.id}">${r.full_name} (${r.organization}) - NIF: ${r.nif}</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar formandos:', err);
  }
}

async function loadTemplatesSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/templates');
    const templates = await res.json();
    select.innerHTML = '<option value="">Selecione o Modelo Visual...</option>';
    templates.forEach(t => {
      select.innerHTML += `<option value="${t.id}">${t.title} (${t.category})</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar modelos:', err);
  }
}

// Common Delete Handler
async function deleteItem(endpoint, id, callback) {
  if (!confirm('Tem a certeza de que deseja eliminar/revogar este registo? Esta ação é irreversível.')) {
    return;
  }
  try {
    const res = await fetch(`${endpoint}/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      if (callback) callback();
    } else {
      showToast(data.message || 'Erro ao eliminar.', 'error');
    }
  } catch (err) {
    showToast('Erro de conexão ao servidor.', 'error');
  }
}

// Export Data
function exportData(fmt) {
  window.location.href = `/api/export/${fmt}`;
  showToast(`Ficheiro de dados ${fmt.toUpperCase()} descarregado com sucesso!`, 'info');
}

// PDF Download Simulation
function downloadPDF(code) {
  showToast(`A compilar documento PDF oficial para o certificado ${code}...`, 'success');
}
