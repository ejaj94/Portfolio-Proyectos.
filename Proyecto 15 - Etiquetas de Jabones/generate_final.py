import os
import glob
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageChops

brain_dir = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\brain\ce4a2ece-d2d7-41c9-acca-716b5f94d19d"
output_dir = os.path.join(brain_dir, "scratch")
os.makedirs(output_dir, exist_ok=True)

data = [
    {"title": "Mel", "drawing": "drawing_mel*.png", "ingredientes": "Água, glicerina 100% vegetal, mel e essência natural de mel.", "esteticos": "Hidratante e ação cicatrizante. Efeito anti-infamatório e antioxidante.", "espiritual": "Prosperidade e cura. Conexão connosco mesmos."},
    {"title": "Arruda e sal grosso", "drawing": "drawing_arruda*.png", "ingredientes": "Arruda, sal grosso, água, glicerina 100% vegetal e essência de arruda.", "esteticos": "Efeito esfoliante com propriedades antibacterianas. Combate a acne e elimina o exesso de oleosidade na pele.", "espiritual": "Elimina as más energias, invejas e mau olhado."},
    {"title": "Rosa", "drawing": "drawing_rosa_1*.png", "ingredientes": "Água, glicerina 100% vegetal, essência aromática de rosas vegetal e rosa.", "esteticos": "Equilibra o PH da pele, combate o acne, antiséptico e anti-envelhecimento.", "espiritual": "Pode trazer desenvolvimento espiritual, atração amorosa e calmante."},
    {"title": "Maçã e canela", "drawing": "drawing_maca_canela*.png", "ingredientes": "Maçã, canela, água, glicerina 100% vegetal e óleo essêncial de maçã e canela.", "esteticos": "Anti-infalmatório e ajuda na diminuição da acne. Suaviza rugas de expressão, renovação de células e ajuda na aparência cansada e sem brilho.", "espiritual": "Fertilidade, beleza e juventude. Prosperidade, abundância e abertura de caminhos."},
    {"title": "Côco", "drawing": "drawing_coco*.png", "ingredientes": "Glicerina 100% vegetal, agua, côco ralado, oleo de coco e essência natural de côco.", "esteticos": "Hidratante facial e corporal. Limpa impurezas. Calmante e exelente para aliviar queimaduras provocadas pela exposição solar.", "espiritual": "O côco simboliza fertilidade e prosperidade."},
    {"title": "Alecrim", "drawing": "drawing_alecrim*.png", "ingredientes": "Alecrim, água, glicerina 100% vegetal e essência vegetal de alecrim.", "esteticos": "Ajuda na cicatrização. O alecrim ajuda no aumento do fluxo sanguíneo e produção de colagénio impedindo que a pele fique flácida.", "espiritual": "Proporciona motivação, confiança e mais energia."},
    {"title": "Jasmin", "drawing": "drawing_jasmin*.png", "ingredientes": "Jasmin, água, glicerina 100% vegetal e essência natural de jasmin.", "esteticos": "Ajuda na produção de colagénio e elasticidade da pele. Reduz acne e rugas.", "espiritual": "O jasmim simboliza amor próprio, pureza, espiritualidade e beleza. Boas energias e conexão."},
    {"title": "Camomila", "drawing": "drawing_camomila*.png", "ingredientes": "Água, glicerina 100% vegetal, camomila e essência 100% vegetal de camomila e flor de laranjeira.", "esteticos": "Acalma a pele irritada, ajuda em problemas de eczema ou acne. Renova o brilho da pele.", "espiritual": "Ajuda a ficar mais tranquilo e equilibrado. Ajuda nas tomadas de decisões e a restaurar forças."},
    {"title": "Lavanda", "drawing": "drawing_lavanda*.png", "ingredientes": "Glicerina 100% vegetal, água, essência natural e lavanda.", "esteticos": "Anti-inflamatório, reduz acne, rosácea e eczemas. Ajuda no tratamento de peles oleosas.", "espiritual": "Calmante, ajuda na ansiedade e stress. Ajuda-nos a conectar com a nossa intuição e sabedoria."},
    {"title": "Aloe Vera", "drawing": "drawing_aloe_vera*.png", "ingredientes": "Glicerina 100% vegetal, àgua, extrato de aloe vera e essência de aloe vera.", "esteticos": "Ajuda na hidratação da pele e rugas. Suaviza a pele.", "espiritual": "Simboliza proteção, esperança, longevidade e sorte."},
    {"title": "Laranja", "drawing": "drawing_naranja*.png", "ingredientes": "Glicerina 100% vegetal, água, laranja desidratada, flor de laranjeira e essência de laranja.", "esteticos": "Excelente adstringente natural. Promove a renovação celular, melhora a elasticidade da pele e auxilia no controle da oleosidade.", "espiritual": "Atrai prosperidade, alegria e vitalidade. Ajuda a dissipar sentimentos negativos e traz energia revitalizante."},
    {"title": "Rosa Mosqueta", "drawing": "drawing_rosa_mosqueta*.png", "ingredientes": "Glicerina 100% vegetal, água, óleo de rosa mosqueta, rosa mosqueta em pó e essência de rosa mosqueta.", "esteticos": "Poderoso regenerador celular e cicatrizante. Ajuda a atenuar manchas, estrias e rugas, promovendo hidratação profunda.", "espiritual": "Promove o amor-próprio, a cura emocional e a harmonia interior. Ajuda a superar mágoas e renova a energia vital."}
]

