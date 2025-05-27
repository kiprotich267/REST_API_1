from flask import Flask 
from flask_restful import Api
from flask_migrate import Migrate
from flasgger import Swagger
from app.resources.user import Users, user
from app.resources.teacher import Teachers, Teacher
from app.resources.student import Students, Student
from app.resources.course import Courses, Course
from app.resources.enrollment import Enrollments, Enrollment
from app.resources.fee import Fees, Fee
from app.extension import db
from config import Config

#swagger configuration
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  
            "model_filter": lambda tag: True,  
        }
    ],
    "static_url_path": "/flasgger_static",
 
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

# API information template
template = {
    "info": {
        "title": "School Management System API",
        "version": "1.0.0",
        "description": "API for managing school operations including users, teachers, students, courses, enrollments, and fees.",
    "contact": {
        "name": "Support Team",
        "email": "admin@enock.com"
    }
},
"host": "localhost:5000",
"basePath": "/api",
"schemes": ["http", "https"],
"tags": [
        {
            "name": "Users",
            "description": "Operations related to users"
        },
        {
            "name": "Teachers",
            "description": "Operations related to teachers"
        },
        {
            "name": "Students",
            "description": "Operations related to students"
        },
        {
            "name": "Courses",
            "description": "Operations related to courses"
        },
        {
            "name": "Enrollments",
            "description": "Operations related to enrollments"
        },
        {
            "name": "Fees",
            "description": "Operations related to fees"
        }
    ]
}

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
swagger = Swagger(app, config=swagger_config, template=template)





# Api endpoints
api.add_resource(Users, '/api/users')
api.add_resource(user, '/api/users/<int:id>')

api.add_resource(Teachers, '/api/teachers')
api.add_resource(Teacher, '/api/teachers/<int:id>')

api.add_resource(Students, '/api/students')
api.add_resource(Student, '/api/students/<int:id>')

api.add_resource(Courses, '/api/courses')
api.add_resource(Course, '/api/courses/<int:id>')

api.add_resource(Enrollments, '/api/enrollments')
api.add_resource(Enrollment, '/api/enrollments/<int:id>')

api.add_resource(Fees, '/api/fees')
api.add_resource(Fee, '/api/fees/<int:id>')




