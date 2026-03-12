# Importación de librerías necesarias
from dash import Input, Output, State, dcc
import plotly.express as px
import plotly.graph_objects as go
import io
from utils.data_loader import load_performance_data
from utils.cache import cache
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


# Cache de datos
@cache.memoize(timeout=300)
# Función para cargar los datos de rendimiento
def get_cached_performance_data():
    """
    Obtiene los datos de rendimiento de jugadores utilizando cache.

    Descripción
    -----------
    Esta función envuelve la carga de datos de rendimiento para evitar múltiples lecturas del archivo CSV.

    Devuelve
    --------
    pandas.DataFrame
        DataFrame con los datos de rendimiento de jugadores.
    """
    return load_performance_data()

# Registro de callbacks
def register_performance_callbacks(app):
    """
    Registra todos los callbacks asociados al Performance Dashboard.

    Parámetros
    ----------
    app : Dash
        Instancia principal de la aplicación Dash.

    Descripción
    -----------
    Esta función agrupa la lógica interactiva de la página de rendimiento.
    """
    @app.callback(

        Output("perf-player-dropdown", "options"),
        Output("perf-player-dropdown", "value"),
        Input("perf-minutes-slider", "value")

    )

    # Función para actualizar el dropdown de jugadores
    def update_player_dropdown(minutes):
        """
        Actualiza las opciones del dropdown de jugadores en función del filtro de minutos jugados.

        Parámetros
        ----------
        minutes : list
            Rango de minutos seleccionados en el slider.

        Devuelve
        --------
        tuple
            Lista de opciones disponibles en el dropdown y valor seleccionado por defecto.
        """
        try:
            # Cargar datos desde cache
            df = get_cached_performance_data()
            if df.empty:
                return [], []
            # Filtrar datos por minutos jugados
            df = df[
                (df["MinutosJugados"] >= minutes[0]) &
                (df["MinutosJugados"] <= minutes[1])
            ]
            # Obtener lista de jugadores únicos
            players = sorted(df["Jugador"].unique())
            # Crear opciones para el dropdown
            options = [{"label": "Todos", "value": "ALL"}]
            options += [{"label": p, "value": p} for p in players]

            return options, ["ALL"]

        except Exception as e:
            print("Error updating dropdown:", e)
            return [], []


    # Actualizar Gráficos
    @app.callback(
        Output("perf-scatter-goals", "figure"),
        Output("perf-radar-player", "figure"),
        Input("perf-player-dropdown", "value"),
        Input("perf-minutes-slider", "value")
    )

    # Función para actualizar los gráficos
    def update_performance_graphs(players, minutes):
        """
        Genera y actualiza los gráficos del Performance Dashboard.

        Parámetros
        ----------
        players : list
            Jugadores seleccionados en el dropdown.

        minutes : list
            Rango de minutos jugados seleccionado.

        Devuelve
        --------
        tuple
            Figura scatter y figura radar con métricas ofensivas.
        """
        try:
            # Cargar datos desde cache
            df = get_cached_performance_data()
            # Comprobación de datos
            if df.empty:
                return {}, {}
            # Filtrar datos por minutos jugados
            df = df[
                (df["MinutosJugados"] >= minutes[0]) &
                (df["MinutosJugados"] <= minutes[1])
            ]
            # Comprobación de datos
            if players and "ALL" not in players:
                df = df[df["Jugador"].isin(players)]


            # Scatter - Gráfico que muestra la relación entre goles esperados y goles por jugador
            scatter = px.scatter(
                df,
                x="GolesEsperados",
                y="Goles",
                color="Jugador",
                size="MinutosJugados",
                hover_name="Jugador",
                title="Goals vs Expected Goals"
            )

            # Radar - Gráfico que muestra el perfil ofensivo de cada jugador
            metrics = [
                "Goles",
                "Asistencias",
                "TirosTotales",
                "TirosAPuerta",
                "PasesClave",
                "RegatesExitosos"
            ]
            # Crear figura radar
            radar = go.Figure()
            # Añadir trazas para cada jugador
            for _, row in df.iterrows():
                radar.add_trace(
                    go.Scatterpolar(
                        r=[row[m] for m in metrics],
                        theta=metrics,
                        fill="toself",
                        name=row["Jugador"]
                    )
                )
            # Actualizar layout del radar
            radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title="Player Offensive Profile"
            )
            # Se devuelven todos los componentes actualizados
            return scatter, radar

        except Exception as e:
            print("Error updating graphs:", e)
            return {}, {}


    # Generación y descarga PDF
    @app.callback(
        Output("download-performance-pdf", "data"),
        Input("btn-download-pdf", "n_clicks"),
        State("perf-player-dropdown", "value"),
        State("perf-minutes-slider", "value"),
        prevent_initial_call=True
    )

    # Función para generar y descargar el PDF
    def download_pdf(n_clicks, players, minutes):
        """
        Genera un reporte PDF con los gráficos del Performance Dashboard.

        Parámetros
        ----------
        n_clicks : int
            Número de veces que se ha pulsado el botón de descarga.

        players : list
            Jugadores seleccionados.

        minutes : list
            Rango de minutos jugados seleccionado.

        Devuelve
        --------
        dcc.Download
            Archivo PDF generado dinámicamente.
        """
        try:
            # Cargar datos desde cache
            df = get_cached_performance_data()
            # Comprobación de datos
            if df.empty:
                return dash.no_update
            # Filtrar datos por minutos jugados
            df = df[
                (df["MinutosJugados"] >= minutes[0]) &
                (df["MinutosJugados"] <= minutes[1])
            ]
            # Comprobación de datos
            if players and "ALL" not in players:
                df = df[df["Jugador"].isin(players)]

            # Scatter - Gráfico que muestra la relación entre goles esperados y goles por jugador
            scatter = px.scatter(
                df,
                x="GolesEsperados",
                y="Goles",
                color="Jugador",
                size="MinutosJugados",
                hover_name="Jugador"
            )

            # Radar - Gráfico que muestra el perfil ofensivo de cada jugador
            metrics = [
                "Goles",
                "Asistencias",
                "TirosTotales",
                "TirosAPuerta",
                "PasesClave",
                "RegatesExitosos"
            ]
            # Crear figura radar
            radar = go.Figure()
            # Añadir trazas para cada jugador
            for _, row in df.iterrows():
                radar.add_trace(
                    go.Scatterpolar(
                        r=[row[m] for m in metrics],
                        theta=metrics,
                        fill="toself",
                        name=row["Jugador"]
                    )
                )
            # Actualizar layout del radar
            radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title="Player Offensive Profile"
            )

            # Convertir gráficos a formato PNG
            scatter_img = io.BytesIO(scatter.to_image(format="png", scale=2))
            radar_img = io.BytesIO(radar.to_image(format="png", scale=2))


            # Crear PDF
            buffer = io.BytesIO()
            styles = getSampleStyleSheet()
            elements = []

            # Título del reporte
            elements.append(Paragraph("Player Performance Report", styles["Title"]))
            elements.append(Spacer(1, 10))

            # Información del reporte sobre los filtros aplicados
            elements.append(Paragraph(f"Players selected: {players}", styles["Normal"]))
            elements.append(Paragraph(f"Minutes filter: {minutes}", styles["Normal"]))
            elements.append(Spacer(1, 25))

            # Añadir gráficos al reporte
            elements.append(Image(scatter_img, width=450, height=300))
            elements.append(Spacer(1, 30))
            elements.append(Image(radar_img, width=450, height=300))

            # Construir PDF
            doc = SimpleDocTemplate(buffer)
            doc.build(elements)

            buffer.seek(0)
            
            # Enviar archivo al navegador para descarga
            return dcc.send_bytes(buffer.getvalue(), "performance_report.pdf")

        except Exception as e:
            print("Error generating PDF:", e)
            return dash.no_update