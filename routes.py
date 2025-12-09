from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message as MailMessage
from app import app, db
from models.models import User, Admin, Project, Skill, Certificate, Message, Resume, SiteImage, Education, Experience, ContactInfo
from forms.forms import LoginForm, RegistrationForm, ProjectForm, SkillForm, CertificateForm, MessageForm, ResumeForm, SiteImageForm, EducationForm, ExperienceForm, ContactInfoForm
from functools import wraps
from datetime import datetime
import os
import secrets

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Direct admin access route with basic authentication
@app.route("/home/admin/", methods=['GET', 'POST'])
def direct_admin_access():
    # Check if user is already authenticated as admin
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    
    # Check for basic auth credentials
    auth = request.authorization
    if auth:
        # Validate admin credentials
        admin = Admin.query.filter_by(email=auth.username).first()
        if admin and admin.check_password(auth.password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    
    # If no auth provided or invalid, return 401 with WWW-Authenticate header
    headers = {'WWW-Authenticate': 'Basic realm="Admin Access"'}
    return (render_template('login.html', form=LoginForm()), 401, headers)

# Home route
@app.route("/")
@app.route("/home")
def home():
    # Get site images for template
    site_images = {}
    for img in SiteImage.query.all():
        site_images[img.name] = img
    
    return render_template('home.html', site_images=site_images)

# About route
@app.route("/about")
def about():
    # Get site images for template
    site_images = {}
    for img in SiteImage.query.all():
        site_images[img.name] = img
    
    # Get education and experience items
    education_items = Education.query.order_by(Education.order).all()
    experience_items = Experience.query.order_by(Experience.order).all()
    
    return render_template('about.html', 
                         site_images=site_images,
                         education_items=education_items,
                         experience_items=experience_items)

# Projects route
@app.route("/projects")
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

# Skills route
@app.route("/skills")
def skills():
    skills = Skill.query.all()
    return render_template('skills.html', skills=skills)

# Certificates route
@app.route("/certificates")
def certificates():
    certificates = Certificate.query.all()
    return render_template('certificates.html', certificates=certificates)

# Contact route
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    # Get contact information
    contact_info = ContactInfo.query.first()
    if not contact_info:
        # Create default contact info if none exists
        contact_info = ContactInfo(
            email='chidanandkhot2@gmail.com',
            phone='',
            location='City, Country',
            map_embed_url='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3001156.428151844!2d-78.01059036852154!3d42.72837739473232!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4ccc4bf0f123a5a9%3A0xddcfc6c1de189567!2sNew%20York%2C%20USA!5e0!3m2!1sen!2sus!4v1690923407186!5m2!1sen!2sus'
        )
        db.session.add(contact_info)
        db.session.commit()
    
    form = MessageForm()
    if form.validate_on_submit():
        message = Message()
        message.name = form.name.data
        message.email = form.email.data
        message.message = form.message.data
        db.session.add(message)
        db.session.commit()
        
        # Send email notification
        try:
            from app import mail
            msg = MailMessage(
                subject=f'New Contact Message from {form.name.data}',
                recipients=[contact_info.email],
                body=f'''Name: {form.name.data}
Email: {form.email.data}

Message:
{form.message.data}'''
            )
            mail.send(msg)
            flash('Your message has been sent successfully! I will get back to you soon.', 'success')
        except Exception as e:
            print(f"Email error: {e}")
            flash('Your message has been saved! (Email notification failed, but message is recorded)', 'info')
        
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, contact_info=contact_info)

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('home'))
    
    form = LoginForm()
    print(f"Request method: {request.method}")
    print(f"Form data: {form.data}")
    
    # Check if form is submitted
    if request.method == 'POST':
        print("Processing POST request")
        print(f"Form validation: {form.validate()}")
        print(f"Form errors: {form.errors}")
        
        # Even if form validation fails, let's try to process the login
        # This is for debugging purposes only
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Raw form data - Email: {email}, Password: {password}")
        
        if email and password:
            # Check if it's an admin login
            admin = Admin.query.filter_by(email=email).first()
            if admin and admin.check_password(password):
                login_user(admin)
                flash('Login successful!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
            
            # Check if it's a user login
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            
            flash('Login unsuccessful. Please check email and password', 'danger')
        else:
            flash('Please provide both email and password', 'danger')
    
    return render_template('login.html', form=form)

# Registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Logout route
@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# Admin dashboard route
@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    # Get counts for dashboard
    project_count = Project.query.count()
    skill_count = Skill.query.count()
    certificate_count = Certificate.query.count()
    message_count = Message.query.count()
    
    return render_template('admin/dashboard.html', 
                          project_count=project_count,
                          skill_count=skill_count,
                          certificate_count=certificate_count,
                          message_count=message_count)

# Admin projects route
@app.route("/admin/projects")
@login_required
@admin_required
def admin_projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

# Admin add/edit project route
@app.route("/admin/projects/new", methods=['GET', 'POST'])
@app.route("/admin/projects/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_project_form(project_id=None):
    project = None
    if project_id:
        project = Project.query.get_or_404(project_id)
    
    form = ProjectForm()
    if form.validate_on_submit():
        if project is None:
            project = Project()
        
        project.title = form.title.data
        project.description = form.description.data
        project.link = form.link.data
        
        # Handle image upload
        if form.image.data:
            # Create projects directory if it doesn't exist
            projects_dir = os.path.join(app.root_path, 'static', 'images', 'projects')
            if not os.path.exists(projects_dir):
                os.makedirs(projects_dir)
            
            # Generate unique filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.image.data.filename)
            image_filename = random_hex + f_ext
            image_path = os.path.join(projects_dir, image_filename)
            
            # Save the image
            form.image.data.save(image_path)
            project.image = image_filename
        
        if project_id is None:
            db.session.add(project)
        
        db.session.commit()
        flash('Project saved successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    elif request.method == 'GET' and project:
        form.title.data = project.title
        form.description.data = project.description
        form.link.data = project.link
    
    return render_template('admin/project_form.html', form=form, project=project)

# Admin delete project route
@app.route("/admin/projects/<int:project_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

# Admin skills route
@app.route("/admin/skills")
@login_required
@admin_required
def admin_skills():
    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)

# Admin add/edit skill route
@app.route("/admin/skills/new", methods=['GET', 'POST'])
@app.route("/admin/skills/<int:skill_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_skill_form(skill_id=None):
    skill = None
    if skill_id:
        skill = Skill.query.get_or_404(skill_id)
    
    form = SkillForm()
    if form.validate_on_submit():
        if skill is None:
            skill = Skill()
        
        skill.name = form.name.data
        
        # Handle image upload
        if form.image.data:
            # Create skills directory if it doesn't exist
            skills_dir = os.path.join(app.root_path, 'static', 'images', 'skills')
            if not os.path.exists(skills_dir):
                os.makedirs(skills_dir)
            
            # Generate unique filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.image.data.filename)
            image_filename = random_hex + f_ext
            image_path = os.path.join(skills_dir, image_filename)
            
            # Save the image
            form.image.data.save(image_path)
            skill.image = image_filename
        
        if skill_id is None:
            db.session.add(skill)
        
        db.session.commit()
        flash('Skill saved successfully!', 'success')
        return redirect(url_for('admin_skills'))
    
    elif request.method == 'GET' and skill:
        form.name.data = skill.name
    
    return render_template('admin/skill_form.html', form=form, skill=skill)

# Admin delete skill route
@app.route("/admin/skills/<int:skill_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin_skills'))

# Admin certificates route
@app.route("/admin/certificates")
@login_required
@admin_required
def admin_certificates():
    certificates = Certificate.query.all()
    return render_template('admin/certificates.html', certificates=certificates)

# Admin add/edit certificate route
@app.route("/admin/certificates/new", methods=['GET', 'POST'])
@app.route("/admin/certificates/<int:certificate_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_certificate_form(certificate_id=None):
    certificate = None
    if certificate_id:
        certificate = Certificate.query.get_or_404(certificate_id)
    
    form = CertificateForm()
    if form.validate_on_submit():
        if certificate is None:
            certificate = Certificate()
        
        certificate.title = form.title.data
        
        # Handle image upload
        if form.image.data:
            # Create certificates directory if it doesn't exist
            cert_dir = os.path.join(app.root_path, 'static', 'images', 'certificates')
            if not os.path.exists(cert_dir):
                os.makedirs(cert_dir)
            
            # Generate unique filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.image.data.filename)
            image_filename = random_hex + f_ext
            image_path = os.path.join(cert_dir, image_filename)
            
            # Save the image
            form.image.data.save(image_path)
            certificate.image = image_filename
        
        if certificate_id is None:
            db.session.add(certificate)
        
        db.session.commit()
        flash('Certificate saved successfully!', 'success')
        return redirect(url_for('admin_certificates'))
    
    elif request.method == 'GET' and certificate:
        form.title.data = certificate.title
    
    return render_template('admin/certificate_form.html', form=form, certificate=certificate)

# Admin delete certificate route
@app.route("/admin/certificates/<int:certificate_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_certificate(certificate_id):
    certificate = Certificate.query.get_or_404(certificate_id)
    db.session.delete(certificate)
    db.session.commit()
    flash('Certificate deleted successfully!', 'success')
    return redirect(url_for('admin_certificates'))

# Admin messages route
@app.route("/admin/messages")
@login_required
@admin_required
def admin_messages():
    messages = Message.query.order_by(Message.date.desc()).all()
    return render_template('admin/messages.html', messages=messages)

# Admin resume upload route
@app.route("/admin/resume", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_resume():
    form = ResumeForm()
    if form.validate_on_submit():
        # Check if a file was uploaded
        if form.resume.data:
            # Get the uploaded file
            file = form.resume.data
            
            # Create the files directory if it doesn't exist
            files_dir = os.path.join(app.root_path, 'static', 'files')
            if not os.path.exists(files_dir):
                os.makedirs(files_dir)
            
            # Generate a random filename to avoid conflicts
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            resume_filename = random_hex + f_ext
            
            # Define the path to save the file
            resume_path = os.path.join(files_dir, resume_filename)
            
            # Save the file
            file.save(resume_path)
            
            # Delete any existing resume records (keep only the latest)
            Resume.query.delete()
            
            # Create new resume record
            resume = Resume(filename=resume_filename)
            db.session.add(resume)
            db.session.commit()
            
            flash('Resume uploaded successfully!', 'success')
            return redirect(url_for('admin_resume'))
    
    # Get the current resume for display
    current_resume = Resume.query.first()
    
    return render_template('admin/resume.html', form=form, current_resume=current_resume)

# Download resume route
@app.route("/download-resume")
def download_resume():
    from flask import send_file
    resume = Resume.query.first()
    if resume:
        file_path = os.path.join(app.root_path, 'static', 'files', resume.filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name='Chidanand_Khot_Resume.pdf')
    flash('Resume not found!', 'danger')
    return redirect(url_for('home'))

# Admin image management route
@app.route("/admin/images", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_images():
    # Define available image positions
    image_types = {
        'profile': 'Profile Image (About Page)',
        'home_hero': 'Home Page Hero Background',
        'about_banner': 'About Page Banner'
    }
    
    # Get current images
    current_images = {}
    for img_type in image_types.keys():
        site_img = SiteImage.query.filter_by(name=img_type).first()
        if site_img:
            current_images[img_type] = site_img
    
    return render_template('admin/images.html', image_types=image_types, current_images=current_images)

# Admin upload image route
@app.route("/admin/images/upload/<image_type>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_upload_image(image_type):
    image_types = {
        'profile': 'Profile Image (About Page)',
        'home_hero': 'Home Page Hero Background',
        'about_banner': 'About Page Banner'
    }
    
    if image_type not in image_types:
        flash('Invalid image type!', 'danger')
        return redirect(url_for('admin_images'))
    
    form = SiteImageForm()
    if form.validate_on_submit():
        if form.image.data:
            # Create images directory if it doesn't exist
            images_dir = os.path.join(app.root_path, 'static', 'images')
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # Generate unique filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.image.data.filename)
            image_filename = random_hex + f_ext
            image_path = os.path.join(images_dir, image_filename)
            
            # Save the image
            form.image.data.save(image_path)
            
            # Update or create database record
            site_image = SiteImage.query.filter_by(name=image_type).first()
            if site_image:
                # Delete old image file
                old_path = os.path.join(images_dir, site_image.filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
                site_image.filename = image_filename
                site_image.upload_date = datetime.utcnow()
            else:
                site_image = SiteImage(name=image_type, filename=image_filename)
                db.session.add(site_image)
            
            db.session.commit()
            flash(f'{image_types[image_type]} uploaded successfully!', 'success')
            return redirect(url_for('admin_images'))
    
    current_image = SiteImage.query.filter_by(name=image_type).first()
    return render_template('admin/image_upload.html', form=form, image_type=image_type, 
                         image_name=image_types[image_type], current_image=current_image)

# Admin delete site image route
@app.route("/admin/images/<image_type>/delete", methods=['POST'])
@login_required
@admin_required
def delete_site_image(image_type):
    image_types = {
        'profile': 'Profile Image (About Page)',
        'home_hero': 'Home Page Hero Background',
        'about_banner': 'About Page Banner'
    }
    
    if image_type not in image_types:
        flash('Invalid image type!', 'danger')
        return redirect(url_for('admin_images'))
    
    site_image = SiteImage.query.filter_by(name=image_type).first()
    if site_image:
        # Delete the image file
        image_path = os.path.join(app.root_path, 'static', 'images', site_image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete the database record
        db.session.delete(site_image)
        db.session.commit()
        flash(f'{image_types[image_type]} deleted successfully!', 'success')
    else:
        flash('Image not found!', 'danger')
    
    return redirect(url_for('admin_images'))

# Admin education routes
@app.route("/admin/education")
@login_required
@admin_required
def admin_education():
    education_items = Education.query.order_by(Education.order).all()
    return render_template('admin/education.html', education_items=education_items)

@app.route("/admin/education/new", methods=['GET', 'POST'])
@app.route("/admin/education/<int:education_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_education_form(education_id=None):
    education = None
    if education_id:
        education = Education.query.get_or_404(education_id)
    
    form = EducationForm()
    if form.validate_on_submit():
        if education is None:
            education = Education()
        
        education.degree = form.degree.data
        education.institution = form.institution.data
        education.start_date = form.start_date.data
        education.end_date = form.end_date.data
        education.description = form.description.data
        education.order = form.order.data
        
        # Handle image upload
        if form.image.data:
            # Create education directory if it doesn't exist
            edu_dir = os.path.join(app.root_path, 'static', 'images', 'education')
            if not os.path.exists(edu_dir):
                os.makedirs(edu_dir)
            
            # Generate unique filename
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.image.data.filename)
            image_filename = random_hex + f_ext
            image_path = os.path.join(edu_dir, image_filename)
            
            # Save the image
            form.image.data.save(image_path)
            education.image = image_filename
        
        if education_id is None:
            db.session.add(education)
        
        db.session.commit()
        flash('Education item saved successfully!', 'success')
        return redirect(url_for('admin_education'))
    
    elif request.method == 'GET' and education:
        form.degree.data = education.degree
        form.institution.data = education.institution
        form.start_date.data = education.start_date
        form.end_date.data = education.end_date
        form.description.data = education.description
        form.order.data = education.order
    
    return render_template('admin/education_form.html', form=form, education=education)

@app.route("/admin/education/<int:education_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_education(education_id):
    education = Education.query.get_or_404(education_id)
    db.session.delete(education)
    db.session.commit()
    flash('Education item deleted successfully!', 'success')
    return redirect(url_for('admin_education'))

# Admin experience routes
@app.route("/admin/experience")
@login_required
@admin_required
def admin_experience():
    experience_items = Experience.query.order_by(Experience.order).all()
    return render_template('admin/experience.html', experience_items=experience_items)

@app.route("/admin/experience/new", methods=['GET', 'POST'])
@app.route("/admin/experience/<int:experience_id>/update", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_experience_form(experience_id=None):
    experience = None
    if experience_id:
        experience = Experience.query.get_or_404(experience_id)
    
    form = ExperienceForm()
    if form.validate_on_submit():
        if experience is None:
            experience = Experience()
        
        experience.position = form.position.data
        experience.company = form.company.data
        experience.start_date = form.start_date.data
        experience.end_date = form.end_date.data
        experience.description = form.description.data
        experience.order = form.order.data
        
        if experience_id is None:
            db.session.add(experience)
        
        db.session.commit()
        flash('Experience item saved successfully!', 'success')
        return redirect(url_for('admin_experience'))
    
    elif request.method == 'GET' and experience:
        form.position.data = experience.position
        form.company.data = experience.company
        form.start_date.data = experience.start_date
        form.end_date.data = experience.end_date
        form.description.data = experience.description
        form.order.data = experience.order
    
    return render_template('admin/experience_form.html', form=form, experience=experience)

@app.route("/admin/experience/<int:experience_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_experience(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience item deleted successfully!', 'success')
    return redirect(url_for('admin_experience'))

# Admin contact info routes
@app.route("/admin/contact", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_contact_info():
    # Get the first (and only) contact info record
    contact_info = ContactInfo.query.first()
    
    # If no contact info exists, create a default one
    if not contact_info:
        contact_info = ContactInfo(
            email='chidanandkhot2@gmail.com',
            phone='',
            location='City, Country',
            map_embed_url='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3001156.428151844!2d-78.01059036852154!3d42.72837739473232!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4ccc4bf0f123a5a9%3A0xddcfc6c1de189567!2sNew%20York%2C%20USA!5e0!3m2!1sen!2sus!4v1690923407186!5m2!1sen!2sus'
        )
        db.session.add(contact_info)
        db.session.commit()
    
    form = ContactInfoForm()
    if form.validate_on_submit():
        contact_info.email = form.email.data
        contact_info.phone = form.phone.data
        contact_info.location = form.location.data
        contact_info.map_embed_url = form.map_embed_url.data
        
        db.session.commit()
        flash('Contact information updated successfully!', 'success')
        return redirect(url_for('admin_contact_info'))
    
    elif request.method == 'GET':
        form.email.data = contact_info.email
        form.phone.data = contact_info.phone
        form.location.data = contact_info.location
        form.map_embed_url.data = contact_info.map_embed_url
    
    return render_template('admin/contact_info.html', form=form)
