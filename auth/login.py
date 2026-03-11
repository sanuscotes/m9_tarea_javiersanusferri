from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth.users import User
from config import Config

login_manager = LoginManager()


def init_login(server):

    login_manager.init_app(server)
    login_manager.login_view = "/login"

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)


def authenticate(username, password):
    """
    Verifica usuario y contraseña contra variables del .env
    """

    if username == Config.APP_USER and password == Config.APP_PASSWORD:
        return User(username)

    return None