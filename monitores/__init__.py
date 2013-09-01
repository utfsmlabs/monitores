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

from flask import (Flask, render_template, request, flash, redirect, url_for, 
        session)
from flask.ext.sqlalchemy import SQLAlchemy
import ldapUsers

class default_config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///asdf.db'
    LDAP_URI = 'ldap://localhost:3890'
    LDAP_SEARCH_ATTR = 'uid'
    LDAP_BASEDN = 'ou=inf,o=utfsm,c=cl'
    SECRET_KEY = 'development secret key'
    LOG_FILE = 'monitores.log'
    ADMINS = ['javier.aravena']

app = Flask(__name__.split('.')[0], instance_relative_config=True)
app.config.from_object(default_config)
app.config.from_envvar('MONITORES_SETTINGS', silent=True)
app.config.from_pyfile('config.py', silent=True)

db = SQLAlchemy(app)

ldap = ldapUsers.ldapConnection(app)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOG_FILE'],
            maxBytes = 1024 * 250, backupCount = 2)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

from monitores import views, models

