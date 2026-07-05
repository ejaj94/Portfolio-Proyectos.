# Proyecto 11 - Generador de CV con Interfaz Gráfica

Una aplicación de escritorio completa en Python (Tkinter) para generar Currículums profesionales en PDF.

## 🚀 Características

* **Interfaz Gráfica Trilingüe**: La aplicación puede usarse en Inglés, Español o Portugués de Portugal.
* **Dinámico**: A diferencia de versiones anteriores, no hay datos *hardcodeados*. Cualquier usuario puede introducir su información.
* **Foto de perfil con máscara circular**: Sube tu foto y la aplicación le aplicará una máscara redonda antes de colocarla en el CV.
* **Diseño Profesional (SOLID)**: Construido siguiendo el principio de responsabilidad única (SRP), inversión de dependencias (DIP) y más. La UI está totalmente separada del motor de PDF.

## 🛠️ Instalación y Uso

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
3. Rellena tus datos, selecciona una foto, elige el idioma del PDF (ES, EN, PT) y dale a **Generar CV**.

## 🏗️ Arquitectura (SOLID)

- **`core/`**: Lógica central para la generación de PDFs (ReportLab).
- **`gui/`**: Componentes visuales de Tkinter (Ventana principal, Pestañas, Sistema de Tema oscuro).
- **`services/`**: Orquestación y lógica de negocio (`cv_service.py`, `i18n.py`).
- **`languages/`**: El proveedor de contenido dinámico (`dynamic.py`) que se encarga de acoplar el formulario con el motor de PDF.
