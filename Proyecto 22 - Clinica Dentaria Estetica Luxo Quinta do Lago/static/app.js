/* QUINTA DO LAGO LUXURY DENTAL CLINIC — JAVASCRIPT ENGINE */

// Multilingual Dictionary (PT, EN, ES, FR)
const i18n = {
    pt: {
        brandTag: "MEDICINA DENTÁRIA DE ALTA PERFORMANCE",
        navTreatments: "Tratamentos",
        navTeam: "Equipa Médica",
        navLocation: "Quinta do Lago",
        navFaq: "Perguntas Frequentes",
        btnBookNav: "Agendar Diagnóstico",
        heroBadge: "QUINTA DO LAGO • ALGARVE",
        heroTitle: "A Arte da <em>Estética Dentária</em>",
        heroDesc: "Reabilitação oral de alta performance, Facetas 3D em Porcelana e Alinhadores Invisíveis numa localização privada e exclusiva.",
        btnHeroBook: "Reservar Consulta Privada",
        btnHeroTreatments: "Ver Tratamentos",
        stat1Num: "100%",
        stat1Lbl: "Personalização 3D",
        stat2Num: "+12",
        stat2Lbl: "Anos de Experiência",
        stat3Num: "0",
        stat3Lbl: "Dor / Procedimentos VIP",
        stat4Num: "Quinta do Lago",
        stat4Lbl: "Localização Privada",
        
        sectionTreatmentsSub: "TRATAMENTOS EXCLUSIVOS DE ALTA PERFORMANCE",
        sectionTreatmentsTitle: "Engenharia do Sorriso & Estética",
        sectionTreatmentsDesc: "Todos os planos de tratamento são desenhados à medida após uma consulta detalhada de Primeiro Diagnóstico & Avaliação Estética 3D.",
        
        pricingNote: "Orçamento atribuído após Consulta de Primeiro Diagnóstico",
        btnBookCard: "Agendar Avaliação Privada",
        
        // Treatments list
        t1Title: "Facetas de Porcelana 3D",
        t1Desc: "Laminados cerâmicos ultrafinos desenhados digitalmente para transformar o alinhamento, cor e proporção dos seus dentes.",
        t2Title: "Ortodoncia Invisível (Spark / Invisalign)",
        t2Desc: "Alinhadores transparentes de alta precisão que corrigem a posição dos seus dentes de forma estética e discreta.",
        t3Title: "Branqueamento a Laser",
        t3Desc: "Tecnologia de iluminação fria polimérica para obter um sorriso até 8 tons mais claro sem sensibilidade dentária.",
        t4Title: "Implantes de Carga Imediata",
        t4Desc: "Reabilitação oral num único dia com implantes dentários de titânio de grau cirúrgico e prótese fixa imediata.",
        t5Title: "Digital Smile Design (DSD 3D)",
        t5Desc: "Simulação tridimensional em tempo real que permite visualizar o seu novo sorriso antes de iniciar qualquer procedimento.",
        t6Title: "Reabilitação Oral Total",
        t6Desc: "Restauração integral estética e funcional da cavidade oral combinando cirurgia guiada por computador e cerâmica estéril.",
        
        // Team
        sectionTeamSub: "CORPO CIENTÍFICO DE EXCELÊNCIA",
        sectionTeamTitle: "Especialistas em Medicina Dentária",
        sectionTeamDesc: "Médicos dentistas dedicados à estética avançada e reabilitação complexa com registo na Ordem dos Médicos Dentistas de Portugal.",
        doc1Title: "Director Clínico • Estética & Implantologia",
        doc1Desc: "Pioneiro em Digital Smile Design e cirurgia guiada na Europa com mais de 5.000 casos clínicos de sucesso.",
        doc2Title: "Especialista em Ortodoncia Invisível",
        doc2Desc: "Doutorada em biomecânica de alinhadores transparentes e especialista no sistema Invisalign Diamond Provider.",
        doc3Title: "Cirurgião Oral & Carga Imediata",
        doc3Desc: "Mestre em cirurgia de reabilitação complexa e implantes dentários com pós-graduação internacional.",
        
        // Location
        locationTitle: "Instalações Privadas na Quinta do Lago",
        locationDesc: "Um refúgio de tranquilidade e saúde no coração do Algarve. Concebido para oferecer total privacidade, estacionamento reservado e o máximo conforto médico.",
        locAddress: "Av. Ayrton Senna, Edifício Quinta Shopping, Quinta do Lago, 8135-024 Almancil, Algarve",
        locPhone: "+351 123 456 789 (Linha Directa)",
        locHours: "Segunda a Sábado: 09:00 - 19:00 (Atendimento por Marcação)",
        
        // FAQ
        sectionFaqSub: "ESCLARECIMENTO DE DÚVIDAS",
        sectionFaqTitle: "Perguntas Frequentes",
        faq1Q: "Como funciona a primeira consulta de diagnóstico?",
        faq1A: "A primeira consulta inclui um exame clínico minucioso, radiografia tridimensional CBCT e rastreio digital 3D. No final, é apresentado o plano estético personalizado sem qualquer compromisso.",
        faq2Q: "Por que motivo a clínica não apresenta preços na página web?",
        faq2A: "Como clínica de alta performance, cada tratamento é 100% individualizado. Os valores finais dependem das necessidades biológicas, número de peças cerâmicas e tecnologia aplicada, sendo definidos na consulta de avaliação.",
        faq3Q: "Os tratamentos estéticos e facetas são dolorosos?",
        faq3A: "Não. Utilizamos anestesia computadorizada de precisão e técnicas minimamente invasivas que garantem o máximo conforto durante e após a intervenção.",
        faq4Q: "Disponibilizam apoio a clientes internacionais na Quinta do Lago?",
        faq4A: "Sim. A nossa equipa é fluente em Português, Inglês, Espanhol e Francês, disponibilizando serviço de concierge para estadias de tratamento intensivo.",
        
        // Modal Form
        modalSubtitle: "MARCAÇÃO DE CONSULTA PRIVADA",
        modalTitle: "Agendar Diagnóstico Estético",
        modalDesc: "Preencha o formulário para ser contactado pela nossa assistente médica dedicada num prazo máximo de 2 horas.",
        lblTreatment: "Tratamento Escolhido",
        lblName: "Nome Completo *",
        lblPhone: "Telemóvel / WhatsApp *",
        lblEmail: "E-mail *",
        lblDate: "Data Preferencial de Marcação",
        btnSubmitModal: "Enviar Solicitação no WhatsApp"
    },
    en: {
        brandTag: "HIGH PERFORMANCE DENTAL MEDICINE",
        navTreatments: "Treatments",
        navTeam: "Medical Team",
        navLocation: "Quinta do Lago",
        navFaq: "FAQ",
        btnBookNav: "Book Diagnostic",
        heroBadge: "QUINTA DO LAGO • ALGARVE",
        heroTitle: "The Art of Luxury <em>Dental Aesthetics</em>",
        heroDesc: "High-performance oral rehabilitation, 3D Porcelain Veneers, and Invisible Aligners in an exclusive private sanctuary.",
        btnHeroBook: "Book Private Consultation",
        btnHeroTreatments: "View Treatments",
        stat1Num: "100%",
        stat1Lbl: "3D Customization",
        stat2Num: "+12",
        stat2Lbl: "Years of Excellence",
        stat3Num: "0",
        stat3Lbl: "Pain / VIP Procedures",
        stat4Num: "Quinta do Lago",
        stat4Lbl: "Private Location",
        
        sectionTreatmentsSub: "EXCLUSIVE HIGH PERFORMANCE TREATMENTS",
        sectionTreatmentsTitle: "Smile Engineering & Luxury Aesthetics",
        sectionTreatmentsDesc: "All treatment plans are tailored after a detailed First Diagnostic & 3D Aesthetic Assessment.",
        
        pricingNote: "Personalized quotation provided after First Diagnostic Assessment",
        btnBookCard: "Book Private Assessment",
        
        t1Title: "3D Porcelain Veneers",
        t1Desc: "Ultra-thin ceramic laminates digitally designed to transform alignment, shade, and proportion.",
        t2Title: "Invisible Orthodontics (Spark / Invisalign)",
        t2Desc: "High-precision clear aligners that correct your smile with ultimate aesthetic discretion.",
        t3Title: "Laser Whitening",
        t3Desc: "Advanced cold-light technology delivering up to 8 shades whiter without tooth sensitivity.",
        t4Title: "Immediate Load Implants",
        t4Desc: "Same-day full smile rehabilitation using surgical-grade titanium implants and immediate fixed teeth.",
        t5Title: "Digital Smile Design (DSD 3D)",
        t5Desc: "Real-time 3D simulation allowing you to preview your new smile before starting any treatment.",
        t6Title: "Total Oral Rehabilitation",
        t6Desc: "Complete functional and aesthetic restoration combining computer-guided surgery and sterile ceramic.",
        
        sectionTeamSub: "SCIENTIFIC BOARD OF EXCELLENCE",
        sectionTeamTitle: "Experts in Dental Medicine",
        sectionTeamDesc: "Specialist dentists registered with the Portuguese Dental Association dedicated to advanced aesthetics.",
        doc1Title: "Clinical Director • Aesthetics & Implantology",
        doc1Desc: "European pioneer in Digital Smile Design with over 5,000 successful clinical cases.",
        doc2Title: "Invisible Orthodontics Specialist",
        doc2Desc: "Ph.D. in clear aligner biomechanics and certified Invisalign Diamond Provider.",
        doc3Title: "Oral Surgeon & Immediate Load",
        doc3Desc: "Master in complex rehabilitation surgery and dental implants with international training.",
        
        locationTitle: "Private Sanctuary in Quinta do Lago",
        locationDesc: "A peaceful haven for world-class dental care in Quinta do Lago, featuring private parking and VIP discretion.",
        locAddress: "Ayrton Senna Ave, Quinta Shopping, Quinta do Lago, 8135-024 Almancil, Algarve",
        locPhone: "+351 123 456 789 (Direct Line)",
        locHours: "Monday to Saturday: 09:00 - 19:00 (By Appointment Only)",
        
        sectionFaqSub: "FREQUENTLY ASKED QUESTIONS",
        sectionFaqTitle: "Everything You Need to Know",
        faq1Q: "What happens during the first diagnostic consultation?",
        faq1A: "The consultation includes a full clinical examination, 3D CBCT digital radiography, and a 3D smile scan to build your custom treatment plan.",
        faq2Q: "Why are prices not listed on the website?",
        faq2A: "As a high-performance luxury clinic, every treatment is 100% bespoke. Precise costs are determined after your diagnostic assessment.",
        faq3Q: "Are aesthetic procedures painful?",
        faq3A: "Not at all. We utilize computerized painless anesthesia and minimally invasive techniques for maximum comfort.",
        faq4Q: "Do you support international clients visiting Quinta do Lago?",
        faq4A: "Yes. Our team speaks English, Portuguese, Spanish, and French, offering dedicated VIP concierge service for international visitors.",
        
        modalSubtitle: "PRIVATE APPOINTMENT BOOKING",
        modalTitle: "Book Aesthetic Diagnostic",
        modalDesc: "Fill in your details and our senior medical assistant will reach out within 2 hours.",
        lblTreatment: "Selected Treatment",
        lblName: "Full Name *",
        lblPhone: "Phone / WhatsApp *",
        lblEmail: "Email *",
        lblDate: "Preferred Appointment Date",
        btnSubmitModal: "Send Inquiry via WhatsApp"
    },
    es: {
        brandTag: "MEDICINA DENTAL DE ALTA PERFORMANCE",
        navTreatments: "Tratamientos",
        navTeam: "Equipo Médico",
        navLocation: "Quinta do Lago",
        navFaq: "Preguntas Frecuentes",
        btnBookNav: "Reservar Diagnóstico",
        heroBadge: "QUINTA DO LAGO • ALGARVE",
        heroTitle: "El Arte de la <em>Estética Dental</em>",
        heroDesc: "Rehabilitación oral de alta performance, Carillas 3D de Porcelana y Ortodoncia Invisible en una ubicación privada y exclusiva.",
        btnHeroBook: "Reservar Consulta Privada",
        btnHeroTreatments: "Ver Tratamientos",
        stat1Num: "100%",
        stat1Lbl: "Personalización 3D",
        stat2Num: "+12",
        stat2Lbl: "Años de Excelencia",
        stat3Num: "0",
        stat3Lbl: "Dolor / Procedimientos VIP",
        stat4Num: "Quinta do Lago",
        stat4Lbl: "Ubicación Privada",
        
        sectionTreatmentsSub: "TRATAMIENTOS EXCLUSIVOS DE ALTA PERFORMANCE",
        sectionTreatmentsTitle: "Ingeniería de la Sonrisa & Estética de Lujo",
        sectionTreatmentsDesc: "Todos los planes se diseñan a medida tras una consulta detallada de Primer Diagnóstico y Evaluación Estética 3D.",
        
        pricingNote: "Presupuesto asignado tras la Consulta de Primer Diagnóstico",
        btnBookCard: "Reservar Evaluación Privada",
        
        t1Title: "Carillas de Porcelana 3D",
        t1Desc: "Laminados cerámicos ultrafinos diseñados digitalmente para transformar alineación, color y proporción.",
        t2Title: "Ortodoncia Invisible (Spark / Invisalign)",
        t2Desc: "Alineadores transparentes de alta precisión que corrigen su sonrisa con absoluta discreción.",
        t3Title: "Blanqueamiento Láser",
        t3Desc: "Tecnología de luz fría polimérica para obtener un tono hasta 8 niveles más claro sin sensibilidad.",
        t4Title: "Implantes de Carga Inmediata",
        t4Desc: "Rehabilitación en un solo día mediante implantes de titanio de grado quirúrgico y prótesis fija inmediata.",
        t5Title: "Digital Smile Design (DSD 3D)",
        t5Desc: "Simulación tridimensional en tiempo real que permite previsualizar su nueva sonrisa antes de iniciar el tratamiento.",
        t6Title: "Rehabilitación Oral Total",
        t6Desc: "Restauración integral estética y funcional combinando cirugía guiada por ordenador y cerámica estéril.",
        
        sectionTeamSub: "CUERPO CIENTÍFICO DE EXCELENCIA",
        sectionTeamTitle: "Especialistas en Medicina Dental",
        sectionTeamDesc: "Odontólogos dedicados a la estética avanzada registrados en el Colegio de Odontólogos de Portugal.",
        doc1Title: "Director Clínico • Estética e Implantología",
        doc1Desc: "Pionero en Digital Smile Design y cirugía guiada en Europa con más de 5.000 casos de éxito.",
        doc2Title: "Especialista en Ortodoncia Invisible",
        doc2Desc: "Doctora en biomecánica de alineadores transparentes y proveedora Invisalign Diamond.",
        doc3Title: "Cirujano Oral & Carga Inmediata",
        doc3Desc: "Máster en cirugía de rehabilitación compleja e implantes con formación internacional.",
        
        locationTitle: "Instalaciones Privadas en Quinta do Lago",
        locationDesc: "Un refugio exclusivo de salud en el corazón del Algarve, con aparcamiento privado y máxima discreción médica.",
        locAddress: "Av. Ayrton Senna, Quinta Shopping, Quinta do Lago, 8135-024 Almancil, Algarve",
        locPhone: "+351 123 456 789 (Línea Directa)",
        locHours: "Lunes a Sábado: 09:00 - 19:00 (Atención con Cita Previa)",
        
        sectionFaqSub: "PREGUNTAS FRECUENTES",
        sectionFaqTitle: "Todo lo que Necesita Saber",
        faq1Q: "¿Cómo funciona la primera consulta de diagnóstico?",
        faq1A: "La primera visita incluye examen clínico completo, radiografía CBCT 3D y escaneo digital para elaborar su plan estético personalizado.",
        faq2Q: "¿Por qué no se publican precios en el sitio web?",
        faq2A: "Al ser una clínica de alta performance, cada tratamiento es 100% único. El presupuesto final se define tras la valoración diagnóstica.",
        faq3Q: "¿Los tratamientos estéticos causan dolor?",
        faq3A: "No. Empleamos anestesia computadorizada de alta precisión y técnicas mínimamente invasivas para un confort absoluto.",
        faq4Q: "¿Atienden a pacientes internacionales en Quinta do Lago?",
        faq4A: "Sí. Nuestro equipo habla español, portugués, inglés y francés, ofreciendo servicio de concierge para pacientes internacionales.",
        
        modalSubtitle: "RESERVA DE CITA PRIVADA",
        modalTitle: "Reservar Diagnóstico Estético",
        modalDesc: "Rellene el formulario y nuestra asistente médica le contactará en un plazo máximo de 2 horas.",
        lblTreatment: "Tratamiento Seleccionado",
        lblName: "Nombre Completo *",
        lblPhone: "Teléfono / WhatsApp *",
        lblEmail: "Correo Electrónico *",
        lblDate: "Fecha Preferida",
        btnSubmitModal: "Enviar Solicitud por WhatsApp"
    },
    fr: {
        brandTag: "MÉDECINE DENTAIRE DE HAUTE PERFORMANCE",
        navTreatments: "Traitements",
        navTeam: "Équipe Médicale",
        navLocation: "Quinta do Lago",
        navFaq: "FAQ",
        btnBookNav: "Prendre RDV",
        heroBadge: "QUINTA DO LAGO • ALGARVE",
        heroTitle: "L'Art de l'<em>Esthétique Dentaire</em>",
        heroDesc: "Réhabilitation orale haute performance, Facettes 3D en Porcelaine et Aligneurs Invisibles dans un cadre privé exclusif.",
        btnHeroBook: "Réserver une Consultation Privée",
        btnHeroTreatments: "Découvrir les Traitements",
        stat1Num: "100%",
        stat1Lbl: "Personnalisation 3D",
        stat2Num: "+12",
        stat2Lbl: "Années d'Expérience",
        stat3Num: "0",
        stat3Lbl: "Douleur / Soins VIP",
        stat4Num: "Quinta do Lago",
        stat4Lbl: "Emplacement Privé",
        
        sectionTreatmentsSub: "TRAITEMENTS EXCLUSIFS DE HAUTE PERFORMANCE",
        sectionTreatmentsTitle: "Ingénierie du Sourire & Esthétique de Luxe",
        sectionTreatmentsDesc: "Chaque plan de traitement est conçu sur mesure après un Premier Diagnostic & Évaluation Esthétique 3D.",
        
        pricingNote: "Devis personnalisé établi lors du Premier Diagnostic",
        btnBookCard: "Réserver un Diagnostic",
        
        t1Title: "Facettes en Porcelaine 3D",
        t1Desc: "Lamines céramiques ultra-fines conçues numériquement pour perfectionner l'alignement, la couleur et la forme.",
        t2Title: "Orthodontie Invisible (Spark / Invisalign)",
        t2Desc: "Aligneurs transparents de haute précision pour corriger votre sourire en toute discrétion.",
        t3Title: "Blanchiment Laser",
        t3Desc: "Technologie de lumière froide polymère offrant jusqu'à 8 teintes plus claires sans sensibilité dentaire.",
        t4Title: "Implants à Charge Immédiate",
        t4Desc: "Réhabilitation complète en 24h avec implants en titane chirurgical et prothèse fixe immédiate.",
        t5Title: "Digital Smile Design (DSD 3D)",
        t5Desc: "Simulation tridimensionnelle permettant de visualiser votre nouveau sourire avant tout soin.",
        t6Title: "Réhabilitation Orale Totale",
        t6Desc: "Restauration complète esthétique et fonctionnelle combinant chirurgie guidée et céramique stérile.",
        
        sectionTeamSub: "CORPS MÉDICAL D'EXCELLENCE",
        sectionTeamTitle: "Spécialistes en Médecine Dentaire",
        sectionTeamDesc: "Chirurgiens-dentistes inscrits à l'Ordre des Dentistes du Portugal dédiés à l'esthétique dentaire avancée.",
        doc1Title: "Directeur Clinique • Esthétique & Implantologie",
        doc1Desc: "Pionnier du Digital Smile Design en Europe avec plus de 5 000 cas cliniques réussis.",
        doc2Title: "Spécialiste en Orthodontie Invisible",
        doc2Desc: "Docteur en biomécanique des aligneurs transparents et praticienne Invisalign Diamond.",
        doc3Title: "Chirurgien Oral & Charge Immédiate",
        doc3Desc: "Expert en chirurgie réparatrice complexe et implants dentaires de haute précision.",
        
        locationTitle: "Clinique Privée à Quinta do Lago",
        locationDesc: "Un havre de paix et de santé au cœur de Quinta do Lago, Algarve, proposant un parking privé et une discrétion absolue.",
        locAddress: "Av. Ayrton Senna, Quinta Shopping, Quinta do Lago, 8135-024 Almancil, Algarve",
        locPhone: "+351 123 456 789 (Ligne Directe)",
        locHours: "Lundi au Samedi: 09:00 - 19:00 (Sur Rendez-vous Uniquement)",
        
        sectionFaqSub: "FOIRE AUX QUESTIONS",
        sectionFaqTitle: "Toutes vos Réponses",
        faq1Q: "Comment se déroule le premier rendez-vous de diagnostic?",
        faq1A: "La séance comprend un examen complet, une radiographie CBCT 3D et un scanner numérique pour élaborer votre plan personnalisé.",
        faq2Q: "Pourquoi aucun tarif n'est-il affiché sur le site web?",
        faq2A: "Chaque plan est 100% sur-mesure. Le devis précis est établi à l'issue de votre première évaluation clinique.",
        faq3Q: "Les soins esthétiques sont-ils douloureux?",
        faq3A: "Non. Nous utilisons une anesthésie informatisée et des techniques peu invasives pour un confort optimal.",
        faq4Q: "Accueillez-vous les clients internationaux à Quinta do Lago?",
        faq4A: "Oui. Notre équipe parle Français, Anglais, Portugais et Espagnol, offrant un service de conciergerie VIP dédié.",
        
        modalSubtitle: "RÉSERVATION DE RDV PRIVÉ",
        modalTitle: "Réserver un Diagnostic Esthétique",
        modalDesc: "Complétez le formulaire et notre assistant médical vous recontactera sous 2 heures.",
        lblTreatment: "Traitement Sélectionné",
        lblName: "Nom Complet *",
        lblPhone: "Téléphone / WhatsApp *",
        lblEmail: "E-mail *",
        lblDate: "Date Souhaitée",
        btnSubmitModal: "Envoyer la Demande sur WhatsApp"
    }
};

