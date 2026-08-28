# Monitor de Precios Inteligente 🕷️💰

Una aplicación con **Interfaz Web en Localhost** e **Interfaz Gráfica de Escritorio** en Python para vigilar automáticamente el precio de cualquier producto en tiendas web y avisarte en tiempo real cuando entra en tu presupuesto objetivo.

---

## ✨ Características

- **🌐 Interfaz Web Localhost (`http://localhost:5000`):** Dashboard web responsivo con tema oscuro, abre automáticamente en el navegador y permite configurar URL, presupuesto e intervalo.
- **🖥️ Interfaz de Escritorio Novedosa:** Opción de ejecutarse como aplicación de escritorio nativa con `CustomTkinter`.
- **Multihilo (`Threading`):** El motor de Web Scraping se ejecuta en segundo plano sin congelar la interfaz ni la navegación web.
- **Modos de Escaneo:**
  - **▶ Vigilancia Continua:** Rastreo en bucle según la frecuencia definida (segundos).
  - **⚡ Escaneo Instantáneo:** Consulta el precio de la web inmediatamente a demanda.
- **Indicador de Estado Visual:** Badge en tiempo real que notifica el estado actual (🟢 *Vigilando*, 🔴 *Detenido*, 🔔 *¡Oferta Encontrada!*).
- **Consola de Registros Integrada:** Registro en tiempo real con estampa de tiempo (`datetime`).

---

## 🛠️ Tecnologías

- **Python 3.x**
- **Flask** (Servidor Web en Localhost `127.0.0.1:5000`)
- **CustomTkinter** (Interfaz gráfica de escritorio)
- **BeautifulSoup4** (Parsing y extracción del HTML)
- **Requests** (Peticiones HTTP)

---

## 🚀 Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install -r requeriments.txt
   ```

2. **Ejecutar en el Navegador Web (Localhost):**
   ```bash
   python app.py
   ```
   *(Abre automáticamente `http://localhost:5000` en tu navegador).*

3. **Ejecutar como Aplicación de Escritorio:**
   ```bash
   python main.py
   ```
