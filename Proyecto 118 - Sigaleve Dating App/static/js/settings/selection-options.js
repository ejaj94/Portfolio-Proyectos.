/**
 * Modais de seleção única/múltipla (género, objetivos, estilo de vida...) e respetivos dados i18n.
 */
// ═══════════════════════════════════════════════════
// SELECCIÓN EXCLUSIVA (ESTILO DEFINIÇÕES TINDER - SIN ESCRITURA MANUAL)
// ═══════════════════════════════════════════════════
let currentSelectCategory = '';
let currentSelectedValue = '';

// Dicionário multilíngue completo para todas as opções de perfil e estilo de vida
const SELECTION_OPTIONS_I18N = {
  pt: {
    // Busco
    'Relación seria, pero con calma': 'Relação séria, mas com calma',
    'Algo casual': 'Algo casual',
    'Nuevos amigos': 'Novos amigos',
    'Aún no lo tengo claro': 'Ainda não decidi',
    'Charlar y ver qué surge': 'Conversar e ver o que acontece',
    'Conexiones a largo plazo': 'Conexões a longo prazo',
    // Planes familiares
    'Quiero tener hijos': 'Quero ter filhos',
    'No quiero hijos': 'Não quero ter filhos',
    'Tengo hijos y quiero más': 'Tenho filhos e quero mais',
    'Tengo hijos y no quiero más': 'Tenho filhos e não quero mais',
    'Aún no lo sé': 'Ainda não tenho a certeza',
    // Estilo de amor
    'Tiempo de calidad': 'Tempo de qualidade',
    'Palabras de afirmación': 'Palavras de afirmação',
    'Detalles y regalos': 'Presentes e miminhos',
    'Actos de servicio': 'Atos de serviço',
    'Contacto físico': 'Contacto físico',
    // Estilo de comunicación
    'Hablo por WhatsApp todo el día': 'Falo pelo WhatsApp o dia todo',
    'Prefiero llamadas telefónicas': 'Prefiro chamadas telefónicas',
    'Mejor siempre en persona': 'Sempre melhor presencialmente',
    'Contesto cuando puedo': 'Respondo quando posso',
    'Poco comunicativo / Desconectado': 'Pouco comunicativo / Desconectado',
    // Mascotas
    'Perros': 'Cães',
    'Gatos': 'Gatos',
    'Aves': 'Pássaros',
    'Reptiles': 'Répteis',
    'Tengo varias mascotas': 'Tenho vários animais de estimação',
    'No tengo pero me encantan': 'Não tenho, mas adoro',
    'Alérgico a animales': 'Alérgico a animais',
    'Prefiero no convivir con animales': 'Prefiro não conviver com animais',
    // Zodiaco
    'Aries': 'Carneiro (Áries)',
    'Tauro': 'Touro',
    'Géminis': 'Gémeos',
    'Cáncer': 'Caranguejo (Câncer)',
    'Leo': 'Leão',
    'Virgo': 'Virgem',
    'Libra': 'Balança (Libra)',
    'Escorpio': 'Escorpião',
    'Sagitario': 'Sagitário',
    'Capricornio': 'Capricórnio',
    'Acuario': 'Aquário',
    'Piscis': 'Peixes',
    // Educación
    'En la universidad': 'Na universidade',
    'Licenciatura completada': 'Licenciatura concluída',
    'Máster / Postgrado': 'Mestrado / Pós-graduação',
    'Doctorado': 'Doutoramento',
    'Formación Profesional': 'Ensino Profissional',
    'Secundaria / Bachillerato': 'Ensino Secundário',
    'Estudiando actualmente': 'A estudar atualmente',
    // Beber
    'Socialmente': 'Socialmente',
    'Los fines de semana': 'Aos fins de semana',
    'Nunca / No bebo': 'Nunca / Não bebo',
    'Con frecuencia': 'Com frequência',
    'En ocasiones especiales': 'Em ocasiões especiais',
    // ¿Cada cuánto fumas?
    'Fumo tabaco socialmente': 'Fumo tabaco socialmente',
    'Fumador diario': 'Fumador diário',
    'Vapeo': 'Vapeio',
    'No fumo': 'Não fumo',
    'Intentando dejarlo': 'A tentar deixar de fumar',
    // Hacer ejercicio
    'A diario': 'Todos os dias',
    '3-4 veces por semana': '3-4 vezes por semana',
    'Los fines de semana': 'Aos fins de semana',
    'Rara vez': 'Raramente',
    'Nunca hago ejercicio': 'Nunca faço exercício',
    // Redes sociales
    'Muy activo / Comparto a diario': 'Muito ativo / Partilho diariamente',
    'Solo mirando / Perfil privado': 'Apenas a observar / Perfil privado',
    'No uso redes sociales': 'Não uso redes sociais',
    'Creador de contenido / Influencer': 'Criador de conteúdo / Influenciador',
    // Intereses
    'Viajes': 'Viagens',
    'Música': 'Música',
    'Gastronomía': 'Gastronomia',
    'Deportes': 'Desporto',
    'Café': 'Café',
    'Cine': 'Cinema',
    'Lectura': 'Leitura',
    'Tecnología': 'Tecnologia',
    'Arte': 'Arte',
    'Naturaleza': 'Natureza',
    'Playa': 'Praia',
    'Fotografía': 'Fotografia',
    'Yoga': 'Ioga',
    'Videojuegos': 'Videojogos',
    'Campismo': 'Campismo',
    'Moda': 'Moda',
    'Senderismo': 'Caminhadas / Trilhos'
  },
  br: {
    'Relación seria, pero con calma': 'Relacionamento sério, mas com calma',
    'Algo casual': 'Algo casual',
    'Nuevos amigos': 'Amizades novas',
    'Aún no lo tengo claro': 'Ainda não decidi',
    'Charlar y ver qué surge': 'Conversar e ver no que dá',
    'Conexiones a largo plazo': 'Relações a longo prazo',
    'Quiero tener hijos': 'Quero ter filhos',
    'No quiero hijos': 'Não quero ter filhos',
    'Tengo hijos y quiero más': 'Tenho filhos e quero mais',
    'Tengo hijos y no quiero más': 'Tenho filhos e não quero mais',
    'Aún no lo sé': 'Ainda não sei',
    'Tiempo de calidad': 'Tempo de qualidade',
    'Palabras de afirmación': 'Palavras de afirmação',
    'Detalles y regalos': 'Detalhes e presentes',
    'Actos de servicio': 'Atos de serviço',
    'Contacto físico': 'Contato físico',
    'Hablo por WhatsApp todo el día': 'Falo no WhatsApp o dia todo',
    'Prefiero llamadas telefónicas': 'Prefiro chamadas telefónicas',
    'Mejor siempre en persona': 'Sempre melhor pessoalmente',
    'Contesto cuando puedo': 'Respondo quando dá',
    'Poco comunicativo / Desconectado': 'Pouco comunicativo / Desconectado',
    'Perros': 'Cães',
    'Gatos': 'Gatos',
    'Aves': 'Pássaros',
    'Reptiles': 'Répteis',
    'Tengo varias mascotas': 'Tenho vários animais de estimação',
    'No tengo pero me encantan': 'Não tenho, mas adoro',
    'Alérgico a animales': 'Alérgico a animais',
    'Prefiero no convivir con animales': 'Prefiro não conviver com animais',
    'Aries': 'Carneiro (Áries)',
    'Tauro': 'Touro',
    'Géminis': 'Gémeos',
    'Cáncer': 'Caranguejo (Câncer)',
    'Leo': 'Leão',
    'Virgo': 'Virgem',
    'Libra': 'Balança (Libra)',
    'Escorpio': 'Escorpião',
    'Sagitario': 'Sagitário',
    'Capricornio': 'Capricórnio',
    'Acuario': 'Aquário',
    'Piscis': 'Peixes',
    'En la universidad': 'Na universidade',
    'Licenciatura completada': 'Licenciatura concluída',
    'Máster / Postgrado': 'Mestrado / Pós-graduação',
    'Doctorado': 'Doutoramento',
    'Formación Profesional': 'Ensino Profissional',
    'Secundaria / Bachillerato': 'Ensino Secundário',
    'Estudiando actualmente': 'A estudar atualmente',
    'Socialmente': 'Socialmente',
    'Los fines de semana': 'Aos fins de semana',
    'Nunca / No bebo': 'Nunca / Não bebo',
    'Con frecuencia': 'Com frequência',
    'En ocasiones especiales': 'Em ocasiões especiais',
    'Fumo tabaco socialmente': 'Fumo tabaco socialmente',
    'Fumador diario': 'Fumador diário',
    'Vapeo': 'Vapeio',
    'No fumo': 'Não fumo',
    'Intentando dejarlo': 'A tentar deixar de fumar',
    'A diario': 'Todos os dias',
    '3-4 veces por semana': '3-4 vezes por semana',
    'Los fines de semana': 'Aos fins de semana',
    'Rara vez': 'Raramente',
    'Nunca hago ejercicio': 'Nunca faço exercício',
    'Muy activo / Comparto a diario': 'Muito ativo / Partilho diariamente',
    'Solo mirando / Perfil privado': 'Apenas a observar / Perfil privado',
    'No uso redes sociales': 'Não uso redes sociais',
    'Creador de contenido / Influencer': 'Criador de conteúdo / Influenciador',
    'Viajes': 'Viagens',
    'Música': 'Música',
    'Gastronomía': 'Gastronomia',
    'Deportes': 'Desporto',
    'Café': 'Café',
    'Cine': 'Cinema',
    'Lectura': 'Leitura',
    'Tecnología': 'Tecnologia',
    'Arte': 'Arte',
    'Naturaleza': 'Natureza',
    'Playa': 'Praia',
    'Fotografía': 'Fotografia',
    'Yoga': 'Ioga',
    'Videojuegos': 'Videogames',
    'Campismo': 'Campismo',
    'Moda': 'Moda',
    'Senderismo': 'Trilhas / Trilhos'
  },
  it: {
    // Busco
    'Relación seria, pero con calma': 'Relazione seria, ma senza fretta',
    'Algo casual': 'Qualcosa di disimpegnato',
    'Nuevos amigos': 'Nuove amicizie',
    'Aún no lo tengo claro': 'Non ho ancora le idee chiare',
    'Charlar y ver qué surge': 'Chiacchierare e vedere cosa nasce',
    'Conexiones a largo plazo': 'Connessioni a lungo termine',
    // Planes familiares
    'Quiero tener hijos': 'Voglio avere figli',
    'No quiero hijos': 'Non voglio figli',
    'Tengo hijos y quiero más': 'Ho figli e ne vorrei altri',
    'Tengo hijos y no quiero más': 'Ho figli e non ne voglio altri',
    'Aún no lo sé': 'Non lo so ancora',
    // Estilo de amor
    'Tiempo de calidad': 'Tempo di qualità',
    'Palabras de afirmación': 'Parole di apprezzamento',
    'Detalles y regalos': 'Piccoli regali e attenzioni',
    'Actos de servicio': 'Gesti di premura',
    'Contacto físico': 'Contatto fisico',
    // Estilo de comunicación
    'Hablo por WhatsApp todo el día': 'Chatto su WhatsApp tutto il giorno',
    'Prefiero llamadas telefónicas': 'Preferisco telefonare',
    'Mejor siempre en persona': 'Sempre meglio di persona',
    'Contesto cuando puedo': 'Rispondo quando posso',
    'Poco comunicativo / Desconectado': 'Poco presente sui messaggi',
    // Mascotas
    'Perros': 'Cani',
    'Gatos': 'Gatti',
    'Aves': 'Uccelli',
    'Reptiles': 'Rettili',
    'Tengo varias mascotas': 'Ho diversi animali domestici',
    'No tengo pero me encantan': 'Non ne ho, ma li adoro',
    'Alérgico a animales': 'Allergico agli animali',
    'Prefiero no convivir con animales': 'Preferisco non convivere con animali',
    // Zodiaco
    'Aries': 'Ariete',
    'Tauro': 'Toro',
    'Géminis': 'Gemelli',
    'Cáncer': 'Cancro',
    'Leo': 'Leone',
    'Virgo': 'Vergine',
    'Libra': 'Bilancia',
    'Escorpio': 'Scorpione',
    'Sagitario': 'Sagittario',
    'Capricornio': 'Capricorno',
    'Acuario': 'Acquario',
    'Piscis': 'Pesci',
    // Educación
    'En la universidad': "All'università",
    'Licenciatura completada': 'Laurea conseguita',
    'Máster / Postgrado': 'Master / Post-laurea',
    'Doctorado': 'Dottorato',
    'Formación Profesional': 'Formazione Professionale',
    'Secundaria / Bachillerato': 'Diploma di scuola superiore',
    'Estudiando actualmente': 'Attualmente studente',
    // Beber
    'Socialmente': 'Socialmente',
    'Los fines de semana': 'Nei fine settimana',
    'Nunca / No bebo': 'Mai / Astemio',
    'Con frecuencia': 'Frequentemente',
    'En ocasiones especiales': 'In occasioni speciali',
    // ¿Cada cuánto fumas?
    'Fumo tabaco socialmente': 'Fumo in compagnia',
    'Fumador diario': 'Fumatore abituale',
    'Vapeo': 'Svapo',
    'No fumo': 'Non fumo',
    'Intentando dejarlo': 'Sto provando a smettere',
    // Hacer ejercicio
    'A diario': 'Tutti i giorni',
    '3-4 veces por semana': '3-4 volte a settimana',
    'Los fines de semana': 'Nei fine settimana',
    'Rara vez': 'Raramente',
    'Nunca hago ejercicio': 'Mai fatto esercizio',
    // Redes sociales
    'Muy activo / Comparto a diario': 'Molto attivo / Condivido ogni giorno',
    'Solo mirando / Perfil privado': 'Solo spettatore / Profilo privato',
    'No uso redes sociales': 'Non uso i social network',
    'Creador de contenido / Influencer': 'Content creator / Influencer',
    // Intereses
    'Viajes': 'Viaggi',
    'Música': 'Musica',
    'Gastronomía': 'Gastronomia & Cucina',
    'Deportes': 'Sport',
    'Café': 'Caffè',
    'Cine': 'Cinema & Film',
    'Lectura': 'Lettura',
    'Tecnología': 'Tecnologia',
    'Arte': 'Arte',
    'Naturaleza': 'Natura',
    'Playa': 'Spiaggia',
    'Fotografía': 'Fotografia',
    'Yoga': 'Yoga',
    'Videojuegos': 'Videogiochi',
    'Campismo': 'Campeggio',
    'Moda': 'Moda',
    'Senderismo': 'Escursionismo & Trekking'
  },
  en: {
    // Busco
    'Relación seria, pero con calma': 'Serious relationship, but taking it slow',
    'Algo casual': 'Something casual',
    'Nuevos amigos': 'New friends',
    'Aún no lo tengo claro': 'Still figuring it out',
    'Charlar y ver qué surge': 'Chat and see what happens',
    'Conexiones a largo plazo': 'Long-term connections',
    // Planes familiares
    'Quiero tener hijos': 'Want children',
    'No quiero hijos': 'Don\'t want children',
    'Tengo hijos y quiero más': 'Have children & want more',
    'Tengo hijos y no quiero más': 'Have children & don\'t want more',
    'Aún no lo sé': 'Not sure yet',
    // Estilo de amor
    'Tiempo de calidad': 'Quality time',
    'Palabras de afirmación': 'Words of affirmation',
    'Detalles y regalos': 'Receiving gifts',
    'Actos de servicio': 'Acts of service',
    'Contacto físico': 'Physical touch',
    // Estilo de comunicación
    'Hablo por WhatsApp todo el día': 'Chat on WhatsApp all day',
    'Prefiero llamadas telefónicas': 'Prefer phone calls',
    'Mejor siempre en persona': 'Always better in person',
    'Contesto cuando puedo': 'Reply when I can',
    'Poco comunicativo / Desconectado': 'Slow texter / Unplugged',
    // Mascotas
    'Perros': 'Dogs',
    'Gatos': 'Cats',
    'Aves': 'Birds',
    'Reptiles': 'Reptiles',
    'Tengo varias mascotas': 'Have multiple pets',
    'No tengo pero me encantan': 'Don\'t have pets but love them',
    'Alérgico a animales': 'Allergic to pets',
    'Prefiero no convivir con animales': 'Prefer not living with pets',
    // Zodiaco
    'Aries': 'Aries',
    'Tauro': 'Taurus',
    'Géminis': 'Gemini',
    'Cáncer': 'Cancer',
    'Leo': 'Leo',
    'Virgo': 'Virgo',
    'Libra': 'Libra',
    'Escorpio': 'Scorpio',
    'Sagitario': 'Sagittarius',
    'Capricornio': 'Capricorn',
    'Acuario': 'Aquarius',
    'Piscis': 'Pisces',
    // Educación
    'En la universidad': 'In college / University',
    'Licenciatura completada': 'Bachelor\'s degree',
    'Máster / Postgrado': 'Master\'s / Postgraduate',
    'Doctorado': 'PhD / Doctorate',
    'Formación Profesional': 'Vocational training',
    'Secundaria / Bachillerato': 'High school',
    'Estudiando actualmente': 'Currently studying',
    // Beber
    'Socialmente': 'Socially',
    'Los fines de semana': 'On weekends',
    'Nunca / No bebo': 'Never / Non-drinker',
    'Con frecuencia': 'Frequently',
    'En ocasiones especiales': 'On special occasions',
    // ¿Cada cuánto fumas?
    'Fumo tabaco socialmente': 'Social smoker',
    'Fumador diario': 'Daily smoker',
    'Vapeo': 'Vaping',
    'No fumo': 'Non-smoker',
    'Intentando dejarlo': 'Trying to quit',
    // Hacer ejercicio
    'A diario': 'Every day',
    '3-4 veces por semana': '3-4 times a week',
    'Los fines de semana': 'On weekends',
    'Rara vez': 'Rarely',
    'Nunca hago ejercicio': 'Never exercise',
    // Redes sociales
    'Muy activo / Comparto a diario': 'Very active / Post daily',
    'Solo mirando / Perfil privado': 'Lurker / Private profile',
    'No uso redes sociales': 'Don\'t use social media',
    'Creador de contenido / Influencer': 'Content creator / Influencer',
    // Intereses
    'Viajes': 'Travel',
    'Música': 'Music',
    'Gastronomía': 'Food & Dining',
    'Deportes': 'Sports',
    'Café': 'Coffee',
    'Cine': 'Cinema & Movies',
    'Lectura': 'Reading',
    'Tecnología': 'Technology',
    'Arte': 'Art',
    'Naturaleza': 'Nature',
    'Fotografía': 'Photography',
    'Yoga': 'Yoga',
    'Videojuegos': 'Gaming',
    'Campismo': 'Camping',
    'Moda': 'Fashion',
    'Senderismo': 'Hiking'
  }
};