logo_path = r"C:\Users\ANGEL RAFAEL\.gemini\antigravity\scratch\com-cheiro-de-amor-pamphlet-preview\assets\logo.jpg"
width, height = 1080, 1600
bg_color = "#FFFFFF"
gold_color = (160, 120, 45)
text_color = (0, 0, 0)

def prepare_for_multiply(img, white_point=210):
    # This acts like Photoshop's "Levels" adjustment.
    # We map anything brighter than white_point to 255 (pure white).
    img = img.convert("RGB")
    table = []
    for i in range(256):
        if i >= white_point:
            table.append(255)
        else:
            table.append(int((i / white_point) * 255))
    return img.point(table * 3)

def blend_multiply(bg, fg, box):
    fg = fg.convert("RGB")
    bg_crop = bg.crop((box[0], box[1], box[0] + fg.width, box[1] + fg.height))
    # Multiply blend mode: makes white totally transparent, darkens with colors
    blended = ImageChops.multiply(bg_crop, fg)
    bg.paste(blended, box)

try:
    logo = Image.open(logo_path)
    logo.thumbnail((250, 250), Image.Resampling.LANCZOS)
    logo = prepare_for_multiply(logo, 230)
except Exception as e:
    logo = None

try:
    font_title = ImageFont.truetype("georgiai.ttf", 100)
    font_bold = ImageFont.truetype("segoeuib.ttf", 42)
    font_body = ImageFont.truetype("segoeuib.ttf", 36)
except:
    font_title = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_body = ImageFont.load_default()

def get_text_width(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]
    except:
        return len(text) * 20

def draw_text_centered(draw, text, y, font, fill, chars_per_line=50, line_spacing=10):
    lines = textwrap.wrap(text, width=chars_per_line)
    if not lines: lines = [text]
    current_y = y
    for line in lines:
        w = get_text_width(draw, line, font)
        x = (width - w) / 2
        draw.text((x, current_y), line, font=font, fill=fill)
        current_y += (font.size + line_spacing) if hasattr(font, 'size') else 40
    return current_y

for i, item in enumerate(data):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = 40
    draw.rectangle([margin, margin, width-margin, height-margin], outline=gold_color, width=4)
    draw.rectangle([margin+15, margin+15, width-margin-15, height-margin-15], outline=gold_color, width=1)
    
    current_y = 70
    
    if logo:
        lx = (width - logo.width) // 2
        blend_multiply(img, logo, (lx, current_y))
        current_y += logo.height + 20
        
    search_path = os.path.join(brain_dir, item["drawing"])
    matches = glob.glob(search_path)
    if "drawing_rosa_1*.png" in item["drawing"]:
        matches = [m for m in glob.glob(os.path.join(brain_dir, "drawing_rosa_*.png")) if "mosqueta" not in m]
    if matches:
        drawing_path = matches[0]
        try:
            drawing_img = Image.open(drawing_path)
            drawing_img.thumbnail((500, 500), Image.Resampling.LANCZOS)
            
            # This acts like Photoshop's "Levels" adjustment.
            # Using 185 instead of 210 keeps more rich colors and prevents pale prints
            drawing_img = prepare_for_multiply(drawing_img, 185)
            
            # Boost colors and contrast for rich, vibrant full-color printing
            from PIL import ImageEnhance
            color_enhancer = ImageEnhance.Color(drawing_img)
            drawing_img = color_enhancer.enhance(1.8) # Boost saturation by 80%
            contrast_enhancer = ImageEnhance.Contrast(drawing_img)
            drawing_img = contrast_enhancer.enhance(1.25) # Boost contrast by 25%
            
            ex = (width - drawing_img.width) // 2
            blend_multiply(img, drawing_img, (ex, current_y))
            
            current_y += drawing_img.height + 18
        except Exception as e:
            print(f"Error drawing {drawing_path}: {e}")
    else:
        current_y += 35
    
    current_y = draw_text_centered(draw, item["title"], current_y, font_title, gold_color, chars_per_line=30, line_spacing=15)
    current_y += 18
    
    sections = [
        ("Ingredientes:", item["ingredientes"]),
        ("Benefícios estéticos:", item["esteticos"]),
        ("Espiritualmente:", item["espiritual"])
    ]
    
    for title, content in sections:
        current_y = draw_text_centered(draw, title, current_y, font_bold, text_color, chars_per_line=46)
        current_y += 5
        current_y = draw_text_centered(draw, content, current_y, font_body, text_color, chars_per_line=46, line_spacing=8)
        current_y += 18
    
    out_path = os.path.join(output_dir, f"drawing_label_{i}.jpeg")
    img.save(out_path, "JPEG", quality=95)
    print(f"Label saved: {out_path}")
