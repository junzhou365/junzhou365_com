#! /usr/bin/python

import sys
import logging
logging.basicConfig(Stream=sys.stderr)
sys.path.insert(0, '/var/www/junzhou365/junzhou365_com')

from manage import app as application
