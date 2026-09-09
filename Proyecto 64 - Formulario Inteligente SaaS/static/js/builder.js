document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('fields-canvas');
    const inspector = document.getElementById('inspector-panel');
    const saveBtn = document.getElementById('btn-save-form');
    const formTitleInput = document.getElementById('form-title');
    const formDescInput = document.getElementById('form-desc');
    const themeColorInput = document.getElementById('theme-color');

    let activeFields = window.INITIAL_FIELDS || [];
    let selectedFieldId = null;

    // FIELD TYPE LABELS & ICONS
    const typeMeta = {
        'text': { label: 'Texto Curto', icon: 'fa-font' },
        'email': { label: 'E-mail', icon: 'fa-envelope' },
        'phone': { label: 'Telefone', icon: 'fa-phone' },
        'number': { label: 'Número', icon: 'fa-hashtag' },
        'textarea': { label: 'Parágrafo', icon: 'fa-paragraph' },
        'radio': { label: 'Opção Única (Radio)', icon: 'fa-circle-dot' },
        'checkbox': { label: 'Caixas de Seleção', icon: 'fa-square-check' },
        'dropdown': { label: 'Menu Suspenso', icon: 'fa-caret-down' },
        'rating': { label: 'Classificação (Estrelas)', icon: 'fa-star' }
    };

    // Render Canvas Fields
    function renderCanvas() {
        if (!canvas) return;
        canvas.innerHTML = '';

        if (activeFields.length === 0) {
            canvas.innerHTML = `
                <div style="text-align: center; padding: 4rem 1.5rem; color: var(--text-muted);">
                    <i class="fa-solid fa-square-plus" style="font-size: 3rem; margin-bottom: 1rem; color: var(--primary-violet);"></i>
                    <h4 style="font-size: 1.1rem; color: white;">Nenhum campo no formulário</h4>
                    <p style="font-size: 0.9rem;">Clique nos botões do painel esquerdo para adicionar campos ao seu formulário.</p>
                </div>
            `;
            return;
        }

        activeFields.forEach((field, index) => {
            const card = document.createElement('div');
            card.className = `draggable-field-card ${selectedFieldId === field.id ? 'selected' : ''}`;
            card.setAttribute('draggable', 'true');
            card.setAttribute('data-id', field.id);
            card.setAttribute('data-index', index);

            const meta = typeMeta[field.type] || { label: field.type, icon: 'fa-asterisk' };

            card.innerHTML = `
                <div class="field-header">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <i class="fa-solid fa-grip-vertical field-drag-handle" title="Arrastar para reordenar"></i>
                        <span style="font-weight: 800; color: white;">${field.label || 'Campo sem rótulo'}</span>
                        ${field.required ? '<span style="color: var(--accent-coral); font-weight: 900;">*</span>' : ''}
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="field-type-badge"><i class="fa-solid ${meta.icon}"></i> ${meta.label}</span>
                        <button type="button" class="btn-remove-field" style="background: none; border: none; color: var(--accent-coral); cursor: pointer; font-size: 1.1rem;" onclick="event.stopPropagation(); removeField('${field.id}');">&times;</button>
                    </div>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">
                    ${field.placeholder ? `<em>Placeholder: "${field.placeholder}"</em>` : ''}
                </div>
            `;

            card.addEventListener('click', () => selectField(field.id));
            setupDragEvents(card);
            canvas.appendChild(card);
        });
    }

    // HTML5 Drag and Drop Logic
    let draggedIndex = null;

    function setupDragEvents(card) {
        card.addEventListener('dragstart', (e) => {
            draggedIndex = parseInt(card.getAttribute('data-index'));
            card.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });

        card.addEventListener('dragend', () => {
            card.classList.remove('dragging');
            draggedIndex = null;
        });

        card.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });

        card.addEventListener('drop', (e) => {
            e.preventDefault();
            const targetIndex = parseInt(card.getAttribute('data-index'));
            if (draggedIndex !== null && draggedIndex !== targetIndex) {
                const movedItem = activeFields.splice(draggedIndex, 1)[0];
                activeFields.splice(targetIndex, 0, movedItem);
                renderCanvas();
            }
        });
    }

    // Add Field
    window.addField = function(type) {
        const id = 'f_' + Date.now();
        const meta = typeMeta[type] || { label: 'Novo Campo' };
        const newField = {
            id: id,
            type: type,
            label: `Novo Campo (${meta.label})`,
            placeholder: '',
            help: '',
            required: false
        };

        if (['radio', 'checkbox', 'dropdown'].includes(type)) {
            newField.options = ['Opção 1', 'Opção 2', 'Opção 3'];
        }

        activeFields.push(newField);
        selectField(id);
    };

    // Remove Field
    window.removeField = function(id) {
        activeFields = activeFields.filter(f => f.id !== id);
        if (selectedFieldId === id) {
            selectedFieldId = null;
            renderInspector();
        }
        renderCanvas();
    };

    // Select Field
    function selectField(id) {
        selectedFieldId = id;
        renderCanvas();
        renderInspector();
    }

    // Render Inspector Panel for Selected Field
    function renderInspector() {
        if (!inspector) return;
        inspector.innerHTML = '';

        const field = activeFields.find(f => f.id === selectedFieldId);

        if (!field) {
            inspector.innerHTML = `
                <div style="text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
                    <i class="fa-solid fa-arrow-pointer" style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--primary-cyan);"></i>
                    <h4 style="font-size: 1.05rem; color: white;">Propriedades do Campo</h4>
                    <p style="font-size: 0.85rem;">Selecione um campo no centro para editar os seus atributos.</p>
                </div>
            `;
            return;
        }

        const meta = typeMeta[field.type] || { label: field.type };

        let optionsHtml = '';
        if (['radio', 'checkbox', 'dropdown'].includes(field.type)) {
            const opts = field.options || [];
            optionsHtml = `
                <div class="form-group" style="margin-top: 1.25rem;">
                    <label class="form-label" style="font-size: 0.85rem;">Opções de Seleção</label>
                    <div id="inspector-options-list">
                        ${opts.map((opt, i) => `
                            <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
                                <input type="text" class="form-input opt-val" value="${opt}" oninput="updateOption(${i}, this.value)">
                                <button type="button" class="btn-sm btn-danger" onclick="removeOption(${i})">&times;</button>
                            </div>
                        `).join('')}
                    </div>
                    <button type="button" class="btn-sm btn-secondary" style="width: 100%; margin-top: 0.5rem;" onclick="addOption()">
                        <i class="fa-solid fa-plus"></i> Adicionar Opção
                    </button>
                </div>
            `;
        }

        inspector.innerHTML = `
            <div style="margin-bottom: 1.25rem;">
                <h4 style="font-size: 1.1rem; font-weight: 800; color: white; margin-bottom: 0.25rem;">Editar Campo</h4>
                <span class="field-type-badge">${meta.label}</span>
            </div>

            <div class="form-group">
                <label class="form-label" style="font-size: 0.85rem;">Rótulo (Label)</label>
                <input type="text" id="insp-label" class="form-input" value="${field.label || ''}">
            </div>

            <div class="form-group">
                <label class="form-label" style="font-size: 0.85rem;">Texto de Ajuda / Instrução</label>
                <input type="text" id="insp-help" class="form-input" value="${field.help || ''}">
            </div>

            ${['text', 'email', 'phone', 'number', 'textarea'].includes(field.type) ? `
                <div class="form-group">
                    <label class="form-label" style="font-size: 0.85rem;">Placeholder (Exemplo)</label>
                    <input type="text" id="insp-placeholder" class="form-input" value="${field.placeholder || ''}">
                </div>
            ` : ''}

            <div class="form-group" style="display: flex; align-items: center; gap: 0.75rem; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 10px; border: 1px solid var(--border-color);">
                <input type="checkbox" id="insp-required" ${field.required ? 'checked' : ''} style="width: 18px; height: 18px; cursor: pointer;">
                <label for="insp-required" style="font-size: 0.9rem; font-weight: 700; cursor: pointer;">Preenchimento Obrigatório</label>
            </div>

            ${optionsHtml}
        `;

        // Bind inspector input events
        document.getElementById('insp-label').addEventListener('input', (e) => {
            field.label = e.target.value;
            renderCanvas();
        });

        document.getElementById('insp-help').addEventListener('input', (e) => {
            field.help = e.target.value;
        });

        const phInput = document.getElementById('insp-placeholder');
        if (phInput) {
            phInput.addEventListener('input', (e) => {
                field.placeholder = e.target.value;
                renderCanvas();
            });
        }

        document.getElementById('insp-required').addEventListener('change', (e) => {
            field.required = e.target.checked;
            renderCanvas();
        });
    };

    window.updateOption = function(idx, val) {
        const field = activeFields.find(f => f.id === selectedFieldId);
        if (field && field.options) {
            field.options[idx] = val;
        }
    };

    window.addOption = function() {
        const field = activeFields.find(f => f.id === selectedFieldId);
        if (field && field.options) {
            field.options.push(`Opção ${field.options.length + 1}`);
            renderInspector();
        }
    };

    window.removeOption = function(idx) {
        const field = activeFields.find(f => f.id === selectedFieldId);
        if (field && field.options && field.options.length > 1) {
            field.options.splice(idx, 1);
            renderInspector();
        }
    };

    // Save Form Handler
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const title = formTitleInput ? formTitleInput.value.trim() : '';
            const description = formDescInput ? formDescInput.value.trim() : '';
            const theme_color = themeColorInput ? themeColorInput.value : '#8B5CF6';

            if (!title) {
                alert('⚠️ Por favor introduza o título do formulário.');
                return;
            }

            if (activeFields.length === 0) {
                alert('⚠️ Adicione pelo menos 1 campo ao formulário.');
                return;
            }

            const payload = {
                id: window.FORM_ID || null,
                title: title,
                description: description,
                theme_color: theme_color,
                fields: activeFields
            };

            fetch('/api/form/save', {
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

    // Initial render
    renderCanvas();
});
