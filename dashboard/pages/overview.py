import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from db import engine

def overview_page():
    trends = pd.read_sql("SELECT t.*, b.brand_name FROM trend_metrics t JOIN brands b ON t.brand_id = b.brand_id", engine)
    events = pd.read_sql("SELECT e.*, b.brand_name FROM events e JOIN brands b ON e.brand_id = b.brand_id", engine)
    trends['date'] = pd.to_datetime(trends['date'])
    events['event_date'] = pd.to_datetime(events['event_date'])

    fig = px.line(trends, x='date', y='search_interest', color='brand_name',
                  title='Search Interest Over Time — with Events')
    fig.update_xaxes(range=[trends['date'].min(), trends['date'].max()])

    event_points = []
    for _, row in events.iterrows():
        brand_trend = trends[trends['brand_name'] == row['brand_name']]
        nearest = brand_trend.iloc[(brand_trend['date'] - row['event_date']).abs().argsort()[:1]]
        if not nearest.empty:
            event_points.append({
                'date': row['event_date'], 'search_interest': nearest['search_interest'].values[0],
                'brand_name': row['brand_name'], 'celebrity': row['celebrity'],
                'event_type': row['event_type'], 'occasion': row['occasion']
            })
    event_df = pd.DataFrame(event_points)

    fig.add_trace(go.Scatter(
        x=event_df['date'], y=event_df['search_interest'], mode='markers',
        marker=dict(size=12, color='black', symbol='star'), name='Events',
        customdata=event_df[['brand_name', 'celebrity', 'event_type', 'occasion']],
        hovertemplate='<b>%{customdata[0]}</b><br>Celebrity: %{customdata[1]}<br>Type: %{customdata[2]}<br>Occasion: %{customdata[3]}<br>Date: %{x}<br>Search Interest: %{y}<extra></extra>'
    ))
    fig.update_layout(paper_bgcolor='#0F0E17', plot_bgcolor='#1C1B29', font_color='white')

    avg_interest = round(trends['search_interest'].mean(), 2)

    return html.Div([
        html.Div([
           
            html.Div("OVERVIEW", style={
    'display': 'inline-block', 'backgroundColor': '#E85D9C', 'color': 'white',
    'fontFamily': 'Anton, sans-serif', 'fontSize': '26px', 'padding': '8px 20px',
    'transform': 'rotate(-2deg)', 'marginBottom': '20px'
})
        ], style={ 'padding': '20px', 'borderRadius': '8px', 'width': '200px', 'marginBottom': '20px'}),
        dcc.Graph(figure=fig)
    ])