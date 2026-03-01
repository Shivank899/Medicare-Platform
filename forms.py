from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TextAreaField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.models import User, Patient, Doctor

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

    def validate_phone(self, phone):
        # Check both Patient and Doctor tables for phone uniqueness
        patient = Patient.query.filter_by(phone=phone.data).first()
        doctor = Doctor.query.filter_by(phone=phone.data).first()
        if patient or doctor:
            raise ValidationError('That phone number is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):
    doctor = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()]) # HTML5 Time input
    reason = TextAreaField('Reason for Visit', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Book Appointment')

class DoctorAddForm(FlaskForm):
    name = StringField('Dr. Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    specialization = StringField('Specialization', validators=[DataRequired()])
    experience = IntegerField('Experience (Years)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Add Doctor')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

    def validate_phone(self, phone):
        doctor = Doctor.query.filter_by(phone=phone.data).first()
        patient = Patient.query.filter_by(phone=phone.data).first()
        if doctor or patient:
            raise ValidationError('Phone number already in use.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Message')
