import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from elasticsearch import Elasticsearch

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Welcome to X-Ray Annotations!',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Thank You for being a part of the community.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Tabs(id="tabs-styled-with-props" , value='tab-1', children=[
        dcc.Tab(label='Single Image Search', value='tab-1'),
        dcc.Tab(label='Multi Image Search', value='tab-2'),
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "grey"
    }),
    html.Div(id='tabs-content-props')
])

@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])



if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0")