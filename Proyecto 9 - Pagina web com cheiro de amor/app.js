/* ==========================================================================
   PRODUCT DATABASE (Artisanal Scented Candles, Bath Soaps, & Gift Sets)
   ========================================================================== */
const PRODUCTS = [
    {
        id: "candle-lavender",
        category: "vela",
        price: 14.90,
        image: "assets/candle_lavender.png",
        qty: 1,
        pt: {
            name: "Vela de Alfazema & Camomila",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Notas florais puras de alfazema francesa combinadas com a suavidade calmante da camomila.",
            description: "Feita à mão com cera de soja 100% natural, pavio de algodão orgânico e infundida com óleos essenciais terapêuticos de alfazema e camomila. Decorada com pétalas secas de lavanda cultivada localmente. Ideal para acalmar a mente antes de dormir ou criar um ambiente relaxante no final do dia.",
            aromaProfile: "Fresco, Floral, Relaxante, Herbal"
        },
        es: {
            name: "Vela de Lavanda & Manzanilla",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Notas florales puras de lavanda francesa combinadas con la suavidad calmante de la manzanilla.",
            description: "Hecha a mano con cera de soja 100% natural, mecha de algodón orgánico e infundida con aceites esenciales terapéuticos de lavanda y manzanilla. Decorada con pétalos secas de lavanda cultivada localmente. Ideal para calmar la mente antes de dormir o crear un ambiente relajante al final del día.",
            aromaProfile: "Fresco, Floral, Relajante, Herbal"
        },
        en: {
            name: "Lavender & Chamomile Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Pure floral notes of French lavender combined with the soothing softness of chamomile.",
            description: "Handcrafted with 100% natural soy wax, organic cotton wick, and infused with therapeutic lavender and chamomile essential oils. Decorated with dried petals of locally grown lavender. Ideal for calming the mind before sleep or creating a relaxing atmosphere at the end of the day.",
            aromaProfile: "Fresh, Floral, Relaxing, Herbal"
        },
        fr: {
            name: "Bougie Lavande & Camomille",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Notes florales pures de lavande française combinées à la douceur apaisante de la camomille.",
            description: "Fabriquée à la main avec de la cire de soja 100% naturelle, une mèche en coton biologique et infusée d'huiles essentielles thérapeutiques de lavande et de camomille. Décorée de pétales séchés de lavande cultivée localement. Idéale pour calmer l'esprit avant de dormir ou créer une ambiance relaxante en fin de journée.",
            aromaProfile: "Frais, Floral, Relaxant, Herbal"
        }
    },
    {
        id: "soap-rose",
        category: "sabonete",
        price: 5.90,
        image: "assets/soap_rose.png",
        qty: 1,
        pt: {
            name: "Sabonete de Rosas & Argila Rosa",
            categoryLabel: "Sabonete de Banho",
            aromaBrief: "Uma fragrância romântica de pétalas de rosa com as propriedades purificantes da argila rosa.",
            description: "Sabonete artesanal elaborado pelo método tradicional de saponificação a frio (cold process). Rico em óleos vegetais de amêndoas doces e manteiga de karité, nutre profundamente a pele. A argila rosa limpa suavemente as impurezas enquanto as pétalas de rosa proporcionam uma leve esfoliação natural.",
            aromaProfile: "Floral Clássico, Delicado, Atalcado, Hidratante"
        },
        es: {
            name: "Jabón de Rosas & Arcilla Rosa",
            categoryLabel: "Jabón de Baño",
            aromaBrief: "Una fragancia romántica de pétalos de rosa con las propiedades purificantes de la arcilla rosa.",
            description: "Jabón artesanal elaborado por el método tradicional de saponificación en frío (cold process). Rico en aceites vegetales de almendras dulces y manteca de karité, nutre profundamente la piel. La arcilla rosa limpia suavemente las impurezas mientras que los pétalos de rosa proporcionan una exfoliación natural suave.",
            aromaProfile: "Floral Clásico, Delicado, Atalcado, Hidratante"
        },
        en: {
            name: "Rose & Pink Clay Soap",
            categoryLabel: "Bath Soap",
            aromaBrief: "A romantic fragrance of rose petals combined with the purifying properties of pink clay.",
            description: "Handcrafted soap made using the traditional cold process saponification method. Rich in sweet almond vegetable oils and shea butter, it deeply nourishes the skin. Pink clay gently cleanses impurities while rose petals provide a gentle natural exfoliation.",
            aromaProfile: "Classic Floral, Delicate, Powdery, Moisturizing"
        },
        fr: {
            name: "Savon aux Roses & Argile Rose",
            categoryLabel: "Savon de Bain",
            aromaBrief: "Un parfum romantique de pétales de rose associé aux propriétés purifiantes de l'argile rose.",
            description: "Savon artisanal élaboré selon la méthode traditionnelle de saponification à froid (cold process). Riche en huiles végétales d'amande douce et en beurre de karité, il nourrit la peau en profondeur. L'argile rose nettoie en douceur les impuretés tandis que les pétales de rose procurent une légère exfoliation naturelle.",
            aromaProfile: "Floral Classique, Délicat, Poudré, Hydratant"
        }
    },
    {
        id: "gift-love",
        category: "set",
        price: 26.90,
        image: "assets/gift_set.png",
        qty: 1,
        pt: {
            name: "Kit Amor Eterno",
            categoryLabel: "Set de Oferta",
            aromaBrief: "O presente perfeito para celebrar o amor. Uma vela e um sabonete artesanal em caixa de luxo.",
            description: "Este conjunto exclusivo reúne o melhor de dois mundos para criar um ritual de carinho completo. Inclui: 1x Vela Aromática Premium de Cera de Soja e 1x Sabonete Artesanal Botânico. Apresentado numa caixa branca elegante com laço de cetim e flores secas decorativas.",
            aromaProfile: "Doce Floral, Sofisticado, Romântico"
        },
        es: {
            name: "Kit Amor Eterno",
            categoryLabel: "Set de Regalo",
            aromaBrief: "El regalo perfecto para celebrar el amor. Una vela y un jabón artesanal en una caja de lujo.",
            description: "Este exclusivo conjunto reúne lo mejor de dos mundos para crear un ritual de cariño completo. Incluye: 1x Vela Aromática Premium de Cera de Soja y 1x Jabón Artesanal Botánico. Presentado en una elegante caja blanca con lazo de satén y flores secas decorativas.",
            aromaProfile: "Dulce Floral, Sofisticado, Romántico"
        },
        en: {
            name: "Eternal Love Gift Set",
            categoryLabel: "Gift Set",
            aromaBrief: "The perfect gift to celebrate love. A candle and handcrafted soap in a luxury box.",
            description: "This exclusive set gathers the best of both worlds to create a complete self-care ritual. Includes: 1x Premium Soy Wax Scented Candle and 1x Botanical Handcrafted Soap. Presented in an elegant white box with a satin bow and decorative dried flowers.",
            aromaProfile: "Sweet Floral, Sophisticated, Romantic"
        },
        fr: {
            name: "Coffret Amour Éternel",
            categoryLabel: "Coffret Cadeau",
            aromaBrief: "Le cadeau parfait pour célébrer l'amour. Une bougie et un savon artisanal dans une boîte de luxe.",
            description: "Ce coffret exclusif réunit le meilleur des deux mondes pour créer un rituel de bien-être complet. Comprend : 1x Bougie Parfumée Premium en Cire de Soja et 1x Savon Artisanal Botanique. Présenté dans une élégante boîte blanche avec un ruban en satin et des fleurs séchées décoratives.",
            aromaProfile: "Doux Floral, Sophistiqué, Romantique"
        }
    },
    {
        id: "candle-orange",
        category: "vela",
        price: 14.90,
        image: "assets/candle_orange.png",
        qty: 1,
        pt: {
            name: "Vela de Laranja & Canela",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Notas vibrantes de casca de laranja combinadas com o calor exótico e reconfortante da canela.",
            description: "Uma experiência acolhedora que evoca noites aconchegantes junto à lareira. Formulada com cera de soja premium, cascas de laranja desidratadas e paus de canela no topo da vela. Uma fragrância cítrica e especiada que enche a casa de calor, energia positiva e alegria.",
            aromaProfile: "Cítrico Quente, Especiado, Aconchegante, Festivo"
        },
        es: {
            name: "Vela de Naranja & Canela",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Notas vibrantes de cáscara de naranja combinadas con el calor exótico y reconfortante de la canela.",
            description: "Una experiencia acogedora que evoca noches reconfortantes junto a la chimenea. Formulada con cera de soja premium, cáscaras de naranja deshidratadas y ramitas de canela en la parte superior de la vela. Una fragrancia cítrica y especiada que llena el hogar de calor, energía positiva y alegría.",
            aromaProfile: "Cítrico Cálido, Especiado, Acogedor, Festivo"
        },
        en: {
            name: "Orange & Cinnamon Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Vibrant notes of orange peel combined with the exotic and comforting warmth of cinnamon.",
            description: "A welcoming experience evoking cozy nights by the fireplace. Formulated with premium soy wax, dehydrated orange peels, and cinnamon sticks on top. A citrus and spiced fragrance that fills the home with warmth, positive energy, and joy.",
            aromaProfile: "Warm Citrus, Spiced, Cozy, Festive"
        },
        fr: {
            name: "Bougie Orange & Cannelle",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Notes vibrantes d'écorce d'orange combinées à la chaleur exotique et réconfortante de la cannelle.",
            description: "Une expérience chaleureuse qui évoque des nuits douillettes au coin du feu. Formulée avec de la cire de soja de qualité supérieure, des écorces d'orange déshydratées et des bâtons de cannelle sur le dessus. Une fragrance hespérisée et épicée qui remplit la maison de chaleur, d'énergie positive et de joie.",
            aromaProfile: "Agrume Chaud, Épicé, Chaleureux, Festif"
        }
    },
    {
        id: "soap-honey",
        category: "sabonete",
        price: 5.90,
        image: "assets/soap_honey.png",
        qty: 1,
        pt: {
            name: "Sabonete de Aveia & Mel de Flores",
            categoryLabel: "Sabonete de Banho",
            aromaBrief: "Notas doces e nutritivas de mel silvestre misturadas com a esfoliação suave da aveia integral.",
            description: "Altamente hidratante, acalma peles secas e sensíveis. Combina mel de abelhas local, que atua como humectante natural, com aveia triturada para uma massagem esfoliante estimulante. Produz uma espuma rica, cremosa e deliciosamente perfumada que deixa a pele incrivelmente macia.",
            aromaProfile: "Doce de Mel, Quente, Amendoado, Esfoliante"
        },
        es: {
            name: "Jabón de Avena & Miel de Flores",
            categoryLabel: "Jabón de Baño",
            aromaBrief: "Notas dulces y nutritivas de miel silvestre mezcladas con la exfoliación suave de la avena integral.",
            description: "Altamente hidratante, calma las pieles secas y sensibles. Combina miel de abejas local, que actúa como humectante natural, con avena triturada para un masaje exfoliante estimulante. Produce una espuma rica, cremosa y deliciosamente perfumada que deja la piel increíblemente suave.",
            aromaProfile: "Dulce de Miel, Cálido, Almendrado, Exfoliante"
        },
        en: {
            name: "Oatmeal & Flower Honey Soap",
            categoryLabel: "Bath Soap",
            aromaBrief: "Sweet and nourishing wild honey notes mixed with the gentle exfoliation of whole oats.",
            description: "Highly moisturizing, it soothes dry and sensitive skins. Combines local bee honey, which acts as a natural humectant, with ground oats for a stimulating exfoliating massage. Produces a rich, creamy, and deliciously scented lather that leaves skin incredibly soft.",
            aromaProfile: "Sweet Honey, Warm, Nutty, Exfoliating"
        },
        fr: {
            name: "Savon Flocons d'Avoine & Miel",
            categoryLabel: "Savon de Bain",
            aromaBrief: "Des notes douces et nourrissantes de miel sauvage mélangées à l'exfoliation douce de l'avoine entière.",
            description: "Hautement hydratant, il apaise les peaux sèches et sensibles. Il combine le miel d'abeilles local, qui agit comme un humectant naturel, et l'avoine moulue pour un massage exfoliant stimulant. Produit une mousse riche, crémeuse et délicieusement parfumée qui laisse la peau incroyablement douce.",
            aromaProfile: "Doux de Miel, Chaud, Amande, Exfoliant"
        }
    },
    {
        id: "gift-spa",
        category: "set",
        price: 32.90,
        image: "assets/gift_relax.png",
        qty: 1,
        pt: {
            name: "Kit Ritual de Spa Relax",
            categoryLabel: "Set de Oferta",
            aromaBrief: "Uma experiência de bem-estar completa para transformar a sua casa num verdadeiro spa de luxo.",
            description: "Mime-se com este kit projetado para relaxamento profundo. Contém: 1x Vela Aromática de Alfazema (tamanho regular), 1x Sabonete de Rosas, 1x Toalha de Algodão Macio e 1x Sal de Banho Aromático com ervas naturais numa bandeja de bambu reutilizável.",
            aromaProfile: "Herbal, Calma, Aromaterapia Completa"
        },
        es: {
            name: "Kit Ritual de Spa Relax",
            categoryLabel: "Set de Regalo",
            aromaBrief: "Una experiencia de bienestar completa para transformar tu hogar en un verdadero spa de lujo.",
            description: "Mímate con este kit diseñado para una relajación profunda. Contiene: 1x Vela Aromática de Lavanda (tamaño regular), 1x Jabón de Rosas, 1x Toalla de Algodón Suave y 1x Sal de Baño Aromática con hierbas naturales en una bandeja de bambú reutilizable.",
            aromaProfile: "Herbal, Calma, Aromaterapia Completa"
        },
        en: {
            name: "Relaxing Spa Ritual Set",
            categoryLabel: "Gift Set",
            aromaBrief: "A complete wellness experience to transform your home into a true luxury spa.",
            description: "Pamper yourself with this kit designed for deep relaxation. Contains: 1x Lavender Scented Candle (regular size), 1x Rose Soap, 1x Soft Cotton Towel, and 1x Aromatic Bath Salt with natural herbs on a reusable bamboo tray.",
            aromaProfile: "Herbal, Calm, Complete Aromatherapy"
        },
        fr: {
            name: "Coffret Rituel Spa Relax",
            categoryLabel: "Coffret Cadeau",
            aromaBrief: "Une expérience de bien-être complète pour transformer votre maison en un véritable spa de luxe.",
            description: "Prenez soin de vous avec ce coffret conçu pour une relaxation profonde. Contient : 1x Bougie Parfumée à la Lavande (taille normale), 1x Savon aux Roses, 1x Serviette en Coton Doux et 1x Sel de Bain Aromatique aux herbes naturelles dans un plateau en bambou réutilisable.",
            aromaProfile: "Herbal, Calme, Aromathérapie Complète"
        }
    }
];