function getLocalizedOptionLabel(opt, lang) {
  if (!opt) return '';
  const l = (lang || (typeof LANG !== 'undefined' ? LANG : null) || (window.LANG) || localStorage.getItem('sigaleve_lang') || 'pt').toLowerCase();
  if (l === 'es') return opt;
  if (SELECTION_OPTIONS_I18N && SELECTION_OPTIONS_I18N[l] && SELECTION_OPTIONS_I18N[l][opt]) {
    return SELECTION_OPTIONS_I18N[l][opt];
  }
  if (SELECTION_OPTIONS_I18N && SELECTION_OPTIONS_I18N.pt && SELECTION_OPTIONS_I18N.pt[opt]) {
    return SELECTION_OPTIONS_I18N.pt[opt];
  }
  return opt;
}

function findOriginalOptionValue(localizedOrOriginalText) {
  if (!localizedOrOriginalText) return '';
  const clean = localizedOrOriginalText.trim();
  // Se já for a chave original em espanhol
  for (const cat of Object.values(SELECTION_CATEGORIES_DATA)) {
    if (cat.options.includes(clean)) return clean;
  }
  // Se for uma tradução em pt ou en, reverter para a chave original
  for (const [lang, dict] of Object.entries(SELECTION_OPTIONS_I18N)) {
    for (const [orig, trans] of Object.entries(dict)) {
      if (trans.toLowerCase() === clean.toLowerCase()) return orig;
    }
  }
  return clean;
}

