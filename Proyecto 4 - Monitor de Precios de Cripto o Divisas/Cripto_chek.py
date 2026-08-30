import yfinance as yf
import time
import os
import math
from datetime import datetime

DEFAULT_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD"]
DEFAULT_FOREX = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDBRL=X", "EURGBP=X", "USDMXN=X"]

NOMBRE_AMIGABLE = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "BNB-USD": "BNB Chain",
    "SOL-USD": "Solana",
    "XRP-USD": "Ripple",
    "ADA-USD": "Cardano",
    "DOGE-USD": "Dogecoin",
    "AVAX-USD": "Avalanche",
    "EURUSD=X": "EUR / USD",
    "GBPUSD=X": "GBP / USD",
    "USDJPY=X": "USD / JPY",
    "USDBRL=X": "USD / BRL",
    "EURGBP=X": "EUR / GBP",
    "USDMXN=X": "USD / MXN",
}


class CryptoMonitorEngine:
    def __init__(self):
        pass

    def _clean_val(self, val):
        if val is None:
            return 0.0
        try:
            f = float(val)
            return 0.0 if math.isnan(f) else f
        except (ValueError, TypeError):
            return 0.0

    def get_ticker_info(self, symbol):
        """Obtiene métricas en tiempo real leyendo tanto camelCase como snake_case de fast_info."""
        try:
            ticker = yf.Ticker(symbol)
            fast = ticker.fast_info

            price = self._clean_val(fast.get('lastPrice') or fast.get('last_price'))
            prev_close = self._clean_val(fast.get('previousClose') or fast.get('previous_close') or fast.get('open'))
            high = self._clean_val(fast.get('dayHigh') or fast.get('day_high'))
            low = self._clean_val(fast.get('dayLow') or fast.get('day_low'))
            volume = self._clean_val(fast.get('lastVolume') or fast.get('last_volume'))

            # Fallback a history si fast_info está vacío
            if price <= 0:
                hist = ticker.history(period="1d")
                if not hist.empty:
                    price = float(hist["Close"].iloc[-1])
                    high = float(hist["High"].iloc[-1])
                    low = float(hist["Low"].iloc[-1])
                    prev_close = float(hist["Open"].iloc[-1])

            if prev_close > 0 and price > 0:
                change = price - prev_close
                change_pct = (change / prev_close) * 100
            else:
                change = 0.0
                change_pct = 0.0

            friendly_name = NOMBRE_AMIGABLE.get(symbol, symbol)
            decimals = 4 if "=X" in symbol else 2

            return {
                "symbol": symbol,
                "name": friendly_name,
                "price": round(price, decimals),
                "prev_close": round(prev_close, decimals),
                "change": round(change, decimals),
                "change_pct": round(change_pct, 2),
                "high": round(high, decimals),
                "low": round(low, decimals),
                "volume": volume,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
        except Exception as e:
            return {
                "symbol": symbol,
                "name": NOMBRE_AMIGABLE.get(symbol, symbol),
                "price": 0.0,
                "error": str(e),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

    def get_multiple_tickers(self, symbols):
        """Obtiene datos de múltiples activos."""
        results = []
        for sym in symbols:
            info = self.get_ticker_info(sym)
            results.append(info)
        return results

    def get_history(self, symbol, period="1d", interval="15m"):
        """Obtiene datos históricos para renderizar gráficos."""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                return {"success": False, "message": "Sin datos históricos"}

            labels = []
            prices = []

            for index, row in df.iterrows():
                if period == "1d":
                    labels.append(index.strftime("%H:%M"))
                else:
                    labels.append(index.strftime("%d/%m %H:%M"))
                prices.append(round(float(row["Close"]), 2 if "=X" not in symbol else 4))

            return {
                "success": True,
                "symbol": symbol,
                "period": period,
                "labels": labels,
                "prices": prices
            }
        except Exception as e:
            return {"success": False, "message": str(e)}


# CLI Fallback Tradicional
def iniciar_monitor_cli():
    engine = CryptoMonitorEngine()
    monedas_top = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"]

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print("==========================================")
        print("   MONITOR CRIPTO Y DIVISAS - TIEMPO REAL")
        print(f"   Última actualización: {ahora}")
        print("==========================================\n")

        for simbolo in monedas_top:
            data = engine.get_ticker_info(simbolo)
            if data and data.get("price", 0) > 0:
                signo = "+" if data["change"] >= 0 else ""
                print(f"🔹 {data['symbol']:<10} | Precio: ${data['price']:,.2f} | 24h: {signo}{data['change_pct']}%")
            else:
                print(f"❌ {simbolo:<10} | Error de conexión")

        print("\n[ Presiona Ctrl+C para detener el monitor ]")
        time.sleep(2)


if __name__ == "__main__":
    try:
        iniciar_monitor_cli()
    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario.")
