import plotly
import numpy
import pandas
import dash

import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from Config import config

def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))


data_tx2 = {
    'time': [],
    'latency': [],

}
# pip install pyorbital

from pyorbital.orbital import Orbital

# satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )
    ])
)


#@app.callback(Output('live-update-text', 'children'),
#              Input('interval-component', 'n_intervals'))
#def update_metrics(n):

#    if not config.log_queue_tx2.empty():
#        data_tx2 = config.log_queue_tx2.get()

    # lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#    style = {'padding': '5px', 'fontSize': '16px'}
#    return [
#        html.Span('Latency: {0:.2f}'.format(data_tx2[-1]), style=style),
        # html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        # html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global data_tx2
    while not config.log_queue_tx2.empty():
        data_tx2 = config.log_queue_tx2.get()
        data_tx2['time'].append(data_tx2[0] )
        data_tx2['latency'].append(data_tx2[-1]* 1000)




    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data_tx2['time'],
        'y': data_tx2['latency'],
        'name': 'latency',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data_tx2['time'],
        'y': data_tx2['latency'],
        'name': 'latency',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
