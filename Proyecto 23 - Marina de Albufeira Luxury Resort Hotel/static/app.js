/* MARINA DE ALBUFEIRA LUXURY RESORT & SPA — JAVASCRIPT ENGINE */

// Multilingual Dictionary (PT, EN, ES, FR)
const i18n = {
    pt: {
        brandTag: "5★ LUXURY RESORT & SPA • ALGARVE",
        navRooms: "Suites & Quartos",
        navDining: "Gastronomia & Bares",
        navGallery: "Galeria",
        navLocation: "Marina de Albufeira",
        btnBookNav: "Reservar Estadia",
        
        heroBadge: "MARINA DE ALBUFEIRA • ALGARVE • PORTUGAL",
        heroTitle: "O Luxo à Beira da <em>Marina de Albufeira</em>",
        heroDesc: "Uma estância de 5 estrelas com suites panorâmicas, restaurante gourmet de autor, piscina infinita e serviço exclusivo de iates no Algarve.",
        btnHeroBook: "Reservar Suite Privada",
        btnHeroRooms: "Ver Tipologias",
        
        lblCheckIn: "Data de Entrada (Check-In)",
        lblCheckOut: "Data de Saída (Check-Out)",
        lblGuests: "Hóspedes",
        lblCategory: "Tipologia",
        btnSearch: "Verificar Disponibilidade",
        
        sectionRoomsSub: "ACOMODAÇÕES EXCLUSIVAS DE 5 ESTRELAS",
        sectionRoomsTitle: "Suites & Penthouse de Luxo",
        sectionRoomsDesc: "Todas as suites dispõem de varanda privada com vista panorâmica para a Marina de Albufeira ou Oceano Atlântico.",
        btnBookRoomCard: "Reservar esta Suite",
        perNight: "/ Noite",
        
        // Rooms list
        r1Title: "Suite Presidencial Vista Marina",
        r1Desc: "Penthouse de topo com terraço panorâmico de 180°, jacuzzi privativo, sala de estar e mordomo dedicado.",
        r2Title: "Suite Marina Deluxe",
        r2Desc: "Elegante suite com varanda virada para os iates da marina, casa de banho em mármore e cama King Size.",
        r3Title: "Suite Executive Spa",
        r3Desc: "Acomodação com circuito térmico privado, banheira hidromassagem e acesso ilimitado ao Royal Marina Spa.",
        r4Title: "Penthouse Familiar (3 Quartos)",
        r4Desc: "Espaçosa suite familiar com 3 quartos master, cozinha totalmente equipada e terraço com zona de refeições.",
        r5Title: "Suite Royal Yacht Club",
        r5Desc: "Acesso direto ao cais da marina com pacote VIP de iate privado e serviço de champanhe ao pôr do sol.",
        r6Title: "Suite Sunset Panoramic",
        r6Desc: "Varanda orientada a poente para apreciar o pôr do sol do Algarve sobre o Oceano Atlântico.",
        
        // Dining
        sectionDiningSub: "GASTRONOMIA DE AUTOR & COCKTAILS",
        sectionDiningTitle: "Restaurante Gourmet & Lounge Bars",
        sectionDiningDesc: "Experiências culinárias de topo com ingredientes frescos do mar Algarvio e carta de vinhos selecionada.",
        d1Title: "Restaurante Gourmet Amura",
        d1Desc: "Alta cozinha Mediterrânica com peixe fresco da costa e vista deslumbrante para a marina.",
        d2Title: "Marina Lounge & Cocktail Club",
        d2Desc: "Cocktails de autor, champanhe e música ao vivo na esplanada sobre a água ao entardecer.",
        d3Title: "Royal Marina Spa & Thermal Club",
        d3Desc: "Circuito de águas, piscina aquecida, saunas e tratamentos de bem-estar corporais de luxo.",
        
        // Location
        locationTitle: "Localização Privilegiada na Marina",
        locationDesc: "Situado no coração da Marina de Albufeira, o resort combina tranquilidade total com acesso direto aos melhores passeios de barco e praias do Algarve.",
        locAddress: "Alameda do Convento, Marina de Albufeira, 8200-394 Albufeira, Algarve, Portugal",
        locPhone: "+351 123 456 789 (Linha Directa de Reservas)",
        locHours: "Recepção & Concierge 24 Horas",
        
        // Modal Form
        modalSubtitle: "MOTOR DE RESERVAS VIP",
        modalTitle: "Confirmar Reserva de Estadia",
        modalDesc: "Selecione as suas datas e os dados para enviar a sua reserva para a equipa de Concierge.",
        lblSelectedRoom: "Acomodação Selecionada",
        lblName: "Nome Completo *",
        lblPhone: "Telemóvel / WhatsApp *",
        lblEmail: "E-mail *",
        btnSubmitModal: "Enviar Reserva no WhatsApp"
    },
    en: {
        brandTag: "5★ LUXURY RESORT & SPA • ALGARVE",
        navRooms: "Suites & Rooms",
        navDining: "Dining & Bars",
        navGallery: "Gallery",
        navLocation: "Albufeira Marina",
        btnBookNav: "Book Stay",
        
        heroBadge: "ALBUFEIRA MARINA • ALGARVE • PORTUGAL",
        heroTitle: "Luxury at the Edge of <em>Albufeira Marina</em>",
        heroDesc: "A 5-star waterfront sanctuary featuring panoramic suites, fine dining restaurant, infinity pool, and private yacht charter.",
        btnHeroBook: "Book Private Suite",
        btnHeroRooms: "View Suites",
        
        lblCheckIn: "Check-In Date",
        lblCheckOut: "Check-Out Date",
        lblGuests: "Guests",
        lblCategory: "Category",
        btnSearch: "Check Availability",
        
        sectionRoomsSub: "EXCLUSIVE 5-STAR ACCOMMODATIONS",
        sectionRoomsTitle: "Luxury Suites & Penthouse",
        sectionRoomsDesc: "All suites offer private balconies with panoramic views of Albufeira Marina or the Atlantic Ocean.",
        btnBookRoomCard: "Book this Suite",
        perNight: "/ Night",
        
        r1Title: "Presidential Marina Suite",
        r1Desc: "Top penthouse featuring 180° panoramic terrace, private Jacuzzi, master lounge, and dedicated butler.",
        r2Title: "Marina Deluxe Suite",
        r2Desc: "Elegant suite overlooking the marina superyachts, marble bathroom, and King size bed.",
        r3Title: "Executive Spa Suite",
        r3Desc: "Accommodation with private thermal circuit, hydromassage bath, and unlimited Royal Spa access.",
        r4Title: "Family Penthouse (3 Bedrooms)",
        r4Desc: "Spacious 3-bedroom family penthouse with fully equipped kitchen and private dining terrace.",
        r5Title: "Royal Yacht Club Suite",
        r5Desc: "Direct dock access with private yacht charter package and sunset champagne service.",
        r6Title: "Sunset Panoramic Suite",
        r6Desc: "West-facing terrace designed to enjoy Algarve’s breathtaking golden hour sunsets.",
        
        sectionDiningSub: "FINE DINING & SIGNATURE COCKTAILS",
        sectionDiningTitle: "Gourmet Restaurant & Lounge Bars",
        sectionDiningDesc: "Culinary excellence showcasing fresh Atlantic seafood and curated wine pairings.",
        d1Title: "Amura Gourmet Restaurant",
        d1Desc: "Mediterranean fine dining featuring fresh coastal seafood and waterfront marina views.",
        d2Title: "Marina Lounge & Cocktail Club",
        d2Desc: "Signature cocktails, champagne, and live music on the waterfront deck at sunset.",
        d3Title: "Royal Marina Spa & Wellness",
        d3Desc: "Thermal water circuit, heated indoor pool, saunas, and luxury body wellness rituals.",
        
        locationTitle: "Prime Waterfront Location",
        locationDesc: "Located in Albufeira Marina, combining peaceful sanctuary privacy with direct yacht charter access.",
        locAddress: "Alameda do Convento, Albufeira Marina, 8200-394 Albufeira, Algarve, Portugal",
        locPhone: "+351 123 456 789 (Direct Reservation Line)",
        locHours: "24-Hour Reception & Concierge",
        
        modalSubtitle: "VIP RESERVATION ENGINE",
        modalTitle: "Confirm Suite Booking",
        modalDesc: "Choose your stay dates and contact info to send your inquiry directly to Concierge.",
        lblSelectedRoom: "Selected Accommodation",
        lblName: "Full Name *",
        lblPhone: "Phone / WhatsApp *",
        lblEmail: "Email *",
        btnSubmitModal: "Send Booking via WhatsApp"
    },
    es: {
        brandTag: "5★ LUXURY RESORT & SPA • ALGARVE",
        navRooms: "Suites & Habitaciones",
        navDining: "Gastronomía & Bares",
        navGallery: "Galería",
        navLocation: "Marina de Albufeira",
        btnBookNav: "Reservar Estancia",
        
        heroBadge: "MARINA DE ALBUFEIRA • ALGARVE • PORTUGAL",
        heroTitle: "El Lujo Frente a la <em>Marina de Albufeira</em>",
        heroDesc: "Un resort de 5 estrellas con suites panorámicas, restaurante gourmet de autor, piscina infinita y servicio exclusivo de yates.",
        btnHeroBook: "Reservar Suite Privada",
        btnHeroRooms: "Ver Tipologías",
        
        lblCheckIn: "Fecha de Entrada",
        lblCheckOut: "Fecha de Salida",
        lblGuests: "Huéspedes",
        lblCategory: "Tipología",
        btnSearch: "Consultar Disponibilidad",
        
        sectionRoomsSub: "ALOJAMIENTOS EXCLUSIVOS DE 5 ESTRELLAS",
        sectionRoomsTitle: "Suites & Penthouse de Lujo",
        sectionRoomsDesc: "Todas las suites disponen de terraza privada con vistas panorámicas a la marina o al Océano Atlántico.",
        btnBookRoomCard: "Reservar esta Suite",
        perNight: "/ Noche",
        
        r1Title: "Suite Presidencial Vista Marina",
        r1Desc: "Penthouse de lujo con terraza panorámica de 180°, jacuzzi privado, salón principal y mayordomo dedicado.",
        r2Title: "Suite Marina Deluxe",
        r2Desc: "Elegante suite orientada a los superyates de la marina, baño de mármol y cama King size.",
        r3Title: "Suite Executive Spa",
        r3Desc: "Alojamiento con circuito térmico privado, bañera de hidromasaje y acceso libre al Royal Spa.",
        r4Title: "Penthouse Familiar (3 Dormitorios)",
        r4Desc: "Amplia suite familiar de 3 dormitorios con cocina completa y terraza comedero al aire libre.",
        r5Title: "Suite Royal Yacht Club",
        r5Desc: "Acceso directo al muelle de la marina con paquete VIP de yate privado y champán al atardecer.",
        r6Title: "Suite Sunset Panoramic",
        r6Desc: "Terraza orientada al oeste para disfrutar del atardecer dorado sobre el océano.",
        
        sectionDiningSub: "ALTA COCINA & COCTELES DE AUTOR",
        sectionDiningTitle: "Restaurante Gourmet & Lounge Bars",
        sectionDiningDesc: "Experiencias gastronómicas de primer nivel con pescados marinos y carta de vinos seleccionada.",
        d1Title: "Restaurante Gourmet Amura",
        d1Desc: "Alta cocina mediterránea con productos frescos del mar y vistas a la marina.",
        d2Title: "Marina Lounge & Cocktail Club",
        d2Desc: "Cócteles de autor, champán y música en vivo en la terraza sobre el agua.",
        d3Title: "Royal Marina Spa & Thermal Club",
        d3Desc: "Circuito de aguas, piscina climatizada, saunas y masajes corporales de relajación.",
        
        locationTitle: "Ubicación Privilegiada en la Marina",
        locationDesc: "Ubicado en la Marina de Albufeira, combinando tranquilidad y acceso directo a paseos en barco.",
        locAddress: "Alameda do Convento, Marina de Albufeira, 8200-394 Albufeira, Algarve, Portugal",
        locPhone: "+351 123 456 789 (Línea Directa de Reservas)",
        locHours: "Recepción y Concierge 24 Horas",
        
        modalSubtitle: "MOTOR DE RESERVAS VIP",
        modalTitle: "Confirmar Reserva de Estancia",
        modalDesc: "Rellene sus datos y fechas para enviar su solicitud al servicio de Concierge.",
        lblSelectedRoom: "Alojamiento Seleccionado",
        lblName: "Nombre Completo *",
        lblPhone: "Teléfono / WhatsApp *",
        lblEmail: "Correo Electrónico *",
        btnSubmitModal: "Enviar Reserva por WhatsApp"
    },
    fr: {
        brandTag: "5★ LUXURY RESORT & SPA • ALGARVE",
        navRooms: "Suites & Chambres",
        navDining: "Gastronomie & Bars",
        navGallery: "Galerie",
        navLocation: "Marina d'Albufeira",
        btnBookNav: "Réserver Séjour",
        
        heroBadge: "MARINA D'ALBUFEIRA • ALGARVE • PORTUGAL",
        heroTitle: "Le Luxe au Bord de la <em>Marina d'Albufeira</em>",
        heroDesc: "Un sanctuaire 5 étoiles comprenant des suites panoramiques, un restaurant gastronomique, une piscine infinie et un yacht privé.",
        btnHeroBook: "Réserver une Suite Privée",
        btnHeroRooms: "Découvrir les Suites",
        
        lblCheckIn: "Date d'Arrivée",
        lblCheckOut: "Date de Départ",
        lblGuests: "Voyageurs",
        lblCategory: "Catégorie",
        btnSearch: "Vérifier la Disponibilité",
        
        sectionRoomsSub: "HÉBERGEMENTS EXCLUSIFS 5 ÉTOILES",
        sectionRoomsTitle: "Suites & Penthouse de Luxe",
        sectionRoomsDesc: "Toutes les suites offrent un balcon privé avec vue panoramique sur la marina ou l'Océan Atlantique.",
        btnBookRoomCard: "Réserver cette Suite",
        perNight: "/ Nuit",
        
        r1Title: "Suite Présidentielle Vue Marina",
        r1Desc: "Penthouse au dernier étage avec terrasse à 180°, jacuzzi privé, grand salon et majordome dédié.",
        r2Title: "Suite Marina Deluxe",
        r2Desc: "Suite élégante donnant sur les yachts de la marina, salle de bain en marbre et lit King size.",
        r3Title: "Suite Executive Spa",
        r3Desc: "Hébergement avec circuit thermique privé, baignoire balnéo et accès illimité au Royal Spa.",
        r4Title: "Penthouse Familial (3 Chambres)",
        r4Desc: "Spacieuse suite de 3 chambres avec cuisine équipée et terrasse extérieure avec coin repas.",
        r5Title: "Suite Royal Yacht Club",
        r5Desc: "Accès direct aux pontons avec forfait VIP de yacht privé et champagne au coucher du soleil.",
        r6Title: "Suite Sunset Panoramic",
        r6Desc: "Terrasse orientée plein ouest pour admirer les couchers de soleil dorés sur l'Atlantique.",
        
        sectionDiningSub: "GASTRONOMIE & COCKTAILS DE SIGNATURE",
        sectionDiningTitle: "Restaurant Gastronomique & Bars",
        sectionDiningDesc: "Excellence culinaire mettant à l'honneur les produits frais de la mer et une carte des vins raffinée.",
        d1Title: "Restaurant Gastronomique Amura",
        d1Desc: "Haute cuisine méditerranéenne face aux yachts de la marina.",
        d2Title: "Marina Lounge & Cocktail Club",
        d2Desc: "Cocktails créatifs, champagne et musique live sur le ponton en soirée.",
        d3Title: "Royal Marina Spa & Wellness",
        d3Desc: "Bassin thermale, piscine couverte chauffée, saunas et soins de bien-être haut de gamme.",
        
        locationTitle: "Emplacement Privilégié sur la Marina",
        locationDesc: "Niché au cœur de la Marina d'Albufeira, alliant sérénité absolue et accès direct aux plus belles traversées.",
        locAddress: "Alameda do Convento, Marina d'Albufeira, 8200-394 Albufeira, Algarve, Portugal",
        locPhone: "+351 123 456 789 (Ligne Directe de Réservation)",
        locHours: "Réception & Conciergerie 24h/24",
        
        modalSubtitle: "MOTEUR DE RÉSERVATION VIP",
        modalTitle: "Confirmer la Réservation",
        modalDesc: "Renseignez vos dates de séjour pour envoyer votre demande directement à la conciergerie.",
        lblSelectedRoom: "Hébergement Sélectionné",
        lblName: "Nom Complet *",
        lblPhone: "Téléphone / WhatsApp *",
        lblEmail: "E-mail *",
        btnSubmitModal: "Envoyer la Réservation sur WhatsApp"
    }
};

