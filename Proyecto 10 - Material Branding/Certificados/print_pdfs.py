import asyncio
from playwright.async_api import async_playwright
import os

async def generate_pdfs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        desktop = r"C:\Users\ANGEL RAFAEL\Desktop"
        base_url = "http://localhost:8088"
        
        print("Generating PT PDF...")
        await page.goto(f"{base_url}/index.html", wait_until="networkidle")
        await page.emulate_media(media="print")
        await page.pdf(path=os.path.join(desktop, "Certificados_PT.pdf"), format="A4", landscape=True, print_background=True)
        
        print("Generating EN PDF...")
        await page.goto(f"{base_url}/index_en.html", wait_until="networkidle")
        await page.emulate_media(media="print")
        await page.pdf(path=os.path.join(desktop, "Certificados_EN.pdf"), format="A4", landscape=True, print_background=True)
        
        await browser.close()
        print("PDFs generated successfully.")

asyncio.run(generate_pdfs())
