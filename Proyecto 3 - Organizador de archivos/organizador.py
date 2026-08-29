import os
import shutil
import hashlib
import json
from datetime import datetime

# Definición estándar de categorías por extensión
EXTENSIONES_DEFAULT = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff"],
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv", ".odt", ".rtf"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Audios": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Codigo": [".py", ".js", ".html", ".css", ".json", ".sql", ".cpp", ".java", ".sh", ".bat", ".php", ".ts"],
    "Ejecutables": [".exe", ".msi", ".apk", ".iso"],
}

FILES_TO_IGNORE = {
    "organizador.py",
    "app.py",
    "history.json",
    "requirements.txt",
    "README.md",
    "license.md",
    ".gitignore"
}


def bytes_a_humano(num_bytes):
    """Convierte bytes a formato legible (KB, MB, GB)."""
    if num_bytes is None:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} PB"


class FileOrganizer:
    def __init__(self, extensiones=None):
        self.extensiones = extensiones or EXTENSIONES_DEFAULT

    def _obtener_categoria_extension(self, extension):
        ext = extension.lower()
        for cat, list_ext in self.extensiones.items():
            if ext in list_ext:
                return cat
        return "Otros"

    def _obtener_categoria_fecha(self, mtime):
        dt = datetime.fromtimestamp(mtime)
        return dt.strftime("%Y\\%Y-%m")

    def _obtener_categoria_tamano(self, num_bytes):
        mb = num_bytes / (1024 * 1024)
        if mb < 1.0:
            return "Pequeños (< 1 MB)"
        elif mb < 100.0:
            return "Medianos (1-100 MB)"
        else:
            return "Grandes (> 100 MB)"

    def calcular_destino(self, nombre_archivo, mtime, size_bytes, modo="category"):
        _, ext = os.path.splitext(nombre_archivo)
        if modo == "date":
            return self._obtener_categoria_fecha(mtime)
        elif modo == "size":
            return self._obtener_categoria_tamano(size_bytes)
        else:
            return self._obtener_categoria_extension(ext)

    def scan(self, ruta, modo="category"):
        """Escanea el directorio y devuelve vista previa e estadísticas."""
        if not os.path.exists(ruta) or not os.path.isdir(ruta):
            raise ValueError(f"La ruta '{ruta}' no existe o no es un directorio válido.")

        archivos_previo = []
        desglose = {}
        total_bytes = 0
        total_archivos = 0

        for item in os.listdir(ruta):
            path_item = os.path.join(ruta, item)

            # Ignorar carpetas y archivos propios de la aplicación
            if os.path.isdir(path_item) or item in FILES_TO_IGNORE or item.startswith('.'):
                continue

            try:
                stat = os.stat(path_item)
                size_bytes = stat.st_size
                mtime = stat.st_mtime
            except Exception:
                continue

            destino_rel = self.calcular_destino(item, mtime, size_bytes, modo)

            if destino_rel not in desglose:
                desglose[destino_rel] = {"count": 0, "size_bytes": 0}
            desglose[destino_rel]["count"] += 1
            desglose[destino_rel]["size_bytes"] += size_bytes

            total_bytes += size_bytes
            total_archivos += 1

            archivos_previo.append({
                "filename": item,
                "size_bytes": size_bytes,
                "size_human": bytes_a_humano(size_bytes),
                "mtime": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "target_folder": destino_rel,
                "extension": os.path.splitext(item)[1].lower() or "sin ext"
            })

        for cat in desglose:
            desglose[cat]["size_human"] = bytes_a_humano(desglose[cat]["size_bytes"])

        return {
            "folder_path": ruta,
            "mode": modo,
            "total_files": total_archivos,
            "total_size_bytes": total_bytes,
            "total_size_human": bytes_a_humano(total_bytes),
            "breakdown": desglose,
            "files": archivos_previo
        }

    def organize(self, ruta, modo="category", dry_run=False):
        """Ejecuta la organización de la carpeta o realiza simulación."""
        scan_res = self.scan(ruta, modo)

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "message": f"Simulación completada. {scan_res['total_files']} archivos serían organizados.",
                "scan": scan_res
            }

        movimientos = []
        errores = []

        for item_data in scan_res["files"]:
            orig_name = item_data["filename"]
            target_folder_rel = item_data["target_folder"]
            orig_path = os.path.join(ruta, orig_name)

            dest_dir = os.path.join(ruta, target_folder_rel)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, orig_name)

            # Resolver colisiones si el archivo ya existe en destino
            if os.path.exists(dest_path) and dest_path != orig_path:
                base_name, ext = os.path.splitext(orig_name)
                counter = 1
                while os.path.exists(dest_path):
                    nuevo_nombre = f"{base_name}_{counter}{ext}"
                    dest_path = os.path.join(dest_dir, nuevo_nombre)
                    counter += 1

            try:
                shutil.move(orig_path, dest_path)
                movimientos.append({
                    "original": orig_path,
                    "destino": dest_path,
                    "target_folder": target_folder_rel,
                    "filename": os.path.basename(dest_path)
                })
            except Exception as e:
                errores.append({"file": orig_name, "error": str(e)})

        # Guardar en historial para permitir Deshacer
        if movimientos:
            self._guardar_historial(ruta, movimientos, modo)

        return {
            "success": True,
            "dry_run": False,
            "moved_count": len(movimientos),
            "error_count": len(errores),
            "movimientos": movimientos,
            "errores": errores,
            "scan_after": self.scan(ruta, modo)
        }

    def _guardar_historial(self, ruta, movimientos, modo):
        hist_path = os.path.join(ruta, "history.json")
        historia = []
        if os.path.exists(hist_path):
            try:
                with open(hist_path, "r", encoding="utf-8") as f:
                    historia = json.load(f)
            except Exception:
                historia = []

        registro = {
            "id": len(historia) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modo": modo,
            "count": len(movimientos),
            "items": movimientos
        }
        historia.append(registro)

        try:
            with open(hist_path, "w", encoding="utf-8") as f:
                json.dump(historia, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"No se pudo guardar el historial: {e}")

    def undo_last(self, ruta):
        """Revierte la última sesión de organización realizada en el directorio."""
        hist_path = os.path.join(ruta, "history.json")
        if not os.path.exists(hist_path):
            return {"success": False, "message": "No hay historial de cambios registrado en esta carpeta."}

        try:
            with open(hist_path, "r", encoding="utf-8") as f:
                historia = json.load(f)
        except Exception:
            return {"success": False, "message": "No se pudo leer el archivo de historial."}

        if not historia:
            return {"success": False, "message": "El historial de cambios está vacío."}

        ultimo = historia.pop()
        revertidos = 0
        errores = []

        for item in reversed(ultimo["items"]):
            src = item["destino"]
            dst = item["original"]

            if os.path.exists(src):
                try:
                    dst_dir = os.path.dirname(dst)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir, exist_ok=True)

                    shutil.move(src, dst)
                    revertidos += 1
                except Exception as e:
                    errores.append({"file": src, "error": str(e)})

        # Actualizar archivo de historial
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(historia, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "reverted_count": revertidos,
            "error_count": len(errores),
            "remaining_history_count": len(historia),
            "message": f"Se revirtieron {revertidos} archivos a sus posiciones originales."
        }

    def find_duplicates(self, ruta):
        """Encuentra archivos duplicados comparando tamaño y hashes MD5."""
        if not os.path.exists(ruta) or not os.path.isdir(ruta):
            raise ValueError("Ruta inválida.")

        por_tamano = {}
        for root, dirs, files in os.walk(ruta):
            # No buscar en carpetas ocultas
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in FILES_TO_IGNORE]
            for file in files:
                if file in FILES_TO_IGNORE or file.startswith('.'):
                    continue
                path = os.path.join(root, file)
                try:
                    sz = os.path.getsize(path)
                    if sz > 0:
                        por_tamano.setdefault(sz, []).append(path)
                except Exception:
                    continue

        duplicados = []

        for sz, path_list in por_tamano.items():
            if len(path_list) < 2:
                continue

            hashes = {}
            for path in path_list:
                try:
                    hasher = hashlib.md5()
                    with open(path, 'rb') as f:
                        buf = f.read(65536)
                        while len(buf) > 0:
                            hasher.update(buf)
                            buf = f.read(65536)
                    h = hasher.hexdigest()
                    hashes.setdefault(h, []).append(path)
                except Exception:
                    continue

            for h, matches in hashes.items():
                if len(matches) > 1:
                    duplicados.append({
                        "hash": h,
                        "size_bytes": sz,
                        "size_human": bytes_a_humano(sz),
                        "wasted_bytes": sz * (len(matches) - 1),
                        "wasted_human": bytes_a_humano(sz * (len(matches) - 1)),
                        "files": matches
                    })

        total_desperdicio = sum(d["wasted_bytes"] for d in duplicados)

        return {
            "folder_path": ruta,
            "group_count": len(duplicados),
            "total_wasted_bytes": total_desperdicio,
            "total_wasted_human": bytes_a_humano(total_desperdicio),
            "groups": duplicados
        }


# Mantener la ejecución CLI tradicional como fallback
def organizar_carpeta(ruta):
    organizer = FileOrganizer()
    res = organizer.organize(ruta, modo="category", dry_run=False)
    print(f"Organización completada: {res['moved_count']} archivos movidos.")


if __name__ == "__main__":
    import sys
    ruta_target = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\ANGEL RAFAEL\Downloads"
    if os.path.exists(ruta_target):
        organizar_carpeta(ruta_target)
    else:
        print(f"La ruta {ruta_target} no existe.")
