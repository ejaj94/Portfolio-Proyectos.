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
            description: "An exclusive handcrafted decorative piece made of premium eco-friendly plaster, finished with a satin waterproof coating. Perfect for organizing jewelry, perfumes, soaps, or as a base for our scented candles. Each piece is unique and individually molded in Portugal.",
            aromaProfile: "Eco-friendly, Exclusive Design, Handcrafted"
        },
        fr: {
            name: `${nameTemplate.fr} #${i}`,
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Design minimaliste et élégant en plâtre écologique avec finition imperméable.",
            description: "Une pièce de plâtre écologique haut de gamme fabriquée à la main, avec une finition satinée imperméable. Parfaite pour organiser des bijoux, des parfums, des savons ou comme support pour nos bougies. Chaque pièce est unique et moulée individuellement en Portugal.",
            aromaProfile: "Éco-responsable, Design Exclusif, Fait Main"
        }
    });
}

// 15 Soap Gallery Items for Showcase with multi-language name and descriptions to support perfect 3-by-3 layout
const SOAP_GALLERY = [
    {
        id: "soap-rose",
        price: 5.90,
        image: "assets/soap_rose.png",
        pt: {
            name: "Sabonete de Rosas & Argila Rosa",
            desc: "Uma fragrância romântica de pétalas de rosa com as propriedades purificantes da argila rosa.",
            longDesc: "Sabonete artesanal elaborado pelo método tradicional de saponificação a frio (cold process). Rico em óleos vegetais de amêndoas doces e manteiga de karité, nutre profundamente a pele. A argila rosa limpa suavemente as impurezas enquanto as pétalas de rosa proporcionam uma leve esfoliação natural.",
            aromaProfile: "Floral Clássico, Delicado, Atalcado, Hidratante"
        },
        es: {
            name: "Jabón de Rosas & Arcilla Rosa",
            desc: "Una fragancia romántica de pétalos de rosa con las propiedades purificantes de la arcilla rosa.",
            longDesc: "Jabón artesanal elaborado por el método tradicional de saponificación en frío (cold process). Rico en aceites vegetales de almendras dulces y manteca de karité, nutre profundamente la piel. La arcilla rosa limpia suavemente las impurezas mientras que los pétalos de rosa proporcionan una exfoliación natural suave.",
            aromaProfile: "Floral Clásico, Delicado, Atalcado, Hidratante"
        },
        en: {
            name: "Rose & Pink Clay Soap",
            desc: "A romantic fragrance of rose petals combined with the purifying properties of pink clay.",
            longDesc: "Handcrafted soap made using the traditional cold process saponification method. Rich in sweet almond vegetable oils and shea butter, it deeply nourishes the skin. Pink clay gently cleanses impurities while rose petals provide a gentle natural exfoliation.",
            aromaProfile: "Classic Floral, Delicate, Powdery, Moisturizing"
        },
        fr: {
            name: "Savon aux Roses & Argile Rose",
            desc: "Un parfum romantique de pétales de rose associé aux propriétés purifiantes de l'argile rose.",
            longDesc: "Savon artisanal élaboré selon la méthode traditionnelle de saponification à froid (cold process). Riche en huiles végétales d'amande douce et en beurre de karité, il nourrit la peau en profondeur. L'argile rose nettoie en douceur les impuretés tandis que les pétales de rose procurent une légère exfoliation naturelle.",
            aromaProfile: "Floral Classique, Délicat, Poudré, Hydratant"
        }
    },
    {
        id: "soap-honey",
        price: 5.90,
        image: "assets/soap_honey.png",
        pt: {
            name: "Sabonete de Aveia & Mel de Flores",
            desc: "Notas doces e nutritivas de mel silvestre misturadas com a esfoliação suave da aveia integral.",
            longDesc: "Altamente hidratante, acalma peles secas e sensíveis. Combina mel de abelhas local, que atua como humectante natural, com aveia triturada para uma massagem esfoliante estimulante. Produz uma espuma rica, cremosa e deliciosamente perfumada que deixa a pele incrivelmente macia.",
            aromaProfile: "Doce de Mel, Quente, Amendoado, Esfoliante"
        },
        es: {
            name: "Jabón de Avena & Miel de Flores",
            desc: "Notas dulces y nutritivas de miel silvestre mezcladas con la exfoliación suave de la avena integral.",
            longDesc: "Altamente hidratante, calma las pieles secas y sensibles. Combina miel de abejas local, que actúa como humectante natural, con avena triturada para un masaje exfoliante estimulante. Produce una espuma rica, cremosa y deliciosamente perfumada que deja la piel increíblemente suave.",
            aromaProfile: "Dulce de Miel, Cálido, Almendrado, Exfoliante"
        },
        en: {
            name: "Oatmeal & Flower Honey Soap",
            desc: "Sweet and nourishing wild honey notes mixed with the gentle exfoliation of whole oats.",
            longDesc: "Highly moisturizing, it soothes dry and sensitive skins. Combines local bee honey, which acts as a natural humectant, with ground oats for a stimulating exfoliating massage. Produces a rich, creamy, and deliciously scented lather that leaves skin incredibly soft.",
            aromaProfile: "Sweet Honey, Warm, Nutty, Exfoliating"
        },
        fr: {
            name: "Savon Flocons d'Avoine & Miel",
            desc: "Des notes douces et nourrissantes de miel sauvage mélangées à l'exfoliation douce de l'avoine entière.",
            longDesc: "Hautement hydratant, il apaise les peaux sèches et sensibles. Il combine le miel d'abeilles local, qui agit comme un humectant naturel, et l'avoine moulue pour un massage exfoliant stimulant. Produit une mousse riche, crémeuse et délicieusement parfumée qui laisse la peau incroyablement douce.",
            aromaProfile: "Doux de Miel, Chaud, Amande, Exfoliant"
        }
    },
    {
        id: "soap-gallery-1",
        price: 5.90,
        image: "assets/soap_gallery_1.jpg",
        pt: {
            name: "Sabonete Rosas & Argila",
            desc: "Esfoliação suave e tonificante botânica com pétalas de rosa.",
            longDesc: "Infundido com argila rosa purificante, este sabonete limpa profundamente a pele sem a ressecar. As pétalas secas de rosa no topo oferecem uma esfoliação física muito suave, estimulando a regeneração celular.",
            aromaProfile: "Floral Clássico, Suave, Hidratante"
        },
        es: {
            name: "Jabón de Rosas & Arcilla",
            desc: "Exfoliación suave y tonificación botánica con pétalos de rosa.",
            longDesc: "Infundido con arcilla rosa purificante, este jabón limpia profundamente la piel sin resecarla. Los pétalos secos de rosa en la parte superior ofrecen una exfoliación física muy suave, estimulando la regeneración celular.",
            aromaProfile: "Floral Clásico, Suave, Hidratante"
        },
        en: {
            name: "Rose & Clay Soap",
            desc: "Gentle exfoliation and botanical toning with rose petals.",
            longDesc: "Infused with purifying pink clay, this soap deeply cleanses the skin without drying it out. The dried rose petals on top offer a very gentle physical exfoliation, stimulating cellular regeneration.",
            aromaProfile: "Classic Floral, Gentle, Moisturizing"
        },
        fr: {
            name: "Savon Rose & Argile",
            desc: "Exfoliation douce et tonification botanique avec des pétales de rose.",
            longDesc: "Infusé d'argile rose purifiante, ce savon nettoie en profondeur la peau sans la dessécher. Les pétales de rose séchés sur le dessus offrent une exfoliation physique très douce, stimulant la régénération cellulaire.",
            aromaProfile: "Floral Classique, Doux, Hydratant"
        }
    },
    {
        id: "soap-gallery-2",
        price: 5.90,
        image: "assets/soap_gallery_2.jpg",
        pt: {
            name: "Sabonete Mel & Aveia",
            desc: "Nutrição e hidratação profunda natural com mel local.",
            longDesc: "Combinando as propriedades cicatrizantes do mel de abelhas local e a ação calmante da aveia integral. Cria uma espuma cremosa ideal para peles sensíveis, ásperas ou com tendência a irritações.",
            aromaProfile: "Doce de Mel, Amendoado, Suave"
        },
        es: {
            name: "Jabón de Miel & Avena",
            desc: "Nutrición e hidratación profunda natural con miel local.",
            longDesc: "Combinando las propiedades cicatrizantes de la miel de abejas local y la acción calmante de la avena integral. Crea una espuma cremosa ideal para pieles sensibles, ásperas o con tendencia a irritaciones.",
            aromaProfile: "Dulce de Miel, Almendrado, Suave"
        },
        en: {
            name: "Honey & Oats Soap",
            desc: "Natural deep nourishment and hydration with local honey.",
            longDesc: "Combining the healing properties of local bee honey and the soothing action of whole oats. Creates a creamy lather ideal for sensitive, rough, or irritation-prone skins.",
            aromaProfile: "Sweet Honey, Nutty, Soothing"
        },
        fr: {
            name: "Savon Miel & Avoine",
            desc: "Nutrition et hydratation profonde naturelle avec du miel local.",
            longDesc: "Combinant les propriétés cicatrisantes du miel d'abeilles local et l'action apaisante de l'avoine entière. Crée une mousse crémeuse idéale pour les peaux sensibles, rugueuses ou sujettes aux irritations.",
            aromaProfile: "Doux de Miel, Amande, Apaisant"
        }
    },
    {
        id: "soap-gallery-3",
        price: 5.90,
        image: "assets/soap_gallery_3.jpg",
        pt: {
            name: "Sabonete Alfazema do Campo",
            desc: "Calmante natural para a pele e mente com óleo essencial de lavanda.",
            longDesc: "Enriquecido com óleo essencial de lavanda puro. Um verdadeiro relaxante natural que acalma pequenas irritações da pele enquanto o aroma suave ajuda a relaxar a mente durante o banho.",
            aromaProfile: "Fresco, Floral, Herbal, Relaxante"
        },
        es: {
            name: "Jabón de Lavanda Silvestre",
            desc: "Calmante natural para la piel y mente con aceite esencial de lavanda.",
            longDesc: "Enriquecido con aceite esencial de lavanda puro. Un verdadero relajante natural que calma pequeñas irritaciones de la piel mientras el aroma suave ayuda a relajar la mente durante el baño.",
            aromaProfile: "Fresco, Floral, Herbal, Relajante"
        },
        en: {
            name: "Wild Lavender Soap",
            desc: "Natural soothing for skin and mind with lavender essential oil.",
            longDesc: "Enriched with pure lavender essential oil. A true natural relaxant that soothes minor skin irritations while the gentle scent helps to relax the mind during your bath.",
            aromaProfile: "Fresh, Floral, Herbal, Relaxing"
        },
        fr: {
            name: "Savon Lavande Sauvage",
            desc: "Apaisement naturel pour peau et esprit avec de l'huile essentielle de lavande.",
            longDesc: "Enrichi en huile essentielle de lavande pure. Un véritable relaxant naturel qui apaise les petites irritations de la peau tandis que le parfum doux aide à détendre l'esprit pendant le bain.",
            aromaProfile: "Frais, Floral, Herbal, Relaxant"
        }
    },
    {
        id: "soap-gallery-4",
        price: 5.90,
        image: "assets/soap_gallery_4.jpg",
        pt: {
            name: "Sabonete Laranja & Canela",
            desc: "Fragrância cítrica quente, revigorante e esfoliante suave.",
            longDesc: "Uma combinação clássica que estimula a circulação e renova a pele. O óleo essencial de laranja doce traz frescura cítrica, enquanto a canela moída oferece uma esfoliação média para remover células mortas.",
            aromaProfile: "Cítrico Quente, Especiado, Revigorante"
        },
        es: {
            name: "Jabón de Naranja & Canela",
            desc: "Fragancia cítrica cálida, vigorizante y exfoliación suave.",
            longDesc: "Una combinación clásica que estimula la circulación y renueva la piel. El aceite esencial de naranja dulce aporta frescura cítrica, mientras que la canela molida ofrece una exfoliación media para eliminar células muertas.",
            aromaProfile: "Cítrico Cálido, Especiado, Vigorizante"
        },
        en: {
            name: "Orange & Cinnamon Soap",
            desc: "Warm citrus fragrance, invigorating, and gentle exfoliation.",
            longDesc: "A classic combination that stimulates circulation and renews the skin. Sweet orange essential oil brings citrus freshness, while ground cinnamon offers medium exfoliation to remove dead skin cells.",
            aromaProfile: "Warm Citrus, Spiced, Invigorating"
        },
        fr: {
            name: "Savon Orange & Cannelle",
            desc: "Fragrance hespéridée chaude, vivifiante et exfoliation douce.",
            longDesc: "Une combinaison classique que stimule la circulation et renouvelle la peau. L'huile essentielle d'orange douce apporte une fraîcheur hespéridée, tandis que la cannelle moulue offre une exfoliation moyenne pour éliminer les cellules mortes.",
            aromaProfile: "Agrume Chaud, Épicé, Vivifiant"
        }
    },
    {
        id: "soap-gallery-5",
        price: 5.90,
        image: "assets/soap_gallery_5.jpg",
        pt: {
            name: "Sabonete Alecrim & Menta",
            desc: "Frescura refrescante e ação antisséptica suave para o corpo.",
            longDesc: "Infundido com óleo essencial de alecrim e hortelã-pimenta. Deixa uma sensação fresca e revigorante na pele, sendo ideal para o banho matinal. O alecrim limpa e tonifica de forma natural.",
            aromaProfile: "Herbal Fresco, Canforado, Estimulante"
        },
        es: {
            name: "Jabón de Romero & Menta",
            desc: "Frescura refrescante y acción antiséptica suave para el cuerpo.",
            longDesc: "Infundido con aceites esenciales de romero y menta piperita. Deja una sensación fresca y vigorizante en la piel, ideal para el baño matutino. El romero limpia y tonifica de forma natural.",
            aromaProfile: "Herbal Fresco, Alcanforado, Estimulante"
        },
        en: {
            name: "Rosemary & Mint Soap",
            desc: "Refreshing freshness and mild antiseptic action for the body.",
            longDesc: "Infused with rosemary and peppermint essential oils. Leaves a fresh, invigorating sensation on the skin, making it perfect for your morning shower. Rosemary cleanses and tones naturally.",
            aromaProfile: "Fresh Herbal, Camphorous, Stimulating"
        },
        fr: {
            name: "Savon Romarin & Menthe",
            desc: "Fraîcheur tonifiante et action antiseptique douce pour le corps.",
            longDesc: "Infusé d'huiles essentielles de romarin et de menthe poivrée. Laisse une sensation fraîche et vivifiante sur la peau, idéale pour la douche du matin. Le romarin nettoie et tonifie naturellement.",
            aromaProfile: "Herbal Frais, Camphré, Stimulant"
        }
    },
    {
        id: "soap-gallery-6",
        price: 5.90,
        image: "assets/soap_gallery_6.jpg",
        pt: {
            name: "Sabonete Carvão Ativado",
            desc: "Limpeza profunda e desintoxicação dos poros para peles oleosas.",
            longDesc: "Formulado com carvão vegetal ativado de coco, atua como um íman para retirar o excesso de sebo e impurezas dos poros. Recomendado para o rosto e zonas propensas a oleosidade excessiva.",
            aromaProfile: "Fresco, Purificante, Neutro"
        },
        es: {
            name: "Jabón de Carbón Activado",
            desc: "Limpieza profunda y desintoxicación de poros para pieles grasas.",
            longDesc: "Formulado con carbón vegetal activado de coco, actúa como un imán para eliminar el exceso de sebo e impurezas de los poros. Recomendado para el rostro y zonas propensas a oleosidad excesiva.",
            aromaProfile: "Fresco, Purificante, Neutro"
        },
        en: {
            name: "Activated Charcoal Soap",
            desc: "Deep pore cleansing and detoxification for oily skins.",
            longDesc: "Formulated with active coconut charcoal, it acts like a magnet to draw out excess sebum and impurities from pores. Recommended for face and oily-prone skin areas.",
            aromaProfile: "Fresh, Purifying, Neutral"
        },
        fr: {
            name: "Savon Charbon Actif",
            desc: "Nettoyage profond et détoxification des pores pour peaux grasses.",
            longDesc: "Formulé avec du charbon actif de coco, il agit comme un aimant pour éliminer l'excès de sébum et les impuretés des pores. Recommandé pour le visage et les zones sujettes à l'excès de sébum.",
            aromaProfile: "Frais, Purifiant, Neutre"
        }
    },
    {
        id: "soap-gallery-7",
        price: 5.90,
        image: "assets/soap_gallery_7.jpg",
        pt: {
            name: "Sabonete Calêndula & Óleos",
            desc: "Nutrição rica e suavidade extra para peles muito secas ou sensíveis.",
            longDesc: "Contém extrato oleoso de calêndula, manteiga de karité e óleo de amêndoas. Acalma a pele sensível, reduz vermelhidões e acelera a regeneração de pequenas descamações.",
            aromaProfile: "Delicado, Amendoado, Calmante"
        },
        es: {
            name: "Jabón de Caléndula & Aceites",
            desc: "Nutrición rica y suavidad extra para pieles muy secas o sensibles.",
            longDesc: "Contiene extracto oleoso de caléndula, manteca de karité y aceite de almendras. Calma la piel fusible, reduce rojeces y acelera la regeneración de pequeñas descamaciones.",
            aromaProfile: "Delicado, Almendrado, Calmante"
        },
        en: {
            name: "Calendula & Oils Soap",
            desc: "Rich nourishment and extra mildness for dry or sensitive skins.",
            longDesc: "Contains calendula oil extract, shea butter, and almond oil. Soothes sensitive skin, reduces redness, and speeds up the regeneration of minor dry patches.",
            aromaProfile: "Delicate, Nutty, Soothing"
        },
        fr: {
            name: "Savon Souci & Huiles",
            desc: "Nutrition riche et douceur extra pour peaux très sèches ou sensibles.",
            longDesc: "Contient de l'extrait d'huile de souci, du beurre de karité et de l'huile d'amande. Apaise les peaux sensibles, réduit les rougeurs et accélère la régénération des petites desquamations.",
            aromaProfile: "Délicat, Amande, Apaisant"
        }
    },
    {
        id: "soap-gallery-8",
        price: 5.90,
        image: "assets/soap_gallery_8.jpg",
        pt: {
            name: "Coleção Flores & Detalhes",
            desc: "Variedade de sabonetes com relevos artísticos e florais refinados.",
            longDesc: "Um conjunto requintado que reúne formatos florais, relevos clássicos e formas ovais trabalhadas. Ideal para criar um presente personalizado ou para adicionar um toque de elegância escultural à sua casa de banho.",
            aromaProfile: "Floral, Delicado, Nobre"
        },
        es: {
            name: "Colección Flores & Detalles",
            desc: "Variedad de jabones con relieves artísticos y florales refinados.",
            longDesc: "Un conjunto exquisito que reúne formas florales, relieves clásicos y moldes ovalados trabajados. Ideal para crear un regalo personalizado o añadir un toque de elegancia escultural a su cuarto de baño.",
            aromaProfile: "Floral, Delicado, Noble"
        },
        en: {
            name: "Flowers & Details Collection",
            desc: "Variety of soaps with artistic and refined floral reliefs.",
            longDesc: "An exquisite set featuring floral shapes, classic reliefs, and crafted oval forms. Ideal for creating a customized gift or adding a touch of sculptural elegance to your bathroom.",
            aromaProfile: "Floral, Delicate, Noble"
        },
        fr: {
            name: "Collection Fleurs & Détails",
            desc: "Variété de savons avec des reliefs artistiques et floraux raffinés.",
            longDesc: "Un coffret exquis réunissant des formes florales, des reliefs classiques et des moules ovales travaillés. Idéal pour composer un cadeau personnalisé ou ajouter une touche d'élégance sculpturale à votre salle de bain.",
            aromaProfile: "Floral, Délicat, Noble"
        }
    },
    {
        id: "soap-gallery-9",
        price: 5.90,
        image: "assets/soap_gallery_9.jpg",
        pt: {
            name: "Renda de Argila Negra",
            desc: "Padrão de renda decorativa infundido com argila preta purificante.",
            longDesc: "A fusão perfeita entre estética e funcionalidade. Com um desenho de renda de alta precisão impresso sobre a superfície, este sabonete liberta minerais purificantes de argila preta ao entrar em contacto com a água.",
            aromaProfile: "Suave, Purificador, Herbal"
        },
        es: {
            name: "Encaje de Arcilla Negra",
            desc: "Patrón de encaje decorativo infundido con arcilla negra purificante.",
            longDesc: "La fusión perfecta entre estética y funcionalidad. Con un diseño de encaje de alta precisión grabado en la superficie, este jabón libera minerales purificantes de arcilla negra al entrar en contacto con el agua.",
            aromaProfile: "Suave, Purificante, Herbal"
        },
        en: {
            name: "Black Clay Lace Soap",
            desc: "Decorative lace pattern infused with purifying black clay.",
            longDesc: "The perfect fusion of aesthetics and functionality. Featuring a high-precision lace design embossed on the surface, this soap releases purifying black clay minerals upon contact with water.",
            aromaProfile: "Gentle, Purifying, Herbal"
        },
        fr: {
            name: "Dentelle d'Argile Noire",
            desc: "Motif dentelle décoratif infusé d'argile noire purifiante.",
            longDesc: "La fusion parfaite entre esthétique et fonctionnalité. Avec un motif de dentelle de haute précision gravé sur la surface, ce savon libère des minéraux purifiants d'argile noire au contact de l'eau.",
            aromaProfile: "Doux, Purifiant, Herbal"
        }
    },
    {
        id: "soap-gallery-10",
        price: 5.90,
        image: "assets/soap_gallery_10.jpg",
        pt: {
            name: "Lótus & Argila Branca",
            desc: "Fórmula de argila branca ultra-suave com padrão floral de lótus.",
            longDesc: "Ideal para peles baças ou cansadas. A argila branca purifica suavemente as camadas da pele, enquanto o desenho em relevo da flor de lótus proporciona uma experiência visualmente encantadora e calmante.",
            aromaProfile: "Fresco, Atalcado, Delicado"
        },
        es: {
            name: "Loto & Arcilla Blanca",
            desc: "Fórmula de arcilla blanca ultra suave con patrón floral de loto.",
            longDesc: "Ideal para pieles apagadas o cansadas. La arcilla blanca purifica suavemente las capas de la piel, mientras que el relieve de la flor de loto proporciona una experiencia visualmente encantadora y calmante.",
            aromaProfile: "Fresco, Atalcado, Delicado"
        },
        en: {
            name: "Lotus & White Clay Soap",
            desc: "Ultra-gentle white clay formula with lotus floral pattern.",
            longDesc: "Ideal for dull or tired skins. White clay gently purifies the skin layers, while the embossed design of the lotus flower provides a visually enchanting and soothing experience.",
            aromaProfile: "Fresh, Powdery, Delicate"
        },
        fr: {
            name: "Lotus & Argile Blanche",
            desc: "Formule d'argile blanche ultra-douce avec motif floral de lotus.",
            longDesc: "Idéal pour les peaux ternes ou fatiguées. L'argile blanche purifie en douceur les couches de la peau, tandis que le relief de la fleur de lotus procure une expérience visuellement charmante et apaisante.",
            aromaProfile: "Frais, Poudré, Délicat"
        }
    },
    {
        id: "soap-gallery-11",
        price: 5.90,
        image: "assets/soap_gallery_11.jpg",
        pt: {
            name: "Anis Estrelado & Mel",
            desc: "Base translúcida de glicerina natural com anis estrelado autêntico.",
            longDesc: "Uma barra artesanal que brilha contra a luz, contendo anis estrelado real no seu interior. O anis tem propriedades estimulantes e o mel acrescenta uma suavidade nutritiva incomparável à espuma.",
            aromaProfile: "Quente Anisado, Doce, Aromático"
        },
        es: {
            name: "Anís Estrellado & Miel",
            desc: "Base translúcida de glicerina natural con anís estrellado auténtico.",
            longDesc: "Una barra artesanal que brilla contra la luz, conteniendo anís estrellado real en su interior. El anís tiene propiedades estimulantes y la miel añade una suavidad nutritiva incomparable a la espuma.",
            aromaProfile: "Cálido Anisado, Dulce, Aromático"
        },
        en: {
            name: "Star Anise & Honey Soap",
            desc: "Translucent natural glycerin base with authentic star anise.",
            longDesc: "A handcrafted bar that shines against the light, containing real star anise inside. Anise has stimulating properties, and honey adds an incomparable nourishing softness to the lather.",
            aromaProfile: "Warm Anise, Sweet, Aromatic"
        },
        fr: {
            name: "Anis Étoilé & Miel",
            desc: "Base translucide de glycérine naturelle avec de l'anis étoilé authentique.",
            longDesc: "Un pain de savon artisanal qui brille à la lumière, contenant de l'anis étoilé véritable. L'anis possède des propriétés stimulantes, et le miel apporte une douceur nutritive incomparable à la mousse.",
            aromaProfile: "Anisé Chaud, Doux, Aromatique"
        }
    },
    {
        id: "soap-gallery-12",
        price: 5.90,
        image: "assets/soap_gallery_12.jpg",
        pt: {
            name: "Flor de Calêndula & Camomila",
            desc: "Design de girassol em relevo dourado sobre glicerina calmante.",
            longDesc: "Desenhado com um deslumbrante girassol em relevo no centro. Combina as propriedades calmantes da calêndula e da camomila com uma base hidratante de glicerina para um banho suave e aromático.",
            aromaProfile: "Fresco, Herbal, Adocicado"
        },
        es: {
            name: "Flor de Caléndula & Manzanilla",
            desc: "Diseño de girasol en relieve dorado sobre glicerina calmante.",
            longDesc: "Diseñado con un deslumbrante girasol en relieve en el centro. Combina las propiedades calmantes de la caléndula y la manzanilla con una base hidratante de glicerina para un baño suave y aromático.",
            aromaProfile: "Fresco, Herbal, Dulce"
        },
        en: {
            name: "Calendula & Chamomile Flower Soap",
            desc: "Golden embossed sunflower design on soothing glycerin base.",
            longDesc: "Designed with a stunning embossed sunflower in the center. Combines the soothing properties of calendula and chamomile with a moisturizing glycerin base for a gentle and aromatic bath.",
            aromaProfile: "Fresh, Herbal, Sweet"
        },
        fr: {
            name: "Fleur de Souci & Camomille",
            desc: "Design de tournesol en relief doré sur base de glycérine apaisante.",
            longDesc: "Dessiné avec un superbe tournesol en relief au centre. Combine les propriétés apaisantes du souci et de la camomille avec une base hydratante de glycérine pour un bain doux et aromatique.",
            aromaProfile: "Frais, Herbal, Doux"
        }
    },
    {
        id: "soap-gallery-13",
        price: 5.90,
        image: "assets/soap_gallery_13.jpg",
        pt: {
            name: "Carvão Ativado & Borboleta",
            desc: "Design de borboleta em relevo sobre sabonete purificante de carvão vegetal.",
            longDesc: "Um trabalho de arte em sabão. O relevo de borboleta de alta definição destaca-se sobre uma barra de carvão vegetal ativado, combinando purificação facial profunda e beleza ornamental superior.",
            aromaProfile: "Purificante, Fresco, Amadeirado"
        },
        es: {
            name: "Carbón Activado & Mariposa",
            desc: "Diseño de mariposa en relieve sobre jabón purificante de carbón vegetal.",
            longDesc: "Una obra de arte en jabón. El relieve de mariposa en alta definición destaca sobre una barra de carbón vegetal activado, combinando una purificación facial profunda y una belleza ornamental superior.",
            aromaProfile: "Purificante, Fresco, Amaderado"
        },
        en: {
            name: "Activated Charcoal & Butterfly Soap",
            desc: "Embossed butterfly design on purifying charcoal soap base.",
            longDesc: "A work of art in soap. The high-definition butterfly relief stands out on a bar of active charcoal, combining deep facial purification with superior ornamental beauty.",
            aromaProfile: "Purifying, Fresh, Woody"
        },
        fr: {
            name: "Charbon Actif & Papillon",
            desc: "Design de papillon en relief sur base de savon purifiant au charbon.",
            longDesc: "Une œuvre d'art en savon. Le relief de papillon en haute definição se détache sur un pain de charbon végétal actif, combinant une purification faciale profonde et une beauté ornementale supérieure.",
            aromaProfile: "Purifiant, Frais, Boisé"
        }
    }
];

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
