import os
import sys

# Ensure the app directory is in the python path for Render
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from config.config import Config
from extensions import db, bcrypt, login_manager
from routes.auth import auth_bp
from routes.main import main_bp
from routes.patient import patient_bp
from routes.doctor import doctor_bp
from routes.admin import admin_bp
from models.models import User, Patient, Doctor, Appointment

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(admin_bp)

    # Error Handlers
    @app.errorhandler(404)
    def error_404(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def error_403(error):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def error_500(error):
        return render_template('500.html'), 500

    return app

app = create_app()

@app.cli.command("seed-db")
def seed_db():
    """Seed the database with admin and sample data."""
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        if not User.query.filter_by(email='admin@medicare.com').first():
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_user = User(email='admin@medicare.com', password=hashed_pw, role='admin')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin created: admin@medicare.com / admin123")
        
        # Sample Doctors
        doctors_data = [
            ('Sarah Johnson', 'sarah@medicare.com', 'Cardiology', 12, '9876543210', 'https://images.unsplash.com/photo-1559839734-2b71f1536783?auto=format&fit=crop&q=80&w=400'),
            ('Mark Miller', 'mark@medicare.com', 'Neurology', 8, '9876543211', 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=400'),
            ('Emily Davis', 'emily@medicare.com', 'Pediatrics', 15, '9876543212', 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&q=80&w=400')
        ]
        
        for name, email, spec, exp, phone, img in doctors_data:
            if not User.query.filter_by(email=email).first():
                pw = bcrypt.generate_password_hash('doctor123').decode('utf-8')
                u = User(email=email, password=pw, role='doctor')
                db.session.add(u)
                db.session.commit()
                d = Doctor(user_id=u.id, name=name, specialization=spec, experience=exp, phone=phone, image_file=img)
                db.session.add(d)
                db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure tables exist
    app.run(debug=True)
