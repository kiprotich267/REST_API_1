from flask import Flask 
from flask_restful import Api
from app.resources.user import Users, user
from app.extension import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
db.init_app(app)

api = Api(app)






# Api endpoints
api.add_resource(Users, '/api/users')
api.add_resource(user, '/api/users/<int:id>')