import dash_bootstrap_components as dbc
from dash import html


navbar = dbc.NavbarSimple(

    children=[

        dbc.NavItem(
            dbc.NavLink("Home", href="/home")
        ),

        dbc.NavItem(
            dbc.NavLink("Performance", href="/performance")
        ),

        dbc.NavItem(
            dbc.NavLink("Market Value", href="/market_value")
        ),

        dbc.NavItem(
            dbc.NavLink("Logout", href="/logout")
        )

    ],

    brand="Sports Analytics Dashboard",
    brand_href="/home",

    color="primary",
    dark=True,

    fluid=True,
    sticky="top"

)