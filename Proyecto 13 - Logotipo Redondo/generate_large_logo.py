import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PIL import Image, ImageEnhance, ImageChops

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

print(f"Escritorio detectado para Logotipo: {desktop_dir}")

# Ruta del logotipo original
logo_path = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\scratch\com-cheiro-de-amor-pamphlet-preview\assets\logo.jpg"

if not os.path.exists(logo_path):
    print("FALTA el logotipo original.")
    exit(1)

# Procesar la imagen para que tenga colores vivos e intensos y fondo blanco puro
img = Image.open(logo_path).convert("RGB")

# 1. Ajustar niveles de blanco (Photoshop levels) para que el fondo sea blanco puro y no se vea gris
table = []
white_point = 230
for i in range(256):
    if i >= white_point:
        table.append(255)
    else:
        table.append(int((i / white_point) * 255))
img = img.point(table * 3)

# 2. Incrementar la saturación del color oro para que sea muy vivo y cálido
color_enhancer = ImageEnhance.Color(img)
img = color_enhancer.enhance(1.8) # Incrementar saturación un 80%

# 3. Incrementar el contraste para que los contornos y las letras sean muy legibles
contrast_enhancer = ImageEnhance.Contrast(img)
img = contrast_enhancer.enhance(1.3) # Incrementar contraste un 30%

# Guardar imagen procesada temporal de alta calidad
temp_logo_path = os.path.join(scratch_dir, "temp_large_logo.jpg")
img.save(temp_logo_path, "JPEG", quality=98, dpi=(300, 300))

# === LAYOUT CON REPORTLAB ===
A4_W, A4_H = A4 # 595.27 x 841.89

# El logotipo grande ocupará casi todo el ancho disponible (dejando 25mm de margen a cada lado)
target_w = A4_W - (50 * mm)  # Margen de 25mm izquierdo y 25mm derecho
# Calcular el alto proporcional basándonos en la relación de aspecto original de la imagen
aspect = img.height / img.width
target_h = target_w * aspect

# Centrar horizontal y verticalmente en la página A4
x = (A4_W - target_w) / 2.0
y = (A4_H - target_h) / 2.0

# Crear PDF
pdf_output_path = os.path.join(desktop_dir, "Logotipo_Grande_A4.pdf")
c = canvas.Canvas(pdf_output_path, pagesize=A4)

# Dibujar la imagen procesada
c.drawImage(temp_logo_path, x, y, width=target_w, height=target_h)
c.showPage()
c.save()

print(f"Logotipo Grande A4 generado con éxito en: {pdf_output_path}")

# Limpiar archivo temporal
try:
    os.remove(temp_logo_path)
except:
    pass
