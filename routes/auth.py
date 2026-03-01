from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from models.models import User, Patient, Doctor
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create User
        user = User(email=form.email.data, password=hashed_password, role='patient')
        db.session.add(user)
        db.session.commit()
        
        # Create Patient Profile
        patient = Patient(
            user_id=user.id,
            name=form.name.data,
            phone=form.phone.data,
            gender=form.gender.data,
            dob=form.dob.data,
            address=form.address.data
        )
        db.session.add(patient)
        db.session.commit()
        
        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        return redirect(url_for('patient.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user.role == 'doctor':
                    return redirect(url_for('doctor.dashboard'))
                else:
                    return redirect(url_for('patient.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
