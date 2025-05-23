from flask import Flask 
from flask_restful import Api
from app.resources.user import Users, user
from app.resources.teacher import Teachers, Teacher
from app.resources.student import Students, Student
from app.extension import db
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)





# Api endpoints
api.add_resource(Users, '/api/users')
api.add_resource(user, '/api/users/<int:id>')

api.add_resource(Teachers, '/api/teachers')
api.add_resource(Teacher, '/api/teachers/<int:id>')

api.add_resource(Students, '/api/students')
api.add_resource(Student, '/api/students/<int:id>')
