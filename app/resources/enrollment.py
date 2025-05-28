from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.enrollment import EnrollmentModel
from app.extension import db
from dateutil import parser as date_parser
#request parser
enrollment_args = reqparse.RequestParser()
enrollment_args.add_argument('student_id', type=int, required=True, help="Student ID cannot be empty")
enrollment_args.add_argument('course_id', type=int, required=True, help="Course ID cannot be empty")
enrollment_args.add_argument('enrollment_date', type=date_parser)
enrollment_args.add_argument('status', type=str, default='active')
#response fields
enrollment_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'course_id': fields.Integer,
    'enrollment_date': fields.DateTime,
    'status': fields.String
}
#enrollment resource
class Enrollments(Resource):
    @marshal_with(enrollment_fields)
    def get(self):
        """
        Get all enrollments
        ---
        tags:
          - Enrollments
        summary: Retrieve all enrollments
        description: This endpoint retrieves all enrollments from the system.
        responses:
          200:
            description: List of all enrollments retrieved successfully
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique identifier of the enrollment
                  student_id:
                    type: integer
                    description: The ID of the student enrolled
                  course_id:
                    type: integer
                    description: The ID of the course in which the student is enrolled
                  enrollment_date:
                    type: string
                    format: date-time
                    description: The date when the student was enrolled in the course
                  status:
                    type: string
                    description: The status of the enrollment (e.g., active, completed, dropped)
          404:
            description: Enrollments not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Error message indicating that no enrollments were found
        """
        enrollments = EnrollmentModel.query.all()
        if not enrollments:
            abort(404, message='Enrollments not found')
        return enrollments

    @marshal_with(enrollment_fields)
    def post(self):
        """
        Create a new enrollment
        ---
        tags:
          - Enrollments
        summary: Create a new enrollment
        description: This endpoint allows the creation of a new enrollment for a student in a course.
        responses:
          201:
            description: Enrollment created successfully
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: The unique identifier of the newly created enrollment
                student_id:
                  type: integer
                  description: The ID of the student enrolled
                course_id:
                  type: integer
                  description: The ID of the course in which the student is enrolled
                enrollment_date:
                  type: string
                  format: date-time
                  description: The date when the student was enrolled in the course
                status:
                  type: string
                  description: The status of the enrollment (e.g., active, completed, dropped)
          400:
            description: Error creating enrollment
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Error message indicating that the enrollment could not be created
        """
        args = enrollment_args.parse_args()
        try:
            enrollment = EnrollmentModel(
                student_id=args['student_id'],
                course_id=args['course_id'],
                enrollment_date=args['enrollment_date'],
                status=args['status']
            )
            db.session.add(enrollment)
            db.session.commit()
            return enrollment, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not create an enrollment. {str(e)}")
class Enrollment(Resource):
    @marshal_with(enrollment_fields)
    def get(self, id):
        """
        Get an enrollment by id
        ---
        tags:
          - Enrollments
        summary: Retrieve an enrollment by ID
        description: This endpoint retrieves an enrollment by its unique identifier (ID).
        parameters:
          - in: path
            name: id
            required: true
            type: integer
            description: The unique identifier of the enrollment to retrieve
        responses:
            200:
                description: Enrollment retrieved successfully
                schema:
                type: object
                properties:
                    id:
                    type: integer
                    description: The unique identifier of the enrollment
                    student_id:
                    type: integer
                    description: The ID of the student enrolled
                    course_id:
                    type: integer
                    description: The ID of the course in which the student is enrolled
                    enrollment_date:
                    type: string
                    format: date-time
                    description: The date when the student was enrolled in the course
                    status:
                    type: string
                    description: The status of the enrollment (e.g., active, completed, dropped)
            404:
                description: Enrollment not found
                schema:
                type: object
                properties:
                    message:
                    type: string
                    description: Error message indicating that the enrollment was not found
            """
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message='Enrollment not found')
        return enrollment

    @marshal_with(enrollment_fields)
    def patch(self, id):
        """
        Update an enrollment by id
        ---
        tags:
          - Enrollments
        summary: Update an existing enrollment
        description: This endpoint allows updating an existing enrollment by its unique identifier (ID).
        parameters:
          - in: path
            name: id
            required: true
            type: integer
            description: The unique identifier of the enrollment to update
        responses:
            200:
                description: Enrollment updated successfully
                schema:
                type: object
                properties:
                    id:
                    type: integer
                    description: The unique identifier of the enrollment
                    student_id:
                    type: integer
                    description: The ID of the student enrolled
                    course_id:
                    type: integer
                    description: The ID of the course in which the student is enrolled
                    enrollment_date:
                    type: string
                    format: date-time
                    description: The date when the student was enrolled in the course
                    status:
                    type: string
                    description: The status of the enrollment (e.g., active, completed, dropped)
            404:
                description: Enrollment not found
                schema:
                type: object
                properties:
                    message:
                    type: string
                    description: Error message indicating that the enrollment was not found
            400:
                description: Error updating enrollment
                schema:
                type: object
                properties:
                    message:
                    type: string
                    description: Error message indicating that the enrollment could not be updated
        """
        args = enrollment_args.parse_args()
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message='Enrollment not found')
        try:
            enrollment.student_id = args['student_id']
            enrollment.course_id = args['course_id']
            enrollment.enrollment_date = args['enrollment_date']
            enrollment.status = args['status']
            db.session.commit()
            return enrollment, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not update the enrollment. {str(e)}")
    @marshal_with(enrollment_fields)
    def delete(self, id):
        """
        Delete an enrollment by id
        ---
        tags:
          - Enrollments
        summary: Delete an enrollment by ID
        description: This endpoint allows the deletion of an enrollment by its unique identifier (ID).
        parameters:
          - in: path
            name: id
            required: true
            type: integer
            description: The unique identifier of the enrollment to delete
        responses:
            204:
                description: Enrollment deleted successfully
            404:
                description: Enrollment not found
                schema:
                type: object
                properties:
                    message:
                    type: string
                    description: Error message indicating that the enrollment was not found
            400:
                description: Error deleting enrollment
                schema:
                type: object
                properties:
                    message:
                    type: string
                    description: Error message indicating that the enrollment could not be deleted
        """
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message='Enrollment not found')
        try:
            db.session.delete(enrollment)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not delete the enrollment. {str(e)}")