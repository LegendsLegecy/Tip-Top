# Tip Top - Flask Application

This is the Flask version of the Tip Top coin-earning platform, converted from the original Django application.

## Features

- **User Authentication**: Sign up, login, logout with email/password
- **Coin System**: Users earn coins and can redeem them for money
- **Dashboard**: View coins, money, and profile information
- **Ad System**: Display ads to users
- **Admin Interface**: Manage ads and users (admin only)
- **Password Reset**: Email-based password reset functionality

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── admin_routes.py       # Admin blueprint routes
├── requirements_flask.txt # Flask dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── forgot-password.html
│   ├── reset-password.html
│   ├── admin/
│   │   ├── ads.html
│   │   └── add_ad.html
│   ├── coins/
│   │   └── coin_price_graph.html
│   └── ads/
│       └── ads_list.html
├── static/               # Static files (CSS, JS, images)
│   ├── style.css
│   ├── signup.css
│   └── ads_images/      # Ad images storage
└── tiptop.db            # SQLite database (created on first run)
```

## Installation

1. **Clone the repository** (if not already done)
   ```bash
   git clone <repository-url>
   cd Tip-Top-master-Flask
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_flask.txt
   ```

4. **Configure the application**
   - Edit `config.py` to set your email credentials
   - Update `SECRET_KEY` for production use

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The application will create the database automatically on first run

## Configuration

### Email Settings
Update the email configuration in `config.py`:
```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'  # Use app password for Gmail
```

### Database
The application uses SQLite by default. To use a different database:
1. Update `SQLALCHEMY_DATABASE_URI` in `config.py`
2. Install the appropriate database driver (e.g., `pip install psycopg2-binary` for PostgreSQL)

## Usage

### Regular Users
1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Access your dashboard
3. **Earn Coins**: Use the earn coins functionality
4. **Redeem Coins**: Convert coins to money (100 coins = $1)

### Admin Users
1. **Admin Access**: Login with username 'admin'
2. **Manage Ads**: Add, edit, activate/deactivate, and delete advertisements
3. **User Management**: View user profiles and manage user data

## Key Differences from Django Version

### Template Changes
- Replaced `{% url 'name' %}` with `{{ url_for('name') }}`
- Replaced `{% static 'file' %}` with `{{ url_for('static', filename='file') }}`
- Replaced `{% csrf_token %}` (not needed in Flask by default)
- Updated Django template filters to Jinja2 equivalents

### Authentication
- Uses Flask-Login instead of Django's built-in auth
- Session management through Flask sessions
- Password hashing with Werkzeug

### Database
- SQLAlchemy ORM instead of Django ORM
- Database models defined in `app.py`
- Automatic database creation on first run

### URL Routing
- Flask routes instead of Django URL patterns
- Blueprint-based organization for admin functionality

## Development

### Adding New Features
1. Add new routes in `app.py` or create new blueprints
2. Create corresponding templates in the `templates/` directory
3. Update the navigation in `base.html` if needed

### Database Migrations
The current setup creates tables automatically. For production:
1. Use Flask-Migrate for database migrations
2. Set up proper migration scripts

### Security Considerations
- Update `SECRET_KEY` for production
- Configure proper email credentials
- Set up HTTPS in production
- Consider adding CSRF protection if needed

## Troubleshooting

### Common Issues

1. **Email not working**
   - Check email credentials in `config.py`
   - Ensure Gmail app password is used (not regular password)
   - Check firewall/antivirus settings

2. **Database errors**
   - Delete `tiptop.db` and restart the application
   - Check file permissions in the project directory

3. **Static files not loading**
   - Ensure the `static/` directory exists
   - Check file paths in templates

4. **Admin access denied**
   - Create a user with username 'admin' first
   - Check the `admin_required` decorator logic

## Production Deployment

1. **Set environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Set up a reverse proxy** (nginx recommended)
4. **Configure SSL/HTTPS**
5. **Set up proper logging**

## License

This project is converted from the original Django application. Please refer to the original project for licensing information.

