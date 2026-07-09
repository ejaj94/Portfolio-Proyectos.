import os
from PIL import Image, ImageDraw

brain_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\brain\ce4a2ece-d2d7-41c9-acca-716b5f94d19d"
scratch_dir = os.path.join(brain_dir, "scratch")
portfolio_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\scratch\Portfolio-Proyectos"

# Encontrar la ruta del escritorio de OneDrive dinámicamente
onedrive_dir = r"C:\Users\ANGEL RAFAEL\OneDrive"
desktop_folder_name = None
for d in os.listdir(onedrive_dir):
    full_path = os.path.join(onedrive_dir, d)
    if os.path.isdir(full_path) and ("trabalho" in d.lower() or "desktop" in d.lower() or "escrit" in d.lower()):
        desktop_folder_name = d
        break
        
if desktop_folder_name:
    desktop_dir = os.path.join(onedrive_dir, desktop_folder_name)
else:
    desktop_dir = r"C:\Users\ANGEL RAFAEL\Desktop"

print(f"Escritorio detectado: {desktop_dir}")

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

# Grid
COLS = 3
ROWS = 7
SLOTS_PER_PAGE = COLS * ROWS # 21

# Cargar las 12 imágenes y rotarlas para el formato horizontal (60x35mm)
labels = []
for i in range(12):
    src = os.path.join(scratch_dir, f"drawing_label_{i}.jpeg")
    if os.path.exists(src):
        img = Image.open(src).convert("RGB")
        img = img.rotate(90, expand=True)
        img = img.resize((LABEL_W, LABEL_H), Image.Resampling.LANCZOS)
        # Añadir 5 copias seguidas
        for _ in range(5):
            labels.append(img)
    else:
        print(f"Falta: {src}")

# Crear las páginas A4 necesarias
pages = []
total_labels = len(labels)
num_pages = (total_labels + SLOTS_PER_PAGE - 1) // SLOTS_PER_PAGE # 3 páginas

for p in range(num_pages):
    sheet = Image.new("RGB", (A4_W, A4_H), "#FFFFFF")
    draw = ImageDraw.Draw(sheet)
    
    # Rellenar slots para la página actual
    start_idx = p * SLOTS_PER_PAGE
    end_idx = min(start_idx + SLOTS_PER_PAGE, total_labels)
    
    for idx in range(start_idx, end_idx):
        slot_pos = idx - start_idx
        col = slot_pos % COLS
        row = slot_pos // COLS
        
        x = MARGIN + col * (LABEL_W + GAP)
        y = MARGIN + row * (LABEL_H + GAP)
        
        # Pegar la etiqueta
        sheet.paste(labels[idx], (x, y))
        
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
        
    pages.append(sheet)

# Guardar todas las páginas en un único PDF multipágina en el escritorio
pdf_output_path = os.path.join(desktop_dir, "Etiquetas_Sabonetes_5xCada_A4.pdf")
pages[0].save(
    pdf_output_path,
    "PDF",
    resolution=DPI,
    save_all=True,
    append_images=pages[1:]
)
print(f"PDF Multihaja Creado exitosamente en: {pdf_output_path}")

# Copiar a carpetas del portafolio y taller
import shutil
shutil.copy(pdf_output_path, os.path.join(portfolio_dir, "Proyecto 15 - Etiquetas de Jabones", "assets", "Etiquetas_Sabonetes_5xCada_A4.pdf"))
shutil.copy(pdf_output_path, r"C:\Users\ANGEL RAFAEL\Desktop\Portfolio de programacion\Proyectos\Proyecto 15 - Etiquetas de Jabones\assets\Etiquetas_Sabonetes_5xCada_A4.pdf")
shutil.copy(pdf_output_path, r"C:\Users\ANGEL RAFAEL\Desktop\Portfolio de programacion\Proyectos reales\Com cheiro de amor pagina web Stephanie Santos\Material workshop\Etiquetas_De_Sabonetes_A4_Para_Imprimir\Etiquetas_Sabonetes_5xCada_A4.pdf")
print("Copiado a las carpetas del proyecto completado.")
