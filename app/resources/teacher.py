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
        teachers = TeacherModel.query.all()
        if not teachers:
            abort(404, message="Teachers not found")
        return teachers

    @marshal_with(teacher_fields)
    def post(self):
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

class New_Teacher(Resource):
    @marshal_with(teacher_fields)
    def get(self, teacher_id):
        teacher = TeacherModel.query.get(teacher_id)
        if not teacher:
            abort(404, message="Teacher not found")
        return teacher

    @marshal_with(teacher_fields)
    def put(self, teacher_id):
        args = teacher_args.parse_args()
        teacher = TeacherModel.query.get(teacher_id)
        if not teacher:
            abort(404, message="Teacher not found")
        teacher.first_name = args['first_name']
        teacher.last_name = args['last_name']
        teacher.email = args['email']
        teacher.phone = args['phone']
        teacher.department = args['department']
        teacher.credits = args['credits']
        try:
            db.session.commit()
            return teacher, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error updating teacher: {str(e)}")

    def delete(self, teacher_id):
        teacher = TeacherModel.query.get(teacher_id)
        if not teacher:
            abort(404, message="Teacher not found")
        try:
            db.session.delete(teacher)
            db.session.commit()
            return {'message': 'Teacher deleted'}, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error deleting teacher: {str(e)}")