const SELECTION_CATEGORIES_DATA = {
  'Intereses': {
    icon: 'fa-heart',
    options: ['Viajes', 'Música', 'Gastronomía', 'Deportes', 'Café', 'Cine', 'Lectura', 'Tecnología', 'Arte', 'Naturaleza', 'Playa', 'Fotografía', 'Yoga', 'Videojuegos', 'Campismo', 'Moda', 'Senderismo']
  },
  'Busco': {
    icon: 'fa-eye',
    options: ['Relación seria, pero con calma', 'Algo casual', 'Nuevos amigos', 'Aún no lo tengo claro', 'Charlar y ver qué surge', 'Conexiones a largo plazo']
  },
    'Agregar idiomas': {
    icon: 'fa-language',
    options: [
      'Español', 'Português', 'English', 'Français', 'Deutsch', 'Italiano', 'Árabe', 'Chino Mandarín',
      'Chino Cantonés', 'Japonés', 'Coreano', 'Ruso', 'Hindi', 'Bengalí', 'Panyabí', 'Urdu',
      'Turco', 'Polaco', 'Ucraniano', 'Neerlandés', 'Griego', 'Checo', 'Sueco', 'Rumano',
      'Húngaro', 'Búlgaro', 'Danés', 'Finlandés', 'Noruego', 'Eslovaco', 'Croata', 'Serbio',
      'Bosnio', 'Esloveno', 'Lituano', 'Letón', 'Estonio', 'Albanés', 'Macedonio', 'Islandés',
      'Irlandés (Gaeilge)', 'Galés', 'Vasco (Euskera)', 'Catalán', 'Gallego', 'Valenciano', 'Bretón',
      'Kiswahili (Suajili)', 'Yorùbá', 'Hausa', 'Igbo', 'Amhárico', 'Somalí', 'Oromo', 'Zulú',
      'Xhosa', 'Afrikaans', 'Lingala', 'Kinyarwanda', 'Tigriña', 'Luganda', 'Shona', 'Tswana',
      'Sesotho', 'Wolof', 'Bambara', 'Fula (Pulaar)', 'Malgache', 'Indonesio', 'Malayo', 'Tagalo (Filipino)',
      'Vietnamita', 'Tailandés', 'Birmano', 'Jemer (Camboyano)', 'Laosiano', 'Mongol', 'Tibetano',
      'Hebreo', 'Persa (Farsi)', 'Pastún', 'Kurdo (Kurmanji)', 'Kurdo (Sorani)', 'Azerí', 'Kazajo',
      'Uzbeko', 'Turcomano', 'Kirguís', 'Tayiko', 'Georgiano', 'Armenio', 'Tártaro', 'Uigur',
      'Nepalí', 'Cingalés', 'Tamil', 'Telugu', 'Canarés (Kannada)', 'Malayalam', 'Maratí', 'Guyaratí',
      'Odia', 'Asamés', 'Maithili', 'Sánscrito', 'Esperanto', 'Latín'
    ]
  },
  'Zodiaco': {
    icon: 'fa-moon',
    options: ['Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo', 'Libra', 'Escorpio', 'Sagitario', 'Capricornio', 'Acuario', 'Piscis']
  },
  'Educación': {
    icon: 'fa-graduation-cap',
    options: ['En la universidad', 'Licenciatura completada', 'Máster / Postgrado', 'Doctorado', 'Formación Profesional', 'Secundaria / Bachillerato', 'Estudiando actualmente']
  },
  'Planes familiares': {
    icon: 'fa-baby',
    options: ['Quiero tener hijos', 'No quiero hijos', 'Tengo hijos y quiero más', 'Tengo hijos y no quiero más', 'Aún no lo sé']
  },
  'Estilo de comunicación': {
    icon: 'fa-comment-dots',
    options: ['Hablo por WhatsApp todo el día', 'Prefiero llamadas telefónicas', 'Mejor siempre en persona', 'Contesto cuando puedo', 'Poco comunicativo / Desconectado']
  },
  'Estilo de amor': {
    icon: 'fa-heart-circle-bolt',
    options: ['Tiempo de calidad', 'Palabras de afirmación', 'Detalles y regalos', 'Actos de servicio', 'Contacto físico']
  },
  'Mascotas': {
    icon: 'fa-paw',
    options: ['Perros', 'Gatos', 'Aves', 'Reptiles', 'Tengo varias mascotas', 'No tengo pero me encantan', 'Alérgico a animales', 'Prefiero no convivir con animales']
  },
  'Beber': {
    icon: 'fa-wine-glass',
    options: ['Socialmente', 'Los fines de semana', 'Nunca / No bebo', 'Con frecuencia', 'En ocasiones especiales']
  },
  '¿Cada cuánto fumas?': {
    icon: 'fa-smoking',
    options: ['Fumo tabaco socialmente', 'Fumador diario', 'Vapeo', 'No fumo', 'Intentando dejarlo']
  },
  'Hacer ejercicio': {
    icon: 'fa-dumbbell',
    options: ['A diario', '3-4 veces por semana', 'Los fines de semana', 'Rara vez', 'Nunca hago ejercicio']
  },
  'Redes sociales': {
    icon: 'fa-at',
    options: ['Muy activo / Comparto a diario', 'Solo mirando / Perfil privado', 'No uso redes sociales', 'Creador de contenido / Influencer']
  }
};

