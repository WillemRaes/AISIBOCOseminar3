"""
General message format:

JSON style:

nodeId : "int"
sensor : "str"
msgType : "int"
"quality: "int"
"ts: " unix timestamp
"payload:  bytes"

"""
import paho.mqtt.client as mqtt
import time
import logging

from MQTTClient import MQTTStreamConsumer
from Config import config
import queue

logging.basicConfig(level=logging.DEBUG, format='(%(asctime)s %(threadName)-9s) %(message)s',
                    filename="Seminar3-framework-log.log")
logging.debug("############### NEW SERVICE START ###############")

# mqtt_thread2 = MQTTStreamConsumer(name="Client-mqtt-pressure", broker_addr="10.128.64.9", queue_out=log_queue_pres, topic="wheelchair/whch1/pressure")
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

data_server = {
    'time': [],
    'latency': [],

}
data_nano = {
    'time': [],
    'latency': [],

}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Latency evaluation edge vs cloud'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 100,  # in milliseconds
            n_intervals=0
        )
    ])
)


# @app.callback(Output('live-update-text', 'children'),
#              Input('interval-component', 'n_intervals'))
# def update_metrics(n):

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
    global data_server
    global data_data_nano
    while not config.log_queue_server.empty():
        data = config.log_queue_server.get()
        if data[0] == 'jetsontx2/RTlatency':

            data_tx2['time'].append(datetime.datetime.fromtimestamp(data[1]))
            if len(data_tx2['time']) > 150:
                del data_tx2['time'][0]

            data_tx2['latency'].append(data[-1] * 1000)
            if len(data_tx2['latency']) > 150:
                del data_tx2['latency'][0]

        if data[0] == 'jetsonnano/latency':

            data_nano['time'].append(datetime.datetime.fromtimestamp(data[1]))
            if len(data_nano['time']) > 150:
                del data_nano['time'][0]

            data_nano['latency'].append(data[-1] * 1000)
            if len(data_nano['latency']) > 150:
                del data_nano['latency'][0]

        if data[0] == 'server/latency':

            data_server['time'].append(datetime.datetime.fromtimestamp(data[1]))
            if len(data_server['time']) > 150:
                del data_server['time'][0]

            data_server['latency'].append(data[-1] * 1000)
            if len(data_server['latency']) > 150:
                del data_server['latency'][0]
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=4, cols=1, vertical_spacing=0.05)
    fig['layout']['margin'] = {
        'l': 10, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.layout.height = 1000
    # fig.layout.xaxis_title = "Local time of day",
    # fig.layout.yaxis_title = "Latency in (ms)",
    fig.append_trace({
        'x': data_tx2['time'],
        'y': data_tx2['latency'],
        'name': 'latency Jetson TX2 (Cloud)',
        'mode': 'lines+markers',
        'type': 'scatter',

    }, 1, 1)
    fig.append_trace({
        'x': data_nano['time'],
        'y': data_nano['latency'],
        'name': 'latency Jetson Nano (Edge)',
        'mode': 'lines+markers',
        'type': 'scatter',

    }, 2, 1)
    # fig.append_trace({
    #     'x': data_server['time'],
    #     'y': data_server['latency'],
    #     'name': 'latency Server',
    #     'mode': 'lines+markers',
    #     'type': 'scatter'
    # }, 3, 1)
    fig.append_trace({
        'x': data_server['time'],
        'y': data_server['latency'],
        'name': 'latency Server',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': data_tx2['time'],
        'y': data_tx2['latency'],
        'name': 'latency Jetson-TX2 (Cloud)',
        'mode': 'lines+markers',
        'type': 'scatter',


    }, row=3, col=1)
    fig.append_trace({
        'x': data_nano['time'],
        'y': data_nano['latency'],
        'name': 'latency Jetson Nano (Edge)',
        'mode': 'lines+markers',
        'type': 'scatter',


    }, row=3, col=1)
    # Update xaxis properties
    fig.update_xaxes(title_text="Local time of day", row=1, col=1)
    fig.update_xaxes(title_text="Local time of day", row=2, col=1)
    fig.update_xaxes(title_text="Local time of day", row=3, col=1)
    # fig.update_xaxes(title_text="Local time of day", row=4, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Latency in (ms)", row=1, col=1)
    fig.update_yaxes(title_text="Latency in (ms)",  row=2, col=1)
    fig.update_yaxes(title_text="Latency in (ms)",  row=3, col=1)
    # fig.update_yaxes(title_text="Latency in (ms)", row=4, col=1)

    return fig


if __name__ == '__main__':
    mqtt_thread = MQTTStreamConsumer(name="Client-mqtt-server", broker_addr="10.128.64.5", queue_out=config.log_queue_server, topic="server/latency")
    mqtt_thread.start()
    mqtt_thread = MQTTStreamConsumer(name="Client-mqtt-nano", broker_addr="10.128.64.5",
                                     queue_out=config.log_queue_server, topic="jetsonnano/latency")
    mqtt_thread.start()
    mqtt_thread = MQTTStreamConsumer(name="Client-mqtt-tx2", broker_addr="10.128.64.5",
                                     queue_out=config.log_queue_server, topic="jetsontx2/RTlatency")
    mqtt_thread.start()
    app.run_server(debug=True)

    while True:
        pass

