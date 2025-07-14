import streamlit as st
import pandas as pd
import yfinance as yf
from ta.momentum import RSIIndicator
import datetime

st.set_page_config(page_title="Panel RSI", layout="wide")

st.title("📊 Panel RSI - Actualizado en Vivo")

# Lista de acciones
tickers = [
    "NVDA","ASML","TXN","JPM","CRM","MMM","AAPL","TMUS","INTU","WMT",
    "AXP","TRV","MSFT","CSCO","VZ","V","DIS","ABBV","AMZN","ISRG",
    "BKNG","JNJ","GS","MS","GOOGL","AZN","AMAT","HD","MCD","PFE",
    "META","LIN","AMGN","PG","MRK","PM","TSLA","PEP","HON","UNH",
    "CAT","CL","AVGO","AMD","PDD","KO","BA","CB","NFLX","QCOM",
    "CMCSA","IBM","NKE","COP","COST","ADBE","MU","CVX","SHW","LMT"
]

# Fecha de análisis
fecha_fin = datetime.date.today()
fecha_ini = fecha_fin - datetime.timedelta(days=90)

rsi_data = []

with st.spinner("Cargando datos y calculando RSI..."):
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=fecha_ini, end=fecha_fin, progress=False, auto_adjust=False)
            if df.empty or len(df) < 15:
                continue

           close = df["Close"]
if isinstance(close, pd.DataFrame):
    close = close.squeeze()

if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]
rsi = RSIIndicator(close=close, window=14).rsi()

            ultimo_rsi = round(rsi.iloc[-1], 2)
            rsi_data.append({"Ticker": ticker, "RSI": ultimo_rsi})
        except Exception as e:
            st.warning(f"No se pudo procesar {ticker}: {e}")

# Crear DataFrame
df_rsi = pd.DataFrame(rsi_data).sort_values(by="RSI").reset_index(drop=True)

# Estilo de colores
def color_rsi(val):
    if val <= 30:
        return "background-color: #ff4d4d; color: white"
    elif val <= 40:
        return "background-color: #fff066"
    elif val >= 70:
        return "background-color: #85e085"
    return ""

# Mostrar tabla con estilo
st.subheader("RSI de Acciones")
st.dataframe(df_rsi.style.applymap(color_rsi, subset=["RSI"]), use_container_width=True)
