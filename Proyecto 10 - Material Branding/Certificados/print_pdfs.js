const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        
        const desktopPath = 'C:\\Users\\ANGEL RAFAEL\\Desktop';
        const baseUrl = 'file:///C:/Users/ANGEL%20RAFAEL/.gemini/antigravity/scratch/Certificados_Workshop';
        
        console.log('Generating PT PDF for Model 3...');
        await page.goto(`${baseUrl}/modelo3_pt.html`, { waitUntil: 'load' });
        await page.pdf({
            path: path.join(desktopPath, 'Certificado_Modelo3_PT.pdf'),
            format: 'A4',
            landscape: true,
            printBackground: true
        });
        
        console.log('Generating EN PDF for Model 3...');
        await page.goto(`${baseUrl}/modelo3_en.html`, { waitUntil: 'load' });
        await page.pdf({
            path: path.join(desktopPath, 'Certificado_Modelo3_EN.pdf'),
            format: 'A4',
            landscape: true,
            printBackground: true
        });
        
        await browser.close();
        console.log('PDFs generated successfully.');
    } catch (e) {
        console.error(e);
    }
})();
