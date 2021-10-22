import plotly
import numpy
import pandas
import dash

import datetime
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from Config import config
import time
from flask import Flask, Response
import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# server = Flask(__name__)
# app = dash.Dash(__name__, server=server)


# @server.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


# app.layout = html.Div([
#     html.H1("Webcam Test"),
#     html.Img(src="/video_feed")
# ])

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
#external_stylesheets = ['./dash-wind-streaming.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Latency evaluation Edge VS Cloud'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 500,  # in milliseconds
            n_intervals=0
        )
    ])
)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global data_tx2

    for val in range(random.randint(1, 12)):
        config.log_queue_tx2.put(["jetsontx2/latency", time.time(), random.uniform(0, 0.1)])
        time.sleep(0.05)
    while not config.log_queue_tx2.empty():
        data = config.log_queue_tx2.get()
        data_tx2['time'].append(datetime.datetime.fromtimestamp(data[1]))
        if len(data_tx2['time']) > 150:
            del data_tx2['time'][0]

        data_tx2['latency'].append(data[-1] * 1000)
        if len(data_tx2['latency']) > 150:
            del data_tx2['latency'][0]

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
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
