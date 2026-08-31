document.addEventListener('DOMContentLoaded', () => {
    // Default Mock Data for Jobs & Education
    let jobsData = [
        {
            company: "Tech Global Solutions",
            title: "Senior Full-Stack Developer",
            dates: "2022 - Presente",
            desc: "Liderança técnica no desenvolvimento de plataformas web escaláveis em Python/Flask e React. Redução de 40% no tempo de resposta das APIs."
        },
        {
            company: "Inovação Digital Lda",
            title: "Desenvolvedor Web",
            dates: "2019 - 2022",
            desc: "Criação de portais corporativos, sistemas de gestão de bases de dados e integração de microsserviços."
        }
    ];

    let eduData = [
        {
            institution: "Instituto Superior Técnico / Universidade",
            degree: "Mestrado em Engenharia Informática e de Computadores",
            dates: "2017 - 2021",
            desc: "Especialização em Sistemas Distribuídos e Arquitetura de Software."
        }
    ];

    let photoB64 = "";

    // DOM Elements
    const cvForm = document.getElementById('cvForm');
    const txtName = document.getElementById('txtName');
    const txtTitle = document.getElementById('txtTitle');
    const txtEmail = document.getElementById('txtEmail');
    const txtPhone = document.getElementById('txtPhone');
    const txtLocation = document.getElementById('txtLocation');
    const txtWebsite = document.getElementById('txtWebsite');
    const txtSummary = document.getElementById('txtSummary');
    const txtSkills = document.getElementById('txtSkills');
    const txtLanguages = document.getElementById('txtLanguages');

    const inputPhoto = document.getElementById('inputPhoto');
    const imgPhotoPreview = document.getElementById('imgPhotoPreview');
    const btnRemovePhoto = document.getElementById('btnRemovePhoto');

    const jobsListContainer = document.getElementById('jobsListContainer');
    const btnAddJob = document.getElementById('btnAddJob');
    const eduListContainer = document.getElementById('eduListContainer');
    const btnAddEdu = document.getElementById('btnAddEdu');

    // Preview DOM Elements
    const cvPaper = document.getElementById('cvPaper');
    const pvPhoto = document.getElementById('pvPhoto');
    const pvName = document.getElementById('pvName');
    const pvTitle = document.getElementById('pvTitle');
    const pvEmail = document.getElementById('pvEmail');
    const pvPhone = document.getElementById('pvPhone');
    const pvLocation = document.getElementById('pvLocation');
    const pvWebsite = document.getElementById('pvWebsite');
    const pvSummary = document.getElementById('pvSummary');
    const pvJobsList = document.getElementById('pvJobsList');
    const pvEduList = document.getElementById('pvEduList');
    const pvSkillsBadges = document.getElementById('pvSkillsBadges');
    const pvLanguagesText = document.getElementById('pvLanguagesText');

    const btnDownloadPDF = document.getElementById('btnDownloadPDF');
    const hiddenPdfForm = document.getElementById('hiddenPdfForm');
    const hiddenPayload = document.getElementById('hiddenPayload');
    const selCvLanguage = document.getElementById('selCvLanguage');

    // Mobile Tabs
    const tabForm = document.getElementById('tabForm');
    const tabPreview = document.getElementById('tabPreview');
    const editorSection = document.getElementById('editorSection');
    const previewSection = document.getElementById('previewSection');

    // Initialize Mobile View Status
    if (window.innerWidth <= 900) {
        editorSection.classList.add('active-mobile');
    }

    tabForm.addEventListener('click', () => {
        tabForm.classList.add('active');
        tabPreview.classList.remove('active');
        editorSection.classList.add('active-mobile');
        previewSection.classList.remove('active-mobile');
    });

    tabPreview.addEventListener('click', () => {
        tabPreview.classList.add('active');
        tabForm.classList.remove('active');
        previewSection.classList.add('active-mobile');
        editorSection.classList.remove('active-mobile');
    });

    // 1. Theme Switcher
    document.querySelectorAll('input[name="themeChoice"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            const theme = e.target.value;
            cvPaper.className = `cv-paper theme-${theme}`;
            document.querySelectorAll('.tpl-radio').forEach(r => r.classList.remove('active'));
            e.target.closest('.tpl-radio').classList.add('active');
        });
    });

    // 2. Photo Handler
    inputPhoto.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                photoB64 = event.target.result;
                imgPhotoPreview.src = photoB64;
                pvPhoto.src = photoB64;
            };
            reader.readAsDataURL(file);
        }
    });

    btnRemovePhoto.addEventListener('click', () => {
        photoB64 = "";
        const defaultAvatar = `https://ui-avatars.com/api/?name=${encodeURIComponent(txtName.value || 'Enmanuel Jimenez')}&background=4f46e5&color=fff&size=128`;
        imgPhotoPreview.src = defaultAvatar;
        pvPhoto.src = defaultAvatar;
    });

    // 3. Render Dynamic Jobs in Form & Preview
    function renderJobsForm() {
        jobsListContainer.innerHTML = '';
        jobsData.forEach((job, index) => {
            const item = document.createElement('div');
            item.className = 'dynamic-item-card';
            item.innerHTML = `
                <button type="button" class="btn-sm btn-danger btn-remove-item" onclick="removeJob(${index})"><i class="fa-solid fa-xmark"></i></button>
                <div class="input-grid">
                    <div class="form-group">
                        <label>Empresa</label>
                        <input type="text" value="${job.company}" oninput="updateJob(${index}, 'company', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Cargo / Título</label>
                        <input type="text" value="${job.title}" oninput="updateJob(${index}, 'title', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Período / Datas</label>
                        <input type="text" value="${job.dates}" oninput="updateJob(${index}, 'dates', this.value)">
                    </div>
                </div>
                <div class="form-group">
                    <label>Descrição de Realizações</label>
                    <textarea rows="2" oninput="updateJob(${index}, 'desc', this.value)">${job.desc}</textarea>
                </div>
            `;
            jobsListContainer.appendChild(item);
        });
        updateLivePreview();
    }

    window.updateJob = (index, field, val) => {
        jobsData[index][field] = val;
        updateLivePreview();
    };

    window.removeJob = (index) => {
        jobsData.splice(index, 1);
        renderJobsForm();
    };

    btnAddJob.addEventListener('click', () => {
        jobsData.push({ company: "Nova Empresa", title: "Cargo", dates: "2023 - Presente", desc: "Descrição de funções..." });
        renderJobsForm();
    });

    // 4. Render Dynamic Education in Form & Preview
    function renderEduForm() {
        eduListContainer.innerHTML = '';
        eduData.forEach((edu, index) => {
            const item = document.createElement('div');
            item.className = 'dynamic-item-card';
            item.innerHTML = `
                <button type="button" class="btn-sm btn-danger btn-remove-item" onclick="removeEdu(${index})"><i class="fa-solid fa-xmark"></i></button>
                <div class="input-grid">
                    <div class="form-group">
                        <label>Instituição</label>
                        <input type="text" value="${edu.institution}" oninput="updateEdu(${index}, 'institution', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Curso / Graduação</label>
                        <input type="text" value="${edu.degree}" oninput="updateEdu(${index}, 'degree', this.value)">
                    </div>
                    <div class="form-group">
                        <label>Período / Ano</label>
                        <input type="text" value="${edu.dates}" oninput="updateEdu(${index}, 'dates', this.value)">
                    </div>
                </div>
            `;
            eduListContainer.appendChild(item);
        });
        updateLivePreview();
    }

    window.updateEdu = (index, field, val) => {
        eduData[index][field] = val;
        updateLivePreview();
    };

    window.removeEdu = (index) => {
        eduData.splice(index, 1);
        renderEduForm();
    };

    btnAddEdu.addEventListener('click', () => {
        eduData.push({ institution: "Universidade / Escola", degree: "Curso", dates: "2020 - 2023", desc: "" });
        renderEduForm();
    });

    // 5. Update Live CV Preview
    function updateLivePreview() {
        const nameVal = txtName.value.trim() || 'Enmanuel Jimenez';
        pvName.textContent = nameVal;
        pvTitle.textContent = txtTitle.value.trim() || 'Título Profissional';
        pvEmail.innerHTML = `<i class="fa-solid fa-envelope"></i> ${txtEmail.value.trim() || 'enmanuel.jimenez@exemplo.pt'}`;
        pvPhone.innerHTML = `<i class="fa-solid fa-phone"></i> ${txtPhone.value.trim() || '+351 912 345 678'}`;
        pvLocation.innerHTML = `<i class="fa-solid fa-location-dot"></i> ${txtLocation.value.trim() || 'Lisboa, Portugal'}`;

        const webVal = txtWebsite.value.trim();
        pvWebsite.innerHTML = webVal ? `<i class="fa-solid fa-globe"></i> ${webVal}` : '';

        if (!photoB64) {
            const defaultAvatar = `https://ui-avatars.com/api/?name=${encodeURIComponent(nameVal)}&background=4f46e5&color=fff&size=128`;
            pvPhoto.src = defaultAvatar;
        }

        pvSummary.textContent = txtSummary.value.trim() || 'Resumo profissional...';

        // Render Jobs in Preview
        pvJobsList.innerHTML = '';
        jobsData.forEach(j => {
            const div = document.createElement('div');
            div.className = 'pv-entry-item';
            div.innerHTML = `
                <div class="pv-entry-header">
                    <span>${j.title} — <strong>${j.company}</strong></span>
                    <span>${j.dates}</span>
                </div>
                <div class="pv-entry-desc">${j.desc}</div>
            `;
            pvJobsList.appendChild(div);
        });

        // Render Edu in Preview
        pvEduList.innerHTML = '';
        eduData.forEach(e => {
            const div = document.createElement('div');
            div.className = 'pv-entry-item';
            div.innerHTML = `
                <div class="pv-entry-header">
                    <span>${e.degree}</span>
                    <span>${e.dates}</span>
                </div>
                <div class="pv-entry-sub">${e.institution}</div>
            `;
            pvEduList.appendChild(div);
        });

        // Skills Badges
        pvSkillsBadges.innerHTML = '';
        const skillsArr = txtSkills.value.split(',').map(s => s.trim()).filter(s => s);
        skillsArr.forEach(sk => {
            const span = document.createElement('span');
            span.className = 'badge-tag';
            span.textContent = sk;
            pvSkillsBadges.appendChild(span);
        });

        // Languages
        pvLanguagesText.textContent = txtLanguages.value.trim() || 'Nenhum idioma especificado';
    }

    // Attach Input Event Listeners
    [txtName, txtTitle, txtEmail, txtPhone, txtLocation, txtWebsite, txtSummary, txtSkills, txtLanguages].forEach(input => {
        input.addEventListener('input', updateLivePreview);
    });

    // 6. Direct Native PDF Download Handler
    btnDownloadPDF.addEventListener('click', () => {
        const payload = {
            lang: selCvLanguage.value,
            photo_b64: photoB64,
            personal: {
                name: txtName.value.trim() || "Enmanuel Jimenez",
                title: txtTitle.value.trim() || "Engenheiro de Software",
                email: txtEmail.value.trim() || "enmanuel.jimenez@exemplo.pt",
                phone: txtPhone.value.trim() || "+351 912 345 678",
                location: txtLocation.value.trim() || "Lisboa, Portugal",
                website: txtWebsite.value.trim() || "linkedin.com/in/enmanueljimenez",
                summary: txtSummary.value.trim() || "Resumo profissional..."
            },
            experience: jobsData,
            education: eduData,
            skills: txtSkills.value.split(',').map(s => s.trim()).filter(s => s),
            languages: txtLanguages.value.split(',').map(s => s.trim()).filter(s => s)
        };

        hiddenPayload.value = JSON.stringify(payload);
        hiddenPdfForm.submit();
        showToast('A transferir o currículo PDF...', 'success');
    });

    function showToast(msg, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `<i class="fa-solid fa-circle-info"></i> <span>${msg}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }

    // Init Forms & Live Preview
    renderJobsForm();
    renderEduForm();
    updateLivePreview();
});
