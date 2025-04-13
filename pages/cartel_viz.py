import dash
from dash import html, dcc, callback, Output, Input
import networkx as nx
import plotly.graph_objects as go
import os

def load_graph():
    G = nx.read_graphml(os.path.join(graphml_folder, filename))

    pos = nx.spring_layout(G, seed=42)

    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1, None], 
            y=[y0, y1, None],
            line=dict(width=1, color='grey'),
            mode='lines',
            hoverinfo='none'
        )
        edge_traces.append(edge_trace)

    # Liste for all nodes
    company_x, company_y, company_text = [], [], []
    cartel_x, cartel_y, cartel_text = [], [], []

    for node, data in G.nodes(data=True):
        x, y = pos[node]
        label = data.get("type", "Unknown")

        if label == "Cartel":
            cartel_x.append(x)
            cartel_y.append(y)
            cartel_text.append(f"{node} (Cartel)")
        else:
            company_x.append(x)
            company_y.append(y)
            company_text.append(f"{node} (Company)")

    # Scatter-Plot for companies (blue)
    company_trace = go.Scatter(
        x=company_x, y=company_y,
        mode='markers',
        marker=dict(color='#3d85c6', size=12, line=dict(width=2)),
        text=company_text,
        hoverinfo='text'
    )

    # Scatter-Plot for cartels (red)
    cartel_trace = go.Scatter(
        x=cartel_x, y=cartel_y,
        mode='markers',
        marker=dict(color='#6aa84f', size=15, line=dict(width=2)),
        text=cartel_text,
        hoverinfo='text'
    )

    # Final Figure
    fig = go.Figure(
        data=edge_traces + [company_trace, cartel_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white'
        )
    )
    
    return fig

dash.register_page(__name__, path="/page2")  # This page is available at /page2

# Set the folder where GraphML files are stored
graphml_folder = "./transformed_data/cartel_networks"
filename = "cartel_network.graphml"

# Dash Layout für Seite 2
layout = html.Div([
    html.H1("Cartel Network", style={'textAlign': 'center'}),
    dcc.Graph(id='cartel-graph', style={'height': '600px'}),
])

@callback(
    Output('cartel-graph', 'figure'),
    Input('cartel-graph', 'id')  # Dummy-Input for initial load
)
def update_graph(_):
    return load_graph()

