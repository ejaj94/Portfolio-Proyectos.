import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PIL import Image

brain_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\brain\ce4a2ece-d2d7-41c9-acca-716b5f94d19d"
scratch_dir = os.path.join(brain_dir, "scratch")

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

print(f"Escritorio detectado para ReportLab: {desktop_dir}")

# === CONFIGURACIÓN DE REPORTLAB ===
# Dimensiones en puntos
A4_W, A4_H = A4  # 595.27 x 841.89

# Etiquetas de 60mm x 35mm
LABEL_W = 60 * mm
LABEL_H = 45 * mm
GAP = 3 * mm

COLS = 3
ROWS = 6
SLOTS_PER_PAGE = COLS * ROWS

# Centrar la rejilla en la página
grid_w = COLS * LABEL_W + (COLS - 1) * GAP
grid_h = ROWS * LABEL_H + (ROWS - 1) * GAP
start_x = (A4_W - grid_w) / 2.0
start_y = (A4_H - grid_h) / 2.0

# Preparar las imágenes: rotarlas para formato horizontal y guardarlas como temporales de alta calidad
temp_paths = []
for i in range(12):
    src = os.path.join(scratch_dir, f"drawing_label_{i}.jpeg")
    if os.path.exists(src):
        img = Image.open(src).convert("RGB")
        # Rotamos 90 grados para que quede horizontal (la imagen original de generate_final es vertical)
        img = img.rotate(90, expand=True)
        temp_path = os.path.join(scratch_dir, f"temp_label_horiz_{i}.jpg")
        img.save(temp_path, "JPEG", quality=98, dpi=(300, 300))
        temp_paths.append(temp_path)
    else:
        print(f"Falta: {src}")

# Expandir la lista para tener 5 copias seguidas de cada uno de los 12 tipos
labels_to_place = []
for p in temp_paths:
    for _ in range(5):
        labels_to_place.append(p)

total_labels = len(labels_to_place)
num_pages = (total_labels + SLOTS_PER_PAGE - 1) // SLOTS_PER_PAGE

pdf_output_path = os.path.join(desktop_dir, "Etiquetas_Sabonetes_5xCada_A4.pdf")
c = canvas.Canvas(pdf_output_path, pagesize=A4)

for p in range(num_pages):
    start_idx = p * SLOTS_PER_PAGE
    end_idx = min(start_idx + SLOTS_PER_PAGE, total_labels)
    
    for idx in range(start_idx, end_idx):
        slot_pos = idx - start_idx
        col = slot_pos % COLS
        row = ROWS - 1 - (slot_pos // COLS) # ReportLab (0,0) está abajo a la izquierda, invertimos filas
        
        x = start_x + col * (LABEL_W + GAP)
        y = start_y + row * (LABEL_H + GAP)
        
        # Dibujar imagen en alta resolución ocupando exactamente el espacio físico del slot
        c.drawImage(labels_to_place[idx], x, y, width=LABEL_W, height=LABEL_H)
        
        # Dibujar marcas de corte delgadas a los lados de la etiqueta
        sp = 2 * mm
        mk = 5 * mm
        c.setStrokeColorRGB(0.66, 0.66, 0.66)
        c.setLineWidth(0.5)
        
        # Esquina superior izquierda
        c.line(x - sp - mk, y + LABEL_H, x - sp, y + LABEL_H)
        c.line(x, y + LABEL_H + sp + mk, x, y + LABEL_H + sp)
        # Esquina superior derecha
        c.line(x + LABEL_W + sp, y + LABEL_H, x + LABEL_W + sp + mk, y + LABEL_H)
        c.line(x + LABEL_W, y + LABEL_H + sp + mk, x + LABEL_W, y + LABEL_H + sp)
        # Esquina inferior izquierda
        c.line(x - sp - mk, y, x - sp, y)
        c.line(x, y - sp - mk, x, y - sp)
        # Esquina inferior derecha
        c.line(x + LABEL_W + sp, y, x + LABEL_W + sp + mk, y)
        c.line(x + LABEL_W, y - sp - mk, x + LABEL_W, y - sp)
        
    c.showPage()

c.save()
print(f"ReportLab PDF generado exitosamente en: {pdf_output_path}")

# Limpiar archivos temporales
for p in temp_paths:
    try:
        os.remove(p)
    except:
        pass
