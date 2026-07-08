import os
from PIL import Image, ImageDraw, ImageOps, ImageChops

brain_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\brain\ce4a2ece-d2d7-41c9-acca-716b5f94d19d"
scratch_dir = os.path.join(brain_dir, "scratch")
desktop_dir = r"C:\Users\ANGEL RAFAEL\Desktop\Etiquetas_A4_ParaImprimir"
os.makedirs(desktop_dir, exist_ok=True)

logo_path = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\scratch\com-cheiro-de-amor-pamphlet-preview\assets\logo.jpg"

# === CONFIGURACIÓN ===
DPI = 300
MM = DPI / 25.4

A4_W = int(210 * MM)  # 2480 px
A4_H = int(297 * MM)  # 3508 px

# Medida solicitada: 3cm x 3cm (30mm x 30mm)
LABEL_SIZE_MM = 30
LABEL_SIZE = int(LABEL_SIZE_MM * MM)  # ~354 px

MARGIN = int(5 * MM)
GAP = int(3 * MM)

# Calcular cuadrícula óptima
avail_w = A4_W - 2 * MARGIN
avail_h = A4_H - 2 * MARGIN
COLS = (avail_w + GAP) // (LABEL_SIZE + GAP)  # 6 columnas
ROWS = (avail_h + GAP) // (LABEL_SIZE + GAP)  # 8 filas
TOTAL = COLS * ROWS

print(f"Medidas: {COLS} columnas x {ROWS} filas = {TOTAL} logos redondos por hoja A4")

# Crear el logo redondo individual con marco doble redondo
bg_color = "#FAFAF7"  # Fondo crema
gold_color = "#C5A059" # Dorado

# Cargar el logo original
logo = Image.open(logo_path).convert("RGB")

# 1. Crear el lienzo circular de 354x354 px
circle_label = Image.new("RGB", (LABEL_SIZE, LABEL_SIZE), bg_color)
draw_label = ImageDraw.Draw(circle_label)

# 2. Redimensionar el logo para que quepa bien centrado dentro del círculo
# Dejar espacio para el marco circular doble
inner_logo_size = int(LABEL_SIZE * 0.7)  # ~247 px
logo_resized = logo.resize((inner_logo_size, inner_logo_size), Image.Resampling.LANCZOS)

# Quitar el fondo blanco del logo usando multiply contra el lienzo circular
# Primero centramos el logo en una plantilla del tamaño de la etiqueta
logo_template = Image.new("RGB", (LABEL_SIZE, LABEL_SIZE), "#FFFFFF")
lx = (LABEL_SIZE - logo_resized.width) // 2
ly = (LABEL_SIZE - logo_resized.height) // 2
logo_template.paste(logo_resized, (lx, ly))

# Multiplicar
circle_label = ImageChops.multiply(circle_label, logo_template)
draw_label = ImageDraw.Draw(circle_label)

# 3. Dibujar marco doble circular dorado
# Círculo exterior (más grueso)
draw_label.ellipse([5, 5, LABEL_SIZE-5, LABEL_SIZE-5], outline=gold_color, width=4)
# Círculo interior (más fino)
draw_label.ellipse([12, 12, LABEL_SIZE-12, LABEL_SIZE-12], outline=gold_color, width=1)

# 4. Crear máscara redonda para que al cortar el JPG no se vea nada fuera del círculo
mask = Image.new("L", (LABEL_SIZE, LABEL_SIZE), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse([0, 0, LABEL_SIZE, LABEL_SIZE], fill=255)

# Aplicar máscara para asegurar transparencia en el fondo exterior del círculo (blanco para imprimir)
circle_label_rgba = circle_label.convert("RGBA")
circle_label_rgba.putalpha(mask)

# --- CREAR LA HOJA A4 ---
sheet = Image.new("RGB", (A4_W, A4_H), "#FFFFFF")
draw_sheet = ImageDraw.Draw(sheet)

# Pegar los 48 logos circulares
for row in range(ROWS):
    for col in range(COLS):
        x = MARGIN + col * (LABEL_SIZE + GAP)
        y = MARGIN + row * (LABEL_SIZE + GAP)
        
        # Pegar el logo circular RGBA (respetando la máscara redonda sobre el papel A4 blanco)
        sheet.paste(circle_label_rgba, (x, y), circle_label_rgba)
        
        # Marcas de corte estilo circular (pequeño círculo o marcas estándar en las esquinas)
        # Dibujamos marcas finas gris para corte
        sp = 4
        mk = 10
        color = "#CCCCCC"
        draw_sheet.line([(x-sp-mk, y), (x-sp, y)], fill=color, width=1)
        draw_sheet.line([(x, y-sp-mk), (x, y-sp)], fill=color, width=1)
        draw_sheet.line([(x+LABEL_SIZE+sp, y), (x+LABEL_SIZE+sp+mk, y)], fill=color, width=1)
        draw_sheet.line([(x+LABEL_SIZE, y-sp-mk), (x+LABEL_SIZE, y-sp)], fill=color, width=1)
        draw_sheet.line([(x-sp-mk, y+LABEL_SIZE), (x-sp, y+LABEL_SIZE)], fill=color, width=1)
        draw_sheet.line([(x, y+LABEL_SIZE+sp), (x, y+LABEL_SIZE+sp+mk)], fill=color, width=1)
        draw_sheet.line([(x+LABEL_SIZE+sp, y+LABEL_SIZE), (x+LABEL_SIZE+sp+mk, y+LABEL_SIZE)], fill=color, width=1)
        draw_sheet.line([(x+LABEL_SIZE, y+LABEL_SIZE+sp), (x+LABEL_SIZE, y+LABEL_SIZE+sp+mk)], fill=color, width=1)

# Guardar la hoja A4 final en formato PDF en el escritorio
pdf_output_path = os.path.join(desktop_dir, "Logotipo_Redondo_3x3cm_A4.pdf")
sheet.save(pdf_output_path, "PDF", resolution=DPI)
print(f"PDF A4 Creado: {pdf_output_path}")

# Guardar preview a escala para el panel lateral
preview = sheet.resize((A4_W // 3, A4_H // 3), Image.Resampling.LANCZOS)
preview_path = os.path.join(brain_dir, "logo_round_preview.jpeg")
preview.save(preview_path, "JPEG", quality=92)
