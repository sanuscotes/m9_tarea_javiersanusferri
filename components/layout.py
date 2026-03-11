from dash import html, dcc

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