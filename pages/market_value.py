from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


layout = dbc.Container(

    [

        html.H2("Market Value Dashboard", className="mb-4"),

        # FILTROS
        dbc.Row(

            [

                dbc.Col(

                    [
                        html.Label("Posición"),

                        dcc.Dropdown(
                            id="position-filter",
                            multi=True,
                            placeholder="Seleccionar posición"
                        )

                    ],

                    width=4
                ),

                dbc.Col(

                    [

                        html.Label("Valor de Mercado"),

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

        # GRÁFICOS
        dbc.Row(

            [

                dbc.Col(

                    dcc.Loading(

                        type="circle",

                        children=dcc.Graph(
                            id="age-value-scatter"
                        )

                    ),

                    width=6

                ),

                dbc.Col(

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

        # TABLA

        dcc.Loading(

            type="circle",

            children=dash_table.DataTable(

                id="market-table",

                page_size=10,

                sort_action="native",
                filter_action="native",

                style_table={"overflowX": "auto"}

            )

        )

    ],

    fluid=True

)