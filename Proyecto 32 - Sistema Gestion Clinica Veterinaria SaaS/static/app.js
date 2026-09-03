/* VETERINARY PET HOSPITAL — JAVASCRIPT ENGINE */

const i18n = {
    pt: {
        titleVet: "Sistema de Gestão Clínica Veterinária",
        subtitleVet: "Cuidados animais, agendamento de consultas, vacinação e cadastro de tutores.",
        btnNewPet: "Registar Novo Paciente",
        
        kpiTotalPets: "Pacientes Registados",
        kpiConsultations: "Consultas Agendadas",
        kpiVaccines: "Vacinas Pendentes",
        kpiTutores: "Tutores Ativos",
        
        filterAll: "Todos os Animais",
        filterDogs: "Cães 🐕",
        filterCats: "Gatos 🐈",
        filterExotics: "Exóticos 🦜",
        
        secPets: "Galeria de Pacientes & Mascotas",
        secAppointments: "Agendamento de Consultas Médicas",
        secVaccines: "Caderneta & Plano de Vacinação",
        
        thPet: "Mascota",
        thTutor: "Tutor",
        thVet: "Veterinário",
        thReason: "Motivo & Diagnóstico",
        thDateTime: "Data & Hora",
        thStatus: "Estado",
        
        modalTitle: "Registar Novo Paciente Animal",
        modalSubtitle: "Introduza os dados da mascota e do tutor responsável.",
        lblPetName: "Nome do Animal *",
        lblSpecies: "Espécie *",
        lblBreed: "Raça *",
        lblAge: "Idade *",
        lblWeight: "Peso (kg) *",
        lblChip: "Número de Microchip *",
        lblTutorName: "Nome do Tutor *",
        lblContact: "Contacto Telefónico *",
        lblDiagnosis: "Diagnóstico Médico ou Serviço *",
        btnSubmitPet: "Guardar Ficha do Paciente"
    },
    en: {
        titleVet: "Veterinary Clinic & Hospital Suite",
        subtitleVet: "Pet patient care, appointment schedule, vaccination log and pet owner directory.",
        btnNewPet: "Register New Pet Patient",
        
        kpiTotalPets: "Registered Pets",
        kpiConsultations: "Appointments Today",
        kpiVaccines: "Pending Vaccines",
        kpiTutores: "Active Pet Owners",
        
        filterAll: "All Animals",
        filterDogs: "Dogs 🐕",
        filterCats: "Cats 🐈",
        filterExotics: "Exotics 🦜",
        
        secPets: "Pet Patient Gallery",
        secAppointments: "Medical Appointments Schedule",
        secVaccines: "Vaccination Ledger & Health Plan",
        
        thPet: "Pet",
        thTutor: "Pet Owner",
        thVet: "Veterinarian",
        thReason: "Reason & Diagnosis",
        thDateTime: "Date & Time",
        thStatus: "Status",
        
        modalTitle: "Register New Pet Patient",
        modalSubtitle: "Enter pet details and owner contact info.",
        lblPetName: "Pet Name *",
        lblSpecies: "Species *",
        lblBreed: "Breed *",
        lblAge: "Age *",
        lblWeight: "Weight (kg) *",
        lblChip: "Microchip Number *",
        lblTutorName: "Pet Owner Name *",
        lblContact: "Phone Contact *",
        lblDiagnosis: "Medical Diagnosis / Service *",
        btnSubmitPet: "Save Pet Record"
    },
    es: {
        titleVet: "Sistema de Gestión Clínica Veterinaria",
        subtitleVet: "Cuidado animal, programación de citas, vacunación y registro de propietarios.",
        btnNewPet: "Registrar Nuevo Paciente",
        
        kpiTotalPets: "Pacientes Registrados",
        kpiConsultations: "Citas Programadas",
        kpiVaccines: "Vacunas Pendientes",
        kpiTutores: "Propietarios Activos",
        
        filterAll: "Todos los Animales",
        filterDogs: "Perros 🐕",
        filterCats: "Gatos 🐈",
        filterExotics: "Exóticos 🦜",
        
        secPets: "Galería de Pacientes y Mascotas",
        secAppointments: "Agenda de Citas Médicas",
        secVaccines: "Cartilla de Vacunación",
        
        thPet: "Mascota",
        thTutor: "Propietario",
        thVet: "Veterinario",
        thReason: "Motivo y Diagnóstico",
        thDateTime: "Fecha y Hora",
        thStatus: "Estado",
        
        modalTitle: "Registrar Nuevo Paciente Animal",
        modalSubtitle: "Introduzca los datos de la mascota y del propietario.",
        lblPetName: "Nombre de la Mascota *",
        lblSpecies: "Especie *",
        lblBreed: "Raza *",
        lblAge: "Edad *",
        lblWeight: "Peso (kg) *",
        lblChip: "Número de Microchip *",
        lblTutorName: "Nombre del Propietario *",
        lblContact: "Contacto Telefónico *",
        lblDiagnosis: "Diagnóstico Médico o Servicio *",
        btnSubmitPet: "Guardar Ficha de Paciente"
    },
    fr: {
        titleVet: "Gestion de Clinique Vétérinaire",
        subtitleVet: "Soins animaux, rendez-vous médicaux, carnet de vaccination et propriétaires.",
        btnNewPet: "Enregistrer un Patient",
        
        kpiTotalPets: "Animaux Enregistrés",
        kpiConsultations: "Rendez-vous Aujourd'hui",
        kpiVaccines: "Vaccins en Attente",
        kpiTutores: "Propriétaires Actifs",
        
        filterAll: "Tous les Animaux",
        filterDogs: "Chiens 🐕",
        filterCats: "Chats 🐈",
        filterExotics: "Exotiques 🦜",
        
        secPets: "Galerie des Patients",
        secAppointments: "Planning des Rendez-vous",
        secVaccines: "Carnet de Vaccination",
        
        thPet: "Animal",
        thTutor: "Propriétaire",
        thVet: "Vétérinaire",
        thReason: "Motif & Diagnostic",
        thDateTime: "Date & Heure",
        thStatus: "Statut",
        
        modalTitle: "Enregistrer un Patient Animal",
        modalSubtitle: "Saisissez les informations de l'animal et du propriétaire.",
        lblPetName: "Nom de l'Animal *",
        lblSpecies: "Espèce *",
        lblBreed: "Race *",
        lblAge: "Âge *",
        lblWeight: "Poids (kg) *",
        lblChip: "Numéro de Puce *",
        lblTutorName: "Nom du Propriétaire *",
        lblContact: "Téléphone *",
        lblDiagnosis: "Diagnostic Médical ou Service *",
        btnSubmitPet: "Enregistrer le Dossier"
    }
};

