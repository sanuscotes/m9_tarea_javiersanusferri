import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

# configuración
from config import Config

# páginas
from pages import home, performance, market_value

# componentes
from components.navbar import navbar
from components.layout import layout

# utilidades
from utils.cache import init_cache

# callbacks
from callbacks import (
    register_performance_callbacks,
    register_market_value_callbacks
)

# -----------------------------------
# Flask server
# -----------------------------------

server = Flask(__name__)
server.secret_key = Config.SECRET_KEY


# -----------------------------------
# Inicializar cache
# -----------------------------------

init_cache(server, Config)


# -----------------------------------
# Flask-Login setup
# -----------------------------------

login_manager = LoginManager()
login_manager.init_app(server)


class User(UserMixin):

    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):

    if user_id == "admin":
        return User(user_id)

    return None


# -----------------------------------
# Dash app
# -----------------------------------

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# layout global
app.layout = layout


# -----------------------------------
# Registrar callbacks externos
# -----------------------------------

register_performance_callbacks(app)
register_market_value_callbacks(app)


# -----------------------------------
# Layout login
# -----------------------------------

login_layout = dbc.Container(

    [

        html.H2("Login", className="mb-3"),

        dbc.Input(
            id="username",
            placeholder="Usuario",
        ),

        dbc.Input(
            id="password",
            type="password",
            placeholder="Contraseña",
            className="mt-2",
        ),

        dbc.Button(
            "Login",
            id="login-button",
            className="mt-3",
            color="primary"
        ),

        html.Div(
            id="login-message",
            style={"color": "red", "marginTop": "10px"}
        ),

    ],

    style={
        "width": "350px",
        "margin": "120px auto"
    },

)


# -----------------------------------
# LOGIN callback
# -----------------------------------

@app.callback(
    Output("url", "pathname"),
    Output("login-message", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login(n_clicks, username, password):

    if not n_clicks:
        return dash.no_update, ""

    if username == "admin" and password == "admin":

        user = User(username)
        login_user(user)

        return "/home", ""

    return dash.no_update, "Usuario o contraseña incorrectos"


# -----------------------------------
# Router protegido
# -----------------------------------

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):

    if pathname == "/logout":

        logout_user()
        return login_layout

    if not current_user.is_authenticated:

        return login_layout

    if pathname == "/home":

        page = home.layout

    elif pathname == "/performance":

        page = performance.layout

    elif pathname == "/market_value":

        page = market_value.layout

    else:

        page = home.layout

    return html.Div(
        [
            navbar,
            html.Div(page)
        ]
    )


# -----------------------------------
# Run
# -----------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)