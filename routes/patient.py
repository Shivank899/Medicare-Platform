from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from extensions import db
from models.models import Appointment, Doctor, Patient
from forms import AppointmentForm
from datetime import datetime

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patient/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        abort(403)
    
    # Get Patient Profile
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if not patient:
        flash('Patient profile not found!', 'danger')
        return redirect(url_for('main.index'))

    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    upcoming = [a for a in appointments if a.status != 'Completed' and a.status != 'Cancelled']
    
    return render_template('dashboard_patient.html', title='Patient Dashboard', appointments=appointments, upcoming=upcoming, patient=patient)

@patient_bp.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if current_user.role != 'patient':
        abort(403)

    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    form = AppointmentForm()
    # Populate doctors
    doctors = Doctor.query.all()
    form.doctor.choices = [(d.id, f"Dr. {d.name} ({d.specialization})") for d in doctors]

    if form.validate_on_submit():
        selected_doctor = Doctor.query.get_or_404(form.doctor.data)
        
        # Check if patient is trying to book with themselves (if they are also a doctor)
        if patient.user_id == selected_doctor.user_id:
            flash('Security Alert: You cannot book an appointment with yourself.', 'danger')
            return redirect(url_for('patient.book_appointment'))

        # Check for double booking (same time, same doctor)
        # Prompt says "Double appointment booking".
        existing = Appointment.query.filter_by(
            doctor_id=form.doctor.data, 
            date=form.date.data, 
            time=form.time.data,
            status='Pending' # Or Approved
        ).first()
        
        if existing:
            flash('This slot is already booked or pending. Please choose another.', 'danger')
        else:
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=form.doctor.data,
                date=form.date.data,
                time=form.time.data,
                reason=form.reason.data
            )
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment request sent successfully!', 'success')
            return redirect(url_for('patient.dashboard'))
            
    return render_template('book_appointment.html', title='Book Appointment', form=form)
