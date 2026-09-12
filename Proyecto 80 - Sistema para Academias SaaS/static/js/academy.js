// AcademyCraft AI SaaS - Shared Frontend JavaScript Logic in pt-PT

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
async function loadStudentsSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/students');
    const students = await res.json();
    select.innerHTML = '<option value="">Selecione o Aluno...</option>';
    students.forEach(s => {
      select.innerHTML += `<option value="${s.id}">${s.name} (NIF: ${s.nif})</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar alunos:', err);
  }
}

async function loadTeachersSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/teachers');
    const teachers = await res.json();
    select.innerHTML = '<option value="">Selecione o Professor/Formador...</option>';
    teachers.forEach(t => {
      select.innerHTML += `<option value="${t.id}">${t.name} - ${t.qualification}</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar professores:', err);
  }
}

async function loadCoursesSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/courses');
    const courses = await res.json();
    select.innerHTML = '<option value="">Selecione o Curso...</option>';
    courses.forEach(c => {
      select.innerHTML += `<option value="${c.id}">${c.name} (${c.code}) - ${c.price.toFixed(2)} €</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar cursos:', err);
  }
}

async function loadClassesSelect(selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;
  try {
    const res = await fetch('/api/classes');
    const classes = await res.json();
    select.innerHTML = '<option value="">Selecione a Aula/Sumário...</option>';
    classes.forEach(cl => {
      select.innerHTML += `<option value="${cl.id}">${cl.course_code}: ${cl.title} (${cl.class_date})</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar aulas:', err);
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
      showToast(data.message || 'Erro ao eliminar registo.', 'error');
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
