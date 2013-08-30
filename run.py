#!/usr/bin/env python
from monitores import app

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0') #You should use a firewall anyways.
