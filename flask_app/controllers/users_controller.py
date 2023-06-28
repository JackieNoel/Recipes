from flask import Flask, render_template, request, session, redirect
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash("You must be logged in to access this page!")
        return redirect('/login')
    data = {
        'users_id': session['user_id']
    }
    return render_template('dashboard.html', user=User.show_one_user(session['user_id']), all_recipes=User.get_user_with_recipes(data))

@app.route('/registration', methods=['post'])
def registration():
    if not User.user_validator(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login_form', methods=['post'])
def login_form():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("The email or password is incorrect!")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("The email or password is incorrect!")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/edit_user_profile/<int:user_id>')
def edit_profile(user_id):
    print(user_id)
    return render_template('edit_profile.html', one_user=User.show_one_user(user_id))

# @app.route('update_user/<int:student_id>', methods=['post'])
# def update_profile()

#ADD EDIT PROFILE ROUTE TO POST NEW DATA !


@app.route('/logout')
def clear_session():
    session.clear()
    return redirect('/login')