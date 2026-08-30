# 📈 Monitor de Precios de Cripto & Divisas PRO (con Interfaz Web GUI)

Plataforma financiera interactiva en tiempo real desarrollada en **Python**, **Flask** y **Chart.js** para el monitoreo contínuo de Criptomonedas y Pares de Divisas (Forex).

---

## ✨ Características Principales

- 🚀 **Cotizaciones en Tiempo Real**: Refresco automático cada 4 segundos de activos principales (Bitcoin, Ethereum, Solana, BNB, EUR/USD, GBP/USD, etc.).
- 📊 **Gráficos Interactivos (Chart.js)**: Gráficos de tendencias históricas de precios (1D, 7D, 1M) con área de degradado dinámico según ganancia/pérdida.
- 🔍 **Búsqueda de Tickers Personalizados**: Agrega cualquier activo financiero soportado por Yahoo Finance (ej: `LTC-USD`, `USDMXN=X`).
- 🔔 **Sistema de Alertas de Precio**: Configura límites objetivo máximos o mínimos y recibe notificaciones tipo Toast cuando se alcancen.
- 🧮 **Calculadora Conversora Cripto/Fiat**: Conversión instantánea de valores según cotización live.
- 💻 **Motor Híbrido CLI + Web GUI**: Funciona como aplicación web local (`app.py`) o como script directo en consola (`Cripto_chek.py`).

---

## 🛠️ Instalación

1. Instalar las dependencias de Python:
   ```bash
   pip install -r Requirements.txt
   ```

---

## 🚀 Cómo Iniciar la Aplicación Web

1. Navega al directorio del proyecto:
   ```bash
   cd "Proyecto 4 - Monitor de Precios de Cripto o Divisas"
   ```
2. Inicia el servidor Flask:
   ```bash
   python app.py
   ```
3. Abre tu navegador en:
   ```text
   http://localhost:5004
   ```

---

## 💻 Uso desde Consola (CLI Fallback)

```bash
python Cripto_chek.py
```
