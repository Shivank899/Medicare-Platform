from datetime import datetime
from extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'patient', 'doctor', 'admin'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    patient_profile = db.relationship('Patient', backref='user', uselist=False)
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.role}')"

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200))
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        return f"Patient('{self.name}', '{self.phone}')"

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False) # Years
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f"Doctor('{self.name}', '{self.specialization}')"

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Approved, Completed, Cancelled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Appointment('{self.date}', '{self.time}', '{self.status}')"

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactMessage('{self.name}', '{self.email}')"
