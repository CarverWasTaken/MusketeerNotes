from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from models import User
from database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 10)], render_kw={"placeholder": "First Name"})

    lastname = StringField('Last Name', validators=[Length(1, 20)], render_kw={"placeholder": "Last Name"})

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()], render_kw={"placeholder": "Email"})

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ],
    render_kw={"placeholder": "Password"}
    )

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10),
        
    ], render_kw={"placeholder": "Confirm Password"}   )
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()], render_kw={"placeholder": "Email"})

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")], render_kw={"placeholder": "Password"})

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

class CommentForm(FlaskForm):
    class Meta:
        csrf = False

    comment = TextAreaField('Comment',validators=[Length(min=1)],render_kw={"placeholder": "Enter a comment..."})

    submit = SubmitField('Add Comment')        