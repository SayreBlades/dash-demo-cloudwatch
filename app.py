# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import boto3

cloudwatch = boto3.client('cloudwatch')
network_in_kwargs = {
    "MetricName": 'NetworkIn',
    "Namespace": 'AWS/EC2',
    "Dimensions": [{'Name':'InstanceId', 'Value':'i-098d99fa82bc865e6'}],
    "StartTime": '2017-06-24',
    "EndTime": '2017-06-25',
    "Period": 600,
    "Statistics": ['Sum'],
}
network_in_data = cloudwatch.get_metric_statistics(**network_in_kwargs)
network_in_datapoints = sorted(network_in_data['Datapoints'], key=lambda o: o['Timestamp'])
network_in_x = [str(d['Timestamp']) for d in network_in_datapoints]
network_in_y = [d['Sum'] for d in network_in_data['Datapoints']]

network_out_kwargs = {
    "MetricName": 'NetworkOut',
    "Namespace": 'AWS/EC2',
    "Dimensions": [{'Name':'InstanceId', 'Value':'i-098d99fa82bc865e6'}],
    "StartTime": '2017-06-24',
    "EndTime": '2017-06-25',
    "Period": 600,
    "Statistics": ['Sum'],
}
network_out_data = cloudwatch.get_metric_statistics(**network_out_kwargs)
network_out_datapoints = sorted(network_out_data['Datapoints'], key=lambda o: o['Timestamp'])
network_out_x = [str(d['Timestamp']) for d in network_out_datapoints]
network_out_y = [d['Sum'] for d in network_out_data['Datapoints']]


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Mock Dashboard', style={
        'text-align':'center'
    }),

    # html.Div(style={'columnCount':2}, children='''
    #     Dash: A web application framework for Python.
    # '''),

    html.Div(style={'columnCount':2}, children=[
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': network_in_x, 'y': network_in_y},
                ],
                'layout': {
                    'title': f'{network_in_kwargs["MetricName"]} on {network_in_kwargs["Dimensions"][0]["Value"]} from {network_in_kwargs["StartTime"]} to {network_in_kwargs["EndTime"]}'
                }
            }
        ),
        dcc.Graph(
            id='example-graph2',
            figure={
                'data': [
                    {'x': network_out_x, 'y': network_out_y},
                ],
                'layout': {
                    'title': f'{network_out_kwargs["MetricName"]} on {network_out_kwargs["Dimensions"][0]["Value"]} from {network_out_kwargs["StartTime"]} to {network_out_kwargs["EndTime"]}'
                }
            }
        ),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
