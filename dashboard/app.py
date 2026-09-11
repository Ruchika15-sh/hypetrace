import dash
from dash import dcc, html, Input, Output

from pages.overview import overview_page
from pages.event_study import event_study_page
from pages.trend_decay import trend_decay_page
from pages.brand_comparison import brand_comparison_page, register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True,
    external_stylesheets=['https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@600&family=Inter:wght@400;600&display=swap'])

navbar = html.Div([
    html.Div("Hi, welcome to", style={'fontFamily': 'Caveat, cursive', 'fontSize': '20px', 'color': '#E85D9C', 'marginBottom': '-8px'}),
    html.H1("HYPETRACE", style={'fontFamily': 'Anton, sans-serif', 'fontSize': '42px', 'color': '#1a1a1a', 'margin': '0'}),
    html.Div([
        dcc.Link("Overview", href="/", style={'color': '#1a1a1a', 'marginRight': '20px', 'fontFamily': 'Inter', 'fontWeight': '600', 'textDecoration': 'none'}),
        dcc.Link("Event Study", href="/event-study", style={'color': '#1a1a1a', 'marginRight': '20px', 'fontFamily': 'Inter', 'fontWeight': '600', 'textDecoration': 'none'}),
        dcc.Link("Trend Decay", href="/trend-decay", style={'color': '#1a1a1a', 'marginRight': '20px', 'fontFamily': 'Inter', 'fontWeight': '600', 'textDecoration': 'none'}),
        dcc.Link("Brand Comparison", href="/brand-comparison", style={'color': '#1a1a1a', 'fontFamily': 'Inter', 'fontWeight': '600', 'textDecoration': 'none'}),
    ], style={'marginTop': '10px'})
], style={'padding': '25px 30px', 'backgroundColor': '#EDE8E0', 'borderBottom': '4px solid #1a1a1a'})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style={'padding': '20px', 'minHeight': '90vh', 'backgroundColor': '#EDE8E0'})
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