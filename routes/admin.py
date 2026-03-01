from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from extensions import db, bcrypt
from models.models import User, Patient, Doctor, Appointment, ContactMessage
from forms import DoctorAddForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        abort(403)
        
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    upcoming_appointments = Appointment.query.filter(Appointment.status.in_(['Pending', 'Approved'])).count()
    
    recent_doctors = Doctor.query.order_by(Doctor.id.desc()).limit(5).all()
    
    return render_template('dashboard_admin.html', title='Admin Dashboard',
                           total_patients=total_patients,
                           total_doctors=total_doctors,
                           total_appointments=total_appointments,
                           upcoming_appointments=upcoming_appointments,
                           recent_doctors=recent_doctors)

@admin_bp.route('/admin/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        abort(403)
        
    form = DoctorAddForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, role='doctor')
        db.session.add(user)
        db.session.commit()
        
        doctor = Doctor(
            user_id=user.id,
            name=form.name.data,
            phone=form.phone.data,
            specialization=form.specialization.data,
            experience=form.experience.data
        )
        db.session.add(doctor)
        db.session.commit()
        
        flash('New doctor added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('add_doctor.html', title='Add Doctor', form=form)

@admin_bp.route('/admin/view_database')
@login_required
def view_database():
    if current_user.role != 'admin':
        abort(403)
        
    all_users = User.query.all()
    all_doctors = Doctor.query.all()
    all_patients = Patient.query.all()
    all_appointments = Appointment.query.all()
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    return render_template('view_database.html', title='Master Database',
                           users=all_users, doctors=all_doctors, 
                           patients=all_patients, appointments=all_appointments,
                           messages=all_messages)
