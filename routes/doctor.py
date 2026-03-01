from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from extensions import db
from models.models import Appointment, Doctor
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctor/dashboard')
@login_required
def dashboard():
    if current_user.role != 'doctor':
        abort(403)
        
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        flash('Doctor profile not found!', 'danger')
        return redirect(url_for('main.index'))

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    pending = [a for a in appointments if a.status == 'Pending']
    upcoming = [a for a in appointments if a.status == 'Approved']
    
    return render_template('dashboard_doctor.html', title='Doctor Dashboard', appointments=appointments, pending=pending, upcoming=upcoming, doctor=doctor)

@doctor_bp.route('/appointment/<int:appointment_id>/update/<string:status>')
@login_required
def update_appointment(appointment_id, status):
    if current_user.role != 'doctor':
        abort(403)
        
    appointment = Appointment.query.get_or_404(appointment_id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if appointment.doctor_id != doctor.id:
        abort(403)
        
    if status in ['Approved', 'Cancelled', 'Completed']:
        appointment.status = status
        db.session.commit()
        flash(f'Appointment status updated to {status}', 'success')
    else:
        flash('Invalid status update', 'danger')
        
    return redirect(url_for('doctor.dashboard'))
