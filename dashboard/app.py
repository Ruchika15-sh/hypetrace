import dash
from dash import dcc, html, Input, Output

from pages.overview import overview_page
from pages.event_study import event_study_page
from pages.trend_decay import trend_decay_page
from pages.brand_comparison import brand_comparison_page, register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
register_callbacks(app)

navbar = html.Div([
    html.H2("HypeTrace", style={'color': 'white', 'margin': '0'}),
    html.Div([
        dcc.Link("Overview", href="/", style={'color': 'white', 'marginRight': '20px'}),
        dcc.Link("Event Study", href="/event-study", style={'color': 'white', 'marginRight': '20px'}),
        dcc.Link("Trend Decay", href="/trend-decay", style={'color': 'white', 'marginRight': '20px'}),
        dcc.Link("Brand Comparison", href="/brand-comparison", style={'color': 'white'}),
    ])
], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '15px 30px', 'backgroundColor': '#1C1B29'})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style={'padding': '20px', 'minHeight': '90vh', 'backgroundColor': '#0F0E17'})
], style={'margin': '0', 'fontFamily': 'Arial'})

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/event-study':
        return event_study_page()
    elif pathname == '/trend-decay':
        return trend_decay_page()
    elif pathname == '/brand-comparison':
        return brand_comparison_page()
    else:
        return overview_page()

if __name__ == '__main__':
    app.run(debug=True)