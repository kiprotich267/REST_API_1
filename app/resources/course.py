from flask_restful import Resource, marshal_with, fields, reqparse,abort
from app.models.course import CourseModel
from app.extension import db



#request parser
from flask_restful import reqparse

course_args = reqparse.RequestParser()
course_args.add_argument('code', type=str, required=True, help="Course code cannot be empty")
course_args.add_argument('name', type=str, required=True, help="Course name cannot be empty")
course_args.add_argument('credits', type=int, default=0, help="Credits must be an integer")
course_args.add_argument('teacher_id', type=int, required=True, help="Teacher ID is required")


#response fields
course_fields = {
    'id': fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'credits': fields.Integer,
    'teacher_id': fields.Integer
    
}
# course resource
class Courses(Resource):
    @marshal_with(course_fields)
    def get(self):
        """
        Get all courses
        ---
        tags:
            - Courses
        summary: Retrieve all courses
        description: This endpoint retrieves all courses from the system.
        responses:
            200:
                description: List of all courses retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the course
                            code:
                                type: string
                                description: The code of the course
                            name:
                                type: string
                                description: The name of the course
                            credits:
                                type: integer
                                description: The number of credits for the course
                            teacher_id:
                                type: integer
                                description: The ID of the teacher for the course
            404:
                description: Courses not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that no courses were found
        """
        courses = CourseModel.query.all()
        if not courses:
            abort(404, message='Courses not found')
        return courses
    
    @marshal_with(course_fields)
    def post(self):
        """
        Create a new course
        ---
        tags:
            - Courses
        summary: Create a new course
        description: This endpoint creates a new course in the system.
        responses:
            201:
                description: Course created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created course
                        code:
                            type: string
                            description: The code of the created course
                        name:
                            type: string
                            description: The name of the created course
                        credits:
                            type: integer
                            description: The number of credits for the created course
                        teacher_id:
                            type: integer
                            description: The ID of the teacher for the created course
            400:
                description: Error creating course
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating why the course could not be created
        """
        args = course_args.parse_args()
        try:
            course = CourseModel(
                code=args['code'],
                name=args['name'],
                credits=args['credits'],
                teacher_id=args['teacher_id']
               
            )
            db.session.add(course)
            db.session.commit()
            return course, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not create a course {str(e)}")
class Course(Resource):
    @marshal_with(course_fields)
    def get(self, id):
        """
        Get a course by id
        ---
        tags:
            - Courses
        summary: Retrieve a course by ID
        description: This endpoint retrieves a course by its unique identifier (ID).
        parameters:
            - in: path
              name: id
              required: true
              type: integer
              description: The unique identifier of the course to retrieve
        responses:
            200:
                description: Course retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the course
                        code:
                            type: string
                            description: The code of the course
                        name:
                            type: string
                            description: The name of the course
                        credits:
                            type: integer
                            description: The number of credits for the course
                        teacher_id:
                            type: integer
                            description: The ID of the teacher for the course
            404:
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the course was not found
        """
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        return course
    @marshal_with(course_fields)
    def put(self, id):
        """ 
        Update a course by id
        ---
        tags:
            - Courses
        summary: Update a course by ID
        description: This endpoint updates a course by its unique identifier (ID).
        parameters:
            - in: path
              name: id
              required: true
              type: integer
              description: The unique identifier of the course to update
        responses:
            200:
                description: Course updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the course
                        code:
                            type: string
                            description: The code of the course
                        name:
                            type: string
                            description: The name of the course
                        credits:
                            type: integer
                            description: The number of credits for the course
                        teacher_id:
                            type: integer
                            description: The ID of the teacher for the course
            404:
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the course was not found
            400:
                description: Error updating course
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating why the course could not be updated
        """
        args = course_args.parse_args()
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        try:
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            db.session.commit()
            return course, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not update a course {str(e)}")
    @marshal_with(course_fields)
    def patch(self, id):
        """
        Update a course by id
        ---
        tags:
            - Courses
        summary: Update a course by ID
        description: This endpoint updates a course by its unique identifier (ID).
        parameters:
            - in: path
              name: id
              required: true
              type: integer
              description: The unique identifier of the course to update
        responses:
            200:
                description: Course updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the course
                        code:
                            type: string
                            description: The code of the course
                        name:
                            type: string
                            description: The name of the course
                        credits:
                            type: integer
                            description: The number of credits for the course
                        teacher_id:
                            type: integer
                            description: The ID of the teacher for the course
            404:
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the course was not found
            400:
                description: Error updating course
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating why the course could not be updated
        """
        args = course_args.parse_args()
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        try:
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            db.session.commit()
            return course, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not update a course {str(e)}")
    @marshal_with(course_fields)
    def delete(self, id):
        """
        Delete a course by id
        ---
        tags:
            - Courses
        summary: Delete a course by ID
        description: This endpoint deletes a course by its unique identifier (ID).
        parameters:
            - in: path
              name: id
              required: true
              type: integer
              description: The unique identifier of the course to delete
        responses:
            204:
                description: Course deleted successfully
            404:
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message indicating that the course was not found
        """
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message='Course not found')
        db.session.delete(course)
        db.session.commit()
        return '', 204