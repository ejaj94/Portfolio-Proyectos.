import os
import glob
import math
from PIL import Image, ImageDraw, ImageChops

brain_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\brain\ce4a2ece-d2d7-41c9-acca-716b5f94d19d"
scratch_dir = os.path.join(brain_dir, "scratch")
desktop_dir = r"C:\Users\ANGEL RAFAEL\Desktop\Etiquetas_A4_ParaImprimir"
os.makedirs(desktop_dir, exist_ok=True)

# === CONFIGURACIÓN ===
DPI = 300
MM = DPI / 25.4

A4_W = int(210 * MM)
A4_H = int(297 * MM)

LABEL_W_MM = 60
LABEL_H_MM = 35
LABEL_W = int(LABEL_W_MM * MM)
LABEL_H = int(LABEL_H_MM * MM)

MARGIN = int(5 * MM)
GAP = int(3 * MM)

avail_w = A4_W - 2 * MARGIN
avail_h = A4_H - 2 * MARGIN
COLS = (avail_w + GAP) // (LABEL_W + GAP)
ROWS = (avail_h + GAP) // (LABEL_H + GAP)
TOTAL = COLS * ROWS

print(f"Layout: {COLS} columnas x {ROWS} filas = {TOTAL} etiquetas por hoja")
print(f"Etiqueta: {LABEL_W_MM}mm x {LABEL_H_MM}mm a {DPI} DPI")

names = [
    "Mel", "Arruda e sal grosso", "Rosa", "Maca e canela",
    "Coco", "Alecrim", "Jasmin", "Camomila",
    "Lavanda", "Aloe Vera", "Laranja", "Rosa Mosqueta"
]

safe_names = [
    "01_Mel", "02_Arruda_e_Sal_Grosso", "03_Rosa", "04_Maca_e_Canela",
    "05_Coco", "06_Alecrim", "07_Jasmin", "08_Camomila",
    "09_Lavanda", "10_Aloe_Vera", "11_Laranja", "12_Rosa_Mosqueta"
]

for i in range(12):
    label_src = os.path.join(scratch_dir, f"drawing_label_{i}.jpeg")
    if not os.path.exists(label_src):
        print(f"FALTA: {label_src}")
        continue

    # Cargar etiqueta original y rotar 90° para formato horizontal
    label_img = Image.open(label_src).convert("RGB")
    label_img = label_img.rotate(90, expand=True)
    label_img = label_img.resize((LABEL_W, LABEL_H), Image.Resampling.LANCZOS)

    # Crear hoja A4 blanca
    sheet = Image.new("RGB", (A4_W, A4_H), "#FFFFFF")
    draw = ImageDraw.Draw(sheet)

    # Colocar etiquetas
    for row in range(ROWS):
        for col in range(COLS):
            x = MARGIN + col * (LABEL_W + GAP)
            y = MARGIN + row * (LABEL_H + GAP)
            sheet.paste(label_img, (x, y))
            # Marcas de corte
            sp = 7
            mk = 16
            color = "#AAAAAA"
            draw.line([(x-sp-mk, y), (x-sp, y)], fill=color, width=2)
            draw.line([(x, y-sp-mk), (x, y-sp)], fill=color, width=2)
            draw.line([(x+LABEL_W+sp, y), (x+LABEL_W+sp+mk, y)], fill=color, width=2)
            draw.line([(x+LABEL_W, y-sp-mk), (x+LABEL_W, y-sp)], fill=color, width=2)
            draw.line([(x-sp-mk, y+LABEL_H), (x-sp, y+LABEL_H)], fill=color, width=2)
            draw.line([(x, y+LABEL_H+sp), (x, y+LABEL_H+sp+mk)], fill=color, width=2)
            draw.line([(x+LABEL_W+sp, y+LABEL_H), (x+LABEL_W+sp+mk, y+LABEL_H)], fill=color, width=2)
            draw.line([(x+LABEL_W, y+LABEL_H+sp), (x+LABEL_W, y+LABEL_H+sp+mk)], fill=color, width=2)

    # Guardar como PDF
    pdf_path = os.path.join(desktop_dir, f"{safe_names[i]}.pdf")
    sheet.save(
        pdf_path,
        "PDF",
        resolution=DPI,
        save_all=False
    )
    print(f"[{i+1}/12] PDF creado: {pdf_path}")

print("\n¡Todos los PDFs generados! Carpeta: " + desktop_dir)
