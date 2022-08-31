import time
from flask import Flask, request
from config import DATABASE_CONNECTION_URI
from models import *
from sqlalchemy.sql import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_database():
    database.create_all()

@app.route('/')
def hello():
    """ populates database with 3 registers"""
    new_user1 = UserModel(login='danribeiro1',senha='daniou2')
    new_user2 = UserModel(login='danribeiro2',senha='daniou3')
    new_user3 = UserModel(login='danribeiro3',senha='daniou4')
    database.session.add(new_user1)
    database.session.commit()
    database.session.add(new_user2)
    database.session.commit()
    database.session.add(new_user3)
    database.session.commit()
    return 'This is running!!. Users created'


@app.route('/usuarios/normal/<int:user_id>')
def get_normal(user_id):
    """
    Runs 50000 times same queries and returns the process time without bind variables
    """
    start_time = time.time()
    aux = 1
    while aux < 50000:
        UserModel.find_user(user_id)
        aux = aux + 1
    return {'performance':"--- %s seconds ---" % (time.time() - start_time)}


@app.route('/usuarios/bind/<int:user_id>')
def get_bind(user_id):
    """
    Returns user using bindparam
    """
    start_time = time.time()
    aux = 1
    while aux < 50000:
        database.session.query(UserModel)\
        .filter(UserModel.user_id == database.bindparam('my_id'))\
        .params(my_id=user_id)
        aux = aux + 1
    return {'performance':"--- %s seconds using bindparam ---" % (time.time() - start_time)}


@app.route('/usuarios/injection', methods=['GET'])
def get_injection():
    """
    SQL injection use case passing str login by filter
    """
    arg_value = request.args.get('login',None)

    try:
        result = database.session.query(UserModel).filter_by(login=arg_value).first()
    except Exception as e:
        result = e
    return { "data":arg_value,'result': str(result)}


if __name__  == '__main__':
    database.init_app(app)
    app.run(host="0.0.0.0", debug=True)
    