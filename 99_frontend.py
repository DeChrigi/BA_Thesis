import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Activate multi-page mode
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # For flask deployment

# Navigation & page layout
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Network Visualizations", href="/", className="ms-2"),
            dbc.Nav(
                [
                    dbc.NavItem(dcc.Link("Cartel Network", href="/page2", className="nav-link")),
                    dbc.NavItem(dcc.Link("Shareholder Network", href="/", className="nav-link")),
                    dbc.NavItem(dcc.Link("Connected Shareholder Network", href="/page4", className="nav-link")),
                    dbc.NavItem(dcc.Link("Test Complete Network", href="/page3", className="nav-link")),
                ],
                className="ms-auto",
                navbar=True
            )
        ]),
        color="dark",
        dark=True
    ),

    # container for the page content
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)