let currentLang = 'pt';

document.addEventListener('DOMContentLoaded', () => {
    // Restore saved theme or default to light emerald
    const savedTheme = localStorage.getItem('hotel_theme') || 'light';
    setTheme(savedTheme);
    
    // Restore saved lang or default to PT
    const savedLang = localStorage.getItem('hotel_lang') || 'pt';
    setLanguage(savedLang);
    
    // Set default check-in and check-out dates
    setDefaultDates();
});

function setDefaultDates() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 3);
    
    const checkInInput = document.getElementById('searchCheckIn');
    const checkOutInput = document.getElementById('searchCheckOut');
    const modalDateIn = document.getElementById('vipCheckIn');
    const modalDateOut = document.getElementById('vipCheckOut');
    
    if (checkInInput && checkOutInput) {
        checkInInput.valueAsDate = today;
        checkOutInput.valueAsDate = tomorrow;
    }
    if (modalDateIn && modalDateOut) {
        modalDateIn.valueAsDate = today;
        modalDateOut.valueAsDate = tomorrow;
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('hotel_theme', theme);
    
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }
}

function setLanguage(lang) {
    if (!i18n[lang]) return;
    currentLang = lang;
    localStorage.setItem('hotel_lang', lang);
    
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    
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

// THE HOOK: Open Booking Modal prefilled with Room & Dates
function openBookingModal(roomTitle = null) {
    const modal = document.getElementById('bookingModal');
    const roomInput = document.getElementById('modalTargetRoom');
    const checkInSearch = document.getElementById('searchCheckIn')?.value;
    const checkOutSearch = document.getElementById('searchCheckOut')?.value;
    
    if (roomInput) {
        if (roomTitle) {
            roomInput.value = roomTitle;
        } else {
            const dict = i18n[currentLang];
            roomInput.value = dict['r1Title'] || 'Suite Presidencial Vista Marina';
        }
    }
    
    if (checkInSearch && document.getElementById('vipCheckIn')) {
        document.getElementById('vipCheckIn').value = checkInSearch;
    }
    if (checkOutSearch && document.getElementById('vipCheckOut')) {
        document.getElementById('vipCheckOut').value = checkOutSearch;
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

// WhatsApp Booking Submission targeting +351 123 456 789
function submitHotelBookingForm(event) {
    event.preventDefault();
    
    const name = document.getElementById('vipName').value.trim();
    const phone = document.getElementById('vipPhone').value.trim();
    const email = document.getElementById('vipEmail').value.trim();
    const room = document.getElementById('modalTargetRoom').value;
    const checkIn = document.getElementById('vipCheckIn').value;
    const checkOut = document.getElementById('vipCheckOut').value;
    const guests = document.getElementById('vipGuests')?.value || '2 Hóspedes';
    
    if (!name || !phone || !email) {
        alert("Por favor, preencha todos os campos obrigatórios (*).");
        return;
    }
    
    const message = `*RESERVA VIP — MARINA DE ALBUFEIRA LUXURY RESORT & SPA*\n\n` +
                    `🏨 *Acomodação:* ${room}\n` +
                    `📅 *Entrada (Check-In):* ${checkIn}\n` +
                    `📅 *Saída (Check-Out):* ${checkOut}\n` +
                    `👥 *Hóspedes:* ${guests}\n\n` +
                    `👤 *Nome do Hóspede:* ${name}\n` +
                    `📞 *Contacto / WhatsApp:* ${phone}\n` +
                    `✉️ *E-mail:* ${email}\n\n` +
                    `_Enviado via website oficial Marina de Albufeira Resort_`;
                    
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/351123456789?text=${encodedMessage}`;
    
    window.open(whatsappUrl, '_blank');
    closeBookingModal();
}