// WhatsApp Contact Configuration
const WHATSAPP_NUMBER = "351939636842";

// Global i18n & Cart State
let currentLang = "pt";
let cart = [];

/* ==========================================================================
   GLOBAL DICTIONARY OF TRANSLATIONS (PT, ES, EN, FR)
   ========================================================================== */
const TRANSLATIONS = {
    // Navigation
    "logo-sub": {
        pt: "Velas & Sabonetes",
        es: "Velas & Jabones",
        en: "Candles & Soaps",
        fr: "Bougies & Savons"
    },
    "nav-link-home": {
        pt: "Início",
        es: "Inicio",
        en: "Home",
        fr: "Accueil"
    },
    "nav-link-catalogo": {
        pt: "Catálogo",
        es: "Catálogo",
        en: "Catalog",
        fr: "Catalogue"
    },
    "nav-link-historia": {
        pt: "A Nossa História",
        es: "Nuestra Historia",
        en: "Our Story",
        fr: "Notre Histoire"
    },
    "nav-link-contacto": {
        pt: "Contacto",
        es: "Contacto",
        en: "Contact",
        fr: "Contact"
    },
    
    // Hero
    "hero-badge": {
        pt: "Artesanal & Natural",
        es: "Artesanal & Natural",
        en: "Handcrafted & Natural",
        fr: "Artisanal & Naturel"
    },
    "hero-title": {
        pt: "Feito à mão, <br><span>com cheiro de amor</span>",
        es: "Hecho a mano, <br><span>con aroma de amor</span>",
        en: "Handcrafted, <br><span>with a scent of love</span>",
        fr: "Fait main, <br><span>avec un parfum d'amour</span>"
    },
    "hero-desc": {
        pt: "Transforme a atmosfera do seu lar com a nossa coleção exclusiva de velas de cera de soja natural e sabonetes de banho aromáticos. Criados com alma, cuidado e carinho.",
        es: "Transforma la atmósfera de tu hogar con nuestra colección exclusiva de velas de cera de soja natural y jabones de baño aromáticos. Creados con alma, cuidado y cariño.",
        en: "Transform your home's atmosphere with our exclusive collection of natural soy wax candles and aromatic bath soaps. Crafted with soul, care, and love.",
        fr: "Transformez l'atmosphère de votre foyer avec notre collection exclusive de bougies en cire de soja naturelle et de savons de bain aromatiques. Créés avec âme, soin et tendresse."
    },
    "btn-hero-shop": {
        pt: 'Explorar Catálogo <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>',
        es: 'Explorar Catálogo <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>',
        en: 'Explore Catalog <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>',
        fr: 'Explorer le Catalogue <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>'
    },
    "btn-hero-contact": {
        pt: "Falar no WhatsApp",
        es: "Hablar por WhatsApp",
        en: "Chat on WhatsApp",
        fr: "Discuter sur WhatsApp"
    },
    
    // Catalog Header & Filters
    "catalog-subtitle": {
        pt: "A Nossa Coleção",
        es: "Nuestra Colección",
        en: "Our Collection",
        fr: "Notre Collection"
    },
    "catalog-title": {
        pt: "Fragrâncias que Encantam",
        es: "Fragancias que Encantan",
        en: "Fragrances that Enchant",
        fr: "Des Fragrances qui Enchantent"
    },
    "filter-all": {
        pt: "Todos os Produtos",
        es: "Todos los Productos",
        en: "All Products",
        fr: "Tous les Produits"
    },
    "filter-velas": {
        pt: "Velas Aromáticas",
        es: "Velas Aromáticas",
        en: "Scented Candles",
        fr: "Bougies Parfumées"
    },
    "filter-sabonetes": {
        pt: "Sabonetes de Banho",
        es: "Jabones de Baño",
        en: "Bath Soaps",
        fr: "Savons de Bain"
    },
    "filter-sets": {
        pt: "Sets de Oferta",
        es: "Sets de Regalo",
        en: "Gift Sets",
        fr: "Coffrets Cadeau"
    },
    
    // Story
    "story-subtitle": {
        pt: "O Nosso Começo",
        es: "Nuestro Comienzo",
        en: "Our Beginning",
        fr: "Nos Débuts"
    },
    "story-title": {
        pt: "A Nossa História",
        es: "Nuestra Historia",
        en: "Our Story",
        fr: "Notre Histoire"
    },
    "story-quote-text": {
        pt: '"Criamos experiências olfativas que aquecem o coração e transformam momentos simples em memórias doces e inesquecíveis."',
        es: '"Creamos experiencias olfativas que calientan el corazón y transforman momentos sencillos en recuerdos dulces e inolvidables."',
        en: '"We create olfactory experiences that warm the heart and transform simple moments into sweet and unforgettable memories."',
        fr: '"Nous créons des expériences olfactives qui réchauffent le cœur et transforment des moments simples en souvenirs doux et inoubliables."'
    },
    "story-body-text": {
        pt: 'A <strong>Com Cheiro de Amor</strong> nasceu do desejo de trazer mais luz, paz e bem-estar para o dia a dia das pessoas. Cada produto é idealizado e criado artesanalmente em pequenos lotes em Portugal. <br><br>Utilizamos cera de soja vegetal ecológica e óleos de fragrância premium para as nossas velas, garantindo uma queima limpa, duradoura e respeitadora do ambiente. Os nossos sabonetes são elaborados com manteigas vegetais hidratantes e ingredientes botânicos que nutrem e perfumam a pele de forma natural.',
        es: '<strong>Com Cheiro de Amor</strong> nació del deseo de traer más luz, paz y bienestar al día a día de las personas. Cada producto es idealizado y creado artesanalmente en pequeños lotes en Portugal. <br><br>Utilizamos cera de soja vegetal ecológica y aceites de fragancia premium para nuestras velas, garantizando una combustión limpia, duradera y respetuosa con el medio ambiente. Nuestros jabones se elaboran con mantecas vegetales hidratantes e ingredientes botánicos que nutren y perfuman la piel de forma natural.',
        en: '<strong>Com Cheiro de Amor</strong> was born from the desire to bring more light, peace, and well-being into people\'s daily lives. Each product is conceptualized and handcrafted in small batches in Portugal. <br><br>We use ecological vegetable soy wax and premium fragrance oils for our candles, ensuring a clean, long-lasting, and environmentally friendly burn. Our soaps are formulated with moisturizing plant butters and botanical ingredients that naturally nourish and perfume the skin.',
        fr: '<strong>Com Cheiro de Amor</strong> est né du désir d\'apporter plus de lumière, de paix et de bien-être dans le quotidien des gens. Chaque produit est imaginé et créé artisanalement en petits lots au Portugal. <br><br>Nous utilisons de la cire de soja végétale écologique et des huiles parfumées de qualité supérieure pour nos bougies, garantissant une combustion propre, durable et respectueuse de l\'environnement. Nos savons sont élaborés avec des beurres végétaux hydratants et des ingrédients botaniques qui nourrissent et parfument la peau de manière naturelle.'
    },
    "story-sig": {
        pt: "Com carinho, Com Cheiro de Amor",
        es: "Con cariño, Com Cheiro de Amor",
        en: "With love, Com Cheiro de Amor",
        fr: "Avec amour, Com Cheiro de Amor"
    },
    
    // Cart Drawer
    "cart-drawer-title": {
        pt: "O seu Carrinho",
        es: "Su Carrito",
        en: "Your Cart",
        fr: "Votre Panier"
    },
    "cart-total-label": {
        pt: "Total Estimado",
        es: "Total Estimado",
        en: "Estimated Total",
        fr: "Total Estimé"
    },
    "cart-notes-label": {
        pt: "Observações ou Dúvidas",
        es: "Observaciones o Dudas",
        en: "Notes or Inquiries",
        fr: "Remarques ou Questions"
    },
    "btn-whatsapp-send-text": {
        pt: "Enviar Pedido por WhatsApp",
        es: "Enviar Pedido por WhatsApp",
        en: "Send Order via WhatsApp",
        fr: "Envoyer la Commande via WhatsApp"
    },
    
    // Modal Detail
    "aroma-label-text": {
        pt: "Perfil Olfativo",
        es: "Perfil Olfativo",
        en: "Scent Profile",
        fr: "Profil Olfactif"
    },
    "btn-modal-add-text": {
        pt: "Adicionar ao Carrinho",
        es: "Añadir al Carrito",
        en: "Add to Cart",
        fr: "Ajouter au Panier"
    },
    
    // Footer Link columns
    "footer-links-title": {
        pt: "Links Rápidos",
        es: "Enlaces Rápidos",
        en: "Quick Links",
        fr: "Liens Rapides"
    },
    "footer-link-home": {
        pt: "Início",
        es: "Inicio",
        en: "Home",
        fr: "Accueil"
    },
    "footer-link-catalogo": {
        pt: "Catálogo",
        es: "Catálogo",
        en: "Catalog",
        fr: "Catalogue"
    },
    "footer-link-historia": {
        pt: "A Nossa História",
        es: "Nuestra Historia",
        en: "Our Story",
        fr: "Notre Histoire"
    },
    "footer-link-contacto": {
        pt: "Contacto",
        es: "Contacto",
        en: "Contact",
        fr: "Contact"
    },
    "footer-info-title": {
        pt: "Informações",
        es: "Información",
        en: "Information",
        fr: "Informations"
    },
    "footer-info-candles": {
        pt: "Velas Aromáticas",
        es: "Velas Aromáticas",
        en: "Scented Candles",
        fr: "Bougies Parfumées"
    },
    "footer-info-soaps": {
        pt: "Sabonetes Botânicos",
        es: "Jabones Botánicos",
        en: "Botanical Soaps",
        fr: "Savons Botaniques"
    },
    "footer-info-shipping": {
        pt: "Prazos de Envio",
        es: "Plazos de Envío",
        en: "Shipping Times",
        fr: "Délais de Livraison"
    },
    "footer-info-custom": {
        pt: "Encomendas Especiais",
        es: "Pedidos Especiales",
        en: "Custom Orders",
        fr: "Commandes Spéciales"
    },
    "footer-contact-title": {
        pt: "Contacto Direto",
        es: "Contacto Directo",
        en: "Direct Contact",
        fr: "Contact Direct"
    },
    "footer-desc-text": {
        pt: "Artesanato delicado e aromas únicos que enchem a sua casa de paz, luz e harmonia. Feito com alma em Portugal.",
        es: "Artesanía delicada y aromas únicos que llenan su hogar de paz, luz y armonía. Hecho con alma en Portugal.",
        en: "Delicate craftsmanship and unique aromas that fill your home with peace, light, and harmony. Handcrafted with soul in Portugal.",
        fr: "Artisanat délicat et arômes uniques qui remplissent votre maison de paix, de lumière et d'harmonie. Fait avec âme au Portugal."
    },
    "footer-loc-text": {
        pt: "Faro, Portugal <br>(Envios para todo o mundo)",
        es: "Faro, Portugal <br>(Envíos a todo el mundo)",
        en: "Faro, Portugal <br>(Worldwide shipping)",
        fr: "Faro, Portugal <br>(Livraison dans le monde entier)"
    },
    "footer-copy-text": {
        pt: "&copy; 2026 Com Cheiro de Amor. Todos os direitos reservados.",
        es: "&copy; 2026 Com Cheiro de Amor. Todos los derechos reservados.",
        en: "&copy; 2026 Com Cheiro de Amor. All rights reserved.",
        fr: "&copy; 2026 Com Cheiro de Amor. Tous droits réservés."
    },
    "footer-made-text": {
        pt: "Feito à mão com ingredientes naturais e muito carinho.",
        es: "Hecho a mano con ingredientes naturales y mucho cariño.",
        en: "Handcrafted with natural ingredients and lots of love.",
        fr: "Fait main avec des ingrédients naturels et beaucoup d'amour."
    }
};

