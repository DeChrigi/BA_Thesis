import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import networkx as nx
import plotly.graph_objects as go
import plotly.colors as pc
from dash import callback
import numpy as np

def load_graph(filename, min_weight_filter):

    G = nx.read_graphml(os.path.join(graphml_folder, filename))
    
    # Identify the central 'Cartel' node (assumed to be of type 'Company')
    central_node = None
    for node, attr in G.nodes(data=True):
        if attr.get('type') == 'Company':
            central_node = node
            break
    
    # Position nodes using spring layout; fix 'Cartel' node at center if found
    if central_node:
        pos = nx.spring_layout(G, center=(0, 0), seed=42)
        pos[central_node] = (0, 0)
    else:
        pos = nx.spring_layout(G, seed=42)

    edge_traces = []
    edge_texts = []

    # Prepare structure to hold weights of nodes
    node_weights = {node: [] for node in G.nodes()}
    filtered_nodes = set()  

    for edge in G.edges(data=True):
        weight = float(edge[2].get('weight', 1))

        # Filter edges based on the minimum weight threshold
        if weight < min_weight_filter:
            continue  

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=1, color='grey'),
            hoverinfo='text',
            text=f"Weight: {weight}",
            mode='lines')
        
        edge_traces.append(edge_trace)
        edge_texts.append(f"{weight}")

        node_weights[edge[0]].append(weight)
        node_weights[edge[1]].append(weight)
        filtered_nodes.add(edge[0])
        filtered_nodes.add(edge[1])

    node_x = []
    node_y = []
    node_text = []
    node_color = []

    # Compute average weight per node for coloring
    avg_weights = {node: np.mean(weights) if weights else 0 for node, weights in node_weights.items()}
    max_weight = max(avg_weights.values()) if avg_weights else 1
    min_weight = min(avg_weights.values()) if avg_weights else 0

    colorscale = pc.sequential.Blues
    for node, data in G.nodes(data=True):
        if node not in filtered_nodes:
            continue  # Skip nodes not part of the filtered graph

        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>% OS: {avg_weights[node]:.2f}")

        # Normalize weight for color mapping
        norm_weight = (avg_weights[node] - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 0
        color = colorscale[int(norm_weight * (len(colorscale) - 1))]  

        node_color.append(color)

    # Plot all nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            colorscale='Blues',
            color=node_color,
            size=15,
            line_width=2))
    
    cartel_x = []
    cartel_y = []
    cartel_text = []

    for node, data in G.nodes(data=True):
        if node == central_node:  # If this is the 'Cartel' node
            x, y = pos[node]
            cartel_x.append(x)
            cartel_y.append(y)
            cartel_text.append(str(node))

    # Highlight the central 'Cartel' node
    cartel_trace = go.Scatter(
        x=cartel_x, y=cartel_y,
        mode='markers',
        hoverinfo='text',
        text=cartel_text,
        marker=dict(
            color='#6aa84f',  # Green color (original German comment said red, but code uses green)
            size=20,          # Slightly bigger for emphasis
            line_width=2
        )
    )

    # Combine all traces into one figure
    fig = go.Figure(data=edge_traces + [node_trace, cartel_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=20, r=20, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='white'))

    return fig

# Register this page as the home page
dash.register_page(__name__, path="/")

# Set the folder where GraphML files are stored
graphml_folder = "./transformed_data/shareholder_networks"

# Get all available GraphML files and clean their names for display
graphml_files = [f for f in os.listdir(graphml_folder) if f.endswith(".graphml")]
graphml_files = [f.split("shareholder_network_")[1].split("_31-Dec")[0] for f in graphml_files]
graphml_files = list(set(graphml_files))

# Define the layout for the Dash web app
layout = html.Div([
    html.H1("Shareholder Network", style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    html.Div([
        html.Label("Select Graph:"),
        dcc.Dropdown(
            id='graph-dropdown',
            options=[{'label': f, 'value': f} for f in graphml_files],
            value=graphml_files[0] if graphml_files else None,
            style={'width': '50%', 'margin': '0 auto', 'marginTop': '10px'}
        ),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
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

    html.Div([
        html.Label("Filter edges by minimum weight:", style={'display': 'block', 'textAlign': 'center'}),
        html.Div([
            dcc.Input(
                id='weight-filter-input',
                type='number',
                value=0.00,
                step=0.01,
                min=0,
                max=100,
                style={'width': '100px', 'marginTop': '10px'}
            ),
        ], style={'textAlign': 'center'})
    ], style={'width': '50%', 'margin': '0 auto', 'marginBottom': '30px'}),
    
    html.Div([
        dcc.Graph(id='graph-display', style={'height': '600px'})
    ], style={'width': '90%', 'margin': '0 auto'})
])

# Callback to update the graph when user changes dropdown, slider, or filter input
@callback(
    Output('graph-display', 'figure'),
    [Input('graph-dropdown', 'value'), Input('year-slider', 'value'), Input('weight-filter-input', 'value')]
)
def update_graph(selected_graph, selected_year, min_weight_filter):
    if selected_graph:
        min_weight_filter = float(min_weight_filter) if min_weight_filter is not None else 0.0
        return load_graph('shareholder_network_' + selected_graph + "_31-Dec-" + str(selected_year) + ".graphml", min_weight_filter)
    return go.Figure()
