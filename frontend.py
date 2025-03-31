import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Multi-Page Support aktivieren
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Für Flask-Hosting

# Navigation & Seitenlayout
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Network Visualizations", href="/", className="ms-2"),
            dbc.Nav(
                [
                    dbc.NavItem(dcc.Link("Cartel Network", href="/page2", className="nav-link")),
                    dbc.NavItem(dcc.Link("Shareholder Network", href="/", className="nav-link")),
                    dbc.NavItem(dcc.Link("Test Complete Network", href="/page3", className="nav-link")),
                ],
                className="ms-auto",
                navbar=True
            )
        ]),
        color="dark",
        dark=True
    ),

    # Container für die Seiteninhalte
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)