let currentLang = 'pt';
let rawMascotasData = [];
let rawCitasData = [];
let rawVacunasData = [];
let activeSpeciesFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchMascotas();
    fetchCitas();
    fetchVacunas();
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
    
    renderPetGallery();
    renderCitasTable();
}

function fetchStats() {
    fetch('/api/stats?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpiTotalPetsVal').innerText = data.total_pacientes;
            document.getElementById('kpiConsultationsVal').innerText = data.consultas_hoje;
            document.getElementById('kpiVaccinesVal').innerText = data.vacunas_pendentes;
            document.getElementById('kpiTutoresVal').innerText = data.tutores_ativos;
        });
}

function fetchMascotas() {
    fetch('/api/mascotas?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawMascotasData = data;
            renderPetGallery();
        });
}

function fetchCitas() {
    fetch('/api/citas?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawCitasData = data;
            renderCitasTable();
        });
}

function fetchVacunas() {
    fetch('/api/vacunas?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
            rawVacunasData = data;
            renderVacunasTable();
        });
}

function setSpeciesFilter(filter) {
    activeSpeciesFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-filter') === filter);
    });
    renderPetGallery();
}

function renderPetGallery() {
    const gallery = document.getElementById('petGalleryContainer');
    const searchVal = document.getElementById('petSearchBox').value.toLowerCase();
    if (!gallery) return;
    gallery.innerHTML = '';
    
    const filtered = rawMascotasData.filter(m => {
        const matchesFilter = activeSpeciesFilter === 'all' || 
            (activeSpeciesFilter === 'cao' && m.especie === 'Cão') ||
            (activeSpeciesFilter === 'gato' && m.especie === 'Gato') ||
            (activeSpeciesFilter === 'exotico' && m.especie === 'Exótico');
            
        const matchesSearch = m.nome.toLowerCase().includes(searchVal) ||
            m.raca.toLowerCase().includes(searchVal) ||
            m.tutor.toLowerCase().includes(searchVal) ||
            (m.diagnostico_servico && m.diagnostico_servico.toLowerCase().includes(searchVal));
            
        return matchesFilter && matchesSearch;
    });

    if (filtered.length === 0) {
        gallery.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-subtle); font-weight: 700;">Nenhum paciente encontrado.</div>`;
        return;
    }

    filtered.forEach(m => {
        let badgeClass = 'species-cao';
        let icon = '<i class="fa-solid fa-dog"></i>';
        if (m.especie === 'Gato') { badgeClass = 'species-gato'; icon = '<i class="fa-solid fa-cat"></i>'; }
        if (m.especie === 'Exótico') { badgeClass = 'species-exotico'; icon = '<i class="fa-solid fa-crow"></i>'; }
        
        const card = document.createElement('div');
        card.className = 'pet-card';
        
        card.innerHTML = `
            <div class="pet-image-container">
                <img src="${m.foto}" alt="${m.nome}" class="pet-card-image">
            </div>
            <div class="pet-card-body">
                <div class="pet-header">
                    <h4 class="pet-name">${m.nome}</h4>
                    <span class="species-badge ${badgeClass}">${icon} ${m.especie}</span>
                </div>
                
                <div class="pet-info">
                    <strong>${m.raca}</strong> • ${m.idade} • ${m.peso}
                </div>
                
                <div style="font-size: 11px; color: var(--text-subtle); font-weight: 700; margin-bottom: 10px;">
                    <i class="fa-solid fa-microchip" style="color: var(--solar-orange);"></i> CHIP: ${m.microchip}
                </div>
                
                <div class="pet-diagnosis-box">
                    <i class="fa-solid fa-stethoscope" style="color: var(--solar-orange-dark);"></i> ${m.diagnostico_servico || 'Serviço: Check-up Clínico Geral'}
                </div>
                
                <div class="pet-tutor-box">
                    <div>
                        <div style="font-size: 10px; text-transform: uppercase; color: var(--text-subtle);">Tutor Responsável</div>
                        <div style="font-weight: 900;">${m.tutor}</div>
                    </div>
                    <a href="tel:${m.contacto}" style="color: var(--solar-orange-dark); font-size: 16px;"><i class="fa-solid fa-phone"></i></a>
                </div>
            </div>
        `;
        gallery.appendChild(card);
    });
}

