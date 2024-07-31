from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.mysql import db

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    employee_email = db.Column(db.String(255), unique=True)
    employee_name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    ponds = db.relationship("Pond", secondary="employee_ponds", backref=db.backref("employees", lazy=True))

    def __init__(self, user_id, employee_name, password):
        self.user_id = user_id
        self.employee_name = employee_name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "user_id": self.user_id,
            "employee_email": self.employee_email,
            "employee_name": self.employee_name,
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        }

employee_ponds = db.Table('employee_ponds',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True),
    db.Column('pond_id', db.Integer, db.ForeignKey('ponds.pond_id'), primary_key=True)
)
