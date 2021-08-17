from app import app, db
from app.models import User, Employer, Employee, Post, Notification, Message

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Employer': Employer, 'Employee': Employee, 'Notification': Notification, 'Message': Message}
    

