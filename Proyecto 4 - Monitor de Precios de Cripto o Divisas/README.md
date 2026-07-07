# Crypto Monitor CLI 🚀

Monitor de criptomonedas de alto rendimiento para terminal. Este script permite vigilar el Top 5 del mercado en tiempo real, utilizando el motor de Yahoo Finance para garantizar la conexión incluso en redes con restricciones estrictas (firewalls).

## ✨ Características

- ⚡ **Live Updates**: Actualización continua de precios directamente en la consola.
- 🕒 **Precisión**: Marca de tiempo (HH:MM:SS) para cada consulta exitosa.
- 🛡️ **Anti-Block**: Diseñado para evitar errores HTTP 403/429 mediante el uso de `yfinance`.
- 📊 **Visualización Limpia**: Limpieza automática de pantalla para una lectura cómoda.

## 🛠️ Tecnologías utilizadas

- **Python 3.x**
- **yfinance**: Extracción de datos financieros.
- **os & time**: Gestión de interfaz de consola y temporizadores.

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
   cd crypto-monitor-cli
   ```
