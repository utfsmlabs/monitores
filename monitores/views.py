from datetime import datetime, timedelta
from functools import wraps
from flask import render_template, request, flash, redirect, url_for, session
from monitores import app, db, ldap
import forms
from models import Monitor

#####################################################################
# Login stuff (probably should have replaced it with flask-login)
#####################################################################


def requires_auth(f):
    '''
    Decorator that checks wether the user is logged in and redirects
    to the login form if he isn't
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            flash('This page requires login')
            return redirect(url_for('login'))
    return decorated

@app.context_processor
def user_processor():
    '''
    Makes the user name available to the templates
    '''
    u = None
    if 'username' in session:
        u = session['username']
    return dict(username=u)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.loginForm(request.form)
    if request.method == 'POST' and form.validate():
        if ldap.search_and_auth(
                form.username.data, form.password.data):
            session['username'] = form.username.data
            return redirect(url_for('index'))
        else:
            flash('incorrect username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#####################################################################

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

