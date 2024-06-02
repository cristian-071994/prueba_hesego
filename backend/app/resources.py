from flask_restful import Resource, reqparse
from app import db
from app.models import Task, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    print(f"Hashed password for {username}: {hashed_password}")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"User {username} not found")
        return False

    print(f"User found: {user.username} with hashed password: {user.password}")
    print(f"Entered password: {password}")

    password_verification = check_password_hash(user.password, password)
    print(f"Password verification result: {password_verification}")

    if not password_verification:
        print(f"Password for user {username} is incorrect")
        return False

    print(f"User {username} logged in successfully")
    return True

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        tasks = Task.query.all()
        return [task.to_dict() for task in tasks], 200

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description')
        parser.add_argument('completed', type=bool, default=False)
        data = parser.parse_args()

        new_task = Task(
            title=data['title'],
            description=data['description'],
            completed=data['completed']
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task.to_dict(), 201

class TaskResource(Resource):
    @jwt_required()
    def get(self, id):
        task = Task.query.get_or_404(id)
        return task.to_dict(), 200

    @jwt_required()
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('completed', type=bool)
        data = parser.parse_args()

        task = Task.query.get_or_404(id)
        if data['title']:
            task.title = data['title']
        if data['description']:
            task.description = data['description']
        if data['completed'] is not None:
            task.completed = data['completed']
        
        db.session.commit()
        return task.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400

        register_user(data['username'], data['password'])

        access_token = create_access_token(identity={'username': data['username']})
        return {'access_token': access_token}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()

        if login_user(data['username'], data['password']):
            access_token = create_access_token(identity={'username': data['username']})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
