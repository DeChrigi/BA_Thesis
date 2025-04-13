import dash
from dash import html, dcc, callback, Output, Input
import networkx as nx
import plotly.graph_objects as go
import os

def load_graph():
    G = nx.read_graphml(os.path.join(graphml_folder, filename))

    # Position nodes using spring layout
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

    # Lists for nodes
    company_x, company_y, company_text = [], [], []
    cartel_x, cartel_y, cartel_text = [], [], []
    investor_x, investor_y, investor_text = [], [], []

    for node, data in G.nodes(data=True):
        x, y = pos[node]
        label = data.get("type", "Unknown")

        if label == "Cartel":
            cartel_x.append(x)
            cartel_y.append(y)
            cartel_text.append(f"{node} (Cartel)")
        elif label == "Entity":
            company_x.append(x)
            company_y.append(y)
            company_text.append(f"{node} (Entity)")
        elif label == "Investor":
            investor_x.append(x)
            investor_y.append(y)
            investor_text.append(f"{node} (Investor)")

    # Scatter plot for cartels (green)
    cartel_trace = go.Scatter(
        x=cartel_x, y=cartel_y,
        mode='markers',
        marker=dict(color='#6aa84f', size=15, line=dict(width=2)),
        text=cartel_text,
        hoverinfo='text'
    )

    # Scatter plot for companies (blue)
    company_trace = go.Scatter(
        x=company_x, y=company_y,
        mode='markers',
        marker=dict(color='#3d85c6', size=12, line=dict(width=2)),
        text=company_text,
        hoverinfo='text'
    )

    # Scatter plot for investors (green)
    investor_trace = go.Scatter(
        x=investor_x, y=investor_y,
        mode='markers',
        marker=dict(color='#6aa84f', size=10, line=dict(width=2)),
        text=investor_text,
        hoverinfo='text'
    )

    # Final figure
    fig = go.Figure(
        data=edge_traces + [company_trace, cartel_trace, investor_trace],
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

# Register this page to be accessible at /page3
dash.register_page(__name__, path="/page3")

# Set the folder where GraphML files are stored
graphml_folder = "./transformed_data/tests"
filename = "complete_cartel_network.graphml"

# Dash layout for page 3
layout = html.Div([
    html.H1("Complete Cartel Network", style={'textAlign': 'center'}),
    dcc.Graph(id='complete-cartel-graph', style={'height': '600px'}),
])

# Callback to load and display the graph on initialization
@callback(
    Output('complete-cartel-graph', 'figure'),
    Input('complete-cartel-graph', 'id')  # Dummy input just to trigger initial load
)
def update_graph(_):
    return load_graph()
