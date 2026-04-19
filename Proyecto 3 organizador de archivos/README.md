# 📂 Organizador de Archivos Automático

Un script de Python sencillo y eficiente para mantener tu carpeta de **Descargas** (o cualquier otra) impecable. Clasifica archivos automáticamente en carpetas según su extensión.

## ✨ Características

- 🚀 **Clasificación instantánea**: Mueve archivos a carpetas como Imagenes, Documentos, Videos, etc.
- 🛡️ **Seguridad**: No mueve carpetas existentes ni el propio script de ejecución.
- 🛠️ **Personalizable**: Fácil de añadir nuevas extensiones o categorías en el diccionario principal.
- 💻 **Multiplataforma**: Funciona en Windows, macOS y Linux.

## 🛠️ Requisitos

- [Python 3.x](https://python.org) instalado.
- No requiere librerías externas (usa `os` y `shutil` que vienen con Python).

## 🚀 Instalación y Uso

1. **Clona o descarga** este repositorio.
2. Abre el archivo `organizador.py`.
3. Modifica la variable `ruta_descargas` con la dirección de tu carpeta:
   ```python
   ruta_descargas = r"C:\Users\TuUsuario\Downloads"
   ```

Categorías incluidas
El script organiza los archivos en:
Imagenes: .jpg, .jpeg, .png, .gif
Documentos: .pdf, .docx, .txt, .xlsx
Videos: .mp4, .mov, .avi
Audios: .mp3, .wav
Comprimidos: .zip, .rar, .tar

📝 Notas de seguridad
El script ignora directorios para evitar mover carpetas dentro de otras.
Se recomienda cerrar archivos abiertos antes de ejecutar para evitar errores de permisos.