let currentLang = 'pt';

// Initialize Theme & Lang on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    // Restore saved theme or default to light mode
    const savedTheme = localStorage.getItem('clinic_theme') || 'light';
    setTheme(savedTheme);
    
    // Restore saved lang or default to PT
    const savedLang = localStorage.getItem('clinic_lang') || 'pt';
    setLanguage(savedLang);
});

// Toggle Theme Function
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('clinic_theme', theme);
    
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }
}

// Change Language Function
function setLanguage(lang) {
    if (!i18n[lang]) return;
    currentLang = lang;
    localStorage.setItem('clinic_lang', lang);
    
    // Update active lang button UI
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    
    // Translate all elements with data-i18n
    const dict = i18n[lang];
    document.querySelectorAll('[data-i18n]').forEach(elem => {
        const key = elem.getAttribute('data-i18n');
        if (dict[key]) {
            if (elem.tagName === 'INPUT' || elem.tagName === 'TEXTAREA') {
                elem.placeholder = dict[key];
            } else {
                elem.innerHTML = dict[key];
            }
        }
    });
}

// THE HOOK: Open Booking Modal pre-filled with treatment
function openBookingModal(treatmentName = null) {
    const modal = document.getElementById('bookingModal');
    const input = document.getElementById('modalTargetTreatment');
    
    if (input) {
        if (treatmentName) {
            input.value = treatmentName;
        } else {
            const dict = i18n[currentLang];
            input.value = dict['t5Title'] || 'Consulta de Primeiro Diagnóstico & Avaliação Estética 3D';
        }
    }
    
    if (modal) {
        modal.classList.add('active');
    }
}

