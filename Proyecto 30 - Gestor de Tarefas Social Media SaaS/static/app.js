/* SOCIAL MEDIA TASK MANAGER — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleAgency: "Gestor de Tarefas Social Media",
        subtitleAgency: "Quadro Kanban de produção de conteúdo, equipa e agendamento de publicações.",
        btnNewTask: "Nova Tarefa",
        
        kpiTotal: "Tarefas no Pipeline",
        kpiProduction: "Em Produção",
        kpiPublished: "Conteúdos Publicados",
        kpiHighPriority: "Alta Prioridade",
        
        colBriefing: "Briefing & Ideias",
        colProduction: "Em Produção",
        colReview: "Em Revisão",
        colPublished: "Publicado / Agendado",
        
        btnMove: "Mover",
        
        modalTitle: "Criar Nova Tarefa de Conteúdo",
        modalSubtitle: "Atribua a tarefa a um membro da equipa de redes sociais.",
        lblTaskTitle: "Título da Tarefa / Post *",
        lblDesc: "Descrição / Briefing *",
        lblPlatform: "Rede Social / Plataforma *",
        lblPriority: "Prioridade *",
        lblAssignee: "Membro da Equipa (Responsável) *",
        lblDueDate: "Data de Publicação *",
        btnSubmitTask: "Guardar Tarefa no Kanban"
    },
    en: {
        titleAgency: "Social Media Task Manager",
        subtitleAgency: "Kanban content workflow, team assignment and social publishing schedule.",
        btnNewTask: "New Task",
        
        kpiTotal: "Tasks in Pipeline",
        kpiProduction: "In Production",
        kpiPublished: "Published Content",
        kpiHighPriority: "High Priority",
        
        colBriefing: "Briefing & Ideas",
        colProduction: "In Production",
        colReview: "In Review",
        colPublished: "Published / Scheduled",
        
        btnMove: "Move",
        
        modalTitle: "Create New Content Task",
        modalSubtitle: "Assign task to a social media team member.",
        lblTaskTitle: "Task / Post Title *",
        lblDesc: "Description / Briefing *",
        lblPlatform: "Social Platform *",
        lblPriority: "Priority *",
        lblAssignee: "Team Member *",
        lblDueDate: "Publish Date *",
        btnSubmitTask: "Save Task in Kanban"
    },
    es: {
        titleAgency: "Gestor de Tareas Social Media",
        subtitleAgency: "Tablero Kanban de producción de contenido, equipo y programación de publicaciones.",
        btnNewTask: "Nueva Tarea",
        
        kpiTotal: "Tareas en Pipeline",
        kpiProduction: "En Producción",
        kpiPublished: "Contenidos Publicados",
        kpiHighPriority: "Alta Prioridad",
        
        colBriefing: "Briefing e Ideas",
        colProduction: "En Producción",
        colReview: "En Revisión",
        colPublished: "Publicado / Programado",
        
        btnMove: "Mover",
        
        modalTitle: "Crear Nueva Tarea de Contenido",
        modalSubtitle: "Asigne la tarea a un miembro del equipo de redes sociales.",
        lblTaskTitle: "Título de la Tarea / Post *",
        lblDesc: "Descripción / Briefing *",
        lblPlatform: "Red Social / Plataforma *",
        lblPriority: "Prioridad *",
        lblAssignee: "Miembro del Equipo *",
        lblDueDate: "Fecha de Publicación *",
        btnSubmitTask: "Guardar Tarea en Kanban"
    },
    fr: {
        titleAgency: "Gestionnaire de Tâches Social Media",
        subtitleAgency: "Tableau Kanban de production de contenu, équipe et calendrier de publication.",
        btnNewTask: "Nouvelle Tâche",
        
        kpiTotal: "Tâches Pipeline",
        kpiProduction: "En Production",
        kpiPublished: "Contenus Publiés",
        kpiHighPriority: "Haute Priorité",
        
        colBriefing: "Briefing & Idées",
        colProduction: "En Production",
        colReview: "En Révision",
        colPublished: "Publié / Programmé",
        
        btnMove: "Déplacer",
        
        modalTitle: "Créer une Tâche de Contenu",
        modalSubtitle: "Attribuez la tâche à un membre de l'équipe social media.",
        lblTaskTitle: "Titre du Post *",
        lblDesc: "Description / Briefing *",
        lblPlatform: "Réseau Social *",
        lblPriority: "Priorité *",
        lblAssignee: "Membre d'Équipe *",
        lblDueDate: "Date de Publication *",
        btnSubmitTask: "Enregistrer dans Kanban"
    }
};

let currentLang = 'pt';
let rawTarefasData = [];
let rawEquipaData = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchEquipa();
    fetchTarefas();
    
    // Set default date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('taskDueDate').value = today;
});

function setLanguage(lang) {
    if (!i18n[lang]) return;
    currentLang = lang;
    
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    
    const dict = i18n[lang];
    document.querySelectorAll('[data-i18n]').forEach(elem => {
        const key = elem.getAttribute('data-i18n');
        if (dict[key]) {
            if (elem.tagName === 'INPUT') {
                elem.placeholder = dict[key];
            } else {
                elem.innerText = dict[key];
            }
        }
    });
    
    renderKanbanBoard();
}

function fetchStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiTotalVal').innerText = data.total_tarefas;
            document.getElementById('kpiProductionVal').innerText = data.em_producao;
            document.getElementById('kpiPublishedVal').innerText = data.publicados;
            document.getElementById('kpiHighPriorityVal').innerText = data.alta_prioridade;
        });
}

function fetchEquipa() {
    fetch('/api/equipa')
        .then(res => res.json())
        .then(data => {
            rawEquipaData = data;
            const select = document.getElementById('taskAssigneeSelect');
            select.innerHTML = '';
            data.forEach(m => {
                select.innerHTML += `<option value="${m.nome}">${m.nome} (${m.cargo})</option>`;
            });
        });
}

function fetchTarefas() {
    fetch('/api/tarefas')
        .then(res => res.json())
        .then(data => {
            rawTarefasData = data;
            renderKanbanBoard();
        });
}

function renderKanbanBoard() {
    const colBriefing = document.getElementById('colBriefingContainer');
    const colProduction = document.getElementById('colProductionContainer');
    const colReview = document.getElementById('colReviewContainer');
    const colPublished = document.getElementById('colPublishedContainer');
    
    colBriefing.innerHTML = '';
    colProduction.innerHTML = '';
    colReview.innerHTML = '';
    colPublished.innerHTML = '';
    
    let cBriefing = 0, cProd = 0, cRev = 0, cPub = 0;
    const filterAssignee = document.getElementById('assigneeFilterSelect').value;
    
    rawTarefasData.forEach(t => {
        if (filterAssignee !== 'all' && t.responsavel !== filterAssignee) return;
        
        const card = document.createElement('div');
        card.className = 'task-card';
        
        let platClass = 'platform-instagram';
        let platIcon = '<i class="fa-brands fa-instagram"></i>';
        
        if (t.plataforma === 'TikTok') { platClass = 'platform-tiktok'; platIcon = '<i class="fa-brands fa-tiktok"></i>'; }
        if (t.plataforma === 'LinkedIn') { platClass = 'platform-linkedin'; platIcon = '<i class="fa-brands fa-linkedin"></i>'; }
        if (t.plataforma === 'YouTube') { platClass = 'platform-youtube'; platIcon = '<i class="fa-brands fa-youtube"></i>'; }
        if (t.plataforma === 'Facebook') { platClass = 'platform-facebook'; platIcon = '<i class="fa-brands fa-facebook"></i>'; }
        
        let priorityColor = '#10b981';
        if (t.prioridade === 'Média') priorityColor = '#f59e0b';
        if (t.prioridade === 'Alta') priorityColor = '#ef4444';
        
        const avatarInitials = t.responsavel.split(' ').map(n => n[0]).join('');
        const dict = i18n[currentLang];
        
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="task-platform-badge ${platClass}">${platIcon} ${t.plataforma}</span>
                <span style="font-size: 10px; font-weight: 900; color: ${priorityColor}; background: var(--bg-hover); padding: 3px 8px; border-radius: 8px;">
                    ${t.prioridade}
                </span>
            </div>
            
            <div class="task-title">${t.titulo}</div>
            <div class="task-desc">${t.descricao}</div>
            
            <div style="font-size: 11px; color: var(--text-subtle); margin-bottom: 12px; font-weight: 700;">
                <i class="fa-regular fa-calendar-check" style="color: var(--primary-indigo);"></i> ${t.data_publicacao}
            </div>
            
            <div class="task-footer">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="assignee-avatar" title="${t.responsavel}">${avatarInitials}</div>
                    <span style="font-size: 11px; font-weight: 800; color: var(--text-muted);">${t.responsavel.split(' ')[0]}</span>
                </div>
                
                ${t.estagio !== 'publicado' ? `
                    <button class="btn-move-stage" onclick="moveTaskStage('${t.id}')">
                        <span>${dict.btnMove || 'Mover'}</span> <i class="fa-solid fa-arrow-right"></i>
                    </button>
                ` : `<span style="font-size: 11px; font-weight: 900; color: var(--accent-emerald);"><i class="fa-solid fa-circle-check"></i> Publicado</span>`}
            </div>
        `;
        
        if (t.estagio === 'briefing') { colBriefing.appendChild(card); cBriefing++; }
        else if (t.estagio === 'producao') { colProduction.appendChild(card); cProd++; }
        else if (t.estagio === 'revisao') { colReview.appendChild(card); cRev++; }
        else if (t.estagio === 'publicado') { colPublished.appendChild(card); cPub++; }
    });
    
    document.getElementById('countBriefing').innerText = cBriefing;
    document.getElementById('countProduction').innerText = cProd;
    document.getElementById('countReview').innerText = cRev;
    document.getElementById('countPublished').innerText = cPub;
}

function moveTaskStage(taskId) {
    fetch(`/api/tarefas/mover/${taskId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                fetchTarefas();
                fetchStats();
            }
        });
}

// Modal Form Controller
function openNewTaskModal() {
    document.getElementById('newTaskModal').classList.add('active');
}

function closeNewTaskModal() {
    document.getElementById('newTaskModal').classList.remove('active');
}

function submitNewTaskForm(event) {
    event.preventDefault();
    
    const newTaskData = {
        titulo: document.getElementById('taskTitleInput').value.trim(),
        descricao: document.getElementById('taskDescInput').value.trim(),
        plataforma: document.getElementById('taskPlatformSelect').value,
        prioridade: document.getElementById('taskPrioritySelect').value,
        responsavel: document.getElementById('taskAssigneeSelect').value,
        data_publicacao: document.getElementById('taskDueDate').value
    };
    
    fetch('/api/tarefas/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTaskData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewTaskModal();
            fetchTarefas();
            fetchStats();
        }
    });
}
