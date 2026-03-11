from flask_login import UserMixin


class User(UserMixin):
    """
    Modelo simple de usuario para Flask-Login.
    """
    
    def __init__(self, username):
        self.id = username