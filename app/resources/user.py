
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
        """
        Get all users
        ---
        tags:
          - Users
        summary: Retrieve all users
        description: This endpoint retrieves all users from the system.
        responses:
          200:
            description: List of all users retrieved successfully
            schema:
              type: array
              items:
            type: object
            properties:
              id:
                type: integer
                description: The unique identifier of the user
              username:
                type: string
                description: The username of the user
              email:
                type: string
                description: The email address of the user
              created_at:
                type: string
                format: date-time
                description: The creation date of the user
          404:
            description: Users not found
            schema:
              type: object
              properties:
            message:
              type: string
              description: users not found
        """
        users = UserModel.query.all()
        if not users:
            abort(404, message='users not found')
        return users 
    
    #create a user

    @marshal_with(user_fields)
    def post(self):
        """
        Create a new user
        ---
        tags:
          - Users
        summary: Create a new user
        description: This endpoint allows you to create a new user in the system.
        parameters:
          - in: body
            name: user
            description: User object that needs to be created
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username of the user
                email:
                  type: string
                  description: The email address of the user
                password:
                  type: string
                  description: The password for the user account
        responses:
          201:
            description: User created successfully
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique identifier of the user
                  username:
                    type: string
                    description: The username of the user
                  email:
                    type: string
                    description: The email address of the user
          400:
            description: Error creating user
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Error message detailing the issue
        """
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
        """
        Get a user by id
        ---
        tags:
          - Users
        summary: Retrieve a user by ID
        description: This endpoint retrieves a user by their unique identifier (ID).
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: The unique identifier of the user to retrieve
        responses:
          200:
            description: User retrieved successfully
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: The unique identifier of the user
                username:
                  type: string
                  description: The username of the user
                email:
                  type: string
                  description: The email address of the user
          404:
            description: User not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: User not found message
        """
         # get a user by id
        if not id:
            abort(400, message="id is required")
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="user not found")
        return user, 200
    
    @marshal_with(user_fields)
    def patch(self, id):
        """
        Update a user by id
        ---
        tags:
          - Users
        summary: Update a user by ID
        description: This endpoint allows you to update a user by their unique identifier (ID).
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: The unique identifier of the user to update
          - in: body
            name: user
            description: User object that needs to be updated
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username of the user
                email:
                  type: string
                  description: The email address of the user
                password:
                  type: string
                  description: The password for the user account
        responses:
            200:
                description: User updated successfully
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The unique identifier of the user
                    username:
                      type: string
                      description: The username of the user
                    email:
                      type: string
                      description: The email address of the user
            404:
                description: User not found
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      description: User not found message
        """
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
        """
        Delete a user by id
        ---
        tags:
          - Users
        summary: Delete a user by ID
        description: This endpoint allows you to delete a user by their unique identifier (ID).
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: The unique identifier of the user to delete
        responses:

            200:
                description: User deleted successfully
                schema:
                type: string
                example: "user deleted successfully"
            404:
                description: User not found
                schema:
                type: object
                properties:
                    message:
                    type: string
                    description: User not found message
            """
        user = UserModel.query.filter_by(id=id).first()
        if not user:
             abort(404, message="cannot delete a non existing user")
        db.session.delete(user)
        db.session.commit()
        return "user deleted succesfully"

        

        





















