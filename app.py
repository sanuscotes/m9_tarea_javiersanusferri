# Importación de librerías
import os

# Importación de Dash y sus componentes
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Importación de Flask y Flask-Login
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

# Importación de la configuración de la app
from config import Config

# Importación de las páginas de la app
from pages import home, performance, market_value

# Importación de componentes de la app
from components.navbar import navbar
from components.layout import layout

# Importación de utilidades de la app
from utils.cache import init_cache

# Importación de callbacks de la app
from callbacks import (register_performance_callbacks, register_market_value_callbacks)



# Flask server (WSGI), se crea una instancia de Flask que actuará como servidor base.
server = Flask(__name__)
server.secret_key = Config.SECRET_KEY



# Inicializar el sistema de cache definido en utils/cache.py
init_cache(server, Config)



# Configuración del sistema de autenticación mediante Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)



# Definición de la clase User que hereda de UserMixin
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Callback para cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    """
    Función utilizada por Flask-Login para recuperar el usuario asociado a una sesión activa.

    Parámetros
    ----------
    user_id : str
        Identificador del usuario almacenado en la sesión cuando se realiza el login.

    Funcionamiento
    --------------
    Flask-Login guarda en la sesión el identificador del usuario autenticado.

    Devuelve
    --------
    User | None
        Objeto User si el usuario existe, o None si no se encuentra un usuario válido.
    """
    if user_id == "admin":
        return User(user_id)

    return None



# Se inicializa la aplicación Dash utilizando el servidor Flask creado anteriormente
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# Referencia explícita para Gunicorn
server = app.server

# Layout global
app.layout = layout

# Registro de callbacks externos
register_performance_callbacks(app)
register_market_value_callbacks(app)

# Layout login que se muestra cuando el usuario no ha iniciado sesión
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

# Callback login que gestiona el proceso de autenticación
@app.callback(
    Output("url", "pathname"),
    Output("login-message", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)

def login(n_clicks, username, password):
    """
    Gestiona el proceso de autenticación del usuario en la aplicación.

    Parámetros
    ----------
    n_clicks : int
        Número de veces que se ha pulsado el botón de login. Es utilizado por Dash para activar el callback.

    username : str
        Valor introducido por el usuario en el campo de nombre de usuario.

    password : str
        Valor introducido por el usuario en el campo de contraseña.

    Funcionamiento
    --------------
    Este callback se ejecuta cuando el usuario pulsa el botón de login.

    Devuelve
    --------
    tuple
        Contiene dos elementos:
        - pathname de la URL a la que se debe redirigir al usuario.
        - mensaje de error mostrado en la interfaz (si existe).
    """
    if not n_clicks:
        return dash.no_update, ""

    if username == "admin" and password == "admin":
        user = User(username)
        login_user(user)
        return "/home", ""

    return dash.no_update, "Usuario o contraseña incorrectos"

# Router protegido que gestiona la navegación entre páginas
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)

def display_page(pathname):
    """
    Gestiona la navegación entre páginas de la aplicación.

    Parámetros
    ----------
    pathname : str
        Ruta actual de la URL detectada por el componente dcc.Location.

    Funcionamiento
    --------------
    Este callback actúa como router principal de la aplicación Dash.

    Devuelve
    --------
    html.Div
    """
    # Ruta para cerrar sesión
    if pathname == "/logout":
        logout_user()
        return login_layout

    # Si el usuario no está autenticado se muestra login
    if not current_user.is_authenticated:
        return login_layout

    # Selección de página según URL
    if pathname == "/home":
        page = home.layout

    elif pathname == "/performance":
        page = performance.layout

    elif pathname == "/market_value":
        page = market_value.layout

    else:
        page = home.layout

    # Renderizado final con navbar + contenido
    return html.Div(
        [
            navbar,
            html.Div(page)
        ]
    )

# Ejecución local de la aplicación
if __name__ == "__main__":
    # Puerto dinámico para compatibilidad con plataformas cloud
    port = int(os.environ.get("PORT", 8080))
    # Arranque del servidor Dash
    app.run(host="0.0.0.0", port=port)