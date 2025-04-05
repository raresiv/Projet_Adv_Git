import pandas as pd
import json
from datetime import datetime

# Charger les données existantes
df = pd.read_csv('silver_prices.csv', names=['timestamp', 'price'], skiprows=1)

# S’assurer que les timestamps sont bien en datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filtrer les données du jour
today = pd.Timestamp.now().normalize()
df_today = df[df['timestamp'].dt.date == today.date()]

if not df_today.empty:
    open_price = df_today.iloc[0]['price']
    close_price = df_today.iloc[-1]['price']
    change = close_price - open_price
    pct_change = (change / open_price) * 100
    volatility = df_today['price'].std()
    average_price = df_today['price'].mean()

    report = {
        "date": today.strftime('%Y-%m-%d'),
        "open_price": round(open_price, 3),
        "close_price": round(close_price, 3),
        "change": round(change, 3),
        "percent_change": round(pct_change, 2),
        "volatility": round(volatility, 3),
        "average_price": round(average_price, 3)
    }

    with open("daily_report.json", "w") as f:
        json.dump(report, f, indent=4)
