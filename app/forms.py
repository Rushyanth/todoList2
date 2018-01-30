from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,EqualTo

# Class for Register Form
class RegisterForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=
		[
			DataRequired(),
			EqualTo('confirm', message='Passwords donot Match')
		])
	confirm = PasswordField('Confirm', validators=[DataRequired()])
	submit = SubmitField('Register')

# Class for loginForm
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField("Login")

# Class for Add Task Form
class AddTaskForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	body = TextAreaField('Description', validators=[DataRequired()])
	submit = SubmitField("Add Task")
