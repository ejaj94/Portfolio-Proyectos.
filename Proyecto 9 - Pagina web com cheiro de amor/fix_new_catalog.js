const fs = require('fs');

let content = fs.readFileSync('app.js', 'utf8');

const pt_desc = "Vela aromática elegante com aroma suave que serve também como decoração para o seu lar. Totalmente personalizável: as cores, modelos e aromas são à escolha do cliente.";
const es_desc = "Vela aromática elegante con un suave aroma que sirve también como decoración para tu hogar. Totalmente personalizable: los colores, modelos y aromas son a elección del cliente.";
const en_desc = "Elegant scented candle with a subtle fragrance that also serves as beautiful home decor. Fully customizable: colors, models, and scents are selected at the customer\\'s choice.";
const fr_desc = "Bougie parfumée élégante au doux parfum qui sert également de décoration pour votre intérieur. Entièrement personnalisable : les couleurs, modèles et parfums sont au choix du client.";

// Rewrite cat-new-4, 16, 19, 20 cleanly without quote breaking
content = content.replace(/{\s*id:\s*'cat-new-4'[\s\S]*?}, es: {[\s\S]*?}, fr: {[\s\S]*?}\s*}/, `{ id: 'cat-new-4', category: 'vela-vaso', price: 29.90, image: 'assets/vela_oceano_redonda.jpg?v=2', pt: { name: 'Vela Oceano Infinito', desc: '${pt_desc.replace(/'/g, "\\'")}' }, es: { name: 'Vela Océano Infinito', desc: '${es_desc.replace(/'/g, "\\'")}' }, en: { name: 'Infinite Ocean Candle', desc: "${en_desc}" }, fr: { name: 'Bougie Océan Infini', desc: "${fr_desc.replace(/'/g, "\\'")}" } }`);

content = content.replace(/{\s*id:\s*'cat-new-16'[\s\S]*?}, es: {[\s\S]*?}, fr: {[\s\S]*?}\s*}/, `{ id: 'cat-new-16', category: 'vela-vaso', price: 28.90, image: 'assets/vela_bowl_rosas.jpg?v=2', pt: { name: 'Bowl Jardim de Rosas', desc: '${pt_desc.replace(/'/g, "\\'")}' }, es: { name: 'Bowl Jardín de Rosas', desc: '${es_desc.replace(/'/g, "\\'")}' }, en: { name: 'Rose Garden Bowl', desc: "${en_desc}" }, fr: { name: 'Bol Jardin de Roses', desc: "${fr_desc.replace(/'/g, "\\'")}" } }`);

content = content.replace(/{\s*id:\s*'cat-new-19'[\s\S]*?}, es: {[\s\S]*?}, fr: {[\s\S]*?}\s*}/, `{ id: 'cat-new-19', category: 'vela-vaso', price: 29.90, image: 'assets/vela_menina_tulipa.jpg', pt: { name: 'Vaso Menina Tulipa', desc: '${pt_desc.replace(/'/g, "\\'")}' }, es: { name: 'Jarrón Niña Tulipán', desc: '${es_desc.replace(/'/g, "\\'")}' }, en: { name: 'Tulip Girl Vase', desc: "${en_desc}" }, fr: { name: 'Vase Fille Tulipe', desc: "${fr_desc.replace(/'/g, "\\'")}" } }`);

content = content.replace(/{\s*id:\s*'cat-new-20'[\s\S]*?}, es: {[\s\S]*?}, fr: {[\s\S]*?}\s*}/, `{ id: 'cat-new-20', category: 'vela-vaso', price: 29.90, image: 'assets/vela_extra.jpg', pt: { name: 'Vaso Decorativo', desc: '${pt_desc.replace(/'/g, "\\'")}' }, es: { name: 'Jarrón Decorativo', desc: '${es_desc.replace(/'/g, "\\'")}' }, en: { name: 'Decorative Vase', desc: "${en_desc}" }, fr: { name: 'Vase Décoratif', desc: "${fr_desc.replace(/'/g, "\\'")}" } }`);

fs.writeFileSync('app.js', content, 'utf8');
console.log("Fixed new catalog items!");
