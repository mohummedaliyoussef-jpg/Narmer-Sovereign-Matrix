import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# تحميل بيانات اختبار الحمل
df = pd.read_csv("docs/locust_50users_final_stats.csv")

app.layout = html.Div([
    html.H1("🔱 NARMER Performance Dashboard", style={'textAlign': 'center', 'color': '#FFD700'}),
    dcc.Graph(
        id='performance-chart',
        figure={
            'data': [
                {'x': df.index, 'y': df['Average'], 'type': 'line', 'name': 'Average Response (ms)'}
            ],
            'layout': {
                'title': 'Locust Performance Test Results',
                'template': 'plotly_dark',
                'xaxis': {'title': 'Request #'},
                'yaxis': {'title': 'Response Time (ms)'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)