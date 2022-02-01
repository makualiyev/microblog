from email import header
import requests
from datetime import datetime
from app import app, db
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, request, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'WTF is that'
        },
        {
            'author' : {'username' : 'Lox'},
            'body' : 'Sosal clen do togo kak eto stalo mainstreamom'
        }
    ]
    return render_template("index.html", title='home', posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author" : user, "body" : "test post 1"},
        {"author" : user, "body" : "test post 2"}
    ]
    return render_template("user.html", user=user, posts=posts)

@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit profile", form=form)

@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following {}'.format(username))
    return redirect(url_for('user', username=username))

@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}'.format(username))
    return redirect(url_for('user', username=username))





# @app.route("/get_stocks", methods=["GET"])
# @login_required
# def get_stocks():
#     return requests.get(
#         url="https://api-seller.ozon.ru/v1/categories/tree",
#         headers={"Client-Id" : "79080", "Api-Key" : "83b2cb46-1cb7-49fb-b02e-e3a93641f384", "Content-Type" : "application/json"}
#     ).content
