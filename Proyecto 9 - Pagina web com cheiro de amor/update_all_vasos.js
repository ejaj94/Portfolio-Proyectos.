const fs = require('fs');

let content = fs.readFileSync('app.js', 'utf8');

const pt_desc = "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.";
const pt_brief = "Vela aromática elegante e decorativa. Cores, modelos e aromas totalmente à escolha do cliente.";
const pt_prof = "Personalizável, Aroma Suave, Decorativo";

const es_desc = "Vela aromática elegante con un suave aroma que sirve también como decoración para tu hogar. Totalmente personalizable: los colores, modelos y aromas son a elección del cliente.";
const es_brief = "Vela aromática elegante y decorativa. Colores, modelos y aromas a elección del cliente.";
const es_prof = "Personalizable, Aroma Suave, Decorativo";

const en_desc = "Elegant scented candle with a subtle fragrance that also serves as beautiful home decor. Fully customizable: colors, models, and scents are selected at the customer's choice.";
const en_brief = "Elegant and decorative scented candle. Colors, models, and scents customizable at customer's choice.";
const en_prof = "Customizable, Gentle Scent, Decorative";

const fr_desc = "Bougie parfumée élégante au doux parfum qui sert également de décoration pour votre intérieur. Entièrement personnalisable : les couleurs, modèles et parfums sont au choix du client.";
const fr_brief = "Bougie parfumée élégante et décorative. Couleurs, modèles et parfums personnalisables au choix du client.";
const fr_prof = "Personnalisable, Parfum Doux, Décoratif";

const startIdx = content.indexOf('id: "candle-vela_en_vaso-1"');
const endIdx = content.indexOf('id: "candle-vela_en_vaso-5"');

if (startIdx !== -1 && endIdx !== -1) {
    const blockStart = content.lastIndexOf('{', startIdx);
    const nextBlock = content.indexOf('},', endIdx) + 2;

    const newVasoBlock = `{
        id: "candle-vela_en_vaso-1",
        category: "vela-vaso",
        price: 19.90,
        image: "assets/candle_vela_en_vaso_1.jpeg",
        qty: 1,
        pt: {
            name: "Vela Floral em Vaso",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${pt_brief}",
            description: "${pt_desc}",
            aromaProfile: "${pt_prof}"
        },
        es: {
            name: "Vela Floral en Vaso",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${es_brief}",
            description: "${es_desc}",
            aromaProfile: "${es_prof}"
        },
        en: {
            name: "Floral Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "${en_brief}",
            description: "${en_desc}",
            aromaProfile: "${en_prof}"
        },
        fr: {
            name: "Bougie Florale en Pot",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "${fr_brief}",
            description: "${fr_desc}",
            aromaProfile: "${fr_prof}"
        }
    },
    {
        id: "candle-vela_en_vaso-2",
        category: "vela-vaso",
        price: 19.90,
        image: "assets/candle_vela_en_vaso_2.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Camomila e Flor de Laranja",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${pt_brief}",
            description: "${pt_desc}",
            aromaProfile: "${pt_prof}"
        },
        es: {
            name: "Vela en Vaso Manzanilla y Flor de Naranja",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${es_brief}",
            description: "${es_desc}",
            aromaProfile: "${es_prof}"
        },
        en: {
            name: "Chamomile & Orange Blossom Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "${en_brief}",
            description: "${en_desc}",
            aromaProfile: "${en_prof}"
        },
        fr: {
            name: "Bougie en Pot Camomille & Fleur d'Oranger",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "${fr_brief}",
            description: "${fr_desc}",
            aromaProfile: "${fr_prof}"
        }
    },
    {
        id: "candle-vela_en_vaso-3",
        category: "vela-vaso",
        price: 19.90,
        image: "assets/candle_vela_en_vaso_3.jpeg",
        qty: 1,
        pt: {
            name: "Vela Floral em Vaso Âmbar",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${pt_brief}",
            description: "${pt_desc}",
            aromaProfile: "${pt_prof}"
        },
        es: {
            name: "Vela Floral en Vaso Ámbar",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${es_brief}",
            description: "${es_desc}",
            aromaProfile: "${es_prof}"
        },
        en: {
            name: "Amber Floral Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "${en_brief}",
            description: "${en_desc}",
            aromaProfile: "${en_prof}"
        },
        fr: {
            name: "Bougie Florale en Pot Ambre",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "${fr_brief}",
            description: "${fr_desc}",
            aromaProfile: "${fr_prof}"
        }
    },
    {
        id: "candle-vela_en_vaso-4",
        category: "vela-vaso",
        price: 19.90,
        image: "assets/candle_vela_en_vaso_4.jpeg",
        qty: 1,
        pt: {
            name: "Vela Tília em Vaso",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${pt_brief}",
            description: "${pt_desc}",
            aromaProfile: "${pt_prof}"
        },
        es: {
            name: "Vela Tília en Vaso",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${es_brief}",
            description: "${es_desc}",
            aromaProfile: "${es_prof}"
        },
        en: {
            name: "Tília Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "${en_brief}",
            description: "${en_desc}",
            aromaProfile: "${en_prof}"
        },
        fr: {
            name: "Bougie en Pot Tília",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "${fr_brief}",
            description: "${fr_desc}",
            aromaProfile: "${fr_prof}"
        }
    },
    {
        id: "candle-vela_en_vaso-5",
        category: "vela-vaso",
        price: 19.90,
        image: "assets/candle_vela_en_vaso_5.jpeg",
        qty: 1,
        pt: {
            name: "Vela em Vaso Flor de Algodão",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${pt_brief}",
            description: "${pt_desc}",
            aromaProfile: "${pt_prof}"
        },
        es: {
            name: "Vela en Vaso Flor de Algodón",
            categoryLabel: "Vela Aromática",
            aromaBrief: "${es_brief}",
            description: "${es_desc}",
            aromaProfile: "${es_prof}"
        },
        en: {
            name: "Cotton Flower Jar Candle",
            categoryLabel: "Scented Candle",
            aromaBrief: "${en_brief}",
            description: "${en_desc}",
            aromaProfile: "${en_prof}"
        },
        fr: {
            name: "Bougie en Pot Fleur de Coton",
            categoryLabel: "Bougie Parfumée",
            aromaBrief: "${fr_brief}",
            description: "${fr_desc}",
            aromaProfile: "${fr_prof}"
        }
    },`;

    content = content.substring(0, blockStart) + newVasoBlock + content.substring(nextBlock);
    console.log("Replaced candle-vela_en_vaso 1-5 successfully!");
}

