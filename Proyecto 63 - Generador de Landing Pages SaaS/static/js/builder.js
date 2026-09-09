document.addEventListener('DOMContentLoaded', () => {
    const iframe = document.getElementById('preview-iframe');
    const form = document.getElementById('landing-builder-form');
    
    const featuresList = document.getElementById('features-list');
    const addFeatureBtn = document.getElementById('btn-add-feature');
    
    const testimonialsList = document.getElementById('testimonials-list');
    const addTestimonialBtn = document.getElementById('btn-add-testimonial');
    
    const saveBtn = document.getElementById('btn-save-landing');
    const templateSelect = document.getElementById('template-select');
    
    // Viewport controls
    const btnDesktop = document.getElementById('vp-desktop');
    const btnTablet = document.getElementById('vp-tablet');
    const btnMobile = document.getElementById('vp-mobile');
    
    if (btnDesktop && btnTablet && btnMobile) {
        btnDesktop.addEventListener('click', () => setViewport('100%', btnDesktop));
        btnTablet.addEventListener('click', () => setViewport('768px', btnTablet));
        btnMobile.addEventListener('click', () => setViewport('375px', btnMobile));
    }
    
    function setViewport(width, activeBtn) {
        if (iframe) {
            iframe.style.width = width;
        }
        [btnDesktop, btnTablet, btnMobile].forEach(btn => btn && btn.classList.remove('active'));
        if (activeBtn) activeBtn.classList.add('active');
    }

    // Dynamic Feature Row Add
    if (addFeatureBtn) {
        addFeatureBtn.addEventListener('click', () => {
            const div = document.createElement('div');
            div.className = 'dynamic-item-card feature-item';
            div.innerHTML = `
                <button type="button" class="btn-remove-item" onclick="this.closest('.dynamic-item-card').remove(); triggerLiveUpdate();">&times;</button>
                <div class="form-group">
                    <input type="text" class="form-input feat-icon" value="fa-bolt" placeholder="Ícone FontAwesome (ex: fa-bolt, fa-shield)">
                </div>
                <div class="form-group">
                    <input type="text" class="form-input feat-title" placeholder="Título do Serviço">
                </div>
                <div class="form-group">
                    <input type="text" class="form-input feat-desc" placeholder="Descrição curta do benefício">
                </div>
            `;
            featuresList.appendChild(div);
            triggerLiveUpdate();
        });
    }

    // Dynamic Testimonial Row Add
    if (addTestimonialBtn) {
        addTestimonialBtn.addEventListener('click', () => {
            const div = document.createElement('div');
            div.className = 'dynamic-item-card testimonial-item';
            div.innerHTML = `
                <button type="button" class="btn-remove-item" onclick="this.closest('.dynamic-item-card').remove(); triggerLiveUpdate();">&times;</button>
                <div class="form-group">
                    <input type="text" class="form-input test-name" placeholder="Nome do Cliente">
                </div>
                <div class="form-group">
                    <input type="text" class="form-input test-role" placeholder="Cargo / Empresa">
                </div>
                <div class="form-group">
                    <textarea class="form-textarea test-comment" placeholder="Comentário ou testemunho"></textarea>
                </div>
            `;
            testimonialsList.appendChild(div);
            triggerLiveUpdate();
        });
    }

    // Color Palette Presets
    window.setColors = function(c1, c2, bg) {
        document.getElementById('primary_color').value = c1;
        document.getElementById('secondary_color').value = c2;
        document.getElementById('bg_color').value = bg;
        triggerLiveUpdate();
    };

    // Gather Form Data
    function getFormData() {
        const title = document.getElementById('title')?.value || 'Minha Landing Page';
        const hero_headline = document.getElementById('hero_headline')?.value || '';
        const hero_subheadline = document.getElementById('hero_subheadline')?.value || '';
        const cta_text = document.getElementById('cta_text')?.value || 'Começar Agora';
        const primary_color = document.getElementById('primary_color')?.value || '#00F5D4';
        const secondary_color = document.getElementById('secondary_color')?.value || '#7000FF';
        const bg_color = document.getElementById('bg_color')?.value || '#0F172A';
        const template_name = templateSelect ? templateSelect.options[templateSelect.selectedIndex].text : 'Custom SaaS';

        const features = [];
        document.querySelectorAll('.feature-item').forEach(el => {
            const icon = el.querySelector('.feat-icon')?.value || 'fa-bolt';
            const t = el.querySelector('.feat-title')?.value || '';
            const d = el.querySelector('.feat-desc')?.value || '';
            if (t || d) {
                features.push({ icon: icon, title: t, desc: d });
            }
        });

        const testimonials = [];
        document.querySelectorAll('.testimonial-item').forEach(el => {
            const name = el.querySelector('.test-name')?.value || '';
            const role = el.querySelector('.test-role')?.value || '';
            const comment = el.querySelector('.test-comment')?.value || '';
            if (name || comment) {
                testimonials.push({ name: name, role: role, comment: comment, rating: 5 });
            }
        });

        return {
            title,
            template_name,
            hero_headline,
            hero_subheadline,
            cta_text,
            primary_color,
            secondary_color,
            bg_color,
            features,
            testimonials
        };
    }

    // Live Update Function
    let updateTimeout;
    window.triggerLiveUpdate = function() {
        clearTimeout(updateTimeout);
        updateTimeout = setTimeout(() => {
            const payload = getFormData();
            fetch('/api/landing/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && iframe) {
                    iframe.srcdoc = data.html_code;
                }
            })
            .catch(err => console.error('Erro na atualização da preview:', err));
        }, 200);
    };

    // Listen to form input changes
    if (form) {
        form.addEventListener('input', window.triggerLiveUpdate);
    }

    // Save Landing Page
    if (saveBtn) {
        saveBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const payload = getFormData();
            
            // Get current iframe html code
            fetch('/api/landing/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(resData => {
                if (resData.success) {
                    payload.html_code = resData.html_code;
                    return fetch('/api/landing/save', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('🎉 ' + data.message);
                    window.location.href = '/history';
                } else {
                    alert('❌ Erro ao guardar: ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro na comunicação com o servidor.'));
        });
    }

    // Load Template Preset Data on Selection
    if (templateSelect) {
        templateSelect.addEventListener('change', () => {
            const selectedOption = templateSelect.options[templateSelect.selectedIndex];
            if (!selectedOption.value) return;

            const tData = JSON.parse(selectedOption.getAttribute('data-json') || '{}');
            if (tData.title) document.getElementById('title').value = tData.title;
            if (tData.hero_headline) document.getElementById('hero_headline').value = tData.hero_headline;
            if (tData.hero_subheadline) document.getElementById('hero_subheadline').value = tData.hero_subheadline;
            if (tData.cta_text) document.getElementById('cta_text').value = tData.cta_text;
            if (tData.primary_color) document.getElementById('primary_color').value = tData.primary_color;
            if (tData.secondary_color) document.getElementById('secondary_color').value = tData.secondary_color;
            if (tData.bg_color) document.getElementById('bg_color').value = tData.bg_color;

            // Load Features
            featuresList.innerHTML = '';
            const feats = tData.features_json ? JSON.parse(tData.features_json) : [];
            feats.forEach(item => {
                const div = document.createElement('div');
                div.className = 'dynamic-item-card feature-item';
                div.innerHTML = `
                    <button type="button" class="btn-remove-item" onclick="this.closest('.dynamic-item-card').remove(); triggerLiveUpdate();">&times;</button>
                    <div class="form-group">
                        <input type="text" class="form-input feat-icon" value="${item.icon || 'fa-bolt'}" placeholder="Ícone FontAwesome">
                    </div>
                    <div class="form-group">
                        <input type="text" class="form-input feat-title" value="${item.title || ''}" placeholder="Título do Serviço">
                    </div>
                    <div class="form-group">
                        <input type="text" class="form-input feat-desc" value="${item.desc || ''}" placeholder="Descrição curta">
                    </div>
                `;
                featuresList.appendChild(div);
            });

            // Load Testimonials
            testimonialsList.innerHTML = '';
            const tests = tData.testimonials_json ? JSON.parse(tData.testimonials_json) : [];
            tests.forEach(item => {
                const div = document.createElement('div');
                div.className = 'dynamic-item-card testimonial-item';
                div.innerHTML = `
                    <button type="button" class="btn-remove-item" onclick="this.closest('.dynamic-item-card').remove(); triggerLiveUpdate();">&times;</button>
                    <div class="form-group">
                        <input type="text" class="form-input test-name" value="${item.name || ''}" placeholder="Nome do Cliente">
                    </div>
                    <div class="form-group">
                        <input type="text" class="form-input test-role" value="${item.role || ''}" placeholder="Cargo / Empresa">
                    </div>
                    <div class="form-group">
                        <textarea class="form-textarea test-comment" placeholder="Comentário">${item.comment || ''}</textarea>
                    </div>
                `;
                testimonialsList.appendChild(div);
            });

            triggerLiveUpdate();
        });
    }

    // Initial Trigger
    triggerLiveUpdate();
});
