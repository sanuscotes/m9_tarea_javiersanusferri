from dash import Input, Output, State, dcc
import plotly.express as px
import plotly.graph_objects as go
import io

from utils.data_loader import load_performance_data
from utils.cache import cache


# -------- CACHE DATA --------

@cache.memoize(timeout=300)
def get_cached_performance_data():

    return load_performance_data()


def register_performance_callbacks(app):

    # -------- DROPDOWN JUGADORES --------

    @app.callback(

        Output("perf-player-dropdown", "options"),
        Output("perf-player-dropdown", "value"),

        Input("perf-minutes-slider", "value")

    )
    def update_player_dropdown(minutes):

        try:

            df = get_cached_performance_data()

            if df.empty:
                return [], []

            df = df[
                (df["MinutosJugados"] >= minutes[0]) &
                (df["MinutosJugados"] <= minutes[1])
            ]

            players = sorted(df["Jugador"].unique())

            options = [{"label": "Todos", "value": "ALL"}]
            options += [{"label": p, "value": p} for p in players]

            return options, ["ALL"]

        except Exception as e:

            print("Error updating dropdown:", e)
            return [], []


    # -------- ACTUALIZAR GRÁFICOS --------

    @app.callback(

        Output("perf-scatter-goals", "figure"),
        Output("perf-radar-player", "figure"),

        Input("perf-player-dropdown", "value"),
        Input("perf-minutes-slider", "value")

    )
    def update_performance_graphs(players, minutes):

        try:

            df = get_cached_performance_data()

            if df.empty:
                return {}, {}

            df = df[
                (df["MinutosJugados"] >= minutes[0]) &
                (df["MinutosJugados"] <= minutes[1])
            ]

            if players and "ALL" not in players:
                df = df[df["Jugador"].isin(players)]

            # -------- SCATTER --------

            scatter = px.scatter(
                df,
                x="GolesEsperados",
                y="Goles",
                color="Jugador",
                size="MinutosJugados",
                hover_name="Jugador",
                title="Goals vs Expected Goals"
            )

            # -------- RADAR --------

            metrics = [
                "Goles",
                "Asistencias",
                "TirosTotales",
                "TirosAPuerta",
                "PasesClave",
                "RegatesExitosos"
            ]

            radar = go.Figure()

            for _, row in df.iterrows():

                radar.add_trace(
                    go.Scatterpolar(
                        r=[row[m] for m in metrics],
                        theta=metrics,
                        fill="toself",
                        name=row["Jugador"]
                    )
                )

            radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title="Player Offensive Profile"
            )

            return scatter, radar

        except Exception as e:

            print("Error updating graphs:", e)
            return {}, {}


    # -------- DESCARGA PDF --------

    @app.callback(

        Output("download-performance-pdf", "data"),

        Input("btn-download-pdf", "n_clicks"),

        State("perf-player-dropdown", "value"),
        State("perf-minutes-slider", "value"),

        prevent_initial_call=True

    )
    def download_pdf(n_clicks, players, minutes):

        try:

            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
            from reportlab.lib.styles import getSampleStyleSheet

            df = get_cached_performance_data()

            if df.empty:
                return dash.no_update

            df = df[
                (df["MinutosJugados"] >= minutes[0]) &
                (df["MinutosJugados"] <= minutes[1])
            ]

            if players and "ALL" not in players:
                df = df[df["Jugador"].isin(players)]

            # -------- SCATTER --------

            scatter = px.scatter(
                df,
                x="GolesEsperados",
                y="Goles",
                color="Jugador",
                size="MinutosJugados",
                hover_name="Jugador"
            )

            # -------- RADAR --------

            metrics = [
                "Goles",
                "Asistencias",
                "TirosTotales",
                "TirosAPuerta",
                "PasesClave",
                "RegatesExitosos"
            ]

            radar = go.Figure()

            for _, row in df.iterrows():

                radar.add_trace(
                    go.Scatterpolar(
                        r=[row[m] for m in metrics],
                        theta=metrics,
                        fill="toself",
                        name=row["Jugador"]
                    )
                )

            radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title="Player Offensive Profile"
            )

            # -------- CONVERTIR GRÁFICOS --------

            scatter_img = io.BytesIO(scatter.to_image(format="png", scale=2))
            radar_img = io.BytesIO(radar.to_image(format="png", scale=2))

            # -------- CREAR PDF --------

            buffer = io.BytesIO()
            styles = getSampleStyleSheet()

            elements = []

            elements.append(Paragraph("Player Performance Report", styles["Title"]))
            elements.append(Spacer(1, 10))

            elements.append(Paragraph(f"Players selected: {players}", styles["Normal"]))
            elements.append(Paragraph(f"Minutes filter: {minutes}", styles["Normal"]))

            elements.append(Spacer(1, 25))

            elements.append(Image(scatter_img, width=450, height=300))

            elements.append(Spacer(1, 30))

            elements.append(Image(radar_img, width=450, height=300))

            doc = SimpleDocTemplate(buffer)
            doc.build(elements)

            buffer.seek(0)

            return dcc.send_bytes(buffer.getvalue(), "performance_report.pdf")

        except Exception as e:

            print("Error generating PDF:", e)

            return dash.no_update