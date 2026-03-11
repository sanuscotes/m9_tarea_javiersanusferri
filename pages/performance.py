from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container(

    [

        html.H2("Performance Dashboard", className="mb-4"),

        # FILTROS
        dbc.Row(

            [

                dbc.Col(

                    [
                        html.Label("Seleccionar Jugador"),
                        dcc.Dropdown(
                            id="perf-player-dropdown",
                            placeholder="Seleccionar jugador",
                            multi=True
                        )
                    ],

                    width=4
                ),

                dbc.Col(

                    [
                        html.Label("Minutos Jugados"),
                        dcc.RangeSlider(
                            id="perf-minutes-slider",
                            min=0,
                            max=4000,
                            step=50,
                            value=[0, 4000],
                            tooltip={"placement": "bottom"}
                        )
                    ],

                    width=6
                ),

                dbc.Col(

                    dbc.Button(
                        "Exportar PDF",
                        id="btn-download-pdf",
                        color="danger",
                        className="mt-4"
                    ),

                    width=2
                )

            ],

            className="mb-4"

        ),

        # GRÁFICOS
        dbc.Row(

            [

                dbc.Col(

                    dcc.Loading(

                        type="circle",

                        children=dcc.Graph(
                            id="perf-scatter-goals"
                        )

                    ),

                    width=6

                ),

                dbc.Col(

                    dcc.Loading(

                        type="circle",

                        children=dcc.Graph(
                            id="perf-radar-player"
                        )

                    ),

                    width=6

                )

            ]

        ),

        dcc.Download(id="download-performance-pdf")

    ],

    fluid=True
)