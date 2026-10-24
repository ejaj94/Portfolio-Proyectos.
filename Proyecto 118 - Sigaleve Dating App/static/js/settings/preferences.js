/**
 * Preferências de descoberta: distância, faixa etária e filtros de opções.
 */
// ── Filtro rápido de opciones para modal-single-select (ej: 100+ idiomas) ──
function filterSingleSelectOptions(query) {
  const list = document.getElementById('modal-select-options-list');
  if (!list) return;
  const q = (query || '').toLowerCase().trim();
  list.querySelectorAll('.single-select-opt').forEach(opt => {
    const txt = opt.textContent.toLowerCase();
    if (!q || txt.includes(q)) {
      opt.style.display = 'flex';
    } else {
      opt.style.display = 'none';
    }
  });
}

// ── Manejo y Persistencia de Slider de Distancia ──
function handleDistanceSliderChange(val) {
  const num = parseInt(val, 10);
  const textEl = document.getElementById('pref-dist-text');
  if (textEl) textEl.textContent = `${num} Km`;
  localStorage.setItem('sigaleve_pref_distance', String(num));
  saveDistancePref(num);
}

let distancePrefTimer = null;
function saveDistancePref(km) {
  clearTimeout(distancePrefTimer);
  distancePrefTimer = setTimeout(async () => {
    try {
      await fetch('/api/v1/profile/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: STATE.currentUser && STATE.currentUser.email,
          max_distance: km
        })
      });
      if (STATE.currentUser) STATE.currentUser.max_distance = km;
    } catch(e){}
  }, 600);
}

// ── Manejo y Persistencia de Slider de Rango de Edad ──
let agePrefTimer = null;
function handleAgeSliderChange() {
  updateAgePrefDisplay();
  const minVal = parseInt(document.getElementById('pref-age-min').value, 10);
  const maxVal = parseInt(document.getElementById('pref-age-max').value, 10);
  const low = Math.min(minVal, maxVal);
  const high = Math.max(minVal, maxVal);
  localStorage.setItem('sigaleve_pref_age_min', String(low));
  localStorage.setItem('sigaleve_pref_age_max', String(high));

  clearTimeout(agePrefTimer);
  agePrefTimer = setTimeout(async () => {
    try {
      await fetch('/api/v1/profile/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: STATE.currentUser && STATE.currentUser.email,
          age_min: low,
          age_max: high
        })
      });
    } catch(e){}
  }, 600);
}

// ── Inicialización de Preferencias de Distancia y Edad en el perfil ──
function initUserPreferencesUI() {
  // Distancia
  const savedDist = localStorage.getItem('sigaleve_pref_distance') ||
    (STATE.currentUser && STATE.currentUser.max_distance) || 50;
  const distSlider = document.getElementById('pref-distance-slider');
  const distText = document.getElementById('pref-dist-text');
  if (distSlider) distSlider.value = savedDist;
  if (distText) distText.textContent = `${savedDist} Km`;

  // Edad
  const savedAgeMin = localStorage.getItem('sigaleve_pref_age_min') || 18;
  const savedAgeMax = localStorage.getItem('sigaleve_pref_age_max') || 70;
  const ageMinSlider = document.getElementById('pref-age-min');
  const ageMaxSlider = document.getElementById('pref-age-max');
  const ageText = document.getElementById('pref-age-text');
  if (ageMinSlider) ageMinSlider.value = savedAgeMin;
  if (ageMaxSlider) ageMaxSlider.value = savedAgeMax;
  if (ageText) ageText.textContent = `${savedAgeMin} - ${savedAgeMax}`;
}

function updateAgePrefDisplay() {
  const minVal = parseInt(document.getElementById('pref-age-min').value, 10);
  const maxVal = parseInt(document.getElementById('pref-age-max').value, 10);
  const low = Math.min(minVal, maxVal);
  const high = Math.max(minVal, maxVal);
  document.getElementById('pref-age-text').textContent = `${low} - ${high}`;
}
