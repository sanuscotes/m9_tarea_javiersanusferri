# Importación de librerías necesarias
from dash import Input, Output
import plotly.express as px
from utils.data_loader import load_market_value_data
from utils.cache import cache


# Cache de datos
@cache.memoize(timeout=300)
# Función para cargar los datos de valor de mercado
def get_cached_market_value_data():
    """
    Obtiene los datos de valor de mercado utilizando un sistema de cache.

    Descripción
    -----------
    Esta función actúa como una capa intermedia entre los callbacks y la función que carga los datos desde la base de datos.

    Devuelve
    --------
    pandas.DataFrame
        DataFrame con los datos de valor de mercado de jugadores.
    """
    return load_market_value_data()

# Registro de callbacks
def register_market_value_callbacks(app):
    """
    Registra los callbacks necesarios para el funcionamiento del dashboard de valor de mercado.

    Parámetros
    ----------
    app : Dash
        Instancia principal de la aplicación Dash.

    Descripción
    -----------
    Esta función agrupa todos los callbacks relacionados con la página Market Value Dashboard y los registra dentro de la aplicación.
    """
    @app.callback(
        Output("age-value-scatter", "figure"),
        Output("league-position-bar", "figure"),
        Output("market-table", "data"),
        Output("market-table", "columns"),
        Output("position-filter", "options"),
        Input("position-filter", "value"),
        Input("value-filter", "value")

    )

    # Actualización de gráficos
    def update_market_value_page(positions, value_range):
        """
        Actualiza todos los componentes del Market Value Dashboard.

        Parámetros
        ----------
        positions : list
            Lista de posiciones seleccionadas en el filtro.

        value_range : list
            Rango de valores seleccionado en el RangeSlider que representa el valor de mercado mínimo y máximo.

        Devuelve
        --------
        tuple
            (scatter_figure, bar_figure, table_data, table_columns, position_options)
        """
        try:
            # Carga de datos
            df = get_cached_market_value_data()
            # Comprobación de datos
            if df.empty:
                return {}, {}, [], [], []

            # Filtro por valores de mercado
            df = df[
                (df["ValorMercado"] >= value_range[0]) &
                (df["ValorMercado"] <= value_range[1])
            ]

            # Filtro por posición
            if positions:
                df = df[df["Posicion"].isin(positions)]
            # Comprobación de datos
            if df.empty:
                return {}, {}, [], [], []

            # Scatter - Gráfico de la relación entre la Edad del jugador y el Valor de Mercado
            scatter = px.scatter(
                df,
                x="Edad",
                y="ValorMercado",
                color="Liga",
                size="ValorMercado",
                hover_name="Jugador",
                title="Age vs Market Value"
            )

            # Barras apiladas - Gráfico de la distribución de jugadores por posición en cada liga
            grouped = (
                df.groupby(["Liga", "Posicion"]).size().reset_index(name="Count")
            )
            bar = px.bar(
                grouped,
                x="Liga",
                y="Count",
                color="Posicion",
                barmode="stack",
                title="Players by Position in Each League"
            )

            # Tabla
            # Conversión del DataFrame a formato compatible con Dash
            data = df.to_dict("records")
            # Definición de columnas de la tabla
            columns = [{"name": c, "id": c} for c in df.columns]

            # Opciones del dropdown
            position_options = [
                {"label": p, "value": p}
                for p in sorted(df["Posicion"].unique())
            ]

            # Se devuelven todos los componentes actualizados
            return scatter, bar, data, columns, position_options

        # Manejo básico de errores para evitar que el dashboard se rompa
        except Exception as e:
            print("Error updating market value page:", e)
            return {}, {}, [], [], []