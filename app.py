#!/usr/bin/env python

# Copyright (C) 2012 Universidad Tecnica Federico Santa Maria
#
# This file is part of Monitores.
#
# Monitores is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Monitores is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Monitores.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, render_template, request, flash, redirect, url_for, 
        session)

import ldapUsers
import forms

class default_config:
    DEBUG = True
    LDAP_URI = 'ldap://localhost:3890'
    LDAP_SEARCH_ATTR = 'uid'
    LDAP_BASEDN = 'ou=inf,o=utfsm,c=cl'
    SECRET_KEY = 'development secret key'
    LOG_FILE = 'monitores.log'

app = Flask(__name__)
app.config.from_object(default_config)
app.config.from_envvar('MONITORES_SETTINGS', silent=True)
app.config.from_pyfile('config.py', silent=True)

ldap = ldapUsers.ldapConnection(app)

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

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')


def config_string():
    # returns the configuration in plain text
    s = ['%s = %s\n' % (k, v) for k, v in app.config.iteritems()]
    return ''.join(s)

if __name__ == '__main__':
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(app.config['LOG_FILE'],
                maxBytes = 1024 * 250, backupCount = 2)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
    app.logger.debug(config_string())
    app.run(host='0.0.0.0')