// 2. Also update NEW_CATALOG_ITEMS items in category vela-vaso
const newCatUpdates = [
    { id: 'cat-new-4', ptName: 'Vela Oceano Infinito', esName: 'Vela Océano Infinito', enName: 'Infinite Ocean Candle', frName: 'Bougie Océan Infini' },
    { id: 'cat-new-16', ptName: 'Bowl Jardim de Rosas', esName: 'Bowl Jardín de Rosas', enName: 'Rose Garden Bowl', frName: 'Bol Jardin de Roses' },
    { id: 'cat-new-19', ptName: 'Vaso Menina Tulipa', esName: 'Jarrón Niña Tulipán', enName: 'Tulip Girl Vase', frName: 'Vase Fille Tulipe' },
    { id: 'cat-new-20', ptName: 'Vaso Decorativo', esName: 'Jarrón Decorativo', enName: 'Decorative Vase', frName: 'Vase Décoratif' }
];

newCatUpdates.forEach(item => {
    const itemRegex = new RegExp(`{\\s*id:\\s*'${item.id}'[\\s\\S]*?}`);
    if (itemRegex.test(content)) {
        let img = 'assets/vela_oceano_redonda.jpg?v=2';
        let price = 29.90;
        if (item.id === 'cat-new-16') {
            img = 'assets/vela_bowl_rosas.jpg?v=2';
            price = 28.90;
        } else if (item.id === 'cat-new-19') {
            img = 'assets/vela_menina_tulipa.jpg';
            price = 29.90;
        } else if (item.id === 'cat-new-20') {
            img = 'assets/vela_extra.jpg';
            price = 29.90;
        }
        const replacement = `{ id: '${item.id}', category: 'vela-vaso', price: ${price}, image: '${img}', pt: { name: '${item.ptName}', desc: '${pt_desc}' }, es: { name: '${item.esName}', desc: '${es_desc}' }, en: { name: '${item.enName}', desc: '${en_desc}' }, fr: { name: '${item.frName}', desc: '${fr_desc}' } }`;
        content = content.replace(itemRegex, replacement);
    }
});

fs.writeFileSync('app.js', content, 'utf8');
console.log("All vaso candles updated successfully!");
