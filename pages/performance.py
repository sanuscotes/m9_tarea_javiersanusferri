# Importación de librerías necesarias
from dash import html, dcc
import dash_bootstrap_components as dbc

# Definición del layout de la página
layout = dbc.Container(
    [
        # Título de la página
        html.H2("Performance Dashboard", className="mb-4"),
        # Filtros de datos
        dbc.Row(
            [
                # Filtro para seleccionar uno o varios jugadores
                dbc.Col(
                    [
                        # Etiqueta del filtro
                        html.Label("Seleccionar Jugador"),
                        # Menú desplegable para seleccionar jugadores. Los valores se cargarán dinámicamente
                        dcc.Dropdown(
                            id="perf-player-dropdown",
                            placeholder="Seleccionar jugador",
                            multi=True
                        )
                    ],
                    width=4
                ),
                # Filtro para seleccionar un rango de minutos jugados
                dbc.Col(
                    [
                        # Etiqueta del filtro
                        html.Label("Minutos Jugados"),
                        # Filtro deslizante que permite seleccionar un rango de valores
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
                # Botón para exportar el análisis a PDF
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
        # Gráficos
        dbc.Row(
            [
                # Gráfico 1: scatter plot de métricas ofensivas
                dbc.Col(
                    # Indicador de carga mientras se renderiza el gráfico
                    dcc.Loading(
                        type="circle",
                        children=dcc.Graph(
                            id="perf-scatter-goals"
                        )
                    ),
                    width=6
                ),
                # Gráfico 2: radar chart con métricas del jugador
                dbc.Col(
                    # Indicador de carga mientras se renderiza el gráfico
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
        # Componente utilizado por Dash para generar la descarga del archivo PDF
        dcc.Download(id="download-performance-pdf")
    ],
    # Permite que el contenedor ocupe todo el ancho de la pantalla
    fluid=True
)