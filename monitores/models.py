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

# A word about users:
# In this particular implementation we have no table for users since they
# will be always be retrieved from LDAP. That's why all references to user, 
# in particular in lended_to fields shall be the dn of the user

from monitores import db

class Monitor(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  brand = db.Column(db.String(128), nullable=False)
  serial = db.Column(db.String(128), nullable=False)
  reserved_by = db.Column(db.String(256))

  def __repr__(self):
    return '<Monitor: %s(%s)>' % (self.brand, self.serial)

