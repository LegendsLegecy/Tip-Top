#!/usr/bin/env python3
"""
Setup script for Tip Top Flask application
This script helps initialize the database and create the first admin user
"""

import os
import sys

# Import after creating the app context
def import_app():
    from app import app, db, User, Profile
    return app, db, User, Profile

def create_admin_user(app, db, User, Profile):
    """Create the first admin user"""
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin',
            email='admin@tiptop.com',
            password_hash=generate_password_hash('admin123')  # You should change this password
        )
        
        # Create admin profile
        profile = Profile(user_id=admin.id, coins=1000, money=100.00)
        
        db.session.add(admin)
        db.session.add(profile)
        db.session.commit()
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Please change the password after first login!")

def init_database(app, db):
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def main():
    """Main setup function"""
    print("Tip Top Flask Application Setup")
    print("=" * 40)
    
    try:
        # Import app components
        print("Importing application components...")
        app, db, User, Profile = import_app()
        
        # Initialize database
        print("Initializing database...")
        init_database(app, db)
        
        # Create admin user
        print("Creating admin user...")
        create_admin_user(app, db, User, Profile)
        
        print("\nSetup completed successfully!")
        print("You can now run the application with: python app.py")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
