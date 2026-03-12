# Importación de librerías necesarias
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Definición del layout de la página
layout = dbc.Container(
    [
        # Título de la página
        html.H2("Market Value Dashboard", className="mb-4"),
        # Filtros de datos
        dbc.Row(
            [
                # Filtro por posición del jugador
                dbc.Col(
                    [
                        # Etiqueta del filtro
                        html.Label("Posición"),
                        # Menú desplegable que permitirá seleccionar una o varias posiciones
                        dcc.Dropdown(
                            id="position-filter",
                            multi=True,
                            placeholder="Seleccionar posición"
                        )
                    ],
                    width=4
                ),
                # Filtro por rango de valor de mercado
                dbc.Col(
                    [
                        # Etiqueta del filtro
                        html.Label("Valor de Mercado"),
                        # Filtro deslizante que permite seleccionar un rango de valores
                        dcc.RangeSlider(
                            id="value-filter",
                            min=0,
                            max=200,
                            step=5,
                            value=[0, 200],
                            tooltip={"placement": "bottom"}
                        )
                    ],
                    width=6
                )
            ],
            className="mb-4"
        ),
        # Gráficos
        dbc.Row(
            [
                # Gráfico 1: relación entre edad y valor de mercado
                dbc.Col(
                    # Indicador de carga mientras se renderiza el gráfico
                    dcc.Loading(
                        type="circle",
                        children=dcc.Graph(
                            id="age-value-scatter"
                        )
                    ),
                    width=6
                ),
                # Gráfico 2: distribución por liga y posición
                dbc.Col(
                    # Indicador de carga mientras se renderiza el gráfico
                    dcc.Loading(
                        type="circle",
                        children=dcc.Graph(
                            id="league-position-bar"
                        )
                    ),
                    width=6
                )
            ],
            className="mb-4"
        ),
        # Tabla
        # Indicador de carga mientras se renderiza el gráfico
        dcc.Loading(
            type="circle",
            children=dash_table.DataTable(
                # Identificador de la tabla para callbacks
                id="market-table",
                # Número de filas visibles por página
                page_size=10,
                # Permite ordenar columnas directamente desde la interfaz
                sort_action="native",
                # Permite aplicar filtros desde la propia tabla
                filter_action="native",
                # Hace que la tabla tenga scroll horizontal si es necesario
                style_table={"overflowX": "auto"}
            )
        )
    ],
    # Permite que el contenedor ocupe todo el ancho de la pantalla
    fluid=True
)