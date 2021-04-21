#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/boolean-solver/")

from boolean_solver import app as application
application.secret_key = 'dantemazza42069'
