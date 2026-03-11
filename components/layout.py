from dash import html, dcc
from components.navbar import navbar

layout = html.Div(

    [

        # Control de URL para navegación
        dcc.Location(id="url", refresh=False),

        # Contenedor donde se cargan las páginas
        html.Div(
            id="page-content",
            className="page-container"
        ),

    ]

)