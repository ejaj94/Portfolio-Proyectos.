# Monitor de Precios Inteligente 🕷️💰

Una aplicación de escritorio moderna con **Interfaz Gráfica (GUI)** en Python para vigilar automáticamente el precio de cualquier producto en tiendas web y avisarte en tiempo real cuando entra en tu presupuesto objetivo.

---

## ✨ Características

- **Interfaz Gráfica Moderna (GUI):** Diseñada con `CustomTkinter` en modo oscuro, con campos interactivos para configurar la URL, presupuesto e intervalo de revisión.
- **Multihilo (`Threading`):** El motor de Web Scraping se ejecuta en segundo plano sin congelar ni bloquear la interfaz de usuario.
- **Modos de Escaneo:**
  - **▶ Vigilancia Continua:** Rastreo en bucle según la frecuencia definida (segundos).
  - **⚡ Escaneo Instantáneo:** Consulta el precio de la web inmediatamente a demanda.
- **Indicador de Estado Visual:** Badge en tiempo real que notifica el estado actual (🟢 *Vigilando*, 🔴 *Detenido*, 🔔 *¡Oferta Encontrada!*).
- **Consola de Registros Integrada:** Registro con estampa de tiempo (`datetime`) de cada consulta y errores de conexión.

---

## 🛠️ Tecnologías

- **Python 3.x**
- **CustomTkinter** (Interfaz gráfica moderna de escritorio)
- **BeautifulSoup4** (Parsing y extracción del HTML)
- **Requests** (Peticiones HTTP)
- **Threading** (Concurrencia y tareas en segundo plano)

---

## 🚀 Instalación y Uso

1. **Instalar dependencias:**
   ```bash
   pip install -r requeriments.txt
   ```

2. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```
