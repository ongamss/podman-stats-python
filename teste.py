import json
import subprocess
import pandas as pd
import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from collections import OrderedDict
from datetime import datetime

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(
        children='Pods Statistics',
    ),
    dash_table.DataTable(
        id='table',
        sort_action='native',
        columns=[],
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'cpu_percent',
                    'filter_query': '{cpu_percent} > 70 && {cpu_percent} < 80' },
                'backgroundColor': 'orange',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'cpu_percent',
                    'filter_query': '{cpu_percent} > 80'},
                'backgroundColor': 'red',
                'color': 'white'
            },   
            {            
                'if': {
                    'column_id': 'mem_percent',
                    'filter_query': '{mem_percent} > 70 && {mem_percent} < 80' },
                'backgroundColor': 'orange',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'mem_percent',
                    'filter_query': '{mem_percent} > 80'},
                'backgroundColor': 'red',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'No Data Available'},
                'backgroundColor': 'red',
                'color': 'white',
                'text-align': 'center'
            }
        ]
    ),
    dcc.Interval(id='interval-component', interval=3000, n_intervals=0)
])

@app.callback(Output('table', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_table(n):
    proc = subprocess.Popen(["podman", "stats", "--no-stream", "--format=json"], stdout=subprocess.PIPE)
    output = proc.stdout.read().decode()
    json_data = json.loads(output,object_pairs_hook=OrderedDict)
    df = pd.DataFrame(json_data)

    if 'mem_percent' not in df.columns or df['mem_percent'].empty:
       return [{'No Data Available': 'No Data Available'}]

    # Processamento dos dados da memória
    df['mem_percent'] = df['mem_percent'].apply(lambda x: x.strip("%"))
    df['mem_percent'] = pd.to_numeric(df['mem_percent'])
    df['mem_percent'] = df['mem_percent'].apply(lambda x: x/1)

    # Processamento dos dados da CPU
    df['cpu_percent'] = df['cpu_percent'].apply(lambda x: x.strip("%"))
    df['cpu_percent'] = pd.to_numeric(df['cpu_percent'])
    df['cpu_percent'] = df['cpu_percent'].apply(lambda x: x/1)
    
    # apenas pra uso de memoria acima de 0
    df = df[df['mem_percent'] > 0]

    if df.empty:
       return [{'No Data Available': 'No Data Available'}]

    return df.to_dict("records")

@app.callback(Output('table', 'columns'),
              [Input('table', 'data')])
def update_columns(data):
    columns = [{'name': i, 'id': i} for i in data[0]]
    return columns

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=False)