let currentSelectedMultiple = [];

function openSelectionModal(category) {
  currentSelectCategory = category;
  const isInterests = (category === 'Intereses');
  const isMulti = (category === 'Agregar idiomas' || isInterests);
  const catData = SELECTION_CATEGORIES_DATA[category] || { icon: 'fa-list-check', options: ['Opção 1', 'Opción 2'] };
  
  const titleEl = document.getElementById('modal-select-title');
  const subEl = document.getElementById('modal-select-subtitle');
  const counterEl = document.getElementById('modal-select-counter');
  const alertEl = document.getElementById('modal-select-limit-alert');
  if (alertEl) alertEl.classList.add('hidden');

  const catI18nKey = {
    'Intereses': 'catInterests',
    'Busco': 'catLookingFor',
    'Agregar idiomas': 'catAddLanguages',
    'Zodiaco': 'catZodiac',
    'Educación': 'catEducation',
    'Planes familiares': 'catFamilyPlans',
    'Estilo de comunicación': 'catCommunicationStyle',
    'Estilo de amor': 'catLoveStyle',
    'Mascotas': 'catPets',
    'Beber': 'catDrinking',
    '¿Cada cuánto fumas?': 'catSmoking',
    'Hacer ejercicio': 'catWorkout',
    'Redes sociales': 'catSocialMedia'
  }[category] || '';

  const catTranslated = (catI18nKey && T(catI18nKey)) ? T(catI18nKey) : category;
  if (titleEl) {
    titleEl.textContent = `${T('selectWord') || 'Selecionar'} ${catTranslated}`;
  }

  const activeLang = (typeof LANG !== 'undefined' && LANG) || (window.LANG) || localStorage.getItem('sigaleve_lang') || 'pt';

  if (isInterests) {
    const subText = (activeLang === 'es')
      ? 'Elige hasta 5 intereses para tu perfil'
      : (activeLang === 'en' ? 'Choose up to 5 interests for your profile' : 'Escolhe até 5 interesses para o teu perfil');
    if (subEl) subEl.textContent = subText;
  } else if (category === 'Agregar idiomas') {
    if (subEl) subEl.textContent = T('multiSelectDesc') || 'Podes selecionar múltiplos idiomas que falas ou entendes';
  } else {
    if (subEl) subEl.textContent = T('singleSelectDesc') || 'Escolhe uma opção da lista para o teu perfil';
  }
  
  const iconEl = document.getElementById('modal-select-icon');
  if (iconEl) iconEl.className = `fa-solid ${catData.icon}`;

  // Buscar valor actual
  const keySafe = category.replace(/\s+/g, '-').replace(/¿|\?/g, '');
  const rowValEl = document.getElementById('row-val-' + keySafe);
  let currentValText = '';
  if (rowValEl && !rowValEl.textContent.includes('Seleccionar') && !rowValEl.textContent.includes('Selecionar') && !rowValEl.textContent.includes('Select')) {
    currentValText = rowValEl.textContent.trim();
  }

  if (isInterests) {
    let rawList = [];
    if (rowValEl && rowValEl.dataset && rowValEl.dataset.originalVal) {
      rawList = rowValEl.dataset.originalVal.split(',').map(s => s.trim()).filter(Boolean);
    } else if (typeof STATE !== 'undefined' && STATE.currentUser && STATE.currentUser.interests && Array.isArray(STATE.currentUser.interests)) {
      rawList = STATE.currentUser.interests;
    } else if (currentValText) {
      rawList = currentValText.split(',').map(s => s.trim()).filter(Boolean);
    }
    
    // Filtrar estritamente para que o contador comece de 0 e APENAS inclua opções reais visíveis
    const validMapped = [];
    rawList.forEach(item => {
      const orig = findOriginalOptionValue(item) || item;
      if (catData.options.includes(orig) && !validMapped.includes(orig)) {
        validMapped.push(orig);
      }
    });

    currentSelectedMultiple = validMapped.slice(0, 5);
  } else if (isMulti) {
    if (currentValText) {
      currentSelectedMultiple = currentValText.split(',').map(s => s.trim()).filter(Boolean);
    } else {
      currentSelectedMultiple = [];
    }
  } else {
    const rawVal = rowValEl && rowValEl.dataset && rowValEl.dataset.originalVal ? rowValEl.dataset.originalVal : findOriginalOptionValue(currentValText);
    currentSelectedValue = rawVal || catData.options[0];
  }

  function updateInterestsCounterBadge() {
    if (counterEl) {
      if (isInterests) {
        counterEl.classList.remove('hidden');
        counterEl.textContent = `${currentSelectedMultiple.length} / 5`;
        if (currentSelectedMultiple.length >= 5) {
          counterEl.className = 'text-[10px] font-black px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/50';
        } else {
          counterEl.className = 'text-[10px] font-black px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/40';
        }
      } else {
        counterEl.classList.add('hidden');
      }
    }
  }
  updateInterestsCounterBadge();

  const listContainer = document.getElementById('modal-select-options-list');
  if (!listContainer) return;
  listContainer.innerHTML = '';

  // Reset del buscador para listas largas
  const searchInp = document.getElementById('modal-select-search-inp');
  if (searchInp) searchInp.value = '';
  const searchContainer = document.getElementById('modal-select-search-container');
  if (searchContainer) {
    if (catData.options.length > 10) {
      searchContainer.classList.remove('hidden');
    } else {
      searchContainer.classList.add('hidden');
    }
  }

  catData.options.forEach(opt => {
    const isSelected = isMulti ? currentSelectedMultiple.includes(opt) : (opt === currentSelectedValue);
    const localizedLabel = (category === 'Agregar idiomas') ? opt : getLocalizedOptionLabel(opt, activeLang);

    const item = document.createElement('div');
    item.className = `single-select-opt flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border ${isSelected ? 'border-purple-500 bg-purple-500/15' : 'border-zinc-800 bg-zinc-900/60 hover:bg-zinc-800/80 hover:border-zinc-700'}`;
    item.dataset.optionVal = opt;
    item.dataset.localizedVal = localizedLabel;

    item.onclick = function() {
      if (isMulti) {
        const idx = currentSelectedMultiple.indexOf(opt);
        if (idx > -1) {
          // Deseleccionar opción
          currentSelectedMultiple.splice(idx, 1);
          item.className = 'single-select-opt flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border border-zinc-800 bg-zinc-900/60 hover:bg-zinc-800/80 hover:border-zinc-700';
          const chk = item.querySelector('.opt-check-icon');
          if (chk) chk.classList.add('hidden');
          const txt = item.querySelector('.opt-label-text');
          if (txt) { txt.classList.remove('text-white', 'font-bold'); txt.classList.add('text-zinc-200'); }
          if (alertEl) alertEl.classList.add('hidden');
          updateInterestsCounterBadge();
        } else {
          // Si es Intereses y ya tiene 5 seleccionados
          if (isInterests && currentSelectedMultiple.length >= 5) {
            if (alertEl) {
              const alertMsg = (activeLang === 'es')
                ? '¡Límite alcanzado! Ya has seleccionado el máximo de 5 intereses. Desmarca uno para elegir otro.'
                : (activeLang === 'en'
                  ? 'Limit reached! You have selected the maximum of 5 interests. Deselect one to choose another.'
                  : 'Limite atingido! Já escolheste o máximo de 5 interesses. Desmarca um para poderes escolher outro.');
              const alertTextEl = document.getElementById('modal-select-limit-text');
              if (alertTextEl) alertTextEl.textContent = alertMsg;
              alertEl.classList.remove('hidden');
              alertEl.classList.add('ring-2', 'ring-amber-400');
              setTimeout(() => { if (alertEl) alertEl.classList.remove('ring-2', 'ring-amber-400'); }, 1200);
            }
            return;
          }
          // Añadir opción
          currentSelectedMultiple.push(opt);
          item.className = 'single-select-opt flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border border-purple-500 bg-purple-500/15';
          const chk = item.querySelector('.opt-check-icon');
          if (chk) chk.classList.remove('hidden');
          const txt = item.querySelector('.opt-label-text');
          if (txt) { txt.classList.remove('text-zinc-200'); txt.classList.add('text-white', 'font-bold'); }
          if (alertEl && currentSelectedMultiple.length < 5) alertEl.classList.add('hidden');
          updateInterestsCounterBadge();
        }
      } else {
        currentSelectedValue = opt;
        document.querySelectorAll('#modal-select-options-list > div').forEach(el => {
          el.className = 'single-select-opt flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border border-zinc-800 bg-zinc-900/60 hover:bg-zinc-800/80 hover:border-zinc-700';
          const chk = el.querySelector('.opt-check-icon');
          if (chk) chk.classList.add('hidden');
          const txt = el.querySelector('.opt-label-text');
          if (txt) { txt.classList.remove('text-white', 'font-bold'); txt.classList.add('text-zinc-200'); }
        });
        item.className = 'single-select-opt flex items-center justify-between p-3.5 rounded-2xl cursor-pointer transition-all border border-purple-500 bg-purple-500/15';
        const myChk = item.querySelector('.opt-check-icon');
        if (myChk) myChk.classList.remove('hidden');
        const txt = item.querySelector('.opt-label-text');
        if (txt) { txt.classList.remove('text-zinc-200'); txt.classList.add('text-white', 'font-bold'); }
      }
    };

    item.innerHTML = `
      <span class="opt-label-text text-xs font-semibold ${isSelected ? 'text-white font-bold' : 'text-zinc-200'}">${localizedLabel}</span>
      <div class="opt-check-icon ${isSelected ? '' : 'hidden'} text-purple-400 font-black">
        <i class="fa-solid fa-check text-sm"></i>
      </div>
    `;
    listContainer.appendChild(item);
  });

  const m = document.getElementById('modal-single-select');
  if (m) m.classList.remove('hidden');
}

