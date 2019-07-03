import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tabs import tab_1
from tabs import tab_2

from elasticsearch import Elasticsearch

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

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
        return tab_1.tab_1_layout
    elif tab == 'tab-2':
        return tab_2.tab_2_layout

# Tab 1 callback
@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

# Tab 2 callback
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)




if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0")