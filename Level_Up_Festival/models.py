from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, surname, email, password, type):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.type = type