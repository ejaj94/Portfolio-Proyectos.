# app_entregador (Módulo Integrado)

Módulo profesional para la gestión de repartidores y verificación básica de documentos mediante OCR, integrado en la plataforma principal de entregas.

## Configuración del Sistema

Este módulo se carga automáticamente al iniciar la aplicación principal. Las variables de entorno de configuración son:

- `APP_ADMIN_PASSWORD`: Contraseña del administrador (Por defecto: `adminpass`).
- `APP_SECRET_KEY`: Clave secreta global para el cifrado de sesiones de Flask.

### Integración de OCR (Opcional)
Para mejorar la lectura y extracción de texto de las licencias y documentos subidos:
1. Regístrate en [OCR.space](https://ocr.space) y obtén una API Key gratuita.
2. Define la variable de entorno `OCR_SPACE_API_KEY` antes de arrancar el servidor.
3. Si la clave no está presente, el sistema intentará usar `pytesseract` de forma local (requiere instalación previa de Tesseract en el sistema operativo).

## Instrucciones de Ejecución

Ya no es necesario arrancar este módulo de forma independiente en el puerto 5001. Al iniciar la aplicación global desde la raíz del proyecto, el módulo se acoplará automáticamente.

1. Instala las dependencias globales en tu entorno virtual:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicia la plataforma de entregas completa ejecutando el archivo principal:
   ```bash
   python app.py
   ```
3. Accede a las funciones del repartidor a través de las siguientes rutas unificadas:
   - **Formulario de Registro:** [http://127.0.0](http://127.0.0)
   - **Panel de Administración:** [http://127.0.0](http://127.0.0)

## Limpieza de Archivos
Puedes ejecutar el script `run_cleanup.bat` de forma periódica para eliminar del servidor los documentos de identidad subidos que tengan más de 30 días de antigüedad.
