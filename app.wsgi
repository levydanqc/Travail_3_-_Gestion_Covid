#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/gestion_covid/')
from app import app as application
application.secret_key = 'ubuntuserver'
