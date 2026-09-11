import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output
from db import engine

def brand_comparison_page():
    summary = pd.read_sql("SELECT * FROM brand_stock_trend_summary", engine)

    fig = px.scatter(
        summary, x='avg_search_interest', y='avg_close_price',
        color='brand_name', size='avg_close_price', hover_name='brand_name',
        hover_data={'parent_company': True, 'avg_search_interest': True, 'avg_close_price': True},
        title='Search Interest vs. Stock Price (via Parent Company)'
    )
    fig.update_layout(paper_bgcolor='#0F0E17', plot_bgcolor='#1C1B29', font_color='white')

    return html.Div([
        html.H2("Brand Comparison", style={'color': 'white'}),
        html.P("Search interest plotted against parent-company stock price. Select a brand to isolate it:", style={'color': '#B4B4C7'}),
        dcc.Dropdown(
            id='brand-dropdown',
            options=[{'label': b, 'value': b} for b in summary['brand_name'].unique()],
            value=None, placeholder="All brands (select one to isolate)",
            style={'width': '300px', 'marginBottom': '20px', 'color': '#000'}
        ),
        dcc.Graph(id='comparison-scatter', figure=fig)
    ])

def register_callbacks(app):
    @app.callback(Output('comparison-scatter', 'figure'), Input('brand-dropdown', 'value'))
    def update_scatter(selected_brand):
        summary = pd.read_sql("SELECT * FROM brand_stock_trend_summary", engine)
        df = summary if not selected_brand else summary[summary['brand_name'] == selected_brand]
        fig = px.scatter(
            df, x='avg_search_interest', y='avg_close_price',
            color='brand_name', size='avg_close_price', hover_name='brand_name',
            hover_data={'parent_company': True, 'avg_search_interest': True, 'avg_close_price': True},
            title='Search Interest vs. Stock Price (via Parent Company)'
        )
        fig.update_layout(paper_bgcolor='#0F0E17', plot_bgcolor='#1C1B29', font_color='white')
        return fig