import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import os
import json

# Fichiers
CSV_FILE = "/home/ubuntu/dash-dashboard/silver_prices.csv"
REPORT_FILE = "/home/ubuntu/dash-dashboard/daily_report.json"

# Fonction pour charger les données du graphe
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df.columns = ["Timestamp", "Price"]
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame(columns=["Timestamp", "Price"])

# Fonction pour charger le rapport quotidien
def load_report():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            return json.load(f)
    return None

# Initialisation de Dash
app = dash.Dash(__name__)
app.title = "Silver Dashboard"

# Contenu du rapport
report = load_report()

# Layout principal
app.layout = html.Div([
    html.H1("💰 Live Silver Price Dashboard", style={"textAlign": "center"}),

    # Graphique des prix
    dcc.Graph(id="price-chart"),

    # Rafraîchissement automatique
    dcc.Interval(
        id="interval-update",
        interval=5 * 60 * 1000,  # Toutes les 5 minutes
        n_intervals=0
    ),

    html.H2("📊 Daily Report - 20h", style={"marginTop": "40px"}),

    html.Div(
        children=[
            html.P(f"📅 Date: {report['date']}"),
            html.P(f"🟢 Open Price: {report['open_price']} $"),
            html.P(f"🔴 Close Price: {report['close_price']} $"),
            html.P(f"📈 Change: {report['change']} $ ({report['percent_change']}%)"),
            html.P(f"📊 Volatility: {report['volatility']}"),
	    html.P(f"📉 Average Price: {report['average_price']} $")
        ] if report else [html.P("No report available yet.")],
        style={
            "padding": "20px",
            "margin": "20px auto",
            "maxWidth": "500px",
            "border": "1px solid #ccc",
            "borderRadius": "10px",
            "backgroundColor": "#f9f9f9"
        }
    ),
])

# Callback pour mettre à jour le graphique
@app.callback(
    dash.Output("price-chart", "figure"),
    dash.Input("interval-update", "n_intervals")
)
def update_graph(n):
    df = load_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Price'], mode='lines+markers', name='Silver Price'))
    fig.update_layout(title="Live Silver Price", xaxis_title="Time", yaxis_title="Price ($)", template="plotly_white")
    return fig

# Lancement de l'app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

