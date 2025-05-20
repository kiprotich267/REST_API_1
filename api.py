from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, marshal_with, fields, reqparse, abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
db = SQLAlchemy(app)
api = Api(app)


#Database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.username} {self.email}"
    

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank" )
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank" )

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
}


class User(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, message='users not found')
        return users 
    
api.add_resource(User, '/api/users')











class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api')







if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)