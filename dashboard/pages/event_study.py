import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
from db import engine

def event_study_page():
    trends = pd.read_sql("SELECT t.*, b.brand_name FROM trend_metrics t JOIN brands b ON t.brand_id = b.brand_id", engine)
    events = pd.read_sql("SELECT e.*, b.brand_name FROM events e JOIN brands b ON e.brand_id = b.brand_id", engine)
    trends['date'] = pd.to_datetime(trends['date'])
    events['event_date'] = pd.to_datetime(events['event_date'])

    def calculate_lift(brand_name, event_date, before_days=14, after_days=14):
        bt = trends[trends['brand_name'] == brand_name].sort_values('date')
        before = bt[(bt['date'] >= event_date - pd.Timedelta(days=before_days)) & (bt['date'] < event_date)]
        after = bt[(bt['date'] >= event_date) & (bt['date'] <= event_date + pd.Timedelta(days=after_days))]
        if len(before) == 0 or len(after) == 0:
            return None
        before_avg, after_avg = before['search_interest'].mean(), after['search_interest'].mean()
        return round(((after_avg - before_avg) / before_avg) * 100, 2)

    results = []
    for _, row in events.iterrows():
        lift = calculate_lift(row['brand_name'], row['event_date'])
        if lift is not None:
            results.append({
                'Brand': row['brand_name'], 'Celebrity': row['celebrity'],
                'Date': row['event_date'].strftime('%Y-%m-%d'),
                'Type': row['event_type'], 'Lift %': lift
            })

    df = pd.DataFrame(results).sort_values('Lift %', ascending=False)

    bar_fig = px.bar(df, x='Celebrity', y='Lift %', color='Type',
                      title='Event Impact: % Change in Search Interest',
                      color_discrete_map={'endorsement': '#8B5CF6', 'controversy': '#F97316'})
    bar_fig.update_layout(paper_bgcolor='#0F0E17', plot_bgcolor='#1C1B29', font_color='white')

    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_header={'backgroundColor': '#1C1B29', 'color': 'white'},
        style_cell={'backgroundColor': '#141420', 'color': 'white', 'border': '1px solid #333'},
    )

    return html.Div([
        html.Div("EVENT STUDY", style={
    'display': 'inline-block', 'backgroundColor': '#E85D9C', 'color': 'white',
    'fontFamily': 'Anton, sans-serif', 'fontSize': '26px', 'padding': '8px 20px',
    'transform': 'rotate(-2deg)', 'marginBottom': '20px'
}),
        dcc.Graph(figure=bar_fig),
        html.Br(),
        table
    ])