from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class UserModel(database.Model):
    __tablename__ = 'usuario'

    user_id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(40))
    senha = database.Column(database.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
        }

    @classmethod
    def find_user(cls, user_id):
        """
        Encontra usuário na lista de usuários
        """
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def check_user_exists(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()