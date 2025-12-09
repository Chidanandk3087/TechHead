from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    link = StringField('Link', validators=[Length(max=200)])
    image = FileField('Project Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Project')

class SkillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    image = FileField('Skill Logo/Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Skill')

class CertificateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    image = FileField('Certificate Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Certificate')

class MessageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class ResumeForm(FlaskForm):
    resume = FileField('Resume (PDF)', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    submit = SubmitField('Upload Resume')

class SiteImageForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Upload Image')

class EducationForm(FlaskForm):
    degree = StringField('Degree', validators=[DataRequired(), Length(max=200)])
    institution = StringField('Institution', validators=[DataRequired(), Length(max=200)])
    start_date = StringField('Start Date', validators=[DataRequired(), Length(max=20)])
    end_date = StringField('End Date', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description')
    order = IntegerField('Order', validators=[NumberRange(min=0)], default=0)
    image = FileField('Institution Logo/Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Education')

class ExperienceForm(FlaskForm):
    position = StringField('Position', validators=[DataRequired(), Length(max=200)])
    company = StringField('Company', validators=[DataRequired(), Length(max=200)])
    start_date = StringField('Start Date', validators=[DataRequired(), Length(max=20)])
    end_date = StringField('End Date', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description')
    order = IntegerField('Order', validators=[NumberRange(min=0)], default=0)
    submit = SubmitField('Save Experience')

class ContactInfoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number')
    location = StringField('Location')
    map_embed_url = TextAreaField('Map Embed URL')
    submit = SubmitField('Save Contact Info')
