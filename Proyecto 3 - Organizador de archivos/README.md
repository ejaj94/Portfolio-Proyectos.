# 📂 Organizador de Archivos PRO (con Interfaz Web GUI)

Un organizador de archivos inteligente, rápido y seguro desarrollado en **Python** y **Flask**, equipado con una interfaz gráfica moderna (Dashboard Web) e intuitiva para gestionar y clasificar tu almacenamiento local en segundos.

---

## ✨ Características Principales

- 🚀 **Interfaz Web Moderna (Localhost)**: Visualiza tus archivos en una pantalla interactiva con indicadores de uso de espacio y desglose por categorías.
- ⚡ **Múltiples Criterios de Organización**:
  - **Por Categoría/Extensión**: Imágenes, Documentos, Vídeos, Audios, Comprimidos, Código, Ejecutables, etc.
  - **Por Fecha**: Agrupa archivos por Año y Mes (`YYYY/YYYY-MM`).
  - **Por Tamaño**: Filtra entre Pequeños (`< 1 MB`), Medianos (`1 - 100 MB`) y Grandes (`> 100 MB`).
- 🧪 **Modo Simulación (Dry-Run)**: Revisa exactamente cómo se organizarán tus archivos antes de realizar ningún movimiento real.
- ↩️ **Función Deshacer (Undo/Rollback)**: Revierte en un solo clic cualquier sesión de organización previa gracias al registro en historial (`history.json`).
- 🔍 **Buscador de Duplicados**: Escanea tu almacenamiento detectando archivos idénticos mediante algoritmos de Hash (MD5) e identifica espacio malgastado.
- 🎯 **Accesos Directos**: Un clic para seleccionar la carpeta de Descargas, Documentos, Escritorio, Imágenes, Vídeos o Música del usuario activo.

---

## 🛠️ Requisitos de Instalación

- **Python 3.8+**
- Dependencias de Python:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🚀 Cómo Iniciar la Aplicación Web

1. Abre la terminal en el directorio del proyecto:
   ```bash
   cd "Proyecto 3 - Organizador de archivos"
   ```
2. Inicia el servidor web Flask:
   ```bash
   python app.py
   ```
3. Abre tu navegador web e ingresa a:
   ```text
   http://127.0.0.1:5000
   ```

---

## 💻 Uso desde la Línea de Comandos (CLI Fallback)

Si prefieres ejecutar el organizador en consola sin interfaz gráfica:
```bash
python organizador.py "C:\Ruta\A\Tu\Carpeta"
```

---

## 🛡️ Seguridad

- Ignora automáticamente archivos propios del sistema, carpetas y scripts de ejecución.
- Colisión inteligente de nombres: si existe un archivo con el mismo nombre en el destino, le asignará un sufijo numérico (`archivo_1.txt`) sin sobrescribir nada.
