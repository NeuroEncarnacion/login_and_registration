from flask_app import app
from flask import request, render_template, redirect, session, flash
from flask_app.models.model_log_reg import User
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)


# login route
@app.route('/')          
def index():
    return render_template('/log_and_reg.html')


# Dashboard route
@app.route('/dashboard')
def users():
    user_data = {
        'id' : session['user_id']
    }
    user_sess = User.get_one(user_data)
    return render_template('dashboard.html', user = user_sess)


# New User Route
@app.route('/new_user', methods=['POST'])
def new_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password'],
    }
    valid = User.user_validation(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data['pw_hash'] = pw_hash
        user = User.save(data)
        session['user_id'] = user
        return redirect('/dashboard')
    return redirect('/')


# Login Route
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')