// Dynamic Helpers
const GRID_ADD_BUTTONS = {
    pt: "Adicionar",
    es: "Añadir",
    en: "Add to Cart",
    fr: "Ajouter"
};

const GRID_ADDED_BUTTONS = {
    pt: "Adicionado ✓",
    es: "Añadido ✓",
    en: "Added ✓",
    fr: "Ajouté ✓"
};

const CART_PLACEHOLDERS = {
    pt: "Ex: Adicionar caixa de presente, aromas preferidos, embalagem personalizada...",
    es: "Ej: Añadir caja de regalo, aromas preferidos, embalaje personalizado...",
    en: "E.g.: Add a gift box, preferred scents, custom packaging...",
    fr: "Ex : Ajouter un coffret cadeau, parfums préférés, emballage personnalisé..."
};

const CART_EMPTY_MESSAGES = {
    pt: {
        main: "O seu carrinho está vazio.",
        sub: "Explore o nosso catálogo e adicione os aromas que mais lhe agradam!"
    },
    es: {
        main: "Su carrito está vacío.",
        sub: "¡Explore nuestro catálogo y añada los aromas que más le gusten!"
    },
    en: {
        main: "Your cart is empty.",
        sub: "Explore our catalog and add the scents you like best!"
    },
    fr: {
        main: "Votre panier est vide.",
        sub: "Explorez notre catalogue et ajoutez les parfums qui vous plaisent le plus!"
    }
};

