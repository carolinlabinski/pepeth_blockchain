from dash import dcc, html
from controllers.block_controller import blocks_prop
from controllers.polygon_api_controller import value_over_time
from datetime import date, timedelta

import numpy as np


def token_value_over_time(days):
    y = value_over_time(days)['values']
    x = [str(date.today() - timedelta(days=i)) for i in range(days)]
    x.reverse()
    return graph(x, y, f"Token value over the last {days} days", 'lines red', )


def size_graph(size, graph_type='lines'):
    col = blocks_prop(size, 'size')
    v = sorted(col['size'].values(), key=lambda a: a[0])
    x = [e[0] for e in v]
    y = [e[1] for e in v]
    return graph(x, y, f"Block Size (last {size} blocks)", graph_type)


def time_graph(size, graph_type='lines'):
    col = blocks_prop(size, 'timestamp')
    v = sorted(col['timestamp'].values(), key=lambda a: a[0])
    x = [e[0] for e in v]
    y = np.diff([e[1] for e in v])
    return graph(x, y, f"Block mining time (last {size} blocks)", graph_type)


def time_graph(size, graph_type='lines'):
    col = blocks_prop(size, 'timestamp')
    v = sorted(col['timestamp'].values(), key=lambda a: a[0])
    x = [e[0] for e in v]
    y = np.diff([e[1] for e in v])
    return graph(x, y, f"Block mining time (last {size} blocks)", graph_type)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def graph(x, y, title, graph_type='lines'):
    element = html.Div(
        children=[
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": x,
                            "y": y,
                            'type': graph_type
                        },
                    ],
                    "layout": {"title": title},
                    
                },
            ),
        ]
    )
    return element
