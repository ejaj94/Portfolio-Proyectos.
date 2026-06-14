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
            aromaBrief: "Notes vibrantes d\'écorce d\'orange combinées à la chaleur exotique et réconfortante de la cannelle.",
            description: "Une expérience chaleureuse qui évoque des nuits douillettes au coin du feu. Formulée avec de la cire de soja de qualité supérieure, des écorces d\'orange déshydratées et des bâtons de cannelle sur le dessus. Une fragrance hespérisée et épicée qui réchauffe l\'atmosphère, apportant de l\'énergie positive et de la joie.",
            aromaProfile: "Agrume Chaud, Épicé, Chaleureux, Festif"
        }
    },

    {
        id: "candle-benedita-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_benedita_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Escultural Benedita",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Silhueta clássica e artística com um aroma suave e reconfortante.",
            description: "Busto feminino clássico esculpido à mão em cera de soja eco-friendly. Um toque de arte e sofisticação para decorar e perfumar a sua casa.",
            aromaProfile: "Floral Suave, Baunilha, Delicado"
        },
        es: {
            name: "Vela Escultural Benedita",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Silueta clásica y artística con un aroma suave y reconfortante.",
            description: "Busto femenino clásico esculpido a mano en cera de soja ecológica. Un toque de arte y sofisticación para decorar y perfumar tu hogar.",
            aromaProfile: "Floral Suave, Vainilla, Delicado"
        },
        en: {
            name: "Benedita Sculptural Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Classic and artistic silhouette with a soft, comforting scent.",
            description: "Classic female bust handcrafted from eco-friendly soy wax. A touch of art and sophistication to decorate and scent your home.",
            aromaProfile: "Soft Floral, Vanilla, Delicate"
        },
        fr: {
            name: "Bougie Sculpturale Benedita",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Silhouette classique et artistique au parfum doux et réconfortant.",
            description: "Buste féminin classique sculpté à la main en cire de soja écologique. Une touche d'art et de sophistication pour décorer et parfumer votre maison.",
            aromaProfile: "Floral Doux, Vanille, Délicat"
        }
    },
    {
        id: "candle-big_bear-1",
        category: "vela",
        price: 15.90,
        image: "assets/candle_big_bear_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Escultural Urso Gigante",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Lindo urso esculpido em cera de soja, traz calor e doçura ao ambiente.",
            description: "Ursinho fofo esculpido em cera de soja biodegradável, perfeito para decorar quartos de crianças ou criar uma atmosfera acolhedora e divertida.",
            aromaProfile: "Doce Caramelo, Mel, Baunilha"
        },
        es: {
            name: "Vela Escultural Oso Gigante",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Lindo oso esculpido en cera de soja, trae calidez y dulzura al hogar.",
            description: "Lindo osito esculpido en cera de soja biodegradable, perfecto para decorar habitaciones infantiles o crear una atmósfera acogedora y divertida.",
            aromaProfile: "Dulce Caramelo, Miel, Vainilla"
        },
        en: {
            name: "Big Bear Sculptural Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Cute bear sculpted in soy wax, bringing warmth and sweetness.",
            description: "Cute little bear sculpted from biodegradable soy wax, perfect for decorating children's rooms or creating a cozy, fun atmosphere.",
            aromaProfile: "Sweet Caramel, Honey, Vanilla"
        },
        fr: {
            name: "Bougie Sculpturale Gros Ourson",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Joli ourson sculpté en cire de soja, apportant chaleur et douceur.",
            description: "Joli petit ourson sculpté en cire de soja biodégradable, parfait pour décorer les chambres d'enfants ou créer une ambiance chaleureuse et ludique.",
            aromaProfile: "Caramel Doux, Miel, Vanille"
        }
    },
    {
        id: "candle-big_heart-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_big_heart_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Coração Geométrico (Big Heart)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Design moderno de coração lapidado em cera de soja com perfume romântico.",
            description: "Vela escultural de coração com desenho geométrico lapidado, fundida com essência romântica de frutas vermelhas. Perfeita para presentear quem mais ama.",
            aromaProfile: "Romântico, Frutas Vermelhas, Amor"
        },
        es: {
            name: "Vela Corazón Geométrico",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Diseño moderno de corazón facetado en cera de soja con fragancia romántica.",
            description: "Vela de corazón escultórica con diseño geométrico facetado, fundida con aroma romántico de frutos rojos. Perfecta para regalar a quien más amas.",
            aromaProfile: "Romántico, Frutos Rojos, Amor"
        },
        en: {
            name: "Geometric Big Heart Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Modern faceted heart design in soy wax with a romantic scent.",
            description: "Sculptural heart candle with a faceted geometric design, infused with a romantic red berries essence. Perfect for gifting to your loved ones.",
            aromaProfile: "Romantic, Red Berries, Love"
        },
        fr: {
            name: "Bougie Cœur Géométrique",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Design moderne de cœur facetté en cire de soja avec parfum romantique.",
            description: "Bougie cœur sculpturale au design géométrique facetté, infusée d'une essence romantique de fruits rouges. Idéale à offrir à ceux que vous aimez.",
            aromaProfile: "Romantique, Fruits Rouges, Amour"
        }
    },
    {
        id: "candle-conjunto_budas-1",
        category: "vela",
        price: 19.90,
        image: "assets/candle_conjunto_budas_1.jpeg",
        qty: 1,
        pt: {
            name: "Conjunto Três Budas da Paz",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Trio de pequenos budas representativos em cera com essência de sândalo.",
            description: "Três velas esculpidas em formato de budas da paz (não fale, não ouça, não veja o mal) com fragrância relaxante de sândalo, trazendo harmonia e paz ao lar.",
            aromaProfile: "Sândalo, Relaxamento, Meditação"
        },
        es: {
            name: "Conjunto de Velas Budas de la Paz",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Trío de pequeños budas representativos en cera con aroma a sándalo.",
            description: "Tres velas escultóricas con forma de budas de la paz (no hables, no oigas, no veas el mal) con aroma relajante a sándalo, aportando armonía y paz al hogar.",
            aromaProfile: "Sándalo, Relajación, Meditación"
        },
        en: {
            name: "Peace Buddhas Candle Set",
            categoryLabel: "Scented Candle",
            aromaBrief: "Trio of small representative buddhas in soy wax with sandalwood scent.",
            description: "Three candles sculpted in the shape of peace buddhas (speak no evil, hear no evil, see no evil) with a relaxing sandalwood fragrance, bringing harmony and peace home.",
            aromaProfile: "Sandalwood, Relaxation, Meditation"
        },
        fr: {
            name: "Coffret Bougies Bouddhas de la Paix",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Trio de petits bouddhas représentatifs en cire au parfum de santal.",
            description: "Trois bougies sculptées en forme de bouddhas de la paix (ne rien dire, ne rien entendre, ne rien voir de mal) au parfum relaxant de bois de santal, apportant harmonie et paix à la maison.",
            aromaProfile: "Bois de Santal, Relaxation, Méditation"
        }
    },
    {
        id: "candle-coracoes-1",
        category: "vela",
        price: 7.90,
        image: "assets/candle_coracoes_1.jpeg",
        qty: 1,
        pt: {
            name: "Mini Velas Corações de Amor",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Pack de mini corações decorativos para momentos românticos e especiais.",
            description: "Conjunto de pequenas velas em formato de coração ideais para jantares românticos, decoração de mesas ou lembranças de casamento personalizadas. Aroma suave de baunilha.",
            aromaProfile: "Baunilha Doce, Jasmim, Romântico"
        },
        es: {
            name: "Mini Velas Corazones de Amor",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Pack de mini corazones decorativos para momentos románticos y especiales.",
            description: "Conjunto de pequeñas velas con forma de corazón ideales para cenas románticas, decoración de mesas o detalles de boda personalizados. Aroma suave a vainilla.",
            aromaProfile: "Vainilla Dulce, Jazmín, Romántico"
        },
        en: {
            name: "Mini Love Hearts Candle Set",
            categoryLabel: "Scented Candle",
            aromaBrief: "Pack of mini decorative hearts for romantic and special moments.",
            description: "Set of small heart-shaped candles ideal for romantic dinners, table decorations, or personalized wedding favors. Sweet vanilla scent.",
            aromaProfile: "Sweet Vanilla, Jasmine, Romantic"
        },
        fr: {
            name: "Mini Bougies Cœurs d'Amour",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Lot de mini cœurs décoratifs pour moments romantiques et spéciaux.",
            description: "Ensemble de petites bougies en forme de cœur idéales pour les dîners romantiques, la décoration de table ou les cadeaux de mariage personnalisés. Parfum doux de vanille.",
            aromaProfile: "Vanille Douce, Jasmin, Romantique"
        }
    },
    {
        id: "candle-flora-1",
        category: "vela",
        price: 10.90,
        image: "assets/candle_flora_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Escultural Flora Clássica",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Flor clássica em relevo geométrico de cera de soja e flor de laranjeira.",
            description: "Esfera de flores em relevo geométrico, uma peça escultural linda e aromática que traz o frescor cítrico da flor de laranjeira para o seu ambiente.",
            aromaProfile: "Flor de Laranjeira, Cítrico, Fresco"
        },
        es: {
            name: "Vela Escultural Flora Clásica",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Flor clásica en relieve geométrico de cera de soja y flor de azahar.",
            description: "Esfera de flores en relieve geométrico, una hermosa pieza escultórica y aromática que aporta el frescor cítrico del azahar a tu hogar.",
            aromaProfile: "Flor de Azahar, Cítrico, Fresco"
        },
        en: {
            name: "Classic Flora Sculptural Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Classic flower in geometric relief with orange blossom scent.",
            description: "Flower sphere in geometric relief, a beautiful and aromatic sculptural piece that brings the citrus freshness of orange blossom to your space.",
            aromaProfile: "Orange Blossom, Citrus, Fresh"
        },
        fr: {
            name: "Bougie Sculpturale Flora Classique",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Fleur classique en relief géométrique et fleur d'oranger.",
            description: "Sphère florale en relief géométrique, une superbe pièce sculpturale et aromatique qui apporte la fraîcheur hespéridée de la fleur d'oranger dans votre intérieur.",
            aromaProfile: "Fleur d'Oranger, Agrume, Frais"
        }
    },
    {
        id: "candle-flora-2",
        category: "vela",
        price: 10.90,
        image: "assets/candle_flora_2.jpeg",
        qty: 1,
        pt: {
            name: "Vela Escultural Flora Esférica",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Esfera de peónias esculpidas com fragrância primaveril de jasmim.",
            description: "Vela esférica de flores de cera vegetal com fragrância primaveril suave e relaxante, decorada com peónias em relevo de alta fidelidade.",
            aromaProfile: "Jasmim, Lírio, Primavera"
        },
        es: {
            name: "Vela Escultural Flora Esférica",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Esfera de peonías esculpidas con fragancia primaveral de jazmín.",
            description: "Vela esférica de flores de cera vegetal con fragancia primaveral suave y relajante, decorada con peonías en relieve de alta definición.",
            aromaProfile: "Jazmín, Lirio, Primavera"
        },
        en: {
            name: "Spherical Flora Sculptural Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Spherical peony flowers with spring jasmine fragrance.",
            description: "Vegetable wax spherical candle decorated with high-fidelity embossed peonies, featuring a soft and relaxing spring jasmine fragrance.",
            aromaProfile: "Jasmine, Lily, Springtime"
        },
        fr: {
            name: "Bougie Sculpturale Flora Sphérique",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Sphère de pivoines sculptées au parfum printanier de jasmin.",
            description: "Bougie sphérique florale en cire végétale au parfum printanier doux et relaxant, ornée de pivoines en relief haute définition.",
            aromaProfile: "Jasmin, Lys, Printemps"
        }
    },
    {
        id: "candle-flora-3",
        category: "vela",
        price: 11.90,
        image: "assets/candle_flora_3.jpeg",
        qty: 1,
        pt: {
            name: "Vela Escultural Flora Colunar",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Coluna de flores esculpida à mão com aroma envolvente de lavanda.",
            description: "Coluna de rosas entrelaçadas esculpida à mão em cera vegetal, perfeita como centro de mesa para jantares ou decoração clássica com aroma calmante de lavanda.",
            aromaProfile: "Lavanda, Herbal, Relaxante"
        },
        es: {
            name: "Vela Escultural Flora Columnar",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Columna de flores esculpida a mano con aroma envolvente a lavanda.",
            description: "Columna de rosas entrelazadas esculpida a mano en cera vegetal, perfecta como centro de mesa para cenas o decoración clásica con aroma calmante de lavanda.",
            aromaProfile: "Lavanda, Herbal, Relajante"
        },
        en: {
            name: "Columnar Flora Sculptural Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Hand-sculpted flower column with wrapping lavender scent.",
            description: "Column of intertwined roses hand-sculpted in vegetable wax, perfect as a table centerpiece for dinners or classic decor with a soothing lavender scent.",
            aromaProfile: "Lavender, Herbal, Relaxing"
        },
        fr: {
            name: "Bougie Sculpturale Flora Colonne",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Colonne de fleurs sculptée à la main au parfum enveloppant de lavande.",
            description: "Colonne de roses entrelacées sculptée à la main en cire végétale, parfaite comme centre de table pour les dîners ou décor classique au parfum apaisant de lavande.",
            aromaProfile: "Lavande, Herbal, Relaxant"
        }
    },
    {
        id: "candle-flowers-1",
        category: "vela",
        price: 14.90,
        image: "assets/candle_flowers_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Aromática Garden (Flores Secas)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Copo decorado com flores botânicas desidratadas e aroma campestre fresco.",
            description: "Vela aromática em copo de vidro decorada no topo com flores e ervas silvestres desidratadas. Exala uma fragrância fresca e herbal que lembra um jardim inglês.",
            aromaProfile: "Flores Silvestres, Alecrim, Fresco"
        },
        es: {
            name: "Vela Aromática Garden (Flores Secas)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Copa decorada con flores botánicas deshidratadas y aroma campestre fresco.",
            description: "Vela aromática en copa de vidrio decorada en la parte superior con flores y hierbas silvestres deshidratadas. Exhala una fragancia fresca y herbal que recuerda a un jardín inglés.",
            aromaProfile: "Flores Silvestres, Romero, Fresco"
        },
        en: {
            name: "Garden Scented Candle (Dried Flowers)",
            categoryLabel: "Scented Candle",
            aromaBrief: "Glass jar decorated with dried botanical flowers and fresh country scent.",
            description: "Aromatic glass jar candle decorated on top with dried wild flowers and herbs. It exudes a fresh and herbal fragrance reminding of an English garden.",
            aromaProfile: "Wild Flowers, Rosemary, Fresh"
        },
        fr: {
            name: "Bougie Parfumée Garden (Fleurs Séchées)",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot en verre décoré de fleurs séchées et parfum de campagne.",
            description: "Bougie parfumée en pot de verre décorée sur le dessus de fleurs sauvages et d'herbes séchées. Elle exhale une fragrance fraîche et herbacée rappelant un jardin anglais.",
            aromaProfile: "Fleurs Sauvages, Romarin, Frais"
        }
    },
    {
        id: "candle-luna-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_luna_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Escultura Luna (Meia-Lua)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Silhueta mística de lua crescente em cera de soja com aroma sedutor.",
            description: "Vela esculpida representando a lua com feições clássicas e calmas. Perfeita para noites de tranquilidade, leitura e meditação.",
            aromaProfile: "Almíscar, Baunilha, Místico"
        },
        es: {
            name: "Vela Escultura Luna (Media Luna)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Silueta mística de luna creciente en cera de soja con aroma seductor.",
            description: "Vela escultórica que representa la luna con rasgos clásicos y calmados. Perfecta para noches de tranquilidad, lectura y meditación.",
            aromaProfile: "Almizcle, Vainilla, Místico"
        },
        en: {
            name: "Luna Moon Sculptural Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Mystical crescent moon silhouette in soy wax with a seductive scent.",
            description: "Sculpted candle representing the moon with classic, calm features. Perfect for nights of tranquility, reading, and meditation.",
            aromaProfile: "Musk, Vanilla, Mystical"
        },
        fr: {
            name: "Bougie Sculpturale Luna (Demi-Lune)",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Silhouette mystique de croissant de lune au parfum séduisant.",
            description: "Bougie sculptée représentant la lune aux traits classiques et calmes. Parfaite pour les nuits de tranquillité, de lecture et de méditation.",
            aromaProfile: "Musc, Vanille, Mystique"
        }
    },
    {
        id: "candle-margarida-1",
        category: "vela",
        price: 8.90,
        image: "assets/candle_margarida_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flor Margarida Delicada",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela em formato de margarida com pétalas detalhadas e mel de camomila.",
            description: "Flor de margarida moldada à mão em cera de soja natural. Perfumada com notas doces de mel de flores e camomila, traz aconchego e calma.",
            aromaProfile: "Margarida, Camomila, Mel de Flores"
        },
        es: {
            name: "Vela Flor Margarita Delicada",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela con forma de margarita con pétalos detallados y miel de manzanilla.",
            description: "Flor de margarita moldeada a mano en cera de soja natural. Perfumada con notas dulces de miel de flores y manzanilla, aporta calidez y calma.",
            aromaProfile: "Margarita, Manzanilla, Miel de Flores"
        },
        en: {
            name: "Delicate Daisy Flower Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Daisy-shaped candle with detailed petals and chamomile honey scent.",
            description: "Hand-molded daisy flower made of natural soy wax. Scented with sweet notes of flower honey and chamomile, bringing warmth and calm.",
            aromaProfile: "Daisy, Chamomile, Flower Honey"
        },
        fr: {
            name: "Bougie Fleur de Marguerite Délicate",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie en forme de marguerite aux pétales détaillés et miel de camomille.",
            description: "Fleur de marguerite moulée à la main en cire de soja naturelle. Parfumée de notes douces de miel de fleurs et de camomille, elle apporte réconfort et calme.",
            aromaProfile: "Marguerite, Camomille, Miel de Fleurs"
        }
    },
    {
        id: "candle-mira-1",
        category: "vela",
        price: 13.90,
        image: "assets/candle_mira_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Busto Escultural Mira",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Busto escultural clássico com essência limpa e suave de talco.",
            description: "Vela escultural de busto clássico em cera de soja premium, aroma limpo a flores de algodão e talco que evoca limpeza e serenidade no lar.",
            aromaProfile: "Suave, Talco, Algodão, Limpo"
        },
        es: {
            name: "Vela Busto Escultural Mira",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Busto escultural clásico con esencia limpia y suave a talco.",
            description: "Vela escultórica de busto clásico de cera de soja premium, aroma limpio a flores de algodón y talco que evoca limpieza y serenidad en el hogar.",
            aromaProfile: "Suave, Talco, Algodón, Limpio"
        },
        en: {
            name: "Mira Sculptural Bust Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Classic sculptural bust with a clean, soft talc scent.",
            description: "Sculptural candle of a classic bust in premium soy wax, featuring a clean cotton and talc scent that evokes cleanliness and serenity at home.",
            aromaProfile: "Soft, Talcum, Cotton, Clean"
        },
        fr: {
            name: "Bougie Buste Sculptural Mira",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Buste sculptural classique à l'essence propre et douce de talc.",
            description: "Bougie sculptée en buste classique en cire de soja haut de gamme, au parfum propre de fleurs de coton et de talc qui évoque la propreté et la sérénité dans la maison.",
            aromaProfile: "Doux, Talc, Coton, Propre"
        }
    },
    {
        id: "candle-olho_grego-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_olho_grego_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Olho Grego Protetor",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela inspirada no olho grego contra más energias com aroma de sal marinho.",
            description: "Vela decorativa inspirada no tradicional amuleto do olho grego, perfumada com essência fresca de sal marinho e sálvia. Um amuleto para purificar o seu espaço.",
            aromaProfile: "Sal Marinho, Sálvia, Proteção, Purificador"
        },
        es: {
            name: "Vela Ojo Turco Protector",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela inspirada en el ojo turco contra malas energías con aroma a sal marina.",
            description: "Vela decorativa inspirada en el tradicional amuleto del ojo turco, perfumada con esencia fresca de sal marina y salvia. Un amuleto para purificar tu espacio.",
            aromaProfile: "Sal Marina, Salvia, Protección, Purificador"
        },
        en: {
            name: "Greek Evil Eye Protective Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Greek evil eye inspired candle against negative energies with sea salt scent.",
            description: "Decorative candle inspired by the traditional Greek evil eye amulet, scented with a fresh sea salt and sage fragrance. An amulet to purify your space.",
            aromaProfile: "Sea Salt, Sage, Protection, Purifier"
        },
        fr: {
            name: "Bougie Œil Grec Protecteur",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie inspirée de l'œil grec contre les mauvaises énergies au parfum de sel marin.",
            description: "Bougie décorative inspirée de la traditionnelle amulette de l'œil grec, parfumée d'une essence fraîche de sel marin et de sauge. Une amulette pour purifier votre espace.",
            aromaProfile: "Sel Marin, Sauge, Protection, Purificateur"
        }
    },
    {
        id: "candle-peonia-1",
        category: "vela",
        price: 9.90,
        image: "assets/candle_peonia_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flor Peónia Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Pétalas de peónia em relevo com aroma floral romântico de rosas.",
            description: "Vela em formato de peónia aberta com pétalas realistas esculpidas. Traz elegância, charme e frescor floral luxuoso a qualquer divisão da casa.",
            aromaProfile: "Peónia, Rosas, Romântico, Luxuoso"
        },
        es: {
            name: "Vela Flor Peonía Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Pétalos de peonía en relieve con aroma floral romántico de rosas.",
            description: "Vela con forma de peonía abierta con pétalos realistas esculpidos. Aporta elegancia, encanto y frescor floral lujoso a cualquier estancia del hogar.",
            aromaProfile: "Peonía, Rosas, Romántico, Lujoso"
        },
        en: {
            name: "Premium Peony Flower Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Peony petals in relief with a romantic floral rose scent.",
            description: "Open peony flower shaped candle with realistic sculpted petals. It brings elegance, charm, and a luxurious floral freshness to any room.",
            aromaProfile: "Peony, Roses, Romantic, Luxurious"
        },
        fr: {
            name: "Bougie Fleur de Pivoine Premium",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pétales de pivoine en relief au parfum floral romantique de roses.",
            description: "Bougie en forme de pivoine ouverte aux pétales réalistes sculptés. Elle apporte de l'élégance, du charme et une fraîcheur florale luxueuse à n'importe quelle pièce.",
            aromaProfile: "Pivoine, Roses, Romantique, Luxueux"
        }
    },
    {
        id: "candle-rosa_bella-1",
        category: "vela",
        price: 10.90,
        image: "assets/candle_rosa_bella_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flor Rosa Bella",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Rosa em botão esculpida à mão com perfume de rosas vermelhas e jasmim.",
            description: "Vela esculpida à mão simulando o desabrochar de uma rosa vermelha com notas intensas e sofisticadas de rosas vermelhas e um toque de jasmim.",
            aromaProfile: "Rosa Vermelha, Jasmim, Intenso"
        },
        es: {
            name: "Vela Flor Rosa Bella",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Rosa en botón esculpida a mano con aroma de rosas rojas y jazmín.",
            description: "Vela esculpida a mano simulando el florecer de una rosa roja con notas intensas y sofisticadas de rosas rojas y un toque de jazmín.",
            aromaProfile: "Rosa Roja, Jazmín, Intenso"
        },
        en: {
            name: "Rosa Bella Flower Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Hand-sculpted rose bud with red roses and jasmine scent.",
            description: "Hand-sculpted candle simulating the blooming of a red rose, featuring intense and sophisticated notes of red roses with a touch of jasmine.",
            aromaProfile: "Red Rose, Jasmine, Intense"
        },
        fr: {
            name: "Bougie Fleur Rose Bella",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bouton de rose sculpté à la main au parfum de roses rouges et jasmin.",
            description: "Bougie sculptée à la main simulant l'éclosion d'une rose rouge avec des notes intenses et sophistiquées de roses rouges et une touche de jasmin.",
            aromaProfile: "Rose Rouge, Jasmin, Intense"
        }
    },
    {
        id: "candle-rose-1",
        category: "vela",
        price: 9.90,
        image: "assets/candle_rose_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flor de Rosa Clássica",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Silhueta clássica de rosa com aroma fresco de jardim na primavera.",
            description: "Uma rosa clássica esculpida com perfume fresco e suave de pétalas de rosas, perfeita para relaxamento e decorações românticas.",
            aromaProfile: "Floral, Jardim de Rosas, Suave"
        },
        es: {
            name: "Vela Flor de Rosa Clásica",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Silueta clásica de rosa con aroma fresco de jardín en primavera.",
            description: "Una rosa clásica esculpida con perfume fresco y suave de pétalos de rosas, perfecta para relajación y decoraciones románticas.",
            aromaProfile: "Floral, Jardín de Rosas, Suave"
        },
        en: {
            name: "Classic Rose Flower Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Classic rose silhouette with a fresh spring garden scent.",
            description: "A classic sculpted rose with a fresh and soft scent of rose petals, perfect for relaxation and romantic decorations.",
            aromaProfile: "Floral, Rose Garden, Soft"
        },
        fr: {
            name: "Bougie Rose Classique",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Silhouette de rose classique au parfum frais de jardin au printemps.",
            description: "Une rose classique sculptée au parfum frais et doux de pétales de roses, idéale pour la relaxation et les décorations romantiques.",
            aromaProfile: "Floral, Jardin de Roses, Doux"
        }
    },
    {
        id: "candle-shinny_light-1",
        category: "vela",
        price: 11.90,
        image: "assets/candle_shinny_light_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Estrela de Luz (Shinny Light)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela geométrica facetada com fragrância refrescante cítrica de hortelã.",
            description: "Vela em formato geométrico facetado de estrela ou gema que reflete a luz de forma linda e preenche a divisão com notas frescas de limão e hortelã.",
            aromaProfile: "Limão, Hortelã, Cítrico Fresco"
        },
        es: {
            name: "Vela Estrella de Luz",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela geométrica facetada con fragancia refrescante cítrica de menta.",
            description: "Vela con formato geométrico facetado de estrella o gema que refleja la luz de forma hermosa y llena la estancia con notas frescas de limón y menta.",
            aromaProfile: "Limón, Menta, Cítrico Fresco"
        },
        en: {
            name: "Shinny Light Star Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Geometric faceted star candle with a refreshing citrus mint scent.",
            description: "Geometric faceted star or gem-shaped candle that beautifully reflects light and fills the room with fresh notes of lemon and mint.",
            aromaProfile: "Lemon, Mint, Fresh Citrus"
        },
        fr: {
            name: "Bougie Étoile de Lumière",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie géométrique facettée au parfum rafraîchissant d'agrume et menthe.",
            description: "Bougie au format géométrique facetté d'étoile ou de gemme qui reflète joliment la lumière et emplit la pièce de notes fraîches de citron et de menthe.",
            aromaProfile: "Citron, Menthe, Agrume Frais"
        }
    },
    {
        id: "candle-vela_en_vaso-1",
        category: "vela",
        price: 13.90,
        image: "assets/candle_vela_en_vaso_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Lavanda & Flores",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso decorado com flores secas de lavanda e fragrância calmante.",
            description: "Vela aromática em vaso de vidro decorada no topo com flores de lavanda e fragrância calmante, ideal para rituais de sono ou banho.",
            aromaProfile: "Lavanda, Calmante, Floral"
        },
        es: {
            name: "Vela en Vaso Lavanda & Flores",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso decorado con flores secas de lavanda y fragancia calmante.",
            description: "Vela aromática en vaso de vidrio decorada en la parte superior con flores de lavanda y fragancia calmante, ideal para rituales de sueño o baño.",
            aromaProfile: "Lavanda, Calmante, Floral"
        },
        en: {
            name: "Lavender & Flowers Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Jar candle decorated with dried lavender flowers and soothing scent.",
            description: "Aromatic glass jar candle decorated on top with dried lavender flowers and a soothing fragrance, ideal for sleep or bath rituals.",
            aromaProfile: "Lavender, Soothing, Floral"
        },
        fr: {
            name: "Bougie en Pot Lavande & Fleurs",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot décoré de fleurs de lavande séchées et parfum apaisant.",
            description: "Bougie parfumée en pot de verre décorée sur le dessus de fleurs de lavande et parfum apaisant, idéale pour les rituels de sommeil ou de bain.",
            aromaProfile: "Lavande, Apaisant, Floral"
        }
    },
    {
        id: "candle-vela_en_vaso-2",
        category: "vela",
        price: 13.90,
        image: "assets/candle_vela_en_vaso_2.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Laranja & Alecrim",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso decorado com laranja desidratada e fragrância cítrica e herbal.",
            description: "Vela aromática em vaso de vidro decorada com rodelas de laranja desidratada e sementes de alecrim. Traz foco e alegria para o seu dia a dia.",
            aromaProfile: "Cítrico, Alecrim, Quente"
        },
        es: {
            name: "Vela en Vaso Naranja & Romero",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso decorado con naranja deshidratada y fragancia cítrica y herbal.",
            description: "Vela aromática en vaso de vidrio decorada con rodajas de naranja deshidratada y semillas de romero. Aporta concentración y alegría a tu día a día.",
            aromaProfile: "Cítrico, Romero, Cálido"
        },
        en: {
            name: "Orange & Rosemary Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Jar candle decorated with dehydrated orange and a citrus herbal scent.",
            description: "Aromatic glass jar candle decorated with dehydrated orange slices and rosemary seeds. Brings focus and joy to your daily life.",
            aromaProfile: "Citrus, Rosemary, Warm"
        },
        fr: {
            name: "Bougie en Pot Orange & Romarin",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot décoré d'orange déshydratée et parfum d'agrume et romarin.",
            description: "Bougie parfumée en pot de verre décorée de tranches d'orange déshydratée et de graines de romarin. Apporte concentration et joie dans votre quotidien.",
            aromaProfile: "Agrume, Romarin, Chaud"
        }
    },
    {
        id: "candle-vela_en_vaso-3",
        category: "vela",
        price: 13.90,
        image: "assets/candle_vela_en_vaso_3.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Âmbar Tradicional",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Pote de vidro âmbar clássico com pavio de madeira e aroma aveludado de baunilha.",
            description: "Vela clássica em pote de vidro âmbar com pavio de madeira que estala levemente ao queimar como uma lareira. Aroma aveludado e acolhedor de baunilha e coco.",
            aromaProfile: "Baunilha, Coco, Amadeirado"
        },
        es: {
            name: "Vela en Vaso Ámbar Tradicional",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Tarro de vidrio ámbar clásico con mecha de madera y aroma aterciopelado a vainilla.",
            description: "Vela clásica en tarro de vidrio ámbar con mecha de madera que cruje suavemente al quemarse como una chimenea. Aroma aterciopelado y acogedor a vainilla y coco.",
            aromaProfile: "Vainilla, Coco, Amaderado"
        },
        en: {
            name: "Traditional Amber Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Classic amber glass jar with wood wick and velvet vanilla scent.",
            description: "Classic candle in an amber glass jar featuring a wooden wick that crackles softly like a fireplace. Cozy and velvety scent of vanilla and coconut.",
            aromaProfile: "Vanilla, Coconut, Woody"
        },
        fr: {
            name: "Bougie en Pot Ambre Traditionnel",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot en verre ambré classique avec mèche en bois et parfum velouté de vanille.",
            description: "Bougie classique en pot de verre ambré avec une mèche en bois qui crépite doucement au brûlage. Parfum velouté et réconfortant de vanille et de noix de coco.",
            aromaProfile: "Vanille, Noix de Coco, Boisé"
        }
    },
    {
        id: "candle-vela_en_vaso-4",
        category: "vela",
        price: 13.90,
        image: "assets/candle_vela_en_vaso_4.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Aromática Canela",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso decorado com especiarias e fragrância exótica e reconfortante.",
            description: "Vela aromática em vaso de vidro com paus de canela e cravinho desidratados. Exala uma fragrância de especiarias quentes que aquece e conforta o lar.",
            aromaProfile: "Canela, Cravinho, Aconchegante"
        },
        es: {
            name: "Vela en Vaso Aromática Canela",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso decorado con especias y fragancia exótica y reconfortante.",
            description: "Vela aromática en vaso de vidrio con ramas de canela y clavo deshidratados. Exhala una fragancia de especias cálidas que calienta y reconforta el hogar.",
            aromaProfile: "Canela, Clavo, Acogedor"
        },
        en: {
            name: "Cinnamon Spiced Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Jar candle decorated with spices and an exotic comforting scent.",
            description: "Aromatic glass jar candle with dried cinnamon sticks and cloves. It exudes a warm spiced fragrance that heats and comforts the home.",
            aromaProfile: "Cinnamon, Clove, Cozy"
        },
        fr: {
            name: "Bougie en Pot Cannelle Épicée",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot décoré d'épices au parfum exotique et réconfortant.",
            description: "Bougie parfumée en pot de verre garnie de bâtons de cannelle et de clous de girofle déshydratés. Elle exhale une fragrance d'épices chaudes qui réchauffe et réconforte la maison.",
            aromaProfile: "Cannelle, Girofle, Chaleureux"
        }
    },
    {
        id: "candle-vela_en_vaso-5",
        category: "vela",
        price: 13.90,
        image: "assets/candle_vela_en_vaso_5.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Flor de Algodão",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso de vidro com aroma limpo e fresco de flores de algodão.",
            description: "Vela aromática em pote de vidro com aroma suave a roupa lavada e flores de algodão. Traz uma sensação inigualável de frescor e tranquilidade.",
            aromaProfile: "Algodão, Fresco, Limpo, Suave"
        },
        es: {
            name: "Vela en Vaso Flor de Algodón",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso de vidrio con aroma limpio y fresco a flores de algodón.",
            description: "Vela aromática en tarro de vidrio con aroma suave a ropa lavada y flores de algodón. Aporta una sensación inigualable de frescura y tranquilidad.",
            aromaProfile: "Algodón, Fresco, Limpio, Suave"
        },
        en: {
            name: "Cotton Flower Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Glass jar with a clean, fresh cotton flower scent.",
            description: "Aromatic glass jar candle with a soft scent of fresh laundry and cotton flowers. It brings an unmatched sense of freshness and peace.",
            aromaProfile: "Cotton, Fresh, Clean, Soft"
        },
        fr: {
            name: "Bougie en Pot Fleur de Coton",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot en verre au parfum propre et frais de fleurs de coton.",
            description: "Bougie parfumée en pot de verre au parfum doux de linge propre et de fleurs de coton. Elle apporte une sensation inégalée de fraîcheur et de sérénité.",
            aromaProfile: "Coton, Frais, Propre, Doux"
        }
    },
    {
        id: "candle-general-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_general_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Aromática Cera de Soja Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Copo de cera natural jateado com pavio de algodão e baunilha suave.",
            description: "Vela aromática clássica em copo de vidro jateado, com cera de soja 100% pura e fragrância acolhedora de baunilha doce que acalma e conforta o ambiente.",
            aromaProfile: "Baunilha Doce, Suave, Acolhedor"
        },
        es: {
            name: "Vela Aromática Cera de Soja Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso de cera natural esmerilado con mecha de algodón y vainilla suave.",
            description: "Vela aromática clásica en vaso de vidrio esmerilado, con cera de soja 100% pura y fragancia acogedora de vainilla dulce que calma y reconforta el hogar.",
            aromaProfile: "Vainilla Dulce, Suave, Acogedor"
        },
        en: {
            name: "Premium Soy Wax Scented Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Frosted glass jar with natural wax, cotton wick, and soft vanilla scent.",
            description: "Classic scented candle in a frosted glass jar, with 100% pure soy wax and a cozy sweet vanilla fragrance that calms and comforts the space.",
            aromaProfile: "Sweet Vanilla, Soft, Welcoming"
        },
        fr: {
            name: "Bougie Parfumée Cire de Soja Premium",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pot en verre dépoli avec cire naturelle, mèche en coton et vanille douce.",
            description: "Bougie parfumée classique en pot de verre dépoli, avec 100% de cire de soja pure et une fragrance accueillante de vanille douce qui apaise et réconforte la pièce.",
            aromaProfile: "Vanille Douce, Doux, Accueillant"
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

// Dynamically generate the 39 decorative pieces to keep codebase clean and modular
const DECORATIVE_NAMES = [
    { pt: "Bandeja Oval em Gesso", es: "Bandeja Ovalada de Yeso", en: "Oval Plaster Tray", fr: "Plateau Oval en Plâtre", basePrice: 8.90 },
    { pt: "Porta-Joias Concha do Mar", es: "Plato Joyero de Concha", en: "Seashell Jewelry Dish", fr: "Vide-poche Coquillage", basePrice: 6.90 },
    { pt: "Porta-Velas Canelado Premium", es: "Porta-velas Acanalado Premium", en: "Premium Ribbed Candle Holder", fr: "Porte-bougie Cannelé Premium", basePrice: 5.90 },
    { pt: "Saboneteira Ondas Minimalista", es: "Jabonera de Ondas Minimalista", en: "Waves Minimalist Soap Dish", fr: "Porte-savon Vagues Minimaliste", basePrice: 7.90 },
    { pt: "Prato de Joias Coração", es: "Plato de Joyas de Corazón", en: "Heart Jewelry Dish", fr: "Coupe à Bijoux Cœur", basePrice: 4.90 },
    { pt: "Bandeja Redonda Terrazzo", es: "Bandeja Redonda Terrazzo", en: "Round Terrazzo Tray", fr: "Plateau Rond Terrazzo", basePrice: 10.90 },
    { pt: "Suporte Decorativo Hexagonal", es: "Soporte Decorativo Hexagonal", en: "Hexagonal Decorative Stand", fr: "Support Décoratif Hexagonal", basePrice: 6.50 },
    { pt: "Vaso de Gesso com Flores Secas", es: "Florero de Yeso con Flores Secas", en: "Plaster Vase with Dried Flowers", fr: "Vase en Plâtre avec Fleurs Séchées", basePrice: 12.90 },
    { pt: "Saboneteira Terrazzo Oval", es: "Jabonera Terrazzo Ovalada", en: "Terrazzo Oval Soap Dish", fr: "Porte-savon Terrazzo Ovale", basePrice: 7.50 },
    { pt: "Bandeja de Perfumes Canelada", es: "Bandeja de Perfumes Acanalada", en: "Ribbed Perfume Tray", fr: "Plateau à Parfum Cannelé", basePrice: 14.90 }
];

for (let i = 1; i <= 39; i++) {
    const nameTemplate = DECORATIVE_NAMES[(i - 1) % DECORATIVE_NAMES.length];
    const priceVariation = ((i * 0.3) % 2.0) - 1.0; // Subtle price variation
    const finalPrice = Math.round((nameTemplate.basePrice + priceVariation) * 10) / 10;
    
    PRODUCTS.push({
        id: `decor-${i}`,
        category: "decorativa",
        price: finalPrice,
        image: `assets/decor_${i}.jpg`,
        qty: 1,
        pt: {
            name: `${nameTemplate.pt} #${i}`,
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Design minimalista e elegante em gesso ecológico com acabamento impermeabilizado.",
            description: "Uma peça decorativa exclusiva feita à mão em gesso ecológico premium, com acabamento impermeável acetinado. Perfeita para organizar joias, perfumes, sabonetes ou como base para as nossas velas aromáticas. Cada peça é única e moldada individualmente em Portugal.",
            aromaProfile: "Eco-friendly, Design Exclusivo, Pintura Manual"
        },
        es: {
            name: `${nameTemplate.es} #${i}`,
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Diseño minimalista y elegante en yeso ecológico con acabado impermeabilizado.",
            description: "Una pieza de yeso ecológica premium hecha a mano, con acabado impermeable satinado. Perfecta para organizar joyas, perfumes, jabones o como base para nuestras velas aromáticas. Cada pieza es única y moldeada individualmente en Portugal.",
            aromaProfile: "Eco-friendly, Diseño Exclusivo, Pintura Manual"
        },
        en: {
            name: `${nameTemplate.en} #${i}`,
            categoryLabel: "Decorative Piece",
            aromaBrief: "Minimalist and elegant design in eco-friendly plaster with waterproof finish.",
            description: "An exclusive handcrafted decorative piece made of premium eco-friendly plaster, with a satin waterproof finish. Perfect for organizing jewelry, perfumes, soaps or as a base for our scented candles. Each piece is unique and individually molded in Portugal.",
            aromaProfile: "Eco-friendly, Exclusive Design, Hand Painted"
        },
        fr: {
            name: `${nameTemplate.fr} #${i}`,
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Design minimaliste et élégant en plâtre écologique avec finition imperméable.",
            description: "Une pièce décorative exclusive fabriquée à la main en plâtre écologique de qualité supérieure, avec une finition imperméable satinée. Parfaite pour organiser bijoux, parfums, savons ou comme base pour nos bougies parfumées. Chaque pièce est unique et moulée individuellement au Portugal.",
            aromaProfile: "Éco-responsable, Design Exclusif, Peint à la Main"
        }
    });
}

const SOAP_GALLERY = [
    {
        id: "soap-aloe-vera",
        price: 5.90,
        image: "assets/soap_aloe_vera.jpeg",
        pt: {
            name: "Sabonete de Aloe Vera",
            desc: "Ajuda na hidratação da pele e rugas. Suaviza a pele.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, água, extrato de aloe vera e essência de aloe vera. Benefícios estéticos: Ajuda na hidratação da pele e rugas. Suaviza a pele. Espiritualmente: Simboliza proteção, esperança, longevidade e sorte.",
            aromaProfile: "Proteção, Esperança, Longevidade e Sorte"
        },
        es: {
            name: "Jabón de Aloe Vera",
            desc: "Ayuda a hidratar la piel y reducir arrugas. Suaviza la piel.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, agua, extracto de aloe vera y esencia de aloe vera. Beneficios estéticos: Ayuda a hidratar la piel y reducir arrugas. Suaviza la piel. Espiritualmente: Simboliza protección, esperanza, longevidad y suerte.",
            aromaProfile: "Protección, Esperanza, Longevidad y Suerte"
        },
        en: {
            name: "Aloe Vera Soap",
            desc: "Helps with skin hydration and wrinkles. Softens the skin.",
            longDesc: "Ingredients: 100% vegetable glycerin, water, aloe vera extract, and aloe vera fragrance. Aesthetic benefits: Helps with skin hydration and wrinkles. Softens the skin. Spiritually: Symbolizes protection, hope, longevity, and luck.",
            aromaProfile: "Protection, Hope, Longevity, and Luck"
        },
        fr: {
            name: "Savon à l'Aloe Vera",
            desc: "Aide à hydrater la peau et réduire les rides. Adoucit la peau.",
            longDesc: "Ingrédients: Glycérine 100% végétale, eau, extrait d'aloe vera et essence d'aloe vera. Bienfaits esthétiques: Aide à hydrater la peau et réduire les rides. Adoucit la peau. Spirituellement: Symbolise la protection, l'espoir, la longévité et la chance.",
            aromaProfile: "Protection, Espoir, Longévité et Chance"
        }
    },
    {
        id: "soap-amendoa-aveia",
        price: 6.50,
        image: "assets/soap_amendoa_aveia.jpeg",
        pt: {
            name: "Sabonete de Aveia & Amêndoa",
            desc: "Ideal para nutrir, proteger e rejuvenescer a pele.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, essência natural de aveia e mel, mel, amêndoa e flocos de aveia e óleo de amêndoas doces. Benefícios estéticos: A amêndoa e a aveia são ricos em propriedades estéticas complementares ideais para nutrir, proteger e rejuvenescer a pele. Enquanto o óleo de amêndoa atua na hidratação e luminosidade, a aveia foca na regeneração celular, firmeza e suavidade. Espiritualmente: Elas nutrem o corpo físico para promover a clareza mental, o equilíbrio emocional e a elevação da vibração energética.",
            aromaProfile: "Clareza Mental, Equilíbrio Emocional, Nutrição"
        },
        es: {
            name: "Jabón de Avena & Almendra",
            desc: "Ideal para nutrir, proteger y rejuvenecer la piel.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, esencia natural de avena y miel, miel, almendra, copos de avena y aceite de almendras dulces. Beneficios estéticos: La almendra y la avena son ricas en propiedades estéticas complementarias ideales para nutrir, proteger y rejuvenecer la piel. Mientras que el aceite de almendras actúa en la hidratación y luminosidad, la avena se enfoca en la regeneración celular, firmeza y suavidad. Espiritualmente: Nutren el cuerpo físico para promover la claridad mental, el equilibrio emocional y la elevación de la vibración energética.",
            aromaProfile: "Claridad Mental, Equilibrio Emocional, Nutrición"
        },
        en: {
            name: "Oatmeal & Almond Soap",
            desc: "Ideal for nourishing, protecting, and rejuvenating the skin.",
            longDesc: "Ingredients: 100% vegetable glycerin, natural oat and honey fragrance, honey, almond, oat flakes, and sweet almond oil. Aesthetic benefits: Almond and oatmeal are rich in complementary aesthetic properties ideal for nourishing, protecting, and rejuvenating the skin. While almond oil acts on hydration and glow, oatmeal focuses on cell regeneration, firmness, and softness. Spiritually: They nourish the physical body to promote mental clarity, emotional balance, and energy vibration elevation.",
            aromaProfile: "Mental Clarity, Emotional Balance, Nourishment"
        },
        fr: {
            name: "Savon Avoine & Amande",
            desc: "Idéal pour nourrir, protéger et rajeunir la peau.",
            longDesc: "Ingrédients: Glycérine 100% végétale, essence naturelle d'avoine et miel, miel, amande, flocons d'avoine et huile d'amande douce. Bienfaits esthétiques: L'amande et l'avoine sont riches en propriétés esthétiques complémentaires idéales pour nourrir, protéger et rajeunir la peau. Tandis que l'huile d'amande agit sur l'hydratation et l'éclat, l'avoine se concentre sur la régénération cellulaire, la fermeté et la douceur. Spirituellement: Ils nourrissent le corps physique pour favoriser la clarté mentale, l'équilibre émotionnel et l'élévation de la vibration énergétique.",
            aromaProfile: "Clarté Mentale, Équilibre Émotionnel, Nutrition"
        }
    },
    {
        id: "soap-anis-mel",
        price: 5.90,
        image: "assets/soap_anis_mel.jpeg",
        pt: {
            name: "Sabonete de Anis Estrelado & Mel",
            desc: "Estimula o colagénio, renovação celular e firmeza da pele.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, água, mel, anis estrelado e canela em pó, essência de mel e canela. Benefícios estéticos: Estimula a produção de colágeno, renovação celular, ajuda a deixar a pele mais firme. Ajuda na acne, dermatite e eczemas. Hidrata profundamente, combate a acne, previne o envelhecimento precoce e promove a cicatrização de pequenas irritações na pele. Espiritualmente: O Anis ajuda na abertura da mediunidade. O mel ajuda na harmonia e a atração de energias positivas.",
            aromaProfile: "Abertura, Harmonia, Energias Positivas"
        },
        es: {
            name: "Jabón de Anís Estrellado & Miel",
            desc: "Estimula el colágeno, la renovación celular y la firmeza de la piel.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, agua, miel, anís estrellado y canela en polvo, esencia de miel y canela. Beneficios estéticos: Estimula la producción de colágeno, renovación celular, ayuda a dejar la piel más firme. Ayuda con el acné, la dermatitis y los eczemas. Hidrata profundamente, combate el acné, previene el envejecimiento prematuro y promueve la cicatrización de pequeñas irritaciones en la piel. Espiritualmente: El anís ayuda en la apertura de la mediumnidad. La miel ayuda a la armonía y la atracción de energías positivas.",
            aromaProfile: "Apertura, Armonía, Energías Positivas"
        },
        en: {
            name: "Star Anise & Honey Soap",
            desc: "Stimulates collagen, cell renewal, and skin firmness.",
            longDesc: "Ingredients: 100% vegetable glycerin, water, honey, star anise, cinnamon powder, and honey & cinnamon fragrance. Aesthetic benefits: Stimulates collagen production, cell renewal, and helps make the skin firmer. Helps with acne, dermatitis, and eczema. Deeply hydrates, fights acne, prevents premature aging, and promotes healing of minor skin irritations. Spiritually: Star anise helps open mediumship. Honey helps with harmony and attracting positive energies.",
            aromaProfile: "Opening, Harmony, Positive Energies"
        },
        fr: {
            name: "Savon Anis Étoilé & Miel",
            desc: "Stimule le collagène, le renouvellement cellulaire et la fermeté.",
            longDesc: "Ingrédients: Glycérine 100% végétale, eau, miel, anis étoilé, cannelle en poudre, essence de miel et cannelle. Bienfaits esthétiques: Stimule la production de collagène, le renouvellement cellulaire et aide à rendre la peau plus ferme. Aide contre l'acné, la dermatite et l'eczéma. Hydrate en profondeur, combat l'acné, prévient le vieillissement prématuré et favorise la guérison des petites irritations cutanées. Spirituellement: L'anis étoilé aide à l'ouverture de la médiumnité. Le miel favorise l'harmonie et l'attraction d'énergies positives.",
            aromaProfile: "Ouverture, Harmonie, Énergies Positives"
        }
    },
    {
        id: "soap-camomila",
        price: 5.50,
        image: "assets/soap_camomila.jpeg",
        pt: {
            name: "Sabonete de Camomila & Flor de Laranjeira",
            desc: "Acalma a pele irritada e ajuda na renovação cutânea.",
            longDesc: "Ingredientes: Água, glicerina 100% vegetal, camomila e essência 100% vegetal de camomila e flor de laranjeira. Benefícios estéticos: Acalma a pele irritada, ajuda em problemas de eczema ou acne. Renovação da pele. Espiritualmente: Ajuda a ficar mais tranquilo e equilibrado. Ajuda nas tomadas de decisões e a restaurar forças.",
            aromaProfile: "Tranquilidade, Equilíbrio, Restauração"
        },
        es: {
            name: "Jabón de Manzanilla & Azahar",
            desc: "Calma la piel irritada y ayuda a la renovación cutánea.",
            longDesc: "Ingredientes: Agua, glicerina 100% vegetal, manzanilla y esencia 100% vegetal de manzanilla y flor de azahar. Beneficios estéticos: Calma la piel irritada, ayuda en problemas de eczema o acné. Renovación de la piel. Espiritualmente: Ayuda a estar más tranquilo y equilibrado. Ayuda en la toma de decisiones y a restaurar fuerzas.",
            aromaProfile: "Tranquilidad, Equilibrio, Restauración"
        },
        en: {
            name: "Chamomile & Orange Blossom Soap",
            desc: "Soothes irritated skin and helps with skin renewal.",
            longDesc: "Ingredients: Water, 100% vegetable glycerin, chamomile, and 100% vegetable chamomile and orange blossom fragrance. Aesthetic benefits: Soothes irritated skin, helps with eczema or acne. Skin renewal. Spiritually: Helps to stay calm and balanced. Helps in decision-making and restoring strength.",
            aromaProfile: "Tranquility, Balance, Restoration"
        },
        fr: {
            name: "Savon Camomille & Fleur d'Oranger",
            desc: "Apaise la peau irritée et aide au renouvellement cutané.",
            longDesc: "Ingrédients: Eau, glycérine 100% végétale, camomille et essence 100% végétale de camomille et fleur d'oranger. Bienfaits esthétiques: Apaise la peau irritée, aide en cas d'eczéma ou d'acné. Renouvellement de la peau. Spirituellement: Aide à rester plus tranquille et équilibré. Aide à la prise de décision et à restaurer les forces.",
            aromaProfile: "Tranquillité, Équilibre, Restauration"
        }
    },
    {
        id: "soap-carvao",
        price: 6.90,
        image: "assets/soap_carvao.jpeg",
        pt: {
            name: "Sabonete de Carbão Ativo & Limão",
            desc: "Controla a oleosidade e limpa profundamente os poros.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, carvão ativo, água e sumo de limão. Benefícios estéticos: Controla a oleosidade da pele, limpeza dos poros, clareador de manchas. Espiritualmente: Ajuda a eliminar energias negativas.",
            aromaProfile: "Purificação, Limpeza, Proteção Energética"
        },
        es: {
            name: "Jabón de Carbón Activo & Limón",
            desc: "Controla la grasa y limpia profundamente los poros.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, carbón activo, agua y zumo de limón. Beneficios estéticos: Controla la grasa de la piel, limpieza de los poros, aclara manchas. Espiritualmente: Ayuda a eliminar energías negativas.",
            aromaProfile: "Purificación, Limpieza, Protección Energética"
        },
        en: {
            name: "Activated Charcoal & Lemon Soap",
            desc: "Controls oiliness and deeply cleanses the pores.",
            longDesc: "Ingredients: 100% vegetable glycerin, activated charcoal, water, and lemon juice. Aesthetic benefits: Controls skin oiliness, cleanses pores, and lightens dark spots. Spiritually: Helps eliminate negative energies.",
            aromaProfile: "Purification, Cleansing, Energy Protection"
        },
        fr: {
            name: "Savon au Charbon Actif & Citron",
            desc: "Contrôle l'excès de sébum et nettoie les pores en profondeur.",
            longDesc: "Ingrédients: Glycérine 100% végétale, charbon actif, eau et jus de citron. Bienfaits esthétiques: Contrôle l'excès de sébum de la peau, nettoie les pores, éclaircit les taches. Spirituellement: Aide à éliminer les énergies négatives.",
            aromaProfile: "Purification, Nettoyage, Protection Énergétique"
        }
    },
    {
        id: "soap-alecrim",
        price: 5.90,
        image: "assets/soap_alecrim.jpeg",
        pt: {
            name: "Sabonete de Alecrim",
            desc: "Ajuda na cicatrização e firmeza da pele.",
            longDesc: "Ingredientes: Alecrim, água, glicerina 100% vegetal e essência vegetal de alecrim. Benefícios estéticos: Ajuda na cicatrização. O alecrim ajuda no aumento do fluxo sanguíneo e produção de colagénio impedindo que a pele fique flácida. Espiritualmente: Proporciona motivação, confiança e mais energia.",
            aromaProfile: "Motivação, Confiança, Energia"
        },
        es: {
            name: "Jabón de Romero",
            desc: "Ayuda a la cicatrización y firmeza de la piel.",
            longDesc: "Ingredientes: Romero, agua, glicerina 100% vegetal y esencia vegetal de romero. Beneficios estéticos: Ayuda a la cicatrización. El romero ayuda a aumentar el flujo sanguíneo y la producción de colágeno, evitando la flacidez de la piel. Espiritualmente: Proporciona motivación, confianza y más energía.",
            aromaProfile: "Motivación, Confianza, Energía"
        },
        en: {
            name: "Rosemary Soap",
            desc: "Helps with healing and skin firmness.",
            longDesc: "Ingredients: Rosemary, water, 100% vegetable glycerin, and rosemary essential oil. Aesthetic benefits: Helps with healing. Rosemary helps increase blood flow and collagen production, preventing sagging skin. Spiritually: Provides motivation, confidence, and more energy.",
            aromaProfile: "Motivation, Confidence, Energy"
        },
        fr: {
            name: "Savon au Romarin",
            desc: "Aide à la cicatrisation et à la fermeté de la peau.",
            longDesc: "Ingrédients: Romarin, eau, glycérine 100% végétale et essence végétale de romarin. Bienfaits esthétiques: Aide à la cicatrisation. Le romarin aide à augmenter le flux sanguin et la production de collagène, empêchant le relâchement cutané. Spirituellement: Apporte de la motivation, de la confiance et plus d'énergie.",
            aromaProfile: "Motivation, Confiance, Énergie"
        }
    },
    {
        id: "soap-coco",
        price: 5.90,
        image: "assets/soap_coco.jpeg",
        pt: {
            name: "Sabonete de Coco & Óleo de Coco",
            desc: "Hidratante facial e corporal, ideal para aliviar queimaduras solares.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, água, coco ralado, óleo de coco e essência natural de coco. Benefícios estéticos: Hidratante facial e corporal. Limpa impurezas. Calmante e excelente para aliviar queimaduras provocadas pela exposição solar. Espiritualmente: O coco simboliza fertilidade e prosperidade.",
            aromaProfile: "Fertilidade, Prosperidade, Alívio"
        },
        es: {
            name: "Jabón de Coco & Aceite de Coco",
            desc: "Hidratante facial y corporal, ideal para aliviar quemaduras solares.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, agua, coco rallado, aceite de coco y esencia natural de coco. Beneficios estéticos: Hidratante facial y corporal. Limpia impurezas. Calmante y excelente para aliviar quemaduras provocadas por la exposición solar. Espiritualmente: El coco simboliza fertilidad y prosperidad.",
            aromaProfile: "Fertilidad, Prosperidad, Alivio"
        },
        en: {
            name: "Coconut & Coconut Oil Soap",
            desc: "Facial and body moisturizer, ideal for soothing sunburns.",
            longDesc: "Ingredients: 100% vegetable glycerin, water, grated coconut, coconut oil, and natural coconut fragrance. Aesthetic benefits: Facial and body moisturizer. Cleanses impurities. Soothing and excellent for relieving sunburns caused by sun exposure. Spiritually: Coconut symbolizes fertility and prosperity.",
            aromaProfile: "Fertility, Prosperity, Relief"
        },
        fr: {
            name: "Savon Noix de Coco & Huile de Coco",
            desc: "Hydratant visage et corps, idéal pour apaiser les coups de soleil.",
            longDesc: "Ingrédients: Glycérine 100% végétale, eau, noix de coco râpée, huile de coco et essence naturelle de noix de coco. Bienfaits esthétiques: Hydratant visage et corps. Nettoie les impuretés. Apaisant et excellent pour soulager les brûlures causées par l'exposition solaire. Spirituellement: La noix de coco symbolise la fertilité et la prospérité.",
            aromaProfile: "Fertilité, Prospérité, Soulagement"
        }
    },
    {
        id: "soap-jasmim",
        price: 6.50,
        image: "assets/soap_jasmim.jpeg",
        pt: {
            name: "Sabonete de Jasmim",
            desc: "Ajuda na produção de colagénio e reduz acne e rugas.",
            longDesc: "Ingredientes: Jasmim, água, glicerina 100% vegetal e essência natural de jasmim. Benefícios estéticos: Ajuda na produção de colagénio e elasticidade da pele. Reduz acne e rugas. Espiritualmente: O jasmim simboliza amor próprio, pureza, espiritualidade e beleza. Boas energias e conexão.",
            aromaProfile: "Amor Próprio, Pureza, Beleza"
        },
        es: {
            name: "Jabón de Jazmín",
            desc: "Ayuda a la producción de colágeno y reduce acné y arrugas.",
            longDesc: "Ingredientes: Jazmín, agua, glicerina 100% vegetal y esencia natural de jazmín. Beneficios estéticos: Ayuda a la producción de colágeno y elasticidad de la piel. Reduce el acné y las arrugas. Espiritualmente: El jazmín simboliza amor propio, pureza, espiritualidad y belleza. Buenas energías y conexión.",
            aromaProfile: "Amor Propio, Pureza, Belleza"
        },
        en: {
            name: "Jasmine Soap",
            desc: "Helps with collagen production and reduces acne and wrinkles.",
            longDesc: "Ingredients: Jasmine, water, 100% vegetable glycerin, and natural jasmine fragrance. Aesthetic benefits: Helps with collagen production and skin elasticity. Reduces acne and wrinkles. Spiritually: Jasmine symbolizes self-love, purity, spirituality, and beauty. Good energies and connection.",
            aromaProfile: "Self-Love, Purity, Beauty"
        },
        fr: {
            name: "Savon au Jasmin",
            desc: "Aide à la production de collagène et réduit l'acné et les rides.",
            longDesc: "Ingrédients: Jasmin, eau, glycérine 100% végétale et essence naturelle de jasmin. Bienfaits esthétiques: Aide à la production de collagène et à l'élasticité de la peau. Réduit l'acné et les rides. Spirituellement: Le jasmin symbolise l'amour-propre, la pureté, la spiritualité et la beauté. Bonnes énergies et connexion.",
            aromaProfile: "Amour-Propre, Pureté, Beauté"
        }
    },
    {
        id: "soap-lavanda",
        price: 5.90,
        image: "assets/soap_lavanda.jpeg",
        pt: {
            name: "Sabonete de Lavanda",
            desc: "Anti-inflamatório, reduz acne, rosácea e eczemas.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, água, essência natural e lavanda. Benefícios estéticos: Anti-inflamatório, reduz acne, rosácea e eczemas. Ajuda no tratamento de peles oleosas. Espiritualmente: Calmante, ajuda na ansiedade e stress. Ajuda a nos conectar com a nossa intuição e sabedoria.",
            aromaProfile: "Calmante, Intuição, Conexão"
        },
        es: {
            name: "Jabón de Lavanda",
            desc: "Antiinflamatorio, reduce acné, rosácea y eczemas.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, agua, esencia natural y lavanda. Beneficios estéticos: Antiinflamatorio, reduce el acné, la rosácea y los eczemas. Ayuda en el tratamiento de pieles grasas. Espiritualmente: Calmante, ayuda con la ansiedad y el estrés. Nos ayuda a conectar con nuestra intuición y sabiduría.",
            aromaProfile: "Calmante, Intuición, Conexión"
        },
        en: {
            name: "Lavender Soap",
            desc: "Anti-inflammatory, reduces acne, rosacea, and eczema.",
            longDesc: "Ingredients: 100% vegetable glycerin, water, natural fragrance, and lavender. Aesthetic benefits: Anti-inflammatory, reduces acne, rosacea, and eczema. Helps treat oily skin. Spiritually: Soothing, helps with anxiety and stress. Helps connect with our intuition and wisdom.",
            aromaProfile: "Calming, Intuition, Connection"
        },
        fr: {
            name: "Savon à la Lavande",
            desc: "Anti-inflammatoire, réduit l'acné, la rosacée et l'eczéma.",
            longDesc: "Ingrédients: Glycérine 100% végétale, eau, essence naturelle et lavande. Bienfaits esthétiques: Anti-inflammatoire, réduit l'acné, la rosacée et l'eczéma. Aide au traitement des peaux grasses. Spirituellement: Apaisant, aide en cas d'anxiété et de stress. Aide à nous connecter à notre intuition et à notre sagesse.",
            aromaProfile: "Apaisant, Intuition, Connexion"
        }
    },
    {
        id: "soap-maca-canela",
        price: 5.90,
        image: "assets/soap_maca_canela.jpeg",
        pt: {
            name: "Sabonete de Maçã & Canela",
            desc: "Renovação celular e suavização de rugas de expressão.",
            longDesc: "Ingredientes: Maçã, canela, água, glicerina 100% vegetal e óleo essencial de maçã e canela. Benefícios estéticos: Anti-inflamatório e ajuda na diminuição da acne. Suaviza rugas de expressão, renovação de células e ajuda na aparência cansada e sem brilho. Espiritualmente: Fertilidade, beleza, juventude, prosperidade, abundância de caminhos e abertura.",
            aromaProfile: "Abundância, Beleza, Prosperidade"
        },
        es: {
            name: "Jabón de Manzana & Canela",
            desc: "Renovación celular y suavizado de arrugas de expresión.",
            longDesc: "Ingredientes: Manzana, canela, agua, glicerina 100% vegetal y aceite esencial de manzana y canela. Beneficios estéticos: Antiinflamatorio y ayuda en la disminución del acné. Suaviza arrugas de expresión, renovación celular y ayuda con la apariencia cansada y sin brillo. Espiritualmente: Fertilidad, belleza, juventud, prosperidad, abundancia y apertura de caminos.",
            aromaProfile: "Abundancia, Belleza, Prosperidad"
        },
        en: {
            name: "Apple & Cinnamon Soap",
            desc: "Cell renewal and smoothing of expression lines.",
            longDesc: "Ingredients: Apple, cinnamon, water, 100% vegetable glycerin, and apple & cinnamon essential oil. Aesthetic benefits: Anti-inflammatory and helps reduce acne. Smooths expression wrinkles, promotes cell renewal, and helps with tired, dull skin. Spiritually: Fertility, beauty, youth, prosperity, abundance, and path opening.",
            aromaProfile: "Abundance, Beauty, Prosperity"
        },
        fr: {
            name: "Savon Pomme & Cannelle",
            desc: "Renouvellement cellulaire et lissage des rides d'expression.",
            longDesc: "Ingrédients: Pomme, cannelle, eau, glycérine 100% végétale et huile essentielle de pomme et cannelle. Bienfaits esthétiques: Anti-inflammatoire et aide à réduire l'acné. Lisse les rides d'expression, favorise le renouvellement cellulaire et aide à revitaliser les peaux ternes et fatiguées. Spirituellement: Fertilité, beauté, jeunesse, prospérité, abondance et ouverture de chemins.",
            aromaProfile: "Abondance, Beauté, Prospérité"
        }
    },
    {
        id: "soap-mel",
        price: 5.50,
        image: "assets/soap_mel.jpeg",
        pt: {
            name: "Sabonete de Mel",
            desc: "Ação hidratante, cicatrizante, anti-inflamatória e antioxidante.",
            longDesc: "Ingredientes: Água, glicerina 100% vegetal, mel e essência natural de mel. Benefícios estéticos: Hidratante e ação cicatrizante. Efeito anti-inflamatório e antioxidante. Espiritualmente: Prosperidade e cura. Conexão connosco mesmos.",
            aromaProfile: "Prosperidade, Cura, Conexão"
        },
        es: {
            name: "Jabón de Miel",
            desc: "Acción hidratante, cicatrizante, antiinflamatoria y antioxidante.",
            longDesc: "Ingredientes: Agua, glicerina 100% vegetal, miel y esencia natural de miel. Beneficios estéticos: Hidratante y acción cicatrizante. Efecto antiinflamatorio y antioxidante. Espiritualmente: Prosperidad y curación. Conexión con nosotros mismos.",
            aromaProfile: "Prosperidad, Curación, Conexión"
        },
        en: {
            name: "Honey Soap",
            desc: "Moisturizing, healing, anti-inflammatory, and antioxidant action.",
            longDesc: "Ingredients: Water, 100% vegetable glycerin, honey, and natural honey fragrance. Aesthetic benefits: Moisturizing and healing action. Anti-inflammatory and antioxidant effect. Spiritually: Prosperity and healing. Connection with ourselves.",
            aromaProfile: "Prosperity, Healing, Connection"
        },
        fr: {
            name: "Savon au Miel",
            desc: "Action hydratante, cicatrisante, anti-inflammatoire et antioxydante.",
            longDesc: "Ingrédients: Eau, glycérine 100% végétale, miel et essence naturelle de miel. Bienfaits esthétiques: Hydratant et cicatrisant. Effet anti-inflammatoire et antioxydant. Spirituellement: Prospérité et guérison. Connexion avec soi-même.",
            aromaProfile: "Prospérité, Guérison, Connexion"
        }
    },
    {
        id: "soap-rosa",
        price: 6.50,
        image: "assets/soap_rosa.jpeg",
        pt: {
            name: "Sabonete de Rosas",
            desc: "Equilibra o PH da pele e previne o envelhecimento.",
            longDesc: "Ingredientes: Água, glicerina 100% vegetal, essência aromática de rosas e pétalas de rosa. Benefícios estéticos: Equilibra o PH da pele, combate o acne, antissético e previne o envelhecimento. Espiritualmente: Capaz de trazer envolvimento espiritual, atração amorosa e calmante.",
            aromaProfile: "Atração, Calma, Envolvimento Espiritual"
        },
        es: {
            name: "Jabón de Rosas",
            desc: "Equilibra el PH de la piel y previene el envejecimiento.",
            longDesc: "Ingredientes: Agua, glicerina 100% vegetal, esencia aromática de rosas y pétalos de rosa. Beneficios estéticos: Equilibra el PH de la piel, combate el acné, antiséptico y previene el envejecimiento. Espiritualmente: Capaz de traer conexión espiritual, atracción amorosa y calma.",
            aromaProfile: "Atracción, Calma, Conexión Espiritual"
        },
        en: {
            name: "Rose Soap",
            desc: "Balances skin PH and prevents aging.",
            longDesc: "Ingredients: Water, 100% vegetable glycerin, aromatic rose fragrance, and rose petals. Aesthetic benefits: Balances skin PH, fights acne, antiseptic, and prevents aging. Spiritually: Capable of bringing spiritual connection, romantic attraction, and calming vibes.",
            aromaProfile: "Attraction, Calming, Spiritual Connection"
        },
        fr: {
            name: "Savon aux Roses",
            desc: "Équilibre le PH de la peau et prévient le vieillissement.",
            longDesc: "Ingrédients: Eau, glycérine 100% végétale, essence aromatique de roses et pétales de rose. Bienfaits esthétiques: Équilibre le PH de la peau, combat l'acné, antiseptique et prévient le vieillissement. Spirituellement: Capable d'apporter connexion spirituelle, attraction amoureuse et calme.",
            aromaProfile: "Attraction, Calme, Connexion Spirituelle"
        }
    },
    {
        id: "soap-sal-grosso-arruda",
        price: 6.50,
        image: "assets/soap_sal_grosso_arruda.jpeg",
        pt: {
            name: "Sabonete de Sal Grosso & Arruda",
            desc: "Efeito esfoliante, antibacteriano e purificação espiritual.",
            longDesc: "Ingredientes: Arruda, sal grosso, água, glicerina 100% vegetal e essência de arruda. Benefícios estéticos: Efeito esfoliante com propriedades antibacterianas. Combate a acne e elimina o excesso de oleosidade na pele. Espiritualmente: Elimina as más energias, invejas e mau olhado.",
            aromaProfile: "Purificação, Limpeza Energética, Proteção"
        },
        es: {
            name: "Jabón de Sal Gorda & Ruda",
            desc: "Efecto exfoliante, antibacteriano y purificación espiritual.",
            longDesc: "Ingredientes: Ruda, sal gorda, agua, glicerina 100% vegetal y esencia de ruda. Beneficios estéticos: Efecto exfoliante con propiedades antibacterianas. Combate el acné y elimina el exceso de grasa en la piel. Espiritualmente: Elimina las malas energías, envidias y mal de ojo.",
            aromaProfile: "Purificación, Limpieza Energética, Protección"
        },
        en: {
            name: "Coarse Salt & Rue Soap",
            desc: "Exfoliating effect, antibacterial, and spiritual purification.",
            longDesc: "Ingredients: Rue, coarse salt, water, 100% vegetable glycerin, and rue fragrance. Aesthetic benefits: Exfoliating effect with antibacterial properties. Fights acne and eliminates excess skin oiliness. Spiritually: Eliminates bad energies, envy, and the evil eye.",
            aromaProfile: "Purification, Energy Cleansing, Protection"
        },
        fr: {
            name: "Savon Gros Sel & Rue",
            desc: "Effet exfoliant, antibactérien et purification spirituelle.",
            longDesc: "Ingrédients: Rue, gros sel, eau, glycérine 100% végétale et essence de rue. Bienfaits esthétiques: Effet exfoliant aux propriétés antibactériennes. Combat l'acné et élimine l'excès de sébum de la peau. Spirituellement: Élimine les mauvaises énergies, la jalousie et le mauvais œil.",
            aromaProfile: "Purification, Nettoyage Énergétique, Protection"
        }
    }
];
/* ==========================================================================
   DYNAMIC PRODUCT ADDITIONS (Bouquets, Summer Collection, Souvenirs & Melts)
   ========================================================================== */
const BOUQUET_NAMES = [
    { pt: "Buquê de Sabonetes Florais Premium", es: "Ramo de Jabones Florales Premium", en: "Premium Floral Soap Bouquet", fr: "Bouquet de Savons Floraux Premium", basePrice: 24.90 },
    { pt: "Cesta de Sabonetes Rosas de Amor", es: "Cesta de Jabones Rosas de Amor", en: "Rose of Love Soap Basket", fr: "Panier de Savons Roses d'Amour", basePrice: 26.90 },
    { pt: "Arranjo Floral de Sabonete Rústico", es: "Arreglo Floral de Jabón Rústico", en: "Rustic Soap Floral Arrangement", fr: "Arrangement Floral de Savon Rustique", basePrice: 19.90 },
    { pt: "Buquê de Sabonetes Elegance", es: "Ramo de Jabones Elegance", en: "Elegance Soap Bouquet", fr: "Bouquet de Savons Élégance", basePrice: 22.90 },
    { pt: "Cesta de Sabonetes Lavanda Real", es: "Cesta de Jabones Lavanda Real", en: "Royal Lavender Soap Basket", fr: "Panier de Savons Lavande Royale", basePrice: 25.90 },
    { pt: "Arranjo de Sabonetes Silvestres", es: "Arreglo de Jabones Silvestres", en: "Wild Flower Soap Arrangement", fr: "Arrangement de Savons Sauvages", basePrice: 21.90 },
    { pt: "Buquê de Sabonetes Doce Carinho", es: "Ramo de Jabones Dulce Cariño", en: "Sweet Affection Soap Bouquet", fr: "Bouquet de Savons Doux Câlin", basePrice: 23.90 },
    { pt: "Cesta de Presente Flores do Campo", es: "Cesta de Regalo Flores del Campo", en: "Wildflowers Gift Basket", fr: "Panier Cadeau Fleurs des Champs", basePrice: 28.90 },
    { pt: "Arranjo de Sabonetes Peónias de Luxo", es: "Arreglo de Jabones Peonías de Lujo", en: "Luxury Peonies Soap Arrangement", fr: "Arrangement de Savons Pivoines de Luxe", basePrice: 27.90 },
    { pt: "Buquê de Sabonetes Amor Eterno", es: "Ramo de Jabones Amor Eterno", en: "Eternal Love Soap Bouquet", fr: "Bouquet de Savons Amour Éternel", basePrice: 29.90 }
];

for (let i = 1; i <= 10; i++) {
    const bouquet = BOUQUET_NAMES[i - 1];
    PRODUCTS.push({
        id: `buque-${i}`,
        category: "set",
        price: bouquet.basePrice,
        image: `assets/buque_${i}.jpeg`,
        qty: 1,
        pt: {
            name: bouquet.pt,
            categoryLabel: "Set de Oferta / Buquê",
            aromaBrief: "Arranjo floral artístico feito inteiramente de sabonetes artesanais perfumados.",
            description: `Um maravilhoso arranjo feito à mão com sabonetes em forma de flores realistas. Ideal para oferecer como um presente único e sofisticado, ou para decorar e perfumar qualquer ambiente com elegância. Apresentado com embrulho decorativo premium.`,
            aromaProfile: "Floral Premium, Elegante, Festivo"
        },
        es: {
            name: bouquet.es,
            categoryLabel: "Set de Regalo / Ramo",
            aromaBrief: "Arreglo floral artístico hecho completamente de jabones artesanales aromáticos.",
            description: `Un maravilloso arreglo hecho a mano con jabones en forma de flores realistas. Ideal para ofrecer como un regalo único y sofisticado, o para decorar y perfumar cualquier ambiente con elegancia. Presentado con envoltorio decorativo premium.`,
            aromaProfile: "Floral Premium, Elegante, Festivo"
        },
        en: {
            name: bouquet.en,
            categoryLabel: "Gift Set / Bouquet",
            aromaBrief: "Artistic floral arrangement made entirely of scented handcrafted soaps.",
            description: `A wonderful handcrafted arrangement featuring realistic flower-shaped soaps. Perfect as a unique and sophisticated gift, or to elegantly decorate and scent any space. Presented in premium decorative packaging.`,
            aromaProfile: "Premium Floral, Elegant, Festive"
        },
        fr: {
            name: bouquet.fr,
            categoryLabel: "Coffret Cadeau / Bouquet",
            aromaBrief: "Arrangement floral artistique entièrement composé de savons artisanaux parfumés.",
            description: `Un magnifique arrangement fait main avec des savons en forme de fleurs réalistes. Idéal à offrir comme cadeau unique et sophistiqué, ou pour décorer et parfumer n'importe quel espace avec élégance. Présenté dans un emballage décoratif de qualité supérieure.`,
            aromaProfile: "Floral Premium, Élégant, Festif"
        }
    });
}

const VERAO_ITEMS = [
    { pt: "Vela Aromática Brisa do Mar", es: "Vela Aromática Brisa del Mar", en: "Sailing Breeze Scented Candle", fr: "Bougie Parfumée Brise Marine", category: "vela", price: 14.90, descPt: "Frescura marinha com notas de sal e brisa costeira.", descEs: "Frescura marina con notas de sal y brisa costera.", descEn: "Ocean freshness with notes of sea salt and coastal breeze.", descFr: "Fraîcheur océanique avec des notes de sel marin et de brise côtière." },
    { pt: "Sabonete de Coco & Lima de Verão", es: "Jabón de Coco & Lima de Verano", en: "Summer Coconut & Lime Soap", fr: "Savon Coco & Limette d'Été", category: "sabonete", price: 5.90, descPt: "Fórmula hidratante com aroma tropical de coco e raspa de lima.", descEs: "Fórmula hidratante con aroma tropical a coco y ralladura de lima.", descEn: "Moisturizing formula with a tropical scent of coconut and lime zest.", descFr: "Formule hydratante au parfum tropical de noix de coco et zeste de lime." },
    { pt: "Vela Aromática Sol de Verão", es: "Vela Aromática Sol de Verano", en: "Summer Sun Scented Candle", fr: "Bougie Parfumée Soleil d'Été", category: "vela", price: 13.90, descPt: "Notas cítricas brilhantes de tangerina e tangerina de verão.", descEs: "Notas cítricas brillantes de mandarina y mandarina de verano.", descEn: "Bright citrus notes of summer mandarin and tangerine.", descFr: "Notes d'agrumes éclatantes de mandarine et tangerine d'été." },
    { pt: "Sabonete Esfoliante de Sal e Citrinos", es: "Jabón Exfoliante de Sal y Cítricos", en: "Citrus & Salt Exfoliating Soap", fr: "Savon Exfoliant Sel & Agrumes", category: "sabonete", price: 6.50, descPt: "Esfoliação revigorante com sal marinho e óleos cítricos.", descEs: "Exfoliación revitalizante con sal marina y aceites cítricos.", descEn: "Invigorating exfoliation with sea salt and citrus essential oils.", descFr: "Exfoliation tonifiante au sel de mer et huiles essentielles d'agrumes." },
    { pt: "Vela Aromática Margaridas do Campo", es: "Vela Aromática Margaritas del Campo", en: "Wild Daisy Scented Candle", fr: "Bougie Parfumée Marguerites des Champs", category: "vela", price: 14.50, descPt: "Notas florais alegres e frescas que trazem a natureza para dentro de casa.", descEs: "Notas florales alegres y frescas que traen la naturaleza al hogar.", descEn: "Cheerful and fresh floral notes that bring nature indoors.", descFr: "Notes florales fraîches et joyeuses qui font entrer la nature chez vous." },
    { pt: "Sabonete de Hortelã e Limão Refrescante", es: "Jabón de Menta y Limón Refrescante", en: "Refreshing Mint & Lemon Soap", fr: "Savon Rafraîchissant Menthe & Citron", category: "sabonete", price: 5.90, descPt: "Efeito refrescante e estimulante para o banho nos dias quentes.", descEs: "Efecto refrescante y estimulante para el baño en días calurosos.", descEn: "Cooling and stimulating effect for bath time on warm days.", descFr: "Effet rafraîchissant et stimulant pour le bain lors des journées chaudes." },
    { pt: "Vela Aromática Pôr do Sol", es: "Vela Aromática Atardecer de Verano", en: "Sunset Scented Candle", fr: "Bougie Parfumée Coucher de Soleil", category: "vela", price: 14.90, descPt: "Uma fragrância quente e aveludada de pêssego e baunilha.", descEs: "Una fragancia cálida y azerciopelada de melocotón y vainilla.", descEn: "A warm and velvety fragrance of summer peach and vanilla.", descFr: "Un parfum chaud et velouté de pêche d'été et de vanille." },
    { pt: "Sabonete Hidratante Aloe de Verão", es: "Jabón Hidratante Aloe de Verano", en: "Summer Aloe Moisturizing Soap", fr: "Savon Hydratant Aloe d'Été", category: "sabonete", price: 5.90, descPt: "Hidratação calmante pós-sol com extrato natural de aloe vera.", descEs: "Hidratación calmante para después del sol con extracto de aloe vera.", descEn: "Calming post-sun hydration with natural aloe vera extract.", descFr: "Hydratation apaisante après-soleil à l'extrait naturel d'aloe vera." },
    { pt: "Vela Aromática Frutas Tropicais", es: "Vela Aromática Frutas Tropicales", en: "Tropical Fruits Scented Candle", fr: "Bougie Parfumée Fruits Tropicaux", category: "vela", price: 13.90, descPt: "Fragrância doce e exótica de manga, maracujá e papaia.", descEs: "Fragancia dulce y exótica de mango, maracuyá y papaya.", descEn: "Sweet and exotic fragrance of mango, passionfruit, and papaya.", descFr: "Parfum doux et exotique de mangue, fruit de la passion et papaye." },
    { pt: "Sabonete Suave de Manga & Papaia", es: "Jabón Suave de Mango & Papaya", en: "Mango & Papaya Soft Soap", fr: "Savon Doux Mangue & Papaye", category: "sabonete", price: 5.90, descPt: "Nutrição tropical com espuma cremosa e aroma frutado doce.", descEs: "Nutrición tropical con espuma cremosa y aroma frutado dulce.", descEn: "Tropical nourishment with creamy lather and sweet fruity scent.", descFr: "Nutrition tropicale avec une mousse crémeuse et un parfum fruité doux." },
    { pt: "Vela Aromática Noites de Verão", es: "Vela Aromática Noches de Verano", en: "Summer Nights Scented Candle", fr: "Bougie Parfumée Nuits d'Été", category: "vela", price: 14.90, descPt: "Sedução noturna com jasmim da meia-noite e sândalo quente.", descEs: "Seducción nocturna con jazmín de medianoche y sándalo cálido.", descEn: "Night seduction with midnight jasmine and warm sandalwood.", descFr: "Séduction nocturne avec du jasmin de minuit et du bois de santal chaud." },
    { pt: "Sabonete de Lavanda de Verão", es: "Jabón de Lavanda de Verano", en: "Summer Lavender Soap", fr: "Savon Lavande d'Été", category: "sabonete", price: 5.90, descPt: "Relaxamento fresco de lavanda colhida no pico do verão.", descEs: "Relajación fresca de lavanda cosechada en el pico del verano.", descEn: "Fresh relaxation of lavender harvested at peak summer.", descFr: "Relaxation fraîche de lavande récoltée au cœur de l'été." }
];

for (let i = 1; i <= 12; i++) {
    const item = VERAO_ITEMS[i - 1];
    const itemData = {
        id: `verao-${i}`,
        category: item.category,
        price: item.price,
        image: `assets/verao_${i}.jpeg`,
        qty: 1,
        pt: {
            name: item.pt,
            categoryLabel: item.category === "vela" ? "Vela Aromática (Verão)" : "Sabonete de Verão",
            aromaBrief: item.descPt,
            description: `${item.pt} da nossa coleção exclusiva de Verão. Feito à mão com ingredientes naturais e selecionados para trazer o frescor da estação.`,
            aromaProfile: "Verão, Frescor, Edição Limitada"
        },
        es: {
            name: item.es,
            categoryLabel: item.category === "vela" ? "Vela Aromática (Verano)" : "Jabón de Verano",
            aromaBrief: item.descEs,
            description: `${item.es} de nuestra colección exclusiva de Verano. Hecho a mano con ingredientes naturales y seleccionados para traer la frescura de la estación.`,
            aromaProfile: "Verano, Frescura, Edición Limitada"
        },
        en: {
            name: item.en,
            categoryLabel: item.category === "vela" ? "Scented Candle (Summer)" : "Summer Soap",
            aromaBrief: item.descEn,
            description: `${item.en} from our exclusive Summer Collection. Handcrafted with natural ingredients chosen to bring the seasonal freshness.`,
            aromaProfile: "Summer, Freshness, Limited Edition"
        },
        fr: {
            name: item.fr,
            categoryLabel: item.category === "vela" ? "Bougie Parfumée (Été)" : "Savon d'Été",
            aromaBrief: item.descFr,
            description: `${item.fr} de notre collection exclusive d'Été. Fait main avec des ingrédients naturels pour apporter la fraîcheur de la saison.`,
            aromaProfile: "Été, Fraîcheur, Édition Limitée"
        }
    };
    
    if (item.category === "sabonete") {
        SOAP_GALLERY.push(itemData);
    } else {
        PRODUCTS.push(itemData);
    }
}

const RECORDACAO_NAMES = [
    { pt: "Recordação de Casamento Personalizada", es: "Recuerdo de Boda Personalizado", en: "Personalized Wedding Favor", fr: "Souvenir de Mariage Personnalisé", price: 3.50 },
    { pt: "Recordação de Batizado Anjinho", es: "Recuerdo de Bautizo Angelito", en: "Little Angel Baptism Favor", fr: "Souvenir de Baptême Petit Ange", price: 3.20 },
    { pt: "Recordação de Comunhão Rústica", es: "Recuerdo de Comunión Rústico", en: "Rustic Communion Favor", fr: "Souvenir de Communion Rustique", price: 3.50 },
    { pt: "Recordação de Aniversário Especial", es: "Recuerdo de Cumpleaños Especial", en: "Special Birthday Favor", fr: "Souvenir d'Anniversaire Spécial", price: 3.00 },
    { pt: "Recordação de Evento Corporativo", es: "Recuerdo de Evento Corporativo", en: "Corporate Event Favor", fr: "Souvenir d'Événement D'Entreprise", price: 4.50 },
    { pt: "Recordação de Maternidade Pés de Bebé", es: "Recuerdo de Maternidad Pies de Bebé", en: "Baby Feet Maternity Favor", fr: "Souvenir de Maternité Pieds de Bébé", price: 2.80 }
];

for (let i = 1; i <= 6; i++) {
    const rec = RECORDACAO_NAMES[i - 1];
    PRODUCTS.push({
        id: `recordacao-${i}`,
        category: "decorativa",
        price: rec.price,
        image: `assets/recordacao_${i}.jpeg`,
        qty: 1,
        pt: {
            name: rec.pt,
            categoryLabel: "Recordação / Lembrancinha",
            aromaBrief: "Lembrança artesanal personalizada para tornar o seu evento inesquecível.",
            description: `Recordação artesanal feita sob encomenda em Portugal. Criada com materiais premium para celebrar datas especiais como casamentos, batizados, comunhões ou eventos corporativos. Personalizável sob consulta.`,
            aromaProfile: "Personalizado, Eventos, Artesanato"
        },
        es: {
            name: rec.es,
            categoryLabel: "Recuerdo / Detalle de Evento",
            aromaBrief: "Detalle artesanal personalizado para hacer tu evento inolvidable.",
            description: `Recuerdo artesanal hecho bajo pedido en Portugal. Creado con materiales premium para celebrar fechas especiales como bodas, bautizos, comuniones o eventos corporativos. Personalizable bajo consulta.`,
            aromaProfile: "Personalizado, Eventos, Artesanía"
        },
        en: {
            name: rec.en,
            categoryLabel: "Event Favor / Souvenir",
            aromaBrief: "Handcrafted personalized favor to make your event unforgettable.",
            description: `Handcrafted event favor made to order in Portugal. Created with premium materials to celebrate special dates like weddings, baptisms, communions, or corporate events. Custom options available.`,
            aromaProfile: "Personalized, Events, Handcrafted"
        },
        fr: {
            name: rec.fr,
            categoryLabel: "Souvenir / Cadeau d'Invité",
            aromaBrief: "Cadeau d'invité artisanal personnalisé pour rendre votre événement inoubliable.",
            description: `Souvenir artisanal fabriqué sur commande au Portugal. Créé avec des matériaux de qualité pour célébrer des occasions spéciales (mariages, baptêmes, communions, événements). Personnalisable.`,
            aromaProfile: "Personnalisé, Événements, Artisanal"
        }
    });
}

PRODUCTS.push({
    id: "wax-melt-1",
    category: "vela",
    price: 4.50,
    image: "assets/wax_melt_1.jpeg",
    qty: 1,
    pt: {
        name: "Wax Melts de Soja Aromáticos",
        categoryLabel: "Cera de Soja / Ambientador",
        aromaBrief: "Wax melts de soja natural e óleos essenciais para queimadores.",
        description: "Fundidos à mão com cera de soja natural e óleos essenciais premium. Perfeitos para libertar fragrâncias intensas e contínuas quando derretidos num queimador de essências. Uma alternativa ecológica e prática para perfumar a sua casa.",
        aromaProfile: "Fragrância Intensa, Cera de Soja, Prático"
    },
    es: {
        name: "Wax Melts de Soja Aromáticos",
        categoryLabel: "Cera de Soja / Ambientador",
        aromaBrief: "Wax melts de soja natural y aceites esenciales para quemadores.",
        description: "Fundidos a mano con cera de soja natural y aceites esenciales premium. Perfectos para liberar fragancias intensas y continuas cuando se derriten en un quemador de esencias. Una alternativa ecológica y práctica para perfumar tu hogar.",
        aromaProfile: "Fragancia Intensa, Cera de Soja, Práctico"
    },
    en: {
        name: "Aromatic Soy Wax Melts",
        categoryLabel: "Soy Wax / Home Fragrance",
        aromaBrief: "Natural soy wax melts and essential oils for burners.",
        description: "Hand-poured with natural soy wax and premium essential oils. Perfect for releasing intense, continuous scents when melted in a fragrance burner. An eco-friendly and practical alternative to scent your home.",
        aromaProfile: "Intense Scent, Soy Wax, Practical"
    },
    fr: {
        name: "Fondants de Cire de Soja Parfumés",
        categoryLabel: "Cire de Soja / Parfum de Maison",
        aromaBrief: "Fondants de cire de soja naturelle et huiles essentielles pour brûleurs.",
        description: "Fabriqués à la main avec de la cire de soja naturelle et des huiles essentielles de qualité. Parfaits pour diffuser des parfums intenses et continus une fois fondus dans un brûle-parfum. Une alternative écologique et pratique.",
        aromaProfile: "Parfum Intense, Cire de Soja, Pratique"
    }
});

PRODUCTS.push({
    id: "candle-special-1",
    category: "vela",
    price: 15.90,
    image: "assets/candle_special_1.jpeg",
    qty: 1,
    pt: {
        name: "Vela Aromática Edição Especial",
        categoryLabel: "Vela Aromática",
        aromaBrief: "Vela aromática premium em vaso de vidro com decoração floral exclusiva.",
        description: "Vela decorativa premium de edição limitada, fundida à mão com cera de soja natural em vaso de vidro elegante. Adornada delicadamente no topo com flores secas botânicas. Proporciona uma queima limpa e perfumada, ideal para criar momentos únicos.",
        aromaProfile: "Cítrico Floral, Edição Especial, Sofisticado"
    },
    es: {
        name: "Vela Aromática Edición Especial",
        categoryLabel: "Vela Aromática",
        aromaBrief: "Vela aromática premium en vaso de vidrio con decoración floral exclusiva.",
        description: "Vela decorativa premium de edición limitada, fundida a mano con cera de soja natural en un elegante vaso de vidrio. Adornada delicadamente en la parte superior con flores secas botánicas. Proporciona una quema limpia y perfumada.",
        aromaProfile: "Cítrico Floral, Edición Especial, Sofisticado"
    },
    en: {
        name: "Special Edition Scented Candle",
        categoryLabel: "Scented Candle",
        aromaBrief: "Premium scented candle in glass jar with exclusive floral decoration.",
        description: "Premium limited-edition decorative candle, hand-poured with natural soy wax in an elegant glass jar. Delicately adorned on top with dried botanical flowers. Provides a clean, scented burn, perfect for creating unique moments.",
        aromaProfile: "Floral Citrus, Special Edition, Sophisticated"
    },
    fr: {
        name: "Bougie Parfumée Édition Spéciale",
        categoryLabel: "Bougie Parfumée",
        aromaBrief: "Bougie parfumée premium en pot de verre avec décoration florale exclusive.",
        description: "Bougie décorative de qualité supérieure en édition limitée, coulée à la main avec de la cire de soja naturelle dans un pot de verre élégant. Délicatement ornée de fleurs séchées sur le dessus. Offre une combustion propre et parfumée.",
        aromaProfile: "Floral Citronné, Édition Spéciale, Sophistiqué"
    }
});


// WhatsApp Contact Configuration
const WHATSAPP_NUMBER = "351939636842";

// Global i18n & Cart State
let currentLang = "pt";
let cart = [];

// Global Pagination & Catalog State
let currentCategory = "all";
let currentPage = 1;
const productsPerPage = 3;

/* ==========================================================================
   GLOBAL DICTIONARY OF TRANSLATIONS (PT, ES, EN, FR)
   ========================================================================== */
const TRANSLATIONS = {
    "page-title": {
        pt: "Com Cheiro de Amor | Velas, Sabonetes e Peças Decorativas",
        es: "Com Cheiro de Amor | Velas, Jabones y Piezas Decorativas",
        en: "Com Cheiro de Amor | Candles, Soaps and Decorative Pieces",
        fr: "Com Cheiro de Amor | Bougies, Savons et Pièces Décoratives"
    },
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
    "nav-link-sabonetes": {
        pt: "Sabonetes",
        es: "Jabones",
        en: "Soaps",
        fr: "Savons"
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
    "filter-decorativas": {
        pt: "Peças Decorativas",
        es: "Piezas Decorativas",
        en: "Decorative Pieces",
        fr: "Pièces Décoratives"
    },
    "brand-reg-title": {
        pt: "Marca Oficial Registada",
        es: "Marca Oficial Registrada",
        en: "Official Registered Trademark",
        fr: "Marque Officielle Déposée"
    },
    "brand-reg-desc": {
        pt: "A marca Com Cheiro de Amor® encontra-se registada e patenteada no INPI (Instituto Nacional da Propriedade Industrial) como MARCA NACIONAL N.º 758901. Garantia de qualidade, autenticidade e design exclusivo em cada produto.",
        es: "La marca Com Cheiro de Amor® se encuentra registrada y patentada en el INPI como MARCA NACIONAL n.º 758901. Garantía de calidad, autenticidad y diseño exclusivo en cada producto.",
        en: "The brand Com Cheiro de Amor® is registered and patented at the INPI as NATIONAL TRADEMARK no. 758901. A guarantee of quality, authenticity, and exclusive design in every product.",
        fr: "La marque Com Cheiro de Amor® est enregistrée et brevetée auprès de l'INPI sous la MARQUE NATIONALE n° 758901. Garantie de qualité, d'authenticité et de design exclusif pour chaque produit."
    },
    "pag-prev": {
        pt: "Página Anterior",
        es: "Página Anterior",
        en: "Previous Page",
        fr: "Page Précédente"
    },
    "pag-next": {
        pt: "Página Seguinte",
        es: "Página Siguiente",
        en: "Next Page",
        fr: "Page Suivante"
    },
    "pag-of": {
        pt: "de",
        es: "de",
        en: "of",
        fr: "sur"
    },
    "pag-page": {
        pt: "Página",
        es: "Página",
        en: "Page",
        fr: "Page"
    },
    "sabonetes-subtitle": {
        pt: "A Nossa Saboaria",
        es: "Nuestra Jabonería",
        en: "Our Soap Collection",
        fr: "Notre Savonnerie"
    },
    "sabonetes-title": {
        pt: "Texturas & Aromas",
        es: "Texturas & Aromas",
        en: "Textures & Aromas",
        fr: "Textures & Arômes"
    },
    "sabonetes-desc": {
        pt: "Conheça a nossa linha exclusiva de sabonetes botânicos e artesanais. Elaborados em pequenos lotes com óleos vegetais de alta qualidade, argilas purificantes e botânicos naturais para mimar a sua pele.",
        es: "Conozca nuestra línea exclusiva de jabones botánicos y artesanales. Elaborados en pequeños lotes con aceites vegetales de alta calidad, arcillas purificantes y botánicos naturales para mimar su piel.",
        en: "Discover our exclusive line of botanical and handcrafted soaps. Made in small batches with high-quality vegetable oils, purifying clays, and natural botanicals to pamper your skin.",
        fr: "Découvrez notre gamme exclusive de savons botaniques et artisanaux. Fabriqués en petits lots avec des huiles végétales de haute qualité, des argiles purifiantes et des plantes naturelles pour chouchouter votre peau."
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
    
    // Theme toggle elements & initialization
    const themeToggleBtn = document.getElementById("btn-theme-toggle");

    const initTheme = () => {
        const savedTheme = localStorage.getItem("theme");
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        
        if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
            document.body.classList.add("dark-theme");
        } else {
            document.body.classList.remove("dark-theme");
        }
    };

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark-theme");
            const isDark = document.body.classList.contains("dark-theme");
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }

    initTheme();
    
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

    // Helper function to resolve active filtered products including soaps
    const getFilteredProducts = (category) => {
        if (category === "sabonete") {
            return SOAP_GALLERY;
        } else if (category === "all") {
            return PRODUCTS;
        } else {
            return PRODUCTS.filter(p => p.category === category);
        }
    };

    // Catalog side navigation buttons
    const catalogPrevBtn = document.getElementById("catalog-prev");
    const catalogNextBtn = document.getElementById("catalog-next");

    if (catalogPrevBtn) {
        catalogPrevBtn.addEventListener("click", () => {
            if (currentPage > 1) {
                changePage(currentPage - 1);
            }
        });
    }

    if (catalogNextBtn) {
        catalogNextBtn.addEventListener("click", () => {
            const filteredProducts = getFilteredProducts(currentCategory);
            const totalProducts = filteredProducts.length;
            const totalPages = Math.ceil(totalProducts / productsPerPage);
            if (currentPage < totalPages) {
                changePage(currentPage + 1);
            }
        });
    }

    // Nav link for Sabonetes to scroll to catalog and click the Sabonetes tab
    const navLinkSabonetes = document.getElementById("nav-link-sabonetes");
    if (navLinkSabonetes) {
        navLinkSabonetes.addEventListener("click", (e) => {
            e.preventDefault();
            const catalogSection = document.getElementById("catalogo");
            if (catalogSection) {
                catalogSection.scrollIntoView({ behavior: "smooth" });
            }
            const filterSabonetesTab = document.getElementById("filter-sabonetes");
            if (filterSabonetesTab) {
                setTimeout(() => {
                    filterSabonetesTab.click();
                }, 100);
            }
        });
    }

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
            // Translate the page title
            if (TRANSLATIONS["page-title"] && TRANSLATIONS["page-title"][lang]) {
                document.title = TRANSLATIONS["page-title"][lang];
            }

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
        
        // Update current category and reset page if category changed
        if (currentCategory !== categoryFilter) {
            currentCategory = categoryFilter;
            currentPage = 1;
        }

        let filteredProducts;
        if (categoryFilter === "sabonete") {
            filteredProducts = SOAP_GALLERY;
        } else if (categoryFilter === "all") {
            filteredProducts = PRODUCTS;
        } else {
            filteredProducts = PRODUCTS.filter(p => p.category === categoryFilter);
        }

        const totalProducts = filteredProducts.length;
        const totalPages = Math.ceil(totalProducts / productsPerPage);
        
        // Ensure current page is within valid range
        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const startIdx = (currentPage - 1) * productsPerPage;
        const endIdx = startIdx + productsPerPage;
        const pageProducts = filteredProducts.slice(startIdx, endIdx);

        pageProducts.forEach(product => {
            const translation = product[currentLang];
            const card = document.createElement("div");
            card.className = "product-card";
            card.setAttribute("data-id", product.id);
            
            // Resolve fallback properties for soap cards
            const categoryLabel = translation.categoryLabel || (currentLang === 'pt' ? 'Sabonete de Banho' : currentLang === 'es' ? 'Jabón de Baño' : currentLang === 'en' ? 'Bath Soap' : 'Savon de Bain');
            const aromaBrief = translation.aromaBrief || translation.desc || "";

            card.innerHTML = `
                <div class="product-image-container">
                    <span class="product-badge">${categoryLabel}</span>
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
                    <span class="product-category">${categoryLabel}</span>
                    <h3 class="product-name">${translation.name}</h3>
                    <p class="product-aroma-brief">${aromaBrief}</p>
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

        // Render Pagination Controls
        renderPagination(totalPages);
    };

    const renderPagination = (totalPages) => {
        const paginationContainer = document.getElementById("catalog-pagination-container");
        const catalogPrevBtn = document.getElementById("catalog-prev");
        const catalogNextBtn = document.getElementById("catalog-next");
        
        if (!paginationContainer) return;

        paginationContainer.innerHTML = "";

        if (totalPages <= 1) {
            paginationContainer.style.display = "none";
            if (catalogPrevBtn) catalogPrevBtn.style.display = "none";
            if (catalogNextBtn) catalogNextBtn.style.display = "none";
            return;
        } else {
            paginationContainer.style.display = "flex";
            if (catalogPrevBtn) catalogPrevBtn.style.display = "flex";
            if (catalogNextBtn) catalogNextBtn.style.display = "flex";
        }

        const isFirstPage = currentPage === 1;
        const isLastPage = currentPage === totalPages;

        // Update disabled states
        if (catalogPrevBtn) {
            catalogPrevBtn.disabled = isFirstPage;
            if (isFirstPage) {
                catalogPrevBtn.classList.add("disabled");
            } else {
                catalogPrevBtn.classList.remove("disabled");
            }
        }

        if (catalogNextBtn) {
            catalogNextBtn.disabled = isLastPage;
            if (isLastPage) {
                catalogNextBtn.classList.add("disabled");
            } else {
                catalogNextBtn.classList.remove("disabled");
            }
        }

        // Page Indicator text
        const pageIndicator = document.createElement("div");
        pageIndicator.className = "pagination-indicator";
        pageIndicator.innerHTML = `
            <span>${TRANSLATIONS["pag-page"][currentLang]} <strong>${currentPage}</strong> ${TRANSLATIONS["pag-of"][currentLang]} <strong>${totalPages}</strong></span>
        `;

        paginationContainer.appendChild(pageIndicator);
    };

    const changePage = (newPage) => {
        const isForward = newPage > currentPage;
        currentPage = newPage;
        
        // Elegant lateral slide transition
        productsGrid.style.transition = "opacity 0.25s ease, transform 0.25s ease";
        productsGrid.style.opacity = "0";
        productsGrid.style.transform = isForward ? "translateX(-30px)" : "translateX(30px)";
        
        setTimeout(() => {
            renderProducts(currentCategory);
            
            // Set initial state for entrance animation
            productsGrid.style.transition = "none";
            productsGrid.style.transform = isForward ? "translateX(30px)" : "translateX(-30px)";
            
            // Force reflow
            void productsGrid.offsetWidth;
            
            // Animate in
            productsGrid.style.transition = "opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), transform 0.35s cubic-bezier(0.16, 1, 0.3, 1)";
            productsGrid.style.opacity = "1";
            productsGrid.style.transform = "translateX(0)";
        }, 250);
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
        let product = PRODUCTS.find(p => p.id === productId);
        if (!product) {
            product = SOAP_GALLERY.find(s => s.id === productId);
            if (product) {
                openSoapModal(productId);
            }
            return;
        }

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

    const openSoapModal = (soapId) => {
        const soap = SOAP_GALLERY.find(s => s.id === soapId);
        if (!soap) return;

        activeModalProductId = soapId;
        activeModalQty = 1;

        const translation = soap[currentLang];

        // Populate Modal Fields
        modalImg.src = soap.image;
        modalImg.alt = translation.name;
        modalCategory.textContent = currentLang === 'pt' ? 'Sabonete de Banho' : currentLang === 'es' ? 'Jabón de Baño' : currentLang === 'en' ? 'Bath Soap' : 'Savon de Bain';
        modalTitle.textContent = translation.name;
        modalPrice.textContent = `€${soap.price.toFixed(2)}`;
        modalDescription.textContent = translation.longDesc || translation.desc;
        aromaNotes.textContent = translation.aromaProfile || "Natural, Hidratante, Botânico";
        
        modalQtyNum.textContent = activeModalQty;

        // Show Modal
        modal.classList.add("active");
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
        let product = PRODUCTS.find(p => p.id === productId);
        if (!product) {
            product = SOAP_GALLERY.find(s => s.id === productId);
        }
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
            const categoryLabel = translation.categoryLabel || (currentLang === 'pt' ? 'Sabonete de Banho' : currentLang === 'es' ? 'Jabón de Baño' : currentLang === 'en' ? 'Bath Soap' : 'Savon de Bain');

            const itemEl = document.createElement("div");
            itemEl.className = "cart-item";
            itemEl.innerHTML = `
                <img src="${item.image}" alt="${translation.name}" class="cart-item-img">
                <div class="cart-item-detail">
                    <div>
                        <span class="cart-item-category">${categoryLabel}</span>
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

    // Initialize default products render
    renderProducts("all");
    updateCartCount();
});
