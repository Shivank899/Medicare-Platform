from flask import Blueprint, render_template, flash, redirect, url_for, request
from forms import ContactForm
from extensions import db
from models.models import ContactMessage, Doctor

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/doctors')
def doctors():
    query = request.args.get('q')
    if query:
        # Search by name or specialization
        doctors_list = Doctor.query.filter(
            (Doctor.name.contains(query)) | 
            (Doctor.specialization.contains(query))
        ).all()
    else:
        doctors_list = Doctor.query.all()
    return render_template('doctors.html', title='Find Doctors', doctors=doctors_list)

@main_bp.route('/about')
def about():
    return render_template('about.html', title='About Us')

@main_bp.route('/services')
def services():
    return render_template('services.html', title='Services')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message received! Thank you for contacting us.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', title='Contact', form=form)
