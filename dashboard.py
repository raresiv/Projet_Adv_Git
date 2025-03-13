import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import os

# File where the scraped data is stored
CSV_FILE  = "/home/ubuntu/dash-dashboard/silver_prices.csv"

# Function to read data
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame(columns=["Timestamp", "Price"])

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Live Silver Price Dashboard"),
    
    dcc.Graph(id="price-chart"),
    
    dcc.Interval(
        id="interval-update",
        interval=5 * 60 * 1000,  # Update every 5 minutes
        n_intervals=0
    )
])

# Callback to update graph
@app.callback(
    dash.Output("price-chart", "figure"),
    dash.Input("interval-update", "n_intervals")
)
def update_graph(n_intervals):
    df = load_data()
    
    if df.empty:
        return go.Figure()

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

# Run the Dash app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
