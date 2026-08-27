
const fs = require('fs');
let code = fs.readFileSync('app.js', 'utf8');

global.document = {
    addEventListener: () => {},
    querySelector: () => ({ addEventListener: () => {} }),
    querySelectorAll: () => [],
    getElementById: () => ({ addEventListener: () => {}, innerHTML: '', textContent: '', appendChild: () => {}, querySelectorAll: () => [] }),
    documentElement: { setAttribute: () => {} }
};
global.window = {
    addEventListener: () => {},
    location: { href: '' },
    scrollTo: () => {}
};

eval(code + '; global.DECORATIVE_OVERRIDES = DECORATIVE_OVERRIDES;');

let output = "KEYS IN DECORATIVE_OVERRIDES: " + Object.keys(DECORATIVE_OVERRIDES).join(', ') + "\n\n";
for (let k in DECORATIVE_OVERRIDES) {
    let o = DECORATIVE_OVERRIDES[k];
    output += `Key ${k}: price=€${o.price} | name PT="${o.pt ? o.pt.name : 'NO PT'}" | name ES="${o.es ? o.es.name : 'NO ES'}"\n`;
}
fs.writeFileSync('overrides_dump.txt', output, 'utf8');
console.log("Wrote overrides_dump.txt successfully!");
