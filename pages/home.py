# Importación de librerías necesarias
from dash import html
import dash_bootstrap_components as dbc

# Layout de la página de inicio
layout = dbc.Container(
    [
        # Título principal del dashboard
        html.H1(
            "Sports Analytics Dashboard",
            className="mt-4"
        ),
        # Descripción del dashboard
        html.P(
            "Plataforma para el análisis de rendimiento y valoración de jugadores basada en datos."
        ),
        html.Hr(),
        # Fila que contiene las tarjetas de navegación
        dbc.Row(
            [
                # Performance
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                # Título de la tarjeta
                                html.H4(
                                    "Performance Dashboard",
                                    className="card-title"
                                ),
                                # Descripción de la tarjeta
                                html.P(
                                    "Análisis de rendimiento ofensivo y métricas avanzadas de jugadores."
                                ),
                                # Botón de navegación
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
                # Market Value
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                # Título de la tarjeta
                                html.H4(
                                    "Market Value Dashboard",
                                    className="card-title"
                                ),
                                # Descripción de la tarjeta
                                html.P(
                                    "Análisis de valor de mercado de jugadores por edad, posición y liga."
                                ),
                                # Botón de navegación
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
    # Permite que el contenedor ocupe todo el ancho de la página
    fluid=True,
    # Clase CSS personalizada que puede definirse en assets/
    className="page-container"
)