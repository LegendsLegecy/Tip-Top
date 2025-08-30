from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db, Ad, User, Profile
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to check if user is admin"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    ads = Ad.query.all()
    return render_template('admin/dashboard.html', users=users, ads=ads)

@admin_bp.route('/ads/')
@login_required
@admin_required
def manage_ads():
    ads = Ad.query.order_by(Ad.created_at.desc()).all()
    return render_template('admin/ads.html', ads=ads)

@admin_bp.route('/ads/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_ad():
    if request.method == 'POST':
        title = request.form.get('title')
        link = request.form.get('link')
        image = request.files.get('image')
        
        if not all([title, link, image]):
            flash('All fields are required.', 'error')
            return redirect(url_for('admin.add_ad'))
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Ensure upload directory exists
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save image
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            
            # Create ad record
            ad = Ad(
                title=title,
                image=filename,
                link=link,
                is_active=True
            )
            
            db.session.add(ad)
            db.session.commit()
            
            flash('Ad created successfully!', 'success')
            return redirect(url_for('admin.manage_ads'))
        else:
            flash('Invalid file type. Allowed: png, jpg, jpeg, gif', 'error')
    
    return render_template('admin/add_ad.html')

@admin_bp.route('/ads/<int:ad_id>/toggle/')
@login_required
@admin_required
def toggle_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    ad.is_active = not ad.is_active
    db.session.commit()
    
    status = 'activated' if ad.is_active else 'deactivated'
    flash(f'Ad "{ad.title}" {status}.', 'success')
    return redirect(url_for('admin.manage_ads'))

@admin_bp.route('/ads/<int:ad_id>/delete/')
@login_required
@admin_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    
    # Delete image file
    if ad.image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], ad.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(ad)
    db.session.commit()
    
    flash(f'Ad "{ad.title}" deleted.', 'success')
    return redirect(url_for('admin.manage_ads'))

@admin_bp.route('/users/')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/profile/')
@login_required
@admin_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_profile.html', user=user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

