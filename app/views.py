from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, lm
from .forms import LoginForm
from .model import User


@lm.user_loader
def user_loader(id):
    return User.query.get(id)

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        #print form.data['user_name']
        #user_id = User.query.get(form.data['user_name'])
        user = User.query.filter_by(email=form.data['user_name']).first()
        if user is None:
            email_addr = form.data['user_name']
            nickname_str = email_addr.split('@')[0]
            user = User(nickname=nickname_str, email=email_addr)
            db.session.add(user)
            db.session.commit()
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))