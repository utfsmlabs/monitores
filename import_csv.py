#!/usr/bin/env python

import csv, sys
from monitores import app, db
from monitores.models import Monitor

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        monitor = Monitor(id=row[0], brand=row[2], serial=row[3])
        print monitor
        db.session.add(monitor)
    db.session.commit()

