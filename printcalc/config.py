from os import environ

# Application version
VERSION = '1.0.0'

# Server settings
HOST = environ.get('PRINTCALC_HOST', '0.0.0.0')
PORT = int(environ.get('PRINTCALC_PORT', 5000))

# Database settings
DATABASE = environ.get('PRINTCALC_DATABASE', 'sqlite.db')

# Application settings
DEBUG = environ.get('PRINTCALC_DEBUG', 'False').lower() == 'true'
SECRET_KEY = environ.get('PRINTCALC_SECRET_KEY', 'dev-key-change-in-production')

# Logging settings
LOG_LEVEL = environ.get('PRINTCALC_LOG_LEVEL', 'INFO')
LOG_FILE = environ.get('PRINTCALC_LOG_FILE', 'logs/printcalc.log') 