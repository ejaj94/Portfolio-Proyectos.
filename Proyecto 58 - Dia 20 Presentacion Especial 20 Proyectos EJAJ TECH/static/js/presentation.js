// EJAJ TECH - DÍA 20 Presentation Interactive JavaScript

let currentSlideIndex = 0;
let slides = [];
let autoPlayInterval = null;
let isPlaying = false;

document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
});

async function loadProjects() {
    try {
        const res = await fetch('/api/projects');
        slides = await res.json();

        if (slides.length > 0) {
            renderCurrentSlide();
            renderThumbnails();
        }
    } catch (err) {
        console.error('Error ao carregar projetos:', err);
    }
}

function renderCurrentSlide() {
    const slide = slides[currentSlideIndex];
    if (!slide) return;

    document.getElementById('slideDayNum').innerText = `DÍA ${slide.day_number}`;
    document.getElementById('slideTitle').innerText = slide.title;
    document.getElementById('slideSubtitle').innerText = slide.subtitle;
    document.getElementById('slideCategory').innerText = slide.category;
    document.getElementById('slideDescription').innerText = slide.description;
    document.getElementById('slideTechStack').innerText = slide.tech_stack;
    document.getElementById('slideImpact').innerText = slide.impact_highlight;

    const badgeEl = document.getElementById('slideBadge');
    if (badgeEl) {
        badgeEl.className = `badge ${slide.badge_color}`;
        badgeEl.innerText = slide.category;
    }

    document.getElementById('slideCounterText').innerText = `Projeto ${currentSlideIndex + 1} de ${slides.length} (Día ${slide.day_number})`;
    
    // Highlight thumbnail
    document.querySelectorAll('.thumb-btn').forEach((btn, idx) => {
        if (idx === currentSlideIndex) {
            btn.style.border = '2px solid var(--purple-accent)';
            btn.style.background = 'rgba(139, 92, 246, 0.2)';
        } else {
            btn.style.border = '1px solid rgba(255, 255, 255, 0.1)';
            btn.style.background = 'rgba(11, 15, 25, 0.7)';
        }
    });
}

function renderThumbnails() {
    const container = document.getElementById('thumbnailsContainer');
    if (!container) return;

    container.innerHTML = '';
    slides.forEach((slide, idx) => {
        const btn = document.createElement('button');
        btn.className = 'thumb-btn';
        btn.style.padding = '0.6rem 1rem';
        btn.style.borderRadius = '10px';
        btn.style.cursor = 'pointer';
        btn.style.color = '#ffffff';
        btn.style.fontWeight = '700';
        btn.style.fontSize = '0.85rem';
        btn.style.transition = 'all 0.2s ease';
        btn.innerHTML = `<span style="color: var(--purple-accent); font-weight: 800;">Día ${slide.day_number}:</span> ${slide.title.split(' ')[0]}`;

        btn.addEventListener('click', () => {
            currentSlideIndex = idx;
            renderCurrentSlide();
        });

        container.appendChild(btn);
    });
}

function nextSlide() {
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    renderCurrentSlide();
}

function prevSlide() {
    currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
    renderCurrentSlide();
}

function toggleAutoPlay() {
    const btn = document.getElementById('btnAutoPlay');
    if (isPlaying) {
        clearInterval(autoPlayInterval);
        isPlaying = false;
        if (btn) btn.innerHTML = '<i class="fa-solid fa-play"></i> Iniciar Apresentação Automática';
    } else {
        autoPlayInterval = setInterval(nextSlide, 4000);
        isPlaying = true;
        if (btn) btn.innerHTML = '<i class="fa-solid fa-pause"></i> Pausar Apresentação';
    }
}
