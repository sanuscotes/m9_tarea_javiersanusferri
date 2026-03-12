# Importación de librerías necesarias
import dash_bootstrap_components as dbc
from dash import html

# Barra de navegación principal
navbar = dbc.NavbarSimple(
    # Enlaces de navegación
    children=[
        # Enlace a la página Home
        dbc.NavItem(
            dbc.NavLink("Home", href="/home")
        ),
        # Enlace a la página Performance
        dbc.NavItem(
            dbc.NavLink("Performance", href="/performance")
        ),
        # Enlace a la página Market Value
        dbc.NavItem(
            dbc.NavLink("Market Value", href="/market_value")
        ),
        # Enlace al Logout
        dbc.NavItem(
            dbc.NavLink("Logout", href="/logout")
        )
    ],

    # Texto principal que aparece en la barra de navegación
    brand="Sports Analytics Dashboard",
    # Enlace al que redirige el logo/título del navbar
    brand_href="/home",

    # Color principal del navbar (tema Bootstrap)
    color="primary",
    # Indica que el navbar utiliza un tema oscuro
    dark=True,

    # Permite que el navbar ocupe todo el ancho de la pantalla
    fluid=True,
    # Hace que el navbar permanezca fijo en la parte superior incluso al hacer scroll en la página
    sticky="top"
)