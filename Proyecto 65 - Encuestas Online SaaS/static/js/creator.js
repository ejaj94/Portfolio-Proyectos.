document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('questions-canvas');
    const inspector = document.getElementById('inspector-panel');
    const saveBtn = document.getElementById('btn-save-survey');
    const titleInput = document.getElementById('survey-title');
    const descInput = document.getElementById('survey-desc');
    const themeInput = document.getElementById('theme-color');

    let activeQuestions = window.INITIAL_QUESTIONS || [];
    let selectedQId = null;

    const typeMeta = {
        'nps': { label: 'Net Promoter Score (0-10)', icon: 'fa-gauge-high' },
        'likert': { label: 'Escala Likert (Concordância)', icon: 'fa-bars-staggered' },
        'choice': { label: 'Escolha Múltipla', icon: 'fa-list-ul' },
        'yesno': { label: 'Sim / Não', icon: 'fa-thumbs-up' },
        'text': { label: 'Texto / Comentário Aberto', icon: 'fa-font' }
    };

    function renderCanvas() {
        if (!canvas) return;
        canvas.innerHTML = '';

        if (activeQuestions.length === 0) {
            canvas.innerHTML = `
                <div style="text-align: center; padding: 4rem 1.5rem; color: var(--text-muted);">
                    <i class="fa-solid fa-square-plus" style="font-size: 3rem; margin-bottom: 1rem; color: var(--primary-emerald);"></i>
                    <h4 style="font-size: 1.1rem; color: white;">Nenhuma pergunta no inquérito</h4>
                    <p style="font-size: 0.9rem;">Adicione perguntas a partir do painel lateral para personalizar o seu inquérito.</p>
                </div>
            `;
            return;
        }

        activeQuestions.forEach((q, index) => {
            const card = document.createElement('div');
            card.className = `survey-card ${selectedQId === q.id ? 'selected' : ''}`;
            card.style.cursor = 'pointer';
            card.style.marginBottom = '1rem';
            card.setAttribute('data-id', q.id);

            const meta = typeMeta[q.type] || { label: q.type, icon: 'fa-question' };

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="background: rgba(16,185,129,0.2); color: var(--primary-emerald); font-size: 0.8rem; font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 20px;">P${index + 1}</span>
                        <strong style="color: white; font-size: 1.05rem;">${q.title || 'Pergunta sem título'}</strong>
                        ${q.required ? '<span style="color: var(--accent-coral); font-weight: 900;">*</span>' : ''}
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;"><i class="fa-solid ${meta.icon}"></i> ${meta.label}</span>
                        <button type="button" style="background: none; border: none; color: var(--accent-coral); cursor: pointer; font-size: 1.1rem;" onclick="event.stopPropagation(); removeQuestion('${q.id}');">&times;</button>
                    </div>
                </div>
                ${q.subtitle ? `<p style="font-size: 0.85rem; color: var(--text-muted);">${q.subtitle}</p>` : ''}
            `;

            card.addEventListener('click', () => selectQuestion(q.id));
            canvas.appendChild(card);
        });
    }

    window.addQuestion = function(type) {
        const id = 'q_' + Date.now();
        const meta = typeMeta[type] || { label: 'Nova Pergunta' };
        const newQ = {
            id: id,
            type: type,
            title: `Nova Pergunta (${meta.label})`,
            subtitle: '',
            required: true
        };

        if (type === 'likert') {
            newQ.options = ['Discordo Totalmente', 'Discordo', 'Neutro', 'Concordo', 'Concordo Totalmente'];
        } else if (type === 'choice') {
            newQ.options = ['Opção A', 'Opção B', 'Opção C'];
        }

        activeQuestions.push(newQ);
        selectQuestion(id);
    };

    window.removeQuestion = function(id) {
        activeQuestions = activeQuestions.filter(q => q.id !== id);
        if (selectedQId === id) {
            selectedQId = null;
            renderInspector();
        }
        renderCanvas();
    };

    function selectQuestion(id) {
        selectedQId = id;
        renderCanvas();
        renderInspector();
    }

    function renderInspector() {
        if (!inspector) return;
        inspector.innerHTML = '';

        const q = activeQuestions.find(item => item.id === selectedQId);

        if (!q) {
            inspector.innerHTML = `
                <div style="text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
                    <i class="fa-solid fa-sliders" style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--primary-emerald);"></i>
                    <h4 style="font-size: 1.05rem; color: white;">Propriedades da Pergunta</h4>
                    <p style="font-size: 0.85rem;">Selecione uma pergunta no centro para editar o seu texto e opções.</p>
                </div>
            `;
            return;
        }

        const meta = typeMeta[q.type] || { label: q.type };

        let optionsHtml = '';
        if (q.type === 'choice' || q.type === 'likert') {
            const opts = q.options || [];
            optionsHtml = `
                <div style="margin-top: 1.25rem;">
                    <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 0.5rem;">Opções de Resposta</label>
                    ${opts.map((opt, i) => `
                        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <input type="text" class="form-input" value="${opt}" oninput="updateOption(${i}, this.value)">
                            <button type="button" class="btn-sm btn-danger" onclick="removeOption(${i})">&times;</button>
                        </div>
                    `).join('')}
                    <button type="button" class="btn-sm btn-secondary" style="width: 100%; margin-top: 0.5rem;" onclick="addOption()">
                        <i class="fa-solid fa-plus"></i> Adicionar Opção
                    </button>
                </div>
            `;
        }

        inspector.innerHTML = `
            <div style="margin-bottom: 1.25rem;">
                <h4 style="font-size: 1.1rem; font-weight: 800; color: white; margin-bottom: 0.25rem;">Editar Pergunta</h4>
                <span class="nps-badge nps-positive">${meta.label}</span>
            </div>

            <div style="margin-bottom: 1rem;">
                <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 0.35rem;">Texto Principal da Pergunta</label>
                <input type="text" id="insp-title" class="form-input" value="${q.title || ''}">
            </div>

            <div style="margin-bottom: 1rem;">
                <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 0.35rem;">Subtítulo / Instrução (Opcional)</label>
                <input type="text" id="insp-subtitle" class="form-input" value="${q.subtitle || ''}">
            </div>

            <div style="display: flex; align-items: center; gap: 0.75rem; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 10px; border: 1px solid var(--border-color);">
                <input type="checkbox" id="insp-required" ${q.required ? 'checked' : ''} style="width: 18px; height: 18px; cursor: pointer;">
                <label for="insp-required" style="font-size: 0.9rem; font-weight: 700; cursor: pointer;">Resposta Obrigatória</label>
            </div>

            ${optionsHtml}
        `;

        document.getElementById('insp-title').addEventListener('input', (e) => {
            q.title = e.target.value;
            renderCanvas();
        });

        document.getElementById('insp-subtitle').addEventListener('input', (e) => {
            q.subtitle = e.target.value;
            renderCanvas();
        });

        document.getElementById('insp-required').addEventListener('change', (e) => {
            q.required = e.target.checked;
            renderCanvas();
        });
    }

    window.updateOption = function(idx, val) {
        const q = activeQuestions.find(item => item.id === selectedQId);
        if (q && q.options) {
            q.options[idx] = val;
        }
    };

    window.addOption = function() {
        const q = activeQuestions.find(item => item.id === selectedQId);
        if (q && q.options) {
            q.options.push(`Opção ${q.options.length + 1}`);
            renderInspector();
        }
    };

    window.removeOption = function(idx) {
        const q = activeQuestions.find(item => item.id === selectedQId);
        if (q && q.options && q.options.length > 1) {
            q.options.splice(idx, 1);
            renderInspector();
        }
    };

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const title = titleInput ? titleInput.value.trim() : '';
            const description = descInput ? descInput.value.trim() : '';
            const theme_color = themeInput ? themeInput.value : '#10B981';

            if (!title) {
                alert('⚠️ Por favor introduza o título do inquérito.');
                return;
            }

            if (activeQuestions.length === 0) {
                alert('⚠️ Adicione pelo menos 1 pergunta ao inquérito.');
                return;
            }

            const payload = {
                id: window.SURVEY_ID || null,
                title: title,
                description: description,
                theme_color: theme_color,
                questions: activeQuestions
            };

            fetch('/api/survey/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('🎉 ' + data.message);
                    window.location.href = '/';
                } else {
                    alert('❌ Erro ao guardar: ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro na comunicação com o servidor.'));
        });
    }

    renderCanvas();
});
