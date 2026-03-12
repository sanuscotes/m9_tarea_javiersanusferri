# Importación de librerías necesarias
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth.users import User
from config import Config

# Inicialización del gestor de sesiones de Flask-Login
login_manager = LoginManager()

# Función que inicializa el gestor de sesiones
def init_login(server):
    """
    Inicializa el sistema de autenticación en la aplicación Flask.

    Parámetros
    ----------
    server : Flask
        Instancia del servidor Flask sobre el que se configurará el sistema de autenticación.

    Funcionamiento
    --------------
    Esta función conecta Flask-Login con el servidor Flask y define el comportamiento del sistema de autenticación.
    Flask-Login utiliza automáticamente la función user_loader para recuperar el usuario activo en cada petición.
    """
    # Registra el sistema de login dentro del servidor Flask
    login_manager.init_app(server)
    # Define la ruta de login a la que se redirigirá al usuario si intenta acceder a una página protegida sin autenticarse
    login_manager.login_view = "/login"

    @login_manager.user_loader
    def load_user(user_id):
        """
        Recupera un usuario a partir de su identificador almacenado en la sesión.

        Parámetros
        ----------
        user_id : str
            Identificador del usuario guardado en la sesión.

        Devuelve
        --------
        User
            Instancia de la clase User correspondiente al identificador.
        """
        return User(user_id)

# Función que autentica al usuario
def authenticate(username, password):
    """
    Verifica las credenciales introducidas por el usuario.

    Descripción
    -----------
    Esta función compara el nombre de usuario y la contraseña.

    Parámetros
    ----------
    username : str
        Nombre de usuario introducido en el formulario de login.

    password : str
        Contraseña introducida en el formulario de login.

    Devuelve
    --------
    User | None
        - Si las credenciales son correctas, devuelve una instancia de la clase User.
        - Si las credenciales son incorrectas, devuelve None.
    """
    if username == Config.APP_USER and password == Config.APP_PASSWORD:
        return User(username)

    return None