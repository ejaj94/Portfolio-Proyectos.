# 🛡️ SentinelNode: Dashboard de Seguridad y Monitoreo

SentinelNode es una herramienta avanzada de monitoreo de sistemas desarrollada en Python. Permite visualizar en tiempo real los procesos activos del sistema operativo, proporcionando una interfaz moderna y oscura diseñada para administradores y entusiastas de la ciberseguridad.

Este proyecto forma parte de mi portafolio como **Desarrollador Python Junior**, demostrando habilidades en programación asíncrona, interfaces gráficas modernas y manejo de recursos del sistema.

## 🚀 Características principales

- **Monitoreo en Tiempo Real:** Visualización dinámica de procesos (PID, Nombre y Estado).
- **Interfaz Moderna (UI):** Construida con `CustomTkinter` para una experiencia de usuario fluida y estética _Dark Mode_.
- **Arquitectura Eficiente:** Uso del método `.after()` para actualizaciones periódicas sin bloquear el hilo principal de la interfaz.
- **Gestión de Recursos:** Integración con la biblioteca `psutil` para la extracción precisa de datos del sistema.
- **Logs Interactivos:** Consola integrada que informa sobre el estado del escaneo.

## 🛠️ Tecnologías utilizadas

- **Python 3.x**
- **CustomTkinter:** Para la interfaz de usuario moderna.
- **psutil:** Para la gestión y consulta de procesos del sistema.
- **Logística de Clases:** Programación Orientada a Objetos (POO).

## 📦 Instalación y Uso

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com
   cd sentinel-node
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   > **Nota:** Se recomienda ejecutar la terminal como **Administrador** para que el programa tenga permisos de lectura sobre todos los procesos del sistema.
   ```bash
   python main.py
   ```

## 📸 Capturas de pantalla

_(Aquí puedes arrastrar una imagen de tu programa funcionando cuando lo subas a GitHub)_

## 🛡️ Seguridad y Buenas Prácticas

Este software ha sido desarrollado con fines educativos y de monitoreo personal. Implementa manejo de excepciones para evitar cierres inesperados al intentar acceder a procesos protegidos del sistema.

---

Desarrollado con ❤️ por [Tu Nombre/Usuario]
