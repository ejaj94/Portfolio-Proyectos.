import os
import glob
from PIL import Image, ImageDraw

brain_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\brain\ce4a2ece-d2d7-41c9-acca-716b5f94d19d"
scratch_dir = os.path.join(brain_dir, "scratch")
desktop_dir = r"C:\Users\ANGEL RAFAEL\Desktop\Etiquetas_A4_ParaImprimir"
os.makedirs(desktop_dir, exist_ok=True)

# === CONFIGURACIÓN A4 ===
DPI = 300
MM = DPI / 25.4

A4_W = int(210 * MM)  # 2480 px
A4_H = int(297 * MM)  # 3508 px

LABEL_W_MM = 40
LABEL_H_MM = 20
LABEL_W = int(LABEL_W_MM * MM)  # 472 px
LABEL_H = int(LABEL_H_MM * MM)  # 236 px

MARGIN = int(5 * MM)
GAP = int(3 * MM)

avail_w = A4_W - 2 * MARGIN
avail_h = A4_H - 2 * MARGIN
COLS = 4
ROWS = 12

# Lista de nombres en orden
names = ["orquea", "mia", "lumiere", "big heart", "glamour", "havana", "tulia", "wave", "mira", "tulipas"]

# Llenar la hoja completa repitiendo la lista equitativamente y agrupándolas (48 etiquetas en total)
# 8 nombres con 5 copias y 2 nombres (mira y tulipas) con 4 copias
labels_to_place = []
for name in names:
    count = 4 if name in ["mira", "tulipas"] else 5
    labels_to_place += [name] * count

# Crear una matriz para organizar verticalmente (por columnas)
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
idx = 0
for col in range(COLS):
    for row in range(ROWS):
        if idx < len(labels_to_place):
            grid[row][col] = labels_to_place[idx]
            idx += 1

# Crear la hoja A4 en blanco
sheet = Image.new("RGB", (A4_W, A4_H), "#FFFFFF")
draw = ImageDraw.Draw(sheet)

# Colocar las etiquetas siguiendo la matriz
for row in range(ROWS):
    for col in range(COLS):
        name = grid[row][col]
        if not name:
            continue
            
        label_filename = f"black_typo_{name}.jpeg"
        label_path = os.path.join(scratch_dir, label_filename)
        
        if not os.path.exists(label_path):
            print(f"No existe: {label_path}")
            continue
            
        label_img = Image.open(label_path).convert("RGB")
        # Ajustar al tamaño de la etiqueta (40x20mm)
        label_img = label_img.resize((LABEL_W, LABEL_H), Image.Resampling.LANCZOS)
        
        # Calcular coordenadas
        x = MARGIN + col * (LABEL_W + GAP)
        y = MARGIN + row * (LABEL_H + GAP)
        
        # Pegar en la hoja
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
        
        idx += 1

# Guardar la hoja A4 final en formato PDF en el escritorio
pdf_output_path = os.path.join(desktop_dir, "Etiquetas_Nombres_4x2cm_A4_Ordenado.pdf")
sheet.save(pdf_output_path, "PDF", resolution=DPI)
print(f"PDF A4 Creado con éxito: {pdf_output_path}")

# También guardar los JPG individuales originales en el Escritorio en formato original
individual_dest_dir = os.path.join(desktop_dir, "Individuales_Originales")
os.makedirs(individual_dest_dir, exist_ok=True)

for name in names:
    label_path = os.path.join(scratch_dir, f"black_typo_{name}.jpeg")
    if os.path.exists(label_path):
        img = Image.open(label_path)
        dest_path = os.path.join(individual_dest_dir, f"etiqueta_{name}.jpg")
        img.save(dest_path, "JPEG", quality=95)
        print(f"Copiado individual: {dest_path}")
