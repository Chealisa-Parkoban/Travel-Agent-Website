import os

# Find the absolute path that this file (config.py) lives
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Get secret key from teh computer, if not found using a random string that can be never guessed
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsuidvnaliewhbqbvbqi'

    # recaptcha key from Google
    # Used to verify that it is a robotic operation at the time of registration
    RECAPTCHA_PUBLIC_KEY = '6LfcGYMiAAAAAF0xYtR-31AbVwL-nIB8b-CXbZNc'
    RECAPTCHA_PRIVATE_KEY = '6LfcGYMiAAAAAHRo-w4lCiI7Ow5pqv7WWxGUmYdQ'

    # If there are an environment variable called 'DATABASE_URL', then use it.
    # If not, use the string to find the default database.
    # If the default database is not found, create it.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'brainmaker.db')

    # SQLALCHEMY_BINDS = True
    # Do not track all the modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False