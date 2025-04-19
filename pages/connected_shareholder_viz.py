import dash
from dash import html, dcc, callback, Output, Input
import networkx as nx
import plotly.graph_objects as go
import os

def load_graph(filename):
    
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
    investor_x, investor_y, investor_text = [], [], []

    for node, data in G.nodes(data=True):
        x, y = pos[node]
        label = data.get("type", "Unknown")


        if label == "company":
            company_x.append(x)
            company_y.append(y)
            company_text.append(f"{node} (company)")
        elif label == "investor":
            investor_x.append(x)
            investor_y.append(y)
            investor_text.append(f"{node} (investor)")

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
        data=edge_traces + [company_trace, investor_trace],
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

# Register this page to be accessible at /page4
dash.register_page(__name__, path="/page4")

# Set the folder where GraphML files are stored
graphml_folder = "./transformed_data/connected_shareholder_networks"

# Dash layout for page 4
layout = html.Div([
    html.H1("Connected Shareholder Network", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Year:", style={'marginBottom': '10px'}),
        dcc.Slider(
            id='year-slider',
            min=1997,
            max=2011,
            value=1997,
            marks={year: str(year) for year in range(1997, 2012)},
            step=1
        ),
    ], style={'textAlign': 'center', 'width': '80%', 'margin': '0 auto', 'marginBottom': '10px'}),

    dcc.Graph(id='connected-shareholder-graph', style={'height': '600px'}),
])

# Callback to update the graph when user changes dropdown, slider, or filter input
@callback(
    Output('connected-shareholder-graph', 'figure'),
    Input('year-slider', 'value')
)
def update_graph(selected_year):
    if selected_year:
        return load_graph('connected_shareholder_network_' + str(selected_year) + '.graphml')
    return go.Figure()