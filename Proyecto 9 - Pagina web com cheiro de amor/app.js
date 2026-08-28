/* ==========================================================================
   PRODUCT DATABASE (Artisanal Scented Candles, Bath Soaps, & Gift Sets)
   ========================================================================== */
const PRODUCTS = [
    {
        id: "candle-cactus-1",
        category: "vela",
        price: 10.90,
        image: "assets/vela_suculentas.jpg",
        qty: 1,
        pt: {
            name: "Vela Cactus & Suculentas",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Jardim de cactos e suculentas em travessa oval artesanal.",
            description: "Espetacular vela aromática em travessa oval de cerâmica branca, decorada com um jardim artesanal de cactos e suculentas esculpidos em cera vegetal em tons de verde e bege. Com múltiplos pavios para uma queima uniforme e um aroma fresco e herbal.",
            aromaProfile: "Chá Verde, Aloé Vera, Ervas Frescas, Revigorante"
        },
        es: {
            name: "Vela Cactus & Suculentas",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Jardín de cactus y suculentas en bandeja ovalada artesanal.",
            description: "Espectacular vela aromática en bandeja ovalada de cerámica blanca, decorada con un jardín artesanal de cactus y suculentas esculpidos en cera vegetal en tonos verde y beige. Con múltiples mechas para una combustión uniforme y un aroma fresco y herbal.",
            aromaProfile: "Té Verde, Aloe Vera, Hierbas Frescas, Revigorante"
        },
        en: {
            name: "Cactus & Succulents Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Garden of wax cacti and succulents in an oval handcrafted dish.",
            description: "Stunning scented candle set in an oval white ceramic dish, featuring a handcrafted garden of detailed wax cacti and succulents in green and beige tones. Includes multiple wicks for an even burn and a refreshing herbal scent.",
            aromaProfile: "Green Tea, Aloe Vera, Fresh Herbs, Invigorating"
        },
        fr: {
            name: "Bougie Cactus & Succulentes",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Jardin de cactus et succulentes en cire dans un plateau ovale.",
            description: "Superbe bougie parfumée présentée dans un plateau ovale en céramique blanche, ornée d'un jardin artisanal de cactus et succulentes sculptés en cire. Dotée de plusieurs mèches pour une combustion uniforme et un parfum frais.",
            aromaProfile: "Thé Vert, Aloe Vera, Herbes Fraîches, Vivifiant"
        }
    },
    {
        id: "buque-menina-1",
        category: "buque",
        price: 14.90,
        image: "assets/buque_menina.jpg",
        qty: 1,
        pt: {
            name: "Menina Buquê",
            categoryLabel: "Buquê",
            aromaBrief: "Arranjo floral de cera em vaso de estatueta de menina com flores secas.",
            description: "Encantador e poético arranjo 'Menina Buquê', combinando uma delicada estatueta de menina serena em vaso branco com uma coroa de flores esculpidas em cera (tulipa fúchsia, rosas brancas e turquesa) acompanhadas de botânicos e flores secas naturais. Uma peça de arte floral aromática inesquecível.",
            aromaProfile: "Tulipa, Peónia, Flores Secas, Poético e Elegante"
        },
        es: {
            name: "Menina Buquê",
            categoryLabel: "Buquê",
            aromaBrief: "Arreglo floral de cera en vasija estatuilla de niña con flores secas.",
            description: "Encantador y poético arreglo 'Menina Buquê', combinando una delicada estatuilla de niña serena en vasija blanca con una corona de flores esculpidas en cera (tulipán fucsia, rosas blancas y turquesa) acompañadas de botánicos y flores secas naturales. Una pieza de arte floral aromática inolvidable.",
            aromaProfile: "Tulipán, Peonía, Flores Secas, Poético y Elegante"
        },
        en: {
            name: "Menina Bouquet",
            categoryLabel: "Bouquet",
            aromaBrief: "Floral wax arrangement in a serene girl bust vase with dried flowers.",
            description: "Charming and poetic 'Menina Bouquet' combining a serene white girl bust vase with a crown of handcrafted wax flowers (fuchsia tulip, white and turquoise roses) arranged with real dried botanicals. An unforgettable piece of aromatic floral art.",
            aromaProfile: "Tulip, Peony, Dried Flowers, Poetic & Elegant"
        },
        fr: {
            name: "Bouquet Menina",
            categoryLabel: "Bouquet",
            aromaBrief: "Composition florale en cire dans un vase buste de jeune fille.",
            description: "Ravissant et poétique bouquet 'Menina' associant un vase buste de jeune fille blanche sérénité à une couronne de fleurs en cire (tulipe fuchsia, roses blanches et turquoise) et fleurs séchées naturelles.",
            aromaProfile: "Tulipe, Pivoine, Fleurs Séchées, Poétique et Élégant"
        }
    },
    {


        id: "candle-laco-1",
        category: "vela",
        price: 10.90,
        image: "assets/vela_laco.jpg",
        qty: 1,
        pt: {
            name: "Vela Laço",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela em vaso transparente de vidro com laço tridimensional esculpido.",
            description: "Encantadora vela aromática em recipiente transparente de vidro, apresentando no centro um delicado laço tridimensional em tom rosa veludo. Feita à mão com cera vegetal para proporcionar elegância e um perfume envolvente.",
            aromaProfile: "Algodão Doce, Baunilha, Floral, Delicado"
        },
        es: {
            name: "Vela Laço (Lazo)",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela en vaso transparente de cristal con lazo tridimensional esculpido.",
            description: "Encantadora vela aromática en recipiente transparente de cristal, con un delicado lazo tridimensional esculpido en tono rosa terciopelo. Hecha a mano con cera vegetal para aportar elegancia y un perfume envolvente.",
            aromaProfile: "Algodón de Azúcar, Vainilla, Floral, Delicado"
        },
        en: {
            name: "Ribbon Bow Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Scented candle in a clear glass jar featuring a 3D sculpted ribbon bow.",
            description: "Charming scented candle in a clear glass jar featuring a handcrafted 3D sculpted ribbon bow in soft velvet pink. Made with natural wax to bring elegance and fragrance to any room.",
            aromaProfile: "Cotton Candy, Vanilla, Soft Floral, Delicate"
        },
        fr: {
            name: "Bougie Ruban",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie en verre transparent avec nœud en ruban sculpté en 3D.",
            description: "Charmante bougie parfumée dans un contenant en verre transparent, ornée d'un élégant nœud en ruban sculpté en 3D dans les tons rose velours. Fabriquée à la main pour une touche raffinée.",
            aromaProfile: "Barbe à Papa, Vanille, Floral, Délicat"
        }
    },
    {
        id: "candle-leveza_set-1",
        category: "vela",
        price: 9.90,
        image: "assets/vela_conchas_pastel.jpg",
        qty: 1,
        pt: {
            name: "Conjunto Leveza - Conchas do Mar",
            categoryLabel: "Conjunto de Velas",
            aromaBrief: "Conjunto de 2 velas aromáticas em formato de concha em tons pastel.",
            description: "Encantador conjunto 'Leveza' composto por duas velas aromáticas moldadas em formato de conchas marinhas em tons pastel (rosa delicado e azul mar). Traz a brisa suave e a tranquilidade do oceano para a sua casa. (Conjunto por 9,90€, grande individual por 4,90€, pequena individual por 3,90€).",
            aromaProfile: "Brisa Marinha, Sal de Maço, Flor de Lótus, Suave"
        },
        es: {
            name: "Conjunto Leveza - Conchas de Mar",
            categoryLabel: "Conjunto de Velas",
            aromaBrief: "Conjunto de 2 velas aromáticas en forma de concha en tonos pastel.",
            description: "Encantador conjunto 'Leveza' compuesto por dos velas aromáticas moldeadas en forma de conchas marinas en tonos pastel (rosa delicado y azul mar). Aporta la brisa suave y la tranquilidad del océano a tu hogar. (Conjunto por 9,90€, grande individual por 4,90€, pequeña individual por 3,90€).",
            aromaProfile: "Brisa Marina, Flor de Loto, Fresco, Suave"
        },
        en: {
            name: "Leveza Sea Shell Candle Set",
            categoryLabel: "Candle Set",
            aromaBrief: "Set of 2 pastel sea shell scented candles.",
            description: "Charming 'Leveza' set featuring two handcrafted sea shell scented candles in soft pastel shades (delicate pink and ocean blue). Brings the serene ocean breeze into your home. (Set for €9.90, large individual for €4.90, small individual for €3.90).",
            aromaProfile: "Ocean Breeze, Lotus Flower, Fresh, Gentle"
        },
        fr: {
            name: "Ensemble Leveza - Coquillages",
            categoryLabel: "Ensemble de Bougies",
            aromaBrief: "Ensemble de 2 bougies coquillages en teintes pastel.",
            description: "Charmant ensemble 'Leveza' composé de deux bougies parfumées en forme de coquillages aux couleurs pastel (rose délicat et bleu mer). (Ensemble à 9,90€, grande seule à 4,90€, petite seule à 3,90€).",
            aromaProfile: "Brise Marine, Fleur de Lotus, Frais, Doux"
        }
    },
    {
        id: "candle-cao_gato_set-1",
        category: "vela",
        price: 9.90,
        image: "assets/vela_cao_gato.jpg",
        qty: 1,
        pt: {
            name: "Conjunto Velas Cão & Gato",
            categoryLabel: "Conjunto de Velas",
            aromaBrief: "Conjunto de 2 velas decorativas aromáticas em formato de cão e gato.",
            description: "Encantador conjunto de duas velas aromáticas artesanais esculpidas em formato de cão e gato. Feitas à mão com cera vegetal e aromas suaves, perfeitas para homenagear os animais de estimação e trazer doçura ao lar. (Disponível em conjunto por 9,90€ ou individualmente por 4,90€ cada).",
            aromaProfile: "Baunilha, Caramelo, Doce, Aconchegante"
        },
        es: {
            name: "Conjunto Velas Perro & Gato",
            categoryLabel: "Conjunto de Velas",
            aromaBrief: "Conjunto de 2 velas decorativas aromáticas en forma de perro y gato.",
            description: "Encantador conjunto de dos velas aromáticas artesanales esculpidas en forma de perro y gato. Hechas a mano con cera vegetal y aromas suaves, perfectas para homenajear a las mascotas y aportar ternura al hogar. (Disponible en conjunto por 9,90€ o individualmente por 4,90€ cada una).",
            aromaProfile: "Vainilla, Caramelo, Dulce, Acogedor"
        },
        en: {
            name: "Dog & Cat Candle Set",
            categoryLabel: "Candle Set",
            aromaBrief: "Set of 2 decorative scented candles shaped as a dog and a cat.",
            description: "Charming set of two handcrafted scented candles sculpted in the shape of a dog and a cat. Made from natural soy wax with sweet soothing aromas, ideal for pet lovers. (Available as a set for €9.90 or individually for €4.90 each).",
            aromaProfile: "Vanilla, Caramel, Sweet, Cozy"
        },
        fr: {
            name: "Ensemble Bougies Chien & Chat",
            categoryLabel: "Ensemble de Bougies",
            aromaBrief: "Ensemble de 2 bougies parfumées décoratives en forme de chien et chat.",
            description: "Charmant ensemble de deux bougies parfumées artisanales sculptées en forme de chien et de chat. Fabriquées à la main avec de la cire naturelle et des senteurs douces. (Disponible en ensemble à 9,90€ ou individuellement à 4,90€ chacune).",
            aromaProfile: "Vanille, Caramel, Doux, Chaleureux"
        }
    },
    {
        id: "candle-camera_preta-1",
        category: "vela",
        price: 6.90,
        image: "assets/vela_camera_preta.jpg",
        qty: 1,
        pt: {
            name: "Vela Máquina Fotográfica Preta",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa em formato de câmara fotográfica vintage preta.",
            description: "Elegante e moderna vela aromática moldada em formato de máquina fotográfica vintage em tom preto fosco. Feita à mão com cera vegetal e fragrâncias marcantes de amadeirado e especiarias, ideal para amantes de arte e fotografia.",
            aromaProfile: "Amadeirado, Café, Especiarias, Moderno"
        },
        es: {
            name: "Vela Cámara Fotográfica Negra",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa en forma de cámara fotográfica vintage negra.",
            description: "Elegante y moderna vela aromática moldeada en forma de cámara fotográfica vintage en tono negro mate. Hecha a mano con cera vegetal y notas amaderadas y especiadas, ideal para amantes del arte y la fotografía.",
            aromaProfile: "Amaderado, Café, Especias, Moderno"
        },
        en: {
            name: "Black Camera Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative vintage camera candle in matte black.",
            description: "Sleek and modern scented candle sculpted into a vintage camera shape in matte black. Handcrafted with plant-based wax and rich woody spice fragrances, perfect for art and photography enthusiasts.",
            aromaProfile: "Woody, Coffee, Spice, Modern"
        },
        fr: {
            name: "Bougie Appareil Photo Noir",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative en forme d'appareil photo vintage noir.",
            description: "Élégante bougie parfumée en forme d'appareil photo vintage en noir mat. Fabriquée à la main avec de la cire naturelle et des notes boisées et épicées, idéale pour les amateurs d'art et de photographie.",
            aromaProfile: "Boisé, Café, Épices, Moderne"
        }
    },
    {
        id: "candle-camera_lilas-1",
        category: "vela",
        price: 6.90,
        image: "assets/vela_camera_lilas.jpg",
        qty: 1,
        pt: {
            name: "Vela Máquina Fotográfica Lilás",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa em formato de câmara fotográfica vintage lilás.",
            description: "Encantadora vela aromática moldada em formato de máquina fotográfica vintage em tom lilás suave. Feita à mão com cera vegetal e fragrâncias delicadas de lavanda, perfeita para os amantes de fotografia e decoração criativa.",
            aromaProfile: "Lavanda, Alfazema, Floral Suave, Criativo"
        },
        es: {
            name: "Vela Cámara Fotográfica Lila",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa en forma de cámara fotográfica vintage lila.",
            description: "Encantadora vela aromática moldeada en forma de cámara fotográfica vintage en tono lila suave. Hecha a mano con cera vegetal y delicadas fragancias de lavanda, perfecta para los amantes de la fotografía y la decoración creativa.",
            aromaProfile: "Lavanda, Alucema, Floral Suave, Creativo"
        },
        en: {
            name: "Lilac Camera Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative vintage camera candle in soft lilac.",
            description: "Charming scented candle sculpted into a vintage camera shape in soft lilac. Handcrafted with natural wax and gentle lavender fragrances, perfect for photography lovers and creative home decor.",
            aromaProfile: "Lavender, Soft Floral, Relaxing, Creative"
        },
        fr: {
            name: "Bougie Appareil Photo Lilas",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative en forme d'appareil photo vintage lilas.",
            description: "Charmante bougie parfumée en forme d'appareil photo vintage en lilas doux. Fabriquée à la main avec de la cire naturelle et des senteurs délicates de lavande, idéale pour les passionnés de photographie.",
            aromaProfile: "Lavande, Floral Doux, Relaxant, Créatif"
        }
    },
    {
        id: "candle-coffee_cream-1",
        category: "vela",
        price: 10.90,
        image: "assets/vela_coffee_cream.jpg",
        qty: 1,
        pt: {
            name: "Vela Coffee Cream",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática de café em vaso artesanal com pavio de madeira.",
            description: "Irresistível vela aromática artesanal em recipiente circular de cerâmica marmorizada, decorada com grãos de café reais e pavio de madeira crepitante. O aroma rico de café torrado e creme traz aconchego imediato a qualquer espaço.",
            aromaProfile: "Café Torrado, Creme de Baunilha, Caramelo, Envolvente"
        },
        es: {
            name: "Vela Coffee Cream",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática de café en vasija artesanal con mecha de madera.",
            description: "Irresistible vela aromática artesanal en recipiente circular de cerámica marmolada, decorada con granos de café reales y mecha de madera crepitante. El rico aroma a café tostado y crema aporta calidez inmediata a cualquier espacio.",
            aromaProfile: "Café Tostado, Crema de Vainilla, Caramelo, Envolvente"
        },
        en: {
            name: "Coffee Cream Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Coffee scented candle in a handcrafted bowl with wooden wick.",
            description: "Irresistible handcrafted scented candle in a marbled ceramic bowl, topped with genuine coffee beans and a crackling wooden wick. The rich aroma of roasted coffee and cream fills your room with cozy warmth.",
            aromaProfile: "Roasted Coffee, Vanilla Cream, Caramel, Cozy"
        },
        fr: {
            name: "Bougie Coffee Cream",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie parfumée au café dans un bol artisanal avec mèche en bois.",
            description: "Irésistible bougie parfumée artisanale dans un bol en céramique marbrée, décorée de véritables grains de café et d'une mèche en bois crépitante. L'arôme riche de café torréfié et de crème apporte une chaleur enveloppante.",
            aromaProfile: "Café Torréfié, Crème Vanille, Caramel, Enveloppant"
        }
    },
    {
        id: "candle-ophelia-1",
        category: "vela",
        price: 12.90,
        image: "assets/vela_ophelia.jpg",
        qty: 1,
        pt: {
            name: "Vela Ophelia",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela em vaso de vidro com rosas esculpidas em relevo.",
            description: "Elegante vela aromática em recipiente redondo de vidro, decorada com delicadas rosas de cera esculpidas em tons de rosa e bordô. Feita à mão com cera vegetal para perfumar e trazer um toque romântico e sofisticado ao seu espaço.",
            aromaProfile: "Rosa Silvestre, Peónia, Floral, Romântico"
        },
        es: {
            name: "Vela Ophelia",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela en recipiente de cristal con rosas esculpidas en relieve.",
            description: "Elegante vela aromática en recipiente redondo de cristal, decorada con delicadas rosas de cera esculpidas en tonos rosa y burdeos. Hecha a mano con cera vegetal para perfumar y aportar un toque romántico y sofisticado a tu hogar.",
            aromaProfile: "Rosa Silvestre, Peonía, Floral, Romántico"
        },
        en: {
            name: "Ophelia Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Scented candle in a glass bowl with sculpted wax roses.",
            description: "Elegant scented candle presented in a clear glass bowl, featuring handcrafted wax roses in soft pink and deep burgundy tones. Made with natural wax to infuse your space with romance and fragrance.",
            aromaProfile: "Wild Rose, Peony, Floral, Romantic"
        },
        fr: {
            name: "Bougie Ophelia",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie parfumée en bol de verre avec roses sculptées.",
            description: "Élégante bougie parfumée dans un bol en verre transparent, ornée de délicates roses en cire faites à la main dans des teintes roses et bordeaux. Fabriquée avec de la cire naturelle pour une touche romantique et raffinée.",
            aromaProfile: "Rose Sauvage, Pivoine, Floral, Romantique"
        }
    },
    {
        id: "candle-abobora-1",
        category: "vela",
        price: 12.90,
        image: "assets/vela_abobora.jpg",
        qty: 1,
        pt: {
            name: "Vela Abóbora",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa em vaso de cerâmica de abóbora.",
            description: "Vela aromática artesanal em recipiente de cerâmica em formato de abóbora, feita à mão com cera vegetal e essências selecionadas para decorar e perfumar o seu lar com um toque acolhedor.",
            aromaProfile: "Canela, Especiarias, Acolhedor, Outono"
        },
        es: {
            name: "Vela Abóbora",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa en vasija de cerámica de calabaza.",
            description: "Vela aromática artesanal en recipiente de cerámica con forma de calabaza, hecha a mano con cera vegetal y esencias seleccionadas para decorar y perfumar tu hogar con un toque acogedor.",
            aromaProfile: "Canela, Especias, Acogedor, Otoño"
        },
        en: {
            name: "Pumpkin Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle in a pumpkin ceramic jar.",
            description: "Handcrafted scented candle in a pumpkin-shaped ceramic jar, made with plant-based wax and premium fragrances to bring warmth and style to your space.",
            aromaProfile: "Cinnamon, Spice, Cozy, Autumn"
        },
        fr: {
            name: "Bougie Citrouille",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie parfumée en pot céramique citrouille.",
            description: "Bougie parfumée artisanale dans un contenant en céramique en forme de citrouille, faite à la main pour une ambiance chaleureuse e raffinée.",
            aromaProfile: "Cannelle, Épices, Chaleureux, Automne"
        }
    },
        {
        id: "candle-benedita-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_benedita_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Benedita",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática com rosa e detalhe marmorizado.",
            description: "Vela decorativa aromática com rosa e detalhe marmorizado, feita à mão com cera de soja natural e essências selecionadas para decorar e perfumar o seu lar.",
            aromaProfile: "Rosa, Marmorizado, Floral, Elegante"
        },
        es: {
            name: "Vela Benedita",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática con rosa y detalle marmolado.",
            description: "Vela decorativa aromática con rosa y detalle marmolado, hecha a mano con cera de soja natural y esencias seleccionadas para decorar y perfumar tu hogar.",
            aromaProfile: "Rosa, Marmolado, Floral, Elegante"
        },
        en: {
            name: "Benedita Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle with rose and marbled detail.",
            description: "Decorative scented candle with rose and marbled detail, handcrafted from natural soy wax and selected fragrances to decorate and scent your home.",
            aromaProfile: "Rose, Marbled, Floral, Elegant"
        },
        fr: {
            name: "Bougie Benedita",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée à la rose et détail marbré.",
            description: "Bougie décorative parfumée à la rose et détail marbré, fabriquée à la main avec de la cire de soja naturelle et des essences sélectionnées pour décorer et parfumer votre maison.",
            aromaProfile: "Rose, Marbré, Floral, Élégant"
        }
    },
        {
        id: "candle-big_bear-1",
        category: "vela",
        price: 12.90,
        image: "assets/candle_big_bear_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Urso Gigante",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática de urso, tamanho grande.",
            description: "Vela decorativa aromática de urso em tamanho grande, feita à mão com cera de soja e aromas suaves para trazer calor e doçura ao ambiente.",
            aromaProfile: "Achegado, Baunilha, Caramelo, Doce"
        },
        es: {
            name: "Vela Oso Gigante",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática de oso, tamaño grande.",
            description: "Vela decorativa aromática de oso en tamaño grande, hecha a mano con cera de soja y aromas suaves para aportar calidez y dulzura a tu hogar.",
            aromaProfile: "Acogedor, Vainilla, Caramelo, Dulce"
        },
        en: {
            name: "Big Bear Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented bear candle, large size.",
            description: "Decorative scented bear candle in a large size, handcrafted from soy wax with soft fragrances to bring warmth and sweetness to your space.",
            aromaProfile: "Cozy, Vanilla, Caramel, Sweet"
        },
        fr: {
            name: "Bougie Gros Ourson",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée ourson, grand format.",
            description: "Bougie décorative parfumée en forme d'ourson grand format, fabriquée à la main avec de la cire de soja et des senteurs douces pour apporter de la chaleur à votre intérieur.",
            aromaProfile: "Chaleureux, Vanille, Caramel, Doux"
        }
    },
        {
        id: "candle-big_heart-1",
        category: "vela",
        price: 14.90,
        image: "assets/candle_big_heart_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Big Heart",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática em recipiente de gesso com detalhes.",
            description: "Vela decorativa aromática em recipiente de gesso com detalhes elegantes, feita à mão com cera de soja natural e essência romântica para perfumar e transformar o seu espaço.",
            aromaProfile: "Romântico, Frutas Vermelhas, Amor"
        },
        es: {
            name: "Vela Big Heart",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática en recipiente de yeso con detalles.",
            description: "Vela decorativa aromática en recipiente de yeso con detalles elegantes, hecha a mano con cera de soja natural y esencia romántica para perfumar y transformar tu hogar.",
            aromaProfile: "Romántico, Frutos Rojos, Amor"
        },
        en: {
            name: "Big Heart Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle in a plaster vessel with details.",
            description: "Decorative scented candle in an elegant plaster vessel with fine details, handcrafted from natural soy wax and romantic fragrance to scent and transform your space.",
            aromaProfile: "Romantic, Red Berries, Love"
        },
        fr: {
            name: "Bougie Big Heart",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée dans un récipient en plâtre avec détails.",
            description: "Bougie décorative parfumée dans un récipient en plâtre aux détails élégants, fabriquée à la main avec de la cire de soja naturelle et un parfum romantique pour illuminer votre intérieur.",
            aromaProfile: "Romantique, Fruits Rouges, Amour"
        }
    },
        {
        id: "candle-conjunto_budas-1",
        category: "vela",
        price: 9.90,
        image: "assets/candle_conjunto_budas_1.jpeg",
        qty: 1,
        pt: {
            name: "Conjunto de Budas",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Conjunto de velas de 4 budas: não fale, não ouça, não veja o mal, oração contínua.",
            description: "Conjunto de velas de 4 budas (não fale, não ouça, não veja o mal, oração contínua) feitas em cera de soja natural com fragrância relaxante de sândalo para trazer harmonia e paz ao lar.",
            aromaProfile: "Sândalo, Relaxamento, Meditação"
        },
        es: {
            name: "Conjunto de Budas",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Conjunto de velas de 4 budas: no hables, no oigas, no veas el mal, oración continua.",
            description: "Conjunto de velas de 4 budas (no hables, no oigas, no veas el mal, oración continua) hechas en cera de soja natural con aroma relajante a sándalo para aportar armonía y paz al hogar.",
            aromaProfile: "Sándalo, Relajación, Meditación"
        },
        en: {
            name: "Buddhas Candle Set",
            categoryLabel: "Scented Candle",
            aromaBrief: "Set of 4 buddha candles: speak no evil, hear no evil, see no evil, continuous prayer.",
            description: "Set of 4 buddha candles (speak no evil, hear no evil, see no evil, continuous prayer) crafted from natural soy wax with a relaxing sandalwood fragrance.",
            aromaProfile: "Sandalwood, Relaxation, Meditation"
        },
        fr: {
            name: "Coffret de Bouddhas",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Ensemble de 4 bougies bouddhas : ne rien dire, ne rien entendre, ne rien voir, prière continue.",
            description: "Ensemble de 4 bougies bouddhas (ne rien dire, ne rien entendre, ne rien voir de mal, prière continue) en cire de soja naturelle avec un parfum relaxant de bois de santal.",
            aromaProfile: "Bois de Santal, Relaxation, Méditation"
        }
    },
        {
        id: "candle-coracoes-1",
        category: "vela",
        price: 4.90,
        image: "assets/candle_coracoes_1.jpeg",
        qty: 1,
        pt: {
            name: "Corações de Amor",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela em formato de coração ideal para momentos românticos e especiais.",
            description: "Vela em formato de coração ideal para jantares românticos, decoração de mesas ou lembranças de casamento personalizadas. Aroma suave e envolvente. Ideal para ambientalizar.",
            aromaProfile: "Suave, Envolvente, Romântico"
        },
        es: {
            name: "Corazones de Amor",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela en forma de corazón ideal para momentos románticos y especiales.",
            description: "Vela en forma de corazón ideal para cenas románticas, decoración de mesas o recuerdos de boda personalizados. Aroma suave y envolvente. Ideal para crear ambiente.",
            aromaProfile: "Suave, Envolvente, Romántico"
        },
        en: {
            name: "Love Hearts Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Heart-shaped candle ideal for romantic and special moments.",
            description: "Heart-shaped candle ideal for romantic dinners, table decorations, or personalized wedding favors. Soft and enveloping scent. Ideal for setting the mood.",
            aromaProfile: "Soft, Enveloping, Romantic"
        },
        fr: {
            name: "Cœurs d'Amour",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie en forme de cœur idéale pour les moments romantiques et spéciaux.",
            description: "Bougie en forme de cœur idéale pour les dîners romantiques, la décoration de table ou les cadeaux de mariage personnalisés. Parfum doux et enveloppant. Idéale pour créer une ambiance.",
            aromaProfile: "Doux, Enveloppant, Romantique"
        }
    },
        {
        id: "candle-flora-1",
        category: "vela",
        price: 10.90,
        image: "assets/candle_flora_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flora",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática com aroma leve e suave em recipiente de gesso cerâmico alfa.",
            description: "Vela decorativa aromática com um aroma leve e suave. Recipiente feito em gesso cerâmico alfa, uma peça simples e elegante que traz o frescor cítrico da flor de laranjeira para o seu ambiente.",
            aromaProfile: "Flor de Laranjeira, Cítrico, Fresco"
        },
        es: {
            name: "Vela Flora",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática con aroma ligero y suave en recipiente de yeso cerámico alfa.",
            description: "Vela decorativa aromática con un aroma ligero y suave. Recipiente hecho en yeso cerámico alfa, una pieza simple y elegante que aporta el frescor cítrico de la flor de azahar a tu hogar.",
            aromaProfile: "Flor de Azahar, Cítrico, Fresco"
        },
        en: {
            name: "Flora Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle with a light and soft aroma in an alpha ceramic plaster vessel.",
            description: "Decorative scented candle with a light and soft aroma. Crafted in an alpha ceramic plaster vessel, a simple and elegant piece that brings the citrus freshness of orange blossom to your space.",
            aromaProfile: "Orange Blossom, Citrus, Fresh"
        },
        fr: {
            name: "Bougie Flora",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée au parfum léger et doux dans un récipient en plâtre céramique alpha.",
            description: "Bougie décorative parfumée au parfum léger et doux. Récipient fabriqué en plâtre céramique alpha, une pièce simple et élégante qui apporte la fraîcheur hespéridée de la fleur d'oranger dans votre intérieur.",
            aromaProfile: "Fleur d'Oranger, Agrume, Frais"
        }
    },
        {
        id: "candle-flora-2",
        category: "vela",
        price: 11.90,
        image: "assets/candle_flora_2.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flora Peónia Azul",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática com pérolas e tom azul céu em recipiente de gesso cerâmico alfa.",
            description: "Vela decorativa aromática com um aroma leve e suave. Recipiente feito em gesso cerâmico alfa, uma peça simples e elegante com pérolas que dão detalhe e um tom azul céu incrível.",
            aromaProfile: "Jasmim, Lírio, Pérolas, Primavera"
        },
        es: {
            name: "Vela Flora Peonía Azul",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática con perlas y tono azul cielo en recipiente de yeso cerámico alfa.",
            description: "Vela decorativa aromática con un aroma ligero y suave. Recipiente hecho en yeso cerámico alfa, una pieza simple y elegante con perlas que aportan detalle y un tono azul cielo increíble.",
            aromaProfile: "Jazmín, Lirio, Perlas, Primavera"
        },
        en: {
            name: "Blue Peony Flora Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle with pearls and sky blue tone in an alpha ceramic plaster vessel.",
            description: "Decorative scented candle with a light and soft aroma. Crafted in an alpha ceramic plaster vessel, a simple and elegant piece adorned with pearls for detail and an incredible sky blue tone.",
            aromaProfile: "Jasmine, Lily, Pearls, Springtime"
        },
        fr: {
            name: "Bougie Flora Pivoine Bleue",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée aux perles et ton bleu ciel dans un récipient en plâtre céramique alpha.",
            description: "Bougie décorative parfumée au parfum léger et doux. Récipient fabriqué en plâtre céramique alpha, une pièce simple et élégante ornée de perles et d'une incroyable nuance bleu ciel.",
            aromaProfile: "Jasmin, Lys, Perles, Printemps"
        }
    },
        {
        id: "candle-flora-3",
        category: "vela",
        price: 8.90,
        image: "assets/candle_flora_3.jpeg",
        qty: 1,
        pt: {
            name: "Vela Aromática Elegance",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática em recipiente de vidro refinado.",
            description: "Vela decorativa aromática com um aroma leve e suave em recipiente de vidro que oferece luxo e elegância para uma maior e melhor experiência olfativa.",
            aromaProfile: "Sofisticado, Vidro Refinado, Elegante"
        },
        es: {
            name: "Vela Aromática Elegance",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática en recipiente de vidrio refinado.",
            description: "Vela decorativa aromática con un aroma ligero y suave en recipiente de vidrio que ofrece lujo y elegancia para una mayor y mejor experiencia olfativa.",
            aromaProfile: "Sofisticado, Vidrio Refinado, Elegante"
        },
        en: {
            name: "Elegance Scented Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle in a refined glass container.",
            description: "Decorative scented candle with a light and soft aroma in a glass container that offers luxury and elegance for a greater and better olfactory experience.",
            aromaProfile: "Sophisticated, Refined Glass, Elegant"
        },
        fr: {
            name: "Bougie Parfumée Elegance",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée dans un récipient en verre raffiné.",
            description: "Bougie décorative parfumée au parfum léger et doux dans un récipient en verre qui offre luxe et élégance pour une expérience olfactive inégalée.",
            aromaProfile: "Sophistiqué, Verre Raffiné, Élégant"
        }
    },
        {
        id: "candle-flowers-1",
        category: "vela",
        price: 4.90,
        image: "assets/candle_flowers_1.jpeg",
        qty: 1,
        pt: {
            name: "Shining Flowers",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática em recipiente de vidro com glitters brilhantes.",
            description: "Vela decorativa aromática com um aroma leve e suave em recipiente de vidro e com glitters para dar um brilho especial ao seu ambiente.",
            aromaProfile: "Flores, Brilho, Suave, Encantador"
        },
        es: {
            name: "Shining Flowers",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa aromática en recipiente de vidrio con purpurina brillante.",
            description: "Vela decorativa aromática con un aroma ligero y suave en recipiente de vidrio y con purpurina para aportar un brillo especial a tu hogar.",
            aromaProfile: "Flores, Brillo, Suave, Encantador"
        },
        en: {
            name: "Shining Flowers",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative scented candle in a glass container with sparkling glitters.",
            description: "Decorative scented candle with a light and soft aroma in a glass container featuring glitters to bring a special shine to your space.",
            aromaProfile: "Flowers, Sparkle, Soft, Enchanting"
        },
        fr: {
            name: "Shining Flowers",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative parfumée dans un récipient en verre avec paillettes brillantes.",
            description: "Bougie décorative parfumée au parfum léger et doux dans un récipient en verre agrémenté de paillettes pour apporter une brillance spéciale à votre intérieur.",
            aromaProfile: "Fleurs, Paillettes, Doux, Enchanteur"
        }
    },
        {
        id: "candle-luna-1",
        category: "vela",
        price: 5.90,
        image: "assets/candle_luna_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Luna",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática com pétalas de rosa para um aroma intenso e único.",
            description: "Vela aromática com pétalas de rosa que dá um aroma intenso e único ao ambiente do seu lar.",
            aromaProfile: "Rosa, Intenso, Único, Místico"
        },
        es: {
            name: "Vela Luna",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática con pétalos de rosa para un aroma intenso y único.",
            description: "Vela aromática con pétalos de rosa que aporta un aroma intenso y único al ambiente de tu hogar.",
            aromaProfile: "Rosa, Intenso, Único, Místico"
        },
        en: {
            name: "Luna Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Scented candle with rose petals for an intense and unique aroma.",
            description: "Scented candle with rose petals that brings an intense and unique aroma to your home environment.",
            aromaProfile: "Rose, Intense, Unique, Mystical"
        },
        fr: {
            name: "Bougie Luna",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie parfumée aux pétales de rose pour un parfum intense et unique.",
            description: "Bougie parfumée aux pétales de rose qui apporte un parfum intense et unique à votre intérieur.",
            aromaProfile: "Rose, Intense, Unique, Mystique"
        }
    },
        {
        id: "candle-margarida-1",
        category: "vela",
        price: 6.90,
        image: "assets/candle_margarida_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Margarida",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa com aroma de camomila e flor de laranjeira.",
            description: "Vela decorativa com aroma de camomila e flor de laranjeira, que dá um aroma único e especial ao seu lar.",
            aromaProfile: "Camomila, Flor de Laranjeira, Único, Especial"
        },
        es: {
            name: "Vela Margarita",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela decorativa con aroma de manzanilla y flor de azahar.",
            description: "Vela decorativa con aroma de manzanilla y flor de azahar, que aporta un aroma único y especial a tu hogar.",
            aromaProfile: "Manzanilla, Flor de Azahar, Único, Especial"
        },
        en: {
            name: "Daisy Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Decorative candle with chamomile and orange blossom fragrance.",
            description: "Decorative candle with chamomile and orange blossom fragrance, bringing a unique and special aroma to your home.",
            aromaProfile: "Chamomile, Orange Blossom, Unique, Special"
        },
        fr: {
            name: "Bougie Marguerite",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie décorative au parfum de camomille et fleur d'oranger.",
            description: "Bougie décorative au parfum de camomille et fleur d'oranger, apportant une senteur unique et spéciale à votre intérieur.",
            aromaProfile: "Camomille, Fleur d'Oranger, Unique, Spécial"
        }
    },
        {
        id: "candle-mira-1",
        category: "vela",
        price: 13.90,
        image: "assets/candle_mira_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Melody",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela em vaso com notas musicais delicadas em cera e aroma harmonioso.",
            description: "Encantadora vela aromática em vaso cerâmico decorada com notas musicais em cera rosa. Uma composição harmoniosa que traz serenidade, elegância e um perfume envolvente para a sua casa.",
            aromaProfile: "Harmonia, Notas Musicais, Doce, Sereno"
        },
        es: {
            name: "Vela Melody",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela en vaso con notas musicales delicadas en cera y aroma armonioso.",
            description: "Encantadora vela aromática en vaso cerámico decorada con notas musicales de cera rosa. Una composición armoniosa que aporta serenidad, elegancia y un perfume envolvente a tu hogar.",
            aromaProfile: "Armonía, Notas Musicales, Dulce, Sereno"
        },
        en: {
            name: "Melody Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Scented candle in a ceramic jar decorated with delicate wax musical notes.",
            description: "Charming scented candle in a ceramic container decorated with pink wax musical notes. A harmonious composition that brings serenity, elegance, and an enfolding fragrance to your home.",
            aromaProfile: "Harmony, Musical Notes, Sweet, Serene"
        },
        fr: {
            name: "Bougie Melody",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie parfumée dans un pot en céramique orné de notes de musique en cire.",
            description: "Charmante bougie parfumée dans un récipient en céramique orné de notes de musique en cire rose. Une composition harmonieuse qui apporte sérénité, élégance et un parfum envoûtant chez vous.",
            aromaProfile: "Harmonie, Notes de Musique, Doux, Sérénité"
        }
    },
        {
        id: "candle-olho_grego-1",
        category: "vela",
        price: 8.90,
        image: "assets/candle_olho_grego_1.jpeg",
        qty: 1,
        pt: {
            name: "Olho Grego de Proteção",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela inspirada na proteção e observação para afastar as más energias.",
            description: "Uma vela inspirada na proteção e observação. O olho grego é conhecido pela proteção contra invejas e mau olhado, com a filosofia de que afasta as más energias do seu ambiente.",
            aromaProfile: "Proteção, Purificação, Místico, Sal Marinho"
        },
        es: {
            name: "Ojo Turco de Protección",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela inspirada en la protección y observación para alejar las malas energías.",
            description: "Una vela inspirada en la protección y observación. El ojo turco es conocido por la protección contra envidias y mal de ojo, con la filosofía de alejar las malas energías de tu hogar.",
            aromaProfile: "Protección, Purificación, Místico, Sal Marina"
        },
        en: {
            name: "Protection Evil Eye Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Candle inspired by protection and observation to ward off negative energies.",
            description: "A candle inspired by protection and observation. The evil eye is known for protection against envy and the evil eye, with the philosophy of warding off negative energies from your space.",
            aromaProfile: "Protection, Purification, Mystical, Sea Salt"
        },
        fr: {
            name: "Bougie Œil Grec de Protection",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Bougie inspirée de la protection et de l'observation pour éloigner les mauvaises énergies.",
            description: "Une bougie inspirée de la protection et de l'observation. L'œil grec est connu pour protéger contre la jalousie et le mauvais œil, avec pour philosophie d'éloigner les mauvaises énergies de votre intérieur.",
            aromaProfile: "Protection, Purification, Mystique, Sel Marin"
        }
    },
        {
        id: "candle-peonia-1",
        category: "vela",
        price: 14.90,
        image: "assets/candle_peonia_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Flor Peónia Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática peónia grande de 19 cm para marcar presença no seu lar.",
            description: "Vela aromática peónia grande. Elegância e aroma combinados numa só vela para marcar presença no seu lar, com um diâmetro de 19 cm que fará ressaltar esta incrível peça única.",
            aromaProfile: "Peónia, Elegância, Luxuoso, Único"
        },
        es: {
            name: "Vela Flor Peonía Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática peonía grande de 19 cm para marcar presencia en tu hogar.",
            description: "Vela aromática peonía grande. Elegancia y aroma combinados en una sola vela para marcar presencia en tu hogar, con un diámetro de 19 cm que hará resaltar esta increíble pieza única.",
            aromaProfile: "Peonía, Elegancia, Lujoso, Único"
        },
        en: {
            name: "Premium Peony Flower Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Large 19 cm peony scented candle to make a bold statement in your home.",
            description: "Large peony scented candle. Elegance and aroma combined in a single candle to make a statement in your home, with a 19 cm diameter that will highlight this incredible unique piece.",
            aromaProfile: "Peony, Elegance, Luxurious, Unique"
        },
        fr: {
            name: "Bougie Fleur de Pivoine Premium",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Grande bougie parfumée pivoine de 19 cm pour faire sensation dans votre intérieur.",
            description: "Grande bougie parfumée pivoine. Élégance et parfum combinés dans une seule bougie pour marquer les esprits dans votre intérieur, avec un diamètre de 19 cm qui fera ressortir cette incroyable pièce unique.",
            aromaProfile: "Pivoine, Élégance, Luxueux, Unique"
        }
    },
        {
        id: "candle-rosa_bella-1",
        category: "vela",
        price: 6.90,
        image: "assets/candle_rosa_bella_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Rosa Bella",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela pensada para um ambiente de elegância, harmonia e tranquilidade.",
            description: "Uma vela pensada para um ambiente de elegância e tranquilidade. Com a Rosa Bella terá uma sensação de harmonia e tranquilidade.",
            aromaProfile: "Rosa Bella, Elegância, Harmonia, Tranquilidade"
        },
        es: {
            name: "Vela Rosa Bella",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela pensada para un ambiente de elegancia, armonía y tranquilidad.",
            description: "Una vela pensada para un ambiente de elegancia y tranquilidad. Con la Rosa Bella tendrás una sensación de armonía y tranquilidad.",
            aromaProfile: "Rosa Bella, Elegancia, Armonía, Tranquilidad"
        },
        en: {
            name: "Rosa Bella Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "A candle designed for an atmosphere of elegance, harmony, and tranquility.",
            description: "A candle designed for an environment of elegance and tranquility. With the Rosa Bella you will experience a sense of harmony and peace.",
            aromaProfile: "Rosa Bella, Elegance, Harmony, Tranquility"
        },
        fr: {
            name: "Bougie Rosa Bella",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Une bougie conçue pour une atmosphère d'élégance, d'harmonie et de sérénité.",
            description: "Une bougie conçue pour un environnement d'élégance et de tranquillité. Avec la Rosa Bella, vous ressentirez une sensation d'harmonie et de sérénité.",
            aromaProfile: "Rosa Bella, Élégance, Harmonie, Sérénité"
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
            name: "Vela Shinny Light",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela geométrica facetada com fragrância refrescante cítrica de hortelã.",
            description: "Vela em formato geométrico facetado de estrela ou gema que reflete a luz de forma linda e preenche a divisão com notas frescas de limão e hortelã.",
            aromaProfile: "Limão, Hortelã, Cítrico Fresco"
        },
        es: {
            name: "Vela Shinny Light",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela geométrica facetada con fragancia refrescante cítrica de menta.",
            description: "Vela con formato geométrico facetado de estrella o gema que refleja la luz de forma hermosa y llena la estancia con notas frescas de limón y menta.",
            aromaProfile: "Limón, Menta, Cítrico Fresco"
        },
        en: {
            name: "Shinny Light Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Geometric faceted star candle with a refreshing citrus mint scent.",
            description: "Geometric faceted star or gem-shaped candle that beautifully reflects light and fills the room with fresh notes of lemon and mint.",
            aromaProfile: "Lemon, Mint, Fresh Citrus"
        },
        fr: {
            name: "Bougie Shinny Light",
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
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Lavanda, Calmante, Floral"
        },
        es: {
            name: "Vela en Vaso Lavanda & Flores",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Lavanda, Calmante, Floral"
        },
        en: {
            name: "Lavender & Flowers Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Lavender, Soothing, Floral"
        },
        fr: {
            name: "Bougie en Pot Lavande & Fleurs",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
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
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Cítrico, Alecrim, Quente"
        },
        es: {
            name: "Vela en Vaso Naranja & Romero",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Cítrico, Romero, Cálido"
        },
        en: {
            name: "Orange & Rosemary Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Citrus, Rosemary, Warm"
        },
        fr: {
            name: "Bougie en Pot Orange & Romarin",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
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
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Baunilha, Coco, Amadeirado"
        },
        es: {
            name: "Vela en Vaso Ámbar Tradicional",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Vainilla, Coco, Amaderado"
        },
        en: {
            name: "Traditional Amber Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Vanilla, Coconut, Woody"
        },
        fr: {
            name: "Bougie en Pot Ambre Traditionnel",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
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
            name: "Vela Tília em Vaso",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Canela, Cravinho, Aconchegante"
        },
        es: {
            name: "Vela Tília en Vaso",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Canela, Clavo, Acogedor"
        },
        en: {
            name: "Tília Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Cinnamon, Clove, Cozy"
        },
        fr: {
            name: "Bougie en Pot Tília",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
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
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Algodão, Fresco, Limpo, Suave"
        },
        es: {
            name: "Vela en Vaso Flor de Algodón",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Algodón, Fresco, Limpio, Suave"
        },
        en: {
            name: "Cotton Flower Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Cotton, Fresh, Clean, Soft"
        },
        fr: {
            name: "Bougie en Pot Fleur de Coton",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.",
            description: "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.",
            aromaProfile: "Coton, Frais, Propre, Doux"
        }
    },
    {
        id: "candle-general-1",
        category: "vela",
        price: 6.90,
        image: "assets/candle_general_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Aromática Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Copo de cera natural jateado com pavio de algodão e baunilha suave.",
            description: "Vela aromática clássica em copo de vidro jateado, com cera de soja 100% pura e fragrância acolhedora de baunilha doce que acalma e conforta o ambiente.",
            aromaProfile: "Baunilha Doce, Suave, Acolhedor"
        },
        es: {
            name: "Vela Aromática Premium",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Vaso de cera natural esmerilado con mecha de algodón y vainilla suave.",
            description: "Vela aromática clásica en vaso de vidrio esmerilado, con cera de soja 100% pura y fragancia acogedora de vainilla dulce que calma y reconforta el hogar.",
            aromaProfile: "Vainilla Dulce, Suave, Acogedor"
        },
        en: {
            name: "Premium Scented Candle",
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
        id: "candle-new-2",
        category: "vela",
        price: 11.90,
        image: "assets/new_prod_2.jpeg",
        qty: 1,
        pt: {
            name: "Vela Aromática Jardim Botânico",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Infusão fresca e floral de alfazema e jasmim para o seu lar.",
            description: "Vela decorativa em recipiente natural infundida com notas frescas e florais de alfazema e jasmim, perfeita para trazer a serenidade da natureza ao seu lar.",
            aromaProfile: "Alfazema, Jasmim, Fresco, Botânico"
        },
        es: {
            name: "Vela Aromática Jardín Botánico",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Infusión fresca y floral de lavanda y jazmín para tu hogar.",
            description: "Vela decorativa en recipiente natural infundida con notas frescas y florales de lavanda y jazmín, perfecta para aportar la serenidad de la naturaleza a tu hogar.",
            aromaProfile: "Lavanda, Jazmín, Fresco, Botánico"
        },
        en: {
            name: "Botanical Garden Scented Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Fresh and floral infusion of lavender and jasmine for your home.",
            description: "Decorative candle in a natural container infused with fresh, floral notes of lavender and jasmine, perfect for bringing nature's serenity into your home.",
            aromaProfile: "Lavender, Jasmine, Fresh, Botanical"
        },
        fr: {
            name: "Bougie Parfumée Jardin Botanique",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Infusion fraîche et florale de lavande et jasmin pour votre intérieur.",
            description: "Bougie décorative dans un récipient naturel infusée de notes fraîches et florales de lavande et jasmin, parfaite pour apporter la sérénité de la nature chez vous.",
            aromaProfile: "Lavande, Jasmin, Frais, Botanique"
        }
    },
    {
        id: "candle-new-3",
        category: "vela",
        price: 14.90,
        image: "assets/new_prod_3.jpeg",
        qty: 1,
        pt: {
            name: "Buquê Aquarium",
            categoryLabel: "Buquê",
            aromaBrief: "Encantador arranjo floral em tons azul e branco moldado em cera de soja natural.",
            description: "Encantador arranjo floral artesanal em tons azul e branco moldado em cera de soja natural. Apresentado em vaso cerâmico com laço decorativo, combina rosas e flores esculpidas com um aroma fresco e relaxante.",
            aromaProfile: "Cera de Soja 100% Natural, Azul & Branco, Fresco, Relaxante"
        },
        es: {
            name: "Ramo Aquarium",
            categoryLabel: "Buqué",
            aromaBrief: "Encantador arreglo floral en tonos azul y blanco moldeado en cera de soja natural.",
            description: "Encantador arreglo floral artesanal en tonos azul y blanco moldeado en cera de soja natural. Presentado en maceta cerámica con lazo decorativo, combina rosas y flores esculpidas con un aroma fresco y relajante.",
            aromaProfile: "Cera de Soja 100% Natural, Azul & Blanco, Fresco, Relajante"
        },
        en: {
            name: "Aquarium Candle Bouquet",
            categoryLabel: "Bouquet",
            aromaBrief: "Charming blue and white floral arrangement handcrafted from natural soy wax.",
            description: "Charming handcrafted floral arrangement in sea blue and white tones molded from 100% natural soy wax. Presented in a ceramic pot with a decorative bow, featuring sculpted roses and fresh, relaxing floral notes.",
            aromaProfile: "100% Natural Soy Wax, Blue & White, Fresh, Relaxing"
        },
        fr: {
            name: "Bouquet Aquarium",
            categoryLabel: "Bouquet",
            aromaBrief: "Ravissant arrangement floral bleu et blanc moulé en cire de soja naturelle.",
            description: "Ravissant arrangement floral artisanal aux teintes bleu mer et blanc moulé en cire de soja 100% naturelle. Présenté dans un pot en céramique avec un ruban décoratif, associant roses sculptées et parfum frais et relaxant.",
            aromaProfile: "Cire de Soja 100% Naturelle, Bleu & Blanc, Frais, Relaxant"
        }
    },
    {
        id: "candle-new-4",
        category: "vela",
        price: 24.90,
        image: "assets/new_prod_4.jpeg",
        qty: 1,
        pt: {
            name: "Vela Mia",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Luxuosa vela artesanal em recipiente canelado tom rosa com grande flor esculpida e pavio triplo.",
            description: "Luxuosa e imponente vela decorativa artesanal moldada em cera de soja pura num elegante recipiente canelado tom rosa poeira. Apresenta uma majestosa peónia esculpida no centro com pavio triplo, exalando um aroma envolvente e sofisticado.",
            aromaProfile: "Peónia, Baunilha, Sofisticado, Pavio Triplo"
        },
        es: {
            name: "Vela Mia",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Lujosa vela artesanal en cuenco acanalado tono rosa con gran flor esculpida y triple mecha.",
            description: "Lujosa e imponente vela decorativa artesanal moldeada en cera de soja pura en un elegante cuenco acanalado tono rosa empolvado. Presenta una majestuosa peonía esculpida en el centro con triple mecha, exhalando un aroma envolvente y sofisticado.",
            aromaProfile: "Peonía, Vainilla, Sofisticado, Triple Mecha"
        },
        en: {
            name: "Mia Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Luxurious handcrafted candle in a dusty pink ribbed bowl with a large sculpted bloom & 3 wicks.",
            description: "Luxurious, statement candle handcrafted from pure soy wax in an elegant dusty pink ribbed vessel. Features a majestic center-sculpted peony bloom with triple wicks, filling your space with a rich, comforting floral scent.",
            aromaProfile: "Peony, Vanilla, Sophisticated, Triple Wick"
        },
        fr: {
            name: "Bougie Mia",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Luxueuse bougie artisanale dans une coupe cannelée rose poudré avec grande fleur sculptée et 3 meches.",
            description: "Luxueuse bougie décorative faite main en cire de soja pure dans une élégante coupe cannelée rose poudré. Arbore une majestueuse pivoine sculptée au centre avec triple mèche, diffusant un parfum floral enveloppant et raffiné.",
            aromaProfile: "Pivoine, Vanille, Sophistiqué, Triple Mèche"
        }
    },
    {
        id: "candle-new-5",
        category: "vela",
        price: 10.90,
        image: "assets/new_prod_5.jpeg",
        qty: 1,
        pt: {
            name: "Vela Margarida",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Delicada vela decorativa num recipiente circular branco com margaridas amarelas e rosa pastel em cera de soja.",
            description: "Encantadora vela artesanal moldada em cera de soja pura num elegante recipiente circular branco. Decorada no topo com delicadas margaridas esculpidas em tons amarelo radiante e rosa pastel com pavios de madeira, enchendo o ambiente de luz, frescura e alegria floral.",
            aromaProfile: "Margarida, Floral Fresco, Pavio de Madeira, Primavera"
        },
        es: {
            name: "Vela Margarida",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Delicada vela decorativa en cuenco circular blanco con margaritas amarillas y rosa pastel en cera de soja.",
            description: "Encantadora vela artesanal moldeada en cera de soja pura en un elegante recipiente circular blanco. Decorada en la superficie con delicadas margaritas esculpidas en tonos amarillo radiante y rosa pastel con mechas de madera, llenando el ambiente de luz, frescura y alegría floral.",
            aromaProfile: "Margarita, Floral Fresco, Mecha de Madera, Primavera"
        },
        en: {
            name: "Daisy Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Delicate decorative candle in a smooth white bowl topped with yellow and soft pink soy daisies with wooden wicks.",
            description: "Charming handcrafted soy wax candle set in a smooth white circular vessel. Beautifully topped with sculpted daisy flowers in vibrant yellow and pastel pink hues featuring wooden wicks, infusing your room with fresh, joyful floral radiance.",
            aromaProfile: "Daisy, Fresh Floral, Wooden Wick, Spring"
        },
        fr: {
            name: "Bougie Marguerite",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Délicate bougie décorative dans une coupe blanche avec marguerites sculptées jaune et rose pastel.",
            description: "Ravissante bougie artisanale en cire de soja pure coulée dans une coupe circulaire blanche. Ornée en surface de délicates marguerites sculptées aux teintes jaune lumineux et rose pastel avec mèches en bois, apportant fraîcheur et joie florale à votre intérieur.",
            aromaProfile: "Marguerite, Floral Frais, Mèche en Bois, Printemps"
        }
    },
    {
        id: "candle-new-6",
        category: "set",
        price: 21.90,
        image: "assets/new_prod_6.jpeg",
        qty: 1,
        pt: {
            name: "Buquê na Mala",
            categoryLabel: "Buquê",
            aromaBrief: "Sofisticado arranjo floral de velas artesanais apresentado numa elegante mala decorativa com corrente dourada.",
            description: "Sofisticado e original arranjo floral artesanal feito com velas em cera de soja pura em tons rosa, roxo e branco. Apresentado numa requintada caixa em formato de mala com asa de corrente dourada, é uma peça de presente inesquecível e ultra charmosa.",
            aromaProfile: "Cera de Soja 100% Natural, Floral Exclusivo, Presente de Luxo"
        },
        es: {
            name: "Ramo en Bolsito",
            categoryLabel: "Buqué",
            aromaBrief: "Sofisticado arreglo floral de velas artesanales presentado en un elegante bolso decorativo con cadena dorada.",
            description: "Sofisticado y original arreglo floral artesanal elaborado con velas en cera de soja pura en tonos rosa, morado y blanco. Presentado en una exquisita caja en formato de bolsito con asa de cadena dorada, es una pieza de regalo inolvidable y llena de encanto.",
            aromaProfile: "Cera de Soja 100% Natural, Floral Exclusivo, Regalo de Lujo"
        },
        en: {
            name: "Handbag Bouquet",
            categoryLabel: "Bouquet",
            aromaBrief: "Sophisticated handcrafted candle floral arrangement presented in an elegant gift handbag box with gold chain.",
            description: "Sophisticated and original handcrafted floral arrangement featuring realistic soy wax flower candles in pink, purple, and white tones. Presented in an exquisite handbag gift box with a delicate gold chain handle, perfect for a chic and memorable gift.",
            aromaProfile: "100% Natural Soy Wax, Exclusive Floral, Luxury Gift"
        },
        fr: {
            name: "Bouquet Sac à Main",
            categoryLabel: "Bouquet",
            aromaBrief: "Arrangement floral artisanal de bougies présenté dans une élégante boîte sac à main avec chaîne dorée.",
            description: "Sophistiqué et original arrangement floral fait main composé de bougies en cire de soja aux teintes rose, violet et blanc. Présenté dans une élégante boîte sac à main avec anse en chaîne dorée, c'est un cadeau d'exception chic et inoubliable.",
            aromaProfile: "Cire de Soja 100% Naturelle, Floral Exclusif, Cadeau de Luxe"
        }
    },
    {
        id: "candle-new-7",
        category: "vela",
        price: 13.90,
        image: "assets/new_prod_7.jpeg",
        qty: 1,
        pt: {
            name: "Vela Havana",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Peça artesanal exclusiva com acabamento orgânico e essências botânicos.",
            description: "Peça artesanal exclusiva com acabamento orgânico em tons neutros, infundida com essências botânicas para harmonizar qualquer divisão do seu lar.",
            aromaProfile: "Orgânico, Botânico, Harmonioso, Neutro"
        },
        es: {
            name: "Vela Havana",
            categoryLabel: "Vela Aromática",
            aromaBrief: "Pieza artesanal exclusiva con acabado orgánico y esencias botánicos.",
            description: "Pieza artesanal exclusiva con acabado orgánico en tonos neutros, infundida con esencias botánicas para armonizar cualquier estancia de tu hogar.",
            aromaProfile: "Orgánico, Botánico, Armonioso, Neutro"
        },
        en: {
            name: "Havana Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "Exclusive handcrafted piece with organic finish and botanical oils.",
            description: "Exclusive handcrafted piece with an organic finish in neutral tones, infused with botanical fragrance essences to harmonize any room in your home.",
            aromaProfile: "Organic, Botanical, Harmonious, Neutral"
        },
        fr: {
            name: "Bougie Havana",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "Pièce artisanale exclusive à la finition biologique et essences botaniques.",
            description: "Pièce artisanale exclusive à la finition biologique aux tons neutres, infusée d'essences botaniques pour harmoniser n'importe quelle pièce de votre maison.",
            aromaProfile: "Biologique, Botanique, Harmonieux, Neutre"
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

const DECORATIVE_OVERRIDES = {
    1: {
        price: 5.90,
        pt: {
            name: "Placa de Reconhecimento",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Placa decorativa de agradecimento em madeira com arranjo de flores secas e aplique dourado.",
            description: "Elegante placa decorativa de homenagem em formato de arco com bordo recortado. Apresenta uma linda mensagem de agradecimento ('Querida Educadora, Obrigada por me ajudares a crescer!'), decorada com um mini bouquet de flores secas em tom rosa vivo e aplique metálico dourado. Um presente inesquecível e emocionante para educadoras e professoras.",
            aromaProfile: "Reconhecimento, Educadora, Flores Secas, Madeira"
        },
        es: {
            name: "Placa de Reconocimiento",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Placa decorativa de agradecimiento en madera con arreglo de flores secas y aplique dorado.",
            description: "Elegante placa decorativa de homenaje en formato de arco con borde festoneado. Presenta una hermosa dedicatoria de agradecimiento ('Querida Educadora, ¡Gracias por ayudarme a crecer!'), decorada con un mini ramo de flores secas en tono rosa vivo y aplique metálico dorado. Un regalo inolvidable y emocionante para educadoras y profesoras.",
            aromaProfile: "Reconocimiento, Educadora, Flores Secas, Madera"
        },
        en: {
            name: "Recognition Plaque",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Decorative wooden thank-you plaque featuring a dried flower bouquet and gold metallic charm.",
            description: "Elegant arched wooden recognition plaque with scalloped edges. Features a heartfelt thank-you dedication, decorated with a vibrant pink dried flower mini bouquet and a gold metal watering can charm. An unforgettable, emotional gift for teachers and educators.",
            aromaProfile: "Recognition, Teacher Gift, Dried Flowers, Wooden"
        },
        fr: {
            name: "Plaque de Reconnaissance",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plaque décorative de remerciement en bois ornée de fleurs séchées et d'un appliqué doré.",
            description: "Élégante plaque décorative en forme d'arche aux bords festonnés. Arbore un tendre message de remerciement ('Chère Éducatrice, Merci de m'avoir aidé à grandir !'), ornée d'un mini bouquet de fleurs séchées rose vif et d'un appliqué métallique doré. Un cadeau inoubliable pour les enseignantes et éducatrices.",
            aromaProfile: "Reconnaissance, Éducatrice, Fleurs Séchées, Bois"
        }
    },
    2: {
        price: 11.90,
        pt: {
            name: "Conjunto Multiusos",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Conjunto decorativo artesanal em Jesmonite marmoreado azul com bandeja oval, porta-objetos e jarra com secas.",
            description: "Elegante conjunto decorativo artesanal moldado em Jesmonite premium com requintado efeito marmoreado em tons azul celeste e branco. Inclui uma bandeja oval canelada, um recipiente circular multiusos e uma graciosa jarra com hastes de flores secas e plumagem natural. Ideal para organizar joias, pincéis ou decorar lavabos e toucadores com máxima sofisticação.",
            aromaProfile: "Jesmonite, Marmoreado Azul, Conjunto Multiusos, Flores Secas"
        },
        es: {
            name: "Conjunto Multiusos",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Conjunto decorativo artesanal de Jesmonite marmolado azul con bandeja ovalada, contenedor y florero con secas.",
            description: "Elegante conjunto decorativo artesanal moldeado en Jesmonite premium con un exquisito efecto marmolado en tonos azul celeste y blanco. Incluye una bandeja ovalada acanalada, un contenedor circular multiusos y un bonito jarrón con espigas de flores secas y plumaje natural. Ideal para organizar joyas, pinceles o decorar tocadores y baños con máxima sofisticación.",
            aromaProfile: "Jesmonite, Marmolado Azul, Conjunto Multiusos, Flores Secas"
        },
        en: {
            name: "Multipurpose Set",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted blue marbled Jesmonite decorative set featuring an oval tray, container, and vase with dried flora.",
            description: "Elegant handcrafted decorative set molded from premium Jesmonite featuring a gorgeous sky blue and white marbled design. Includes a ribbed oval tray, a circular multipurpose trinket holder, and a charming vase with natural dried fluffy flora. Perfect for organizing jewelry, brushes, or styling vanities and bathrooms with refined elegance.",
            aromaProfile: "Jesmonite, Blue Marbled, Multipurpose Set, Dried Flora"
        },
        fr: {
            name: "Ensemble Multi-usages",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Ensemble décoratif artisanal en Jesmonite marbré bleu comprenant un plateau ovale, un pot et un vase à fleurs séchées.",
            description: "Élégant ensemble décoratif fait main moulé en Jesmonite premium au délicat motif marbré bleu céleste et blanc. Comprend un plateau ovale cannelé, un contenant circulaire multi-usages et un ravissant vase garni d'herbes et fleurs séchées naturelles. Idéal pour organiser bijoux, pinceaux ou sublimer une coiffeuse avec chic.",
            aromaProfile: "Jesmonite, Marbré Bleu, Ensemble Multi-usages, Fleurs Séchées"
        }
    },
    3: {
        price: 9.90,
        pt: {
            name: "Suporte Magnético Decorativo",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Suporte artesanal em bambu com íman, mola com coração e colher de pau personalizada.",
            description: "Encantadora peça decorativa artesanal em bambu natural com íman posterior para fixar no frigorífico ou superfícies metálicas. Apresenta o aplique em madeira 'Mãe', uma miniatura de colher de pau e uma mola com coração vermelho perfeita para prender notas, receitas carinhosas ou fotografias na cozinha.",
            aromaProfile: "Bambu Natural, Magnético, Personalizado, Mãe"
        },
        es: {
            name: "Soporte Magnético Decorativo",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Soporte artesanal de bambú con imán, pinza con corazón y cuchara de madera personalizada.",
            description: "Encantadora pieza decorativa artesanal de bambú natural con imán posterior para fijar en el frigorífico o superficies metálicas. Presenta la palabra tallada 'Mãe/Mamá', una miniatura de cuchara de madera y una pinza con corazón rojo perfecta para sujetar notas, recetas entrañables o fotografías en la cocina.",
            aromaProfile: "Bambú Natural, Magnético, Personalizado, Mamá"
        },
        en: {
            name: "Decorative Magnetic Holder",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted bamboo magnetic holder featuring wooden spoon, heart peg, and 'Mãe' inscription.",
            description: "Charming handcrafted natural bamboo decorative holder with a back magnet for fridge attachment. Features a wooden 'Mãe' cut-out, a decorative mini wooden spoon, and a red heart clothespin ideal for holding notes, sweet recipes, or photos in the kitchen.",
            aromaProfile: "Natural Bamboo, Magnetic, Personalized, Mother's Day"
        },
        fr: {
            name: "Support Magnétique Décoratif",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Support artisanal en bambou avec aimant, pince cœur et cuillère en bois personnalisée.",
            description: "Ravissante pièce décorative artisanale en bambou naturel avec aimant au dos pour réfrigérateur. Décorée d'un mot en bois 'Mãe', d'une cuillère miniature en bois et d'une pince à cœur rouge idéale pour accrocher mots doux, recettes ou photos dans la cuisine.",
            aromaProfile: "Bambou Naturel, Magnétique, Personnalisé, Maman"
        }
    },
    4: {
        price: 9.90,
        pt: {
            name: "Placa de Reconhecimento",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Placa decorativa de homenagem em madeira com borboletas metálicas e vaso busto com coroa dourada.",
            description: "Encantadora placa decorativa de agradecimento em formato de arco com a mensagem ('Querida Professora, Obrigada por me ajudares a crescer com alegria e a ganhar asas para voar mais alto'). Acompanha borboletas decorativas refletivas e um vaso de busto em gesso ecológico com coroa de flores dourada. Um presente inesquecível e profundamente emocionante para professoras.",
            aromaProfile: "Reconhecimento, Professora, Borboletas Douradas, Homenagem"
        },
        es: {
            name: "Placa de Reconocimiento",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Placa decorativa de homenaje en madera con mariposas metálicas y jarrón busto con corona dorada.",
            description: "Encantadora placa decorativa de agradecimiento en formato de arco con la dedicatoria ('Querida Professora, ¡Gracias por ayudarme a crecer con alegría y a ganar alas para volar más alto!'). Acompañada por mariposas decorativas reflectantes y un jarrón de busto en yeso ecológico con corona de flores dorada. Un regalo inolvidable y profundamente emocionante para profesoras.",
            aromaProfile: "Reconocimiento, Profesora, Mariposas Doradas, Homenaje"
        },
        en: {
            name: "Recognition Plaque",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Decorative wooden thank-you plaque with metallic butterflies and small bust vase with golden crown.",
            description: "Charming arched wooden recognition plaque featuring an inspirational thank-you quote for teachers. Decorated with metallic gold reflective butterflies and paired on the base with a white bust vase crowned in gold flowers. An unforgettable, heartfelt tribute gift for educators.",
            aromaProfile: "Recognition, Teacher Gift, Golden Butterflies, Tribute"
        },
        fr: {
            name: "Plaque de Reconnaissance",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plaque décorative de remerciement en bois avec papillons métalliques et vase buste à couronne dorée.",
            description: "Charmante plaque décorative de remerciement en forme d'arche avec un émouvant message d'hommage pour les enseignantes. Ornée de papillons dorés réfléchissants et accompagnée d'un petit vase buste en plâtre écologique couronné de fleurs dorées. Un cadeau inoubliable et plein de tendresse.",
            aromaProfile: "Reconnaissance, Enseignante, Papillons Dorés, Hommage"
        }
    },
    5: {
        price: 4.90,
        pt: {
            name: "Caixa Porta-Alianças",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Caixa artesanal em madeira para alianças com aplique de argolas entrelaçadas e renda.",
            description: "Encantadora caixa porta-alianças artesanal em madeira com fecho vintage em latão. Decorada na tampa com argolas de casamento entrelaçadas em relevo e uma elegante faixa de juta com renda branca. Ideal para cerimónias de casamento, noivados ou guardar anéis e joias com enorme valor sentimental.",
            aromaProfile: "Casamento, Porta-Alianças, Madeira, Elegante"
        },
        es: {
            name: "Caja Porta-Alianzas",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Cajita artesanal de madera para alianzas con aplique de anillos entrelazados y encaje.",
            description: "Encantadora cajita porta-alianzas artesanal en madera con cierre vintage de latón. Decorada en la tapa con alianzas de boda entrelazadas en relieve y una elegante cinta de yute con encaje blanco. Ideal para ceremonias de boda, compromisos o guardar anillos y joyas con gran valor sentimental.",
            aromaProfile: "Boda, Porta-Alianzas, Madera, Elegante"
        },
        en: {
            name: "Wooden Ring Box",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted wooden wedding ring box featuring interlocking rings emblem, burlap & lace trim.",
            description: "Charming handcrafted wooden wedding ring box with a vintage brass latch. Beautifully styled on the lid with relief 3D interlocking wedding bands and accented with burlap and white lace trim. Perfect for wedding ceremonies, proposals, or keeping precious rings safe with sentimental elegance.",
            aromaProfile: "Wedding, Ring Box, Wooden, Elegant"
        },
        fr: {
            name: "Boîte Porte-Alliances",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Boîte artisanale en bois pour alliances ornée d'anneaux entrelacés et dentelle blanche.",
            description: "Ravissante boîte porte-alliances artisanale en bois avec fermoir vintage en laiton. Décorée sur le couvercle d'anneaux de mariage entrelacés en relief et d'un élégant ruban de jute avec dentelle blanche. Idéale pour les cérémonies de mariage, fiançailles ou pour conserver précieusement vos bagues.",
            aromaProfile: "Mariage, Porte-Alliances, Bois, Élégant"
        }
    },
    6: {
        price: 6.90,
        pt: {
            name: "Espelho Decorativo com Moldura de Contas",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Espelho decorativo artesanal redondo emoldurado por esferas de contas em relevo.",
            description: "Sofisticado espelho decorativo redondo feito artesanalmente em gesso ecológico premium, emoldurado por esferas de contas esculpidas em relevo com acabamento acetinado e impermeabilizado. Uma peça charmosa e funcional para toucadores, mesas-de-cabeceira, prateleiras ou para compor cantinhos especiais no seu lar.",
            aromaProfile: "Espelho Decorativo, Moldura de Contas, Gesso Ecológico, Elegante"
        },
        es: {
            name: "Espejo Decorativo con Marco de Cuentas",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Espejo decorativo artesanal redondo enmarcado por esferas de cuentas en relieve.",
            description: "Sofisticado espejo decorativo redondo hecho artesanalmente en yeso ecológico premium, enmarcado por esferas de cuentas esculpidas en relieve con acabado satinado e impermeabilizado. Una pieza encantadora y funcional para tocadores, mesas de noche, estanterías o crear rincones especiales en tu hogar.",
            aromaProfile: "Espejo Decorativo, Marco de Cuentas, Yeso Ecológico, Elegante"
        },
        en: {
            name: "Beaded Frame Decorative Mirror",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted round decorative mirror framed by raised spherical beaded details.",
            description: "Sophisticated round decorative mirror handcrafted from premium eco-friendly plaster, framed by sculpted spherical beaded details with a smooth satin waterproof finish. A stylish and functional mirror accent for dressers, vanity displays, nightstands, or jewelry styling.",
            aromaProfile: "Decorative Mirror, Beaded Frame, Eco Plaster, Elegant"
        },
        fr: {
            name: "Miroir Décoratif à Cadre Perlé",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Miroir décoratif artisanal rond encadré par des billes perlées en relief.",
            description: "Miroir décoratif rond sophistiqué fabriqué à la main en plâtre écologique de qualité supérieure, encadré par des billes perlées sculptées en relief avec finition satinée et imperméable. Une pièce charmante et fonctionnelle pour embellir votre coiffeuse ou table de chevet.",
            aromaProfile: "Miroir Décoratif, Cadre Perlé, Plâtre Écologique, Élégant"
        }
    },
    7: {
        price: 4.90,
        pt: {
            name: "Bandeja Decorativa Flor",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Bandeja artesanal em gesso ecológico com elegante formato de flor.",
            description: "Bandeja decorativa exclusiva em formato de flor com pétalas esculpidas em gesso ecológico premium. Com acabamento impermeável acetinado, é perfeita para organizar joias, velas ou compor a decoração do ambiente.",
            aromaProfile: "Formato Flor, Gesso Ecológico, Pintura Manual"
        },
        es: {
            name: "Bandeja Decorativa Flor",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Bandeja artesanal de yeso ecológico con elegante forma de flor.",
            description: "Bandeja decorativa exclusiva en forma de flor con pétalos esculpidos en yeso ecológico premium. Con acabado impermeable satinado, es perfecta para organizar joyas, velas o decorar tu hogar.",
            aromaProfile: "Forma de Flor, Yeso Ecológico, Pintura Manual"
        },
        en: {
            name: "Flower Decorative Tray",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted eco-friendly plaster tray with an elegant flower shape.",
            description: "Exclusive decorative tray featuring a flower silhouette with sculpted petals in premium eco-friendly plaster. Satin waterproof finish, perfect for organizing jewelry, candles, or home decor.",
            aromaProfile: "Flower Shape, Eco-friendly, Hand Painted"
        },
        fr: {
            name: "Plateau Décoratif Fleur",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plateau artisanal en plâtre écologique au forme élégante de fleur.",
            description: "Plateau décoratif exclusif en forme de fleur avec des pétales sculptés en plâtre écologique. Finition imperméable satinée, idéale pour organiser bijoux, bougies ou embellir votre intérieur.",
            aromaProfile: "Forme Fleur, Éco-responsable, Fait Main"
        }
    },
    8: {
        price: 4.90,
        pt: {
            name: "Vaso Terrazzo",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso artesanal em Jesmonite com padrão terrazzo minimalista salpicado.",
            description: "Vaso decorativo artesanal moldado em Jesmonite premium com detalhes salpicados estilo terrazzo na borda e interior. Possui acabamento impermeável acetinado, sendo ideal para organizar pequenos objetos, pincéis ou como elegante peça decorativa.",
            aromaProfile: "Vaso Decorativo, Terrazzo, Jesmonite Premium"
        },
        es: {
            name: "Vaso Terrazzo",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Cuenco decorativo artesanal de Jesmonite con patrón terrazzo minimalista salpicado.",
            description: "Vaso/cuenco decorativo artesanal moldeado en Jesmonite premium con detalles salpicados estilo terrazzo en el borde e interior. Posee acabado impermeable satinado, siendo ideal para organizar pequeños objetos, pinceles o como elegante pieza decorativa.",
            aromaProfile: "Vaso Decorativo, Terrazzo, Jesmonite Premium"
        },
        en: {
            name: "Terrazzo Pot",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted Jesmonite pot with minimalist terrazzo speckles.",
            description: "Handcrafted decorative pot molded from premium Jesmonite with terrazzo speckled details around the rim and interior. Features a satin waterproof finish, perfect for holding small trinkets, brushes, or accenting home decor.",
            aromaProfile: "Decorative Pot, Terrazzo, Premium Jesmonite"
        },
        fr: {
            name: "Pot Terrazzo",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Pot décoratif artisanal en Jesmonite au motif terrazzo minimaliste.",
            description: "Pot décoratif artisanal moulé en Jesmonite de qualité supérieure avec détails mouchetés style terrazzo sur le rebord. Finition imperméable satinée, idéal pour organiser de petits objets ou embellir votre intérieur.",
            aromaProfile: "Pot Décoratif, Terrazzo, Jesmonite Premium"
        }
    },
    9: {
        price: 4.90,
        pt: {
            name: "Bandeja Oval Terrazzo",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Bandeja oval artesanal em Jesmonite com requintado acabamento terrazzo salpicado.",
            description: "Elegante bandeja oval artesanal moldada em Jesmonite premium com padrão terrazzo salpicado em tons de verde e turquesa. Impermeabilizada com acabamento acetinado de alta resistência. Perfeita como saboneteira, porta-joias, organizador de toucador ou base para velas e perfumes.",
            aromaProfile: "Bandeja Oval, Terrazzo, Jesmonite Premium, Multiusos"
        },
        es: {
            name: "Bandeja Oval Terrazzo",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Bandeja ovalada artesanal de Jesmonite con exquisito acabado terrazzo salpicado.",
            description: "Elegante bandeja ovalada artesanal moldeada en Jesmonite premium con patrón terrazzo salpicado en tonos verde y turquesa. Impermeabilizada con un acabado satinado de alta resistencia. Perfecta como jabonera, joyero, organizador de tocador o base para velas y perfumes.",
            aromaProfile: "Bandeja Ovalada, Terrazzo, Jesmonite Premium, Multiusos"
        },
        en: {
            name: "Oval Terrazzo Tray",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted oval Jesmonite tray featuring speckled terrazzo pattern.",
            description: "Elegant handcrafted oval tray molded from premium Jesmonite featuring a vibrant green and teal terrazzo speckled design. Waterproofed with a smooth satin finish. Ideal as a soap dish, trinket tray, vanity organizer, or candle base.",
            aromaProfile: "Oval Tray, Terrazzo, Premium Jesmonite, Multipurpose"
        },
        fr: {
            name: "Plateau Oval Terrazzo",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plateau ovale artisanal en Jesmonite avec finition terrazzo mouchetée.",
            description: "Élégant plateau ovale artisanal moulé en Jesmonite premium au motif terrazzo moucheté vert et turquoise. Imperméabilisé avec une finition satinée. Parfait comme porte-savon, vide-poche, organisateur de coiffeuse ou socle pour bougies.",
            aromaProfile: "Plateau Ovale, Terrazzo, Jesmonite Premium, Multi-usages"
        }
    },
    10: {
        price: 11.90,
        pt: {
            name: "Coração em Madeira com Íman & Molas",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Suporte decorativo em madeira em forma de coração com íman para fotos e notas.",
            description: "Peça decorativa artesanal em madeira em formato de coração com suporte magnético e cordel com molas decorativas. Perfeita para pendurar fotografias, recados, listas ou lembranças com um toque amoroso e personalizado.",
            aromaProfile: "Suporte de Madeira, Magnético, Personalizado, Coração"
        },
        es: {
            name: "Corazón en Madera con Imán & Pinzas",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Soporte decorativo de madera en forma de corazón con imán para fotos y notas.",
            description: "Pieza decorativa artesanal de madera en formato de corazón con soporte magnético y cordel con pinzas decorativas. Perfecta para colgar fotografías, notas, listas o recuerdos con un toque amoroso y personalizado.",
            aromaProfile: "Soporte de Madera, Magnético, Personalizado, Corazón"
        },
        en: {
            name: "Wooden Heart Board with Magnet & Clips",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Heart-shaped wooden decorative board with magnet and clips for photos & notes.",
            description: "Handcrafted heart-shaped wooden decorative board with magnetic support and twine featuring cute heart pegs. Perfect for hanging photos, lists, notes, or memories with a loving, personalized touch.",
            aromaProfile: "Wooden Board, Magnetic, Custom, Heart"
        },
        fr: {
            name: "Cœur en Bois avec Aimant & Pinces",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Panneau décoratif en bois en forme de cœur avec aimant pour photos et notes.",
            description: "Pièce décorative artisanale en bois en forme de cœur avec support aimanté et corde à petites pinces décoratives. Parfaite pour accrocher des photos, des notes ou des souvenirs avec une touche personnalisée.",
            aromaProfile: "Panneau Bois, Aimanté, Personnalisé, Cœur"
        }
    },
    11: {
        price: 4.90,
        pt: {
            name: "Bandeja Oval",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Bandeja oval artesanal em Jesmonite com acabamento suave e elegante.",
            description: "Elegante bandeja oval artesanal moldada em Jesmonite premium com suave toque aveludado e acabamento impermeável acetinado. Perfeita para organizar joias, perfumes, sabonetes, chaves ou servir como base sofisticada para as nossas velas aromáticas.",
            aromaProfile: "Bandeja Oval, Jesmonite Premium, Suave, Multiusos"
        },
        es: {
            name: "Bandeja Ovalada",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Bandeja ovalada artesanal de Jesmonite con acabado suave y elegante.",
            description: "Elegante bandeja ovalada artesanal moldeada en Jesmonite premium con suave tacto aterciopelado y acabado impermeable satinado. Perfecta para organizar joyas, perfumes, jabones, llaves o servir como base sofisticada para nuestras velas aromáticas.",
            aromaProfile: "Bandeja Ovalada, Jesmonite Premium, Suave, Multiusos"
        },
        en: {
            name: "Oval Tray",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted oval Jesmonite tray with smooth velvet finish.",
            description: "Elegant handcrafted oval tray molded from premium Jesmonite featuring a smooth velvet feel and waterproof satin finish. Perfect for organizing jewelry, perfumes, soaps, keys, or serving as a stylish base for our scented candles.",
            aromaProfile: "Oval Tray, Premium Jesmonite, Smooth, Multipurpose"
        },
        fr: {
            name: "Plateau Ovale",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plateau ovale artisanal en Jesmonite à la finition douce et élégante.",
            description: "Élégant plateau ovale artisanal moulé en Jesmonite premium au toucher velouté et à la finition imperméable satinée. Parfait pour organiser bijoux, parfums, savons, clés ou servir de socle raffiné pour nos bougies parfumées.",
            aromaProfile: "Plateau Ovale, Jesmonite Premium, Doux, Multi-usages"
        }
    },
    12: {
        price: 19.90,
        pt: {
            name: "Conjunto Black Gold",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Conjunto artesanal multiusos em Jesmonite preto mate com luxuosos detalhes a folha de ouro.",
            description: "Sofisticado conjunto decorativo artesanal moldado em Jesmonite premium num elegante tom preto mate com pormenores em folha de ouro salpicada. Este conjunto multiusos de 3 peças inclui uma bandeja oval com rebordo de contas, um jarro canelado para flores secas e um recipiente circular flor de lótus. Perfeito para organizar joias, velas aromáticas, pincéis ou decorar lavabos e toucadores com o máximo requinte.",
            aromaProfile: "Preto Mate, Folha de Ouro, Jesmonite Premium, Multiusos"
        },
        es: {
            name: "Conjunto Black Gold",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Conjunto artesanal multiusos de Jesmonite negro mate con lujosos detalles en pan de oro.",
            description: "Sofisticado conjunto decorativo artesanal moldeado en Jesmonite premium en un elegante tono negro mate con detalles salpicados en pan de oro. Este conjunto multiusos de 3 piezas incluye una bandeja ovalada con borde de cuentas, un jarrón acanalado para flores secas y un cuenco flor de loto. Perfecto para organizar joyas, velas aromáticas, pinceles o decorar tocadores y baños con la máxima distinción.",
            aromaProfile: "Negro Mate, Pan de Oro, Jesmonite Premium, Multiusos"
        },
        en: {
            name: "Black Gold Set",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted multipurpose matte black Jesmonite set with luxurious gold leaf accents.",
            description: "Sophisticated handcrafted decorative set molded from premium Jesmonite in an elegant matte black finish with shimmering gold leaf flakes. This 3-piece multipurpose set includes a beaded rim oval tray, a ribbed dried flower vase, and a lotus trinket/candle holder. Ideal for organizing jewelry, brushes, candles, or styling vanities with supreme luxury.",
            aromaProfile: "Matte Black, Gold Leaf, Premium Jesmonite, Multipurpose"
        },
        fr: {
            name: "Ensemble Black Gold",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Ensemble artisanal multi-usages en Jesmonite noir mat avec somptueux détails à la feuille d'or.",
            description: "Somptueux ensemble décoratif artisanal moulé en Jesmonite premium au fini noir mat élégant rehaussé d'éclats de feuille d'or. Cet ensemble multi-usages de 3 pièces comprend un plateau ovale à rebord perlée, un vase cannelé pour fleurs séchées et un pot fleur de lotus. Idéal pour organiser bijoux, pinceaux, bougies ou sublimer une coiffeuse avec chic.",
            aromaProfile: "Noir Mat, Feuille d'Or, Jesmonite Premium, Multi-usages"
        }
    },
    13: {
        price: 17.90,
        pt: {
            name: "Espelho Decorativo de Mesa com Moldura Canelada",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Espelho redondo artesanal de mesa com moldura detalhada em gesso ecológico.",
            description: "Elegante espelho redondo de mesa com moldura artesanal ricamente detalhada em gesso ecológico premium. Uma peça decorativa única e luminosa, perfeita para compor a decoração de toucadores, mesas de cabeceira ou aparadores.",
            aromaProfile: "Espelho de Mesa, Design Canelado, Moldura Artesanal"
        },
        es: {
            name: "Espejo Decorativo de Mesa con Marco Acanalado",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Espejo redondo artesanal de mesa con marco detallado en yeso ecológico.",
            description: "Elegante espejo redondo de mesa con marco artesanal ricamente detallado en yeso ecológico premium. Una pieza decorativa única y luminosa, perfecta para vestir peinadoras, mesitas de noche o aparadores.",
            aromaProfile: "Espejo de Mesa, Diseño Acanalado, Marco Artesanal"
        },
        en: {
            name: "Tabletop Decorative Mirror with Ribbed Frame",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted round tabletop mirror with detailed eco-friendly plaster frame.",
            description: "Elegant round tabletop mirror with a richly detailed handcrafted eco-friendly plaster frame. A unique, luminous decorative accent piece, perfect for dressing tables, nightstands, or sideboards.",
            aromaProfile: "Tabletop Mirror, Ribbed Design, Handcrafted Frame"
        },
        fr: {
            name: "Miroir Décoratif de Table à Cadre Cannelé",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Miroir rond de table artisanal avec cadre détaillé en plâtre écologique.",
            description: "Élégant miroir rond de table doté d'un cadre artisanal minutieusement détaillé en plâtre écologique. Une pièce décorative lumineuse et raffinée, idéale pour habiller une coiffeuse, une table de chevet ou un buffet.",
            aromaProfile: "Miroir de Table, Design Cannelé, Cadre Artisanal"
        }
    },
    14: {
        price: 5.90,
        pt: {
            name: "Porta-Joias Canelado com Tampa",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Porta-joias artesanal em Jesmonite com tampa de coroa esculpida e padrão marmoreado.",
            description: "Elegante porta-joias artesanal moldado em Jesmonite premium com requintado efeito marmoreado em tons rosa e branco. Apresenta corpo canelado e tampa decorativa com pega esculpida em coroa. Perfeito para guardar anéis, joias e pequenos tesouros no toucador com charme e impermeabilização acetinada.",
            aromaProfile: "Porta-Joias, Jesmonite Premium, Marmoreado Rosa, Elegante"
        },
        es: {
            name: "Joyero Acanalado con Tapa",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Joyero artesanal de Jesmonite con tapa de corona esculpida y patrón marmolado.",
            description: "Elegante joyero artesanal moldeado en Jesmonite premium con exquisito efecto marmolado en tonos rosa y blanco. Presenta cuerpo acanalado y tapa decorativa con tirador esculpido en forma de corona. Perfecto para guardar anillos, joyas y pequeños tesoros en el tocador con encanto y acabado impermeable satinado.",
            aromaProfile: "Joyero, Jesmonite Premium, Marmolado Rosa, Elegante"
        },
        en: {
            name: "Ribbed Jewelry Box with Lid",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted Jesmonite trinket & jewelry box with sculpted crown lid and pink marbled design.",
            description: "Elegant handcrafted trinket and jewelry box molded from premium Jesmonite featuring a gorgeous pink and white marbled pattern. Styled with a ribbed body and a decorative lid topped with a sculpted crown finial. Perfect for safely keeping rings, jewelry, and small treasures.",
            aromaProfile: "Jewelry Box, Premium Jesmonite, Pink Marbled, Elegant"
        },
        fr: {
            name: "Boîte à Bijoux Cannelée avec Couvercle",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Boîte à bijoux artisanale en Jesmonite avec couvercle couronné et motif marbré rose.",
            description: "Élégante boîte à bijoux artisanale moulée en Jesmonite premium au délicat motif marbré rose et blanc. Dotée d'un corps cannelé et d'un couvercle décoratif surmonté d'une couronne sculptée. Idéale pour ranger avec soin vos bagues, bijoux et précieux souvenirs.",
            aromaProfile: "Boîte à Bijoux, Jesmonite Premium, Marbré Rose, Élégant"
        }
    },
    15: {
        price: 5.90,
        pt: {
            name: "Placa de Homenagem Personalizada",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Placa de madeira decorada com flores secas e dedicatória personalizável.",
            description: "Elegante placa de madeira com dedicatória personalizada e arranjo de flores secas. Ideal para homenagear educadoras, professoras, mães ou pessoas especiais com uma mensagem única e inesquecível.",
            aromaProfile: "Homenagem, Personalizado, Flores Secas"
        },
        es: {
            name: "Placa de Condecoración Personalizada",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Placa de madera decorada con flores secas y dedicatoria personalizable.",
            description: "Elegante placa de madera con dedicatoria personalizada y arreglo de flores secas. Ideal para homenajear a educadoras, profesoras, madres o personas especiales con un mensaje único e inolvidable.",
            aromaProfile: "Condecoración, Personalizado, Flores Secas"
        },
        en: {
            name: "Personalized Commemorative Plaque",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Wooden plaque decorated with dried flowers and custom dedication.",
            description: "Elegant wooden plaque featuring a custom dedication and dried flower arrangement. Ideal for honoring teachers, educators, mothers, or loved ones with a unique message.",
            aromaProfile: "Commemorative, Custom, Dried Flowers"
        },
        fr: {
            name: "Plaque Commémorative Personnalisée",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plaque en bois ornée de fleurs séchées et dédicace personnalisable.",
            description: "Élégante plaque en bois avec dédicace personnalisée et arrangement de fleurs séchées. Idéale pour rendre hommage aux éducatrices, enseignantes, mères ou personnes spéciales.",
            aromaProfile: "Hommage, Personnalisé, Fleurs Séchées"
        }
    },
    16: {
        price: 9.90,
        pt: {
            name: "Peça Decorativa Sweet Home",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Escultura decorativa Sweet Home artesanal em Jesmonite marmoreado.",
            description: "Peça decorativa esculpida à mão em Jesmonite premium com tipografia elegante 'Home Sweet Home' e padrão marmoreado em tons roxo e branco. Uma escultura moderna e acolhedora perfeita para decorar prateleiras, consolas ou mesas de entrada.",
            aromaProfile: "Jesmonite, Sweet Home, Marmoreado, Escultura"
        },
        es: {
            name: "Pieza Decorativa Sweet Home",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Escultura decorativa Sweet Home artesanal de Jesmonite marmolado.",
            description: "Pieza decorativa esculpida a mano en Jesmonite premium con tipografía elegante 'Home Sweet Home' y patrón marmolado en tonos morado y blanco. Una escultura moderna y acogedora perfecta para decorar estanterías, consolas o recibidores.",
            aromaProfile: "Jesmonite, Sweet Home, Marmolado, Escultura"
        },
        en: {
            name: "Sweet Home Decorative Sculpture",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted Sweet Home decorative sculpture in marbled Jesmonite.",
            description: "Handcrafted decorative sculpture molded from premium Jesmonite featuring stylish 'Home Sweet Home' lettering in a purple and white marbled finish. A warm, modern accent piece ideal for shelving, entryways, or console tables.",
            aromaProfile: "Jesmonite, Sweet Home, Marbled, Sculpture"
        },
        fr: {
            name: "Pièce Décorative Sweet Home",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Sculpture décorative Sweet Home artisanale en Jesmonite marbrée.",
            description: "Sculpture décorative faite main en Jesmonite premium avec lettrage élégant 'Home Sweet Home' et fini marbré violet et blanc. Une pièce moderne et chaleureuse idéale pour embellir une étagère, une console ou une entrée.",
            aromaProfile: "Jesmonite, Sweet Home, Marbré, Sculpture"
        }
    },
    17: {
        price: 6.90,
        pt: {
            name: "Vaso Geométrico para Flores",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso decorativo bicolor com design geométrico em Jesmonite para flores.",
            description: "Vaso para flores artesanal moldado em Jesmonite premium com exclusivo design geométrico facetado em estilo origami bicolor (rosa e bege creme). Impermeabilizado com acabamento acetinado, ideal para arranjos de flores secas ou frescas e decoração contemporânea.",
            aromaProfile: "Jesmonite, Bicolor, Geométrico, Vaso para Flores"
        },
        es: {
            name: "Florero Geométrico",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Florero decorativo bicolor con diseño geométrico en Jesmonite.",
            description: "Florero decorativo artesanal moldeado en Jesmonite premium con exclusivo diseño geométrico facetado estilo origami bicolor (rosa y beige crema). Impermeabilizado con acabado satinado, ideal para arreglos de flores secas o frescas y decoración contemporánea.",
            aromaProfile: "Jesmonite, Bicolor, Geométrico, Florero"
        },
        en: {
            name: "Geometric Flower Vase",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted two-tone geometric Jesmonite vase for flowers.",
            description: "Handcrafted flower vase molded from premium Jesmonite featuring an exclusive two-tone faceted geometric origami silhouette (dusty pink and cream beige). Features a satin waterproof finish, perfect for dried or fresh flower arrangements and modern home decor.",
            aromaProfile: "Jesmonite, Two-tone, Geometric, Flower Vase"
        },
        fr: {
            name: "Vase Géométrique pour Fleurs",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase décoratif bicolore au design géométrique en Jesmonite pour fleurs.",
            description: "Vase pour fleurs artisanal moulé en Jesmonite premium au design géométrique facetté style origami bicolore (rose poudré et beige crème). Imperméabilisé avec finition satinée, idéal pour bouquets de fleurs séchées ou fraîches et déco moderne.",
            aromaProfile: "Jesmonite, Bicolore, Géométrique, Vase à Fleurs"
        }
    },
    18: {
        price: 19.90,
        pt: {
            name: "Conjunto Bloom",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Conjunto de bandejas artesanais com rebordo de contas em Jesmonite marmoreado.",
            description: "Elegante conjunto decorativo composto por bandeja redonda e bandeja oval artesanais esculpidas em Jesmonite premium com elegante efeito marmoreado em tons cinza e branco. Ambas as peças possuem rebordo decorado em contas (beaded design), ideais para organizar perfumes, joias, velas aromáticas ou como peças de destaque no ambiente.",
            aromaProfile: "Jesmonite, Marmoreado, Rebordo em Contas, Conjunto Decorativo"
        },
        es: {
            name: "Conjunto Bloom",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Conjunto de bandejas artesanales con borde de cuentas en Jesmonite marmolado.",
            description: "Elegante conjunto decorativo compuesto por bandeja redonda y bandeja ovalada artesanales esculpidas en Jesmonite premium con elegante efecto marmolado en tonos gris y blanco. Ambas piezas poseen borde decorado en cuentas (diseño perlado), ideales para organizar perfumes, joyas, velas aromáticas o como piezas destacadas en tu hogar.",
            aromaProfile: "Jesmonite, Marmolado, Borde de Cuentas, Conjunto Decorativo"
        },
        en: {
            name: "Bloom Tray Set",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted round & oval beaded tray set in marbled Jesmonite.",
            description: "Elegant decorative tray set featuring a round tray and an oval tray handcrafted from premium grey and white marbled Jesmonite. Both pieces display a distinctive beaded rim, perfect for styling perfumes, jewelry, scented candles, or home decor accents.",
            aromaProfile: "Jesmonite, Marbled, Beaded Rim, Decorative Set"
        },
        fr: {
            name: "Ensemble Bloom",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Ensemble de plateaux artisanaux à rebord perlé en Jesmonite marbrée.",
            description: "Élégant ensemble décoratif comprenant un plateau rond et un plateau ovale faits main en Jesmonite premium au motif marbré gris et blanc. Les deux pièces disposent d'une finition perlée raffinée, parfaites pour disposer parfums, bijoux, bougies ou embellir votre intérieur.",
            aromaProfile: "Jesmonite, Marbré, Rebord Perlé, Ensemble Décoratif"
        }
    },
    19: {
        price: 9.90,
        pt: {
            name: "Vaso para Velas Família",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Suporte para velas artesanal com a palavra Família e figuras esculpidas.",
            description: "Exclusivo suporte artesanal para velas moldado em gesso ecológico com padrão marmoreado em tons cinza e branco. Apresenta o nome 'Família' esculpido em relevo com delicadas figuras familiares no topo, criando uma atmosfera acolhedora e cheia de amor.",
            aromaProfile: "Família, Suporte para Velas, Marmoreado, Artesanal"
        },
        es: {
            name: "Vaso para Velas Família",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Portavelas artesanal con la palabra Família y figuras esculpidas.",
            description: "Exclusivo portavelas artesanal moldeado en yeso ecológico con patrón marmolado en tonos gris y blanco. Presenta la palabra 'Família' esculpida en relieve con delicadas figuras familiares en la parte superior, creando una atmósfera acogedora y llena de amor.",
            aromaProfile: "Família, Portavelas, Marmolado, Artesanal"
        },
        en: {
            name: "Família Candle Holder Vessel",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted candle holder with 'Família' lettering and sculpted family figures.",
            description: "Exclusive handcrafted candle holder vessel molded from eco-friendly plaster featuring a grey and white marbled effect. Features sculpted 'Família' lettering with charming family silhouettes on top, creating a warm, love-filled atmosphere.",
            aromaProfile: "Família, Candle Holder, Marbled, Handcrafted"
        },
        fr: {
            name: "Photophore / Vase à Bougies Família",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Porte-bougie artisanal gravé 'Família' avec figurines sculptées.",
            description: "Porte-bougie artisanal exclusif moulé en plâtre écologique au motif marbré gris et blanc. Arbore le mot 'Família' sculpté en relief surmonté de délicates figures familiales, apportant une atmosphère chaleureuse et empreinte d'amour.",
            aromaProfile: "Família, Porte-bougie, Marbré, Artisanal"
        }
    },
    20: {
        price: 7.90,
        pt: {
            name: "Vaso Geométrico Azul & Branco para Flores",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso decorativo artesanal bicolor azul marmoreado e branco para flores.",
            description: "Vaso para flores artesanal com design geométrico facetado estilo origami. Moldado em gesso ecológico premium com acabamento bicolor: parte superior azul petressência marmoreado e base branca. Impermeabilizado com toque acetinado, perfeito para arranjos florais secos ou naturais.",
            aromaProfile: "Vaso para Flores, Bicolor Azul e Branco, Geométrico, Artesanal"
        },
        es: {
            name: "Florero Geométrico Azul & Blanco",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Florero decorativo artesanal bicolor azul marmolado y blanco para flores.",
            description: "Florero decorativo artesanal con diseño geométrico facetado estilo origami. Moldeado en yeso ecológico premium con acabado bicolor: parte superior azul petressência marmolado y base blanca. Impermeabilizado con toque satinado, perfecto para arreglos florales secos o naturales.",
            aromaProfile: "Florero, Bicolor Azul y Blanco, Geométrico, Artesanal"
        },
        en: {
            name: "Blue & White Geometric Flower Vase",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted two-tone marbled blue and white geometric vase for flowers.",
            description: "Handcrafted flower vase featuring a faceted geometric origami design. Molded from premium eco-friendly plaster with a two-tone finish: marbled navy blue top and clean white base. Satin waterproof finish, ideal for dried or fresh floral arrangements.",
            aromaProfile: "Flower Vase, Blue & White, Geometric, Handcrafted"
        },
        fr: {
            name: "Vase Géométrique Bleu & Blanc pour Fleurs",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase décoratif bicolore bleu marbré et blanc pour fleurs.",
            description: "Vase pour fleurs artisanal au design géométrique facetté style origami. Moulé en plâtre écologique premium avec finition bicolore : partie supérieure bleu pétrole marbré et base blanche. Imperméabilisé au fini satiné, idéal pour bouquets séchés ou frais.",
            aromaProfile: "Vase à Fleurs, Bicolore Bleu & Blanc, Géométrique"
        }
    },
    21: {
        price: 4.90,
        pt: {
            name: "Vaso com Relevo de Corações",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso artesanal em Jesmonite marmoreado com relevos de corações 3D.",
            description: "Encantador vaso artesanal moldado em Jesmonite premium com efeito marmoreado em tom rosa e delicados corações esculpidos em relevo 3D na superfície externa. Perfeito para velas, pincéis, canetas ou como adorável peça decorativa.",
            aromaProfile: "Jesmonite, Corações em Relevo, Marmoreado, Artesanal"
        },
        es: {
            name: "Vaso con Relevo de Corazones",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Vaso artesanal de Jesmonite marmolado con relieves de corazones 3D.",
            description: "Encantador vaso artesanal moldeado en Jesmonite premium con efecto marmolado en tono rosa y delicados corazones esculpidos en relieve 3D en la superficie exterior. Perfecto para velas, pinceles, bolígrafos o como adorable pieza decorativa.",
            aromaProfile: "Jesmonite, Corazones en Relieve, Marmolado, Artesanal"
        },
        en: {
            name: "3D Heart Relief Pot",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted marbled pink Jesmonite pot with 3D heart reliefs.",
            description: "Charming handcrafted pot molded from premium Jesmonite featuring a soft pink marbled finish and delicate 3D heart reliefs around the exterior. Ideal for holding candles, makeup brushes, pens, or accenting home decor.",
            aromaProfile: "Jesmonite, 3D Heart Relief, Marbled, Handcrafted"
        },
        fr: {
            name: "Vase avec Relief Cœurs",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase artisanal en Jesmonite marbrée avec reliefs de cœurs 3D.",
            description: "Ravissant vase artisanal moulé en Jesmonite premium au motif marbré rose avec de délicats cœurs sculptés en relief 3D sur la paroi extérieure. Parfait pour accueillir bougies, pinceaux, stylos ou embellir votre intérieur.",
            aromaProfile: "Jesmonite, Relief Cœurs 3D, Marbré, Artisanal"
        }
    },
    22: {
        price: 6.90,
        pt: {
            name: "Vaso Canelado Lilás & Branco",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso artesanal canelado bicolor lilás e branco em Jesmonite.",
            description: "Elegante vaso decorativo canelado moldado em Jesmonite premium com sofisticado design bicolor: topo em tom lilás/púrpura suave e base branca. Com acabamento impermeável acetinado, é perfeito para arranjos florais secos ou como gracioso elemento decorativo.",
            aromaProfile: "Jesmonite, Bicolor Lilás e Branco, Canelado, Vaso Decorativo"
        },
        es: {
            name: "Florero Acanalado Lilas & Blanco",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Florero artesanal acanalado bicolor lila y blanco en Jesmonite.",
            description: "Elegante florero decorativo acanalado moldeado en Jesmonite premium con sofisticado diseño bicolor: parte superior en tono lila/púrpura suave y base blanca. Con acabado impermeable satinado, es perfecto para arreglos florales secos o como gracioso elemento decorativo.",
            aromaProfile: "Jesmonite, Bicolor Lila y Blanco, Acanalado, Florero"
        },
        en: {
            name: "Lilac & White Ribbed Vase",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted two-tone lilac and white ribbed Jesmonite vase.",
            description: "Elegant ribbed decorative vase handcrafted from premium Jesmonite featuring a sophisticated two-tone finish: dusty lilac/purple top and crisp white base. Satin waterproof finish, ideal for dried florals or modern tabletop decor.",
            aromaProfile: "Jesmonite, Two-tone Lilac & White, Ribbed, Decorative Vase"
        },
        fr: {
            name: "Vase Cannelé Lilas & Blanc",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase artisanal cannelé bicolore lilas et blanc en Jesmonite.",
            description: "Élégant vase décoratif cannelé fait main en Jesmonite premium avec une finition bicolore raffinée : haut en teinte lilas/violet poudré et base blanche. Imperméabilisé au fini satiné, idéal pour arrangements séchés ou déco tendance.",
            aromaProfile: "Jesmonite, Bicolore Lilas & Blanc, Cannelé, Vase Décoratif"
        }
    },
    23: {
        price: 5.90,
        pt: {
            name: "Bandeja Oval com Rebordo de Contas",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Bandeja oval artesanal em Jesmonite bege com rebordo decorado em contas.",
            description: "Elegante bandeja oval artesanal moldada em Jesmonite premium num tom bege neutro e minimalista. Apresenta rebordo interior trabalhado em contas (beaded detail) e acabamento suave acetinado. Perfeita para organizar joias, perfumes, sabonetes ou como base sofisticada para velas.",
            aromaProfile: "Jesmonite, Bandeja Oval, Rebordo em Contas, Bege Minimalista"
        },
        es: {
            name: "Bandeja Ovalada con Borde de Cuentas",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Bandeja ovalada artesanal de Jesmonite beige con borde decorado en cuentas.",
            description: "Elegante bandeja ovalada artesanal moldeada en Jesmonite premium en un tono beige neutro y minimalista. Presenta borde interior trabajado en cuentas (detalle perlado) y acabado suave satinado. Perfecta para organizar joyas, perfumes, jabones o como base sofisticada para velas.",
            aromaProfile: "Jesmonite, Bandeja Ovalada, Borde de Cuentas, Beige Minimalista"
        },
        en: {
            name: "Oval Beaded Rim Tray",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted neutral beige oval Jesmonite tray with beaded inner rim.",
            description: "Handcrafted oval decorative tray molded from premium Jesmonite in a neutral beige tone. Features a detailed beaded inner rim and smooth satin finish. Ideal for styling jewelry, perfumes, soaps, or as a chic candle base.",
            aromaProfile: "Jesmonite, Oval Tray, Beaded Rim, Neutral Beige"
        },
        fr: {
            name: "Plateau Ovale à Rebord Perlé",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plateau ovale artisanal en Jesmonite beige avec rebord perlé.",
            description: "Élégant plateau ovale artisanal moulé en Jesmonite premium dans une nuance beige neutre et minimaliste. Arbore un rebord intérieur travaillé en perles et une finition satinée. Parfait pour disposer bijoux, parfums, savons ou comme base pour bougies.",
            aromaProfile: "Jesmonite, Plateau Ovale, Rebord Perlé, Beige Minimaliste"
        }
    },
    25: {
        price: 6.90,
        pt: {
            name: "Vaso Decorativo de Natal",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso artesanal de Natal em tom vinho com relevos 3D natalícios.",
            description: "Encantador vaso decorativo artesanal moldado em gesso ecológico premium num tom vermelho vinho festivo. Apresenta ricos relevos 3D com motivos de Natal como árvores de Natal, flocos de neve, renas e prendas. Perfeito para iluminar a decoração natalícia do seu lar.",
            aromaProfile: "Natal, Relevos 3D, Vermelho Vinho, Artesanal"
        },
        es: {
            name: "Florero Decorativo de Navidad",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Florero artesanal de Navidad en tono vino con relieves 3D navideños.",
            description: "Encantador florero decorativo artesanal moldeado en yeso ecológico premium en un tono rojo vino festivo. Presenta ricos relieves 3D con motivos navideños como pinos, copos de nieve, renos y regalos. Perfecto para iluminar la decoración navideña de tu hogar.",
            aromaProfile: "Navidad, Relieves 3D, Rojo Vino, Artesanal"
        },
        en: {
            name: "Christmas Decorative Vase",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted burgundy Christmas vase featuring 3D holiday reliefs.",
            description: "Charming decorative vase handcrafted from premium eco-friendly plaster in a festive burgundy red hue. Decorated with intricate 3D Christmas reliefs including pine trees, snowflakes, reindeer, and gifts. Perfect for styling cozy holiday table settings.",
            aromaProfile: "Christmas, 3D Reliefs, Festive Burgundy, Handcrafted"
        },
        fr: {
            name: "Vase Décoratif de Noël",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase de Noël artisanal bordeaux à reliefs 3D féeriques.",
            description: "Ravissant vase décoratif fait main en plâtre écologique dans un ton rouge bordeaux festif. Arbore de riches reliefs 3D représentant sapins de Noël, flocons de neige, rennes et cadeaux. Parfait pour illuminer votre décoration de fêtes.",
            aromaProfile: "Noël, Reliefs 3D, Rouge Bordeaux, Artisanal"
        }
    },
    26: {
        price: 4.90,
        pt: {
            name: "Caixa Multiusos Corações em Relevo",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Caixa multiusos com tampa em Jesmonite cinza com corações 3D em relevo.",
            description: "Caixa decorativa multiusos artesanal com tampa moldada em Jesmonite premium num tom cinza suave. Apresenta delicados corações esculpidos em relevo 3D ao redor do corpo. Perfeita para guardar joias, pequenos objetos, algodão ou utilizar como adorável peça decorativa.",
            aromaProfile: "Jesmonite, Corações em Relevo, Caixa Multiusos, Artesanal"
        },
        es: {
            name: "Cajita Multiusos Corazones en Relieve",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Cajita multiusos con tapa en Jesmonite gris con corazones 3D en relieve.",
            description: "Cajita decorativa multiusos artesanal con tapa moldeada en Jesmonite premium en un tono gris suave. Presenta delicados corazones esculpidos en relieve 3D alrededor del cuerpo. Perfecta para guardar joyas, pequeños objetos, algodón o utilizar como adorable pieza decorativa.",
            aromaProfile: "Jesmonite, Corazones en Relieve, Cajita Multiusos, Artesanal"
        },
        en: {
            name: "3D Heart Relief Multipurpose Box",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted soft grey Jesmonite box with lid and 3D heart reliefs.",
            description: "Handcrafted multipurpose decorative box with lid molded from premium soft grey Jesmonite. Decorated with sweet 3D heart reliefs around the exterior. Ideal for holding jewelry, small trinkets, cotton pads, or accenting home decor.",
            aromaProfile: "Jesmonite, 3D Heart Relief, Multipurpose Box, Handcrafted"
        },
        fr: {
            name: "Boîte Multi-usages Cœurs en Relief",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Boîte multi-usages avec couvercle en Jesmonite gris avec cœurs 3D.",
            description: "Boîte décorative multi-usages artisanale avec couvercle moulée en Jesmonite premium dans un ton gris doux. Arbore de délicats cœurs sculptés en relief 3D. Parfaite pour ranger bijoux, petits accessoires, ou embellir votre intérieur.",
            aromaProfile: "Jesmonite, Relief Cœurs 3D, Boîte Multi-usages"
        }
    },
    27: {
        price: 5.90,
        pt: {
            name: "Caixa Multiusos Flor",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Caixa decorativa multiusos artesanal em formato de flor em Jesmonite com tampa.",
            description: "Encantadora caixa decorativa multiusos moldada em Jesmonite premium com gracioso formato de flor e tampa a condizer. Possui acabamento suave acetinado, ideal para guardar joias, pequenos objetos, algodão ou utilizar como elegante elemento decorativo.",
            aromaProfile: "Jesmonite, Formato Flor, Caixa Multiusos, Artesanal"
        },
        es: {
            name: "Cajita Multiusos Flor",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Cajita decorativa multiusos artesanal en forma de flor en Jesmonite con tapa.",
            description: "Encantadora cajita decorativa multiusos moldeada en Jesmonite premium con graciosa forma de flor y tapa a juego. Posee acabado suave satinado, ideal para guardar joyas, pequeños objetos, algodón o utilizar como elegante elemento decorativo.",
            aromaProfile: "Jesmonite, Forma de Flor, Cajita Multiusos, Artesanal"
        },
        en: {
            name: "Flower Shaped Multipurpose Box",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted flower-shaped Jesmonite box with matching lid.",
            description: "Charming handcrafted multipurpose decorative box molded from premium Jesmonite featuring an elegant flower silhouette with matching lid. Features a smooth satin finish, perfect for storing jewelry, small trinkets, cotton pads, or home accent styling.",
            aromaProfile: "Jesmonite, Flower Shape, Multipurpose Box, Handcrafted"
        },
        fr: {
            name: "Boîte Multi-usages Fleur",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Boîte décorative multi-usages artisanale en forme de fleur en Jesmonite.",
            description: "Ravissante boîte décorative multi-usages moulée en Jesmonite premium aux élégantes formes de fleur avec couvercle assorti. Finition satinée, idéale pour ranger bijoux, petits accessoires, ou comme pièce maîtresse de votre décoration.",
            aromaProfile: "Jesmonite, Forme Fleur, Boîte Multi-usages"
        }
    },
    28: {
        price: 3.90,
        pt: {
            name: "Base / Porta-Velas Flor de Lótus",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Porta-velas artesanal em formato de flor de lótus em Jesmonite verde água.",
            description: "Delicado suporte artesanal para velas em formato de flor de lótus com pétalas gravadas em relevo, esculpido em Jesmonite premium num suave tom verde água/menta. Acabamento acetinado impermeável, perfeito para acolher velas tealight, velas moldadas ou enriquecer o seu altar e decoração.",
            aromaProfile: "Jesmonite, Flor de Lótus, Porta-Velas, Verde Água"
        },
        es: {
            name: "Base / Portavelas Flor de Loto",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Portavelas artesanal en forma de flor de loto en Jesmonite verde agua.",
            description: "Delicado soporte artesanal para velas en forma de flor de loto con pétalos grabados en relieve, esculpido en Jesmonite premium en un suave tono verde agua/menta. Acabado satinado impermeable, perfecto para acoger velas tealight, velas moldeadas o enriquecer tu altar y decoración.",
            aromaProfile: "Jesmonite, Flor de Loto, Portavelas, Verde Agua"
        },
        en: {
            name: "Lotus Flower Candle Holder Base",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted seafoam green Jesmonite candle holder in lotus flower shape.",
            description: "Delicate handcrafted candle holder base shaped like a lotus flower with etched petal patterns, molded from premium seafoam green/mint Jesmonite. Features a smooth satin finish, ideal for tealight candles, molded candles, or mindful home styling.",
            aromaProfile: "Jesmonite, Lotus Flower, Candle Holder, Seafoam Green"
        },
        fr: {
            name: "Base / Photophore Fleur de Lotus",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Porte-bougie artisanal en forme de fleur de lotus en Jesmonite vert eau.",
            description: "Délicat support artisanal pour bougies en forme de fleur de lotus aux pétales gravés en relief, moulé en Jesmonite premium dans un doux ton vert eau. Finition satinée imperméable, parfait pour accueillir bougies chauffe-plat ou sublimer votre décoration.",
            aromaProfile: "Jesmonite, Fleur de Lotus, Photophore, Vert Eau"
        }
    },
    29: {
        price: 5.90,
        pt: {
            name: "Bandeja Oval Marmoreada",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Bandeja oval artesanal marmoreada cinza e branco em Jesmonite com rebordo de contas.",
            description: "Elegante bandeja oval artesanal moldada em Jesmonite premium com sofisticado padrão marmoreado em tons cinza e branco. Possui rebordo interior em contas (beaded rim) e acabamento impermeável acetinado. Perfeita para organizar perfumes, joias, sabonetes ou utilizar como base de velas.",
            aromaProfile: "Jesmonite, Bandeja Oval, Marmoreado Cinza, Rebordo em Contas"
        },
        es: {
            name: "Bandeja Ovalada Marmolada",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Bandeja ovalada artesanal marmolada gris y blanco en Jesmonite con borde de cuentas.",
            description: "Elegante bandeja ovalada artesanal moldeada en Jesmonite premium con sofisticado patrón marmolado en tonos gris y blanco. Posee borde interior en cuentas (borde perlado) y acabado impermeable satinado. Perfecta para organizar perfumes, joyas, jabones o utilizar como base de velas.",
            aromaProfile: "Jesmonite, Bandeja Ovalada, Marmolado Gris, Borde de Cuentas"
        },
        en: {
            name: "Marbled Oval Tray with Beaded Rim",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted grey and white marbled oval Jesmonite tray with beaded rim.",
            description: "Handcrafted decorative oval tray molded from premium Jesmonite featuring a beautiful grey and white marbled pattern. Designed with a delicate beaded inner rim and satin waterproof finish. Ideal for organizing perfumes, jewelry, soaps, or styling candles.",
            aromaProfile: "Jesmonite, Oval Tray, Grey Marbled, Beaded Rim"
        },
        fr: {
            name: "Plateau Ovale Marbré à Rebord Perlé",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plateau ovale artisanal marbré gris et blanc en Jesmonite avec rebord perlé.",
            description: "Élégant plateau ovale artisanal moulé en Jesmonite premium au motif marbré gris et blanc. Arbore un rebord intérieur perlé et une finition satinée imperméable. Parfait pour disposer parfums, bijoux, savons ou utiliser comme socle pour bougies.",
            aromaProfile: "Jesmonite, Plateau Ovale, Marbré Gris, Rebord Perlé"
        }
    },
    30: {
        price: 15.90,
        pt: {
            name: "Conjunto Lívia",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Conjunto artesanal em Jesmonite tom lilás com recipiente canelado, prato lótus e bandeja.",
            description: "Exclusivo conjunto decorativo feito à mão em Jesmonite premium num requintado tom lilás/malva. Composto por recipiente canelado com tampa, prato artesanal em formato de flor de lótus e bandeja oval com rebordo em contas. Uma combinação sofisticada e funcional para organizar joias, perfumes ou enriquecer qualquer ambiente.",
            aromaProfile: "Jesmonite Premium, Lilás Malva, Conjunto Decorativo, Artesanal"
        },
        es: {
            name: "Conjunto Lívia",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Conjunto artesanal de Jesmonite tono lila con recipiente acanalado, plato loto y bandeja.",
            description: "Exclusivo conjunto decorativo hecho a mano en Jesmonite premium en un exquisito tono lila/malva. Compuesto por recipiente acanalado con tapa, plato artesanal en forma de flor de loto y bandeja ovalada con borde de cuentas. Una combinación sofisticada y funcional para organizar joyas, perfumes o enriquecer cualquier estancia.",
            aromaProfile: "Jesmonite Premium, Lila Malva, Conjunto Decorativo, Artesanal"
        },
        en: {
            name: "Lívia Decorative Set",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted dusty lilac Jesmonite set with ribbed jar, lotus dish, and tray.",
            description: "Exclusive handcrafted decorative set molded from premium Jesmonite in a sophisticated dusty lilac hue. Includes a ribbed vessel with lid, lotus flower dish, and beaded oval tray. A refined, functional trio perfect for styling jewelry, perfumes, or tabletop accents.",
            aromaProfile: "Premium Jesmonite, Dusty Lilac, Decorative Trio, Handcrafted"
        },
        fr: {
            name: "Ensemble Lívia",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Ensemble artisanal en Jesmonite lilas avec pot cannelé, coupe lotus et plateau.",
            description: "Ensemble décoratif exclusif fait main en Jesmonite premium dans un élégant ton lilas/mauve. Composé d'un pot cannelé avec couvercle, d'une coupe en forme de fleur de lotus et d'un plateau ovale perlé. Un trio raffiné et fonctionnel pour organiser bijoux, parfums ou sublimer votre intérieur.",
            aromaProfile: "Jesmonite Premium, Lilas Mauve, Ensemble Décoratif, Artisanal"
        }
    },
    31: {
        price: 6.90,
        pt: {
            name: "Vaso Canelado Marmoreado",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso decorativo artesanal canelado com efeito marmoreado rosa e terracota em Jesmonite.",
            description: "Elegante vaso decorativo artesanal moldado em Jesmonite premium com sofisticado textura canelada e padrão marmoreado em tons rosa suave e terracota. Possui acabamento impermeável acetinado, sendo ideal para acolher flores secas ou embelezar toucadores, mesas e estantes.",
            aromaProfile: "Jesmonite, Marmoreado Rosa, Canelado, Vaso Decorativo"
        },
        es: {
            name: "Florero Acanalado Marmolado",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Florero decorativo artesanal acanalado con efecto marmolado rosa y terracota en Jesmonite.",
            description: "Elegante florero decorativo artesanal moldeado en Jesmonite premium con sofisticada textura acanalada y patrón marmolado en tonos rosa suave y terracota. Posee acabado impermeable satinado, siendo ideal para acoger flores secas o embellecer tocadores, mesas y estanterías.",
            aromaProfile: "Jesmonite, Marmolado Rosa, Acanalado, Florero"
        },
        en: {
            name: "Pink Marbled Ribbed Vase",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted ribbed Jesmonite vase with dusty pink and terracotta marbled pattern.",
            description: "Elegant handcrafted decorative vase molded from premium Jesmonite featuring a ribbed texture and a stunning dusty pink & terracotta marbled pattern. Finished with a satin waterproof coating, perfect for dried flowers or tabletop styling.",
            aromaProfile: "Jesmonite, Pink Marbled, Ribbed, Decorative Vase"
        },
        fr: {
            name: "Vase Cannelé Marbré",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase décoratif artisanal cannelé au motif marbré rose et terre cuite en Jesmonite.",
            description: "Élégant vase décoratif artisanal moulé en Jesmonite premium à la texture cannelée et au motif marbré rose poudré et terre cuite. Finition satinée imperméable, idéal pour accueillir des fleurs séchées ou embellir votre intérieur.",
            aromaProfile: "Jesmonite, Marbré Rose, Cannelé, Vase Décoratif"
        }
    },
    32: {
        price: 12.90,
        pt: {
            name: "Conjunto Vaso & Bandeja Azul Marmoreado",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Conjunto artesanal de vaso canelado e bandeja oval em Jesmonite azul marmoreado.",
            description: "Elegante conjunto decorativo composto por vaso canelado e bandeja oval com rebordo em contas, moldados artesanalmente em Jesmonite premium com deslumbrante efeito marmoreado em tons azul céu e branco. Perfeito para organizar perfumes, joias ou utilizar como refinada peça de destaque.",
            aromaProfile: "Jesmonite, Azul Céu Marmoreado, Vaso e Bandeja, Artesanal"
        },
        es: {
            name: "Conjunto Florero & Bandeja Azul Marmolado",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Conjunto artesanal de florero acanalado y bandeja ovalada en Jesmonite azul marmolado.",
            description: "Elegante conjunto decorativo compuesto por florero acanalado y bandeja ovalada con borde de cuentas, moldeados artesanalmente en Jesmonite premium con deslumbrante efecto marmolado en tonos azul cielo y blanco. Perfecto para organizar perfumes, joyas o utilizar como refinada pieza destacada.",
            aromaProfile: "Jesmonite, Azul Cielo Marmolado, Florero y Bandeja, Artesanal"
        },
        en: {
            name: "Marbled Sky Blue Vase & Tray Set",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted marbled sky blue and white Jesmonite ribbed vase and beaded tray set.",
            description: "Handcrafted decorative duo featuring a ribbed vase paired with a beaded-rim oval tray, molded from premium Jesmonite with a stunning sky blue and white marbled effect. Finished with a satin waterproof seal, perfect for styling perfumes, jewelry, or tabletop decor.",
            aromaProfile: "Jesmonite, Sky Blue Marbled, Vase & Tray Set, Handcrafted"
        },
        fr: {
            name: "Ensemble Vase & Plateau Bleu Marbré",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Ensemble artisanal avec vase cannelé et plateau ovale en Jesmonite bleu marbré.",
            description: "Élégant duo décoratif composé d'un vase cannelé et d'un plateau ovale à rebord perlé, moulés à la main en Jesmonite premium au superbe motif marbré bleu ciel et blanc. Imperméabilisé avec finition satinée, idéal pour disposer parfums, bijoux ou embellir votre intérieur.",
            aromaProfile: "Jesmonite, Bleu Ciel Marbré, Ensemble Vase & Plateau"
        }
    },
    33: {
        price: 5.90,
        pt: {
            name: "Base para Velas",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Base artesanal em Jesmonite desenhada para acolher e destacar velas decorativas.",
            description: "Elegante base artesanal para velas moldada em Jesmonite premium com acabamento suave impermeabilizado. Desenhada especialmente para proteger superfícies e proporcionar um suporte sofisticado e seguro para as nossas velas aromáticas ou decorativas.",
            aromaProfile: "Jesmonite, Base para Velas, Design Minimalista, Artesanal"
        },
        es: {
            name: "Base para Velas",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Base artesanal en Jesmonite diseñada para acoger y destacar velas decorativas.",
            description: "Elegante base artesanal para velas moldeada en Jesmonite premium con acabado suave impermeabilizado. Diseñada especialmente para proteger superficies y proporcionar un soporte sofisticado y seguro para nuestras velas aromáticas o decorativas.",
            aromaProfile: "Jesmonite, Base para Velas, Diseño Minimalista, Artesanal"
        },
        en: {
            name: "Candle Tray Base",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted Jesmonite tray base designed to display and protect candles.",
            description: "Elegant handcrafted candle base molded from premium Jesmonite featuring a smooth waterproof satin finish. Designed to protect surfaces while offering a stylish, secure stand for scented or decorative pillar candles.",
            aromaProfile: "Jesmonite, Candle Base, Minimalist Design, Handcrafted"
        },
        fr: {
            name: "Base pour Bougies",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Base artisanale en Jesmonite conçue pour sublimer et protéger vos bougies.",
            description: "Élégante base artisanale pour bougies moulée en Jesmonite premium avec une finition satinée imperméabilisée. Conçue pour protéger vos meubles tout en offrant un support élégant et sécurisé à vos bougies parfumées.",
            aromaProfile: "Jesmonite, Base pour Bougies, Design Minimaliste"
        }
    },
    36: {
        price: 3.90,
        pt: {
            name: "Base / Porta-Velas Flor de Lótus Malva",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Porta-velas artesanal em formato de flor de lótus em Jesmonite tom malva.",
            description: "Delicado suporte artesanal para velas em formato de flor de lótus com pétalas gravadas em relevo, esculpido em Jesmonite premium num elegante tom lilás/malva. Acabamento acetinado impermeável, perfeito para acolher velas tealight, velas moldadas ou enriquecer o seu altar e decoração.",
            aromaProfile: "Jesmonite, Flor de Lótus, Porta-Velas, Lilás Malva"
        },
        es: {
            name: "Base / Portavelas Flor de Loto Malva",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Portavelas artesanal en forma de flor de loto en Jesmonite tono malva.",
            description: "Delicado soporte artesanal para velas en forma de flor de loto con pétalos grabados en relief, esculpido en Jesmonite premium en un elegante tono lila/malva. Acabado satinado impermeable, perfecto para acoger velas tealight, velas moldeadas o enriquecer tu altar y decoración.",
            aromaProfile: "Jesmonite, Flor de Loto, Portavelas, Lila Malva"
        },
        en: {
            name: "Mauve Lotus Flower Candle Holder Base",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted dusty mauve Jesmonite candle holder in lotus flower shape.",
            description: "Delicate handcrafted candle holder base shaped like a lotus flower with etched petal details, molded from premium dusty lilac/mauve Jesmonite. Features a smooth satin finish, ideal for tealight candles, molded candles, or elegant home styling.",
            aromaProfile: "Jesmonite, Lotus Flower, Candle Holder, Dusty Mauve"
        },
        fr: {
            name: "Base / Photophore Fleur de Lotus Mauve",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Porte-bougie artisanal en forme de fleur de lotus en Jesmonite mauve.",
            description: "Délicat support artisanal pour bougies en forme de fleur de lotus aux pétales gravés en relief, moulé en Jesmonite premium dans une douce teinte lilas/mauve. Finition satinée imperméable, parfait pour accueillir bougies chauffe-plat ou sublimer votre intérieur.",
            aromaProfile: "Jesmonite, Fleur de Lotus, Photophore, Mauve"
        }
    },
    34: {
        price: 6.90,
        pt: {
            name: "Vaso Geométrico com Arranjo Floral",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Vaso geométrica artesanal em Jesmonite marmoreado com arranjo de flores secas.",
            description: "Elegante vaso para flores artesanal com design geométrico facetado em estilo origami, moldado em Jesmonite premium com acabamento marmoreado em tons cinza carvão e branco. Acompanha um gracioso arranjo de flores secas em tons rosa vibrante e bege natural. Impermeabilizado com toque acetinado, perfeito para trazer vida e requinte a qualquer ambiente.",
            aromaProfile: "Vaso Geométrico, Jesmonite Premium, Flores Secas, Marmoreado"
        },
        es: {
            name: "Florero Geométrico con Arreglo Floral",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Florero geométrico artesanal de Jesmonite marmolado con arreglo de flores secas.",
            description: "Elegante florero artesanal con diseño geométrico facetado estilo origami, moldeado en Jesmonite premium con acabado marmolado en tonos gris carbón y blanco. Acompañado por un vistoso arreglo de flores secas en tonos rosa vibrante y beige natural. Impermeabilizado con un toque satinado, perfecto para dar vida y refinamiento a cualquier espacio.",
            aromaProfile: "Florero Geométrico, Jesmonite Premium, Flores Secas, Marmolado"
        },
        en: {
            name: "Geometric Origami Vase with Dried Flowers",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted marbled Jesmonite origami vase featuring vibrant dried flower bouquet.",
            description: "Elegant handcrafted flower vase with a faceted geometric origami design, molded from premium Jesmonite in a charcoal gray and white marbled finish. Paired with a charming arrangement of vibrant pink and beige natural dried flowers. Waterproofed with a smooth satin seal.",
            aromaProfile: "Geometric Vase, Premium Jesmonite, Dried Flowers, Marbled"
        },
        fr: {
            name: "Vase Géométrique Origami avec Fleurs Séchées",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Vase géométrique artisanal en Jesmonite marbré accompagné d'un bouquet de fleurs séchées.",
            description: "Élégant vase artisanal au design géométrique facetté style origami, moulé en Jesmonite premium au fini marbré gris charbon et blanc. Accompagné d'un ravissant bouquet de fleurs séchées aux nuances rose vif et beige naturel. Imperméabilisé avec une finition satinée.",
            aromaProfile: "Vase Géométrique, Jesmonite Premium, Fleurs Séchées, Marbré"
        }
    },
    35: {
        price: 6.90,
        pt: {
            name: "Bandeja Redonda Floral",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Bandeja redonda artesanal em Jesmonite com relevos florais em estilo mandala.",
            description: "Encantadora bandeja redonda artesanal esculpida em Jesmonite premium num elegante tom azul acinzentado suave. Apresenta um trabalhado e minucioso padrão floral em relevo entalhado estilo mandala. Possui acabamento impermeável acetinado, sendo perfeita para acolher joias, copos, velas aromáticas ou servir como porta-copos e suporte decorativo de destaque.",
            aromaProfile: "Bandeja Redonda, Jesmonite Premium, Relevos Florais, Mandala"
        },
        es: {
            name: "Bandeja Redonda Floral",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Bandeja redonda artesanal de Jesmonite con relieves florales estilo mandala.",
            description: "Encantadora bandeja redonda artesanal esculpida en Jesmonite premium en un elegante tono azul grisáceo suave. Presenta un detallado y minucioso patrón floral en relieve grabado estilo mandala. Posee acabado impermeable satinado, siendo perfecta para acoger joyas, vasos, velas aromáticas o servir como posavasos y soporte decorativo destacado.",
            aromaProfile: "Bandeja Redonda, Jesmonite Premium, Relieves Florales, Mandala"
        },
        en: {
            name: "Floral Engraved Round Tray",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted round Jesmonite tray featuring carved mandala floral reliefs.",
            description: "Charming handcrafted round tray molded from premium Jesmonite in a soothing dusty blue shade. Styled with an intricately carved mandala floral relief pattern and a waterproof satin seal. Ideal for organizing jewelry, scented candles, or serving as an elegant decorative coaster.",
            aromaProfile: "Round Tray, Premium Jesmonite, Floral Reliefs, Mandala"
        },
        fr: {
            name: "Plateau Rond Floral",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Plateau rond artisanal en Jesmonite avec reliefs floraux style mandala.",
            description: "Ravissant plateau rond artisanal moulé en Jesmonite premium dans une douce teinte bleu gris. Arbore un minutieux motif floral gravé en relief style mandala et une finition satinée imperméable. Parfait pour disposer bijoux, bougies parfumées, ou servir de dessous de verre raffiné.",
            aromaProfile: "Plateau Rond, Jesmonite Premium, Reliefs Floraux, Mandala"
        }
    },
    37: {
        price: 4.90,
        pt: {
            name: "Pote Decorativo com Tampa",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Pote multiusos artesanal marmoreado em tons cinza escuro com tampa em Jesmonite.",
            description: "Elegante pote decorativo multiusos artesanal moldado em Jesmonite premium com requintado efeito marmoreado em tons cinza escuro e carvão. Acompanha tampa encaixável a condizer e acabamento suave impermeabilizado. Ideal para guardar joias, pequenos objetos, algodão ou utilizar como sofisticado acessório decorativo.",
            aromaProfile: "Jesmonite, Pote Decorativo, Marmoreado Cinza, Com Tampa"
        },
        es: {
            name: "Pote Decorativo con Tapa",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Pote multiusos artesanal marmolado en tonos gris oscuro con tapa en Jesmonite.",
            description: "Elegante pote decorativo multiusos artesanal moldeado en Jesmonite premium con exquisito efecto marmolado en tonos gris oscuro y carbón. Incluye tapa encajable a juego y acabado suave impermeabilizado. Ideal para guardar joyas, pequeños objetos, algodón o utilizar como sofisticado accesorio decorativo.",
            aromaProfile: "Jesmonite, Pote Decorativo, Marmolado Gris, Con Tapa"
        },
        en: {
            name: "Charcoal Marbled Pot with Lid",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted charcoal grey marbled Jesmonite multipurpose jar with lid.",
            description: "Handcrafted multipurpose decorative pot molded from premium Jesmonite featuring a deep charcoal grey marbled finish. Includes a matching stepped lid and satin waterproof seal. Perfect for storing jewelry, cotton pads, trinkets, or sleek modern tabletop styling.",
            aromaProfile: "Jesmonite, Decorative Pot, Charcoal Marbled, With Lid"
        },
        fr: {
            name: "Pot Décoratif avec Couvercle",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Pot multi-usages artisanal marbré gris foncé avec couvercle en Jesmonite.",
            description: "Élégant pot décoratif multi-usages artisanal moulé en Jesmonite premium au fini marbré gris foncé et anthracite. Livré avec un couvercle assorti et une finition satinée imperméabilisée. Idéal pour ranger bijoux, petits accessoires, coton ou embellir votre intérieur.",
            aromaProfile: "Jesmonite, Pot Décoratif, Marbré Gris, Avec Couvercle"
        }
    },
    38: {
        price: 9.90,
        pt: {
            name: "Peça Decorativa Amor Eterno",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Escultura artesanal de enamorados em Jesmonite para celebrar o amor.",
            description: "Romântica e elegante escultura artesanal moldada em Jesmonite premium, desenhada para celebrar o amor e o carinho entre namorados e casais. Com linhas fluídas e acabamento suave impermeabilizado, é um presente inesquecível para aniversários de namoro, Dia dos Namorados ou como peça carregada de significado para o lar.",
            aromaProfile: "Jesmonite, Amor Eterno, Enamorados, Escultura Romântica"
        },
        es: {
            name: "Pieza Decorativa Amor Eterno",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Escultura artesanal de enamorados en Jesmonite para celebrar el amor.",
            description: "Romántica y elegante escultura artesanal moldeada en Jesmonite premium, diseñada para celebrar el amor y el cariño entre enamorados y parejas. Con líneas fluidas y acabado suave impermeabilizado, es un regalo inolvidable para aniversarios, San Valentín o como una pieza llena de significado para el hogar.",
            aromaProfile: "Jesmonite, Amor Eterno, Enamorados, Escultura Romántica"
        },
        en: {
            name: "Eternal Love Couple Sculpture",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted Jesmonite romantic couple sculpture celebrating love.",
            description: "Romantic and elegant handcrafted sculpture molded from premium Jesmonite, created to celebrate love and devotion between couples. Featuring fluid sculptural lines and a smooth satin finish, it makes an unforgettable gift for anniversaries, Valentine's Day, or romantic home decor.",
            aromaProfile: "Jesmonite, Eternal Love, Lovers Sculpture, Handcrafted"
        },
        fr: {
            name: "Sculpture Amour Éternel",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Sculpture romantique d'amoureux en Jesmonite faite main pour célébrer l'amour.",
            description: "Élégante sculpture romantique faite main en Jesmonite premium, conçue pour célébrer l'amour et l'union des couples. Aux lignes fluides et au fini satiné imperméabilisé, c'est un cadeau inoubliable pour les anniversaires de rencontre, la Saint-Valentin ou pour sublimer votre intérieur.",
            aromaProfile: "Jesmonite, Amour Éternel, Sculpture Amoureux, Romantique"
        }
    },
    39: {
        price: 5.90,
        pt: {
            name: "Saboneteira Oval",
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Saboneteira e bandeja oval artesanal em Jesmonite azul marmoreado com rebordo em contas.",
            description: "Elegante saboneteira e bandeja oval artesanal moldada em Jesmonite premium com encantador acabamento marmoreado em tons azul céu e branco. Apresenta rebordo interior trabalhado em contas (beaded rim) e impermeabilização acetinada de alta resistência. Perfeita para organizar sabonetes artesanais, joias ou pequenas peças de toucador.",
            aromaProfile: "Jesmonite, Saboneteira Oval, Azul Céu Marmoreado, Rebordo em Contas"
        },
        es: {
            name: "Jabonera Ovalada",
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Jabonera y bandeja ovalada artesanal en Jesmonite azul marmolado con borde de cuentas.",
            description: "Elegante jabonera y bandeja ovalada artesanal moldeada en Jesmonite premium con encantador acabado marmolado en tonos azul cielo y blanco. Presenta borde interior trabajado en cuentas (borde perlado) e impermeabilización satinada de alta resistencia. Perfecta para organizar jabones artesanales, joyas o pequeñas piezas de tocador.",
            aromaProfile: "Jesmonite, Jabonera Ovalada, Azul Cielo Marmolado, Borde de Cuentas"
        },
        en: {
            name: "Oval Marbled Soap Dish",
            categoryLabel: "Decorative Piece",
            aromaBrief: "Handcrafted sky blue and white marbled oval Jesmonite soap dish tray with beaded rim.",
            description: "Handcrafted oval soap dish tray molded from premium Jesmonite featuring a soothing sky blue & white marbled pattern. Designed with a delicate beaded rim and a durable waterproof satin coating. Ideal for artisan soaps, jewelry, or bathroom vanity styling.",
            aromaProfile: "Jesmonite, Oval Soap Dish, Sky Blue Marbled, Beaded Rim"
        },
        fr: {
            name: "Porte-Savon Ovale",
            categoryLabel: "Pièce Décorative",
            aromaBrief: "Porte-savon et plateau ovale artisanal en Jesmonite bleu marbré avec rebord perlé.",
            description: "Élégant porte-savon et plateau ovale fait main en Jesmonite premium au superbe fini marbré bleu ciel et blanc. Arbore un rebord intérieur perlé et une imperméabilisation satinée haute résistance. Parfait pour vos savons artisanaux, bijoux ou accessoires de toilette.",
            aromaProfile: "Jesmonite, Porte-Savon Ovale, Bleu Ciel Marbré, Rebord Perlé"
        }
    }
};

for (let i = 1; i <= 39; i++) {
    if (i === 24) continue; // User requested to delete/remove decor-24
    const override = DECORATIVE_OVERRIDES[i];
    const nameTemplate = DECORATIVE_NAMES[(i - 1) % DECORATIVE_NAMES.length];
    const priceVariation = ((i * 0.3) % 2.0) - 1.0; // Subtle price variation
    const finalPrice = override ? override.price : Math.round((nameTemplate.basePrice + priceVariation) * 10) / 10;
    
    PRODUCTS.push({
        id: `decor-${i}`,
        category: "decorativa",
        price: finalPrice,
        image: `assets/decor_${i}.jpg`,
        qty: 1,
        pt: (override && override.pt) ? override.pt : {
            name: `${nameTemplate.pt} #${i}`,
            categoryLabel: "Peça Decorativa",
            aromaBrief: "Design minimalista e elegante em gesso ecológico com acabamento impermeabilizado.",
            description: "Uma peça decorativa exclusiva feita à mão em gesso ecológico premium, com acabamento impermeável acetinado. Perfeita para organizar joias, perfumes, sabonetes ou como base para as nossas velas aromáticas. Cada peça é única e moldada individualmente em Portugal.",
            aromaProfile: "Eco-friendly, Design Exclusivo, Pintura Manual"
        },
        es: (override && override.es) ? override.es : {
            name: `${nameTemplate.es} #${i}`,
            categoryLabel: "Pieza Decorativa",
            aromaBrief: "Diseño minimalista y elegante en yeso ecológico con acabado impermeabilizado.",
            description: "Una pieza de yeso ecológica premium hecha a mano, con acabado impermeable satinado. Perfecta para organizar joyas, perfumes, jabones o como base para nuestras velas aromáticas. Cada pieza es única y moldeada individualmente en Portugal.",
            aromaProfile: "Eco-friendly, Diseño Exclusivo, Pintura Manual"
        },
        en: (override && override.en) ? override.en : {
            name: `${nameTemplate.en} #${i}`,
            categoryLabel: "Decorative Piece",
            aromaBrief: "Minimalist and elegant design in eco-friendly plaster with waterproof finish.",
            description: "An exclusive handcrafted decorative piece made of premium eco-friendly plaster, with a satin waterproof finish. Perfect for organizing jewelry, perfumes, soaps or as a base for our scented candles. Each piece is unique and individually molded in Portugal.",
            aromaProfile: "Eco-friendly, Exclusive Design, Hand Painted"
        },
        fr: (override && override.fr) ? override.fr : {
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
        price: 6.90,
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
        price: 6.90,
        image: "assets/soap_amendoa_aveia.jpeg",
        pt: {
            name: "Sabonete de Aveia & Amêndoa",
            desc: "Ideal para nutrir, proteger e rejuvenescer a pele.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, essência natural de aveia e mel, mel, amêndoa e flocos de aveia e essência de amêndoas doces. Benefícios estéticos: A amêndoa e a aveia são ricos em propriedades estéticas complementares ideais para nutrir, proteger e rejuvenescer a pele. Enquanto o essência de amêndoa atua na hidratação e luminosidade, a aveia foca na regeneração celular, firmeza e suavidade. Espiritualmente: Elas nutrem o corpo físico para promover a clareza mental, o equilíbrio emocional e a elevação da vibração energética.",
            aromaProfile: "Clareza Mental, Equilíbrio Emocional, Nutrição"
        },
        es: {
            name: "Jabón de Avena & Almendra",
            desc: "Ideal para nutrir, proteger y rejuvenecer la piel.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, esencia natural de avena y miel, miel, almendra, copos de avena y esencia de almendras dulces. Beneficios estéticos: La almendra y la avena son ricas en propiedades estéticas complementarias ideales para nutrir, proteger y rejuvenecer la piel. Mientras que el esencia de almendras actúa en la hidratación y luminosidad, la avena se enfoca en la regeneración celular, firmeza y suavidad. Espiritualmente: Nutren el cuerpo físico para promover la claridad mental, el equilibrio emocional y la elevación de la vibración energética.",
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
            longDesc: "Ingrédients: Glycérine 100% végétale, essence naturelle d'avoine et miel, miel, amande, flocons d'avoine et essence d'amande douce. Bienfaits esthétiques: L'amande et l'avoine sont riches en propriétés esthétiques complémentaires idéales pour nourrir, protéger et rajeunir la peau. Tandis que l'essence d'amande agit sur l'hydratation et l'éclat, l'avoine se concentre sur la régénération cellulaire, la fermeté et la douceur. Spirituellement: Ils nourrissent le corps physique pour favoriser la clarté mentale, l'équilibre émotionnel et l'élévation de la vibration énergétique.",
            aromaProfile: "Clarté Mentale, Équilibre Émotionnel, Nutrition"
        }
    },
    {
        id: "soap-anis-mel",
        price: 6.90,
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
        price: 6.90,
        image: "assets/soap_camomila.jpeg",
        pt: {
            name: "Sabonete de Camomila",
            desc: "Acalma a pele irritada e ajuda na renovação cutânea.",
            longDesc: "Ingredientes: Água, glicerina 100% vegetal, camomila e essência de camomila. Benefícios estéticos: Acalma a pele irritada, ajuda em problemas de eczema ou acne. Renovação da pele. Espiritualmente: Ajuda a ficar mais tranquilo e equilibrado. Ajuda nas tomadas de decisões e a restaurar forças.",
            aromaProfile: "Tranquilidade, Equilíbrio, Restauração"
        },
        es: {
            name: "Jabón de Manzanilla",
            desc: "Calma la piel irritada y ayuda a la renovación cutánea.",
            longDesc: "Ingredientes: Agua, glicerina 100% vegetal, manzanilla y esencia de manzanilla. Beneficios estéticos: Calma la piel irritada, ayuda en problemas de eczema o acné. Renovación de la piel. Espiritualmente: Ayuda a estar más tranquilo y equilibrado. Ayuda en la toma de decisiones y a restaurar fuerzas.",
            aromaProfile: "Tranquilidad, Equilibrio, Restauración"
        },
        en: {
            name: "Chamomile Soap",
            desc: "Soothes irritated skin and helps with skin renewal.",
            longDesc: "Ingredients: Water, 100% vegetable glycerin, chamomile, and chamomile fragrance. Aesthetic benefits: Soothes irritated skin, helps with eczema or acne. Skin renewal. Spiritually: Helps to stay calm and balanced. Helps in decision-making and restoring strength.",
            aromaProfile: "Tranquility, Balance, Restoration"
        },
        fr: {
            name: "Savon à la Camomille",
            desc: "Apaise la peau irritée et aide au renouvellement cutané.",
            longDesc: "Ingrédients: Eau, glycérine 100% végétale, camomille et essence de camomille. Bienfaits esthétiques: Aide à hydrater la peau irritée, aide en cas d'eczéma ou d'acné. Renouvellement de la peau. Spirituellement: Aide à rester plus tranquille et équilibré. Aide à la prise de décision et à restaurer les forces.",
            aromaProfile: "Tranquillité, Équilibre, Restauration"
        }
    },
    {
        id: "soap-carvao",
        price: 6.90,
        image: "assets/soap_carvao.jpeg",
        pt: {
            name: "Sabonete de Carbão",
            desc: "Controla a oleosidade e limpa profundamente os poros.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, carvão ativo e água. Benefícios estéticos: Controla a oleosidade da pele, limpeza dos poros, clareador de manchas. Espiritualmente: Ajuda a eliminar energias negativas.",
            aromaProfile: "Purificação, Limpeza, Proteção Energética"
        },
        es: {
            name: "Jabón de Carbón",
            desc: "Controla la grasa y limpia profundamente los poros.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, carbón activo y agua. Beneficios estéticos: Controla la grasa de la piel, limpieza de los poros, aclara manchas. Espiritualmente: Ayuda a eliminar energías negativas.",
            aromaProfile: "Purificación, Limpieza, Protección Energética"
        },
        en: {
            name: "Charcoal Soap",
            desc: "Controls oiliness and deeply cleanses the pores.",
            longDesc: "Ingredients: 100% vegetable glycerin, activated charcoal, and water. Aesthetic benefits: Controls skin oiliness, cleanses pores, and lightens dark spots. Spiritually: Helps eliminate negative energies.",
            aromaProfile: "Purification, Cleansing, Energy Protection"
        },
        fr: {
            name: "Savon au Charbon",
            desc: "Contrôle l'excès de sébum et nettoie les pores en profondeur.",
            longDesc: "Ingrédients: Glycérine 100% végétale, charbon actif et eau. Bienfaits esthétiques: Contrôle l'excès de sébum de la peau, nettoie les pores, éclaircit les taches. Spirituellement: Aide à éliminer les énergies négatives.",
            aromaProfile: "Purification, Nettoyage, Protection Énergétique"
        }
    },
    {
        id: "soap-chia",
        price: 6.90,
        image: "assets/soap_chia.jpeg",
        pt: {
            name: "Sabonete de Chia",
            desc: "Massagem esfoliante estimulante que ativa a microcirculação.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, água, sementes de chia e essência de hortelã. Benefícios estéticos: Massagem esfoliante estimulante que ativa a microcirculação, removendo impurezas e células mortas. Espiritualmente: A chia simboliza prosperidade, crescimento e renovação de energias.",
            aromaProfile: "Prosperidade, Crescimento, Renovação"
        },
        es: {
            name: "Jabón de Chía",
            desc: "Masaje exfoliante estimulante que activa la microcirculación.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, agua, semillas de chía y esencia de menta. Beneficios estéticos: Masaje exfoliante estimulante que activa la microcirculación, eliminando impurezas y células muertas. Espiritualmente: La chía simboliza prosperidad, crecimiento y renovación de energías.",
            aromaProfile: "Prosperidad, Crecimiento, Renovación"
        },
        en: {
            name: "Chia Seed Soap",
            desc: "Stimulating exfoliating massage that boosts microcirculation.",
            longDesc: "Ingredients: 100% vegetable glycerin, water, chia seeds, and mint fragrance. Aesthetic benefits: Stimulating exfoliating massage that boosts microcirculation, removing impurities and dead cells. Spiritually: Chia symbolizes prosperity, growth, and energy renewal.",
            aromaProfile: "Prosperity, Growth, Renewal"
        },
        fr: {
            name: "Savon aux Graines de Chia",
            desc: "Massage exfoliant stimulant qui active la microcirculation.",
            longDesc: "Ingrédients: Glycérine 100% végétale, eau, graines de chia et essence de menthe. Bienfaits esthétiques: Massage exfoliant stimulant qui active la microcirculation, éliminant les impuretés et les cellules mortes. Spirituellement: Le chia symbolise la prospérité, la croissance et le renouvellement des énergies.",
            aromaProfile: "Prospérité, Croissance, Renouvellement"
        }
    },
    {
        id: "soap-coco",
        price: 6.90,
        image: "assets/soap_coco.jpeg",
        pt: {
            name: "Sabonete de Coco",
            desc: "Hidratante facial e corporal, ideal para aliviar queimaduras solares.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, água, coco ralado e essência natural de coco. Benefícios estéticos: Hidratante facial e corporal. Limpa impurezas. Calmante e excelente para aliviar queimaduras provocadas pela exposição solar. Espiritualmente: O coco simboliza fertilidade e prosperidade.",
            aromaProfile: "Fertilidade, Prosperidade, Alívio"
        },
        es: {
            name: "Jabón de Coco",
            desc: "Hidratante facial y corporal, ideal para aliviar quemaduras solares.",
            longDesc: "Ingredientes: Glicerina 100% vegetal, agua, coco rallado y esencia natural de coco. Beneficios estéticos: Hidratante facial y corporal. Limpia impurezas. Calmante y excelente para aliviar quemaduras provocadas por la exposición solar. Espiritualmente: El coco simboliza fertilidad y prosperidad.",
            aromaProfile: "Fertilidad, Prosperidad, Alivio"
        },
        en: {
            name: "Coconut Soap",
            desc: "Facial and body moisturizer, ideal for soothing sunburns.",
            longDesc: "Ingredients: 100% vegetable glycerin, water, grated coconut, and natural coconut fragrance. Aesthetic benefits: Facial and body moisturizer. Cleanses impurities. Soothing and excellent for relieving sunburns caused by sun exposure. Spiritually: Coconut symbolizes fertility and prosperity.",
            aromaProfile: "Fertility, Prosperity, Relief"
        },
        fr: {
            name: "Savon Noix de Coco",
            desc: "Hydratant visage et corps, idéal pour apaiser les coups de soleil.",
            longDesc: "Ingrédients: Glycérine 100% végétale, eau, noix de coco râpée et essence naturelle de noix de coco. Bienfaits esthétiques: Hydratant visage et corps. Nettoie les impuretés. Apaisant et excellent pour soulager les brûlures causées par l'exposition solaire. Spirituellement: La noix de coco symbolise la fertilité et la prospérité.",
            aromaProfile: "Fertilité, Prospérité, Soulagement"
        }
    },
    {
        id: "soap-jasmim",
        price: 6.90,
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
        price: 6.90,
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
        price: 6.90,
        image: "assets/soap_maca_canela.jpeg",
        pt: {
            name: "Sabonete de Maçã & Canela",
            desc: "Renovação celular e suavização de rugas de expressão.",
            longDesc: "Ingredientes: Maçã, canela, água, glicerina 100% vegetal e essência de maçã e canela. Benefícios estéticos: Anti-inflamatório e ajuda na diminuição da acne. Suaviza rugas de expressão, renovação de células e ajuda na aparência cansada e sem brilho. Espiritualmente: Fertilidade, beleza, juventude, prosperidade, abundância de caminhos e abertura.",
            aromaProfile: "Abundância, Beleza, Prosperidade"
        },
        es: {
            name: "Jabón de Manzana & Canela",
            desc: "Renovación celular y suavizado de arrugas de expresión.",
            longDesc: "Ingredientes: Manzana, canela, agua, glicerina 100% vegetal y esencia de manzana y canela. Beneficios estéticos: Antiinflamatorio y ayuda en la disminución del acné. Suaviza arrugas de expresión, renovación celular y ayuda con la apariencia cansada y sin brillo. Espiritualmente: Fertilidad, belleza, juventud, prosperidad, abundancia y apertura de caminos.",
            aromaProfile: "Abundancia, Belleza, Prosperidad"
        },
        en: {
            name: "Apple & Cinnamon Soap",
            desc: "Cell renewal and smoothing of expression lines.",
            longDesc: "Ingredients: Apple, cinnamon, water, 100% vegetable glycerin, and apple & cinnamon fragrance essence. Aesthetic benefits: Anti-inflammatory and helps reduce acne. Smooths expression wrinkles, promotes cell renewal, and helps with tired, dull skin. Spiritually: Fertility, beauty, youth, prosperity, abundance, and path opening.",
            aromaProfile: "Abundance, Beauty, Prosperity"
        },
        fr: {
            name: "Savon Pomme & Cannelle",
            desc: "Renouvellement cellulaire et lissage des rides d'expression.",
            longDesc: "Ingrédients: Pomme, cannelle, eau, glycérine 100% végétale et essence parfumée de pomme et cannelle. Bienfaits esthétiques: Anti-inflammatoire et aide à réduire l'acné. Lisse les rides d'expression, favorise le renouvellement cellulaire et aide à revitaliser les peaux ternes et fatiguées. Spirituellement: Fertilité, beauté, jeunesse, prospérité, abondance et ouverture de chemins.",
            aromaProfile: "Abondance, Beauté, Prospérité"
        }
    },
    {
        id: "soap-mel",
        price: 6.90,
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
        price: 6.90,
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
        price: 6.90,
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
    { pt: "Buquê de Velas Florais Premium", es: "Ramo de Velas Florales Premium", en: "Premium Floral Candle Bouquet", fr: "Bouquet de Bougies Florales Premium", basePrice: 15.90 },
    { pt: "Buquê Blue Rose", es: "Buquê Blue Rose", en: "Blue Rose Bouquet", fr: "Bouquet Blue Rose", basePrice: 15.90 },
    { pt: "Buquê Essence Flowers", es: "Buquê Essence Flowers", en: "Essence Flowers Bouquet", fr: "Bouquet Essence Flowers", basePrice: 34.90 },
    { pt: "Buquê de Velas Elegance", es: "Ramo de Velas Elegance", en: "Elegance Candle Bouquet", fr: "Bouquet de Bougies Élégance", basePrice: 34.90 },
    { pt: "Buquê de Velas Lavanda Real", es: "Buquê de Velas Lavanda Real", en: "Royal Lavender Candle Bouquet", fr: "Bouquet de Bougies Lavande Royale", basePrice: 34.90 },
    { pt: "Buquê de Velas Silvestres", es: "Buquê de Velas Silvestres", en: "Wild Flower Candle Bouquet", fr: "Bouquet de Bougies Sauvages", basePrice: 24.90 },
    { pt: "Buquê de Velas Doce Carinho", es: "Ramo de Velas Dulce Cariño", en: "Sweet Affection Candle Bouquet", fr: "Bouquet de Bougies Doux Câlin", basePrice: 24.90 },
    { pt: "Estatueta Serena com Arranjo Girassol", es: "Estatuilla Serena con Arreglo de Girasoles", en: "Serenity Statuette with Sunflower Bouquet", fr: "Statuette Sérénité avec Tournesol", basePrice: 14.90 },
    { pt: "Arranjo de Velas Peónias de Luxo", es: "Arreglo de Velas Peonías de Lujo", en: "Luxury Peonies Candle Arrangement", fr: "Arrangement de Bougies Pivoines de Luxe", basePrice: 32.90 },
    { pt: "Buquê de Velas Amor Eterno", es: "Ramo de Velas Amor Eterno", en: "Eternal Love Candle Bouquet", fr: "Bouquet de Bougies Amour Éternel", basePrice: 32.90 }
];

for (let i = 1; i <= 10; i++) {
    const bouquet = BOUQUET_NAMES[i - 1];
    let ptDesc = `Um maravilhoso arranjo feito à mão com velas em cera de soja em forma de flores realistas. Ideal para oferecer como um presente único e sofisticado, ou para decorar e perfumar qualquer ambiente com elegância e iluminação acolhedora. Apresentado com embrulho decorativo premium.`;
    let esDesc = `Un maravilloso arreglo hecho a mano con velas en cera de soja en forma de flores realistas. Ideal para ofrecer como un regalo único y sofisticado, o para decorar y perfumar cualquier ambiente con elegancia e iluminación acogedora. Presentado con envoltorio decorativo premium.`;
    let enDesc = `A wonderful handcrafted arrangement featuring realistic flower-shaped soy wax candles. Perfect as a unique and sophisticated gift, or to elegantly decorate and scent any space with soft warm light. Presented in premium decorative packaging.`;
    let frDesc = `Un magnifique arrangement fait main avec des bougies en cire de soja en forme de fleurs réalistes. Idéal à offrir comme cadeau unique et sophistiqué, ou pour décorer et parfumer n'importe quel espace avec élégance. Présenté dans un emballage decoratif de qualidade superior.`;
    let ptBrief = "Arranjo floral artístico feito inteiramente de velas em cera de soja artesanais perfumadas.";
    let esBrief = "Arreglo floral artístico hecho completamente de velas en cera de soja artesanales aromáticas.";
    let enBrief = "Artistic floral arrangement made entirely of scented handcrafted soy wax candles.";
    let frBrief = "Arrangement floral artistique entièrement composé de bougies parfumées en cire de soja.";

    if (i === 2) {
        ptDesc = "Encantador arranjo artesanal 'Buquê Blue Rose', elaborado com rosas esculpidas à mão em cera de soja em tons azul marinho e branco suave, decorado com laço de fita de cetim azul e gipsófilas secas sobre um vaso canelado. Um presente gracioso e memorável.";
        esDesc = "Encantador arreglo artesanal 'Buquê Blue Rose', elaborado con rosas esculpidas a mano en cera de soja en tonos azul marino y blanco suave, decorado con lazo de cinta de satén azul y gipsófilas secas sobre un jarrón acanalado. Un regalo gracioso y memorable.";
        enDesc = "Charming handcrafted 'Buquê Blue Rose' arrangement featuring hand-carved blue and white soy wax rose candles, tied with a blue satin ribbon and dried gypsophila in a white ribbed pot.";
        frDesc = "Ravissant arrangement artisanal 'Buquê Blue Rose' composé de roses en cire de soja bleu et blanc, orné d'un ruban en satin bleu et de fleurs séchées dans un vase ondulé.";
        ptBrief = "Arranjo de velas artesanais de rosas azuis e brancas com laço de cetim.";
        esBrief = "Arreglo de velas artesanales de rosas azules y blancas con lazo de satén.";
        enBrief = "Handcrafted blue and white rose soy candle bouquet with satin ribbon.";
        frBrief = "Bouquet de bougies artisanales en forme de roses bleues et blanches avec ruban.";
    }

    if (i === 3) {
        ptDesc = "Espetacular e volumoso 'Buquê Essence Flowers', elaborado artesanalmente com um deslumbrante jardim de velas em cera de soja natural esculpidas em forma de flores em tons rosa suave, creme e branco. Envolvido num requintado tule preto transparente com debrum dourado e rematado com um vibrante laço de fita cor-de-rosa choque. Uma peça floral de luxo para surpreender em momentos inesquecíveis.";
        esDesc = "Espectacular y voluminoso 'Buquê Essence Flowers', elaborado artesanalmente con un deslumbrante jardín de velas en cera de soja natural esculpidas en forma de flores en tonos rosa suave, crema y blanco. Envuelto en un exquisito tul negro transparente con ribete dorado y rematado con un vibrante lazo de cinta fucsia. Una pieza floral de lujo para sorprender en momentos inolvidables.";
        enDesc = "Spectacular and lush 'Buquê Essence Flowers' bouquet, handcrafted with a stunning array of sculpted soy wax flower candles in soft pink, cream, and white. Wrapped in sheer black tulle with gold-trimmed edges and finished with a bold hot pink ribbon bow. A luxurious candle bouquet designed for unforgettable moments.";
        frDesc = "Spectaculaire et généreux 'Buquê Essence Flowers' composé d'un somptueux jardin de bougies en cire de soja sculptées en fleurs aux nuances rose, crème et blanc. Enveloppé dans un tulle noir transparent bordé de liseré doré et rehaussé d'un ruban rose fuchsia. Une création florale d'exception.";
        ptBrief = "Arranjo volumoso de velas florais em tule preto com laço rosa vibrante.";
        esBrief = "Arreglo voluminoso de velas florales en tul negro con lazo rosa vibrante.";
        enBrief = "Lush soy candle flower bouquet wrapped in gold-trimmed black tulle.";
        frBrief = "Généreux bouquet de bougies fleurs dans un tulle noir et ruban fuchsia.";
    }

    if (i === 8) {
        ptDesc = "Delicada estatueta decorativa esculpida artesanalmente em Jesmonite premium em tom branco acetinado com feição serena. Coroada no topo por um radiante arranjo floral de girassóis e flores secas. Uma peça artística singular e inspiradora para harmonizar toucadores e mesas com distinção.";
        esDesc = "Delicada estatuilla decorativa esculpida artesanalmente en Jesmonite premium en tono blanco satinado con expresión serena. Coronada en la parte superior por un radiante arreglo floral de girasoles y flores secas. Una pieza artística singular e inspiradora para armonizar tocadores y mesas con distinción.";
        enDesc = "Delicate decorative statuette sculpted from premium white Jesmonite featuring a serene aesthetic. Crowned at the top with a vibrant sunflower and dried flower arrangement. A unique artistic accent piece to elevate any vanity or tabletop display.";
        frDesc = "Délicate statuette décorative sculptée à la main en Jesmonite premium blanc satiné à l'expression sereine. Couronnée d'un lumineux arrangement floral de tournesols et fleurs séchées. Une pièce artistique unique et inspirante pour embellir votre intérieur.";
        ptBrief = "Estatueta artesanal em Jesmonite com arranjo floral de girassol e flores secas.";
        esBrief = "Estatuilla artesanal de Jesmonite con arreglo floral de girasoles y flores secas.";
        enBrief = "Handcrafted Jesmonite statuette featuring sunflower dried floral arrangement.";
        frBrief = "Statuette artisanale en Jesmonite avec arrangement floral de tournesol.";
    }

    PRODUCTS.push({
        id: `buque-${i}`,
        category: "set",
        price: bouquet.basePrice,
        image: `assets/buque_${i}.jpeg`,
        qty: 1,
        pt: {
            name: bouquet.pt,
            categoryLabel: "Buquê",
            aromaBrief: ptBrief,
            description: ptDesc,
            aromaProfile: i === 8 ? "Jesmonite Premium, Estatueta Artesanal, Girassóis, Flores Secas" : "Cera de Soja 100% Natural, Floral Premium, Elegante"
        },
        es: {
            name: bouquet.es,
            categoryLabel: "Buqué",
            aromaBrief: esBrief,
            description: esDesc,
            aromaProfile: i === 8 ? "Jesmonite Premium, Estatuilla Artesanal, Girasoles, Flores Secas" : "Cera de Soja 100% Natural, Floral Premium, Elegante"
        },
        en: {
            name: bouquet.en,
            categoryLabel: "Bouquet",
            aromaBrief: enBrief,
            description: enDesc,
            aromaProfile: i === 8 ? "Premium Jesmonite, Handcrafted Statuette, Sunflowers, Dried Flowers" : "100% Natural Soy Wax, Premium Floral, Elegant"
        },
        fr: {
            name: bouquet.fr,
            categoryLabel: "Bouquet",
            aromaBrief: frBrief,
            description: frDesc,
            aromaProfile: i === 8 ? "Jesmonite Premium, Statuette Artisanale, Tournesols, Fleurs Séchées" : "Cire de Soja 100% Naturelle, Floral Premium, Élégant"
        }
    });
}

const VERAO_ITEMS = [
    { pt: "Conjunto Búzio Marê", es: "Conjunto Búzio Marê", en: "Búzio Marê Seashell Set", fr: "Ensemble Coquillages Búzios Marê", category: "decorativa", price: 10.90, descPt: "Conjunto marinho artesanal em Jesmonite com conchas e detalhes oceânicos.", descEs: "Conjunto marino artesanal en Jesmonite con conchas y detalles oceánicos.", descEn: "Handcrafted Jesmonite ocean set featuring seashells and marine embeds.", descFr: "Ensemble marin artisanal en Jesmonite avec coquillages et éléments océaniques." },
    { pt: "Conjunto Areal", es: "Conjunto Areal", en: "Areal Decorative Set", fr: "Ensemble Décoratif Areal", category: "decorativa", price: 9.90, descPt: "Conjunto decorativo artesanal em Jesmonite com vaso étnico terracota e bandeja oval.", descEs: "Conjunto decorativo artesanal en Jesmonite con maceta étnica terracota y bandeja ovalada.", descEn: "Handcrafted Jesmonite decorative set featuring terracotta tribal pot and oval tray.", descFr: "Ensemble decoratif artisanal en Jesmonite avec pot ethnique terre cuite et plateau." },
    { pt: "Vela Aromática Estrela do Mar", es: "Vela Aromática Estrella de Mar", en: "Starfish Scented Candle", fr: "Bougie Parfumée Étoile de Mer", category: "vela", price: 8.90, descPt: "Vela aromática artesanal em formato de estrela-do-mar em Jesmonite com gel azul e conchas.", descEs: "Vela aromática artesanal en forma de estrella de mar en Jesmonite con gel azul y conchas.", descEn: "Handcrafted starfish scented candle in Jesmonite with ocean blue gel and shells.", descFr: "Bougie parfumée artisanale en forme d'étoile de mer en Jesmonite avec gel bleu et coquillages." },
    { pt: "Concha do Mar", es: "Concha de Mar", en: "Seashell Decorative Dish", fr: "Coquillage Décoratif Marine", category: "decorativa", price: 3.90, descPt: "Delicada concha marinha artesanal em gesso ecológico premium.", descEs: "Delicada concha marina artesanal en yeso ecológico premium.", descEn: "Handcrafted seashell decorative dish in premium eco-friendly plaster.", descFr: "Vide-poche artisanal en forme d' coquillage en plâtre écologique." },
    { pt: "Estrela da Marê", es: "Estrela da Marê", en: "Estrela da Marê Starfish Dish", fr: "Vide-Poche Étoile da Marê", category: "decorativa", price: 3.90, descPt: "Graciosa estrela-do-mar artesanal em gesso ecológico com acabamento branco.", descEs: "Graciosa estrella de mar artesanal en yeso ecológico con acabado blanco.", descEn: "Handcrafted starfish decorative dish in premium eco-friendly plaster.", descFr: "Vide-poche artisanal en forme d'étoile de mer en plâtre écologique." },
    { pt: "Búzio da Marê", es: "Búzio da Marê", en: "Búzio da Marê Conch Shell", fr: "Coquillage Búzio da Marê", category: "decorativa", price: 6.90, descPt: "Recipiente artesanal em formato de búzios em Jesmonite com gel azul e detalhes marinhos.", descEs: "Recipiente artesanal en forma de caracola en Jesmonite con gel azul y detalles marinos.", descEn: "Handcrafted conch shell vessel in Jesmonite with ocean blue gel and nautical embeds.", descFr: "Coquillage artisanal en Jesmonite avec gel bleu et éléments marins." },
    { pt: "Vela Concha do Mar", es: "Vela Concha de Mar", en: "Seashell Candle", fr: "Bougie Coquillage de Mer", category: "vela", price: 5.90, descPt: "Encantadora vela artesanal vertida numa concha marinha em gesso ecológico com pérolas e conchas.", descEs: "Encantadora vela artesanal vertida en una concha marina en yeso ecológico con perlas y conchas.", descEn: "Charming handcrafted soy candle poured in an eco-friendly plaster seashell dish with pearls.", descFr: "Bougie artisanale en cire de soja moulée dans un coquillage en plâtre écologique avec perles." },
    { pt: "Saboneteira Oval Canelada", es: "Jabonera Ovalada Acanalada", en: "Ribbed Oval Soap Dish", fr: "Porte-Savon Ovale Ondulé", category: "decorativa", price: 2.90, descPt: "Elegante saboneteira e bandeja decorativa em gesso ecológico com rebordo canelado.", descEs: "Elegante jabonera y bandeja decorativa en yeso ecológico con borde acanalado.", descEn: "Handcrafted oval soap dish and trinket tray in premium eco-friendly plaster.", descFr: "Élégant porte-savon et plateau décoratif en plâtre écologique." },
    { pt: "Vela Estrela da Marê", es: "Vela Estrela da Marê", en: "Estrela da Marê Gel Candle", fr: "Bougie Gel Étoile da Marê", category: "vela", price: 6.90, descPt: "Vela aromática artesanal em cera em gel azul cristalino em formato de estrela-do-mar em Jesmonite.", descEs: "Vela aromática artesanal en cera en gel azul cristalino en forma de estrella de mar en Jesmonite.", descEn: "Handcrafted ocean blue gel wax candle in a Jesmonite starfish dish with gold accents.", descFr: "Bougie artisanale en cire de gel bleu lagon coulée dans une étoile de mer en Jesmonite." },
    { pt: "Búzio Maresia", es: "Búzio Maresia", en: "Búzio Maresia Conch Shell", fr: "Coquillage Búzio Maresia", category: "decorativa", price: 5.90, descPt: "Recipiente decorativo marinho em gesso ecológico com textura escultural realista de búzios.", descEs: "Recipiente decorativo marino en yeso ecológico con textura escultural realista de caracola.", descEn: "Handcrafted conch shell decorative holder in premium eco-friendly plaster.", descFr: "Récipient décoratif en forme de coquillage en plâtre écologique." },
    { pt: "Vaso Pôr do Sol", es: "Vaso Pôr do Sol", en: "Sunset Decorative Bowl", fr: "Coupe Décorative Coucher de Soleil", category: "decorativa", price: 4.90, descPt: "Elegante vaso decorativo circular em gesso ecológico em tom alaranjado do pôr do sol.", descEs: "Elegante vaso decorativo circular en yeso ecológico en tono anaranjado del atardecer.", descEn: "Handcrafted circular decorative bowl in eco-friendly plaster with warm sunset orange tones.", descFr: "Coupe décorative circulaire en plâtre écologique aux teintes chaudes du coucher de soleil." },
    { pt: "Vaso Wave", es: "Vaso Wave", en: "Wave Ocean Decorative Bowl", fr: "Coupe Décorative Wave", category: "decorativa", price: 8.90, descPt: "Espetacular vaso decorativo em gesso ecológico com padrão marmoreado de ondas azuis oceânicas.", descEs: "Espectacular vaso decorativo en yeso ecológico con patrón marmoleado de olas azules oceánicas.", descEn: "Handcrafted circular decorative bowl in eco-friendly plaster with a blue wave marble swirl.", descFr: "Coupe décorative en plâtre écologique avec effet marbré bleu lagon." }
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
            categoryLabel: item.category === "vela" ? "Vela Aromática (Verão)" : (item.category === "set" ? "Set Decorativo (Verão)" : "Peça Decorativa (Verão)"),
            aromaBrief: item.descPt,
            description: item.category === "vela" 
                ? `${item.pt} da nossa coleção exclusiva de Verão. Vela aromática feita à mão com cera de soja e essências selecionadas.`
                : `${item.pt} da nossa coleção exclusiva de Verão. Peça decorativa feita à mão em Jesmonite premium com acabamento impermeabilizado.`,
            aromaProfile: "Verão, Frescor, Edição Limitada"
        },
        es: {
            name: item.es,
            categoryLabel: item.category === "vela" ? "Vela Aromática (Verano)" : "Pieza Decorativa (Verano)",
            aromaBrief: item.descEs,
            description: item.category === "vela" 
                ? `${item.es} de nuestra colección exclusiva de Verano. Vela aromática hecha a mano con cera de soja y esencias seleccionadas.`
                : `${item.es} de nuestra colección exclusiva de Verano. Pieza decorativa hecha a mano con yeso ecológico y acabado impermeabilizado.`,
            aromaProfile: "Verano, Frescura, Edición Limitada"
        },
        en: {
            name: item.en,
            categoryLabel: item.category === "vela" ? "Scented Candle (Summer)" : "Decorative Piece (Summer)",
            aromaBrief: item.descEn,
            description: item.category === "vela" 
                ? `${item.en} from our exclusive Summer Collection. Scented candle handcrafted with soy wax and selected fragrances.`
                : `${item.en} from our exclusive Summer Collection. Decorative piece handcrafted with premium eco-friendly plaster and waterproof finish.`,
            aromaProfile: "Summer, Freshness, Limited Edition"
        },
        fr: {
            name: item.fr,
            categoryLabel: item.category === "vela" ? "Bougie Parfumée (Été)" : "Pièce Décorative (Été)",
            aromaBrief: item.descFr,
            description: item.category === "vela" 
                ? `${item.fr} de notre collection exclusive d'Été. Bougie parfumée fabriquée à la main avec de la cire de soja et des essences sélectionnées.`
                : `${item.fr} de notre collection exclusive d'Été. Pièce décortive fabriquée à la main avec du plâtre écologique et une finition imperméabilisée.`,
            aromaProfile: "Été, Fraîcheur, Édition Limitée"
        }
    };
    
    if (i === 1) {
        itemData.pt.description = "Exclusivo conjunto marinho artesanal moldado em Jesmonite premium com acabamento branco acetinado. Composto por dois recipientes em formato de búzios e conchas marinhas, sendo um deles recheado com gel/cera em tom azul cristalino e detalhes marinhos de âncoras, leme e estrelas-do-mar. Perfeito para organizar joias ou decorar toucadores e casas de banho.";
        itemData.es.description = "Exclusivo conjunto marino artesanal moldeado en Jesmonite premium con acabado blanco satinado. Compuesto por dos recipientes en forma de búzios y conchas marinas, estando uno de ellos relleno con gel/cera en tono azul cristalino y detalles marinos de anclas, timón y estrellas de mar. Perfecto para organizar joyas o decorar tocadores y baños.";
        itemData.en.description = "Exclusive ocean-inspired handcrafted set molded from premium white Jesmonite featuring intricate seashell silhouettes. Includes a conch vessel and a crystal-blue gel sea dish embedded with miniature anchors, steering wheel, and starfish. Ideal for organizing jewelry or styling bathroom vanities.";
        itemData.fr.description = "Ensemble marin exclusif moulé à la main en Jesmonite premium blanc satiné. Composé de deux récipients en forme de coquillages et bucaz, dont un incrusté de gel bleu azur avec ancres, gouvernail et étoiles de mer miniatures. Idéal pour organiser vos bijoux ou sublimer votre salle de bain.";
        itemData.pt.aromaProfile = "Jesmonite Premium, Conchas Marinhas, Azul Marês, Artesanal";
        itemData.es.aromaProfile = "Jesmonite Premium, Conchas Marinas, Azul Marês, Artesanal";
        itemData.en.aromaProfile = "Premium Jesmonite, Seashells, Ocean Blue, Handcrafted";
        itemData.fr.aromaProfile = "Jesmonite Premium, Coquillages, Bleu Lagon, Artisanal";
    } else if (i === 2) {
        itemData.pt.description = "Encantador conjunto decorativo artesanal moldado em Jesmonite premium num elegante estilo étnico-praiano. Composto por um vaso/recipiente em terracota com padrões tribais gravados a branco e pés esculpidos, acompanhado por uma elegante bandeja oval canelada em tom branco puro. Uma peça inspirada nas areias e na essência do Verão, perfeita para plantas, velas ou organização de toucador.";
        itemData.es.description = "Encantador conjunto decorativo artesanal moldeado en Jesmonite premium en un elegante estilo étnico playero. Compuesto por un recipiente/maceta en terracota con patrones tribales grabados en blanco y patas esculpidas, acompañado por una elegante bandeja ovalada acanalada en tono blanco puro. Una pieza inspirada en las arenas y en la esencia del Verano, perfecta para plantas, velas o para la organización del tocador.";
        itemData.en.description = "Charming handcrafted decorative duo molded from premium Jesmonite featuring a coastal ethnic vibe. Includes a terracotta footed planter with engraved white tribal motifs paired with a crisp white ribbed oval tray. Inspired by warm sandy shores and summer aesthetic.";
        itemData.fr.description = "Ravissant duo décoratif artisanal moulé en Jesmonite premium au style ethnique balnéaire. Composé d'un pot sur pieds en terre cuite aux motifs tribaux gravés en blanc, accompagné d'un plateau ovale ondulé blanc pur. Inspiré par la douceur des sables et l'été.";
        itemData.pt.aromaProfile = "Jesmonite Premium, Terracota & Branco, Estilo Étnico, Artesanal";
        itemData.es.aromaProfile = "Jesmonite Premium, Terracota y Blanco, Estilo Étnico, Artesanal";
        itemData.en.aromaProfile = "Premium Jesmonite, Terracotta & White, Ethnic Vibe, Handcrafted";
        itemData.fr.aromaProfile = "Jesmonite Premium, Terre Cuite & Blanc, Style Ethnique, Artisanal";
    } else if (i === 3) {
        itemData.pt.description = "Vela aromática artesanal em formato de estrela-do-mar moldada em Jesmonite premium com bordas douradas elegantes e interior decorado com gel/cera em tom azul oceânico, conchas naturais e pérolas. Um encanto marinho perfeito para iluminação e decoração de verão.";
        itemData.es.description = "Vela aromática artesanal en forma de estrella de mar moldeada en Jesmonite premium con bordes dorados elegantes e interior decorado con gel/cera en tono azul oceánico, conchas naturales y perlas. Un encanto marino perfecto para iluminación y decoración de verano.";
        itemData.en.description = "Handcrafted starfish-shaped scented candle molded from premium Jesmonite with elegant gold rim detailing and a crystal-blue gel wax core embedded with natural seashells and pearls. Ideal for summer ambiance and coastal decor.";
        itemData.fr.description = "Bougie parfumée artisanale en forme d'étoile de mer moulée en Jesmonite premium avec liseré doré élégant, garnie de gel/cire bleu océan, coquillages naturels et perles. Parfaite pour créer une ambiance marine enchanteresse.";
        itemData.pt.aromaProfile = "Jesmonite Premium, Estrela do Mar, Detalhes Dourados, Azul Oceano";
        itemData.es.aromaProfile = "Jesmonite Premium, Estrella de Mar, Detalles Dorados, Azul Océano";
        itemData.en.aromaProfile = "Premium Jesmonite, Starfish, Gold Edges, Ocean Blue";
        itemData.fr.aromaProfile = "Jesmonite Premium, Étoile de Mer, Bordure Dorée, Bleu Océan";
    } else if (i === 4) {
        itemData.pt.description = "Delicada bandeja decorativa em formato de concha marinha esculpida artesanalmente em gesso ecológico premium com acabamento branco acetinado impermeabilizado. Perfeita para organizar anéis, pequenos acessórios de joalharia ou decorar lavabos e toucadores com elegância marinha.";
        itemData.es.description = "Delicada bandeja decorativa en forma de concha marina esculpida artesanalmente en yeso ecológico premium con acabado blanco satinado impermeabilizado. Perfecta para organizar anillos, pequeños accesorios de joyería o decorar tocadores y baños con elegancia marina.";
        itemData.en.description = "Delicate seashell-shaped trinket dish handcrafted from premium eco-friendly plaster with a smooth white waterproof finish. Ideal for storing rings, small jewelry pieces, or adding a charming coastal touch to your vanity.";
        itemData.fr.description = "Vide-poche décoratif délicat en forme de coquillage sculpté à la main en plâtre écologique premium avec finition blanc satiné imperméabilisée. Parfait pour ranger bagues, petits bijoux ou sublimer votre coiffeuse.";
        itemData.pt.aromaProfile = "Gesso Ecológico, Concha do Mar, Branco Acetinado, Artesanal";
        itemData.es.aromaProfile = "Yeso Ecológico, Concha de Mar, Blanco Satinado, Artesanal";
        itemData.en.aromaProfile = "Eco Plaster, Seashell Dish, Satin White, Handcrafted";
        itemData.fr.aromaProfile = "Plâtre Écologique, Coquillage, Blanc Satiné, Artisanal";
    } else if (i === 5) {
        itemData.pt.description = "Graciosa peça decorativa em formato de estrela-do-mar esculpida artesanalmente em gesso ecológico premium com textura exterior realista e acabamento branco acetinado impermeabilizado. Ideal para apoiar joias, pequenos pertences ou servir como suporte decorativo para toucadores e mesas.";
        itemData.es.description = "Graciosa pieza decorativa en forma de estrella de mar esculpida artesanalmente en yeso ecológico premium con textura exterior realista y acabado blanco satinado impermeabilizado. Ideal para apoyar joyas, pequeños objetos o servir como soporte decorativo para tocadores y mesas.";
        itemData.en.description = "Charming starfish-shaped decorative holder handcrafted from premium eco-friendly plaster featuring a realistic textured exterior and smooth white waterproof finish. Perfect for holding jewelry or adding a coastal accent to your home.";
        itemData.fr.description = "Raffiné vide-poche en forme d'étoile de mer sculpté à la main en plâtre écologique premium avec texture extérieure réaliste et finition blanc satiné. Parfait pour vos bijoux ou pour agrémenter votre décoration estivale.";
        itemData.pt.aromaProfile = "Gesso Ecológico, Estrela da Marê, Branco Acetinado, Artesanal";
        itemData.es.aromaProfile = "Yeso Ecológico, Estrela da Marê, Blanco Satinado, Artesanal";
        itemData.en.aromaProfile = "Eco Plaster, Starfish Dish, Satin White, Handcrafted";
        itemData.fr.aromaProfile = "Plâtre Écologique, Étoile de Mer, Blanc Satiné, Artisanal";
    } else if (i === 6) {
        itemData.pt.description = "Encantador recipiente artesanal em formato de búzios moldado em Jesmonite premium com acabamento branco acetinado. O seu interior acolhe uma delicada camada de gel/cera em tom azul cristalino, incrustada com detalhes náuticos de âncoras, leme, mini conchas e pérolas. Uma peça oceânica e inspiradora para decorar toucadores, casas de banho e estantes com a serenidade do mar.";
        itemData.es.description = "Encantador recipiente artesanal en forma de caracola marina moldeado en Jesmonite premium con acabado blanco satinado. Su interior alberga una delicada capa de gel/cera en tono azul cristalino, incrustada con detalles náuticos de anclas, timón, mini conchas y perlas. Una pieza oceánica e inspiradora para decorar tocadores, baños y estanterías con la serenidad del mar.";
        itemData.en.description = "Charming conch shell vessel handcrafted from premium white Jesmonite. Filled with a translucent ocean-blue gel/wax layer embedded with miniature nautical helm, anchor, sea pearls, and tiny starfish. A beautiful coastal decor accent designed to bring sea tranquility into your space.";
        itemData.fr.description = "Magnifique coquillage artisanal sculpté en Jesmonite premium blanc satiné. L'intérieur révèle une couche translucide de gel/cire bleu lagon incrustée d'ancres, gouvernail, mini coquillages et perles marines. Une pièce idéale pour ajouter une touche océanique à votre intérieur.";
        itemData.pt.aromaProfile = "Jesmonite Premium, Búzio da Marê, Detalhes Náuticos, Azul Marês";
        itemData.es.aromaProfile = "Jesmonite Premium, Búzio da Marê, Detalles Náuticos, Azul Marês";
        itemData.en.aromaProfile = "Premium Jesmonite, Conch Shell, Nautical Details, Ocean Blue";
        itemData.fr.aromaProfile = "Jesmonite Premium, Coquillage, Détails Nautiques, Bleu Lagon";
    } else if (i === 7) {
        itemData.pt.description = "Encantadora vela aromática artesanal vertida numa delicada concha marinha em gesso ecológico branco. Elaborada com cera de soja 100% natural, decorada com requintadas pérolas brancas e mini conchas naturais ao longo do bordo. Uma peça delicada que ilumina, decora e perfuma qualquer espaço com uma atmosfera praiana elegante.";
        itemData.es.description = "Encantadora vela aromática artesanal vertida en una delicada concha marina en yeso ecológico blanco. Elaborada con cera de soja 100% natural, decorada con exquisitas perlas blancas y mini conchas naturales a lo largo del borde. Una pieza delicada que ilumina, decora y perfuma cualquier espacio con una atmósfera playera elegante.";
        itemData.en.description = "Charming handcrafted scented candle poured into a white eco-friendly plaster seashell dish. Made with 100% natural soy wax and adorned with white pearls and mini seashells along the rim. Perfect for adding delicate coastal light and aroma to your home.";
        itemData.fr.description = "Raffinée bougie parfumée artisanale moulée dans un élégant coquillage blanc en plâtre écologique. Conçue en cire de soja 100% naturelle et agrémentée de perles blanches et mini coquillages naturels sur le contour. Idéale pour apporter une lumière douce et une ambiance marine.";
        itemData.pt.aromaProfile = "Cera de Soja 100% Natural, Gesso Ecológico, Pérolas, Concha do Mar";
        itemData.es.aromaProfile = "Cera de Soja 100% Natural, Yeso Ecológico, Perlas, Concha de Mar";
        itemData.en.aromaProfile = "100% Natural Soy Wax, Eco Plaster, White Pearls, Seashell";
        itemData.fr.aromaProfile = "Cire de Soja 100% Naturelle, Plâtre Écologique, Perles, Coquillage";
    } else if (i === 8) {
        itemData.pt.description = "Elegante saboneteira e bandeja decorativa oval com rebordo canelado, esculpida artesanalmente em gesso ecológico premium com acabamento impermeabilizado. Perfeita para apoiar sabonetes artesanais, organizar joias ou complementar a decoração da casa de banho com sofisticação.";
        itemData.es.description = "Elegante jabonera y bandeja decorativa ovalada con borde acanalado, esculpida artesanalmente en yeso ecológico premium con acabado impermeabilizado. Perfecta para apoyar jabones artesanales, organizar joyas o complementar la decoración del baño con sofisticación.";
        itemData.en.description = "Elegant oval soap dish and decorative trinket tray featuring a scalloped ribbed rim, handcrafted from premium eco-friendly plaster with a sealed waterproof finish. Ideal for artisanal soap bars or organizing small bathroom accents.";
        itemData.fr.description = "Élégant porte-savon et plateau décoratif ovale à bord ondulé, sculpté à la main en plâtre écologique premium avec finition imperméabilisée. Parfait pour vos savons artisanaux ou pour organiser vos petits accessoires de salle de bain.";
        itemData.pt.aromaProfile = "Gesso Ecológico, Saboneteira, Branco Puro, Artesanal";
        itemData.es.aromaProfile = "Yeso Ecológico, Jabonera, Blanco Puro, Artesanal";
        itemData.en.aromaProfile = "Eco Plaster, Soap Dish, Pure White, Handcrafted";
        itemData.fr.aromaProfile = "Plâtre Écologique, Porte-Savon, Blanc Pur, Artisanal";
    } else if (i === 9) {
        itemData.pt.description = "Espetacular vela aromática artesanal em formato de estrela-do-mar moldada em Jesmonite premium com requintado acabamento de bordas douradas. Vertida com cera em gel marinho transparente em tom azul cristalino, decorada com conchas naturais, pérolas e pavio de madeira. Uma obra de arte decorativa que transmite o charme e a magia do oceano.";
        itemData.es.description = "Espectacular vela aromática artesanal en forma de estrella de mar moldeada en Jesmonite premium con exquisito acabado de bordes dorados. Vertida con cera en gel marino transparente en tono azul cristalino, decorada con conchas naturales, perlas y mecha de madera. Una obra de arte decorativa que transmite el encanto y la magia del océano.";
        itemData.en.description = "Stunning handcrafted scented candle molded in a starfish Jesmonite vessel with elegant gold rim detailing. Poured with crystal-clear blue gel wax and adorned with natural seashells, sea pearls, and a crackling wooden wick. A coastal masterpiece designed to bring sea magic to your room.";
        itemData.fr.description = "Spectaculaire bougie parfumée en gel translucide bleu azur coulée dans un récipient en forme d'étoile de mer en Jesmonite premium rehaussé de bordures dorées. Agrémentée de coquillages naturels, perles et mèche en bois.";
        itemData.pt.aromaProfile = "Cera em Gel Marinho, Jesmonite Premium, Estrela da Marê, Pavio de Madeira";
        itemData.es.aromaProfile = "Cera en Gel Marino, Jesmonite Premium, Estrela da Marê, Mecha de Madera";
        itemData.en.aromaProfile = "Marine Gel Wax, Premium Jesmonite, Starfish, Wooden Wick";
        itemData.fr.aromaProfile = "Cire en Gel Marine, Jesmonite Premium, Étoile de Mer, Mèche en Bois";
    } else if (i === 10) {
        itemData.pt.description = "Majestoso recipiente decorativo em formato de búzios e concha marinha, esculpido artesanalmente em gesso ecológico premium com textura escultural realista e acabamento branco acetinado impermeabilizado. Perfeito para servir como organizador de joias, porta-objetos de toucador ou destaque elegante na decoração de verão.";
        itemData.es.description = "Majestoso recipiente decorativo en forma de caracola marina, esculpido artesanalmente en yeso ecológico premium con textura escultural realista y acabado blanco satinado impermeabilizado. Perfecto para servir como organizador de joyas, vaciabolsillos de tocador o destacar con elegancia en la decoración de verano.";
        itemData.en.description = "Majestic conch shell decorative holder handcrafted from premium white eco-friendly plaster featuring detailed realistic textures and a waterproof satin seal. Ideal as a jewelry tray, trinket holder, or elegant coastal decorative accent.";
        itemData.fr.description = "Majestueux récipient décoratif en forme de coquillage sculpté à la main en plâtre écologique premium avec texture réaliste et finition blanc satiné imperméabilisée. Parfait pour vos bijoux ou comme objet de décoration balnéaire.";
        itemData.pt.aromaProfile = "Gesso Ecológico, Búzio Maresia, Branco Acetinado, Artesanal";
        itemData.es.aromaProfile = "Yeso Ecológico, Búzio Maresia, Blanco Satinado, Artesanal";
        itemData.en.aromaProfile = "Eco Plaster, Conch Shell, Satin White, Handcrafted";
        itemData.fr.aromaProfile = "Plâtre Écologique, Coquillage, Blanc Satiné, Artisanal";
    } else if (i === 11) {
        itemData.pt.description = "Elegante vaso e taça decorativa circular esculpida artesanalmente em gesso ecológico premium numa calorosa tonalidade alaranjada inspirada nas cores radiantes do pôr do sol. Com acabamento impermeabilizado e linhas suaves, é ideal para apoiar pequenos objetos, potes-pourris, velas ou servir como um ponto focal acolhedor na decoração do lar.";
        itemData.es.description = "Elegante cuenco y vaso decorativo circular esculpido artesanalmente en yeso ecológico premium en una cálida tonalidad anaranjada inspirada en los colores radiantes del atardecer. Con acabado impermeabilizado y líneas suaves, es ideal para apoyar pequeños objetos, potpourris, velas o servir como un punto focal acogedor en la decoración del hogar.";
        itemData.en.description = "Elegant circular decorative bowl handcrafted from premium eco-friendly plaster in a warm sunset orange shade. Sealed with a smooth waterproof finish, this piece brings the golden warmth of summer sunsets to your table or vanity decor.";
        itemData.fr.description = "Élégante coupe décorative circulaire sculptée à la main en plâtre écologique premium dans une nuance orangée chaleureuse rappelant les teintes dorées du coucher de soleil. Idéale pour exposer de petits objets ou sublimer votre décoration.";
        itemData.pt.aromaProfile = "Gesso Ecológico, Vaso Pôr do Sol, Tom Alaranjado, Artesanal";
        itemData.es.aromaProfile = "Yeso Ecológico, Vaso Pôr do Sol, Tono Anaranjado, Artesanal";
        itemData.en.aromaProfile = "Eco Plaster, Sunset Bowl, Warm Orange, Handcrafted";
        itemData.fr.aromaProfile = "Plâtre Écologique, Coupe Coucher de Soleil, Orange Chaleureux, Artisanal";
    } else if (i === 12) {
        itemData.pt.description = "Espetacular vaso e taça decorativa circular esculpida artesanalmente em gesso ecológico premium com um deslumbrante efeito marmoreado de ondas em tons de azul marinho sobre base branca acetinada. Com acabamento impermeabilizado e toque suave, evoca o movimento fluido do mar e acrescenta uma elegância contemporânea a qualquer mesa, aparador ou toucador.";
        itemData.es.description = "Espectacular cuenco y vaso decorativo circular esculpido artesanalmente en yeso ecológico premium con un deslumbrante efecto marmoleado de olas en tonos de azul marino sobre base blanca satinada. Com acabamento impermeabilizado e toque suave, evoca o movimento fluido do mar e acrescenta uma elegância contemporânea a qualquer mesa, aparador ou toucador.";
        itemData.pt.aromaProfile = "Gesso Ecológico, Vaso Wave, Mármore Azul Oceano, Artesanal";
        itemData.es.aromaProfile = "Yeso Ecológico, Vaso Wave, Mármol Azul Océano, Artesanal";
        itemData.en.aromaProfile = "Eco Plaster, Wave Bowl, Ocean Blue Marble, Handcrafted";
        itemData.fr.aromaProfile = "Plâtre Écologique, Coupe Wave, Marbré Bleu Lagon, Artisanal";
    }

    if (item.category === "sabonete") {
        SOAP_GALLERY.push(itemData);
    } else {
        PRODUCTS.push(itemData);
    }
}

const RECORDACAO_NAMES = [
    { pt: "Gift Box Love", es: "Gift Box Love", en: "Gift Box Love", fr: "Gift Box Love", price: 24.90 }
];

for (let i = 1; i <= RECORDACAO_NAMES.length; i++) {
    const rec = RECORDACAO_NAMES[i - 1];
    const recData = {
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
    };

    if (i === 1) {
        recData.pt.description = "Exclusivo e romântico caixote em formato de coração 'Gift Box Love', preparado artesanalmente para celebrar o amor. Recheado com rosas aveludadas vermelhas, deliciosos bombons Ferrero Rocher dourados, um adorável ursinho branco e um topo decorativo especial 'Happy Valentine's Day'. O presente perfeito para surpreender quem mais ama em aniversários, Dia dos Namorados ou momentos inesquecíveis.";
        recData.es.description = "Exclusiva y romántica caja en forma de corazón 'Gift Box Love', preparada artesanalmente para celebrar el amor. Rellena con rosas aterciopeladas rojas, deliciosos bombones Ferrero Rocher dorados, un adorable osito blanco y un topper decorativo especial 'Happy Valentine's Day'. El regalo perfecto para sorprender a quien más amas en aniversarios, San Valentín o momentos inolvidables.";
        recData.en.description = "Exclusive romantic heart-shaped 'Gift Box Love' gift box handcrafted to celebrate love. Filled with velvety red roses, decadent golden Ferrero Rocher chocolates, a cute white plush bear, and a decorative 'Happy Valentine's Day' topper. The ultimate romantic surprise for anniversaries, Valentine's Day, or special moments.";
        recData.fr.description = "Coffret romantique exclusif en forme de cœur 'Gift Box Love' confectionné à la main avec amour. Garni de roses rouges veloutées, de délicieux chocolats dorés Ferrero Rocher, d'un adorable petit ours blanc et d'un topper décoratif 'Happy Valentine's Day'. Le cadeau parfait pour surprendre votre être cher.";
        recData.pt.aromaProfile = "Edição Especial Amor, Ferrero Rocher, Rosas Vermelhas, Ursinho";
        recData.es.aromaProfile = "Edición Especial Amor, Ferrero Rocher, Rosas Rojas, Osito";
        recData.en.aromaProfile = "Special Love Edition, Ferrero Rocher, Red Roses, Teddy Bear";
        recData.fr.aromaProfile = "Édition Spéciale Amour, Ferrero Rocher, Roses Rouges, Ourson";
    }

    PRODUCTS.push(recData);
}


PRODUCTS.push({
    id: "wax-melt-1",
    category: "vela",
    price: 6.90,
    image: "assets/wax_melt_1.jpeg",
    qty: 1,
    pt: {
        name: "Wax Melts de Soja Aromáticos",
        categoryLabel: "Cera de Soja / Ambientador",
        aromaBrief: "Wax melts de soja natural e essências para queimadores.",
        description: "Fundidos à mão com cera de soja natural e essências premium. Perfeitos para libertar fragrâncias intensas e contínuas quando derretidos num queimador de essências. Uma alternativa ecológica e prática para perfumar a sua casa.",
        aromaProfile: "Fragrância Intensa, Cera de Soja, Prático"
    },
    es: {
        name: "Wax Melts de Soja Aromáticos",
        categoryLabel: "Cera de Soja / Ambientador",
        aromaBrief: "Wax melts de soja natural y esencias para quemadores.",
        description: "Fundidos a mano con cera de soja natural y esencias premium. Perfectos para liberar fragancias intensas y continuas cuando se derriten en un quemador de esencias. Una alternativa ecológica y práctica para perfumar tu hogar.",
        aromaProfile: "Fragancia Intensa, Cera de Soja, Práctico"
    },
    en: {
        name: "Aromatic Melts",
        categoryLabel: "Soy Wax / Home Fragrance",
        aromaBrief: "Natural soy wax melts and fragrance essences for burners.",
        description: "Hand-poured with natural soy wax and premium fragrance essences. Perfect for releasing intense, continuous scents when melted in a fragrance burner. An eco-friendly and practical alternative to scent your home.",
        aromaProfile: "Intense Scent, Soy Wax, Practical"
    },
    fr: {
        name: "Fondants de Cire de Soja Parfumés",
        categoryLabel: "Cire de Soja / Parfum de Maison",
        aromaBrief: "Fondants de cire de soja naturelle et essences parfumées pour brûleurs.",
        description: "Fabriqués à la main avec de la cire de soja naturelle et des essences parfumées de qualité. Parfaits pour diffuser des parfums intenses et continus une fois fondus dans un brûle-parfum. Une alternative écologique et pratique.",
        aromaProfile: "Parfum Intense, Cire de Soja, Pratique"
    }
});

PRODUCTS.push({
    id: "candle-special-1",
    category: "vela",
    price: 9.90,
    image: "assets/candle_special_1.jpeg",
    qty: 1,
    pt: {
        name: "Vela Santa",
        categoryLabel: "Vela Escultural Decorativa",
        aromaBrief: "Vela artesanal escultural de Nossa Senhora com detalhes dourados e flores secas.",
        description: "Majestosa e devota vela artesanal escultural 'Vela Santa', moldada à mão em cera de soja ecológica em forma da imagem sagrada de Nossa Senhora com coroa e detalhes pintados à mão a ouro. Assenta sobre uma elegante base canelada em gesso ecológico rodeada por delicadas flores secas brancas (gipsófilas). Uma peça cheia de fé, paz e serenidade para abençoar o seu lar ou oferecer como lembrança especial.",
        aromaProfile: "Devoção, Cera de Soja, Detalhes a Ouro, Flores Secas"
    },
    es: {
        name: "Vela Santa",
        categoryLabel: "Vela Escultórica Decorativa",
        aromaBrief: "Vela artesanal escultórica de Nuestra Señora con detalles dorados y flores secas.",
        description: "Majestuosa y devota vela artesanal escultórica 'Vela Santa', moldeada a mano con cera de soja ecológica en forma de la sagrada figura de Nuestra Señora con corona y detalles pintados a mano en pan de oro. Reposa sobre una elegante base acanalada de yeso ecológico rodeada por delicadas flores secas blancas (gipsófilas). Una pieza llena de fe, paz y serenidad para bendecir tu hogar o regalar en fechas especiales.",
        aromaProfile: "Devoción, Cera de Soja, Detalles Dorados, Flores Secas"
    },
    en: {
        name: "Vela Santa",
        categoryLabel: "Decorative Sculptural Candle",
        aromaBrief: "Handcrafted Virgin Mary sculptural candle with gold accents and dried flowers.",
        description: "Exquisite and peaceful handcrafted sculptural 'Vela Santa' candle, hand-poured with eco-friendly soy wax in the sacred image of Our Lady wearing a crown with hand-painted gold mantle accents. Resting on a white scalloped eco-plaster dish surrounded by delicate white dried botanical flowers. A sacred piece of faith, peace, and serenity for your home or as a meaningful gift.",
        aromaProfile: "Devotion, Eco Soy Wax, Gold Accents, Dried Flowers"
    },
    fr: {
        name: "Vela Santa",
        categoryLabel: "Bougie Sculpturale Décorative",
        aromaBrief: "Bougie sculpturale artisanale de la Sainte Vierge avec détails dorés et fleurs séchées.",
        description: "Majestueuse bougie sculpturale artisanale 'Vela Santa' coulée à la main en cire de soja écologique à l'effigie de la Sainte Vierge couronnée avec détails peints à la main à la dorure. Présentée dans un élégant réceptacle en plâtre écologique bordé de délicates fleurs séchées blanches. Une pièce empreinte de foi, de sérénité et de bénédiction.",
        aromaProfile: "Dévotion, Cire de Soja, Touches Dorées, Fleurs Séchées"
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
        pt: "Velas, Sabonetes e Peças Decorativas",
        es: "Velas, Jabones y Piezas Decorativas",
        en: "Candles, Soaps and Decorative Pieces",
        fr: "Bougies, Savons et Pièces Décoratives"
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
        pt: "Bem-vindo à Com Cheiro de Amor, <br><span>onde não é apenas artesanato, mas sim a paixão e entrega do detalhe</span>",
        es: "Bienvenido a Com Cheiro de Amor, <br><span>donde no es solo artesanía, sino la pasión y entrega por el detalle</span>",
        en: "Welcome to Com Cheiro de Amor, <br><span>where it is not just craft, but the passion and dedication to detail</span>",
        fr: "Bienvenue chez Com Cheiro de Amor, <br><span>où ce n'est pas seulement de l'artisanat, mais la passion et le souci du détail</span>"
    },
    "hero-desc": {
        pt: "Não procuramos a perfeição, procuramos a entrega. Transforme o seu lar com a luz das nossas velas e aromas, onde cada peça se transforma num detalhe e cada sabonete oferece uma experiência única. Criados com alma, cuidado e carinho.",
        es: "No buscamos la perfección, buscamos la entrega. Transforma tu hogar con la luz de nuestras velas y aromas, donde cada pieza se convierte en un detalle y cada jabón ofrece una experiencia única. Creados con alma, cuidado y cariño.",
        en: "We don't seek perfection, we seek dedication. Transform your home with the light of our candles and scents, where each piece becomes a detail and every soap offers a unique experience. Crafted with soul, care, and devotion.",
        fr: "Nous ne cherchons pas la perfection, nous cherchons le dévouement. Transformez votre foyer avec la lumière de nos bougies et de nos parfums, où chaque pièce devient un détail et chaque savon offre une expérience unique. Créés avec âme, soin et tendresse."
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
        pt: "Buquês",
        es: "Buqués",
        en: "Bouquets",
        fr: "Bouquets"
    },
    "filter-decorativas": {
        pt: "Peças Decorativas",
        es: "Piezas Decorativas",
        en: "Decorative Pieces",
        fr: "Pièces Décoratives"
    },
    "filter-verao": {
        pt: "Coleção de Verão",
        es: "Colección de Verano",
        en: "Summer Collection",
        fr: "Collection d'Été"
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
        pt: "Conheça a nossa linha exclusiva de sabonetes botânicos e artesanais. Elaborados em pequenos lotes com essências selecionadas de alta qualidade, argilas purificantes e botânicos naturais para mimar a sua pele.",
        es: "Conozca nuestra línea exclusiva de jabones botánicos y artesanales. Elaborados en pequeños lotes con esencias seleccionadas de alta calidad, arcillas purificantes y botánicos naturales para mimar su piel.",
        en: "Discover our exclusive line of botanical and handcrafted soaps. Made in small batches with high-quality selected essences, purifying clays, and natural botanicals to pamper your skin.",
        fr: "Découvrez notre gamme exclusive de savons botaniques et artisanaux. Fabriqués en petits lots avec des essences sélectionnées de haute qualité, des argiles purifiantes et des plantes naturelles pour chouchouter votre peau."
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
        pt: 'A <strong>Com Cheiro de Amor</strong> nasceu do desejo de trazer mais luz, paz e bem-estar para o dia a dia das pessoas. Cada produto é idealizado e criado artesanalmente em pequenos lotes em Portugal. <br><br>Utilizamos cera de soja vegetal ecológica e essências de fragrância premium para as nossas velas, garantindo uma queima limpa, duradoura e respeitadora do ambiente. Os nossos sabonetes são elaborados com manteigas vegetais hidratantes e ingredientes botânicos que nutrem e perfumam a pele de forma natural.',
        es: '<strong>Com Cheiro de Amor</strong> nació del deseo de traer más luz, paz y bienestar al día a día de las personas. Cada producto es idealizado y creado artesanalmente en pequeños lotes en Portugal. <br><br>Utilizamos cera de soja vegetal ecológica y esencias de fragancia premium para nuestras velas, garantizando una combustión limpia, duradera y respetuosa con el medio ambiente. Nuestros jabones se elaboran con mantecas vegetales hidratantes e ingredientes botánicos que nutren y perfuman la piel de forma natural.',
        en: '<strong>Com Cheiro de Amor</strong> was born from the desire to bring more light, peace, and well-being into people\'s daily lives. Each product is conceptualized and handcrafted in small batches in Portugal. <br><br>We use ecological vegetable soy wax and premium fragrance oils for our candles, ensuring a clean, long-lasting, and environmentally friendly burn. Our soaps are formulated with moisturizing plant butters and botanical ingredients that naturally nourish and perfume the skin.',
        fr: '<strong>Com Cheiro de Amor</strong> est né du désir d\'apporter plus de lumière, de paix et de bien-être dans le quotidien des gens. Chaque produit est imaginé et créé artisanalement en petits lots au Portugal. <br><br>Nous utilisons de la cire de soja végétale écologique et des essences parfumées de qualité supérieure pour nos bougies, garantissant une combustion propre, durable et respectueuse de l\'environnement. Nos savons sont élaborés avec des beurres végétaux hydratants et des ingrédients botaniques qui nourrissent et parfument la peau de manière naturelle.'
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
    const modalAddToCartBtn = document.getElementById("btn-modal-add-to-cart") || document.querySelector(".modal-wrapper .btn-primary");

    // Dynamic state variables for modal
    let activeModalProductId = null;
    let activeModalQty = 1;

    // Helper function to resolve active filtered products including soaps
    const getFilteredProducts = (category) => {
        if (category === "sabonete") {
            return SOAP_GALLERY;
        } else if (category === "all") {
            return PRODUCTS;
        } else if (category === "verao") {
            return PRODUCTS.filter(p => p.id.startsWith("verao-"));
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
        } else if (categoryFilter === "verao") {
            filteredProducts = PRODUCTS.filter(p => p.id.startsWith("verao-"));
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
        if (aromaNotes) aromaNotes.textContent = translation.aromaProfile;
        
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
        if (aromaNotes) aromaNotes.textContent = translation.aromaProfile || "Natural, Hidratante, Botânico";
        
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
        renderCart();
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


console.log("=== PRODUCTS category='vaso' ===");
PRODUCTS.forEach((p, idx) => {
    if (p.category === 'vaso') {
        console.log(`[PRODUCTS ${idx}] ID=${p.id} | Name=${p.pt ? p.pt.name : 'N/A'}`);
    }
});

console.log("=== PRODUCTS containing 'vaso' or 'Vaso' in ID or name ===");
PRODUCTS.forEach((p, idx) => {
    const ptName = p.pt ? p.pt.name : '';
    const catLabel = p.pt ? p.pt.categoryLabel : '';
    const desc = p.pt ? p.pt.description : '';
    if (p.id.includes('vaso') || ptName.toLowerCase().includes('vaso') || catLabel.toLowerCase().includes('vaso') || desc.toLowerCase().includes('vaso')) {
        console.log(`[PRODUCTS ${idx}] ID=${p.id} | Current Category=${p.category} | Name=${ptName} | CatLabel=${catLabel}`);
    }
});