#!/usr/bin/env python

import csv, sys
from monitores import app, db
from monitores.models import Monitor

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        monitor_id = row[0]
        brand = row[2]
        serial = row[3]
        specs = row[6].decode('utf-8')
        monitor = Monitor(id=monitor_id, brand=brand, serial=serial, specs=specs )
        print monitor
        db.session.add(monitor)
    db.session.commit()

