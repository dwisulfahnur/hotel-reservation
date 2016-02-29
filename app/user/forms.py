from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from .models import User
from flask.ext.bcrypt import check_password_hash

class LoginForm(Form):
    username = StringField('Username', validators=[validators.Required('Username tidak boleh kosong')])
    password = PasswordField('Password', validators=[validators.Required('Username tidak boleh kosong')])


class RegisterForm(Form):
    full_name = StringField('Full Name', validators=[validators.Required()])
    username = StringField('Username', validators=[validators.Required()])
    email = StringField('Email', validators=[validators.Required()])
    address = StringField('Address', validators=[validators.Required()])
    phone_number = StringField('Phone Number', validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required(),
                                                     validators.EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        #Check Existing User
        if User.query.filter_by(username=self.username.data).first():
            self.username.errors.append("Username has used")
            return False
        #Check existing email
        if User.query.filter_by(email=self.email.data).first():
            self.email.errors.append("Email cannot be used")
            return False
        return True
