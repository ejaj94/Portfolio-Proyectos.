import yfinance as yf
import requests
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

BINANCE_PAIRS = {
    "BTC-USD": "BTCUSDT",
    "ETH-USD": "ETHUSDT",
    "BNB-USD": "BNBUSDT",
    "SOL-USD": "SOLUSDT",
    "XRP-USD": "XRPUSDT",
    "ADA-USD": "ADAUSDT",
    "DOGE-USD": "DOGEUSDT",
    "AVAX-USD": "AVAXUSDT",
}


class CryptoMonitorEngine:
    def __init__(self):
        self._forex_cache = None
        self._forex_cache_time = 0

    def _clean_val(self, val):
        if val is None:
            return 0.0
        try:
            f = float(val)
            return 0.0 if math.isnan(f) else f
        except (ValueError, TypeError):
            return 0.0

    def _fetch_crypto_rest(self, symbol):
        """Consulta cotización cripto directa vía Binance API."""
        b_sym = BINANCE_PAIRS.get(symbol, symbol.replace("-", ""))
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={b_sym}"
            res = requests.get(url, timeout=3.5).json()
            price = self._clean_val(res.get("lastPrice"))
            change_pct = self._clean_val(res.get("priceChangePercent"))
            high = self._clean_val(res.get("highPrice"))
            low = self._clean_val(res.get("lowPrice"))
            volume = self._clean_val(res.get("volume"))

            if price > 0:
                change = price * (change_pct / 100.0)
                prev_close = price - change
                return {
                    "symbol": symbol,
                    "name": NOMBRE_AMIGABLE.get(symbol, symbol),
                    "price": round(price, 2),
                    "prev_close": round(prev_close, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "volume": volume,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
        except Exception:
            pass
        return None

    def _fetch_forex_rates(self):
        """Consulta tasas forex actualizadas vía Open Exchange Rates REST API."""
        now = time.time()
        if self._forex_cache and (now - self._forex_cache_time < 30):
            return self._forex_cache

        try:
            url = "https://open.er-api.com/v6/latest/USD"
            res = requests.get(url, timeout=3.5).json()
            rates = res.get("rates", {})
            if rates:
                self._forex_cache = rates
                self._forex_cache_time = now
                return rates
        except Exception:
            pass
        return self._forex_cache or {}

    def _fetch_forex_rest(self, symbol):
        rates = self._fetch_forex_rates()
        if not rates:
            return None

        try:
            price = 0.0
            if symbol == "EURUSD=X" and "EUR" in rates:
                price = 1.0 / rates["EUR"]
            elif symbol == "GBPUSD=X" and "GBP" in rates:
                price = 1.0 / rates["GBP"]
            elif symbol == "USDJPY=X" and "JPY" in rates:
                price = rates["JPY"]
            elif symbol == "USDBRL=X" and "BRL" in rates:
                price = rates["BRL"]
            elif symbol == "EURGBP=X" and "EUR" in rates and "GBP" in rates:
                price = rates["GBP"] / rates["EUR"]
            elif symbol == "USDMXN=X" and "MXN" in rates:
                price = rates["MXN"]

            if price > 0:
                return {
                    "symbol": symbol,
                    "name": NOMBRE_AMIGABLE.get(symbol, symbol),
                    "price": round(price, 4),
                    "prev_close": round(price, 4),
                    "change": 0.0,
                    "change_pct": 0.0,
                    "high": round(price * 1.002, 4),
                    "low": round(price * 0.998, 4),
                    "volume": 0.0,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
        except Exception:
            pass
        return None

    def get_ticker_info(self, symbol):
        """Obtiene métricas en tiempo real intentando REST APIs ultra-rápidas con yfinance fallback."""
        # 1. Si es cripto, intentar Binance API
        if "-USD" in symbol or symbol in BINANCE_PAIRS:
            c_data = self._fetch_crypto_rest(symbol)
            if c_data:
                return c_data

        # 2. Si es forex, intentar REST Forex API
        if "=X" in symbol:
            f_data = self._fetch_forex_rest(symbol)
            if f_data:
                return f_data

        # 3. Fallback a yfinance convirtiendo fast_info a dict
        try:
            ticker = yf.Ticker(symbol)
            fast_dict = dict(ticker.fast_info)

            price = self._clean_val(fast_dict.get('lastPrice') or fast_dict.get('last_price'))
            prev_close = self._clean_val(fast_dict.get('previousClose') or fast_dict.get('previous_close') or fast_dict.get('open'))
            high = self._clean_val(fast_dict.get('dayHigh') or fast_dict.get('day_high'))
            low = self._clean_val(fast_dict.get('dayLow') or fast_dict.get('day_low'))
            volume = self._clean_val(fast_dict.get('lastVolume') or fast_dict.get('last_volume'))

            if price > 0:
                change = price - prev_close if prev_close > 0 else 0.0
                change_pct = (change / prev_close) * 100 if prev_close > 0 else 0.0
                decimals = 4 if "=X" in symbol else 2

                return {
                    "symbol": symbol,
                    "name": NOMBRE_AMIGABLE.get(symbol, symbol),
                    "price": round(price, decimals),
                    "prev_close": round(prev_close, decimals),
                    "change": round(change, decimals),
                    "change_pct": round(change_pct, 2),
                    "high": round(high, decimals),
                    "low": round(low, decimals),
                    "volume": volume,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
        except Exception:
            pass

        return {
            "symbol": symbol,
            "name": NOMBRE_AMIGABLE.get(symbol, symbol),
            "price": 0.0,
            "error": "Cotización no disponible",
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
