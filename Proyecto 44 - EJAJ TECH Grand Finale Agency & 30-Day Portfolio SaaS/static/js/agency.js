/**
 * EJAJ TECH Grand Finale Agency & 30-Day Portfolio SaaS
 * Client-Side Controller
 */

window.ejajAgency = {
    currentCategory: '',
    searchQuery: '',

    init: function() {
        console.log('[EJAJ TECH] Agência Digital & Desafio 30 Dias Inicializado.');
        this.bindEvents();
    },

    bindEvents: function() {
        const searchInput = document.getElementById('projectSearchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value;
                this.filterProjects();
            });
        }
    },

    selectCategory: function(cat, btn) {
        this.currentCategory = cat;
        document.querySelectorAll('.cat-filter-btn').forEach(b => b.classList.remove('active', 'btn-cyber-primary'));
        document.querySelectorAll('.cat-filter-btn').forEach(b => b.classList.add('btn-cyber-outline'));
        
        btn.classList.remove('btn-cyber-outline');
        btn.classList.add('active', 'btn-cyber-primary');
        
        this.filterProjects();
    },

    filterProjects: function() {
        const url = `/api/projects?q=${encodeURIComponent(this.searchQuery)}&category=${encodeURIComponent(this.currentCategory)}`;
        fetch(url)
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.renderProjectsGrid(data.projects);
                }
            })
            .catch(err => console.error('Erro ao filtrar projetos:', err));
    },

    renderProjectsGrid: function(projects) {
        const grid = document.getElementById('projectsGrid');
        if (!grid) return;

        if (projects.length === 0) {
            grid.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-search text-muted" style="font-size: 3rem;"></i>
                    <h4 class="mt-3 text-muted">Nenhum projeto encontrado para a pesquisa.</h4>
                </div>
            `;
            return;
        }

        grid.innerHTML = projects.map(p => `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="glass-card h-100 p-3 d-flex flex-column justify-content-between position-relative">
                    <div>
                        <div class="position-relative mb-3 overflow-hidden rounded-3" style="height: 190px;">
                            <img src="${p.image_url}" alt="${p.title}" class="w-100 h-100 object-fit-cover">
                            <span class="position-absolute top-0 start-0 m-2 badge badge-day">
                                Dia ${p.day}
                            </span>
                            <span class="position-absolute top-0 end-0 m-2 badge bg-dark text-cyan border border-info">
                                ${p.category}
                            </span>
                        </div>

                        <h5 class="fw-bold text-white mb-2">${p.title}</h5>
                        <p class="text-muted small mb-3">${p.short_desc}</p>
                        
                        <div class="d-flex flex-wrap gap-1 mb-3">
                            ${p.tech_stack.split(',').map(t => `<span class="badge badge-tech">${t.trim()}</span>`).join('')}
                        </div>
                    </div>

                    <div class="pt-3 border-top border-secondary-subtle d-flex justify-content-between align-items-center">
                        <button class="btn btn-sm btn-outline-info rounded-pill px-3" onclick="ejajAgency.openScriptModal(${p.day}, '${this.escapeStr(p.title)}', '${this.escapeStr(p.script_pt)}')">
                            <i class="bi bi-mic-fill me-1"></i>Guião Vídeo
                        </button>
                        <a href="/project/${p.day}" class="btn btn-sm btn-cyber-primary px-3">
                            Ver Projeto <i class="bi bi-arrow-right ms-1"></i>
                        </a>
                    </div>
                </div>
            </div>
        `).join('');
    },

    scrollToDay: function(day) {
        // Highlight day pill
        document.querySelectorAll('.day-pill').forEach(p => p.classList.remove('active'));
        const activePill = document.getElementById(`day-pill-${day}`);
        if (activePill) {
            activePill.classList.add('active');
            activePill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }

        // Search day card or filter
        const dayCard = document.getElementById(`project-card-day-${day}`);
        if (dayCard) {
            dayCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            dayCard.classList.add('border-info');
            setTimeout(() => dayCard.classList.remove('border-info'), 2000);
        }
    },

    openScriptModal: function(day, title, script) {
        document.getElementById('scriptModalTitle').innerText = `Guião do Locutor — Dia ${day}: ${title}`;
        document.getElementById('scriptModalBody').innerText = `"${script}"`;
        const modal = new bootstrap.Modal(document.getElementById('scriptModal'));
        modal.show();
    },

    submitContactForm: function() {
        const name = document.getElementById('contactName').value.trim();
        const email = document.getElementById('contactEmail').value.trim();
        const phone = document.getElementById('contactPhone').value.trim();
        const service = document.getElementById('contactService').value;
        const budget = document.getElementById('contactBudget').value;
        const message = document.getElementById('contactMessage').value.trim();

        if (!name || !email || !message) {
            alert('Por favor preencha o seu nome, e-mail e mensagem.');
            return;
        }

        fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, service, budget, message })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✨ ${data.message}`);
                document.getElementById('contactForm').reset();
            } else {
                alert(`⚠️ ${data.message}`);
            }
        })
        .catch(err => {
            console.error('Erro na submissão:', err);
            alert('Ocorreu um erro ao enviar a mensagem. Tente novamente.');
        });
    },

    escapeStr: function(str) {
        if (!str) return '';
        return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    ejajAgency.init();
});
