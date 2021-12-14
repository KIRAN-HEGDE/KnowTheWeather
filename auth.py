from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .model import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email').lower()
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # retrieve the user data with the email 
    user = User.query.filter_by(email=email).first()

    # check if the user exists and compare the hashed passwords
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # if user exist and credentials are correct, authorize the user
    login_user(user, remember=remember)

    return redirect(url_for('app.index'))

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email').lower()
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')

    if password!=confirmPassword:
        flash("Passwords doesn't match")
        return redirect(url_for('auth.register'))

    # retrieve the user data with the email 
    user = User.query.filter_by(email=email).first() 

    # if a user already exists, we want to redirect back to signup page so user can try again
    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.register'))

    # create a new user, hash the password before saving to the db
    new_user = User(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully Logged-out")
    return redirect(url_for('auth.login'))