function renderCitasTable() {
    const tbody = document.getElementById('citasTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawCitasData.forEach(c => {
        let statusStyle = 'background: var(--solar-orange-light); color: var(--solar-orange-dark);';
        if (c.estado === 'Concluída') statusStyle = 'background: var(--accent-emerald-light); color: var(--accent-emerald);';
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span style="font-size: 12px; font-weight: 900; color: var(--solar-orange-dark);">${c.id}</span></td>
            <td style="font-weight: 900;">${c.mascota}</td>
            <td>${c.tutor}</td>
            <td><span style="font-size: 12px; font-weight: 800; color: var(--text-muted);">${c.veterinario}</span></td>
            <td>
                <div style="font-weight: 800;">${c.motivo}</div>
                <div style="font-size: 11px; color: var(--solar-orange-dark); font-weight: 700;">Diagnóstico: ${c.diagnostico_previsto || 'Avaliação Médica'}</div>
            </td>
            <td><i class="fa-regular fa-clock" style="color: var(--solar-orange);"></i> ${c.data} às ${c.hora}</td>
            <td><span style="padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 900; ${statusStyle}">${c.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderVacunasTable() {
    const tbody = document.getElementById('vacunasTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    rawVacunasData.forEach(v => {
        let badgeClass = 'background: var(--accent-emerald-light); color: var(--accent-emerald);';
        if (v.estado === 'Reforço Próximo') badgeClass = 'background: var(--accent-red-light); color: var(--accent-red);';
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 900; font-size: 14px;">${v.mascota}</td>
            <td style="font-weight: 800; color: var(--solar-orange-dark);">${v.vacuna}</td>
            <td>${v.data_aplicacao}</td>
            <td style="font-weight: 900;"><i class="fa-solid fa-syringe" style="color: var(--golden-yellow);"></i> ${v.proxima_dose}</td>
            <td><span style="padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 900; ${badgeClass}">${v.estado}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Modal Form Controller
function openNewPetModal() {
    document.getElementById('newPetModal').classList.add('active');
}

function closeNewPetModal() {
    document.getElementById('newPetModal').classList.remove('active');
}

function submitNewPetForm(event) {
    event.preventDefault();
    
    const newPetData = {
        nome: document.getElementById('petNameInput').value.trim(),
        especie: document.getElementById('petSpeciesSelect').value,
        raca: document.getElementById('petBreedInput').value.trim(),
        idade: document.getElementById('petAgeInput').value.trim(),
        peso: document.getElementById('petWeightInput').value.trim(),
        microchip: document.getElementById('petChipInput').value.trim(),
        tutor: document.getElementById('tutorNameInput').value.trim(),
        contacto: document.getElementById('tutorContactInput').value.trim(),
        diagnostico_servico: document.getElementById('petDiagnosisInput').value.trim() || 'Serviço: Check-up Clínico Geral'
    };
    
    fetch('/api/mascotas/criar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPetData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeNewPetModal();
            fetchMascotas();
            fetchStats();
        }
    });
}
