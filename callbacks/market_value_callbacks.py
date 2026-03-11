from dash import Input, Output
import plotly.express as px

from utils.data_loader import load_market_value_data
from utils.cache import cache


# -------- CACHE DATA --------

@cache.memoize(timeout=300)
def get_cached_market_value_data():

    return load_market_value_data()


def register_market_value_callbacks(app):

    @app.callback(

        Output("age-value-scatter", "figure"),
        Output("league-position-bar", "figure"),
        Output("market-table", "data"),
        Output("market-table", "columns"),
        Output("position-filter", "options"),

        Input("position-filter", "value"),
        Input("value-filter", "value")

    )
    def update_market_value_page(positions, value_range):

        try:

            df = get_cached_market_value_data()

            if df.empty:
                return {}, {}, [], [], []

            # -------- filtro valor --------

            df = df[
                (df["ValorMercado"] >= value_range[0]) &
                (df["ValorMercado"] <= value_range[1])
            ]

            # -------- filtro posición --------

            if positions:
                df = df[df["Posicion"].isin(positions)]

            if df.empty:
                return {}, {}, [], [], []

            # -------- scatter --------

            scatter = px.scatter(

                df,
                x="Edad",
                y="ValorMercado",
                color="Liga",
                size="ValorMercado",
                hover_name="Jugador",
                title="Age vs Market Value"

            )

            # -------- barras apiladas --------

            grouped = (
                df
                .groupby(["Liga", "Posicion"])
                .size()
                .reset_index(name="Count")
            )

            bar = px.bar(

                grouped,
                x="Liga",
                y="Count",
                color="Posicion",
                barmode="stack",
                title="Players by Position in Each League"

            )

            # -------- tabla --------

            data = df.to_dict("records")

            columns = [{"name": c, "id": c} for c in df.columns]

            # -------- opciones dropdown --------

            position_options = [

                {"label": p, "value": p}

                for p in sorted(df["Posicion"].unique())

            ]

            return scatter, bar, data, columns, position_options

        except Exception as e:

            print("Error updating market value page:", e)

            return {}, {}, [], [], []