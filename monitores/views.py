from datetime import datetime, timedelta
from functools import wraps
from flask import render_template, request, flash, redirect, url_for, session
from monitores import app, db, ldap
import forms
from models import Monitor

#####################################################################
# Login stuff (probably should have replaced it with flask-login)
#####################################################################


def requires_auth(require_admin=False):
    '''
    Decorator that checks wether the user is logged in and redirects
    to the login form if he isn't.

    :param require_admin: Whether it should block non-admin users
    '''
    #This function is called when a function is decorated with @requires_auth
    def decorator(f):
        @wraps(f)
        #This function is called whenever the original would've been called.
        def decorated(*args, **kwargs):
            if 'username' in session:
                if not require_admin or session['username'] in app.config['ADMINS']:
                    return f(*args, **kwargs)
            flash('This page requires login')
            return redirect(url_for('login'))
        return decorated
    return decorator

@app.context_processor
def user_processor():
    '''
    Makes the user name available to the templates
    '''
    u = None
    if 'username' in session:
        u = session['username']
    is_admin = u in app.config['ADMINS'] # I really need to start using flask-login
    return dict(username=u, user_is_admin=is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login Form
    '''

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
@requires_auth()
def index():
    monitores = Monitor.query.order_by('id').filter(
            db.or_(Monitor.reserved_by == None, Monitor.reserved_by == session['username']))
    return render_template('index.html', monitores=monitores)

@app.route('/reserve/<int:monitor_id>')
@requires_auth()
def reserve(monitor_id):
    '''
    Sets the reserved_by attribute to the logged user's username if it isn't
    reserved by anyone else
    '''
    #The lockmode causes a SELECT FOR UPDATE
    monitor = Monitor.query.with_lockmode('update').get_or_404(monitor_id)
    if monitor.reserved_by:
        flash('Monitor no disponible')
        return redirect(url_for('index'))

    monitor.reserved_by = session['username']
    db.session.add(monitor)
    db.session.commit()
    flash('Monitor reservado!')
    return redirect(url_for('index'))

@app.route('/reservations')
@requires_auth(require_admin=True)
def show_reservations():
    monitores = Monitor.query.order_by('id')
    return render_template('show_reservations.html', monitores=monitores)

