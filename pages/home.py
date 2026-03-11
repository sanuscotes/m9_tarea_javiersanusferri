from dash import html
import dash_bootstrap_components as dbc


layout = dbc.Container(

    [

        html.H1(
            "Sports Analytics Dashboard",
            className="mt-4"
        ),

        html.P(
            "Plataforma para el análisis de rendimiento y valoración de jugadores basada en datos."
        ),

        html.Hr(),

        dbc.Row(

            [

                # ---------------------------
                # PERFORMANCE
                # ---------------------------

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H4(
                                    "Performance Dashboard",
                                    className="card-title"
                                ),

                                html.P(
                                    "Análisis de rendimiento ofensivo y métricas avanzadas de jugadores."
                                ),

                                dbc.Button(
                                    "Abrir Dashboard",
                                    href="/performance",
                                    color="primary"
                                )

                            ]

                        )

                    ),

                    width=6

                ),

                # ---------------------------
                # MARKET VALUE
                # ---------------------------

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H4(
                                    "Market Value Dashboard",
                                    className="card-title"
                                ),

                                html.P(
                                    "Análisis de valor de mercado de jugadores por edad, posición y liga."
                                ),

                                dbc.Button(
                                    "Abrir Dashboard",
                                    href="/market_value",
                                    color="primary"
                                )

                            ]

                        )

                    ),

                    width=6

                ),

            ],

            className="mt-4"

        )

    ],

    fluid=True,
    className="page-container"

)