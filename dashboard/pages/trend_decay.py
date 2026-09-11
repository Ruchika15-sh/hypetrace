import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from dash import dcc, html
from db import engine

def trend_decay_page():
    trends = pd.read_sql("SELECT t.*, b.brand_name FROM trend_metrics t JOIN brands b ON t.brand_id = b.brand_id", engine)
    trends['date'] = pd.to_datetime(trends['date'])

    bal = trends[trends['brand_name'] == 'Balenciaga'].sort_values('date')
    spike_date = pd.Timestamp('2022-11-22')
    window = bal[(bal['date'] >= spike_date - pd.Timedelta(days=14)) & (bal['date'] <= spike_date + pd.Timedelta(days=90))].copy()
    window['days_since_peak'] = (window['date'] - spike_date).dt.days

    def decay_func(x, a, b, c):
        return a * np.exp(-b * x) + c

    x_data = window['days_since_peak'].values
    y_data = window['search_interest'].values

    try:
        popt, _ = curve_fit(decay_func, x_data, y_data, p0=[80, 0.05, 10], maxfev=5000)
        x_smooth = np.linspace(x_data.min(), x_data.max(), 200)
        y_smooth = decay_func(x_smooth, *popt)
        half_life = round(np.log(2) / popt[1], 1) if popt[1] > 0 else None
    except Exception:
        x_smooth, y_smooth, half_life = [], [], None

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers', name='Actual Search Interest', marker=dict(color='#60A5FA')))
    fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name='Fitted Decay Curve', line=dict(color='#F97316', width=3)))
    fig.update_layout(
        title='Trend Decay: Balenciaga Controversy (Nov 2022)',
        xaxis_title='Days Since Peak', yaxis_title='Search Interest',
        paper_bgcolor='#0F0E17', plot_bgcolor='#1C1B29', font_color='white'
    )

    half_life_text = f"Estimated half-life: ~{half_life} days" if half_life else "Could not estimate half-life"

    return html.Div([
        html.H2("Trend Decay Analysis", style={'color': 'white'}),
        html.P("How quickly does public interest fade after a major spike?", style={'color': '#B4B4C7'}),
        html.H4(half_life_text, style={'color': '#F97316'}),
        dcc.Graph(figure=fig)
    ])