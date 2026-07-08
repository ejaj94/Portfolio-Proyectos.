import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

logo_path = os.path.join("assets", "logo.jpg")
output_dir = "assets"
os.makedirs(output_dir, exist_ok=True)

# 1. Load and process logo (make white background transparent)
logo = Image.open(logo_path).convert("RGBA")

# Auto-crop white borders from logo
# Convert to grayscale and invert to find bounding box of non-white areas
gray = logo.convert("L")
inverted = ImageOps.invert(gray)
bbox = inverted.getbbox()
if bbox:
    # Add a bit of padding to the bbox
    padding = 10
    w, h = logo.size
    bbox = (
        max(0, bbox[0] - padding),
        max(0, bbox[1] - padding),
        min(w, bbox[2] + padding),
        min(h, bbox[3] + padding)
    )
    logo = logo.crop(bbox)

# Convert white/light pixels to transparent
datas = logo.getdata()
newData = []
for item in datas:
    # If pixel is very close to white, make it transparent
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)
logo.putdata(newData)

# Scale logo to a reasonable size (e.g., width of 400px for a 1200px canvas)
logo_w, logo_h = logo.size
target_w = 400
target_h = int(logo_h * (target_w / logo_w))
logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Warning Text Content
title_text = "VELA AROMÁTICA"
aviso_header = "AVISO:"
rules = [
    "PARA EVITAR INCÊNDIO E FERIMENTOS GRAVES.",
    "NÃO QUEIME A VELA SEM SUPERVISÃO.",
    "MANTER EM UMA SUPERFÍCIE PLANA.",
    "MANTER LONGE DE OBJETOS INFLAMÁVEIS,",
    "CRIANÇAS E ANIMAIS DE ESTIMAÇÃO."
]
burn_header = "INSTRUÇÕES DE QUEIMA:"
burn_instructions = [
    "ANTES DE ACENDER APARE O PAVIO DA VELA.",
    "NÃO QUEIME A VELA POR MAIS DE 2 HORAS SEGUIDAS.",
    "TIRE QUALQUER PAPEL QUE ESTEJA NA SUPERFÍCIE",
    "ANTES DE ACENDER. DESCARTE QUANDO TIVER",
    "SOMENTE CERA NO RECIPIENTE."
]
composition = "COMPOSIÇÃO: CERA VEGETAL DE SOJA, PAVIO DE ALGODÃO E ESSÊNCIA"
footer = "FAB.: _______________   USO IDEAL: 2 ANOS   PESO: _________"

# Load Fonts
try:
    font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\calibrib.ttf", 32)
    font_reg = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", 24)
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\georgiab.ttf", 44)
    font_small = ImageFont.truetype("C:\\Windows\\Fonts\\calibri.ttf", 20)
except:
    # Fallback to default
    font_bold = ImageFont.load_default()
    font_reg = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_small = ImageFont.load_default()

def draw_label(bg_color, border_color, text_color, is_dark_bg=False):
    # Create canvas
    canvas_size = 1200
    img = Image.new("RGB", (canvas_size, canvas_size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw circular border
    margin = 40
    draw.ellipse(
        [margin, margin, canvas_size - margin, canvas_size - margin], 
        outline=border_color, 
        width=8
    )
    
    # Paste logo at top center
    logo_y = 120
    logo_x = (canvas_size - target_w) // 2
    
    # If background is dark/kraft/pink, we can tint the logo or just paste it
    # Since the logo is golden/beige, it should look good on white, pink, and kraft.
    # If we need to make it white for dark/lavender bg:
    if is_dark_bg:
        # Tint logo to white
        logo_tinted = Image.new("RGBA", logo.size)
        draw_tint = ImageDraw.Draw(logo_tinted)
        draw_tint.rectangle([0, 0, logo.size[0], logo.size[1]], fill=(255, 255, 255, 255))
        # Use logo as alpha mask
        logo_to_paste = Image.composite(logo_tinted, Image.new("RGBA", logo.size, (0,0,0,0)), logo)
    else:
        logo_to_paste = logo
        
    img.paste(logo_to_paste, (logo_x, logo_y), logo_to_paste)
    
    # Text Layout Y positions
    current_y = logo_y + target_h + 30
    
    # Title "VELA AROMÁTICA"
    w = draw.textlength(title_text, font=font_title)
    draw.text(((canvas_size - w)/2, current_y), title_text, fill=text_color, font=font_title)
    current_y += 60
    
    # AVISO (Red for warning style, or matching text color)
    aviso_color = (200, 50, 50) if not is_dark_bg else (255, 100, 100)
    w = draw.textlength(aviso_header, font=font_bold)
    draw.text(((canvas_size - w)/2, current_y), aviso_header, fill=aviso_color, font=font_bold)
    current_y += 40
    
    # Rules
    for r in rules:
        w = draw.textlength(r, font=font_reg)
        draw.text(((canvas_size - w)/2, current_y), r, fill=text_color, font=font_reg)
        current_y += 30
    
    current_y += 15
    
    # Burn Header
    w = draw.textlength(burn_header, font=font_bold)
    draw.text(((canvas_size - w)/2, current_y), burn_header, fill=text_color, font=font_bold)
    current_y += 35
    
    # Burn Instructions
    for r in burn_instructions:
        w = draw.textlength(r, font=font_reg)
        draw.text(((canvas_size - w)/2, current_y), r, fill=text_color, font=font_reg)
        current_y += 30
        
    current_y += 20
    
    # Composition
    w = draw.textlength(composition, font=font_small)
    draw.text(((canvas_size - w)/2, current_y), composition, fill=text_color, font=font_small)
    current_y += 40
    
    # Footer
    w = draw.textlength(footer, font=font_reg)
    draw.text(((canvas_size - w)/2, current_y), footer, fill=text_color, font=font_reg)
    
    return img

# Generate 3 styles
# Style 1: Classic White (Logo original colors, white background, gold/beige border, black text)
label3 = draw_label(
    bg_color=(255, 255, 255), 
    border_color=(212, 175, 125), # Gold-ish
    text_color=(30, 30, 30),
    is_dark_bg=False
)
label3.save(os.path.join(output_dir, "etiqueta_original_3.jpg"), "JPEG", quality=95)
print("Saved etiqueta_original_3.jpg")

# Style 2: Kraft Rustic (Logo original, kraft background, brown border, charcoal text)
label4 = draw_label(
    bg_color=(225, 206, 181), # Kraft brown
    border_color=(120, 95, 70), # Darker brown
    text_color=(45, 40, 35),
    is_dark_bg=False
)
label4.save(os.path.join(output_dir, "etiqueta_original_4.jpg"), "JPEG", quality=95)
print("Saved etiqueta_original_4.jpg")

# Style 3: Blush Pink (Logo original, soft pink background, white border, dark brown text)
label5 = draw_label(
    bg_color=(252, 230, 230), # Blush pink
    border_color=(255, 255, 255), # White border
    text_color=(60, 50, 50),
    is_dark_bg=False
)
label5.save(os.path.join(output_dir, "etiqueta_original_5.jpg"), "JPEG", quality=95)
print("Saved etiqueta_original_5.jpg")
