
from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.extension import db
from app.models.user import UserModel



 # request parser
user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank" )
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank" )
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank" )

 # output field
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,

}

 # resource for all users
class Users(Resource):
    #Get all users
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, message='users not found')
        return users 
    
    #create a user
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        try:
            new_user = UserModel(username=args['username'], email=args['email'], password=args['password'])
            db.session.add(new_user)
            db.session.commit()
            users = UserModel.query.all()
            return users, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"there was an error creating user: {e}")
        users = UserModel.query.all()
        return users, 201


class user(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="user not found")
        return user, 200
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="No user with that id")
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        db.session.commit()
        return user, 200
    
    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
             abort(404, message="cannot delete a non existing user")
        db.session.delete(user)
        db.session.commit()
        return "user deleted succesfully"

        

        





















