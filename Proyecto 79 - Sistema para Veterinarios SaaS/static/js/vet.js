// VetCraft AI SaaS - Shared Frontend Logic in pt-PT

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

// Global Search Filter for Tables
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

// Populate Owner Select dropdowns
async function loadOwnersSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/owners');
    const owners = await res.json();
    select.innerHTML = '<option value="">Selecione o Proprietário...</option>';
    owners.forEach(o => {
      select.innerHTML += `<option value="${o.id}">${o.name} (NIF: ${o.nif})</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar proprietários:', err);
  }
}

// Populate Pet Select dropdowns
async function loadPetsSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/pets');
    const pets = await res.json();
    select.innerHTML = '<option value="">Selecione o Animal...</option>';
    pets.forEach(p => {
      select.innerHTML += `<option value="${p.id}">${p.name} - ${p.species} (${p.owner_name})</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar animais:', err);
  }
}

// Common Delete Handler
async function deleteItem(endpoint, id, callback) {
  if (!confirm('Tem a certeza de que deseja eliminar este registo? Esta ação é irreversível.')) {
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

// Send Reminder
async function sendReminderAlert(reminderId, callback) {
  try {
    const res = await fetch(`/api/reminders/send/${reminderId}`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      if (callback) callback();
    } else {
      showToast('Erro ao enviar lembrete.', 'error');
    }
  } catch (err) {
    showToast('Erro ao contactar servidor.', 'error');
  }
}

// Export Data
function exportData(fmt) {
  window.location.href = `/api/export/${fmt}`;
  showToast(`Transferência de ficheiro ${fmt.toUpperCase()} iniciada!`, 'info');
}
