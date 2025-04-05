import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import os

# Chemin vers le fichier où les prix scrappés sont enregistrés
CSV_FILE  = "/home/ubuntu/dash-dashboard/silver_prices.csv"

# Fonction pour charger les données depuis le CSV
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    # Si le fichier existe pas encore, on retourne un DataFrame vide avec les bonnes colonnes    
    return pd.DataFrame(columns=["Timestamp", "Price"])

# On intialise le Dash
app = dash.Dash(__name__)

# Layout = ce qu’on voit à l’écran
app.layout = html.Div([
    html.H1("Live Silver Price Dashboard"), #Titre
    
    dcc.Graph(id="price-chart"), # On affiche les prix
    
    dcc.Interval(
        id="interval-update",
        interval=5 * 60 * 1000,  # Refresh la page toutes les 5min
        n_intervals=0
    )
])

# Fonction pour appeler automatiquement toutes les 5 min pour mettre à jour le graphique
@app.callback(
    dash.Output("price-chart", "figure"),
    dash.Input("interval-update", "n_intervals")
)
def update_graph(n_intervals):
    df = load_data()
    
    if df.empty:
        return go.Figure()
        
    # Graphique avec les données disponibles
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Timestamp"],
        y=df["Price"],
        mode="lines+markers",
        name="Silver Price"
    ))
    
    fig.update_layout(
        title="Silver Price Over Time",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )

    return fig

# Lancement de l'app en local
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