const WHATSAPP_TEMPLATES = {
    pt: {
        greeting: "Olá! Gostaria de consultar a disponibilidade dos seguintes produtos de *Com Cheiro de Amor*:\n\n",
        qty: "Qtd",
        totalLabel: "Valor Estimado",
        notesLabel: "Mensagem/Observações",
        footer: "Por favor, indique-me a disponibilidade e os prazos de entrega / métodos de envio. Muito obrigado(a)!"
    },
    es: {
        greeting: "¡Hola! Me gustaría consultar la disponibilidad de los siguientes productos de *Com Cheiro de Amor*:\n\n",
        qty: "Cant",
        totalLabel: "Valor Estimado",
        notesLabel: "Mensaje/Observaciones",
        footer: "Por favor, indíqueme la disponibilidad y los plazos de entrega / métodos de envío. ¡Muchas gracias!"
    },
    en: {
        greeting: "Hello! I would like to check the availability of the following products from *Com Cheiro de Amor*:\n\n",
        qty: "Qty",
        totalLabel: "Estimated Value",
        notesLabel: "Message/Special Notes",
        footer: "Please let me know the availability, delivery times, and shipping methods. Thank you very much!"
    },
    fr: {
        greeting: "Bonjour ! Je souhaiterais vérifier la disponibilité des produits suivants chez *Com Cheiro de Amor*:\n\n",
        qty: "Qté",
        totalLabel: "Valeur Estimée",
        notesLabel: "Message/Remarques",
        footer: "Veuillez m'indiquer la disponibilité, les délais de livraison et les modes d'expédition. Merci beaucoup !"
    }
};