function closeSingleSelectModal() {
  const m = document.getElementById('modal-single-select');
  if (m) m.classList.add('hidden');
  const alertEl = document.getElementById('modal-select-limit-alert');
  if (alertEl) alertEl.classList.add('hidden');
}

function saveSingleSelectChoice() {
  if (!currentSelectCategory) {
    closeSingleSelectModal();
    return;
  }

  const isInterests = (currentSelectCategory === 'Intereses');
  const isMulti = (currentSelectCategory === 'Agregar idiomas' || isInterests);
  let finalVal = '';
  let localizedDisplayVal = '';

  const activeLang = (typeof LANG !== 'undefined' && LANG) || (window.LANG) || localStorage.getItem('sigaleve_lang') || 'pt';

  if (isMulti) {
    if (currentSelectedMultiple.length === 0) {
      closeSingleSelectModal();
      return;
    }
    finalVal = currentSelectedMultiple.join(', ');
    if (isInterests) {
      localizedDisplayVal = currentSelectedMultiple.map(it => getLocalizedOptionLabel(it, activeLang)).join(', ');
    } else {
      localizedDisplayVal = finalVal;
    }
  } else {
    if (!currentSelectedValue) {
      closeSingleSelectModal();
      return;
    }
    finalVal = currentSelectedValue;
    localizedDisplayVal = getLocalizedOptionLabel(finalVal, activeLang);
  }

  const keySafe = currentSelectCategory.replace(/\s+/g, '-').replace(/¿|\?/g, '');
  const rowValEl = document.getElementById('row-val-' + keySafe);
  if (rowValEl) {
    rowValEl.classList.remove('red-val');
    rowValEl.classList.add('text-zinc-300');
    rowValEl.dataset.originalVal = finalVal;
    rowValEl.dataset.category = currentSelectCategory;
    rowValEl.innerHTML = `${localizedDisplayVal} <i class="fa-solid fa-chevron-right text-xs ml-1 text-zinc-500"></i>`;
  }

  if (isInterests) {
    // Atualizar etiquetas visuais na página do perfil
    const tagsBox = document.getElementById('prof-interests-tags');
    if (tagsBox) {
      tagsBox.innerHTML = '';
      currentSelectedMultiple.forEach(it => {
        const label = getLocalizedOptionLabel(it, activeLang);
        const sp = document.createElement('span');
        sp.className = 'px-3 py-1 rounded-full text-xs font-semibold border';
        sp.style.borderColor = 'var(--bdr)';
        sp.textContent = label;
        tagsBox.appendChild(sp);
      });
    }
    if (typeof STATE !== 'undefined' && STATE.currentUser) {
      STATE.currentUser.interests = [...currentSelectedMultiple];
    }
    // Persistir no backend
    fetch('/api/v1/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ interests: currentSelectedMultiple })
    }).catch(() => {});
  } else if (currentSelectCategory === 'Zodiaco') {
    const profSigno = document.querySelector('#sec-profile .fa-moon')?.nextElementSibling?.querySelector('p:last-child');
    if (profSigno) {
      profSigno.dataset.originalVal = finalVal;
      profSigno.textContent = localizedDisplayVal;
    }
  } else if (currentSelectCategory === 'Educación') {
    const profEdu = document.querySelector('#sec-profile .fa-graduation-cap')?.nextElementSibling?.querySelector('p:last-child');
    if (profEdu) {
      profEdu.dataset.originalVal = finalVal;
      profEdu.textContent = localizedDisplayVal;
    }
  } else if (currentSelectCategory === 'Busco') {
    const profGoal = document.getElementById('prof-relationship-goal');
    if (profGoal) {
      profGoal.dataset.originalVal = finalVal;
      profGoal.textContent = localizedDisplayVal;
    }
  }

  closeSingleSelectModal();
}
