import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, views
from app.core.db import db
from app.core.json import json_respon
from models import User, UserRoles
from forms import RegisterForm, LoginForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.bcrypt import check_password_hash
from sqlalchemy.exc import IntegrityError

user_views = Blueprint('user', __name__, template_folder='../templates/user', static_folder='../static')

#REGISTER CLASS
class Register(views.MethodView):
    def post(self):
        fullname = request.values.get("fullname")
        username = request.values.get("username")
        email = request.values.get("email")
        address = request.values.get("address")
        phone_number = request.values.get("phone_number")
        password = request.values.get("password")

        #validate form
        errors = []
        if fullname is None or not fullname:
            errors.append(dict(field="fullname",
                               message="Input Empty"))
        if username is None or not username:
            errors.append(dict(field="username",
                               message="Input Empty"))
        if '@' not in unicode(email) and email is not None:
            errors.append(dict(field="email",
                                message="Email not valid"))
        if email is None or not email:
            errors.append(dict(field="email",
                               message="Input Empty"))
        if address is None or not address:
            errors.append(dict(field="address",
                               message="Input Empty"))
        if phone_number is None or not phone_number:
            errors.append(dict(field="phone_number",
                           message="Input Empty"))
        if password is None or not password:
            errors.append(dict(field="password",
                               message="Input Empty"))
        if len(errors) > 0:
            return json_respon(code=400,
                               msg="Input Empty",
                               errors=errors)
        #Check Existing User
        if  User.query.filter_by(username=username).first():
            return json_respon(code=400,
                               msg="Username can't be used")
        if User.query.filter_by(email=email).first():
            return json_respon(code=400,
                               msg="Email has registered")
        user = User(fullname = fullname,
                    username = username,
                    email = email,
                    address = address,
                    phone_number = phone_number,
                    password = unicode(password))
        try:
            #Register User
            db.session.add(user)
            db.session.commit()
            # Assign User Role as User
            db.session.add(UserRoles(2,user.id))
            db.session.commit()
        except IntegrityError as e:
            return json_respon(code=400,
                               msg=e.message)
        #Create User Session
        login_user(user)
        return json_respon(msg="User registered successfully")
user_views.add_url_rule('/register', view_func=Register.as_view('register'))

#USER LOGIN CLASS
class Login(views.MethodView):
    def post(self):
        username = request.values.get("username", None)
        password = request.values.get("password", None)

        #VALIDATE FORM LOGIN
        errors = []
        if username is None or not username:
            errors.append(dict(field="username",
                          message="Input Empty"))
        if password is None or not password:
            errors.append(dict(field="password",
                           message="Input Empty"))
        if errors:
            return json_respon(code=400,
                               msg="Input Empty",
                               errors=errors)
        #Check Existing User
        user = User.query.filter_by(username=username).first()
        if not user:
            return json_respon(code=400,
                               msg="Unknown Username")
        #Check Hashed Password
        if not check_password_hash(user.password, password):
            return json_respon(code=400,
                               msg = "Password Wrong.")
        #Create Session User
        login_user(user)
        return json_respon(msg="You're logged in")
user_views.add_url_rule('/login', view_func=Login.as_view('login'))

#ADMIN LOGIN
class AdminLogin(views.MethodView):
    def post(self):
        username = request.values.get("username", None)
        password = request.values.get("password", None)

        #VALIDATE FORM
        errors = []
        if username is None or not username:
            errors.append(dict(field="username",
                          message="Input Empty"))
        if password is None or not password:
            errors.append(dict(field="password",
                           message="Input Empty"))
        if errors:
            return json_respon(code=400,
                               msg="Input Empty",
                               errors=errors)
        #CHECK EXISTING USER
        user = User.query.filter_by(username=username).first()

        if not user:
            return json_respon(code=400,
                               msg="Unknown Username")

        #CHECK USER ROLE
        user_role = UserRoles.query.filter_by(user_id=user.id).first()
        if user_role.role_id is not 1:
            return json_respon(code = 401,
                                   msg = "You account is not Admin")

        #CHECK HASHED PASSWORD
        if not check_password_hash(user.password, password):
            return json_respon(code = 400,
                               msg = "Password Wrong.")

        #CREATE USER SESSION
        login_user(user)
        return json_respon(msg = "You're login successfull as admin")
user_views.add_url_rule('/admin', view_func=AdminLogin.as_view('admin'))

@user_views.route('/logout/')
@login_required
def logout():
    #commit time logout to database User
    user = User.query.get(current_user.id)
    user.last_login = datetime.datetime.now()
    db.session.commit()
    flash('You\'re logged out')
    #Remove User session
    logout_user()
    return json_respon(msg="you're logged out")
