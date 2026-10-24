/**
 * Seletor de localização (países/cidades), indicativos telefónicos e formatação de telemóvel.
 */
// ═══════════════════════════════════════════════════
// BASE DE DATOS GLOBAL DE MÁS DE 100 PAÍSES Y SUS CIUDADES
// ═══════════════════════════════════════════════════
const GLOBAL_LOCATIONS_DATABASE = {
  // ── EUROPA ──
  "Portugal": ["Faro", "Lisboa", "Porto", "Coimbra", "Braga", "Funchal (Madeira)", "Ponta Delgada (Açores)", "Setúbal", "Aveiro", "Évora", "Portimão", "Albufeira", "Cascais", "Sintra", "Viseu", "Guimarães"],
  "España": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia", "Palma de Mallorca", "Las Palmas de Gran Canaria", "Bilbao", "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón", "Granada", "A Coruña", "Santa Cruz de Tenerife", "Salamanca"],
  "Francia": ["París", "Marsella", "Lyon", "Toulouse", "Niza", "Nantes", "Estrasburgo", "Montpellier", "Burdeos", "Lille", "Rennes", "Reims"],
  "Alemania": ["Berlín", "Múnich", "Fráncfort", "Hamburgo", "Colonia", "Stuttgart", "Düsseldorf", "Leipzig", "Dresde", "Núremberg", "Hannover", "Bremen"],
  "Italia": ["Roma", "Milán", "Nápoles", "Turín", "Palermo", "Florencia", "Bolonia", "Venecia", "Génova", "Verona", "Bari", "Catania"],
  "Reino Unido": ["Londres", "Manchester", "Birmingham", "Edimburgo", "Glasgow", "Liverpool", "Bristol", "Leeds", "Belfast", "Cardiff", "Newcastle", "Sheffield"],
  "Irlanda": ["Dublín", "Cork", "Galway", "Limerick", "Waterford", "Drogheda"],
  "Países Bajos": ["Ámsterdam", "Róterdam", "La Haya", "Utrecht", "Eindhoven", "Groninga", "Tilburgo", "Breda"],
  "Bélgica": ["Bruselas", "Amberes", "Gante", "Lieja", "Brujas", "Namur", "Lovaina"],
  "Suiza": ["Zúrich", "Ginebra", "Basilea", "Berna", "Lausana", "Lucerna", "San Galo", "Lugano"],
  "Austria": ["Viena", "Graz", "Linz", "Salzburgo", "Innsbruck", "Klagenfurt"],
  "Suecia": ["Estocolmo", "Gotemburgo", "Malmö", "Upsala", "Västerås", "Örebro"],
  "Noruega": ["Oslo", "Bergen", "Trondheim", "Stavanger", "Drammen", "Tromsø"],
  "Dinamarca": ["Copenhague", "Aarhus", "Odense", "Aalborg", "Esbjerg"],
  "Finlandia": ["Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu", "Turku"],
  "Polonia": ["Varsovia", "Cracovia", "Lodz", "Breslavia", "Poznan", "Gdansk", "Szczecin"],
  "República Checa": ["Praga", "Brno", "Ostrava", "Pilsen", "Liberec", "Olomouc"],
  "Grecia": ["Atenas", "Salónica", "Patras", "Heraclión", "Larisa", "Volos", "Rodas"],
  "Rumanía": ["Bucarest", "Cluj-Napoca", "Timisoara", "Iasi", "Constanta", "Craiova", "Brasov"],
  "Hungría": ["Budapest", "Debrecen", "Szeged", "Miskolc", "Pécs", "Gyor"],
  "Croacia": ["Zagreb", "Split", "Rijeka", "Osijek", "Zadar", "Dubrovnik"],
  "Bulgaria": ["Sofía", "Plovdiv", "Varna", "Burgas", "Ruse"],
  "Eslovaquia": ["Bratislava", "Kosice", "Presov", "Zilina", "Nitra"],
  "Eslovenia": ["Liubliana", "Maribor", "Kranj", "Celje", "Koper"],
  "Serbia": ["Belgrado", "Novi Sad", "Nis", "Kragujevac", "Subotica"],
  "Ucrania": ["Kiev", "Leópolis", "Odesa", "Járkov", "Dnipró", "Zaporiyia"],
  "Lituania": ["Vilna", "Kaunas", "Klaipeda", "Siauliai", "Panevezys"],
  "Letonia": ["Riga", "Daugavpils", "Liepaja", "Jelgava", "Jurmala"],
  "Estonia": ["Tallin", "Tartu", "Narva", "Pärnu"],
  "Islandia": ["Reikiavik", "Kópavogur", "Hafnarfjörður", "Akureyri"],
  "Luxemburgo": ["Ciudad de Luxemburgo", "Esch-sur-Alzette", "Differdange", "Dudelange"],
  "Malta": ["La Valeta", "Sliema", "San Julián", "Birkirkara", "Mosta"],
  "Andorra": ["Andorra la Vella", "Escaldes-Engordany", "Encamp"],
  "Chipre": ["Nicosia", "Limasol", "Lárnaca", "Pafos", "Famagusta"],
  "Mónaco": ["Mónaco", "Montecarlo", "La Condamine"],

  // ── AMÉRICA LATINA Y EL CARIBE ──
  "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Cancún", "Mérida", "Querétaro", "León", "Juárez", "Playa del Carmen", "San Luis Potosí", "Toluca", "Aguascalientes", "Hermosillo"],
  "Colombia": ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena de Indias", "Bucaramanga", "Pereira", "Santa Marta", "Manizales", "Cúcuta", "Ibagué", "Villavicencio", "Pasto", "Armenia"],
  "Argentina": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata", "Mar del Plata", "San Miguel de Tucumán", "Salta", "Santa Fe", "Bariloche", "Neuquén", "San Juan", "Resistencia", "Corrientes"],
  "Brasil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", "Curitiba", "Recife", "Porto Alegre", "Florianópolis", "Manaus", "Goiânia", "Belém", "Campinas", "Vitória"],
  "Chile": ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", "Temuco", "Viña del Mar", "Iquique", "Rancagua", "Puerto Montt", "Talca", "Arica"],
  "Perú": ["Lima", "Arequipa", "Trujillo", "Cusco", "Chiclayo", "Piura", "Iquitos", "Huancayo", "Tacna", "Pucallpa", "Cajamarca"],
  "Venezuela": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto", "Maracay", "Ciudad Guayana", "San Cristóbal", "Mérida", "Puerto La Cruz", "Cumaná", "Maturín"],
  "Ecuador": ["Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Ambato", "Manta", "Portoviejo", "Machala", "Loja", "Esmeraldas"],
  "Uruguay": ["Montevideo", "Punta del Este", "Salto", "Ciudad de la Costa", "Paysandú", "Maldonado", "Rivera", "Tacuarembó"],
  "Paraguay": ["Asunción", "Ciudad del Este", "San Lorenzo", "Luque", "Capiatá", "Encarnación"],
  "Bolivia": ["La Paz", "Santa Cruz de la Sierra", "Cochabamba", "Sucre", "Oruro", "Tarija", "Potosí"],
  "República Dominicana": ["Santo Domingo", "Santiago de los Caballeros", "Punta Cana", "La Romana", "Puerto Plata", "San Pedro de Macorís", "Higüey"],
  "Cuba": ["La Habana", "Santiago de Cuba", "Camagüey", "Holguín", "Santa Clara", "Varadero", "Cienfuegos"],
  "Costa Rica": ["San José", "Alajuela", "Cartago", "Heredia", "Liberia", "Puntarenas"],
  "Panamá": ["Ciudad de Panamá", "San Miguelito", "David", "Colón", "La Chorrera", "Santiago"],
  "Guatemala": ["Ciudad de Guatemala", "Mixco", "Villa Nueva", "Quetzaltenango", "Antigua Guatemala", "Escuintla"],
  "Honduras": ["Tegucigalpa", "San Pedro Sula", "Choloma", "La Ceiba", "El Progreso", "Roatán"],
  "El Salvador": ["San Salvador", "Santa Ana", "San Miguel", "Soyapango", "Santa Tecla"],
  "Nicaragua": ["Managua", "León", "Masaya", "Matagalpa", "Chinandega", "Granada"],
  "Puerto Rico": ["San Juan", "Bayamón", "Carolina", "Ponce", "Caguas", "Mayagüez"],

  // ── AMÉRICA DEL NORTE ──
  "Estados Unidos": ["Nueva York, NY", "Los Ángeles, CA", "Miami, FL", "Chicago, IL", "Houston, TX", "San Francisco, CA", "Las Vegas, NV", "Orlando, FL", "Dallas, TX", "Austin, TX", "Seattle, WA", "Boston, MA", "Atlanta, GA", "Washington D.C.", "Denver, CO", "Filadelfia, PA", "San Diego, CA", "Phoenix, AZ"],
  "Canadá": ["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa", "Quebec", "Edmonton", "Winnipeg", "Halifax", "Victoria"],

  // ── ÁFRICA ──
  "Angola": ["Luanda", "Benguela", "Huambo", "Lubango", "Cabinda", "Malanje", "Lobito", "Soyo"],
  "Mozambique": ["Maputo", "Matola", "Beira", "Nampula", "Chimoio", "Quelimane", "Tete", "Pemba"],
  "Cabo Verde": ["Praia (Santiago)", "Mindelo (São Vicente)", "Santa Maria (Sal)", "Espargos", "Assomada", "Tarrafal"],
  "Guinea Ecuatorial": ["Malabo", "Bata", "Ebebiyín", "Mongomo", "Aconibe"],
  "Santo Tomé y Príncipe": ["Santo Tomé", "Trindade", "Santana", "Neves"],
  "Sudáfrica": ["Johannesburgo", "Ciudad del Cabo", "Durban", "Pretoria", "Port Elizabeth", "Bloemfontein"],
  "Nigeria": ["Lagos", "Abuya", "Ibadán", "Kano", "Port Harcourt", "Benin City"],
  "Marruecos": ["Casablanca", "Rabat", "Marrakech", "Tánger", "Fez", "Agadir", "Meknes"],
  "Egipto": ["El Cairo", "Alejandría", "Guiza", "Sharm el-Sheij", "Hurgada", "Lúxor"],
  "Kenia": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"],
  "Ghana": ["Acra", "Kumasi", "Tamale", "Sekondi-Takoradi", "Cape Coast"],
  "Senegal": ["Dakar", "Touba", "Thiès", "Saint-Louis", "Ziguinchor"],
  "Costa de Marfil": ["Abiyán", "Bouaké", "Daloa", "Yamoussoukro", "San Pedro"],
  "Túnez": ["Túnez", "Sfax", "Susa", "Kairuán", "Bizerta"],
  "Argelia": ["Argel", "Orán", "Constantina", "Annaba", "Blida"],
  "Etiopía": ["Adís Abeba", "Dire Dawa", "Hawassa", "Bahir Dar"],
  "Tanzania": ["Dar es-Salam", "Dodoma", "Mwanza", "Arusha", "Zanzíbar"],
  "Camerún": ["Duala", "Yaundé", "Bamenda", "Bafoussam", "Garua"],
  "Uganda": ["Kampala", "Entebbe", "Gulu", "Jinja", "Mbarara"],
  "Namibia": ["Windhoek", "Walvis Bay", "Swakopmund", "Henties Bay"],
  "Zimbabue": ["Harare", "Bulawayo", "Chitungwiza", "Mutare", "Victoria Falls"],

  // ── ASIA Y MEDIO ORIENTE ──
  "Japón": ["Tokio", "Osaka", "Kioto", "Yokohama", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Hiroshima"],
  "China": ["Pekín", "Shanghái", "Cantón (Guangzhou)", "Shenzhen", "Chengdu", "Hangzhou", "Wuhan", "Hong Kong", "Macao"],
  "Corea del Sur": ["Seúl", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju"],
  "India": ["Nueva Delhi", "Bombay (Mumbai)", "Bangalore", "Hyderabad", "Chennai", "Calcuta", "Pune", "Jaipur"],
  "Emiratos Árabes Unidos": ["Dubái", "Abu Dabi", "Sharjah", "Ajmán", "Ras al-Jaima"],
  "Turquía": ["Estambul", "Ankara", "Esmirna", "Antalya", "Bursa", "Bodrum"],
  "Tailandia": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Krabi", "Hua Hin"],
  "Singapur": ["Singapur", "Sentosa", "Jurong"],
  "Indonesia": ["Yakarta", "Bali (Denpasar)", "Surabaya", "Bandung", "Medan"],
  "Filipinas": ["Manila", "Ciudad Quezón", "Cebú", "Dávao", "Makati"],
  "Malasia": ["Kuala Lumpur", "George Town (Penang)", "Johor Bahru", "Ipoh", "Malaca"],
  "Vietnam": ["Ciudad Ho Chi Minh", "Hanói", "Da Nang", "Nha Trang", "Hai Phong"],
  "Arabia Saudita": ["Riad", "Yeda", "La Meca", "Medina", "Dammam"],
  "Qatar": ["Doha", "Al Wakrah", "Al Khor", "Lusail"],
  "Israel": ["Tel Aviv", "Jerusalén", "Haifa", "Rishon LeZion", "Beerseba"],

  // ── OCEANÍA ──
  "Australia": ["Sídney", "Melbourne", "Brisbane", "Perth", "Adelaida", "Gold Coast", "Canberra"],
  "Nueva Zelanda": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Queenstown"]
};

// Variables de estado del Selector de Ubicación
let locSelectedCountry = 'Portugal';
let locSelectedCity = 'Faro';
let locActiveTab = 'countries';

function openLocationPicker() {
  const currentLocText = document.getElementById('drawer-pref-location')?.textContent || '';
  
  // Extraer país y ciudad actual si existen
  let foundCountry = 'Portugal';
  let foundCity = 'Faro';

  for (const c of Object.keys(GLOBAL_LOCATIONS_DATABASE)) {
    if (currentLocText.toLowerCase().includes(c.toLowerCase())) {
      foundCountry = c;
      const cities = GLOBAL_LOCATIONS_DATABASE[c];
      for (const ct of cities) {
        if (currentLocText.toLowerCase().includes(ct.toLowerCase())) {
          foundCity = ct;
          break;
        }
      }
      break;
    }
  }

  locSelectedCountry = foundCountry;
  locSelectedCity = foundCity;

  updateLocationSummary();

  const searchInp = document.getElementById('loc-search-input');
  if (searchInp) searchInp.value = '';

  switchLocationTab('countries');

  const m = document.getElementById('modal-location-picker');
  if (m) m.classList.remove('hidden');
}

function switchLocationTab(tab) {
  locActiveTab = tab;
  const tabCountries = document.getElementById('loc-tab-countries');
  const tabCities = document.getElementById('loc-tab-cities');
  const viewCountries = document.getElementById('loc-view-countries');
  const viewCities = document.getElementById('loc-view-cities');
  const searchInp = document.getElementById('loc-search-input');
  if (searchInp) searchInp.value = '';

  if (tab === 'countries') {
    if (tabCountries) {
      tabCountries.className = 'flex-1 py-2 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-1.5 bg-zinc-800 text-white shadow';
    }
    if (tabCities) {
      tabCities.className = 'flex-1 py-2 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-1.5 text-zinc-400 hover:text-zinc-200';
    }
    if (viewCountries) viewCountries.classList.remove('hidden');
    if (viewCities) viewCities.classList.add('hidden');
    renderCountriesList();
  } else {
    if (tabCountries) {
      tabCountries.className = 'flex-1 py-2 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-1.5 text-zinc-400 hover:text-zinc-200';
    }
    if (tabCities) {
      tabCities.className = 'flex-1 py-2 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-1.5 bg-zinc-800 text-white shadow';
    }
    if (viewCountries) viewCountries.classList.add('hidden');
    if (viewCities) viewCities.classList.remove('hidden');
    renderCitiesList();
  }
}

function renderCountriesList(query = '') {
  const container = document.getElementById('loc-view-countries');
  if (!container) return;
  container.innerHTML = '';

  const q = query.toLowerCase().trim();
  const allCountries = Object.keys(GLOBAL_LOCATIONS_DATABASE);
  const filtered = q ? allCountries.filter(c => c.toLowerCase().includes(q)) : allCountries;

  if (filtered.length === 0) {
    container.innerHTML = `<div class="p-6 text-center text-xs text-zinc-500">Ningún país coincide con "${query}"</div>`;
    return;
  }

  filtered.forEach(country => {
    const isSelected = (country === locSelectedCountry);
    const citiesCount = (GLOBAL_LOCATIONS_DATABASE[country] || []).length;
    const item = document.createElement('div');
    item.className = `flex items-center justify-between p-3 rounded-2xl cursor-pointer transition-all border select-none ${isSelected ? 'border-purple-500 bg-purple-500/15' : 'border-zinc-850 bg-zinc-900/60 hover:bg-zinc-850 hover:border-zinc-700'}`;
    
    item.onclick = function() {
      locSelectedCountry = country;
      // Pre-seleccionar la primera ciudad del país
      const cities = GLOBAL_LOCATIONS_DATABASE[country] || ["Capital / Centro"];
      locSelectedCity = cities[0];
      updateLocationSummary();

      // Pasar automáticamente a la pestaña de ciudades para que elija la ciudad
      switchLocationTab('cities');
    };

    item.innerHTML = `
      <div class="flex items-center gap-2.5">
        <i class="fa-solid fa-earth-americas text-xs ${isSelected ? 'text-purple-400' : 'text-zinc-500'}"></i>
        <span class="text-xs font-bold ${isSelected ? 'text-white' : 'text-zinc-300'}">${country}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-[10px] text-zinc-500 font-semibold">${citiesCount} cidades</span>
        <div class="${isSelected ? '' : 'hidden'} text-purple-400 font-black">
          <i class="fa-solid fa-check text-xs"></i>
        </div>
      </div>
    `;
    container.appendChild(item);
  });
}

function renderCitiesList(query = '') {
  const container = document.getElementById('loc-view-cities');
  if (!container) return;
  container.innerHTML = '';

  const q = query.toLowerCase().trim();
  const allCities = GLOBAL_LOCATIONS_DATABASE[locSelectedCountry] || ["Capital / Centro"];
  const filtered = q ? allCities.filter(ct => ct.toLowerCase().includes(q)) : allCities;

  if (filtered.length === 0) {
    container.innerHTML = `<div class="p-6 text-center text-xs text-zinc-500">Ninguna ciudad de ${locSelectedCountry} coincide con "${query}"</div>`;
    return;
  }

  filtered.forEach(city => {
    const isSelected = (city === locSelectedCity);
    const item = document.createElement('div');
    item.className = `flex items-center justify-between p-3 rounded-2xl cursor-pointer transition-all border select-none ${isSelected ? 'border-pink-500 bg-pink-500/15' : 'border-zinc-850 bg-zinc-900/60 hover:bg-zinc-850 hover:border-zinc-700'}`;
    
    item.onclick = function() {
      locSelectedCity = city;
      updateLocationSummary();
      renderCitiesList(query);
    };

    item.innerHTML = `
      <div class="flex items-center gap-2.5">
        <i class="fa-solid fa-city text-xs ${isSelected ? 'text-pink-400' : 'text-zinc-500'}"></i>
        <span class="text-xs font-bold ${isSelected ? 'text-white' : 'text-zinc-300'}">${city}</span>
      </div>
      <div class="${isSelected ? '' : 'hidden'} text-pink-400 font-black">
        <i class="fa-solid fa-check text-xs"></i>
      </div>
    `;
    container.appendChild(item);
  });
}

function filterLocationList(query) {
  if (locActiveTab === 'countries') {
    renderCountriesList(query);
  } else {
    renderCitiesList(query);
  }
}

function updateLocationSummary() {
  const bCountry = document.getElementById('loc-badge-selected-country');
  if (bCountry) bCountry.textContent = locSelectedCountry;

  const bCity = document.getElementById('loc-badge-selected-city');
  if (bCity) bCity.textContent = locSelectedCity;

  const summary = document.getElementById('loc-summary-text');
  if (summary) summary.textContent = `${locSelectedCity}, ${locSelectedCountry}`;
}

function closeLocationPickerModal() {
  const m = document.getElementById('modal-location-picker');
  if (m) m.classList.add('hidden');
}

function saveLocationPickerChoice() {
  const fullLoc = `${locSelectedCity}, ${locSelectedCountry}`;

  // Actualizar en el Drawer de Ajustes
  const drawerLoc = document.getElementById('drawer-pref-location');
  if (drawerLoc) {
    drawerLoc.innerHTML = `${fullLoc} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;
  }

  // Actualizar en el modal de Editar Perfil
  const editCityInput = document.getElementById('edit-city');
  if (editCityInput) editCityInput.value = fullLoc;

  // Actualizar en el Onboarding Wizard
  const onboardCityInput = document.getElementById('onboard-city');
  if (onboardCityInput) onboardCityInput.value = fullLoc;

  // Actualizar en la tarjeta de perfil
  const profCityEl = document.getElementById('my-city');
  if (profCityEl) profCityEl.textContent = fullLoc;

  if (STATE.currentUser) {
    STATE.currentUser.city = fullLoc;
  }

  closeLocationPickerModal();
}

function openInterestedInPicker() {
  const currentLang = (typeof LANG !== 'undefined' && LANG) || localStorage.getItem('sigaleve_lang') || 'pt';
  const isPt = (currentLang === 'pt');
  const isEn = (currentLang === 'en');
  const choices = isPt ? ['Mulheres', 'Homens', 'Todos'] : (isEn ? ['Women', 'Men', 'Everyone'] : ['Mujeres', 'Hombres', 'Todos']);
  const title = (typeof T === 'function' ? T('interestedIn') : null) || (isEn ? 'Interested in' : (isPt ? 'Interesse em' : 'Interesado en'));
  openSelectionModalCustom(title, 'fa-venus-mars', choices, (selected) => {
    const el = document.getElementById('drawer-pref-gender');
    if (el) el.innerHTML = `${selected} <i class="fa-solid fa-chevron-right text-xs ml-1"></i>`;
  });
}

function openSelectionModalCustom(title, iconClass, optionsList, onSaveCallback) {
  const titleEl = document.getElementById('modal-select-title');
  if (titleEl) titleEl.textContent = title;
  
  const iconEl = document.getElementById('modal-select-icon');
  if (iconEl) iconEl.className = `fa-solid ${iconClass}`;

  currentSelectedValue = optionsList[0];

  const listContainer = document.getElementById('modal-select-options-list');
  if (!listContainer) return;
  listContainer.innerHTML = '';

  optionsList.forEach((opt, idx) => {
    const isSelected = (idx === 0);
    const item = document.createElement('div');
    item.className = `flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border ${isSelected ? 'border-purple-500 bg-purple-500/15' : 'border-zinc-800 bg-zinc-900/60 hover:bg-zinc-800/80 hover:border-zinc-700'}`;
    item.onclick = function() {
      currentSelectedValue = opt;
      document.querySelectorAll('#modal-select-options-list > div').forEach(el => {
        el.className = 'flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border border-zinc-800 bg-zinc-900/60 hover:bg-zinc-800/80 hover:border-zinc-700';
        const chk = el.querySelector('.opt-check-icon');
        if (chk) chk.classList.add('hidden');
      });
      item.className = 'flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border border-purple-500 bg-purple-500/15';
      const myChk = item.querySelector('.opt-check-icon');
      if (myChk) myChk.classList.remove('hidden');
    };

    item.innerHTML = `
      <span class="text-xs font-semibold ${isSelected ? 'text-white font-bold' : 'text-zinc-200'}">${opt}</span>
      <div class="opt-check-icon ${isSelected ? '' : 'hidden'} text-purple-400 font-black">
        <i class="fa-solid fa-check text-sm"></i>
      </div>
    `;
    listContainer.appendChild(item);
  });

  const saveBtn = document.getElementById('btn-modal-select-save');
  saveBtn.onclick = function() {
    onSaveCallback(currentSelectedValue);
    closeSingleSelectModal();
  };

  const m = document.getElementById('modal-single-select');
  if (m) m.classList.remove('hidden');
}

const GLOBAL_PHONE_CODES = [
  { code: '+351', country: 'Portugal', flag: '🇵🇹' },
  { code: '+34', country: 'España', flag: '🇪🇸' },
  { code: '+33', country: 'France', flag: '🇫🇷' },
  { code: '+44', country: 'United Kingdom', flag: '🇬🇧' },
  { code: '+1', country: 'USA / Canada', flag: '🇺🇸' },
  { code: '+49', country: 'Deutschland', flag: '🇩🇪' },
  { code: '+39', country: 'Italia', flag: '🇮🇹' },
  { code: '+55', country: 'Brasil', flag: '🇧🇷' },
  { code: '+52', country: 'México', flag: '🇲🇽' },
  { code: '+54', country: 'Argentina', flag: '🇦🇷' },
  { code: '+57', country: 'Colombia', flag: '🇨🇴' },
  { code: '+56', country: 'Chile', flag: '🇨🇱' },
  { code: '+51', country: 'Perú', flag: '🇵🇪' },
  { code: '+58', country: 'Venezuela', flag: '🇻🇪' },
  { code: '+244', country: 'Angola', flag: '🇦🇴' },
  { code: '+238', country: 'Cabo Verde', flag: '🇨🇻' },
  { code: '+258', country: 'Moçambique', flag: '🇲🇿' },
  { code: '+239', country: 'São Tomé e Príncipe', flag: '🇸🇹' },
  { code: '+245', country: 'Guiné-Bissau', flag: '🇬🇼' },
  { code: '+254', country: 'Kenya', flag: '🇰🇪' },
  { code: '+234', country: 'Nigeria', flag: '🇳🇬' },
  { code: '+27', country: 'South Africa', flag: '🇿🇦' },
  { code: '+41', country: 'Schweiz / Suisse', flag: '🇨🇭' },
  { code: '+31', country: 'Nederland', flag: '🇳🇱' },
  { code: '+32', country: 'Belgique', flag: '🇧🇪' },
  { code: '+46', country: 'Sverige', flag: '🇸🇪' },
  { code: '+47', country: 'Norge', flag: '🇳🇴' },
  { code: '+45', country: 'Danmark', flag: '🇩🇰' },
  { code: '+358', country: 'Suomi', flag: '🇫🇮' },
  { code: '+48', country: 'Polska', flag: '🇵🇱' },
  { code: '+30', country: 'Ελλάδα', flag: '🇬🇷' },
  { code: '+90', country: 'Türkiye', flag: '🇹🇷' },
  { code: '+971', country: 'UAE', flag: '🇦🇪' },
  { code: '+966', country: 'Saudi Arabia', flag: '🇸🇦' },
  { code: '+81', country: 'Japan', flag: '🇯🇵' },
  { code: '+82', country: 'South Korea', flag: '🇰🇷' },
  { code: '+86', country: 'China', flag: '🇨🇳' },
  { code: '+91', country: 'India', flag: '🇮🇳' },
  { code: '+61', country: 'Australia', flag: '🇦🇺' },
  { code: '+64', country: 'New Zealand', flag: '🇳🇿' }
];

function formatPhoneNumber(num) {
  if (!num) return '';
  const str = ('' + num).trim();
  if (!str) return '';
  return str;
}

function openPhoneChangePrompt() {
  const currentPhone = (STATE.currentUser && STATE.currentUser.phone) || '';
  toggleProfileEditModal(true);
  setTimeout(() => {
    const el = document.getElementById('edit-phone');
    if (el) el.focus();
  }, 300);
}
