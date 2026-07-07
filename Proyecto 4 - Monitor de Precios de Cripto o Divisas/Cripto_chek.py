#Importamos nuestras bibliotecas:
import yfinance as yf
import time
import os
from datetime import datetime

def obtener_precio_cripto(ticker_simbolo):
    """
    Obtiene el precio en tiempo real de una criptomoneda 
    usando el motor financiero de Yahoo Finance.
    """
    try:
        # Configuramos el activo (Ticker)
        # Ejemplo: "BTC-USD" para Bitcoin en Dólares
        activo = yf.Ticker(ticker_simbolo)
        # Usamos el fast info para obtener la ultima actualizacion disponible:
        return activo.fast_info['last_price']
    except:
        return None
    
    # Definimos la(s) moneda(s) a consultar:
    # Definimos el Top 5 de criptomonedas (puedes cambiarlas a tu gusto):

monedas_top = ["BTC-USD", "ETH-USD", "STETH-USD", "BNB-USD", "SOL-USD"]

#Creamos un bucle para que se actualize a cada momento:

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

#Obtenemos la fecha y hora de la ultima actualizacion:
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print(f"==========================================")
    print(f"   MONITOR CRIPTO - TIEMPO REAL")
    print(f"   Última actualización: {ahora}")
    print(f"==========================================\n")

   #Recorre y muestra los precios:

    for simbolo in monedas_top:
        precio = obtener_precio_cripto(simbolo)
        if precio:
            print(f"🔹 {simbolo:<10} | Precio: ${precio:,.2f}")
        else:
            print(f"❌ {simbolo:<10} | Error de conexión")

    print("\n[ Presiona Ctrl+C para detener el monitor ]")
    
    # 4. Pausa de 1 segundo para no saturar la red.
    time.sleep(1)

