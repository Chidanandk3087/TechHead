# Chidanand Khot - Portfolio & Admin Panel

A professional portfolio website with an integrated admin panel built using Flask, SQLite, and modern web technologies.

## Features

### Frontend Pages
- Home Page with animated introduction
- About Page with timeline
- Projects Page (dynamically loaded from database)
- Skills Page (dynamically loaded from database)
- Certificates Page (dynamically loaded from database)
- Contact Page with Google Map integration

### Authentication System
- Admin login (email: chidanandkhot03@gmail.com, password: ChidanandK@3087)
- User registration and login
- Password hashing with Werkzeug Security

### Admin Panel
- Dashboard with site statistics
- Manage Projects (Add, Edit, Delete)
- Manage Skills (Add, Edit, Delete)
- Manage Certificates (Add, Edit, Delete)
- View Contact Messages
- Resume Upload

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python Flask
- **Database**: SQLite
- **Authentication**: Flask-Login, Werkzeug Security
- **Forms**: Flask-WTF, WTForms
- **Mail**: Flask-Mail (for contact form)

## Installation

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```
   python test_db.py
   ```
4. Run the application:
   ```
   python app.py
   ```
   or
   ```
   run.bat
   ```

## Access

- **Website**: http://127.0.0.1:5000
- **Admin Panel**: http://127.0.0.1:5000/admin/dashboard
- **Admin Login**: 
  - Email: chidanandkhot03@gmail.com
  - Password: ChidanandK@3087

## Database Structure

- `users`: User accounts (name, email, password)
- `admin`: Admin accounts (email, password)
- `projects`: Portfolio projects (title, description, image, link)
- `skills`: Technical skills (name, icon)
- `certificates`: Certificates (title, image)
- `messages`: Contact form messages (name, email, message, date)

## Customization

- Update the resume file in `static/files/`
- Add project images to `static/images/projects/`
- Add certificate images to `static/images/certificates/`
- Modify templates in `templates/` directory
- Update styles in `static/css/style.css`
- Add JavaScript functionality in `static/js/script.js`