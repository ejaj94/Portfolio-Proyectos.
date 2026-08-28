# Proyecto 1: Calculadora de Calorías y Tasa Metabólica Basal

Este proyecto es una calculadora nutricional completa en Python con soporte para **Servidor Web Localhost**, **Interfaz Gráfica Desktop (GUI)** y **Modo Consola (CLI)**.

## Archivos del Proyecto

- `App.py`: Punto de entrada principal (inicia la interfaz de escritorio o la versión web/consola mediante argumentos).
- `web_app.py`: Servidor web Flask para ejecutar la aplicación en `http://127.0.0.1:5000`.
- `gui.py`: Módulo de interfaz gráfica de escritorio con CustomTkinter.
- `Calculos.py`: Módulo matemático con las fórmulas de TMB y cálculo calórico.
- `templates/index.html` & `static/style.css`: Plantillas y estilos para la interfaz web.
- `requirements.txt`: Lista de dependencias del proyecto.

## Cómo Ejecutar

1. **Servidor Web en Localhost (Navegador)** 🌐:
   ```bash
   python web_app.py
   ```
   o alternativamente:
   ```bash
   python App.py --web
   ```
   Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador preferido.

2. **Interfaz Gráfica de Escritorio (Desktop GUI)** 💻:
   ```bash
   python App.py
   ```

3. **Modo Consola (CLI)** 💻:
   ```bash
   python App.py --cli
   ```

## Características

- **Servidor Web Local (Localhost)**:
  - Diseño responsive oscuro con CSS3 moderno.
  - Cálculo instantáneo mediante API REST JSON en `/api/calcular` sin recargar la página.
- **Validaciones de Seguridad**: Evita valores negativos o no numéricos.
- **Misma Lógica Matemática**: Todas las modalidades comparten el mismo núcleo en `Calculos.py`.
