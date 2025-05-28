from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.teacher import TeacherModel
from app.extension import db


teacher_args = reqparse.RequestParser()
teacher_args.add_argument('first_name', type=str, required=True, help="First name is required")
teacher_args.add_argument('last_name', type=str, required=True, help="Last name is required")
teacher_args.add_argument('email', type=str, required=True, help="Email is required")
teacher_args.add_argument('phone', type=str)
teacher_args.add_argument('department', type=str)
teacher_args.add_argument('credits', type=int, help="Credits are required")

teacher_fields = {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'department': fields.String,
    'credits': fields.Integer,
    'hire_date': fields.DateTime
}

class Teachers(Resource):
    @marshal_with(teacher_fields)
    def get(self):
        """
        Get all teachers
        ---
        tags:
            - Teachers
        summary: Retrieve all teachers
        description: This endpoint retrieves all teachers from the system.
        responses:
            200:
                description: List of all teachers retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: string
                                description: The unique identifier of the teacher
                            first_name:
                                type: string
                                description: The first name of the teacher
                            last_name:
                                type: string
                                description: The last name of the teacher
                            email:
                                type: string
                                description: The email address of the teacher
                            phone:
                                type: string
                                description: The phone number of the teacher
                            department:
                                type: string
                                description: The department of the teacher
                            credits:
                                type: integer
                                description: The credits assigned to the teacher
                            hire_date:
                                type: string
                                format: date-time
                                description: The hire date of the teacher
            404:
                description: Teachers not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that no teachers were found.
        """
        teachers = TeacherModel.query.all()
        if not teachers:
            abort(404, message="Teachers not found")
        return teachers

    @marshal_with(teacher_fields)
    def post(self):
        """
        Create a new teacher
        ---
        tags:
            - Teachers
        summary: Create a new teacher
        description: This endpoint allows you to create a new teacher in the system.

        parameters:
            - in: body
              name: teacher
              description: Teacher object that needs to be created
              required: true
              schema:
                type: object
                properties:
                    first_name:
                        type: string
                        description: The first name of the teacher
                    last_name:
                        type: string
                        description: The last name of the teacher
                    email:
                        type: string
                        description: The email address of the teacher
                    phone:
                        type: string
                        description: The phone number of the teacher (optional)
                    department:
                        type: string
                        description: The department of the teacher (optional)
                    credits:
                        type: integer
                        description: The credits assigned to the teacher (optional)
        responses:
            201:
                description: Teacher created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: string
                            description: The unique identifier of the created teacher
                        first_name:
                            type: string
                            description: The first name of the created teacher
                        last_name:
                            type: string
                            description: The last name of the created teacher
                        email:
                            type: string
                            description: The email address of the created teacher
                        phone:
                            type: string
                            description: The phone number of the created teacher
                        department:
                            type: string
                            description: The department of the created teacher
                        credits:
                            type: integer
                            description: The credits assigned to the created teacher
                        hire_date:
                            type: string
                            format: date-time
                            description: The hire date of the created teacher
            400:
                description: Error creating teacher
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating what went wrong.
        """
        args = teacher_args.parse_args()
        try:
            new_teacher = TeacherModel(
                first_name=args['first_name'],
                last_name=args['last_name'],
                email=args['email'],
                phone=args['phone'],
                department=args['department'],
                credits=args['credits']
            )
            db.session.add(new_teacher)
            db.session.commit()
            return new_teacher, 201
        
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error creating as teacher{str(e)}")

            #specific teacher,edit and delete a teacher

class Teacher(Resource):
    @marshal_with(teacher_fields)
    def get(self, id):
        """
        Get a specific teacher by ID
        ---
        tags:
            - Teachers
        summary: Retrieve a teacher by ID
        description: This endpoint retrieves a specific teacher's details by their unique ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the teacher to retrieve
        responses:
            200:
                description: Teacher details retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: string
                            description: The unique identifier of the teacher
                        first_name:
                            type: string
                            description: The first name of the teacher
                        last_name:
                            type: string
                            description: The last name of the teacher
                        email:
                            type: string
                            description: The email address of the teacher
                        phone:
                            type: string
                            description: The phone number of the teacher
                        department:
                            type: string
                            description: The department of the teacher
                        credits:
                            type: integer
                            description: The credits assigned to the teacher
                        hire_date:
                            type: string
                            format: date-time
                            description: The hire date of the teacher
            404:
                description: Teacher not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the teacher was not found.
        """
        teacher = TeacherModel.query.filter_by(id=id).first()
        if not teacher:
            abort(404, message='Teacher not found')
        return teacher
    
    @marshal_with(teacher_fields)
    def patch(self, id):
        """
        Update a specific teacher by ID
        ---
        tags:
            - Teachers
        summary: Update a teacher's details by ID
        description: This endpoint allows you to update a specific teacher's details by their unique ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the teacher to update
            - in: body
              name: teacher
              description: Teacher object that needs to be updated
              required: true
              schema:
                type: object
                properties:
                    first_name:
                        type: string
                        description: The first name of the teacher (optional)
                    last_name:
                        type: string
                        description: The last name of the teacher (optional)
                    email:
                        type: string
                        description: The email address of the teacher (optional)
                    phone:
                        type: string
                        description: The phone number of the teacher (optional)
                    department:
                        type: string
                        description: The department of the teacher (optional)
                    credits:
                        type: integer
                        description: The credits assigned to the teacher (optional)
        responses:
            200:
                description: Teacher updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: string
                            description: The unique identifier of the updated teacher
                        first_name:
                            type: string
                            description: The first name of the updated teacher
                        last_name:
                            type: string
                            description: The last name of the updated teacher
                        email:
                            type: string
                            description: The email address of the updated teacher
                        phone:
                            type: string
                            description: The phone number of the updated teacher
                        department:
                            type: string
                            description: The department of the updated teacher
                        credits:
                            type: integer
                            description: The credits assigned to the updated teacher
                        hire_date:
                            type: string
                            format: date-time
                            description: The hire date of the updated teacher
            404:
                description: Teacher not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the teacher was not found.
        """
        args = teacher_args.parse_args()
        teacher = TeacherModel.query.filter_by(id=id).first()
        if not teacher:
            abort(404, message='Teacher not found')
        teacher.first_name = args['first_name']
        teacher.last_name = args['last_name']
        teacher.email = args['email']
        teacher.phone = args['phone']
        teacher.department = args['department']
        teacher.credits = args['credits']
        db.session.commit()
        return teacher
    @marshal_with(teacher_fields)
    def delete(self, id):
        """
        Delete a specific teacher by ID
        ---
        tags:
            - Teachers
        summary: Delete a teacher by ID
        description: This endpoint allows you to delete a specific teacher by their unique ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the teacher to delete
        responses:
            204:
                description: Teacher deleted successfully
            404:
                description: Teacher not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the teacher was not found.
        """
        teacher = TeacherModel.query.filter_by(id=id).first()
        if not teacher:
            abort(404, message='Teacher not found')
        db.session.delete(teacher)
        db.session.commit()
        return '', 204