/* ==========================================================================
   DOM ELEMENTS & INITIALIZATION
   ========================================================================== */
document.addEventListener("DOMContentLoaded", () => {
    // Nav elements
    const navbar = document.querySelector(".navbar");
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    const langSelect = document.getElementById("lang-select");
    
    // Cart elements
    const cartToggleBtn = document.querySelector(".cart-toggle");
    const cartDrawer = document.querySelector(".cart-drawer");
    const cartCloseBtn = document.querySelector(".cart-close-btn");
    const cartOverlay = document.querySelector(".cart-overlay");
    const cartCountEl = document.querySelector(".cart-count");
    const cartItemsWrapper = document.querySelector(".cart-items-wrapper");
    const cartTotalPriceEl = document.querySelector(".cart-total-price");
    const cartNotesEl = document.querySelector(".cart-notes");
    const whatsappCheckoutBtn = document.querySelector(".btn-whatsapp-checkout");

    // Modal elements
    const modal = document.querySelector(".modal");
    const modalCloseBtn = document.querySelector(".modal-close-btn");
    const modalBackdrop = document.querySelector(".modal-backdrop");
    const modalImg = document.querySelector(".modal-img");
    const modalCategory = document.querySelector(".modal-category");
    const modalTitle = document.querySelector(".modal-title");
    const modalPrice = document.querySelector(".modal-price");
    const modalDescription = document.querySelector(".modal-description");
    const aromaNotes = document.querySelector(".aroma-notes");
    const modalQtyNum = document.querySelector(".modal-qty-selector .qty-num");
    const modalMinusBtn = document.querySelector(".modal-qty-selector .qty-btn:first-child");
    const modalPlusBtn = document.querySelector(".modal-qty-selector .qty-btn:last-child");
    const modalAddToCartBtn = document.querySelector(".modal-info-panel .btn-primary");

    // Dynamic state variables for modal
    let activeModalProductId = null;
    let activeModalQty = 1;

    // Scroll Navbar Effect
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    // Mobile Menu Toggle
    menuToggle.addEventListener("click", () => {
        navLinks.classList.toggle("open");
        menuToggle.classList.toggle("active");
        
        // Simple visual change for hamburger to X
        const bars = menuToggle.querySelectorAll("span");
        if (menuToggle.classList.contains("active")) {
            bars[0].style.transform = "rotate(45deg) translate(6px, 6px)";
            bars[1].style.opacity = "0";
            bars[2].style.transform = "rotate(-45deg) translate(5px, -6px)";
        } else {
            bars[0].style.transform = "none";
            bars[1].style.opacity = "1";
            bars[2].style.transform = "none";
        }
    });

    // Close Mobile Menu on link click
    navLinks.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("open");
            menuToggle.classList.remove("active");
            menuToggle.querySelectorAll("span").forEach(bar => bar.style.transform = "none");
            menuToggle.querySelectorAll("span")[1].style.opacity = "1";
        });
    });

    /* ==========================================================================
   MULTI-LANGUAGE TRANSITION CONTROLLER (i18n)
   ========================================================================== */
    const setLanguage = (lang) => {
        currentLang = lang;
        document.documentElement.lang = lang;

        // Apply dynamic fadeout to body for premium transitions
        document.body.classList.add("lang-fade-active");

        setTimeout(() => {
            // Translate static elements
            for (const [id, translations] of Object.entries(TRANSLATIONS)) {
                const el = document.getElementById(id);
                if (el) {
                    if (id === "hero-title" || id === "story-body-text" || id === "footer-loc-text" || id === "btn-hero-shop") {
                        el.innerHTML = translations[lang];
                    } else {
                        el.textContent = translations[lang];
                    }
                }
            }

            // Translate cart special notes placeholder
            if (cartNotesEl) {
                cartNotesEl.placeholder = CART_PLACEHOLDERS[lang];
            }

            // Re-render product catalog under active category filter
            const activeFilterTab = document.querySelector(".filter-tab.active");
            const activeFilter = activeFilterTab ? activeFilterTab.getAttribute("data-filter") : "all";
            renderProducts(activeFilter);

            // Re-render cart elements
            renderCart();

            // Fade back in smoothly
            document.body.classList.remove("lang-fade-active");
        }, 150);
    };

    // Attach Selector Change Event Listener
    if (langSelect) {
        langSelect.addEventListener("change", (e) => {
            setLanguage(e.target.value);
        });
    }

    /* ==========================================================================
       CART DRAWER MANAGEMENT
       ========================================================================== */
    const openCart = () => {
        cartDrawer.classList.add("open");
        cartOverlay.classList.add("active");
        renderCart();
    };

    const closeCart = () => {
        cartDrawer.classList.remove("open");
        cartOverlay.classList.remove("active");
    };

    cartToggleBtn.addEventListener("click", openCart);
    cartCloseBtn.addEventListener("click", closeCart);
    cartOverlay.addEventListener("click", closeCart);

    /* ==========================================================================
       PRODUCT GRID DYNAMIC RENDERING & FILTERING
       ========================================================================== */
    const productsGrid = document.querySelector(".products-grid");
    const filterTabs = document.querySelectorAll(".filter-tab");

    const renderProducts = (categoryFilter = "all") => {
        productsGrid.innerHTML = "";
        
        const filteredProducts = categoryFilter === "all" 
            ? PRODUCTS 
            : PRODUCTS.filter(p => p.category === categoryFilter);

        filteredProducts.forEach(product => {
            const translation = product[currentLang];
            const card = document.createElement("div");
            card.className = "product-card";
            card.setAttribute("data-id", product.id);
            
            card.innerHTML = `
                <div class="product-image-container">
                    <span class="product-badge">${translation.categoryLabel}</span>
                    <img src="${product.image}" alt="${translation.name}" class="product-img" loading="lazy">
                    <div class="product-overlay">
                        <button class="btn-icon btn-view" title="Ver Detalhes" data-id="${product.id}">
                            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        </button>
                        <button class="btn-icon btn-quick-add" title="Adicionar Rápido" data-id="${product.id}">
                            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
                        </button>
                    </div>
                </div>
                <div class="product-info">
                    <span class="product-category">${translation.categoryLabel}</span>
                    <h3 class="product-name">${translation.name}</h3>
                    <p class="product-aroma-brief">${translation.aromaBrief}</p>
                    <div class="product-footer">
                        <span class="product-price">€${product.price.toFixed(2)}</span>
                        <button class="btn-add-cart" data-id="${product.id}">
                            ${GRID_ADD_BUTTONS[currentLang]}
                            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
                        </button>
                    </div>
                </div>
            `;
            productsGrid.appendChild(card);
        });

        // Add event listeners to newly created product buttons
        attachProductEventListeners();
    };

    // Filter Navigation Click Handler
    filterTabs.forEach(tab => {
        tab.addEventListener("click", (e) => {
            filterTabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            
            const filterValue = tab.getAttribute("data-filter");
            
            // Subtle transition effect
            productsGrid.style.opacity = "0";
            productsGrid.style.transform = "translateY(15px)";
            
            setTimeout(() => {
                renderProducts(filterValue);
                productsGrid.style.opacity = "1";
                productsGrid.style.transform = "translateY(0)";
            }, 300);
        });
    });

    /* ==========================================================================
       PRODUCT EVENT LISTENERS (Quick View & Add to Cart)
       ========================================================================== */
    function attachProductEventListeners() {
        // Quick Add & Normal Add Buttons
        const addButtons = document.querySelectorAll(".btn-quick-add, .btn-add-cart");
        addButtons.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                const productId = btn.getAttribute("data-id");
                addToCart(productId, 1);
                
                // Visual feedback on button (briefly change state)
                const originalContent = btn.innerHTML;
                if (btn.classList.contains("btn-add-cart")) {
                    btn.innerHTML = `${GRID_ADDED_BUTTONS[currentLang]}`;
                    btn.style.color = "var(--color-whatsapp)";
                    setTimeout(() => {
                        btn.innerHTML = originalContent;
                        btn.style.color = "";
                    }, 1500);
                } else {
                    btn.style.backgroundColor = "var(--color-whatsapp)";
                    btn.style.color = "var(--color-white)";
                    setTimeout(() => {
                        btn.style.backgroundColor = "";
                        btn.style.color = "";
                    }, 1000);
                }
                
                openCart();
            });
        });

        // Quick View (Modal triggers)
        const viewButtons = document.querySelectorAll(".btn-view");
        const productCards = document.querySelectorAll(".product-card");

        const triggerView = (productId) => {
            openProductModal(productId);
        };

        viewButtons.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                triggerView(btn.getAttribute("data-id"));
            });
        });

        // Clicking the whole card opens details too
        productCards.forEach(card => {
            card.addEventListener("click", () => {
                triggerView(card.getAttribute("data-id"));
            });
        });
    }

    /* ==========================================================================
       PRODUCT DETAIL MODAL LOGIC
       ========================================================================== */
    const openProductModal = (productId) => {
        const product = PRODUCTS.find(p => p.id === productId);
        if (!product) return;

        activeModalProductId = productId;
        activeModalQty = 1;

        const translation = product[currentLang];

        // Populate Modal Fields
        modalImg.src = product.image;
        modalImg.alt = translation.name;
        modalCategory.textContent = translation.categoryLabel;
        modalTitle.textContent = translation.name;
        modalPrice.textContent = `€${product.price.toFixed(2)}`;
        modalDescription.textContent = translation.description;
        aromaNotes.textContent = translation.aromaProfile;
        
        modalQtyNum.textContent = activeModalQty;

        // Show Modal
        modal.classList.add("active");
    };

    const closeProductModal = () => {
        modal.classList.remove("active");
        activeModalProductId = null;
    };

    modalCloseBtn.addEventListener("click", closeProductModal);
    modalBackdrop.addEventListener("click", closeProductModal);

    // Modal Quantity Controls
    modalMinusBtn.addEventListener("click", () => {
        if (activeModalQty > 1) {
            activeModalQty--;
            modalQtyNum.textContent = activeModalQty;
        }
    });

    modalPlusBtn.addEventListener("click", () => {
        activeModalQty++;
        modalQtyNum.textContent = activeModalQty;
    });

    // Add to Cart from Modal
    modalAddToCartBtn.addEventListener("click", () => {
        if (activeModalProductId) {
            addToCart(activeModalProductId, activeModalQty);
            closeProductModal();
            openCart();
        }
    });

    /* ==========================================================================
       CART & INTERACTIVE SHOPPING LOGIC
       ========================================================================== */
    const addToCart = (productId, qty) => {
        const product = PRODUCTS.find(p => p.id === productId);
        if (!product) return;

        const existingItem = cart.find(item => item.id === productId);

        if (existingItem) {
            existingItem.qty += qty;
        } else {
            cart.push({
                ...product,
                qty: qty
            });
        }

        updateCartCount();
    };

    const removeFromCart = (productId) => {
        cart = cart.filter(item => item.id !== productId);
        updateCartCount();
        renderCart();
    };

    const updateQty = (productId, change) => {
        const item = cart.find(item => item.id === productId);
        if (!item) return;

        item.qty += change;

        if (item.qty <= 0) {
            removeFromCart(productId);
        } else {
            updateCartCount();
            renderCart();
        }
    };

    const updateCartCount = () => {
        const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
        cartCountEl.textContent = totalItems;
        
        // Add dynamic heartbeat effect if count increases
        cartCountEl.classList.remove("animate-pulse");
        void cartCountEl.offsetWidth; // Trigger reflow
        cartCountEl.classList.add("animate-pulse");
    };

    const renderCart = () => {
        cartItemsWrapper.innerHTML = "";
        
        if (cart.length === 0) {
            cartItemsWrapper.innerHTML = `
                <div class="cart-empty-message">
                    <svg width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
                    <p id="cart-empty-text">${CART_EMPTY_MESSAGES[currentLang].main}</p>
                    <p style="font-size: 0.8rem; font-weight: normal; color: var(--color-text-muted);">${CART_EMPTY_MESSAGES[currentLang].sub}</p>
                </div>
            `;
            cartTotalPriceEl.textContent = "€0.00";
            return;
        }

        let total = 0;

        cart.forEach(item => {
            const itemTotal = item.price * item.qty;
            total += itemTotal;

            const translation = item[currentLang];

            const itemEl = document.createElement("div");
            itemEl.className = "cart-item";
            itemEl.innerHTML = `
                <img src="${item.image}" alt="${translation.name}" class="cart-item-img">
                <div class="cart-item-detail">
                    <div>
                        <span class="cart-item-category">${translation.categoryLabel}</span>
                        <h4 class="cart-item-name">${translation.name}</h4>
                    </div>
                    <div class="cart-item-qty">
                        <button class="qty-btn btn-qty-minus" data-id="${item.id}">-</button>
                        <span class="qty-num">${item.qty}</span>
                        <button class="qty-btn btn-qty-plus" data-id="${item.id}">+</button>
                        <span class="cart-item-price" style="margin-left: auto;">€${itemTotal.toFixed(2)}</span>
                    </div>
                </div>
                <button class="cart-item-remove" data-id="${item.id}">
                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
            `;
            cartItemsWrapper.appendChild(itemEl);
        });

        cartTotalPriceEl.textContent = `€${total.toFixed(2)}`;

        // Attach listeners for cart actions
        const minusBtns = cartItemsWrapper.querySelectorAll(".btn-qty-minus");
        const plusBtns = cartItemsWrapper.querySelectorAll(".btn-qty-plus");
        const removeBtns = cartItemsWrapper.querySelectorAll(".cart-item-remove");

        minusBtns.forEach(btn => {
            btn.addEventListener("click", () => updateQty(btn.getAttribute("data-id"), -1));
        });

        plusBtns.forEach(btn => {
            btn.addEventListener("click", () => updateQty(btn.getAttribute("data-id"), 1));
        });

        removeBtns.forEach(btn => {
            btn.addEventListener("click", () => removeFromCart(btn.getAttribute("data-id")));
        });
    };

    /* ==========================================================================
       WHATSAPP ORDER COMPILER & REDIRECTION (LOCALIZED TO SELECTED LANGUAGE)
       ========================================================================== */
    whatsappCheckoutBtn.addEventListener("click", () => {
        if (cart.length === 0) return;

        const template = WHATSAPP_TEMPLATES[currentLang];

        // Build elegant, translatable WhatsApp message
        let message = template.greeting;
        
        let total = 0;
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.qty;
            total += itemTotal;
            const translation = item[currentLang];
            message += `*${index + 1}. ${translation.name}*\n`;
            message += `   ${template.qty}: ${item.qty} x €${item.price.toFixed(2)} = *€${itemTotal.toFixed(2)}*\n\n`;
        });

        message += `--------------------------------\n`;
        message += `*${template.totalLabel}:* €${total.toFixed(2)}\n\n`;

        // Append custom user note if present
        const note = cartNotesEl.value.trim();
        if (note) {
            message += `*${template.notesLabel}:* _"${note}"_\n\n`;
        }

        message += template.footer;

        // URL encode the message
        const encodedMessage = encodeURIComponent(message);
        const whatsappUrl = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodedMessage}`;

        // Open WhatsApp in a new tab
        window.open(whatsappUrl, "_blank");
    });

    /* ==========================================================================
       APPLICATION START
       ========================================================================== */
    // Initialize default products render
    renderProducts("all");
    updateCartCount();
});