function closeBookingModal() {
    const modal = document.getElementById('bookingModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// FAQ Accordion Toggle
function toggleFaq(headerElem) {
    const item = headerElem.parentElement;
    const isActive = item.classList.contains('active');
    
    // Close all other items
    document.querySelectorAll('.faq-item').forEach(el => el.classList.remove('active'));
    
    if (!isActive) {
        item.classList.add('active');
    }
}

// Submit Inquiry to WhatsApp (+351 123 456 789)
function submitBookingForm(event) {
    event.preventDefault();
    
    const name = document.getElementById('vipName').value.trim();
    const phone = document.getElementById('vipPhone').value.trim();
    const email = document.getElementById('vipEmail').value.trim();
    const date = document.getElementById('vipDate').value;
    const treatment = document.getElementById('modalTargetTreatment').value;
    
    if (!name || !phone || !email) {
        alert("Por favor, preencha todos os campos obrigatórios (*).");
        return;
    }
    
    const message = `*SOLICITAÇÃO DE CONSULTA VIP — QUINTA DO LAGO LUXURY DENTAL CLINIC*\n\n` +
                    `📌 *Tratamento Escolhido:* ${treatment}\n` +
                    `👤 *Nome do Paciente:* ${name}\n` +
                    `📞 *Contacto / WhatsApp:* ${phone}\n` +
                    `✉️ *E-mail:* ${email}\n` +
                    `📅 *Data Preferencial:* ${date || 'A combinar com assistente'}\n\n` +
                    `_Enviado via website Quinta do Lago Dental Clinic_`;
                    
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/351123456789?text=${encodedMessage}`;
    
    window.open(whatsappUrl, '_blank');
    closeBookingModal();
}
