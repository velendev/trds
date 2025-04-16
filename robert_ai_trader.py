import requests
import yfinance as yf
import pandas as pd

API_KEY = "IABQ6677LMDLV2Q8" # <-- la tua vera API key di Alpha Vantage

# ==== Calcolo RSI ====
def calcola_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)

# ==== BTC da Alpha Vantage ====
def get_rsi_btc():
    url = f"https://www.alphavantage.co/query?function=RSI&symbol=BTCUSD&interval=60min&time_period=14&series_type=close&apikey={API_KEY}"
    response = requests.get(url)
    
    try:
        data = response.json()
        last_date = list(data['Technical Analysis: RSI'].keys())[0]
        rsi = float(data['Technical Analysis: RSI'][last_date]['RSI'])
        return round(rsi, 2)
    except Exception as e:
        print("Errore RSI BTC:", e)
        return None

# ==== XAU/USD da Yahoo Finance ====
def get_rsi_xau():
    df = yf.download("GC=F", period="15d", interval="1h")
    if df.empty or 'Close' not in df:
        return None
    close = df['Close']
    rsi_series = calcola_rsi(close)
    rsi_value = rsi_series if isinstance(rsi_series, float) else rsi_series.iloc[-1]
    return round(rsi_value, 2) 

# ==== Analisi ====
def analizza_rsi(rsi):
    if rsi is None or pd.isna(rsi):
        return "Dati non disponibili"
    if rsi > 80:
        return f"RSI: {rsi} | Probabilità discesa: 85% | Consiglio: Short possibile"
    elif rsi > 70:
        return f"RSI: {rsi} | Probabilità discesa: 65% | Consiglio: Attendere"
    elif rsi > 60:
        return f"RSI: {rsi} | Trend forte"
    elif rsi >= 40:
        return f"RSI: {rsi} | Zona neutra, attendere conferme"
    elif rsi >= 30:
        return f"RSI: {rsi} | Probabilità salita: 60% | Consiglio: Preparati al long"
    else:
        return f"RSI: {rsi} | Probabilità salita: 85% | Consiglio: Forte segnale long"

# ==== Esecuzione ====
print("=== Analisi BTC/USD ===")
btc_rsi = get_rsi_btc()
print(analizza_rsi(btc_rsi))

print("\n=== Analisi XAU/USD ===")
xau_rsi = get_rsi_xau()
print(analizza_rsi(xau_rsi))