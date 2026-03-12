# Importación de UserMixin de Flask-Login
from flask_login import UserMixin

# Clase usuario
class User(UserMixin):
    """
    Modelo simple de usuario para Flask-Login.
    """
    # Constructor de la clase User
    def __init__(self, username):
        self.id = username