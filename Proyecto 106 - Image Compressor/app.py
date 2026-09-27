from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import io
import base64
import time
from database import init_db, add_compression, get_all_history, clear_all_history

app = Flask(__name__)
PORT = 6959

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB max upload limit

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

init_db()

@app.route('/')
def index():
    history = get_all_history()
    return render_template('index.html', history=history)

@app.route('/api/compress', methods=['POST'])
def compress_image():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhuma imagem fornecida."}), 400
    
    file = request.files['file']
    quality = int(request.form.get('quality', 80))
    scale = float(request.form.get('scale', 1.0))
    output_fmt = request.form.get('output_format', 'WEBP').upper()
    
    if not file or file.filename == '':
        return jsonify({"error": "Ficheiro de imagem inválido."}), 400
    
    filename = file.filename
    name_part, _ = os.path.splitext(filename)
    
    file_bytes = file.read()
    original_size_kb = round(len(file_bytes) / 1024.0, 2)
    
    if not HAS_PILLOW:
        return jsonify({"error": "Biblioteca Pillow nao instalada no servidor."}), 500

    try:
        image = Image.open(io.BytesIO(file_bytes))
        orig_w, orig_h = image.size
        orig_dims = f"{orig_w}x{orig_h}"
        
        # Calculate new dimensions if scaled
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))
        
        if (new_w, new_h) != (orig_w, orig_h):
            image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        comp_dims = f"{new_w}x{new_h}"

        # Target extension & format mapping
        ext = output_fmt.lower()
        if ext == 'jpeg':
            ext = 'jpg'

        converted_filename = f"{name_part}_compressed.{ext}"

        out_io = io.BytesIO()
        save_format = output_fmt
        if save_format == 'JPG':
            save_format = 'JPEG'

        # Color mode conversions for JPEG/WEBP
        if save_format in ('JPEG', 'JPG') and image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        elif save_format in ('WEBP', 'PNG') and image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')

        # Perform compression
        if save_format == 'PNG':
            image.save(out_io, format='PNG', optimize=True)
        else:
            image.save(out_io, format=save_format, quality=quality, optimize=True)

        comp_bytes = out_io.getvalue()
        compressed_size_kb = round(len(comp_bytes) / 1024.0, 2)

        # Savings percentage calculation
        diff_kb = original_size_kb - compressed_size_kb
        savings_pct = round((diff_kb / original_size_kb) * 100, 1) if original_size_kb > 0 else 0.0

        # Save compressed file to uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, converted_filename)
        with open(file_path, 'wb') as f:
            f.write(comp_bytes)

        # Prepare Base64 data URL for instant live preview
        mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
        comp_b64 = base64.b64encode(comp_bytes).decode('utf-8')
        data_url = f"data:{mime_type};base64,{comp_b64}"

        # Save record in SQLite database
        add_compression(
            original_filename=filename,
            compressed_filename=converted_filename,
            output_format=output_fmt,
            quality=quality,
            original_size_kb=original_size_kb,
            compressed_size_kb=compressed_size_kb,
            savings_pct=savings_pct,
            original_dimensions=orig_dims,
            compressed_dimensions=comp_dims,
            file_path=f"uploads/{converted_filename}"
        )

        return jsonify({
            "success": True,
            "original_filename": filename,
            "compressed_filename": converted_filename,
            "output_format": output_fmt,
            "quality": quality,
            "original_size_kb": original_size_kb,
            "compressed_size_kb": compressed_size_kb,
            "savings_pct": savings_pct,
            "original_dimensions": orig_dims,
            "compressed_dimensions": comp_dims,
            "data_url": data_url,
            "download_url": f"/api/download/{converted_filename}"
        })

    except Exception as e:
        return jsonify({"error": f"Erro ao processar imagem: {str(e)}"}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/api/history', methods=['GET', 'DELETE'])
def manage_history():
    if request.method == 'DELETE':
        clear_all_history()
        return jsonify({"message": "Historico de compressao limpo com sucesso."})
    return jsonify(get_all_history())

if __name__ == '__main__':
    print(f"Servidor CompressPic AI iniciado na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
