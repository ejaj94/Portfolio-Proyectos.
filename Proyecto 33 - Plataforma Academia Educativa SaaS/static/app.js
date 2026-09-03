/* LUMEN CAREER ACADEMY — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleAcademy: "Plataforma de Gestão Académica Enterprise",
        subtitleAcademy: "Programas de licenciatura, cursos profissionais, acompanhamento de alunos, corpo docente e exames.",
        btnNewStudent: "Matricular Novo Aluno",
        
        kpiTotalStudents: "Alunos Matriculados",
        kpiTotalCourses: "Cursos Ativos",
        kpiCompletion: "Taxa de Conclusão",
        kpiGpa: "Média Geral (GPA)",
        kpiFaculty: "Corpo Docente",
        
        secCareers: "Graus Académicos & Carreras Profissionais",
        secCourses: "Catálogo de Cursos & Módulos",
        secStudents: "Diretório de Alunos & Progresso",
        secFaculty: "Corpo Docente & Professores",
        secExams: "Calendário de Exames & Avaliações",
        
        thStudent: "Aluno",
        thMat: "Matrícula",
        thCareer: "Carrera Profissional",
        thProgress: "Progresso Geral",
        thGpa: "Média GPA",
        thStatus: "Estado",
        
        thExam: "Disciplina",
        thType: "Tipo de Avaliação",
        thDate: "Data do Exame",
        thDuration: "Duração",
        thEnrolled: "Inscritos",
        
        modalTitle: "Matricular Novo Aluno na Academia",
        modalSubtitle: "Introduza os dados do aluno e selecione a carrera profissional.",
        lblStudentName: "Nome Completo do Aluno *",
        lblStudentEmail: "Email Académico *",
        lblCareerSelect: "Carrera Profissional *",
        btnSubmitStudent: "Confirmar Matrícula"
    },
    en: {
        titleAcademy: "Enterprise Academic Management Platform",
        subtitleAcademy: "Degree programs, professional courses, student progress tracking, faculty and exam schedule.",
        btnNewStudent: "Enroll New Student",
        
        kpiTotalStudents: "Enrolled Students",
        kpiTotalCourses: "Active Courses",
        kpiCompletion: "Completion Rate",
        kpiGpa: "Average GPA Score",
        kpiFaculty: "Academic Faculty",
        
        secCareers: "Degree Programs & Career Tracks",
        secCourses: "Course Catalog & Modules",
        secStudents: "Student Directory & Progress",
        secFaculty: "Faculty & Professors",
        secExams: "Exam Calendar & Assessments",
        
        thStudent: "Student",
        thMat: "ID Number",
        thCareer: "Career Track",
        thProgress: "Overall Progress",
        thGpa: "GPA Grade",
        thStatus: "Status",
        
        thExam: "Course Subject",
        thType: "Assessment Type",
        thDate: "Exam Date",
        thDuration: "Duration",
        thEnrolled: "Enrolled",
        
        modalTitle: "Enroll New Student into Academy",
        modalSubtitle: "Enter student info and select their degree program.",
        lblStudentName: "Student Full Name *",
        lblStudentEmail: "Academic Email *",
        lblCareerSelect: "Career Track *",
        btnSubmitStudent: "Confirm Enrollment"
    },
    es: {
        titleAcademy: "Plataforma de Gestión Académica Empresarial",
        subtitleAcademy: "Programas de grado, cursos profesionales, seguimiento de alumnos, cuerpo docente y exámenes.",
        btnNewStudent: "Matricular Nuevo Alumno",
        
        kpiTotalStudents: "Alumnos Matriculados",
        kpiTotalCourses: "Cursos Activos",
        kpiCompletion: "Tasa de Finalización",
        kpiGpa: "Promedio General (GPA)",
        kpiFaculty: "Cuerpo Docente",
        
        secCareers: "Carreras Profesionales y Grados",
        secCourses: "Catálogo de Cursos y Módulos",
        secStudents: "Directorio de Alumnos y Progreso",
        secFaculty: "Cuerpo Docente y Profesores",
        secExams: "Calendario de Exámenes y Evaluaciones",
        
        thStudent: "Alumno",
        thMat: "Matrícula",
        thCareer: "Carrera Profesional",
        thProgress: "Progreso General",
        thGpa: "Promedio GPA",
        thStatus: "Estado",
        
        thExam: "Asignatura",
        thType: "Tipo de Evaluación",
        thDate: "Fecha de Examen",
        thDuration: "Duración",
        thEnrolled: "Inscritos",
        
        modalTitle: "Matricular Nuevo Alumno en la Academia",
        modalSubtitle: "Introduzca los datos del estudiante y seleccione su carrera.",
        lblStudentName: "Nombre Completo del Alumno *",
        lblStudentEmail: "Correo Académico *",
        lblCareerSelect: "Carrera Profesional *",
        btnSubmitStudent: "Confirmar Matrícula"
    },
    fr: {
        titleAcademy: "Plateforme de Gestion Académique Enterprise",
        subtitleAcademy: "Programmes de diplôme, cours professionnels, suivi des étudiants, corps professoral et examens.",
        btnNewStudent: "Inscrire un Étudiant",
        
        kpiTotalStudents: "Étudiants Inscrits",
        kpiTotalCourses: "Cours Actifs",
        kpiCompletion: "Taux de Réussite",
        kpiGpa: "Moyenne Générale (GPA)",
        kpiFaculty: "Corps Professoral",
        
        secCareers: "Filières & Programmes Académiques",
        secCourses: "Catalogue des Cours & Modules",
        secStudents: "Répertoire des Étudiants & Progrès",
        secFaculty: "Corps Professoral & Enseignants",
        secExams: "Calendrier des Examens",
        
        thStudent: "Étudiant",
        thMat: "Matricule",
        thCareer: "Filière Académique",
        thProgress: "Progrès Global",
        thGpa: "Moyenne GPA",
        thStatus: "Statut",
        
        thExam: "Matière",
        thType: "Type d'Évaluation",
        thDate: "Date de l'Examen",
        thDuration: "Durée",
        thEnrolled: "Inscrits",
        
        modalTitle: "Inscrire un Nouvel Étudiant",
        modalSubtitle: "Saisissez les informations de l'étudiant et sélectionnez sa filière.",
        lblStudentName: "Nom Complet de l'Étudiant *",
        lblStudentEmail: "Email Académique *",
        lblCareerSelect: "Filière Académique *",
        btnSubmitStudent: "Confirmer l'Inscription"
    }
};

let currentLang = 'pt';
let rawCarrerasData = [];
let rawCursosData = [];
let rawAlunosData = [];
let rawProfesoresData = [];
let rawExamenesData = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchCarreras();
    fetchCursos();
    fetchAlunos();
    fetchProfesores();
    fetchExamenes();
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
    
    renderCarreras();
    renderCursos();
    renderAlunos();
    renderProfesores();
    renderExamenes();
}

function fetchStats() {
    fetch('/api/stats?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiStudentsVal').innerText = data.total_alunos;
            document.getElementById('kpiCoursesVal').innerText = data.total_cursos;
            document.getElementById('kpiCompletionVal').innerText = data.taxa_conclusao;
            document.getElementById('kpiGpaVal').innerText = data.media_gpa;
            document.getElementById('kpiFacultyVal').innerText = data.total_docentes;
        });
}

function fetchCarreras() {
    fetch('/api/carreras?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawCarrerasData = data;
            renderCarreras();
            initCharts();
        });
}

function fetchCursos() {
    fetch('/api/cursos?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawCursosData = data;
            renderCursos();
        });
}

function fetchAlunos() {
    fetch('/api/alunos?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawAlunosData = data;
            renderAlunos();
        });
}

function fetchProfesores() {
    fetch('/api/profesores?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawProfesoresData = data;
            renderProfesores();
        });
}

function fetchExamenes() {
    fetch('/api/examenes?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawExamenesData = data;
            renderExamenes();
        });
}

function renderCarreras() {
    const grid = document.getElementById('carrerasGridContainer');
    if (!grid) return;
    grid.innerHTML = '';
    
    rawCarrerasData.forEach(c => {
        const card = document.createElement('div');
        card.className = 'carrera-card';
        
        card.innerHTML = `
            <div class="carrera-header">
                <span class="carrera-badge">${c.id}</span>
                <span style="font-size: 12px; font-weight: 800; color: var(--text-subtle);"><i class="fa-regular fa-clock"></i> ${c.duracao}</span>
            </div>
            
            <h3 class="carrera-title">${c.nome}</h3>
            <p class="carrera-desc">${c.descricao}</p>
            
            <div class="carrera-footer">
                <div>
                    <div style="font-size: 10px; color: var(--text-subtle); text-transform: uppercase;">Coordenador Docente</div>
                    <div style="font-weight: 900;">${c.coordenador}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 10px; color: var(--text-subtle); text-transform: uppercase;">Alunos Matriculados</div>
                    <div style="font-size: 16px; font-weight: 900; color: var(--jet-black);">${c.alunos_inscritos}</div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderCursos() {
    const grid = document.getElementById('cursosGridContainer');
    if (!grid) return;
    grid.innerHTML = '';
    
    rawCursosData.forEach(crs => {
        const card = document.createElement('div');
        card.className = 'curso-card';
        
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 11px; font-weight: 900; background: var(--bg-hover); padding: 4px 10px; border-radius: 6px;">${crs.codigo}</span>
                <span style="font-size: 12px; font-weight: 900; color: var(--jet-black);">${crs.classificacao}</span>
            </div>
            
            <h4 style="font-family: var(--font-heading); font-size: 17px; font-weight: 900; margin-bottom: 8px; color: var(--jet-black);">${crs.titulo}</h4>
            <div style="font-size: 12px; color: var(--text-subtle); font-weight: 700; margin-bottom: 12px;">
                <i class="fa-solid fa-graduation-cap"></i> ${crs.carrera}
            </div>
            
            <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 800; color: var(--text-dark);">
                <span>Progresso Médio</span>
                <span>${crs.progresso_medio}%</span>
            </div>
            
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: ${crs.progresso_medio}%;"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; color: var(--text-subtle); margin-top: 10px;">
                <span><i class="fa-solid fa-chalkboard-user"></i> ${crs.professor}</span>
                <span><i class="fa-solid fa-users"></i> ${crs.alunos} alunos</span>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderAlunos() {
    const tbody = document.getElementById('alunosTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawAlunosData.forEach(a => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <img src="${a.foto}" alt="${a.nome}" style="width: 38px; height: 38px; border-radius: 10px; object-fit: cover;">
                    <div>
                        <div style="font-weight: 900;">${a.nome}</div>
                        <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700;">${a.email}</div>
                    </div>
                </div>
            </td>
            <td><span style="font-size: 12px; font-weight: 900; background: var(--bg-hover); padding: 4px 8px; border-radius: 6px;">${a.matricula}</span></td>
            <td><span style="font-size: 13px; font-weight: 800;">${a.carrera}</span></td>
            <td style="width: 180px;">
                <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 800; margin-bottom: 4px;">
                    <span>Concluído</span>
                    <span>${a.progresso_geral}%</span>
                </div>
                <div class="progress-bar-bg" style="margin: 0;">
                    <div class="progress-bar-fill" style="width: ${a.progresso_geral}%;"></div>
                </div>
            </td>
            <td><span style="font-weight: 900; font-size: 14px;">${a.media_gpa}</span></td>
            <td><span style="padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: 900; background: var(--jet-black); color: #ffffff;">${a.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderProfesores() {
    const grid = document.getElementById('profesoresGridContainer');
    if (!grid) return;
    grid.innerHTML = '';
    
    rawProfesoresData.forEach(p => {
        const card = document.createElement('div');
        card.className = 'person-card';
        
        card.innerHTML = `
            <div class="person-avatar-container">
                <img src="${p.foto}" alt="${p.nome}" class="person-avatar">
            </div>
            <div class="person-info">
                <h4>${p.nome}</h4>
                <p>${p.titulo}</p>
                <div style="font-size: 11px; font-weight: 900; color: var(--jet-black); margin-top: 6px;">
                    <i class="fa-solid fa-book-bookmark"></i> ${p.cursos_lecionados} Cursos • ${p.avaliacao}
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderExamenes() {
    const tbody = document.getElementById('examenesTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawExamenesData.forEach(ex => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span style="font-size: 12px; font-weight: 900; color: var(--text-subtle);">${ex.id}</span></td>
            <td style="font-weight: 900;">${ex.disciplina}</td>
            <td><span style="font-size: 12px; font-weight: 800; color: var(--text-muted);">${ex.tipo}</span></td>
            <td><i class="fa-regular fa-calendar-check"></i> ${ex.data}</td>
            <td>${ex.duracao}</td>
            <td><span style="font-weight: 900;">${ex.alunos_inscritos} Alunos</span></td>
            <td><span style="padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 900; border: 1.5px solid var(--jet-black);">${ex.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Chart.js Telemetry Initializer
let chartCarreras, chartStatus;

function initCharts() {
    const ctxBar = document.getElementById('carrerasEnrollmentChart');
    if (ctxBar && !chartCarreras) {
        chartCarreras = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: rawCarrerasData.map(c => c.nome.split('&')[0]),
                datasets: [{
                    label: 'Alunos Inscritos',
                    data: rawCarrerasData.map(c => c.alunos_inscritos),
                    backgroundColor: '#09090b',
                    borderRadius: 10
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#e4e4e7' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}

// Modal Controllers
function openNewStudentModal() {
    document.getElementById('newStudentModal').classList.add('active');
}

function closeNewStudentModal() {
    document.getElementById('newStudentModal').classList.remove('active');
}

function submitNewStudentForm(event) {
    event.preventDefault();
    
    const newStudentData = {
        nome: document.getElementById('studentNameInput').value.trim(),
        email: document.getElementById('studentEmailInput').value.trim(),
        carrera: document.getElementById('studentCareerSelect').value
    };
    
    fetch('/api/alunos/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newStudentData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewStudentModal();
            fetchAlunos();
            fetchStats();
        }
    });
}
